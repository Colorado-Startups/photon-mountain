---
name: pm-task-closeout
description: Run the Photon Mountain end-of-task close-out routine (task_protocol.md phase 4). Use when the user says "close out this task", "run pm-task-closeout", "task end", "wrap up this Project Task", or asks to finish a task and update the project system.
---

# pm-task-closeout

The phase 4 close-out routine from `00_project_system/task_protocol.md`, invocable by name. The protocol file is canonical. Read it first each run; if this skill and `task_protocol.md` disagree, `task_protocol.md` wins, and this skill needs an update in the same session.

## When to use

- At the end of every Photon Mountain Project Task, once the work itself is done.
- Only after the phase 3 Task Review gate has been run on the deliverables (step 1 below verifies against it).

## Inputs

1. The task being closed (its entry in `00_project_system/tasks.md` or its brief).
2. The list of files the task touched.

## The routine

Run these six steps, quoted from `task_protocol.md` phase 4:

1. Verify deliverables against the brief's acceptance checks (the phase 3 gate).
2. Update `tasks.md`: move the item to Done, promote the next Active.
3. Update `CLAUDE.md` Status if project state changed; check the folder map for drift; check that `project_context.md` still tells the truth about where the project is.
4. Instructions counter: if the mirror was edited, log the change in its `## Change log` and check the count against 7 (protocol in `instructions_guide.md`).
5. Memory: did this task lock a decision a future session must know without reading files? If yes, write or update one entry. If a memory proved wrong during the task, fix it now. Conventions in `operating_notes.md`.
6. Recommend the kickoff for the next task in one short paragraph.

Notes on execution:

- Step 1: the phase 3 gate is the voice, honesty, freshness, mechanical, and user-review checks in `task_protocol.md`. On new or edited text, run the first three via `pm-voice-check` and `pm-fact-guardrails`.
- Step 2: `tasks.md` Done entries are dated one-liners, newest first.
- Step 5: one durable fact per entry, index kept current.
- External-facing work needs Paul's explicit sign-off before it counts as done (phase 3, user review).

## Report

Close with a short summary: acceptance checks and their results, the `tasks.md` move, and any Status or folder-map edits. Add the counter state if the mirror was touched, memory written or fixed, and the recommended next kickoff.
