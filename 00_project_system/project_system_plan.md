# Photon Mountain · Project System Plan
*Draft for review, created 2026-07-05. This is the plan to stand up the full Cowork project system: instructions, context, memory, task lifecycle, and tooling. Review and tweak it in this Project Task; execute it in the new Project Tasks listed in section 6.*

---

## 1. Where the project stands

What already exists and works:

- `cowork_project_instructions.md` mirrors the Cowork Settings > Instructions field. The mirror convention is already established.
- `CLAUDE.md` is the router and behavioral contract; `project_context.md` is the five-minute overview. Status is current as of 2026-07-05, but the folder map has drift: it omits `01_doctrine/brand_creation_plan.md`, `02_substance/colorado_photonics_companies.md` (and `.xlsx`), `02_substance/rocky_flats_restoration_brainstorm.md`, and the `03_deliverables/maps/` files. PT-2 fixes this.
- `00_project_system/operating_notes.md` holds conventions and an informal near-term task list (GitHub repo, brand identity, substance reframe).
- Cowork project memory holds three entries (project identity, domains, corridor map) with an index.
- Deliverables render; build scripts await the brand re-skin; the corridor map is done and locked.

What is missing:

- No best-practice guide for writing and updating the project instructions, and no change counter.
- No formal task system (the near-term list in operating notes is explicitly "not yet a formal system").
- No written conventions for what goes into project memory versus the repo.
- No defined task lifecycle (plan, start, review, end).
- No Photon Mountain tooling: no project skills, no verification automation beyond the map verifier, no scheduled watches.

## 2. Best-practice findings (research summary)

The recommendations in this plan rest on these findings. Sources at the end.

**Instructions and CLAUDE.md.** Treat instructions as a behavioral contract, not documentation; every line should change behavior, and anything that does not should be cut. Keep files concise and structured (Anthropic guidance clusters around roughly 200 lines for CLAUDE.md-class files); models follow a limited budget of distinct instructions per context, so short and specific beats long and complete. Put durable rules in files, not in conversation, because conversation context gets compacted. Photon Mountain already follows the strongest pattern here: a short instructions field that points to a fuller router file.

**Memory.** Cowork memory persists inside a Project and complements the repo; it does not replace it. Best practice is one durable fact per entry, an index kept current, and a review step so stale or wrong memories get corrected. The repo stays the source of truth for substance; memory holds orientation facts and locked decisions that every future session should recall without reading files.

**Task workflow.** The strongest documented pattern is Explore, Plan, Code (execute), Commit (close): explore before touching anything, plan before executing, verify against the plan, and close with a record. Each phase kills a different failure mode. The one-sentence rule governs ceremony: if the change can be described in one sentence, skip the formal plan; if it cannot, plan first. Quality of the task brief predicts quality of the output.

**Tooling layers.** Start with skills (cheap, load only when invoked); add deterministic checks (scripts, hooks) when a rule must always hold rather than usually hold; use subagents for isolated or parallel work; bundle into a plugin only when the set stabilizes and is worth one-click reuse. Hooks in the strict sense are a Claude Code feature; in Cowork the equivalent is a skill plus a script the skill always runs.

## 3. Project System recommendations

### 3.1 Project Instructions

Keep `cowork_project_instructions.md` as the mirror. Add two things.

**A best-practice guide**, new file `00_project_system/instructions_guide.md`. Contents: the behavioral-contract rule (every line must change behavior); the router pattern (the field stays the short version, `CLAUDE.md` stays the source of truth, never let them disagree); a length budget for the field (target under 500 words); ordering (identity, scope, voice, hard rules, how to work); the no-em-dash and honesty rules restated as non-negotiable; and a short checklist to run before any edit ships (does it conflict with CLAUDE.md, does it duplicate something already there, is it phrased as an instruction rather than background).

**A change counter**, a `## Change log` section at the bottom of the mirror file. Each editing session that changes the mirror body appends one dated one-line entry and increments a counter line reading `Changes since last paste into Cowork Settings: N of 7` (one count per session, however many lines moved). When N reaches 7, the session stops and prompts you to paste the body into Settings > Instructions and reset the counter to 0. Any session may also prompt earlier if an edit is urgent (a hard rule changed). The guide documents this protocol so every future session honors it.

### 3.2 Project Context

`project_context.md` stays the single orientation file. Recommendations:

- Keep it under one page. It answers "what is this and where is it" in five minutes; depth lives in the linked files.
- `CLAUDE.md` Status stays the dated state of record. Any task that changes project state (deliverable done, decision locked, phase complete) updates Status in the same session, and updates `project_context.md` only when the orientation story itself changes.
- Add a freshness check to the task-end routine (section 4.4): "does CLAUDE.md Status and the folder map still match reality; does project_context still tell the truth about where the project is."

No new files needed. The existing pair is already the right shape; the gap is only the discipline of updating them at task end, which the lifecycle fixes.

### 3.3 Project Memory

Memory conventions, written into `operating_notes.md` as a new section (no new file; keep the system small):

- **What memory holds:** durable orientation facts and locked decisions. Examples already present: what the project is, the domains, the map conventions. Future examples: the locked brand identity, the GitHub repo location, major strategic decisions.
- **What memory never holds:** substance (corridor facts, figures, sources belong in `02_substance/`), drafts, task state, anything the repo already records. Repo is truth; memory is recall.
- **Format:** one fact per entry, linked entries, index kept current. This matches how the three existing entries are built.
- **Cadence:** at task end, ask "did this task lock a decision a future session must know without reading files?" If yes, write or update one entry. If a memory proved wrong during the task, fix it then.

### 3.4 Task system home

New file `00_project_system/tasks.md`, the source of truth for the work queue. Three sections: **Active** (the current Project Task, one at a time as a norm), **Backlog** (ordered, each item a one-line objective plus a pointer to its brief if one exists), **Done** (dated one-liners, newest first). The near-term list in `operating_notes.md` migrates here and the operating notes point to it. The Cowork task widget is per-session scaffolding only; `tasks.md` is what persists.

## 4. Task lifecycle recommendations

One new file, `00_project_system/task_protocol.md`, defines all four phases. Kept under two pages so it gets read. The phases:

### 4.1 Task Plan

- Every non-trivial task gets a short brief before work starts, either in `tasks.md` (one paragraph) or as its own kickoff file in `00_project_system/` for large tasks (the existing kickoff files are the model).
- Brief template: objective (one sentence), files to read first, deliverables, constraints that bind this task, acceptance checks, and what "done" updates (Status, tasks.md, memory, counter).
- The one-sentence rule: if the task can be described in one sentence and touches one file, skip the brief and just do it with the standard close-out.

### 4.2 Task Start

- Read in order: `CLAUDE.md`, `project_context.md`, the task brief, then only the files the task needs.
- Confirm scope back to you in two or three sentences before any file changes; ask the clarifying questions then, not mid-task.
- Explore before editing: read the files the task touches before proposing changes.
- Create the session task list (widget) from the brief's deliverables.

### 4.3 Task Review

The verification gate before anything ships or the task is called done:

- **Voice check:** no em dashes anywhere in new or edited text; plain sentences; one idea per sentence (per `01_doctrine/voice.md`).
- **Honesty check:** every figure attributed or labeled a goal; operating versus opening-2026 versus horizon framing correct; "formerly NREL" on first reference; association figures attributed; photonic compute framed as emerging.
- **Freshness check:** any stated current status (who operates what, what a program funds) was searched this session, not recalled.
- **Mechanical checks:** run the map verifier if the map was touched; re-render and eyeball any rebuilt deliverable.
- **User review:** anything external-facing (copy, graphics, posts, the instructions field) gets your explicit sign-off before it counts as done.

### 4.4 Task End

The close-out routine, run every task:

1. Verify deliverables against the brief's acceptance checks (the 4.3 gate).
2. Update `tasks.md` (move the item to Done, promote the next Active).
3. Update `CLAUDE.md` Status if project state changed; check the folder map for drift.
4. Instructions counter: if the mirror was edited, log the change and check the count against 7.
5. Memory: write or fix entries per the 3.3 cadence.
6. Recommend the kickoff for the next task in one short paragraph.

This mirrors the close-out gate you run in your other projects, adapted to Photon Mountain's guardrails. Once the protocol is stable, it becomes a project skill (section 5.2) so it runs by name.

## 5. Tooling audit and recommendations

Format per category: what is built in and fits, gaps worth filling with existing tools, and what to build.

### 5.1 Plugins

- **Built in and fits:** the installed plugin set is broad (legal, finance, sales, small business) and almost none of it touches this project. Nothing needs removing; unused plugins cost nothing until invoked. `cowork-plugin-management` is the one directly useful plugin (it builds new plugins).
- **Gaps to fill:** none now.
- **Build:** a `photon-mountain` plugin, but only after the project skills (5.2) exist and stabilize. A plugin is packaging, not capability; premature bundling just adds maintenance. Your other projects show the end state: a set of project skills worth one-click reuse. Target: after brand and first skills, not before.

### 5.2 Skills

- **Built in and fits:** `docx`, `pptx`, `xlsx`, `pdf` (deliverables), `canvas-design` and `theme-factory` (visuals until the real brand exists), `doc-coauthoring` (long documents), `skill-creator` (builds the skills below).
- **Adjacent but off limits for output:** the Colorado AI skills (`new-infographic`, `fact-check-sweep`, `linkedin`, `emails`) and the Heaven Governance skills encode the pattern to copy but carry other projects' brands and voices. Use them as structural references only; never let them produce Photon Mountain output.
- **Build,** in order:
  1. **`pm-voice-check`**: lint a draft against `01_doctrine/voice.md`. Mechanical part is a script (em-dash detection, sentence length, hedge words, missing attribution lines); judgment part is a checklist (honest framing, one idea per sentence). Modeled on your fact-check-sweep pattern.
  2. **`pm-fact-guardrails`**: the honesty gate as a skill; walks the 4.3 honesty and freshness checks against a named file, with search steps for every current-status claim.
  3. **`pm-task-closeout`**: the 4.4 routine as an invocable skill, so "close out this task" runs the whole gate.
  4. **`pm-infographic`** (blocked by brand): render on-brand graphics from the re-skinned build scripts. Cannot exist until `01_doctrine/brand_brief.md` becomes a locked identity.

### 5.3 Agents

- **Built in and fits:** the `Explore` agent (read-only fan-out research; right tool for corridor fact sweeps across many sources), `general-purpose` (multi-step research), `claude-code-guide` (questions about Claude Code during repo work). The deep-research skill covers heavyweight cited reports.
- **Gaps to fill:** none; built-ins cover current needs.
- **Build:** nothing yet. A custom "corridor fact verifier" subagent only becomes worth it if the pm-fact-guardrails skill proves too slow inline. Revisit after the skills exist. Custom agents carry fixed overhead per spawn; this project's scale does not justify them today.

### 5.4 Connectors

- **Built in and fits:** Cloudflare MCP is connected and matters (both domains live there; a future site on Cloudflare Pages or Workers fits the free-tools rule). Chrome and computer use cover ad-hoc web work. Word and PowerPoint MCPs exist if native-app output is ever preferred over the file skills.
- **Gaps to fill:** a GitHub connector, once the repo exists, if reviewing issues or PRs from Cowork turns out to be common; one already ships with the installed engineering plugin but sits unauthenticated. Until the repo exists, Claude Code owns git end to end and no connector is needed. Nothing else: there is no CRM, no Slack workspace, no external system in this project's loop.
- **Build:** nothing. Do not add connectors speculatively; each one adds context cost to every session.

### 5.5 Scripts

- **Built in and fits:** the reportlab build scripts (awaiting re-skin), the map verifier (`photon_mountain_map_verify.py`, locked convention: run after any map edit), the sandbox render pipeline (reportlab then pdftoppm) documented in operating notes.
- **Gaps to fill:** none from outside; the pipeline is proven.
- **Build:**
  1. **`voice_lint.py`**: the mechanical half of pm-voice-check (em dashes, sentence length, unattributed-figure patterns). Small, deterministic, callable by skills and by hand.
  2. **`brand_tokens.py`** (blocked by brand): one shared token file (colors, fonts, spacing) that every build script imports, so the re-skin happens once and future scripts cannot drift off brand.

### 5.6 Hooks

- **Built in and fits:** hooks in the strict lifecycle sense are a Claude Code feature; Cowork exposes no user-configurable hook settings. The one Cowork route is indirect: plugins can bundle hooks, so the eventual `photon-mountain` plugin (5.1, PT-7) could carry them if a rule ever needs deterministic enforcement inside Cowork.
- **Gaps to fill:** in the Claude Code repo sessions (git side), a pre-commit check is the real hook surface.
- **Build:** a pre-commit hook in the repo (once it exists) that runs `voice_lint.py` on staged markdown and blocks commits containing em dashes or unattributed-figure patterns. Deterministic enforcement of the two rules most likely to slip. In Cowork, the equivalent enforcement lives in the task protocol plus the skills; that is the correct layering (skills for judgment, scripts and hooks for rules that must always hold).

### 5.7 Orchestrators

- **Built in and fits:** the plan-plus-tasks.md layer in this document is the orchestrator for a one-person project; scheduled tasks are the built-in automation surface.
- **Gaps to fill:** none. A standing corridor-news watch was considered and declined (decision 2026-07-05: corridor developments move too slowly for a weekly cadence). Fact freshness stays enforced per task by the search-before-stating rule and the 4.3 freshness check. If a fast-moving stretch ever arrives (launch season, a fab opening), a scheduled watch can be added then in minutes.
- **Build:** no multi-agent orchestration. Fan-out (one orchestrator spawning parallel workers) pays off on wide independent workloads; this project's tasks are sequential and judgment-heavy. Revisit only if the substance reframe turns out to parallelize cleanly.

### 5.8 Anything else

- **Memory:** covered in 3.3; the built-in system is sufficient.
- **Artifacts (live HTML views):** skip for now. A status dashboard would duplicate `tasks.md` for a team of one. Revisit if collaborators join.
- **Apple Notes, iMessage, PowerPoint and Word MCPs:** available, no current role.
- **GitHub:** already planned (`github_setup_plan.md`); it slots into the execution sequence below rather than the tooling list.

## 6. Execution plan

Sequenced Project Tasks. Each becomes a new Cowork Project Task with a brief per section 4.1. Order matters where noted.

| # | Task | Deliverables | Depends on |
|---|------|-------------|------------|
| PT-1 | **Review this plan** (this task) | Plan reviewed, tweaked, locked; execution order confirmed | none |
| PT-2 | **Stand up the project system** | `instructions_guide.md`; change-log section and counter added to the mirror; `task_protocol.md`; `tasks.md` (backlog migrated from operating notes); memory conventions section in operating notes; CLAUDE.md folder map and Status updated | PT-1 |
| PT-3 | **Build core skills and the lint script** | `voice_lint.py`; `pm-voice-check`; `pm-fact-guardrails`; `pm-task-closeout` | PT-2 |
| PT-4 | **Design the brand identity** | Locked identity from `01_doctrine/brand_brief.md`, following the existing `01_doctrine/brand_creation_plan.md`; recorded in memory | PT-2 (can run parallel to PT-3) |
| PT-5 | **Reframe the substance seeds** | `02_substance/` docs rewritten to the corridor and photonics focus per `SEED_README.md`, each passed through pm-fact-guardrails | PT-3 preferred (the gate exists) |
| PT-6 | **Re-skin the build pipeline** | `brand_tokens.py`; build scripts re-skinned; deliverables re-rendered; `RESKIN_NEEDED.md` retired; `pm-infographic` skill | PT-4 |
| PT-7 | **Packaging (optional)** | `photon-mountain` plugin bundling the skills, if reuse justifies it | PT-3, PT-6 |
| PT-8 | **Create the GitHub repo** | Repo live per `github_setup_plan.md` (Claude Code session, its own plan) under the Colorado-AI org; pre-commit hook with `voice_lint.py` from PT-3 | PT-2 (runs last per the 2026-07-05 amendment) |

Suggested rhythm: PT-3 next, then PT-4 (they can also run parallel), then PT-5, PT-6, PT-7, and PT-8 last as its own plan. Brand (PT-4) runs before substance (PT-5), per the 2026-07-05 review.

## 7. Review decisions (2026-07-05)

1. Counter scope: one counted change per editing session that touches the mirror, regardless of lines changed.
2. PT order: brand before substance (PT-4 before PT-5 in the renumbered sequence).
3. Corridor watch: declined; corridor developments move too slowly for a weekly cadence. Freshness is enforced per task instead.
4. Skill naming: `pm-` prefix (pm-voice-check, pm-fact-guardrails, pm-task-closeout, pm-infographic).

## Amendments

- 2026-07-05 (post-PT-2, per Paul): the GitHub repo task moves to last in the sequence and runs as its own plan, and the repo target changed from the Soul-Craft org to the Colorado-AI org (https://github.com/Colorado-AI).
- 2026-07-05 (post-PT-2, per Paul): the PTs were renumbered to execution order, and section 6 above now carries the new numbers. Mapping from the original numbering: skills PT-4 → PT-3, brand PT-5 → PT-4, substance PT-6 → PT-5, re-skin PT-7 → PT-6, packaging PT-8 → PT-7, GitHub PT-3 → PT-8. PT-1 and PT-2 are unchanged. Any PT reference in files dated before this amendment uses the original numbering.

## Sources

Best-practice research, 2026-07-05: [Claude Code best practices (Anthropic)](https://code.claude.com/docs/en/best-practices), [Customize Claude Cowork (Anthropic)](https://claude.com/resources/tutorials/customize-claude-cowork), [Get started with Claude Cowork (Anthropic Help Center)](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork), [Equipping agents for the real world with Agent Skills (Anthropic Engineering)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), [Agent Skills docs (Anthropic)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [How Claude remembers your project (Anthropic docs)](https://code.claude.com/docs/en/memory), [Hooks guide (Anthropic docs)](https://code.claude.com/docs/en/hooks-guide), plus practitioner guides on the explore-plan-code-commit workflow and extension-layer selection ([extension layer decision guide](https://hidekazu-konishi.com/entry/claude_code_extension_layers_decision_guide.html), [skills vs subagents vs hooks](https://www.buildthisnow.com/blog/tools/claude-code-skills-vs-subagents-vs-hooks)).
