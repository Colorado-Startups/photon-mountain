# Photon Mountain · GitHub Setup Plan

*Rewritten 2026-09-22. The 2026-07-05 version named the wrong org, the wrong home directory, and assumed permissions Paul does not have. This version is the live plan for PT-8. Sibling record: `../TRANSFER_PLAN.md` (the founding spin-out record).*

## Goal

A private `photon-mountain` repository under the **Colorado-Startups** org, carrying the full project tree, with the doctrine gates running as CI and as a local pre-commit hook.

## Status

- **Org:** `Colorado-Startups` created by Paul 2026-09-21. Free plan, Paul is an active admin, `members_can_create_repositories` is true. The name `photon-mountain` is available.
- **Sequencing:** brought forward from last by Paul on 2026-09-21, superseding the 2026-07-05 "runs last" decision. PT-6 closed first, so the repo captures an on-brand pipeline instead of a stale one.
- **Pre-flight:** done 2026-09-22. File ownership fixed, content triage complete, deliverables regenerated.

## The two constraints that shape this plan

**Paul cannot create repos in the Colorado-AI org.** His membership there reports `state: inactive, role: unaffiliated, direct_membership: false`. He has admin on the `colorado-ai` repo as an **outside collaborator**, which does not carry repo-creation rights. This is why the target moved to Colorado-Startups.

**A private repo in a Free org could not enforce anything server-side.** That was the 2026-09-22 premise. *Superseded 2026-11-12:* the org API now reports plan `enterprise`, and an org ruleset has protected `main` since 2026-11-02. At go-public (PT-9) a repo ruleset made `voice-check`, `secret scan` and `DCO` required checks, and GitHub's secret scanning and push protection turned on. Public repos also get unlimited use of standard runners, per GitHub's billing documentation.

## Division of labor

The folder is the source of truth. Paul edits files; Claude Code owns git (init, commits, branches, push). A push to a remote needs Paul's explicit approval before it runs.

## The plan

### Step 1 · Pre-flight (done 2026-09-22)

- File ownership corrected. The tree was owned by the `soulcraft` macOS account with 23 files at mode `0600`, unreadable to the account that runs git, which would have failed `git add`.
- Content triage complete: spent files deleted, process docs consolidated, the Colorado AI "Why and How" guide rewritten native.
- `.gitignore` covers `local/`, `__pycache__/`, `.venv/`, `.claude/settings.local.json`, and OS files.
- Nothing sensitive sits outside `local/`, which is empty and gitignored.

### Step 2 · Licensing, before the first commit

The repo carries three different kinds of material and needs a per-path scheme. One blanket license is not legally available, because the corridor map data is derived from OpenStreetMap.

| Path | License |
|---|---|
| Prose and doctrine | CC0 1.0 |
| `03_deliverables/maps/` data files | ODbL 1.0, with OpenStreetMap attribution |
| Rendered map images | CC0 1.0, with the OSM credit (ODbL Produced Works) |
| Code | CC0 1.0 OR 0BSD |
| Name, wordmark, Summit Sun, palette | Not reserved |

Relicensed 2026-11-12 per Paul: "as lenient as possible for everything." The table first shipped as CC BY 4.0, MIT and a reserved brand. `LICENSING.md` is current.

`MAP_NOTES.md` records that the corridor centerlines were traced from OpenStreetMap via the OSRM router, and that many markers sit at OSM building centroids. Under the OSM Foundation's Produced Work guideline, the `.geojson` and `.kml` are a **Derivative Database**, since they are intended for extraction of the data. That binds them to ODbL share-alike. The rendered `.png` and `.pdf` images are Produced Works and can be licensed freely.

**Open compliance item:** the four data files carry no OpenStreetMap attribution today. The HTML and JSX credit OSM, but only for their basemap tiles, which is a different obligation. ODbL requires both attribution and the license text or a link to it, placed where a user would look.

### Step 3 · Repo and first commit

1. `git init -b main`.
2. First commit: `Initial commit: Photon Mountain spun out of Colorado AI (2026-06-22)`.
3. **Stop for Paul's approval.** A push to a remote is his call.
4. `gh repo create Colorado-Startups/photon-mountain --private --source=. --remote=origin --push`
5. Verify `local/`, `.venv/`, `__pycache__/`, and `.DS_Store` are absent from the remote, and that the working tree is clean.

### Step 4 · The GitHub layer

One PR against the fresh `main`, so the repo's own review flow runs from day one. Every action pinned to a commit SHA.

| Workflow | Trigger | Behavior |
|---|---|---|
| `voice-check.yml` | pull request | Runs the same hook script the local harness runs, on changed Markdown. Required since 2026-11-12; fails only on a voice FAIL. |
| `lint-selftest.yml` | push, pull request on `04_tools/**` | `voice_lint.py --self-test` and `brand_tokens.py --self-test`. Blocking: the gates must be trustworthy. |
| `marker-parity.yml` | pull request on `03_deliverables/maps/**` | The 53-marker four-file invariant. |
| `comparison-map-verify.yml` | pull request on `03_deliverables/infographics/**` | `photon_mountain_map_verify.py`. Needs matplotlib. |
| `secret-scan.yml` | pull request, weekly | The gitleaks **binary**, not `gitleaks-action`, which requires a license key for organization-owned repos. |

Plus `.githooks/pre-commit`, issue and PR templates, `CODEOWNERS`, `dependabot.yml` scoped to GitHub Actions only, `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, labels, and a Projects board mirroring `tasks.md`.

**Pre-commit policy**, set after research into current practice. Block on `em-dash`, a literal character test with no false positives. Warn on `unattributed-figure`, which the lint's own docstring calls a heuristic. Fail open when the script or Python is missing, because "could not verify" is not "verified and red". Advertise `--no-verify` in the failure message. A `PreToolUse` hook denies `--no-verify` to Claude while leaving it available to Paul, so the human keeps the judgment call and the agent cannot route around the gate.

*Amended 2026-10-08.* `voice_lint.py` was adopted from Claude-OS, which regraded `spaced-en-dash` to FAIL and `unattributed-figure` to WARN. The hook now blocks on any FAIL the lint assigns and no longer names `em-dash`, so the lint alone owns the grades. Figures still warn, as decided above. A spaced en dash now blocks too.

### Step 5 · The Claude layer

`.claude/` carrying the three pm- skills moved from `04_tools/skills/`, two hooks wrapping `voice_lint.py`, two slash commands, and one reviewer subagent. CI invokes the same hook scripts, so the gate has one definition and three call sites. Those are the local harness, the pre-commit hook, and CI. Hooks are invoked as `bash <hook>`, never by exec bit, so a checkout that strips the bit cannot silently disable them.

### Step 6 · Claude Code GitHub App

`claude setup-token`, then `/install-github-app` from an interactive session. Authenticate with `CLAUDE_CODE_OAUTH_TOKEN` so runs bill against the existing Claude subscription, not a separate API key. Two things to know going in. The Claude GitHub App grants eleven permissions all-or-nothing. Public repos run on standard runners without the private-repo minute allowance, per GitHub's billing documentation. Cap every run anyway with `--max-turns`, a job timeout, and a concurrency group. On a public repo, also limit any `@claude` trigger to users with write access.

## Definition of done

The private repo exists under Colorado-Startups, `main` holds the full tree, `local/` and `.venv/` are absent from the remote, the gates run locally and in CI, and `tasks.md` plus the `CLAUDE.md` Status record the repo URL.

## After this plan

PT-7 (packaging) is optional. PT-9 (go public) waited on the roster row-by-row re-verification, which closed 2026-10-08; it ran 2026-11-12. Git conventions from here: Claude Code commits and pushes, substantive changes go through branches and pull requests.
