#!/usr/bin/env python3
"""voice_lint.py: the mechanical half of the Photon Mountain voice check.

Deterministic, no network, standard library only. Rules source:
01_doctrine/voice.md. This script enforces the rules a machine can
enforce; the judgment half (honest framing, one idea per sentence as
meaning rather than word count) lives in the pm-voice-check skill.

Checks:
  em-dash              FAIL  Any em dash (U+2014). voice.md: never.
  spaced-en-dash       WARN  " - " styled en dash (U+2013) used as an
                             em-dash substitute.
  sentence-length      WARN  Sentence longer than --max-words words
                             (default 30). A proxy for "one idea per
                             sentence"; the skill makes the real call.
  hedge-word           WARN  Hedging that fights "plain and direct".
  unattributed-figure  FAIL  A money amount, percentage, comma-grouped
                             number, magnitude figure (million, billion),
                             or counted quantity (companies, workers,
                             jobs...) in a sentence with no attribution
                             cue and no goal label. Heuristic: it flags
                             candidates for human review; an attributed
                             figure the regex misses is a false positive
                             to wave through, not a rule change.

Skipped: fenced code blocks, inline code spans, and URLs.

Usage:
  python3 voice_lint.py FILE [FILE ...]
  python3 voice_lint.py --max-words 35 FILE
  python3 voice_lint.py --self-test

Exit codes: 0 = no FAIL findings (warnings allowed), 1 = at least one
FAIL, 2 = usage or read error.
"""

import argparse
import re
import sys

EM_DASH = "—"
EN_DASH = "–"

DEFAULT_MAX_WORDS = 30

HEDGE_WORDS = [
    "arguably",
    "probably",
    "perhaps",
    "maybe",
    "somewhat",
    "fairly",
    "rather",
    "quite",
    "relatively",
    "potentially",
    "seemingly",
    "appears to",
    "seems to",
    "could be",
    "might be",
    "may be",
    "sort of",
    "kind of",
    "more or less",
    "virtually",
    "essentially",
    "basically",
    "generally",
    "in some sense",
    "to some extent",
]

# A figure worth flagging. Deliberately narrow so that small inline
# numbers ("step 4", "under 7 days", years) never flag.
FIGURE_RE = re.compile(
    r"""
    (?:
        [$€£]\s?\d[\d,.]*                # money
      | \d[\d,.]*\s?(?:%|\bpercent\b)              # percentage
      | \b\d{1,3}(?:,\d{3})+\b                     # comma-grouped number
      | \b\d[\d,.]*\s?(?:million|billion|trillion|thousand)\b
      | \b\d[\d,.]*\+?\s(?:[a-z-]+\s)?(?:companies|firms|workers|employees|
            jobs|students|researchers|startups|acres|megawatts|gigawatts|
            patents|labs|buildings)\b
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

# If any of these appear in the same sentence as a figure, the figure
# counts as attributed or labeled a goal.
ATTRIBUTION_CUES = [
    "according to",
    "per ",
    "source",
    "cite",
    "cites",
    "cited",
    "reports",
    "reported",
    "says",
    "said",
    "estimate",
    "estimates",
    "estimated",
    "announced",
    "association",
    "study",
    "survey",
    "census",
    "data from",
    "figures from",
    "goal",
    "target",
    "on the order of",
]

LINK_RE = re.compile(r"\[[^\]]*\]\([^)]+\)|https?://\S+")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")

HEDGE_RES = [
    (h, re.compile(r"\b" + re.escape(h).replace(r"\ ", r"\s+") + r"\b", re.IGNORECASE))
    for h in HEDGE_WORDS
]


def strip_noise(line):
    """Remove inline code and URLs before content checks."""
    line = INLINE_CODE_RE.sub(" ", line)
    line = LINK_RE.sub(" LINKED-SOURCE ", line)
    return line


def sentence_has_attribution(sentence):
    low = sentence.lower()
    if "linked-source" in low:
        return True
    return any(cue in low for cue in ATTRIBUTION_CUES)


def lint_text(text, max_words=DEFAULT_MAX_WORDS):
    """Return a list of findings: (line_no, severity, check, message)."""
    findings = []
    in_fence = False
    for line_no, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if EM_DASH in raw:
            findings.append(
                (line_no, "FAIL", "em-dash",
                 "em dash found; use a comma, semicolon, period, or parentheses")
            )
        if f" {EN_DASH} " in raw:
            findings.append(
                (line_no, "WARN", "spaced-en-dash",
                 "spaced en dash reads as an em dash; restructure")
            )

        line = strip_noise(raw)

        for hedge, hedge_re in HEDGE_RES:
            if hedge_re.search(line):
                findings.append(
                    (line_no, "WARN", "hedge-word",
                     f'hedge "{hedge}"; say it plainly or cut it')
                )

        for sentence in SENTENCE_SPLIT_RE.split(line):
            words = sentence.split()
            if len(words) > max_words:
                findings.append(
                    (line_no, "WARN", "sentence-length",
                     f"sentence has {len(words)} words (limit {max_words}); "
                     "split it, one idea per sentence")
                )
            m = FIGURE_RE.search(sentence)
            if m and not sentence_has_attribution(sentence):
                findings.append(
                    (line_no, "FAIL", "unattributed-figure",
                     f'figure "{m.group(0).strip()}" has no attribution cue '
                     "and no goal label; attribute it or label it a goal")
                )
    return findings


def report(path, findings):
    if not findings:
        print(f"{path}: clean")
        return
    for line_no, severity, check, message in findings:
        print(f"{path}:{line_no}: {severity} [{check}] {message}")
    fails = sum(1 for f in findings if f[1] == "FAIL")
    warns = len(findings) - fails
    print(f"{path}: {fails} FAIL, {warns} WARN")


SELF_TEST_BAD = (
    "The corridor is booming — photonics is the future.\n"
    "Colorado has 250 photonics companies and 8,000 workers.\n"
    "It is arguably the best place in America to build with light, and this "
    "sentence keeps going and going, adding clause after clause, idea after "
    "idea, well past the point where a reader can hold it in one breath.\n"
)

SELF_TEST_CLEAN = (
    "The corridor builds computing on light.\n"
    "The Colorado Photonics Industry Association has cited on the order of "
    "250 photonics companies statewide; confirm the current figure before "
    "publishing.\n"
    "Reaching 10,000 photonics workers is a goal, not a count.\n"
)


def self_test():
    bad = lint_text(SELF_TEST_BAD)
    clean = lint_text(SELF_TEST_CLEAN)
    checks_hit = {f[2] for f in bad}
    ok = True
    for expected in ("em-dash", "unattributed-figure", "hedge-word", "sentence-length"):
        if expected in checks_hit:
            print(f"self-test: seeded {expected} flagged: OK")
        else:
            print(f"self-test: seeded {expected} NOT flagged: FAIL")
            ok = False
    if any(f[1] == "FAIL" for f in clean):
        print("self-test: clean sample raised a FAIL: FAIL")
        for f in clean:
            print(f"  clean-sample:{f[0]}: {f[1]} [{f[2]}] {f[3]}")
        ok = False
    else:
        print("self-test: clean sample passes: OK")
    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="Photon Mountain voice lint")
    parser.add_argument("files", nargs="*", help="files to lint")
    parser.add_argument("--max-words", type=int, default=DEFAULT_MAX_WORDS,
                        help=f"sentence word limit (default {DEFAULT_MAX_WORDS})")
    parser.add_argument("--self-test", action="store_true",
                        help="run the embedded seeded samples and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()
    if not args.files:
        parser.print_usage()
        return 2

    any_fail = False
    for path in args.files:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            print(f"{path}: cannot read ({exc})", file=sys.stderr)
            return 2
        findings = lint_text(text, max_words=args.max_words)
        report(path, findings)
        if any(f[1] == "FAIL" for f in findings):
            any_fail = True
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
