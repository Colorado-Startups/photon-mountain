## What this changes

<!-- One or two sentences. What is different after this merges, and why. -->

## Gates

<!-- Tick what applies. An unticked box is fine if it does not apply; an
     unticked box that DOES apply is the thing reviewers should ask about.
     While this repo is private, CI cannot be a required check, so these
     boxes and the pre-commit hook are the real gate. -->

- [ ] **Voice.** `/pm-voice-check` run on every file of prose I touched, and the findings are addressed or explained.
- [ ] **No em dashes.** Commas, semicolons, periods, or parentheses instead.
- [ ] **Figures.** Every figure names a credible source or is labeled a goal.
- [ ] **Facts.** If this touches `02_substance/` or any current-status claim, pm-fact-guardrails was run and the claims were re-searched, not recalled.
- [ ] **Three clocks.** What operates today, what opens in 2026, and what is on the horizon are kept distinct.
- [ ] **Gates self-test.** If `04_tools/` changed: `voice_lint.py`, `brand_tokens.py`, and `marker_parity.py` all pass `--self-test`.
- [ ] **Corridor atlas.** If `03_deliverables/maps/` changed: `marker_parity.py` passes, and `MAP_NOTES.md` has a revision entry.
- [ ] **Deliverables.** If a build script changed: rebuilt, `brand_fonts= True`, `OVERFLOW none`, and the geometry check passes.

## Brand and licensing

- [ ] No Colorado AI carryover introduced: no motto, no pillars, no turquoise, pine green, or flag gold, no IBM Plex, Work Sans, or JetBrains Mono.
- [ ] No brand value hardcoded. Colors and fonts come from `04_tools/brand_tokens.py`.
- [ ] If this touches the corridor map data, the OpenStreetMap attribution and the ODbL notice are intact. See `LICENSING.md`.

## Notes for the reviewer

<!-- Anything you are unsure about, decisions you made that could reasonably
     have gone the other way, or things you deliberately left out of scope. -->
