# Task protocol
*The four-phase lifecycle for every Photon Mountain Project Task. Created 2026-07-05 (PT-2), per section 4 of `project_system_plan.md`. Kept short so it gets read.*

The work queue lives in `tasks.md`. The Cowork task widget is per-session scaffolding only; `tasks.md` is what persists.

## 1. Task Plan

- Every non-trivial task gets a short brief before work starts: one paragraph in `tasks.md`, or its own kickoff file in `00_project_system/` for large tasks (the existing kickoff files are the model).
- Brief template: objective (one sentence), files to read first, deliverables, constraints that bind this task, acceptance checks, and what "done" updates (Status, tasks.md, memory, counter).
- The one-sentence rule: if the task can be described in one sentence and touches one file, skip the brief and just do it with the standard close-out (phase 4).

## 2. Task Start

- Read in order: `CLAUDE.md`, `project_context.md`, the task brief, then only the files the task needs.
- Confirm scope back to Paul in two or three sentences before any file changes; ask clarifying questions then, not mid-task.
- Explore before editing: read the files the task touches before proposing changes.
- Create the session task list (widget) from the brief's deliverables.

## 3. Task Review

The verification gate before anything ships or the task is called done:

- **Voice check.** No em dashes anywhere in new or edited text; plain sentences; one idea per sentence (per `01_doctrine/voice.md`).
- **Honesty check.** Every figure attributed or labeled a goal; operating versus opening-2026 versus horizon framing correct; "formerly NREL" on first reference; Colorado Photonics Industry Association figures attributed to the association; photonic compute framed as emerging.
- **Freshness check.** Any stated current status (who operates what, what a program funds) was searched this session, not recalled.
- **Mechanical checks.** Run the map verifier (`photon_mountain_map_verify.py`) if the map was touched; re-render and eyeball any rebuilt deliverable.
- **User review.** Anything external-facing (copy, graphics, posts, the instructions field) gets Paul's explicit sign-off before it counts as done.

## 4. Task End

The close-out routine, run every task:

1. Verify deliverables against the brief's acceptance checks (the phase 3 gate).
2. Update `tasks.md`: move the item to Done, promote the next Active.
3. Update `CLAUDE.md` Status if project state changed; check the folder map for drift; check that `project_context.md` still tells the truth about where the project is.
4. Instructions counter: if the mirror was edited, log the change in its `## Change log` and check the count against 7 (protocol in `instructions_guide.md`).
5. Memory: did this task lock a decision a future session must know without reading files? If yes, write or update one entry. If a memory proved wrong during the task, fix it now. Conventions in `operating_notes.md`.
6. Recommend the kickoff for the next task in one short paragraph.

Once this protocol is stable it becomes the `pm-task-closeout` skill (PT-3), so "close out this task" runs the whole gate by name.
