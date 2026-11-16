"""The --self-test of brand_tokens.py, one small check per rule.

brand_tokens.py loads this file by path and passes itself in as `bt`, so the
checks read the running module's tokens and the self-test works under
`python3 -I`, which keeps the script's folder off sys.path. Each check returns
(failures, ok_line): an empty failure list prints "self-test: <ok_line>: OK".
Standard library only.
"""

import json
import os
import re
import tempfile

# Derived neutrals are computed from the palette, not declared in the doc, so
# they are checked by contrast rather than by name.
DERIVED = {"COLOR_RULE_HAIRLINE", "COLOR_TEXT_DIM_ON_DARK", "COLOR_TEXT_SECONDARY_ON_DARK"}


def check_palette(bt, declared):
    mine = {k: v for k, v in vars(bt).items()
            if k.startswith("COLOR_") and isinstance(v, str) and k not in DERIVED}
    fails = []
    missing = sorted(set(declared) - set(mine))
    extra = sorted(set(mine) - set(declared))
    if missing:
        fails.append("in the identity doc but not this module: %s" % ", ".join(missing))
    if extra:
        fails.append("in this module but not the identity doc: %s" % ", ".join(extra))
    fails += ["%s doc=%s module=%s" % (k, declared[k], mine[k])
              for k in sorted(set(declared) & set(mine))
              if declared[k].upper() != mine[k].upper()]
    return fails, "%d palette tokens match the identity doc" % len(declared)


def check_fonts(bt, _):
    """Every font the type scale names must resolve."""
    absent = [f for f in map(bt.font_path, bt.FONT) if not os.path.isfile(f)]
    return (["missing font %s" % os.path.basename(f) for f in absent],
            "%d font files resolve" % len(bt.FONT))


def check_contrast(bt, _):
    """The contrast figures brand_identity.md states, re-derived here."""
    expected = [
        (bt.COLOR_SUMMIT_NIGHT, bt.COLOR_WHITE, 17.2),
        (bt.COLOR_SUMMIT_NIGHT, bt.COLOR_SNOWFIELD, 16.0),
        (bt.COLOR_GRANITE, bt.COLOR_WHITE, 6.8),
        (bt.COLOR_WHITE, bt.COLOR_SUMMIT_NIGHT, 17.2),
        (bt.COLOR_ALPENGLOW, bt.COLOR_SUMMIT_NIGHT, 5.5),
        (bt.COLOR_ALPENGLOW_DEEP, bt.COLOR_WHITE, 5.2),
        (bt.COLOR_VIOLET_DEEP, bt.COLOR_WHITE, 7.3),
        (bt.COLOR_GOLD, bt.COLOR_SUMMIT_NIGHT, 9.2),
        (bt.COLOR_GOLD_DEEP, bt.COLOR_WHITE, 5.5),
        (bt.COLOR_GOLD_DEEP, bt.COLOR_SNOWFIELD, 5.1),
    ]
    fails = ["contrast %s on %s doc=%.1f computed=%.1f" % (f, b, e, bt.contrast_ratio(f, b))
             for f, b, e in expected if abs(bt.contrast_ratio(f, b) - e) > 0.1]
    return fails, "%d contrast ratios match the identity doc" % len(expected)


def check_derived(bt, _):
    """Derived on-dark neutrals must still clear AA against Summit Night."""
    checks = [("text_dim_on_dark", bt.COLOR_TEXT_DIM_ON_DARK, 4.5),
              ("text_secondary_on_dark", bt.COLOR_TEXT_SECONDARY_ON_DARK, 4.5)]
    fails = ["derived %s contrast %.1f below AA %.1f" % (n, bt.contrast_ratio(fg, bt.COLOR_SUMMIT_NIGHT), floor)
             for n, fg, floor in checks if bt.contrast_ratio(fg, bt.COLOR_SUMMIT_NIGHT) < floor]
    return fails, "%d derived on-dark neutrals clear AA" % len(checks)


def check_hairline(bt, _):
    """The hairline rule stays visibly lighter than Granite without vanishing into white."""
    ratio = bt.contrast_ratio(bt.COLOR_RULE_HAIRLINE, bt.COLOR_WHITE)
    fails = [] if 1.05 <= ratio <= 2.0 else ["hairline rule contrast %.2f outside 1.05-2.00" % ratio]
    return fails, "hairline rule reads on white (%.2f)" % ratio


def check_gate(bt, _):
    """The gate must bite. The failing case is the real one found on 2026-09-21:
    on-light violet over a Summit Night panel, at 2.37."""
    try:
        bt.check_pairing(bt.COLOR_VIOLET_DEEP, bt.COLOR_SUMMIT_NIGHT, where="self-test")
        return ["contrast gate did NOT raise on violet-deep over summit-night"], ""
    except bt.ContrastError:
        pass
    try:
        bt.check_pairing(bt.COLOR_VIOLET_BRIGHT, bt.COLOR_SUMMIT_NIGHT)
        bt.check_pairing(bt.COLOR_ALPENGLOW, bt.COLOR_WHITE, large=True)
    except bt.ContrastError as exc:
        return ["gate rejected a valid pairing (%s)" % exc], ""
    return [], "contrast gate raises on the known-bad pairing and passes the good ones"


def check_body_roles(bt, _):
    """No accent color may be offered as a body-text role."""
    leaked = sorted(r for r in ("text_primary", "text_secondary", "text_on_dark")
                    if bt.ROLE[r] in bt.ACCENT_COLORS)
    fails = ["accent color used for body text role(s) %s" % ", ".join(leaked)] if leaked else []
    return fails, "no accent color in a body-text role"


def check_gold(bt, _):
    """Every gold pairing the identity doc allows passes the gate, and gold text is
    refused even where its ratio would clear AA (9.2 on Summit Night)."""
    pairs = [(bt.COLOR_GOLD_DEEP, bt.COLOR_SNOWFIELD, False),
             (bt.COLOR_GOLD_DEEP, bt.COLOR_WHITE, False),
             (bt.COLOR_GOLD_DEEP, bt.COLOR_GOLD_TINT, False),
             (bt.COLOR_SUMMIT_NIGHT, bt.COLOR_GOLD_TINT, False),
             (bt.COLOR_GOLD, bt.COLOR_SUMMIT_NIGHT, True)]

    def refusal(fg, bg, graphic=False):
        try:
            bt.check_pairing(fg, bg, where="gold", graphic=graphic)
            return None
        except bt.ContrastError as exc:
            return str(exc)
    fails = [m for m in (refusal(*p) for p in pairs) if m]
    if not refusal(bt.COLOR_GOLD, bt.COLOR_SUMMIT_NIGHT):
        fails.append("the gate let Gold carry text")
    return fails, "%d gold pairings pass the gate, gold text is refused" % len(pairs)


def check_type_scale(bt, _):
    """The doc's STEPn lines match, steps ascend, and each lands inside a web range the doc names."""
    doc = open(bt.IDENTITY_DOC, encoding="utf-8").read()
    doc_steps = {k.lower(): float(v) for k, v in re.findall(r"^(STEP\d+)\s*=\s*([0-9.]+)", doc, re.M)}
    steps = list(bt.TYPE_STEP_REM.values())
    in_range = all(any(lo <= s * 16 <= hi for lo, hi in bt.TYPE_RANGES_WEB_PX.values()) for s in steps)
    good = doc_steps == bt.TYPE_STEP_REM and steps == sorted(set(steps)) and in_range
    fails = [] if good else ["type scale differs from the doc, repeats a step or leaves the doc's ranges"]
    return fails, "%d type steps match the doc and its ranges" % len(steps)


def check_emit(bt, _):
    """--emit: both files carry this module's tokens, and a rerun is identical."""
    with tempfile.TemporaryDirectory() as tmp:
        runs = []
        for _ in range(2):
            bt.emit(tmp)
            runs.append([open(os.path.join(tmp, n), encoding="utf-8").read() for n in ("tokens.json", "tokens.css")])
    js = json.loads(runs[0][0])
    css = dict(re.findall(r"--([a-z0-9-]+): ([^;]+);", runs[0][1]))
    want_css = {"color-" + k.replace("_", "-"): v for k, v in js["color"].items()}
    want_css.update(js["type"])
    good = (set(js) == {"color", "type"} and runs[0] == runs[1] and css == want_css
            and all(js["color"].get(k) == v for k, v in bt.COLOR.items())
            and list(js["type"]) == list(bt.TYPE_STEP_REM))
    fails = [] if good else ["--emit output drifts from the module"]
    return fails, "--emit writes %d colors and %d type steps, twice the same" % (len(js["color"]), len(js["type"]))


CHECKS = [check_palette, check_fonts, check_contrast, check_derived, check_hairline,
          check_gate, check_body_roles, check_gold, check_type_scale, check_emit]


def run(bt):
    declared, err = bt.tokens_from_identity_doc()
    if err:
        print("self-test: %s: FAIL" % err)
        return 1
    ok = True
    for check in CHECKS:
        fails, ok_line = check(bt, declared)
        for f in fails:
            print("self-test: %s: FAIL" % f)
        if not fails:
            print("self-test: %s: OK" % ok_line)
        ok = ok and not fails
    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1
