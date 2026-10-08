# Notes for agents

The operating manual for any AI agent or automated contributor working in this repository: a Claude Code session, a cloud agent, or anything editing through the GitHub web UI without the local hooks.

`CLAUDE.md` is the router and comes first. This file covers what an agent specifically needs to know, and what it specifically must not do.

## What this project is

Photon Mountain is a place brand for Colorado's computing-with-light corridor. It is doctrine, corridor substance, and deliverables, not an application. There is no server, no test suite in the usual sense, and no deploy. The "build" is three Python scripts that render an infographic and two maps.

The project's whole value is that its claims are true. Read that sentence again before changing anything in `02_substance/`.

## The rules that are not negotiable

1. **No em dashes, ever.** Commas, semicolons, periods, or parentheses. An en dash with a space on each side reads as one, so it is out too. The pre-commit hook blocks on both; they are the voice rules it enforces by blocking, because they have no false positives.
2. **Never invent a figure, an institution, or a quote.** If you cannot attribute it, do not write it. A figure with no source is a defect. The lint only warns on an unattributed figure, because its detection is a heuristic. Treat that warning as a defect to fix, not a suggestion.
3. **Search before stating any current status.** The corridor moves in real time. Do not recall a status from training data or from earlier in a conversation; check it.
4. **Keep the three clocks apart.** What operates today, what opens in 2026, and what is on the horizon are three different claims. NIST Boulder's cleanroom operates. The Arvada photonic-IC fab opens. Photonic compute is emerging, not shipping at scale. Blurring these is the most damaging mistake available here.
5. **No Colorado AI carryover.** Photon Mountain does not use that project's motto ("AI to serve all Coloradans"), its three-pillar framing, its logo, its palette (turquoise, pine green, flag gold), or its fonts (IBM Plex, Work Sans, JetBrains Mono). This was violated for months in the deliverables before anyone noticed, so it is worth checking rather than assuming.
6. **Never hardcode a brand value.** Colors and fonts come from `04_tools/brand_tokens.py`.

## Before you open a pull request

Run the gates. They are fast, they need no network, and two of the three are standard library only.

```bash
python3 04_tools/voice_lint.py <files you changed>
python3 04_tools/brand_tokens.py --self-test
python3 04_tools/marker_parity.py          # if you touched 03_deliverables/maps/
```

Enable the local hooks once per clone, or the pre-commit gate will not run for you at all:

```bash
git config core.hooksPath .githooks
```

## Things that will surprise you

- **`04_tools/voice_lint.py` is a synced copy.** Claude-OS owns it, and `.claude-os-managed.json` records the sync. Do not edit it here. An in-place edit reads as `modified` to `claude_os_sync.py status`, and the next sync refuses to overwrite it without `--force`. Change it in Claude-OS and re-sync.
- **`photon_mountain_map_verify.py` does not check the corridor map.** It checks the Silicon Valley comparison maps' geometry. The corridor atlas is checked by `04_tools/marker_parity.py`. An earlier version of the operating notes got this wrong and misled a planning session.
- **The build scripts' y axis increases downward.** Every primitive renders at `PAGE_H - y`. "Above" means a smaller y. A shape drawn with the intuitive convention comes out upside down.
- **The two violets are not interchangeable.** Violet Deep is for text on light grounds, Violet Bright for text on dark. Getting this backwards scores 2.37 against WCAG AA's 4.5 floor and looks completely plausible. `brand_tokens.check_pairing` raises on it; do not work around that.
- **Notes differ between map formats by design.** The HTML and JSX notes are `"<Category>. "` plus the GeoJSON note, because GeoJSON keeps `category` as its own property. That is not drift.
- **Corridor map data is ODbL, not CC BY.** It derives from OpenStreetMap. See `LICENSING.md` before touching `03_deliverables/maps/`.

## What an agent must not do

- **Do not use the pre-commit bypass flag.** A `PreToolUse` hook blocks it for Claude specifically. If a gate objects, fix the finding or say why you think the gate is wrong; do not route around it.
- **Do not touch the Colorado AI repository** from a session working here. They are separate projects with a locked boundary.
- **Do not publish anything externally.** Every external-facing artifact needs Paul's sign-off. Staging it is fine; sending it is not.
- **Do not mark a task done without running its gates** and writing a dated entry in `00_project_system/tasks.md` that says what was actually found.

## Where to look

| You want | Read |
|---|---|
| The router and current status | `CLAUDE.md` |
| The work queue, which is the source of truth | `00_project_system/tasks.md` |
| How a task opens and closes | `00_project_system/task_protocol.md` |
| Writing conventions | `01_doctrine/voice.md` |
| The locked brand and its origin | `01_doctrine/brand_identity.md` |
| Corridor facts and their guardrails | `02_substance/corridor_facts_and_sources.md` |
| How to rebuild a deliverable | `03_deliverables/infographics/BUILD.md` |
| Map method and locked conventions | `03_deliverables/maps/MAP_NOTES.md` |
| Licensing, and why the map data differs | `LICENSING.md` |
