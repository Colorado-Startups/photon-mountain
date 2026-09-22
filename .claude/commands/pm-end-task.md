---
description: Close a task through the project's four-phase lifecycle.
---

Close the current task per `00_project_system/task_protocol.md`, which is canonical. If the
`pm-task-closeout` skill ever disagrees with that file, the protocol wins and the skill gets
updated in the same session.

Work through it in order:

1. **Gates.** Run `/pm-voice-check` on everything written or edited. Run pm-fact-guardrails on
   anything carrying current-status claims. If `04_tools/` changed, run all three self-tests:
   `voice_lint.py`, `brand_tokens.py`, `marker_parity.py`. If the corridor atlas changed, run
   `marker_parity.py` against it. If the comparison maps changed, run `photon_mountain_map_verify.py`.
2. **Record.** Add a dated entry to the Done section of `00_project_system/tasks.md`. Say what
   changed, what was decided, and what was found. A close-out entry that only says "done" is
   worthless six months later.
3. **Propagate.** Update `CLAUDE.md` Status if the project's state changed. If the Cowork
   instructions mirror changed, add a dated changelog line and increment its counter per
   `00_project_system/instructions_guide.md`.
4. **Memory.** Ask whether this task locked a decision a future session must know without reading
   files. If yes, write or update one entry. If a memory proved wrong during the task, fix it now.

Report what passed, what changed, and anything left open.
