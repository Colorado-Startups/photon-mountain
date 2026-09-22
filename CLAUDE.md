# Photon Mountain · Project Instructions
*Router file. Created 2026-06-22, spun out of the Colorado AI project. New here? Read this top-to-bottom, then `project_context.md`, then the file you need.*

## What this is

**Photon Mountain** is the identity for Colorado's computing-with-light corridor: the Front Range stretch where the state builds the future of computing on the photon, the particle of light. It is a place and ecosystem brand, the deliberate answer to "Silicon Valley." Silicon Valley was named for the material of the last computing era. Photon Mountain is named for the medium of the next one.

This project was spun out of **Colorado AI** on 2026-06-22. The split is clean:
- **Colorado AI** stays the statewide AI policy movement. It keeps its own Lead-pillar substance (photonic chips, renewable and fusion energy, and quantum for materials breakthroughs) for its candidate framework.
- **Photon Mountain** is this project: a place brand for the corridor, focused on photonics, growing its own identity, materials, and (eventually) its own movement.

The two share subject matter but are separate projects with separate brands and repos. Photon Mountain does not carry Colorado AI's motto, pillars, logo, or palette.

## Scope

**Geography.** The core corridor is **Boulder, Golden, Arvada, Denver**, with a greater ring (Louisville, Lafayette, Broomfield, Westminster, Longmont). Boulder is the research anchor (NIST, JILA, CU); Arvada holds the corridor's photonic-integrated-circuit fab; Denver is the metro anchor.

**Subject focus: what the corridor builds with light, energy, and compute.** (Broadened from light-only per Paul, 2026-07-05.)
- **Photonic chips** (processors and optical interconnects)
- **Photonic sensors and fiber optics**
- **Solar** (light as energy)
- **Laser fusion energy**
- **Energy for compute**: generation, storage, and grid research that powers the computing corridor; wind counts when it powers compute.
- **Space** when it involves solar or compute.
- **Photonic quantum only**: quantum optics and the photonic-IC fab count, because they are light-based. The broad "quantum for materials discovery" story belongs to Colorado AI, not here.

## Folder map

```
CLAUDE.md            This router
README.md            What the project is
project_context.md   Five-minute overview
TRANSFER_PLAN.md     The spin-out plan and the full reference audit (founding record)
cowork_project_instructions.md  Mirror of the Cowork Settings > Instructions field
00_project_system/   The project system
  tasks.md           Work queue (Active, Backlog, Done); source of truth
  task_protocol.md   The four-phase task lifecycle (plan, start, review, end)
  instructions_guide.md   How to edit the instructions mirror; change-counter protocol
  project_system_plan.md  The locked system plan and PT-2..PT-8 sequence
  operating_notes.md Conventions, sandbox notes, memory conventions
  github_setup_plan.md  The repo plan (PT-8)
01_doctrine/
  brand_identity.md  The locked v1 identity (canonical brand record, including its origin)
  brand_assets/      Summit Sun mark SVGs (locked)
    fonts/           The seven brand TTFs, OFL licenses, and how they were cut
  brand_guidelines.md  Usage-facing guidelines (external-ready form; internal until sign-off)
  branding_best_practices.md  Place-branding practice guide, sourced, with two case studies
  voice.md           Writing conventions; tone locked 2026-07-05
  why_and_how_guide.md   Structure standard for the substance docs (rewritten native 2026-09-22)
02_substance/        Corridor substance, reframed from the Colorado AI seeds 2026-07-06 (PT-5)
  README.md          Folder guide: verification dates, usage rules, standing boundaries
  corridor_facts_and_sources.md   Anchor institutions and the honesty guardrails
  colorado_photonics_companies.md (+ .xlsx)   Company roster
  photonics_why_and_how.md, energy_why_and_how.md, manufacturing_strategy.md,
  ai_compute_by_function.md, rocky_flats_restoration_brainstorm.md
03_deliverables/
  infographics/      The Photon Mountain launch infographic and the comparison maps
    BUILD.md         How to regenerate, and what to check on every build
  maps/              The definitive corridor boundary and marker atlas
    MAP_NOTES.md     Method, sources, locked conventions; read before editing the map
04_tools/
  voice_lint.py      Deterministic voice lint (em dashes, sentence length, hedges, unattributed figures); --self-test built in
  brand_tokens.py    The single source of brand values in code; --self-test checks it against brand_identity.md
  skills/            pm-voice-check, pm-fact-guardrails, pm-task-closeout skill directories; install via Settings > Capabilities
requirements.txt     Build dependencies (the doctrine tooling needs none)
local/               Gitignored operational files
```

## Status (updated 2026-09-22)

- **Project system:** stood up 2026-07-05 (PT-2). The work queue is `00_project_system/tasks.md`; the task lifecycle is `00_project_system/task_protocol.md`; the instructions mirror carries a change counter per `00_project_system/instructions_guide.md`; memory conventions are in `00_project_system/operating_notes.md`. The plan and PT sequence stay in `project_system_plan.md`. PTs renumbered to execution order 2026-07-05. PT-6 closed 2026-09-22. Active: PT-8, the GitHub repo. Paul brought it forward from last on 2026-09-21.
- **Tooling:** built 2026-07-05 (PT-3). `04_tools/voice_lint.py` is the deterministic voice lint (callable by hand and by skills; `--self-test` verifies it). The `pm-voice-check`, `pm-fact-guardrails`, and `pm-task-closeout` skills live in `04_tools/skills/` and install via Settings > Capabilities. `task_protocol.md` stays canonical; if pm-task-closeout ever disagrees with it, the protocol wins and the skill gets updated in the same session.
- **Deliverables:** on-brand and regenerating, as of 2026-09-22 (PT-6). Both build scripts import every color and font from `04_tools/brand_tokens.py`; neither hardcodes a brand value. The launch infographic and both comparison maps were regenerated in the locked identity. The geometry verifier passes with core diameters unchanged at 18.0 and 24.1 miles, which is the proof the re-skin touched styling only. Colorado AI's motto, flag, palette, fonts, and pillar framing are gone from every deliverable. How to rebuild, and what to check: `03_deliverables/infographics/BUILD.md`.
- **Corridor map:** done 2026-07-05. The definitive boundary and marker atlas lives in `03_deliverables/maps/` (HTML, GeoJSON, KML, JSX; 53 markers, seven two-word categories). Method, sources, and every locked convention are in `03_deliverables/maps/MAP_NOTES.md`; read it before editing the map.
- **Substance:** reframed 2026-07-06 (PT-5). The four Colorado AI seeds are now corridor substance in the locked voice, each with per-doc honesty guardrails and a dated source block (claims searched 2026-07-06). `lead_abundance.md` was archived 2026-07-06 and deleted 2026-09-22 as Colorado AI candidate-framework material. The three Photon Mountain-native docs got a freshness pass the same day. `02_substance/README.md` is the folder guide (formerly `SEED_README.md`, renamed 2026-07-06). Before any external use, re-run pm-fact-guardrails on the file; the roster's row-by-row re-verification stays a pre-publication step.
- **Brand:** locked 2026-07-05 (PT-4). The canonical record is `01_doctrine/brand_identity.md`: builders-first strategy, essence and master tagline "Build with light.", supporting line "The era of intelligence, built with light.". The mark is Summit Sun (locked 2026-07-05; approved drafts in `01_doctrine/brand_assets/`). Palette is Summit Night / Alpenglow / Laser Violet (AA-checked); type is Space Grotesk / Inter / Space Mono. Usage rules live in `01_doctrine/brand_guidelines.md`; practice research in `01_doctrine/branding_best_practices.md`. PT-6 closed 2026-09-22. `04_tools/brand_tokens.py` is built from the tokens block and self-tests against it. The seven brand fonts are cut and documented in `01_doctrine/brand_assets/fonts/`. The Summit Sun mark is drawn from its locked construction spec in both the PDF and the HTML. The identity doc now carries its own origin record; the brief and creation plan were folded in and retired.
- **GitHub:** in progress (PT-8). Target: private `photon-mountain` under the **Colorado-Startups** org, created 2026-09-21. The earlier Colorado-AI target was unreachable: Paul is an outside collaborator there, not a member, so he cannot create repos in that org. Plan and status: `00_project_system/github_setup_plan.md`.
- **Colorado AI cleanup:** done 2026-07-05. The Photon Mountain concept is cleared from the Colorado AI Cowork project and repo (record in `TRANSFER_PLAN.md`).

## Voice

Plain and direct, one idea per sentence. No em dashes, ever (use commas, semicolons, periods, or parentheses). Honest framing: name what is operating today versus what opens in 2026 versus what is on the horizon. Attribute every figure to a credible source or label it a goal; do not invent figures, and search before stating any current status. Full conventions in `01_doctrine/voice.md`. The tone layer locked with the identity on 2026-07-05: inspire by showing, speak to the builder, warm-technical, horizon statements labeled. The full version, with the lexicon and boilerplate, is in `01_doctrine/brand_identity.md`.

## Hard rules

- Do not invent figures, institutions, or quotes. The corridor's credibility is its honesty. Search and attribute.
- Keep the honesty guardrails on the corridor facts. An operating fab is not the same as one opening in 2026. NLR is "formerly NREL" on first reference. The Colorado Photonics Industry Association figures are the association's figures. Photonic compute is emerging, not shipping at scale.
- Free tools only unless decided otherwise.
