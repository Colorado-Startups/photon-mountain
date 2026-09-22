# Contributing

Photon Mountain is a place brand for Colorado's computing-with-light corridor. The repository holds doctrine, corridor substance, and deliverables. It is not an application.

The project is solo-maintained today. These conventions exist so it stays coherent as that changes.

## Setup, once per clone

```bash
git config core.hooksPath .githooks
```

**Do this first.** Without it the pre-commit gate does not run for you, and the repo is private on a Free-tier organization, which means GitHub cannot enforce a required status check either. Until the repo goes public, that hook is the only gate that actually stops anything.

For the deliverable build scripts only:

```bash
python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt
```

The doctrine tooling in `04_tools/` is standard library by design and needs none of that.

### Quieting Claude Code in this project

If you use Claude Code here and your account has a large set of claude.ai connectors, they load into every session and crowd the context. Three settings turn that off **for Claude Code only**, leaving Chat and Cowork untouched. They go in `.claude/settings.local.json`, which is gitignored and per-user:

```json
{
  "disableClaudeAiConnectors": true,
  "syncClaudeAiSkills": false,
  "syncClaudeAiPlugins": false
}
```

This cannot be committed for you. A `false` for the two `sync` keys is explicitly ignored in the shared `.claude/settings.json`; only the local file or your user settings work.

## The gates

Three scripts, all with `--self-test`:

| Script | Checks | Needs |
|---|---|---|
| `04_tools/voice_lint.py` | Em dashes, sentence length, hedges, unattributed figures | nothing |
| `04_tools/brand_tokens.py` | Code matches `brand_identity.md`; contrast; fonts resolve | nothing |
| `04_tools/marker_parity.py` | The corridor atlas's four files agree | nothing |

Plus `03_deliverables/infographics/photon_mountain_map_verify.py`, which checks the **comparison maps'** geometry and needs matplotlib. It does not check the corridor atlas; `marker_parity.py` does.

### What blocks and what warns

The pre-commit hook **blocks** on an em dash. That is a literal character test with no false positives, so it is enforced absolutely.

It **warns** on unattributed figures and every style finding. The figure check is a heuristic by the lint's own description, and blocking on a heuristic just teaches people to bypass the hook.

It **fails open** if it cannot run at all. A missing interpreter is not a doctrine violation.

The escape hatch is `git commit --no-verify`, documented in the hook's own failure message. It is yours to use with judgment. A `PreToolUse` hook denies it to Claude, so the agent cannot route around a gate it dislikes while you still can.

## The rules

1. **No em dashes, ever.**
2. **Every figure names a credible source or is labeled a goal.** Never invent one.
3. **Search before stating any current status.** Do not recall it.
4. **Keep the three clocks apart:** operating today, opening in 2026, on the horizon.
5. **No Colorado AI carryover:** not the motto, the pillars, the palette, or the fonts.
6. **No hardcoded brand values.** Import from `brand_tokens.py`.

Full conventions: `01_doctrine/voice.md`. If this file and that one disagree, that one wins.

## Branches, commits, and pull requests

Branch from `main`. Prefix by intent: `setup/`, `doctrine/`, `substance/`, `deliverable/`, `tooling/`, `fix/`.

Write commit messages that will still be useful in a year. Say what changed, what was decided, and what was found. "Update docs" is worthless; the initial commit in this repo is the house style.

Open a pull request even when working alone. The template's checklist is the gate record, and the PR is where the reasoning lives after the branch is gone.

## Issue labels

| Label | For |
|---|---|
| `fact-correction` | A corridor claim is wrong, stale, or unsourced. The highest-value issue here. |
| `tooling` | Build pipeline, gate scripts, CI. |
| `doctrine` | Voice, brand, or project-system changes. |
| `substance` | Corridor content and sources. |
| `deliverable` | Infographics and maps. |

## The work queue

`00_project_system/tasks.md` is the source of truth. The GitHub Projects board mirrors it; it does not replace it. If the two disagree, the file wins, and the board needs fixing.

The task lifecycle is `00_project_system/task_protocol.md`. A task is not done until its gates pass and a dated entry lands in `tasks.md` saying what was actually found.

## Licensing

Contributions are accepted under the licenses in `LICENSING.md`: CC BY 4.0 for prose, MIT for code, ODbL 1.0 for the corridor map data. The map data is different because it derives from OpenStreetMap; read that section before touching `03_deliverables/maps/`.

The name and the Summit Sun mark are reserved. See `TRADEMARKS.md`.
