# Photon Mountain: Spin-Out Transfer and Setup Plan
*Created 2026-06-22. **Closed 2026-07-05.** The transfer is complete: files moved and copied, project scaffolded, Cowork project connected, and the Colorado AI cleanup done. The one remaining item (verifying the repo's first commit holds the full tree) was handed to `00_project_system/github_setup_plan.md` and is no longer this plan's. This file stands as the founding record.*

## The split, in one line

**Colorado AI** stays the statewide AI movement (policy across all of Colorado, including the Lead-pillar substance: photonic chips, renewable and fusion energy, and quantum for materials breakthroughs). **Photon Mountain** becomes its own project: the Boulder, Golden, Denver, Longmont corridor, focused specifically on photonics (chips, processors, interconnects, solar, sensors, laser fusion). The Photon Mountain *concept and brand* leave Colorado AI; the *substance* is shared, so Colorado AI keeps its copies and Photon Mountain gets its own to grow independently.

This means the work is three things, not one:
1. **Move** the Photon Mountain identity and deliverables out (they belong to the new project).
2. **Copy** the shared compute substance as seed material (Colorado AI keeps the originals).
3. **Build fresh** everything Colorado-AI-specific that should not carry over (brand, project scaffolding).

A fourth piece, scrubbing the Photon Mountain concept out of Colorado AI, is a separate follow-on tracked at the end.

## Your decisions, locked

| Decision | Your call |
|---|---|
| Shared substance | Colorado AI keeps it; Photon Mountain gets independent copies |
| Project depth | Full standalone Cowork project and GitHub repo |
| Brand | Fresh identity; do not carry over the Colorado AI look |
| Folder access | Granted (folder now connected) |
| Quantum scope | Photonic quantum only (optics, the photonic-IC fab); broad quantum-materials stays Colorado AI |
| Core corridor | Boulder, Golden, Arvada, Denver (Longmont in the greater ring), matches the current maps |
| Rendering | Start visually blank; carry no Colorado AI fonts or colors |
| Lead wording | Keep the materials idea documented in Colorado AI (already is); no exact-phrase mandate |
| GitHub repo | Private `photon-mountain` under the Soul-Craft org |

## Decisions resolved (2026-06-22)

- **Quantum:** photonic quantum only. Photon Mountain carries quantum optics and the photonic-IC fab as light-based work; the broad quantum-materials-discovery story stays with Colorado AI. So Colorado AI's `quantum_why_and_how.md` is **not** copied wholesale; only the photonic-quantum threads are woven into Photon Mountain's photonics doc and corridor facts.
- **Core corridor:** Boulder, Golden, Arvada, Denver, with Longmont in the greater ring. This is already what the current maps show, so the maps transfer as-is with no geography rework needed.
- **Rendering:** start visually blank. No Colorado AI fonts or colors are copied. The already-rendered `.pdf` and `.png` outputs still move and still display; the build scripts simply need Photon Mountain's own fonts and colors before they can be re-run.
- **Lead wording:** the materials idea is already documented in Colorado AI canon (`ai_compute_by_function.md`, `quantum_why_and_how.md`), so no exact-phrase mandate; the cleanup pass will just make sure a close equivalent stays in place.
- **Repo:** private `photon-mountain` under the Soul-Craft org.

## What transfers (the manifest)

### Bucket A: Photon Mountain's own files (move)

From `Colorado AI/04_deliverables/infographics/`, the eleven Photon Mountain files:

- `photon_mountain.html`, `photon_mountain.pdf`, `photon_mountain.png` (the launch infographic and its renders)
- `photon_mountain_build.py` (the reportlab source for the infographic)
- `photon_mountain_vs_silicon_valley.html`, `photon_mountain_vs_silicon_valley_core.html` (the two comparison-map cuts)
- `photon_mountain_vs_silicon_valley_preview.png`, `photon_mountain_vs_silicon_valley_core_preview.png` (the map previews)
- `photon_mountain_map_generator.py`, `photon_mountain_map_verify.py` (the map build and check scripts)
- `photon_mountain_map_README.md` (the locked-decisions source of truth for the maps)

These land in `Photon Mountain/03_deliverables/infographics/`. The `__pycache__` is skipped.

### Bucket B: Shared substance (copy as seed, then reframe)

Copied from Colorado AI so Photon Mountain can stand alone. Colorado AI keeps every original. Each carries Colorado AI voice and Lead-pillar framing today, so each needs a reframing pass to the corridor and the photonics focus (a content task in the new project, not part of the copy).

- `02_framework/photonics_why_and_how.md` (the core Photon Mountain substance: how AI runs on light)
- `02_framework/energy_why_and_how.md` (solar and laser-fusion energy)
- `02_framework/manufacturing_strategy.md` (the chips-manufacturing story)
- `02_framework/lead_abundance.md` (the abundance framing for a compute economy)
- `02_framework/quantum_why_and_how.md` is **not** copied (decision: photonic quantum only). Its photonic-quantum threads (quantum optics, the photonic-IC fab) get folded into Photon Mountain's photonics doc and corridor facts instead.
- `01_doctrine/ai_compute_by_function.md` (the compute-roles taxonomy: invent / run / power)
- `01_doctrine/why_and_how_guide.md` (the eight-part structure standard these docs follow)
- The corridor facts (NIST/JILA Boulder, the Boulder microfab, Arvada Quantum Commons, Mines, NLR, Marvel Fusion ATLAS, Lightwave Logic, CPIA figures): I will assemble these into a fresh `02_substance/corridor_facts_and_sources.md` rather than copy Colorado AI's whole `sources_and_research.md`, keeping only what is corridor-relevant and preserving the honesty guardrails (operating vs opening-2026 fabs, "formerly NREL," attributed CPIA counts).

### Bucket C: Build fresh, do not carry over

Per your "fresh identity" call, none of the Colorado AI visual brand moves:

- No logos, banners, wordmarks, the Colorado-flag mark, or favicons.
- No brand canon: `brand_identity_locked.md`, `brand_tokens.yaml`, `brand_application_kit.md`, `cheat_card.md`, `font_guide.md`, `icon_guide.md`, `icons_for_claude.md`, the `icons/` set.
- No Colorado AI motto, pillars, or candidate-facing rules.
- No `colorado-ai-*` hooks, skills, commands, or subagents (they are namespaced to that project).

Instead I seed a `01_doctrine/brand_brief.md` stub that frames the fresh identity to be designed (the photon/light concept, the anti-Silicon-Valley positioning, a place brand), plus a slim `01_doctrine/voice.md` carrying only the general writing conventions that are yours rather than Colorado AI's (plain and direct, no em dashes, honest framing, complete-sentence closers). Both are clearly marked as starting points, not locked.

**One technical note (decision: start visually blank).** The two build scripts (`photon_mountain_build.py`, `photon_mountain_map_generator.py`) embed Colorado AI colors (turquoise, pine green, flag gold) and fonts (IBM Plex Serif, Work Sans, JetBrains Mono). Per your call, no fonts or tokens are copied. The already-rendered outputs (`photon_mountain.pdf`, `.png`, and the two map `_preview.png` files) still move and still display, and the HTML files carry their own inline CSS so they open in a browser as-is. The Python scripts, however, will not re-render until Photon Mountain picks its own fonts and colors. So the new project gets a short `03_deliverables/infographics/RESKIN_NEEDED.md` note flagging that the scripts carry Colorado AI styling and must be re-pointed at the fresh identity before regeneration.

## Proposed Photon Mountain project structure

```
Photon Mountain/
  CLAUDE.md                     Router and project rules (fresh, Photon-Mountain-specific)
  README.md                     What this project is
  project_context.md            Five-minute overview
  TRANSFER_PLAN.md              This file
  .gitignore
  00_project_system/            Lightweight operating notes + a task log
  01_doctrine/
    brand_brief.md              Fresh-identity brief (to be designed)
    voice.md                    General writing conventions
    why_and_how_guide.md        (copied) the structure standard
  02_substance/
    photonics_why_and_how.md    (copied, to reframe)
    energy_why_and_how.md       (copied, to reframe)
    manufacturing_strategy.md   (copied, to reframe)
    lead_abundance.md           (copied, to reframe)
    (quantum_why_and_how.md deliberately NOT copied: photonic quantum only)
    ai_compute_by_function.md   (copied)
    corridor_facts_and_sources.md  (fresh, assembled from verified corridor facts)
  03_deliverables/
    infographics/               the eleven Photon Mountain files
  archive/
  local/                        gitignored, operational files
```

This mirrors Colorado AI's numeric-prefix convention so it feels familiar, but it is trimmed to what a one-person place-brand project needs. Adjustable.

## Complete Photon Mountain reference audit (verified 2026-06-22)

I swept the whole Colorado AI repo (excluding the `.git` and `.claude/worktrees` duplicate trees), plus the website and the memory layer. Every reference to the Photon Mountain *concept* falls into one of three groups. The photonics *substance* (photonic chips, interconnects, quantum, energy) is a separate thing and stays in Colorado AI; it is not in this list.

**Group 1: files that ARE Photon Mountain (move out).** All in `04_deliverables/infographics/`:
`photon_mountain.html`, `photon_mountain.pdf`, `photon_mountain.png`, `photon_mountain_build.py`, `photon_mountain_vs_silicon_valley.html`, `photon_mountain_vs_silicon_valley_core.html`, `photon_mountain_vs_silicon_valley_preview.png`, `photon_mountain_vs_silicon_valley_core_preview.png`, `photon_mountain_map_generator.py`, `photon_mountain_map_verify.py`, `photon_mountain_map_README.md`. (The `__pycache__/*.pyc` is a regenerable cache, skipped.)

**Group 2: concept references inside files that STAY in Colorado AI (edit during cleanup, do not move):**
- `01_doctrine/glossary.md`: section 11 "Photon Mountain (the ecosystem name)". Delete the section; keep Compute-vocabulary sections 1 to 10.
- `01_doctrine/brand_identity_locked.md`: the "Ecosystem name" section. Delete it.
- `04_deliverables/CLAUDE.md`: the folder listing of the `photon_mountain.*` pieces. Remove those lines once the files move.
- `00_project_system/cowork_task_plans_lead.md`: lines 7, 127, 129, 171 (the #6 identity task history and a "read first" pointer). These are completed-task history; annotate as "spun out to the Photon Mountain project 2026-06-22," do not delete the record.
- `00_project_system/cowork_task_plans_deliverables.md`: tasks #18 and #19 history. Same: annotate, keep the record.
- `.gitignore`: line 37, the Photon Mountain map-generator scratch-preview ignore rule. Remove once the files are gone.

**Group 3: the memory layer (Cowork auto-memory, edit during cleanup):**
- `colorado-ai-photon-mountain.md`: the concept's main memory. Retire it from Colorado AI (or rewrite to a one-line "spun out to the Photon Mountain project; see that repo").
- `colorado-fusion-facilities.md`: references the corridor; light edit to drop the Photon Mountain framing.
- `MEMORY.md`: index line 70 (the Photon Mountain entry). Remove or repoint.

**Confirmed clean (no concept references):** the root `CLAUDE.md`, `project_context.md`, `cowork_project_instructions.md`, the entire `site/` website, and all candidate-pack deliverables. The split does not touch them.

## Lead-pillar substance: verified still present in Colorado AI

You asked me to confirm Colorado AI's Lead pillar still carries the substance after Photon Mountain leaves. It does, and none of the substance lives in a file that the cleanup touches. Evidence:

- **Photonic chips, processors and interconnects.** `01_doctrine/ai_compute_by_function.md` has "Photonic processor (emerging)" in the do-the-thinking layer and "Interconnect (NVLink, photonic and optical)" in the connect-the-brains layer, and its closing section names photonics as the Lead pillar's near-term win (interconnects) and next bet (optical compute). The root `CLAUDE.md` North-star bullet says "photonic chips that compute and move data with light."
- **Renewable energy now: solar, geothermal, wind.** `02_framework/energy_why_and_how.md` leads with "wind, solar, storage, and geothermal" and frames "The renewable layer is now." Geothermal was added and fact-checked 2026-06-22, with the honest caveat that Colorado's geothermal lead today is strongest in heating, not yet a fleet of power plants.
- **Unlimited energy later: fusion.** Same doc puts "fusion next" in the horizon column ("Wind, sun, storage, and geothermal now, fusion next, all of it built here").
- **Quantum to invent the materials implemented statewide.** `ai_compute_by_function.md` section 7 and its "invent it" layer cast quantum as "the discovery engine that can simulate molecules and materials beyond classical reach, and so help design better chips and better energy"; full role in `02_framework/quantum_why_and_how.md`.

**One small wording flag.** The substance is all there, but the literal phrase "materials science" does not appear in canon; the idea is written as "simulate molecules and materials" and "design better chips and energy." If you want the exact phrase "quantum systems to invent the material science implemented statewide" in the Lead copy, that is a one-line wording add to `ai_compute_by_function.md` and/or the `CLAUDE.md` Lead bullet. Say the word and I will fold it into the cleanup pass.

## Execution sequence

1. **You approve** this plan and answer the three open decisions.
2. **I copy and scaffold** directly into `/Users/soulcraft/Developer/Photon Mountain`: Bucket A, Bucket B, the fresh stubs (Bucket C), and the structure above. I verify the PDF and the map previews render in the new location.
3. **Claude Code sets up GitHub**: `git init`, create the new private `photon-mountain` repo under Soul-Craft, first commit and push. (Per project rules, Claude Code owns commits and pushes, not Cowork.)
4. **You connect Photon Mountain as its own Cowork project** in the desktop app (point a new project at the folder). I will write a short kickoff note for that first session.
5. **First content tasks inside the new project** (not part of the transfer): design the fresh identity, re-skin the build scripts to it, and reframe the copied substance to the corridor and the photonics focus. (The map geography already matches Boulder/Golden/Arvada/Denver, so no map rework is needed.)

## Colorado AI cleanup (separate follow-on)

*Status update 2026-07-05: done. Paul confirmed the Photon Mountain concept has been cleared from the Colorado AI Cowork project and GitHub repo. The paragraph below stands as the founding record of what the cleanup covered.*

Removing the Photon Mountain concept from Colorado AI is its own task, done through Claude Code under the project's rules, and kept separate so the spin-out does not destabilize the live movement before the primary. The exact edit list is the Group 2 and Group 3 inventory above (glossary section 11, the `brand_identity_locked.md` ecosystem-name section, the deliverables `CLAUDE.md` listing, the two Lead/deliverables task-plan history blocks, the `.gitignore` line, and the three memory entries). Note: the concept is NOT in `cowork_task_plans_sweeps.md`, the root `CLAUDE.md`, `project_context.md`, the Settings mirror, or the website, so none of those are touched. The underlying compute substance (photonics, energy, fusion, quantum) stays in Colorado AI, verified above. This cleanup does not block standing up Photon Mountain.

## Verification

*2026-07-05: the repo-related check below now belongs to `00_project_system/github_setup_plan.md`. The folder-side checks passed during the move.*

Before calling the transfer done: confirm all eleven deliverable files are present and the PDF plus both map previews render in the new folder; run `photon_mountain_map_verify.py` and confirm it passes; confirm no Colorado AI brand asset was copied except the flagged interim fonts/tokens; and confirm the new repo's first commit contains the full tree.
