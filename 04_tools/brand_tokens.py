#!/usr/bin/env python3
"""brand_tokens.py: the single source of Photon Mountain's visual identity in code.

Every build script imports its colors, fonts, and type scale from here rather
than hardcoding them, so the locked identity has exactly one definition. The
canonical record is 01_doctrine/brand_identity.md. If this module and that
document disagree, the document wins and this module is the bug.

--self-test proves they agree: it re-reads the tokens block out of
brand_identity.md and compares it against the constants below, then confirms
every font file the type scale names is actually on disk. That makes palette
drift a test failure instead of a silent render.

Standard library only, matching 04_tools/voice_lint.py.

Usage:
  from brand_tokens import COLOR, FONT, contrast_ratio
  python3 brand_tokens.py --self-test

Exit codes: 0 = tokens match the identity doc and fonts resolve, 1 = drift.
"""

import argparse
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
    "rule": COLOR_GRANITE,
    "rule_hairline": COLOR_RULE_HAIRLINE,
    "text_dim_on_dark": COLOR_TEXT_DIM_ON_DARK,
    "text_secondary_on_dark": COLOR_TEXT_SECONDARY_ON_DARK,
}

# Colors that must never carry body text (brand_identity.md: "Never set body
# text in an accent color"). Used by the self-test and available to callers.
ACCENT_COLORS = frozenset({
    COLOR_ALPENGLOW, COLOR_LASER_VIOLET, COLOR_VIOLET_BRIGHT,
    COLOR_ALPENGLOW_DEEP, COLOR_VIOLET_DEEP,
})

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
def check_pairing(fg, bg, large=False, where=""):
    """Assert a foreground/background pairing clears WCAG AA.

    fg, bg  -- #RRGGBB strings, ideally from ROLE
    large   -- True for text at or above 18pt regular / 14pt bold
    where   -- optional caller label, quoted back in the error

    Returns True, or raises ContrastError.
    """
    threshold = 3.0 if large else 4.5
    ratio = contrast_ratio(fg, bg)
    if ratio < threshold:
        raise ContrastError(
            "%s%s on %s scores %.2f, below the WCAG AA floor of %.1f for %s "
            "text. Pick the on-dark or on-light variant of this role in "
            "brand_identity.md, or pass large=True if this really is display "
            "type." % ("%s: " % where if where else "", fg, bg, ratio,
                       threshold, "large" if large else "body"))
    return True


# ----------------------------------------------------------------- tests ----
def _tokens_from_identity_doc():
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
    ok = True

    declared, err = _tokens_from_identity_doc()
    if err:
        print("self-test: %s: FAIL" % err)
        return 1

    # Derived neutrals are computed from the palette, not declared in the doc,
    # so they are checked by contrast below rather than by name comparison.
    derived = {"COLOR_RULE_HAIRLINE", "COLOR_TEXT_DIM_ON_DARK",
               "COLOR_TEXT_SECONDARY_ON_DARK"}
    mine = {k: v for k, v in globals().items()
            if k.startswith("COLOR_") and isinstance(v, str)
            and k not in derived}

    missing = sorted(set(declared) - set(mine))
    extra = sorted(set(mine) - set(declared))
    drifted = sorted(k for k in set(declared) & set(mine)
                     if declared[k].upper() != mine[k].upper())

    if missing:
        ok = False
        print("self-test: in the identity doc but not this module: %s: FAIL"
              % ", ".join(missing))
    if extra:
        ok = False
        print("self-test: in this module but not the identity doc: %s: FAIL"
              % ", ".join(extra))
    for k in drifted:
        ok = False
        print("self-test: %s doc=%s module=%s: FAIL" % (k, declared[k], mine[k]))
    if not (missing or extra or drifted):
        print("self-test: %d palette tokens match the identity doc: OK"
              % len(declared))

    # Every font the type scale names must actually resolve.
    absent = [f for role in FONT
              for f in [font_path(role)] if not os.path.isfile(f)]
    if absent:
        ok = False
        for f in absent:
            print("self-test: missing font %s: FAIL" % os.path.basename(f))
    else:
        print("self-test: %d font files resolve: OK" % len(FONT))

    # The contrast figures brand_identity.md states, re-derived here. If the
    # palette is edited without re-checking contrast, this catches it.
    expected = [
        (COLOR_SUMMIT_NIGHT, COLOR_WHITE, 17.2),
        (COLOR_SUMMIT_NIGHT, COLOR_SNOWFIELD, 16.0),
        (COLOR_GRANITE, COLOR_WHITE, 6.8),
        (COLOR_WHITE, COLOR_SUMMIT_NIGHT, 17.2),
        (COLOR_ALPENGLOW, COLOR_SUMMIT_NIGHT, 5.5),
        (COLOR_ALPENGLOW_DEEP, COLOR_WHITE, 5.2),
        (COLOR_VIOLET_DEEP, COLOR_WHITE, 7.3),
    ]
    bad = [(f, b, e, contrast_ratio(f, b)) for f, b, e in expected
           if abs(contrast_ratio(f, b) - e) > 0.1]
    if bad:
        ok = False
        for f, b, e, got in bad:
            print("self-test: contrast %s on %s doc=%.1f computed=%.1f: FAIL"
                  % (f, b, e, got))
    else:
        print("self-test: %d contrast ratios match the identity doc: OK"
              % len(expected))

    # Derived on-dark neutrals must still clear AA against Summit Night, and
    # the hairline rule must stay visibly lighter than Granite without
    # vanishing into white.
    derived_checks = [
        ("text_dim_on_dark", COLOR_TEXT_DIM_ON_DARK, COLOR_SUMMIT_NIGHT, 4.5),
        ("text_secondary_on_dark", COLOR_TEXT_SECONDARY_ON_DARK,
         COLOR_SUMMIT_NIGHT, 4.5),
    ]
    failed = [(n, contrast_ratio(fg, bg), floor)
              for n, fg, bg, floor in derived_checks
              if contrast_ratio(fg, bg) < floor]
    if failed:
        ok = False
        for n, got, floor in failed:
            print("self-test: derived %s contrast %.1f below AA %.1f: FAIL"
                  % (n, got, floor))
    else:
        print("self-test: %d derived on-dark neutrals clear AA: OK"
              % len(derived_checks))

    hairline_vs_white = contrast_ratio(COLOR_RULE_HAIRLINE, COLOR_WHITE)
    if not 1.05 <= hairline_vs_white <= 2.0:
        ok = False
        print("self-test: hairline rule contrast %.2f outside 1.05-2.00: FAIL"
              % hairline_vs_white)
    else:
        print("self-test: hairline rule reads on white (%.2f): OK"
              % hairline_vs_white)

    # The gate must actually bite. The failing case is the real one found on
    # 2026-09-21: on-light violet over a Summit Night panel, at 2.37.
    try:
        check_pairing(COLOR_VIOLET_DEEP, COLOR_SUMMIT_NIGHT, where="self-test")
    except ContrastError:
        try:
            check_pairing(COLOR_VIOLET_BRIGHT, COLOR_SUMMIT_NIGHT)
            check_pairing(COLOR_ALPENGLOW, COLOR_WHITE, large=True)
            print("self-test: contrast gate raises on the known-bad pairing "
                  "and passes the good ones: OK")
        except ContrastError as exc:
            ok = False
            print("self-test: gate rejected a valid pairing (%s): FAIL" % exc)
    else:
        ok = False
        print("self-test: contrast gate did NOT raise on violet-deep over "
              "summit-night: FAIL")

    # No accent color may be offered as a body-text role.
    leaked = sorted(r for r in ("text_primary", "text_secondary", "text_on_dark")
                    if ROLE[r] in ACCENT_COLORS)
    if leaked:
        ok = False
        print("self-test: accent color used for body text role(s) %s: FAIL"
              % ", ".join(leaked))
    else:
        print("self-test: no accent color in a body-text role: OK")

    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="Photon Mountain brand tokens")
    parser.add_argument("--self-test", action="store_true",
                        help="verify the tokens against brand_identity.md")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    for name, value in sorted(COLOR.items()):
        print("%-16s %s" % (name, value))
    print()
    for role in sorted(FONT):
        family, weight, filename = FONT[role]
        print("%-16s %s %d  %s" % (role, family, weight, filename))
    return 0


if __name__ == "__main__":
    sys.exit(main())
