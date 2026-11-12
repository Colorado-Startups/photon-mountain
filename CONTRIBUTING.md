# Contributing

Photon Mountain is a place brand for Colorado's computing-with-light corridor. The repository holds doctrine, corridor substance, and deliverables. It is not an application.

Colorado Startups maintains it. Claude Code does the day-to-day triage and review, under the rules in `AGENTS.md`. The founder decides questions of brand and vision.

Everyone here follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute, most valuable first

1. **Fact corrections.** A corridor claim is wrong, stale, or missing its source. [Open a fact correction](https://github.com/Colorado-Startups/photon-mountain/issues/new?template=1-fact-correction.yml), or send a pull request with the fix and the source.
2. **Roster additions.** A corridor company that builds with light, energy, or compute and is missing from `02_substance/colorado_photonics_companies.md`. Every row needs a source showing the company exists, does what the row says, and is where the row says.
3. **Map markers.** A missing or misplaced point on the corridor atlas. Read `03_deliverables/maps/MAP_NOTES.md` first, because a marker lives in four files that must agree.
4. **Deliverable fixes.** A broken label, a render bug, or a build script problem.
5. **Tooling.** The gate scripts and CI.

Issues labeled [good first issue](https://github.com/Colorado-Startups/photon-mountain/labels/good%20first%20issue) need only a careful web search.

**The brand is locked.** The identity, voice, and guidelines in `01_doctrine/` change only through a decision record. To propose a change there, open an issue first. A change to the brand itself goes to the founder.

## How a contribution lands

1. Fork the repository and branch from `main`. Prefix the branch by intent: `doctrine/`, `substance/`, `deliverable/`, `tooling/`, `fix/`.
2. Enable the local gate once per clone:

   ```bash
   git config core.hooksPath .githooks
   ```

3. Commit with a sign-off: `git commit -s`. That adds a `Signed-off-by:` line certifying the [Developer Certificate of Origin](https://developercertificate.org/), which the `DCO` check requires. Edits made in GitHub's web editor get the sign-off automatically.
4. Open a pull request. The template's checklist is the gate record.

Forgot the sign-off? Add it to every commit on your branch and push again:

```bash
git rebase --signoff main
git push --force-with-lease
```

Commits by members of the Colorado-Startups organization that GitHub shows as Verified skip the sign-off, per `.github/dco.yml`.

## The checks on a pull request

Three checks must pass before anything merges:

| Check | What it does |
|---|---|
| `voice-check` | Runs the voice lint on the prose you changed. It fails only on an em dash or a spaced en dash. |
| `secret scan` | Runs gitleaks over every commit. |
| `DCO` | Confirms each commit carries a sign-off. |

The rest report and advise: the gate self-tests, the corridor atlas parity check, and the comparison-map geometry check each run when their paths change. On a pull request from a fork, workflows wait until a maintainer approves the run. That is a guard against abuse of the runners, not a judgment on your change.

## The gates

Three scripts, all with `--self-test`:

| Script | Checks | Needs |
|---|---|---|
| `04_tools/voice_lint.py` | Em dashes, spaced en dashes, sentence length, hedges, AI tells, unattributed figures | nothing |
| `04_tools/brand_tokens.py` | Code matches `brand_identity.md`; contrast; fonts resolve | nothing |
| `04_tools/marker_parity.py` | The corridor atlas's four files agree | nothing |

Plus `03_deliverables/infographics/photon_mountain_map_verify.py`, which checks the **comparison maps'** geometry and needs matplotlib. It does not check the corridor atlas; `marker_parity.py` does.

The three shell gates take `--self-test` too: `.githooks/pre-commit`, `.claude/hooks/pm-check-voice.sh`, and `.claude/hooks/pm-guard-bypass.sh`. CI runs all six in `gate-selftests.yml`.

### What blocks and what warns

The pre-commit hook and `voice-check` **block** on any FAIL finding from the voice lint. That means an em dash, or an en dash with a space on each side, which reads as one. Both are literal character tests with no false positives, so they are enforced absolutely. A dash counts even inside inline code or a link; only a fenced code block skips it. A file that has to show the character goes on `04_tools/voice_exempt.txt`, with a reason.

They **warn** on everything else the lint finds: unattributed figures, AI tells, hedges, and long sentences. Each of those checks is a heuristic by the lint's own description, and blocking on a heuristic just teaches people to bypass the gate. A figure warning still needs an answer, because rule 2 below does not soften.

The grades live in `voice_lint.py`, not in the hooks. `voice_lint.py` is a vendored copy, and its first lines name its source commit. Do not edit it here. Propose a change upstream in [`SoulCraft-Org/git-crafter`](https://github.com/SoulCraft-Org/git-crafter) (`tools/voice_lint.py`), then a maintainer copies the merged file in.

The hook **fails open** if it cannot run at all. A missing interpreter, or a crash inside the lint, is not a doctrine violation. The hook says it could not verify and lets the commit through.

The hook **tests itself**. `bash .githooks/pre-commit --self-test` commits seeded files in throwaway repositories, through copies of the hook, `pm-check-voice.sh` and the lint. It checks that each dash blocks, that a figure warns and proceeds, and that a lint crash proceeds with a notice.

The escape hatch is `git commit --no-verify`, documented in the hook's own failure message. It skips the local hook only; `voice-check` still runs on the pull request. A `PreToolUse` hook denies the flag to Claude, so the agent cannot route around a gate it dislikes.

## The rules

1. **No em dashes, ever.**
2. **Every figure names a credible source or is labeled a goal.** Never invent one.
3. **Search before stating any current status.** Do not recall it.
4. **Keep the three clocks apart:** operating today, opening in 2026, on the horizon.
5. **No Colorado AI carryover:** not the motto, the pillars, the palette, or the fonts.
6. **No hardcoded brand values.** Import from `brand_tokens.py`.

Full conventions: `01_doctrine/voice.md`. If this file and that one disagree, that one wins.

## Commits and pull requests

Write commit messages that will still be useful in a year. Say what changed, what was decided, and what was found. "Update docs" is worthless.

Open a pull request even for a small change. The PR is where the reasoning lives after the branch is gone.

## Issue labels

| Label | For |
|---|---|
| `fact-correction` | A corridor claim is wrong, stale, or unsourced. The highest-value issue here. |
| `substance` | Corridor content and sources. |
| `deliverable` | Infographics and maps. |
| `tooling` | Build pipeline, gate scripts, CI. |
| `doctrine` | Voice, brand, or project-system changes. |
| `good first issue` | Doable with a careful search and no setup. |

## The work queue

`00_project_system/tasks.md` is the source of truth. If an issue and that file disagree, the file wins.

The task lifecycle is `00_project_system/task_protocol.md`. A task is not done until its gates pass and a dated entry lands in `tasks.md` saying what was actually found.

## Licensing

By contributing, you license your work under the licenses in `LICENSING.md`: CC BY 4.0 for prose, MIT for code, ODbL 1.0 for the corridor map data. The map data is different because it derives from OpenStreetMap; read that section before touching `03_deliverables/maps/`. Your sign-off certifies you have the right to do so.

The name and the Summit Sun mark are reserved. See `TRADEMARKS.md`.

## Maintainers using Claude Code

This section is for the maintainers' own sessions. A contributor can skip it.

Builds and renders run in the cloud, never on the maintainers' MacBook Air (Paul, 2026-11-02). The build scripts render on a hosted runner through `.github/workflows/cloud-test.yml`, which installs `requirements.txt` there. `03_deliverables/infographics/BUILD.md` has the commands. To run the gate self-tests in the cloud on demand:

```bash
gh workflow run cloud-test.yml --ref <your branch> -f script=selftests
```

If your account has a large set of claude.ai connectors, they load into every session and crowd the context. Three settings turn that off for Claude Code only, leaving Chat and Cowork untouched. They go in `.claude/settings.local.json`, which is gitignored and per-user:

```json
{
  "disableClaudeAiConnectors": true,
  "syncClaudeAiSkills": false,
  "syncClaudeAiPlugins": false
}
```

This cannot be committed for you. A `false` for the two `sync` keys is ignored in the shared `.claude/settings.json`; only the local file or your user settings work.
