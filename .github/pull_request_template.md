Closes #

<!-- Tables over prose. Delete these comments. -->

| Item | Detail |
|---|---|
| What changed | |
| Why | |
| How it was verified | |
| How to reverse it | |
| Notes for the reviewer | Decisions that could have gone the other way, and scope left out on purpose |

<!-- Tick each check that applies and holds; delete the ones that do not apply. -->

- [ ] Each commit signed off (`git commit -s`), for the DCO check
- [ ] No secret, token, key or personal data in any file
- [ ] User input reaches no HTML, SQL or header unescaped
- [ ] An AI tool wrote part of this, and the table says which part
- [ ] Voice: `python3 04_tools/voice_lint.py` (or `/pm-voice-check`) run on every prose file touched; no em dashes
- [ ] Figures name a credible source or are labeled a goal
- [ ] Facts: a `02_substance/` or current-status claim was re-searched, not recalled, and its source is linked
- [ ] Three clocks kept distinct: operating today, opening in 2026, on the horizon
- [ ] `04_tools/` changed: `voice_lint.py`, `brand_tokens.py` and `marker_parity.py` pass `--self-test`
- [ ] `03_deliverables/maps/` changed: `marker_parity.py` passes and `MAP_NOTES.md` has a revision entry
- [ ] A build script changed: rebuilt, `brand_fonts= True`, `OVERFLOW none`, geometry check passes
- [ ] No Colorado AI carryover: no motto, pillars, turquoise, pine green, flag gold, IBM Plex, Work Sans or JetBrains Mono
- [ ] No brand value hardcoded; colors and fonts come from `04_tools/brand_tokens.py`
- [ ] Own work under CC0 1.0 (code: CC0 1.0 OR 0BSD); third-party work keeps its license and has a row in `LICENSING.md`
- [ ] Corridor map data touched: the OpenStreetMap attribution and ODbL notice are intact
