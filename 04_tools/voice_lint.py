#!/usr/bin/env python3
"""voice_lint.py: the generic half of a prose voice check.

Canonical source: Claude-OS/tools/voice_lint.py. Synced into each repo,
where it is the one definition behind every call site:

  1. The agent surface, either a tool-use hook that fires on each edit
     or a slash command someone runs. These are not the same thing and
     a repo should say which one it has.
  2. The pre-commit hook, on staged files.
  3. CI, on files changed in a pull request.

CI shells out to the same script rather than reimplementing the check,
so the gate cannot drift between a laptop, a web edit, and a cloud agent.

This file holds only checks that are true for any writing project. Project
doctrine (banned terms, stale figures, named people, retired addresses,
brand tokens) never goes in here. It goes in a rules file the project owns
and passes with --rules.

Built-in checks:
  em-dash              FAIL  Any em dash (U+2014).
  spaced-en-dash       FAIL  " - " styled en dash (U+2013). It reads as an
                             em dash, so it is out too.
  sentence-length      WARN  Sentence longer than max_words (default 30).
  hedge-word           WARN  Hedging that fights plain and direct.
  ai-tell              WARN  Phrasing that reads as machine-written.
  unattributed-figure  WARN  A money amount, percentage, comma-grouped
                             number, magnitude, or counted quantity in a
                             sentence with no attribution cue and no goal
                             label. A heuristic: it flags candidates for
                             human review, so it warns. An attributed
                             figure the regex misses is a false positive
                             to wave through, not a rule change.

Defaults follow ~/.claude/rules/writing-and-gates.md: block on the certain,
warn on the likely. The two dash checks are literal character tests, so
they block. The rest are heuristics, so they warn. A project that wants a
different grade sets it in its rules file, for example
"severity": {"unattributed-figure": "FAIL"}.

Skipped: fenced code blocks, inline code spans, and URLs.

Rules file (JSON, all keys optional):
  {
    "max_words": 30,
    "hedge_words": ["as it were"],
    "attribution_cues": ["per the 2026 filing"],
    "figure_nouns": ["megawatts"],
    "severity": {"sentence-length": "off", "ai-tell": "FAIL"},
    "patterns": [
      {"id": "banned-term", "severity": "FAIL",
       "regex": "\\\\bsynergy\\\\b", "message": "say what actually happens"}
    ]
  }

Project patterns add to the built-ins, they never replace them. Severity
accepts FAIL, WARN, or off. Requires Python 3.9, standard library only.

Usage:
  python3 voice_lint.py FILE [FILE ...]
  python3 voice_lint.py --rules 01_doctrine/voice_rules.json FILE
  python3 voice_lint.py --max-words 35 FILE
  python3 voice_lint.py --self-test

Exit codes: 0 = no FAIL findings (warnings allowed), 1 = at least one
FAIL, 2 = usage, read, or rules error.
"""

import argparse
import json
import re
import sys

EM_DASH = "—"
EN_DASH = "–"

DEFAULT_MAX_WORDS = 30

HEDGE_WORDS = [
    "arguably", "probably", "perhaps", "maybe", "somewhat", "fairly",
    "rather", "quite", "relatively", "potentially", "seemingly",
    "appears to", "seems to", "could be", "might be", "may be",
    "sort of", "kind of", "more or less", "virtually", "essentially",
    "basically", "generally", "in some sense", "to some extent",
]

# Phrasing that reads as machine-written. Ported from the colorado-ai voice
# hook, where it is advisory. Advisory here too: WARN, not FAIL.
AI_TELLS = [
    (r"\bdelve\b", "write plainly: look at, dig into"),
    (r"\btapestry\b", "cut the spatial metaphor"),
    (r"\bplethora\b", "use many or a lot of"),
    (r"\bseamless(ly)?\b", "say what actually happens"),
    (r"\bgame[- ]changer\b", "name the specific change"),
    (r"\ba testament to\b", "state the fact directly"),
    (r"it(?:'|’)?s important to note|it is important to note",
     "just say the thing"),
    (r"in (today(?:'|’)?s|an?) (fast-paced|ever-evolving|rapidly evolving)",
     "cut the opener"),
    (r"navigat(e|ing) the complexit", "say what you do"),
    (r"look no further", "chatbot filler"),
    (r"^\s*(Certainly|Absolutely|Of course)[,!]", "start with the answer"),
    (r"(^|\s)(in conclusion|in summary|in essence)[,:]",
     "stop when you are done"),
    (r"it(?:'|’)?s not (just|only) .{1,60}, it(?:'|’)?s",
     "write the affirmative"),
]

# Nouns that make a bare number a countable claim worth attributing.
FIGURE_NOUNS = [
    "companies", "firms", "workers", "employees", "jobs", "students",
    "researchers", "startups", "acres", "megawatts", "gigawatts",
    "patents", "labs", "buildings",
]

# If any of these appear in the same sentence as a figure, the figure counts
# as attributed or labeled a goal.
ATTRIBUTION_CUES = [
    "according to", "per ", "source", "cite", "cites", "cited", "reports",
    "reported", "says", "said", "estimate", "estimates", "estimated",
    "announced", "association", "study", "survey", "census", "data from",
    "figures from", "goal", "target", "on the order of",
]

LINK_RE = re.compile(r"\[[^\]]*\]\([^)]+\)|https?://\S+")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")

# Default grade per built-in check. A rules file may regrade any of them.
# House rule: block on the certain, warn on the likely. The dash checks are
# literal character tests; everything else is a heuristic.
DEFAULT_SEVERITY = {
    "em-dash": "FAIL",
    "spaced-en-dash": "FAIL",
    "sentence-length": "WARN",
    "hedge-word": "WARN",
    "ai-tell": "WARN",
    "unattributed-figure": "WARN",
}
BUILTIN_CHECKS = tuple(DEFAULT_SEVERITY)
VALID_SEVERITIES = ("FAIL", "WARN", "off")


def build_figure_re(extra_nouns=()):
    nouns = "|".join(re.escape(n) for n in list(FIGURE_NOUNS) + list(extra_nouns))
    return re.compile(
        r"""
        (?:
            [$€£]\s?\d[\d,.]*                   # money
          | \d[\d,.]*\s?(?:%|\bpercent\b)                 # percentage
          | \b\d{1,3}(?:,\d{3})+\b                        # comma-grouped
          | \b\d[\d,.]*\s?(?:million|billion|trillion|thousand)\b
          | \b\d[\d,.]*\+?\s(?:[a-z-]+\s)?(?:""" + nouns + r""")\b
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )


# A hedge word that also starts a plain phrase gets a negative lookahead here,
# so the phrase never matches. "Rather than" is contrast, not hedging, and the
# house rules use it themselves; a bare "rather" still flags.
HEDGE_NOT_FOLLOWED_BY = {
    "rather": r"(?!\s+than\b)",
}


def compile_hedges(words):
    return [
        (w, re.compile(r"\b" + re.escape(w).replace(r"\ ", r"\s+") + r"\b"
                       + HEDGE_NOT_FOLLOWED_BY.get(w.lower(), ""),
                       re.IGNORECASE))
        for w in words
    ]


class Rules(object):
    """Built-in checks plus whatever a project adds."""

    def __init__(self, data=None, max_words=None):
        data = data or {}
        self.max_words = max_words or data.get("max_words", DEFAULT_MAX_WORDS)
        self.hedges = compile_hedges(
            HEDGE_WORDS + list(data.get("hedge_words", []))
        )
        self.figure_re = build_figure_re(data.get("figure_nouns", []))
        self.cues = ATTRIBUTION_CUES + [
            c.lower() for c in data.get("attribution_cues", [])
        ]
        self.ai_tells = [
            (re.compile(p, re.IGNORECASE | re.MULTILINE), p, advice)
            for p, advice in AI_TELLS
        ]
        self.severity = dict(data.get("severity", {}))
        self.patterns = []
        for i, spec in enumerate(data.get("patterns", [])):
            check_id = spec.get("id") or "project-rule-%d" % (i + 1)
            sev = str(spec.get("severity", "WARN")).upper()
            if sev == "OFF":
                continue
            self.patterns.append((
                check_id,
                sev if sev in ("FAIL", "WARN") else "WARN",
                re.compile(spec["regex"], re.IGNORECASE),
                spec.get("message", "project rule"),
            ))

    def sev(self, check):
        """Severity for a built-in check, after project override."""
        default = DEFAULT_SEVERITY[check]
        raw = str(self.severity.get(check, default))
        upper = raw.upper()
        if upper == "OFF":
            return None
        return upper if upper in ("FAIL", "WARN") else default


def load_rules(path, max_words=None):
    if path is None:
        return Rules(None, max_words)
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("rules file must contain a JSON object")
    for check in data.get("severity", {}):
        if check not in BUILTIN_CHECKS:
            raise ValueError(
                "severity names unknown check %r; known: %s"
                % (check, ", ".join(BUILTIN_CHECKS))
            )
    for check, value in data.get("severity", {}).items():
        if str(value).upper() not in [s.upper() for s in VALID_SEVERITIES]:
            raise ValueError(
                "severity for %r must be FAIL, WARN, or off" % check
            )
    for i, spec in enumerate(data.get("patterns", [])):
        if "regex" not in spec:
            raise ValueError("patterns[%d] has no regex" % i)
        re.compile(spec["regex"])
    return Rules(data, max_words)


def strip_noise(line):
    """Remove inline code and URLs before content checks."""
    line = INLINE_CODE_RE.sub(" ", line)
    line = LINK_RE.sub(" LINKED-SOURCE ", line)
    return line


def sentence_has_attribution(sentence, cues):
    low = sentence.lower()
    if "linked-source" in low:
        return True
    return any(cue in low for cue in cues)


def lint_text(text, rules=None, max_words=None):
    """Return a list of findings: (line_no, severity, check, message)."""
    if rules is None:
        rules = Rules(None, max_words)
    findings = []
    in_fence = False
    for line_no, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        sev = rules.sev("em-dash")
        if sev and EM_DASH in raw:
            findings.append((
                line_no, sev, "em-dash",
                "em dash found; use a comma, semicolon, period, or parentheses",
            ))
        sev = rules.sev("spaced-en-dash")
        if sev and (" %s " % EN_DASH) in raw:
            findings.append((
                line_no, sev, "spaced-en-dash",
                "spaced en dash reads as an em dash; restructure",
            ))

        line = strip_noise(raw)

        sev = rules.sev("hedge-word")
        if sev:
            for hedge, hedge_re in rules.hedges:
                if hedge_re.search(line):
                    findings.append((
                        line_no, sev, "hedge-word",
                        'hedge "%s"; say it plainly or cut it' % hedge,
                    ))

        sev = rules.sev("ai-tell")
        if sev:
            for tell_re, pattern, advice in rules.ai_tells:
                m = tell_re.search(line)
                if m:
                    findings.append((
                        line_no, sev, "ai-tell",
                        'AI tell "%s" (%s)' % (m.group(0).strip(), advice),
                    ))

        for check_id, pat_sev, pat_re, message in rules.patterns:
            m = pat_re.search(line)
            if m:
                findings.append((
                    line_no, pat_sev, check_id,
                    '"%s" (%s)' % (m.group(0).strip(), message),
                ))

        len_sev = rules.sev("sentence-length")
        fig_sev = rules.sev("unattributed-figure")
        for sentence in SENTENCE_SPLIT_RE.split(line):
            if len_sev:
                words = sentence.split()
                if len(words) > rules.max_words:
                    findings.append((
                        line_no, len_sev, "sentence-length",
                        "sentence has %d words (limit %d); split it, "
                        "one idea per sentence" % (len(words), rules.max_words),
                    ))
            if fig_sev:
                m = rules.figure_re.search(sentence)
                if m and not sentence_has_attribution(sentence, rules.cues):
                    findings.append((
                        line_no, fig_sev, "unattributed-figure",
                        'figure "%s" has no attribution cue and no goal '
                        "label; attribute it or label it a goal"
                        % m.group(0).strip(),
                    ))
    return findings


def report(path, findings):
    if not findings:
        print("%s: clean" % path)
        return
    for line_no, severity, check, message in findings:
        print("%s:%d: %s [%s] %s" % (path, line_no, severity, check, message))
    fails = sum(1 for f in findings if f[1] == "FAIL")
    warns = len(findings) - fails
    print("%s: %d FAIL, %d WARN" % (path, fails, warns))


SELF_TEST_BAD = (
    "The corridor is booming " + EM_DASH + " photonics is the future.\n"
    "Light moves data " + EN_DASH + " and it moves it fast.\n"
    "Colorado has 250 photonics companies and 8,000 workers.\n"
    "It is arguably the best place in America to build with light, and this "
    "sentence keeps going and going, adding clause after clause, idea after "
    "idea, well past the point where a reader can hold it in one breath.\n"
    "Let us delve into the tapestry of a seamless future.\n"
)

SELF_TEST_CLEAN = (
    "The corridor builds computing on light.\n"
    "The industry association has cited on the order of 250 photonics "
    "companies statewide; confirm the current figure before publishing.\n"
    "Reaching 10,000 photonics workers is a goal, not a count.\n"
    "Count signed letters rather than estimates.\n"
)

# The default grade of every built-in check, written out apart from
# DEFAULT_SEVERITY, so a changed default fails here instead of passing quietly.
# Source: ~/.claude/rules/writing-and-gates.md, "Block on the certain, warn on
# the likely." The two dash checks are literal character tests, so they
# block. The rest are heuristics, so they warn.
SELF_TEST_EXPECTED = {
    "em-dash": "FAIL",
    "spaced-en-dash": "FAIL",
    "sentence-length": "WARN",
    "hedge-word": "WARN",
    "ai-tell": "WARN",
    "unattributed-figure": "WARN",
}

# One row of the "Built-in checks" table in the module docstring.
DOC_TABLE_RE = re.compile(r"^  ([a-z][a-z-]+)\s+(FAIL|WARN)\s", re.MULTILINE)

SELF_TEST_RULES = {
    "max_words": 30,
    "patterns": [
        {"id": "banned-term", "severity": "FAIL",
         "regex": r"\bsynergy\b", "message": "say what actually happens"}
    ],
    "severity": {"hedge-word": "off"},
}

SELF_TEST_PROJECT = "We unlocked real synergy this quarter.\n"


def self_test():
    ok = True

    def check(condition, label):
        print("self-test: %s: %s" % (label, "OK" if condition else "FAIL"))
        return condition

    def graded(findings, check_id):
        return set(f[1] for f in findings if f[2] == check_id)

    bad = lint_text(SELF_TEST_BAD)
    for check_id in BUILTIN_CHECKS:
        expected = SELF_TEST_EXPECTED.get(check_id)
        ok = check(
            graded(bad, check_id) == {expected},
            "seeded %s flagged at %s" % (check_id, expected),
        ) and ok

    # Nothing at all, not merely no FAIL. A figure check that warns would
    # otherwise let a broken attribution cue through unseen.
    clean = lint_text(SELF_TEST_CLEAN)
    if clean:
        print("self-test: clean sample raised a finding: FAIL")
        for f in clean:
            print("  clean-sample:%d: %s [%s] %s" % f)
        ok = False
    else:
        print("self-test: clean sample raises nothing: OK")

    # "Rather than" is contrast, and the house rules use it themselves. The
    # clean sample above carries one; a bare "rather" must still hedge.
    ok = check(
        any(f[2] == "hedge-word"
            for f in lint_text("The plan is rather ambitious.\n")),
        'a bare "rather" still flags as a hedge',
    ) and ok

    if __doc__:
        ok = check(
            dict(DOC_TABLE_RE.findall(__doc__)) == SELF_TEST_EXPECTED,
            "docstring table matches the default grades",
        ) and ok
    else:
        print("self-test: docstring stripped (python -OO); table not checked")

    regraded = lint_text(SELF_TEST_BAD, Rules({"severity": {
        "spaced-en-dash": "WARN", "unattributed-figure": "FAIL",
    }}))
    ok = check(
        graded(regraded, "spaced-en-dash") == {"WARN"}
        and graded(regraded, "unattributed-figure") == {"FAIL"},
        "a rules file regrades a built-in default in either direction",
    ) and ok

    rules = Rules(SELF_TEST_RULES)
    proj = lint_text(SELF_TEST_PROJECT, rules)
    ok = check(
        any(f[2] == "banned-term" and f[1] == "FAIL" for f in proj),
        "project pattern flagged at its declared severity",
    ) and ok

    off = lint_text(SELF_TEST_BAD, rules)
    ok = check(
        not any(f[2] == "hedge-word" for f in off),
        "severity off suppresses a built-in check",
    ) and ok
    ok = check(
        any(f[2] == "em-dash" for f in off),
        "project rules do not replace the built-ins",
    ) and ok

    try:
        load_rules_from_obj({"severity": {"no-such-check": "off"}})
        ok = check(False, "unknown check name rejected")
    except ValueError:
        ok = check(True, "unknown check name rejected") and ok

    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def load_rules_from_obj(data):
    """Validate an in-memory rules dict. Used by the self-test."""
    import tempfile
    import os
    fd, path = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        return load_rules(path)
    finally:
        os.unlink(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generic prose voice lint")
    parser.add_argument("files", nargs="*", help="files to lint")
    parser.add_argument("--rules", help="path to a project rules JSON file")
    parser.add_argument("--max-words", type=int, default=None,
                        help="sentence word limit (default %d)"
                             % DEFAULT_MAX_WORDS)
    parser.add_argument("--self-test", action="store_true",
                        help="run the embedded seeded samples and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()
    if not args.files:
        parser.print_usage()
        return 2

    try:
        rules = load_rules(args.rules, args.max_words)
    except (OSError, ValueError) as exc:
        print("rules error: %s" % exc, file=sys.stderr)
        return 2

    any_fail = False
    for path in args.files:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            print("%s: cannot read (%s)" % (path, exc), file=sys.stderr)
            return 2
        findings = lint_text(text, rules)
        report(path, findings)
        if any(f[1] == "FAIL" for f in findings):
            any_fail = True
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
