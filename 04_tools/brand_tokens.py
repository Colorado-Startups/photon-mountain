#!/usr/bin/env python3
"""brand_tokens.py: the single source of Photon Mountain's visual identity in code.

Every build script imports its colors, fonts, and type scale from here rather
than hardcoding them, so the locked identity has exactly one definition. The
canonical record is 01_doctrine/brand_identity.md. If this module and that
document disagree, the document wins and this module is the bug.

--self-test proves they agree: it re-reads the tokens block out of
brand_identity.md and compares it against the constants below, then confirms
every font file the type scale names is actually on disk. That makes palette
drift a test failure instead of a silent render. It also checks the gold
pairings, the STEPn type scale and --emit.

Standard library only, matching 04_tools/voice_lint.py.

Usage:
  from brand_tokens import COLOR, FONT, TYPE_STEP_REM, contrast_ratio
  python3 brand_tokens.py --self-test
  python3 brand_tokens.py --emit DIR   # writes DIR/tokens.json, DIR/tokens.css

Exit codes: 0 = tokens match the identity doc and fonts resolve, 1 = drift.
"""

import argparse
import importlib.util
import json
import os
import re
import sys

# ---------------------------------------------------------------- paths -----
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)
IDENTITY_DOC = os.path.join(ROOT, "01_doctrine", "brand_identity.md")
FONT_DIR = os.path.join(ROOT, "01_doctrine", "brand_assets", "fonts")

# --------------------------------------------------------------- palette ----
# Verbatim from the "Tokens for PT-6" block in brand_identity.md.
# Colorado AI carryover (turquoise, pine green, flag gold) is prohibited.
COLOR_SUMMIT_NIGHT = "#131A33"
COLOR_SNOWFIELD = "#F6F7FB"
COLOR_WHITE = "#FFFFFF"
COLOR_GRANITE = "#545B6B"
COLOR_ALPENGLOW = "#FF5A36"
COLOR_ALPENGLOW_DEEP = "#C43C1C"
COLOR_LASER_VIOLET = "#7B5CFF"
COLOR_VIOLET_BRIGHT = "#8F75FF"
COLOR_VIOLET_DEEP = "#5636D6"
COLOR_DAWN_TINT = "#FFE9E2"
COLOR_GOLD = "#F2B233"
COLOR_GOLD_DEEP = "#8A6212"
COLOR_GOLD_TINT = "#FFF3D6"

COLOR = {
    "summit_night": COLOR_SUMMIT_NIGHT,
    "snowfield": COLOR_SNOWFIELD,
    "white": COLOR_WHITE,
    "granite": COLOR_GRANITE,
    "alpenglow": COLOR_ALPENGLOW,
    "alpenglow_deep": COLOR_ALPENGLOW_DEEP,
    "laser_violet": COLOR_LASER_VIOLET,
    "violet_bright": COLOR_VIOLET_BRIGHT,
    "violet_deep": COLOR_VIOLET_DEEP,
    "dawn_tint": COLOR_DAWN_TINT,
    "gold": COLOR_GOLD,
    "gold_deep": COLOR_GOLD_DEEP,
    "gold_tint": COLOR_GOLD_TINT,
}

def mix(a, b, t):
    """Blend two #RRGGBB colors in sRGB. t=0 returns a, t=1 returns b."""
    a, b = a.lstrip("#"), b.lstrip("#")
    out = []
    for i in (0, 2, 4):
        ca, cb = int(a[i:i + 2], 16), int(b[i:i + 2], 16)
        out.append(round(ca + (cb - ca) * t))
    return "#%02X%02X%02X" % tuple(out)


# Derived neutrals. The locked palette deliberately has no mid-tones, but the
# build scripts need hairline rules and dimmed text on dark panels. Deriving
# them from palette colors keeps one source of truth instead of introducing
# off-palette hexes. Every on-dark value below is contrast-checked in
# self_test(), so a palette edit that breaks AA fails the test.
COLOR_RULE_HAIRLINE = mix(COLOR_GRANITE, COLOR_WHITE, 0.78)
COLOR_TEXT_DIM_ON_DARK = mix(COLOR_WHITE, COLOR_SUMMIT_NIGHT, 0.30)
COLOR_TEXT_SECONDARY_ON_DARK = mix(COLOR_WHITE, COLOR_SUMMIT_NIGHT, 0.18)

# Semantic roles, from the Role column of the palette table. Build scripts
# should reach for these rather than raw color names, so a layout says what a
# value is for instead of what it looks like.
ROLE = {
    "text_primary": COLOR_SUMMIT_NIGHT,      # body text on light
    "text_secondary": COLOR_GRANITE,         # captions, rules
    "text_on_dark": COLOR_WHITE,
    "surface_dark": COLOR_SUMMIT_NIGHT,
    "surface_light": COLOR_SNOWFIELD,
    "surface_paper": COLOR_WHITE,
    "surface_tint": COLOR_DAWN_TINT,
    "accent": COLOR_ALPENGLOW,               # graphic use on light
    "accent_text_on_light": COLOR_ALPENGLOW_DEEP,
    "accent_text_on_dark": COLOR_ALPENGLOW,
    "accent2": COLOR_LASER_VIOLET,           # data, links, secondary highlights
    "accent2_text_on_light": COLOR_VIOLET_DEEP,
    "accent2_text_on_dark": COLOR_VIOLET_BRIGHT,
    "accent3": COLOR_GOLD,                   # graphic only: fills, rules, marks
    "accent3_text_on_light": COLOR_GOLD_DEEP,
    "surface_tint_gold": COLOR_GOLD_TINT,
    "rule": COLOR_GRANITE,
    "rule_hairline": COLOR_RULE_HAIRLINE,
    "text_dim_on_dark": COLOR_TEXT_DIM_ON_DARK,
    "text_secondary_on_dark": COLOR_TEXT_SECONDARY_ON_DARK,
}

# Colors that must never carry body text (brand_identity.md: "Never set body
# text in an accent color"). Used by the self-test and available to callers.
ACCENT_COLORS = frozenset({
    COLOR_ALPENGLOW, COLOR_LASER_VIOLET, COLOR_VIOLET_BRIGHT,
    COLOR_ALPENGLOW_DEEP, COLOR_VIOLET_DEEP, COLOR_GOLD, COLOR_GOLD_DEEP,
})

# Colors that carry no text at any size, on any ground (Paul, 2026-11-16:
# gold is graphic only). check_pairing refuses them unless graphic=True.
GRAPHIC_ONLY = frozenset({COLOR_GOLD})

# ------------------------------------------------------------------ type ----
FONT_DISPLAY = "Space Grotesk"   # Google Fonts, OFL
FONT_BODY = "Inter"              # Google Fonts, OFL
FONT_MONO = "Space Mono"         # Google Fonts, OFL

# Role -> (family, weight, filename). Exactly the weights the Typography table
# names; see 01_doctrine/brand_assets/fonts/README.md for how they were cut.
FONT = {
    "display_medium": (FONT_DISPLAY, 500, "SpaceGrotesk-Medium.ttf"),
    "display_bold": (FONT_DISPLAY, 700, "SpaceGrotesk-Bold.ttf"),
    "body_regular": (FONT_BODY, 400, "Inter-Regular.ttf"),
    "body_medium": (FONT_BODY, 500, "Inter-Medium.ttf"),
    "body_semibold": (FONT_BODY, 600, "Inter-SemiBold.ttf"),
    "mono_regular": (FONT_MONO, 400, "SpaceMono-Regular.ttf"),
    "mono_bold": (FONT_MONO, 700, "SpaceMono-Bold.ttf"),
}

# Print points, from "Type scale for PT-6" in brand_identity.md.
TYPE_SCALE_PRINT = {
    "display_min": 40, "display_max": 64,
    "headline_min": 24, "headline_max": 32,
    "body_min": 10.5, "body_max": 12,
}
TYPE_SCALE_WEB_BODY = (16, 18)  # px

# Web type scale in rem (1rem = 16 px), the STEPn lines of the tokens block in
# brand_identity.md. Every step lands inside a web range that doc names.
TYPE_STEP_REM = {
    "step0": 0.875,  # caption, 14 px
    "step1": 1.0,    # body, 16 px
    "step2": 1.125,  # body, 18 px
    "step3": 1.5,    # headline, 24 px
    "step4": 2.0,    # headline, 32 px
    "step5": 2.5,    # display, 40 px
    "step6": 3.0,    # display, 48 px
    "step7": 4.0,    # display, 64 px
}
TYPE_RANGES_WEB_PX = {"caption": (14, 14), "body": TYPE_SCALE_WEB_BODY,
                      "headline": (24, 32), "display": (40, 64)}

# The wordmark: "Photon Mountain" in Space Grotesk Medium, tracking a touch
# tighter than default. PT-6 picks the exact value when the wordmark is cut.
WORDMARK_FONT = FONT["display_medium"]
WORDMARK_TRACKING_EM = -0.01

# ----------------------------------------------------------------- marks ----
MARK_SUMMIT_SUN = os.path.join(ROOT, "01_doctrine", "brand_assets",
                               "concept_d_summit_sun.svg")
MARK_SUMMIT_SUN_ONECOLOR = os.path.join(ROOT, "01_doctrine", "brand_assets",
                                        "summit_sun_mark_onecolor.svg")


# ------------------------------------------------------------- functions ----
def font_path(role):
    """Absolute path to the TTF for a FONT role. Raises if the role is unknown."""
    try:
        _family, _weight, filename = FONT[role]
    except KeyError:
        raise KeyError("unknown font role %r; known roles: %s"
                       % (role, ", ".join(sorted(FONT)))) from None
    return os.path.join(FONT_DIR, filename)


def _srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color):
    """WCAG 2.1 relative luminance for a #RRGGBB string."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (0.2126 * _srgb_to_linear(r)
            + 0.7152 * _srgb_to_linear(g)
            + 0.0722 * _srgb_to_linear(b))


def contrast_ratio(fg, bg):
    """WCAG 2.1 contrast ratio between two #RRGGBB colors. 1.0 to 21.0."""
    a, b = relative_luminance(fg), relative_luminance(bg)
    lo, hi = sorted((a, b))
    return (hi + 0.05) / (lo + 0.05)


class ContrastError(AssertionError):
    """A color pairing that would render below WCAG AA."""


# --- The accessibility gate --------------------------------------------------
# brand_identity.md computes every pairing and sorts them into AA body text,
# AA large-text-only, and never-body-text. This is where that becomes
# enforceable instead of advisory.
#
# Policy, decided by Paul 2026-09-21: raise. A build that would emit an
# inaccessible pairing fails outright rather than rendering something the
# corridor then has to defend. The decision came straight out of a real bug
# the same day: the infographic's core-city captions were set in the on-light
# violet over a Summit Night panel, which scores 2.37 against that ground.
# It looked plausible and was unreadable. A deliberate exception passes
# large=True, which is WCAG's 3.0 allowance for text at or above 18pt
# regular / 14pt bold, and is what makes Alpenglow on White legal for a
# headline but never for body copy.
def check_pairing(fg, bg, large=False, where="", graphic=False):
    """Assert a foreground/background pairing clears WCAG AA.

    fg, bg  -- #RRGGBB strings, ideally from ROLE
    large   -- True for text at or above 18pt regular / 14pt bold
    where   -- optional caller label, quoted back in the error
    graphic -- True for a non-text mark (icon, rule, chart mark), held to
               WCAG's 3.0 non-text floor; the only use a GRAPHIC_ONLY color gets

    Returns True, or raises ContrastError.
    """
    label = "%s: " % where if where else ""
    if fg.upper() in GRAPHIC_ONLY and not graphic:
        raise ContrastError("%s%s is graphic only; gold text uses Gold Deep."
                            % (label, fg))
    threshold = 3.0 if (large or graphic) else 4.5
    ratio = contrast_ratio(fg, bg)
    if ratio < threshold:
        raise ContrastError(
            "%s%s on %s scores %.2f, below the WCAG AA floor of %.1f for %s. "
            "Pick the on-dark or on-light variant of this role in "
            "brand_identity.md, or pass large=True if this really is display "
            "type." % (label, fg, bg, ratio, threshold, "graphics" if graphic
                       else "large text" if large else "body text"))
    return True


def emit(out_dir):
    """Write tokens.json and tokens.css into out_dir. Same tokens, same bytes."""
    color = dict(COLOR, rule_hairline=COLOR_RULE_HAIRLINE,
                 text_dim_on_dark=COLOR_TEXT_DIM_ON_DARK,
                 text_secondary_on_dark=COLOR_TEXT_SECONDARY_ON_DARK)
    tokens = {"color": dict(sorted(color.items())),
              "type": {k: "%grem" % v for k, v in TYPE_STEP_REM.items()}}
    css = ["/* Generated by 04_tools/brand_tokens.py --emit. Do not edit. */",
           ":root {"]
    css += ["  --color-%s: %s;" % (k.replace("_", "-"), v)
            for k, v in tokens["color"].items()]
    css += ["  --%s: %s;" % kv for kv in tokens["type"].items()]
    os.makedirs(out_dir, exist_ok=True)
    for name, body in (("tokens.json", json.dumps(tokens, indent=2)),
                       ("tokens.css", "\n".join(css + ["}"]))):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8",
                  newline="\n") as f:
            f.write(body + "\n")
    return tokens


# ----------------------------------------------------------------- tests ----
def tokens_from_identity_doc():
    """Re-read the COLOR_* block out of brand_identity.md."""
    if not os.path.isfile(IDENTITY_DOC):
        return None, "identity doc not found at %s" % IDENTITY_DOC
    text = open(IDENTITY_DOC, encoding="utf-8").read()
    found = dict(re.findall(r"^(COLOR_[A-Z_]+)\s*=\s*\"(#[0-9A-Fa-f]{6})\"",
                            text, re.M))
    if not found:
        return None, "no COLOR_* token block found in the identity doc"
    return found, None


def self_test():
    """Run brand_tokens_selftest.py, loaded by path so it works under python3 -I."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand_tokens_selftest.py")
    spec = importlib.util.spec_from_file_location("brand_tokens_selftest", path)
    checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checks)
    return checks.run(sys.modules[__name__])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Photon Mountain brand tokens")
    parser.add_argument("--self-test", action="store_true",
                        help="verify the tokens against brand_identity.md")
    parser.add_argument("--emit", metavar="DIR",
                        help="write tokens.json and tokens.css into DIR")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.emit:
        emit(args.emit)
        print("wrote tokens.json and tokens.css to %s" % args.emit)
        return 0
    for name, value in sorted(COLOR.items()):
        print("%-16s %s" % (name, value))
    print()
    for role in sorted(FONT):
        family, weight, filename = FONT[role]
        print("%-16s %s %d  %s" % (role, family, weight, filename))
    return 0


if __name__ == "__main__":
    sys.exit(main())
