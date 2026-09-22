---
description: Run the Photon Mountain voice gate on the files changed in this branch, or on named files.
---

Run the voice gate.

1. If the user named files, use those. Otherwise use what has changed against `main`:
   `git diff --name-only main...HEAD`
2. Run the shared hook on them, which is the same script CI and the pre-commit hook run:
   `bash .claude/hooks/pm-check-voice.sh <files>`
3. Then do the judgment pass the script cannot, per the `pm-voice-check` skill and `01_doctrine/voice.md`:
   honest framing with the three clocks kept apart, one idea per sentence as meaning rather than word count,
   plain and direct, affirmative framing, every figure attributed or labeled a goal.
4. Report script findings and judgment findings together, each with a line number and a proposed rewrite.
   Verdict: **Clean** or **Fix first**.

Do not auto-apply fixes. Propose them; the writer decides.

If any file carries current-status claims, hand off to `pm-fact-guardrails`. That skill owns the honesty
and freshness gate, and it searches before it asserts.
