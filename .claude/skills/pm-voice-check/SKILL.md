---
name: pm-voice-check
description: Run the Photon Mountain voice check on a named file. Mechanical pass via 04_tools/voice_lint.py, then the judgment checklist from 01_doctrine/voice.md. Use when the user says "voice check this", "lint this draft", "run pm-voice-check on X", or wants a draft checked against the Photon Mountain voice before ship.
---

# pm-voice-check

Two passes over one named file. The script catches what a machine can catch. The judgment pass catches what it cannot. Rules source: `01_doctrine/voice.md` in the Photon Mountain project folder. If this skill and `voice.md` disagree, `voice.md` wins.

## When to use

- A draft, doc, or copy edit needs a voice pass before it ships or closes.
- The Task Review voice check (phase 3 of `00_project_system/task_protocol.md`) is being run on new or edited text.

Do not use for: code files, data files, or third-party text quoted as evidence.

## Inputs

1. The target file path. Ask if not given.
2. Nothing else. The rules come from `voice.md`, not from the user.

## Pass 1: mechanical (the script)

Run `04_tools/voice_lint.py` from the project folder on the target file, using the session's shell path for the project mount:

```bash
python3 "<project folder>/04_tools/voice_lint.py" "<target file>"
```

The script is deterministic and needs no network. It reports, with line numbers:

- `em-dash` (FAIL): any em dash.
- `spaced-en-dash` (FAIL): an en dash with a space on each side, which reads as an em dash.
- `unattributed-figure` (WARN): a figure with no attribution cue and no goal label.
- `ai-tell`, `sentence-length`, `hedge-word` (WARN).

The script owns these grades. It is a copy synced from Claude-OS, and the "Built-in checks" table in its docstring is the canonical list. If this list and that table disagree, the table wins; update this list in the same session.

Treat every FAIL as a required fix. Treat every WARN as a prompt: confirm it is fine or fix it. The figure check warns because it is a heuristic, not because the rule is soft. Every figure still needs a source or a goal label. If a flagged figure is attributed in a way the script missed, wave it through and say so in the report.

## Pass 2: judgment (the checklist)

Read the target file and check each item:

- **Honest framing.** What operates today, what opens in 2026, and what is on the horizon stay distinct.
- **One idea per sentence.** As meaning, not word count. A short sentence carrying two claims still fails.
- **Plain and direct.** Say it once. No overselling; the corridor story is true and does not need it.
- **Affirmative framing.** Describe what the corridor builds and can build, not what it lacks.
- **Attribution in substance.** Every figure traces to a named credible source or carries a goal label.

For corridor facts and current-status claims, hand off to `pm-fact-guardrails`; that skill owns the honesty and freshness gate.

## Report

One consolidated report:

- Script findings, each with line number and a proposed rewrite.
- Judgment findings, each with location and a proposed rewrite.
- Verdict: **Clean** (ship) or **Fix first** (apply the listed fixes, then re-run this skill).

Do not auto-apply fixes. Propose them; the writer decides.
