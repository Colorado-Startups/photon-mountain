# Operating notes

Lightweight for now. Photon Mountain is a one-person project on day one; this grows as needed.

## Editing and version control

- The project folder is the source of truth. Paul edits in Cowork; Claude Code handles git (init, commits, branches, PRs, push), mirroring the Colorado AI convention.
- The GitHub repo is private `photon-mountain` under the **Colorado-Startups** org (https://github.com/Colorado-Startups, created 2026-09-21). The earlier Colorado-AI target was dropped: Paul is an outside collaborator there, not a member, so he cannot create repos in that org. Plan and status: `github_setup_plan.md`.

## Build notes

- No browser in the build sandbox. Render PDFs with reportlab, then rasterize to PNG with `pdftoppm -png -r 200 -singlefile`.
- Build dependencies are pinned in `../requirements.txt`. Nothing builds or renders on the MacBook Air (Paul, 2026-11-02). The cloud-test entries in `../.github/cloud-test.json` install them on a hosted runner and return the outputs as artifacts. Full steps and the per-build checklist: `../03_deliverables/infographics/BUILD.md`.
- **What the map verifier actually checks.** `photon_mountain_map_verify.py` verifies the **Silicon Valley comparison maps**, not the corridor atlas. It checks tier membership, blob nesting, and core diameters. It is indifferent to styling, which makes it a good re-skin regression test. It is not font-free: it imports the generator, which imports matplotlib. The corridor atlas in `../03_deliverables/maps/` is guarded separately by `../04_tools/marker_parity.py`. An earlier version of this file said the verifier was a pure numeric check to run after any map edit; that was wrong on both counts and misled a later planning session.
- npm and PyPI may be blocked in-sandbox; rebuild from the scripts already in the repo rather than installing.

## Retired prompts

Both one-time Claude Code prompts that used to live here were deleted 2026-09-22 once spent. The Colorado AI cleanup completed 2026-07-05, and the GitHub setup prompt was superseded by `github_setup_plan.md`, which owns the repo work end to end.

## Task queue

The work queue lives in `tasks.md` (Active, Backlog, Done). The task lifecycle lives in `task_protocol.md`. The informal list that used to sit here migrated to `tasks.md` on 2026-07-05 (PT-2).

## Memory conventions

Cowork project memory complements the repo; it does not replace it. Repo is truth; memory is recall.

- **What memory holds:** durable orientation facts and locked decisions. Present examples: what the project is, the domains, the map conventions, the project system plan. Future examples: the locked brand identity, the GitHub repo location, major strategic decisions.
- **What memory never holds:** substance (corridor facts, figures, and sources belong in `02_substance/`), drafts, task state, anything the repo already records.
- **Format:** one fact per entry, entries linked to each other, index kept current. This matches how the existing entries are built.
- **Cadence:** at task end, ask "did this task lock a decision a future session must know without reading files?" If yes, write or update one entry. If a memory proved wrong during the task, fix it then.
