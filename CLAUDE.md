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
AGENTS.md            Operating manual for AI agents and automated contributors
CONTRIBUTING.md      Setup, the gates, branches, labels, licensing
SECURITY.md          Reporting, what is in place, known gaps
LICENSE              CC0 1.0 (everything Colorado Startups owns)
LICENSES/            CC0 1.0, 0BSD, ODbL 1.0 and Apache 2.0 full texts, and Git Crafter's NOTICE
LICENSING.md         CC0 1.0 (code: CC0 1.0 OR 0BSD), and the exceptions
CODE_OF_CONDUCT.md   Contributor Covenant 3.0, adapted (CC BY-SA 4.0)
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
  colorado_photonics_companies.md   Company roster
  photonics_why_and_how.md, energy_why_and_how.md, manufacturing_strategy.md,
  ai_compute_by_function.md, rocky_flats_restoration_brainstorm.md
03_deliverables/
  infographics/      The launch infographic, the comparison maps, and the vision infographic
    BUILD.md         How to regenerate, and what to check on every build
    photon_mountain_vision_build.py  Generates the vision page; `--check` audits the result
  maps/              The definitive corridor boundary and marker atlas
    MAP_NOTES.md     Method, sources, locked conventions; read before editing the map
04_tools/            The gates, all standard library, all with --self-test
  voice_lint.py      Dashes, sentence length, hedges, AI tells, unattributed figures (vendored from Git Crafter; edit it there)
  brand_tokens.py    The single source of brand values in code; checks itself against brand_identity.md
  marker_parity.py   The corridor atlas's four files must carry the same 53 markers
  voice_exempt.txt   Files the voice gate skips, as data, with a contract test in the hook's --self-test
.claude/             Travels with the repo
  skills/            pm-voice-check, pm-fact-guardrails, pm-task-closeout, pm-design-check
  hooks/             pm-check-voice.sh (the shared gate, --self-test), pm-check-facts.sh,
                     pm-on-edit.sh (PostToolUse router), pm-guard-bypass.sh
  commands/          /pm-voice-check, /pm-end-task
  agents/            pm-voice-reviewer (the judgment half of the voice gate)
  settings.json      Permissions and the PreToolUse bypass guard
.githooks/pre-commit The local voice and secret gate (--self-test)
.github/             Workflows, the cloud-test allowlist, issue and PR templates, CODEOWNERS, dependabot
requirements.txt     Build dependencies (the doctrine tooling needs none)
local/               Gitignored operational files
```

## Status (updated 2026-11-12)

- **Project system:** stood up 2026-07-05 (PT-2). The work queue is `00_project_system/tasks.md`; the task lifecycle is `00_project_system/task_protocol.md`; the instructions mirror carries a change counter per `00_project_system/instructions_guide.md`; memory conventions are in `00_project_system/operating_notes.md`. The plan and PT sequence stay in `project_system_plan.md`. PTs renumbered to execution order 2026-07-05. PT-6 closed 2026-09-22. PT-7 closed 2026-10-08 as a recorded skip, with the Cowork mechanism settled by documentation. PT-8, the GitHub repo, has two leftover steps. PT-9 closed 2026-11-12: the repo is public and open to contributors, with a weekly triage task (`photon-mountain-triage`).
- **Tooling:** built 2026-07-05 (PT-3). `04_tools/voice_lint.py` is the deterministic voice lint (callable by hand and by skills; `--self-test` verifies it). The `pm-voice-check`, `pm-fact-guardrails`, and `pm-task-closeout` skills moved to `.claude/skills/` on 2026-09-22, so they travel with the repo. `pm-design-check` joined them the same day, gating the visual surface the way `pm-voice-check` gates prose. **Cowork and repo skills, settled 2026-10-08: Cowork does not load this repo's `.claude/skills/`.** Anthropic's skills documentation states that Cowork sessions do not read `~/.claude/skills/` and that they load the skills enabled for your claude.ai account, synced at session start. The same page names only cloud sessions as additionally loading project skills from a cloned repository. So the `pm-` skills reach the terminal, the Code tab, and cloud sessions, and reach Cowork only by way of the account. Source: `https://code.claude.com/docs/en/skills`. The upstream request for project-scoped Cowork skills, `anthropics/claude-code#60205`, was closed as not planned. This retires an open question that had been raised twice; the full record, including why the 2026-09-22 observation misled, is in `tasks.md` Done. Cowork does read `CLAUDE.md`, which is the one doctrine surface confirmed to reach every app, so put anything Cowork must know here. Two more gates joined the lint: `brand_tokens.py` and `marker_parity.py`, both with self-tests. The shared shell gate `.claude/hooks/pm-check-voice.sh` gained its own `--self-test` on 2026-10-05, which also asserts that every entry in `04_tools/voice_exempt.txt` still matches a real file. Its call sites are wired, not just described. `pm-on-edit.sh` runs it on every Write and Edit through PostToolUse. The pre-commit hook runs it on staged files, and CI runs it on pull requests. If you change that wiring, change the header comment in the same edit. The pre-commit hook gained its own `--self-test` on 2026-10-08. It commits seeded files through copies of the hook, `pm-check-voice.sh` and the lint, and checks what blocks and what proceeds. The hook runs it when a commit stages any of those files, and `gate-selftests.yml` runs it in CI. `.github/workflows/cloud-test.yml` runs any gate self-test, or a deliverable render, on dispatch (`.github/cloud-test.json` lists the names). `task_protocol.md` stays canonical; if pm-task-closeout ever disagrees with it, the protocol wins and the skill gets updated in the same session.
- **Deliverables:** on-brand and regenerating, as of 2026-09-22 (PT-6). Both build scripts import every color and font from `04_tools/brand_tokens.py`; neither hardcodes a brand value. The launch infographic and both comparison maps were regenerated in the locked identity. The geometry verifier passes with core diameters unchanged at 18.0 and 24.1 miles, which is the proof the re-skin touched styling only. Colorado AI's motto, flag, palette, fonts, and pillar framing are gone from every deliverable. Their claim text was fact gated again on 2026-11-12, before the repo went public, and re-rendered in the cloud. How to rebuild, and what to check: `03_deliverables/infographics/BUILD.md`.
- **Corridor map:** done 2026-07-05, published to Felt 2026-09-22. The definitive boundary and marker atlas lives in `03_deliverables/maps/` (HTML, GeoJSON, KML, JSX; 53 markers, seven two-word categories). Method, sources, and every locked convention are in `03_deliverables/maps/MAP_NOTES.md`; read it before editing the map. The same roster is now a live Felt map, one layer per category, view-only by link. Its boundary there is a simplified display ring; the full trace stays canonical in this repo. Map: https://felt.com/map/Photon-Mountain-the-corridor-built-with-light-OSOsyDNWTDe1acx9BDkkJ4D. Record in `MAP_NOTES.md` Rev 7x.
- **Vision infographic:** published 2026-09-22 as a private Artifact, generated by `03_deliverables/infographics/photon_mountain_vision_build.py`. Light ground (Snowfield) per Paul: the corridor's subject is light, so the field is light. Every accent is the on-light variant. Alpenglow measures 2.90 against Snowfield, so it carries no text at any size. Every graphic is drawn from project data, so a roster change regenerates the page. `--check` bounds every SVG label and scans for off-token hexes. The artifact sandbox blocks third-party frames, so the Felt map is a link and not an embed.
- **Substance:** reframed 2026-07-06 (PT-5). The four Colorado AI seeds are now corridor substance in the locked voice, each with per-doc honesty guardrails and a dated source block (claims searched 2026-07-06 and re-searched 2026-11-12). `lead_abundance.md` was archived 2026-07-06 and deleted 2026-09-22 as Colorado AI candidate-framework material. The three Photon Mountain-native docs got a freshness pass the same day. `02_substance/README.md` is the folder guide (formerly `SEED_README.md`, renamed 2026-07-06). Before any external use, re-run pm-fact-guardrails on the file. **The roster's row-by-row re-verification is done**, closed 2026-10-08 across two passes covering all 58 rows: one row removed, 22 corrected or sharpened, three left flagged. That was the pre-publication step gating PT-9. A delta pass on 2026-11-12 found 19 rows changed and settled Areté in Niwot. Two rows still carry flags rather than claims: ASD's Boulder site and Lever Photonics' entity status. Findings live in the roster itself. The roster spreadsheet was deleted the same day, because it never received the October corrections.
- **Brand:** locked 2026-07-05 (PT-4). The canonical record is `01_doctrine/brand_identity.md`: builders-first strategy, essence and master tagline "Build with light.", supporting line "The era of intelligence, built with light.". The mark is Summit Sun (locked 2026-07-05; approved drafts in `01_doctrine/brand_assets/`). Palette is Summit Night / Alpenglow / Laser Violet (AA-checked); type is Space Grotesk / Inter / Space Mono. Usage rules live in `01_doctrine/brand_guidelines.md`; practice research in `01_doctrine/branding_best_practices.md`. PT-6 closed 2026-09-22. `04_tools/brand_tokens.py` is built from the tokens block and self-tests against it. The seven brand fonts are cut and documented in `01_doctrine/brand_assets/fonts/`. The Summit Sun mark is drawn from its locked construction spec in both the PDF and the HTML. The identity doc now carries its own origin record; the brief and creation plan were folded in and retired.
- **GitHub:** live since 2026-09-22, public since 2026-11-12. `photon-mountain` under the **Colorado-Startups** org: https://github.com/Colorado-Startups/photon-mountain. The earlier Colorado-AI target was unreachable: Paul is an outside collaborator there, not a member, so he cannot create repos in that org. The gates run in three places from one definition: the Claude Code harness on every edit, `.githooks/pre-commit` on every commit, and five CI workflows on every pull request. **Enable the hooks once per clone** with `git config core.hooksPath .githooks`, or none of it runs for you. An org ruleset has protected `main` since 2026-11-02: pull request required, no force push, no deletion. Since 2026-11-12 a repo ruleset also requires `voice-check`, `secret scan` and the DCO app's `DCO` on every pull request. Remaining in PT-8: the Claude Code GitHub App, which needs Paul's `claude setup-token` sign-in, and the Projects board. The token already carries the `project` scope. Plan and status: `00_project_system/github_setup_plan.md`.
- **Voice lint:** adopted from Claude-OS 2026-10-08. Git Crafter (`SoulCraft-Org/git-crafter`) owns `04_tools/voice_lint.py` since 2026-11-12. Change it there by pull request, then copy the merged file here; its first lines name the source commit. The adoption regraded two checks. A spaced en dash now blocks a commit, and an unattributed figure now warns instead of failing. It also added an `ai-tell` warning. The hooks block on any FAIL the lint assigns and name no check, so the lint alone owns the grades.
- **Colorado AI cleanup:** done 2026-07-05. The Photon Mountain concept is cleared from the Colorado AI Cowork project and repo (record in `TRANSFER_PLAN.md`).

## Which gates fire and which wait

**Compute:** cloud first, the Mac last and small (Paul, 2026-11-02). CI, test suites, builds, browsers, e2e, renders and GPU jobs run in the cloud (`.github/workflows/cloud-test.yml` here). The MacBook Air runs only rare, seconds-long checks, such as one test file or one lint. House rule: `~/.claude/rules/compute.md` (canonical: Git Crafter `rules/compute.md`), which wins any disagreement.

`.claude/settings.json` is the authority on the harness wiring, and each workflow's `on:` block on the CI wiring.

| Gate | When | Blocking |
| --- | --- | --- |
| `.githooks/pre-commit` | **Fires** on every commit, once the clone has run `git config core.hooksPath .githooks`. Runs the voice gate on staged files, a gitleaks scan when gitleaks is installed, and the gate self-tests when a commit stages a gate file | Yes, on a voice FAIL or a failing self-test. The secret scan and voice warnings are advisory |
| Claude Code harness: `.claude/hooks/pm-on-edit.sh` (PostToolUse) and `.claude/hooks/pm-guard-bypass.sh` (PreToolUse on Bash) | **Fire** on every Write and Edit, and on every Bash call | The voice check: no, advisory, since the edit is already saved. The bypass guard: yes, it refuses the pre-commit bypass flag to Claude |
| GitHub Actions `voice-check`, `secret-scan`, `gate-selftests`, `marker-parity`, `comparison-map-verify` | **Fire** on pull requests and on pushes to `main` (`gate-selftests` on a push to any branch). `gate-selftests`, `marker-parity` and `comparison-map-verify` fire only when their paths change; `secret-scan` also runs weekly | `voice-check` and `secret scan` are required on every pull request, with the DCO app's `DCO`. `voice-check` fails only on a voice FAIL. The three path-filtered workflows stay advisory, because a required check that never starts leaves a pull request pending |
| GitHub Actions `cloud-test` (`.github/workflows/cloud-test.yml`, a caller of the shared workflow in Colorado-Startups/.github) | **Waits** for a dispatch: `gh workflow run cloud-test.yml --ref <branch> -f script=<name>` runs a name from `.github/cloud-test.json` on a hosted runner. **Fires** on a pull request that changes the caller or the allowlist | No, advisory |

## Voice

Plain and direct, one idea per sentence. No em dashes, ever (use commas, semicolons, periods, or parentheses). Honest framing: name what is operating today versus what opens in 2026 versus what is on the horizon. Attribute every figure to a credible source or label it a goal; do not invent figures, and search before stating any current status. Full conventions in `01_doctrine/voice.md`. The tone layer locked with the identity on 2026-07-05: inspire by showing, speak to the builder, warm-technical, horizon statements labeled. The full version, with the lexicon and boilerplate, is in `01_doctrine/brand_identity.md`.

## Hard rules

- Do not invent figures, institutions, or quotes. The corridor's credibility is its honesty. Search and attribute.
- Keep the honesty guardrails on the corridor facts. An operating fab is not the same as one opening in 2026. NLR is "formerly NREL" on first reference. The Colorado Photonics Industry Association figures are the association's figures. Photonic compute is emerging, not shipping at scale.
- Free tools only unless decided otherwise.
