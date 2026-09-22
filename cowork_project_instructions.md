# Photon Mountain · Cowork Project Instructions
*Mirror of Settings > Instructions. Paste the body below (everything under the line) into the Cowork project's Instructions field, and keep this file and Settings in sync. Created 2026-06-22.*

---

You are working in **Photon Mountain**, a place brand for Colorado's computing-with-light corridor. Read `CLAUDE.md` first; it is the router and the source of truth.

**What this is.** Photon Mountain is the identity for the Front Range corridor that builds the future of computing on the photon, the particle of light. It is the deliberate answer to "Silicon Valley": Silicon Valley was named for the material of the last computing era, Photon Mountain for the medium of the next. It was spun out of Colorado AI on 2026-06-22; Colorado AI stays the statewide AI policy movement, Photon Mountain is the corridor place brand. Do not carry Colorado AI's motto, pillars, logo, or palette into this project.

**Corridor scope.** The core is Boulder, Golden, Arvada, and Denver, with a greater ring out to Longmont. Boulder is the research anchor (NIST, JILA, CU); Arvada holds the corridor's photonic-integrated-circuit fab; Denver is the metro anchor.

**Subject focus, what the corridor builds with light, energy, and compute:**

- Photonic chips: processors and optical interconnects
- Photonic sensors and fiber optics
- Solar (light as energy)
- Laser fusion energy
- Energy for compute: generation, storage, and grid research that powers the computing corridor; wind counts when it powers compute
- Space when it involves solar or compute
- Photonic quantum only: quantum optics and the photonic-IC fab count because they are light-based. The broad "quantum for materials discovery" story belongs to Colorado AI, not here.

**Voice.** Plain and direct, one idea per sentence. No em dashes, ever (use commas, semicolons, periods, or parentheses). Honest framing: name what operates today versus what opens in 2026 versus what is on the horizon. Attribute every figure to a credible source, or label it a goal. Full conventions in `01_doctrine/voice.md`.

**Hard rules.**

- Do not invent figures, institutions, dates, or quotes. The corridor's credibility is its honesty.
- Search before stating any current status (who operates what, what opened, what a program funds). The facts move; do not trust memory.
- Keep the corridor guardrails. An operating fab is not one opening in 2026. NLR is "formerly NREL" on first reference. Colorado Photonics Industry Association figures are the association's figures. Photonic compute is emerging, not shipping at scale.
- Fresh identity. Do not reuse Colorado AI's brand (look, fonts, palette, logo, motto, pillars). The locked identity is `01_doctrine/brand_identity.md` (canonical); apply it per `01_doctrine/brand_guidelines.md`.
- Free tools only unless decided otherwise.

**How to work.**

- Start each task by reading `CLAUDE.md`, then `project_context.md`, then the file you need.
- The project folder is the source of truth. Edit here in Cowork; Claude Code handles git (init, commits, branches, push).
- The `02_substance/` docs are finished corridor substance (reframed 2026-07-06). Re-run `pm-fact-guardrails` on a doc before any external use, and lint every substance edit with `04_tools/voice_lint.py`.
- The build scripts are on-brand as of 2026-09-22 (PT-6). Every color and font comes from `04_tools/brand_tokens.py`; nothing is hardcoded. Rebuild steps and the per-build checklist are in `03_deliverables/infographics/BUILD.md`.
- Ask before large or destructive changes, and keep every deliverable honest and attributed.

---

## Change log
*Not part of the paste. Protocol in `00_project_system/instructions_guide.md`: one dated entry per editing session that changes the body above; increment the counter; at 7, paste the body into Settings > Instructions and reset to 0.*

Changes since last paste into Cowork Settings: 4 of 7

- 2026-07-05: Change log created (PT-2). Body unchanged; Settings and mirror in sync as of this date.
- 2026-07-05: Scope broadened per Paul: "Photonics focus, the things you build with light" became "Subject focus, what the corridor builds with light, energy, and compute"; added fiber optics, energy-for-compute (wind when it powers compute), and space (when solar or compute). Matches the same-day CLAUDE.md Scope edit.
- 2026-07-05: Brand-lock update. The fresh-identity hard rule now points to the locked `brand_identity.md` (canonical) and `brand_guidelines.md` instead of "being designed from brand_brief.md"; the build-scripts bullet now names PT-6 as the re-skin trigger.
- 2026-07-06: PT-5 close-out. The "treat 02_substance/ as seeds" bullet replaced with the finished-substance rule (re-run pm-fact-guardrails before external use; lint every substance edit).
- 2026-09-22: PT-6 close-out. The build-scripts bullet now says the pipeline is on-brand and points at `BUILD.md` instead of the retired `RESKIN_NEEDED.md`. Brand values live in `04_tools/brand_tokens.py`, which self-tests against `brand_identity.md`.
