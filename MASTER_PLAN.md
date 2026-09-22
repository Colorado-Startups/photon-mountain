# Photon Mountain · Master Plan

*Rewritten 2026-09-22 in the project's own terms. The 2026-07-14 version was written under an external orchestration system and used its PT/DS/UA vocabulary, which does not match this project's `00_project_system/task_protocol.md`, and it referenced a repository that is not part of this one. Plan only; nothing here builds anything. `00_project_system/tasks.md` remains the source of truth for the queue. This file is the phase-level narrative that a flat queue cannot carry: what order the work goes in, and why.*

## Mission

Photon Mountain is the identity for Colorado's computing-with-light corridor: the Front Range stretch from Boulder through Golden and Arvada to Denver, where the state builds the next computing era on the photon. Silicon Valley was named for the material of the last era. Photon Mountain is named for the medium of the next one.

The project turns that idea into shippable corridor doctrine: a locked brand, verified substance, honest deliverables, and eventually a public presence. Everything ships through the project's own gates, so the corridor's credibility rests on its honesty. It was spun out of Colorado AI on 2026-06-22 and carries none of that project's motto, pillars, logo, or palette.

## Where things actually stand (verified 2026-09-22)

- **Brand: locked and now applied.** `01_doctrine/brand_identity.md` is canonical and carries its own origin record. Tagline "Build with light." Mark: Summit Sun. Palette: Summit Night, Alpenglow, Laser Violet. Type: Space Grotesk, Inter, Space Mono.
- **Substance: reframed, not seeds.** The four Colorado AI seeds became corridor substance on 2026-07-06, each with per-document honesty guardrails and a dated source block.
- **Corridor map: done, and now machine-checked.** 53 markers across four files, with `04_tools/marker_parity.py` enforcing the roster invariant that used to be confirmed by hand.
- **Build pipeline: on-brand.** Closed 2026-09-22. Every color and font comes from `04_tools/brand_tokens.py`.
- **Tooling:** three gate scripts, all standard library, all with self-tests: `voice_lint.py`, `brand_tokens.py`, `marker_parity.py`.
- **Repo: in progress.** Private `photon-mountain` under Colorado-Startups. Plan: `00_project_system/github_setup_plan.md`.
- **Roster verification: never run.** This is the project's one standing verification debt, and it gates going public.
- **Deliverable cadence and public presence: undecided.** Nothing in the project files commits to either.

## The phases, in order

### Phase A · Version control (active)

**Goal.** The project under git, with the doctrine gates running locally and in CI.
**Why first now.** It was scheduled last, on the reasoning that the tooling should exist before the repo captured it. That reasoning held until the tooling did exist. Once the build pipeline closed, every further change to the project was a change nobody could review or revert. Paul moved this forward on 2026-09-21.
**Exit.** Repo live and private under Colorado-Startups, full tree pushed, pre-commit hook firing, `local/` and `.venv/` absent from the remote, status recorded in `tasks.md` and `CLAUDE.md`.
**Detail.** `00_project_system/github_setup_plan.md`.

### Phase B · Substance verification closeout

**Goal.** Clear the standing verification debt so every substance document is publication-eligible on demand.
**Exit.** All seven documents in `02_substance/` pass a fresh fact-guardrails run dated within this phase. The company roster has a completed row-by-row re-verification with a dated record in the file. `02_substance/README.md` reflects the new dates.

The roster check is the real work: every row verified by search, confirming the company exists, does what the row says, at the location stated. Rows that fail get corrected or explicitly flagged, never silently kept. This phase gates Phase D.

### Phase C · Deliverable cadence

**Goal.** A repeatable rhythm of corridor deliverables, drawn only from verified substance, each shipped through the gates.
**Exit.** A cadence definition exists in `00_project_system/`, with the open choices resolved: which deliverable types, what frequency, which channels. At least one full cycle has shipped end to end.

Nothing decides this today. Candidate types from existing assets: the corridor one-pager, the launch infographic, map excerpts, substance-doc briefs. The standing rule to write into the definition: every ship re-runs the fact gate that day. Cadence claims about the corridor are re-verified per ship, never recalled.

### Phase D · Go public

**Goal.** The repo public, and the corridor's materials citable.
**Gated on.** Phase B. Publishing an unverified roster would violate the project's own honesty rule, and once public it can be cited by anyone.
**What it unlocks.** Rulesets, required status checks, protected `main`, CODEOWNERS enforcement, and unmetered Actions, all free; a private repo in a Free organization gets none of them. So this is a capability upgrade, not a visibility toggle.
**Also in scope.** `CODE_OF_CONDUCT.md`, and confirming the license files and OpenStreetMap attribution, since ODbL obligations attach on distribution.

### Phase E · Packaging (optional)

**Goal.** Bundle the pm- skills as an installable plugin, if reuse justifies it.
**Exit.** Either a working plugin, exercised once, or a recorded decision to skip with the reason.

Research on 2026-09-21 weakened the case: `claude-code-action` runs a repository skill directly after a checkout, so the plugin is not needed for CI. Its only remaining value is installability outside this repo. If no second project wants these skills, skip it and record that.

### Phase F · Public presence (not drafted)

Website, social channels, and launch timing are undecided everywhere in the project files. Drafting this before the cadence has run a cycle would be planning ahead of evidence. Revisit after Phase C.

## Dependencies and standing constraints

- **Colorado AI.** The two projects share subject matter with a locked boundary: photonic quantum lives here, the broad quantum-for-materials story and statewide AI policy stay with Colorado AI. Any substance edit that moves a claim across that boundary needs a check against the other project first.
- **Honesty gates.** Every step closes through pm-voice-check and, for anything carrying current-status claims, pm-fact-guardrails. No step is done until its gates pass. External-facing work also needs Paul's sign-off.
- **Free-tier GitHub.** Until Phase D, nothing can be enforced server-side. The pre-commit hook is the only real gate, which is why its policy was set deliberately rather than by default.
- **Three clocks.** Operating today, opening in 2026, on the horizon. Blurring them is the fastest way to lose a technical audience, and it is the failure mode every gate in this project exists to catch.

## Open questions for Paul

1. **Cadence shape.** Which deliverable types, what frequency, which channels? Phase C cannot start without this.
2. **Roster timing.** Run the row-by-row verification as its own phase, as planned here, or defer it to the first real publication event?
3. **Packaging.** Is there a second project that would use the pm- skills? If not, Phase E is a recorded skip.
4. **Public presence.** Draft Phase F now, or wait until the cadence has run at least one cycle?
