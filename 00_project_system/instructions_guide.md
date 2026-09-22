# Instructions guide
*How to write and update the Photon Mountain project instructions. Created 2026-07-05 (PT-2), per section 3.1 of `project_system_plan.md`.*

## What the instructions are

The Cowork Settings > Instructions field is a behavioral contract, not documentation. Every line must change how Claude behaves in a session. Anything that does not change behavior gets cut.

## The router pattern

- The Instructions field is the short version. `CLAUDE.md` is the router and the source of truth.
- The field points to `CLAUDE.md`; it never contradicts it. If the two disagree, the field is wrong; fix it.
- `cowork_project_instructions.md` in the project root mirrors the field exactly. Edit the mirror first, then paste the body into Settings. Never let the mirror and Settings drift apart silently; the change log below tracks the gap.

## Length budget

Target under 500 words for the field body. Models follow a limited budget of distinct instructions per context; short and specific beats long and complete. If a new line is worth adding, look for an old line to cut.

## Ordering

The field body keeps this order: identity (what the project is), scope (geography and photonics focus), voice, hard rules, how to work.

## Non-negotiable rules

These lines never leave the field, and no edit may soften them:

- No em dashes, ever.
- Do not invent figures, institutions, dates, or quotes; attribute or label as a goal.
- Search before stating any current status.
- Keep the corridor honesty guardrails (operating versus opening-2026 framing, "formerly NREL" on first reference, association figures attributed, photonic compute framed as emerging).

## Pre-edit checklist

Run before any edit to the mirror ships:

1. Does the new line conflict with `CLAUDE.md`? If yes, resolve there first.
2. Does it duplicate something already in the field? If yes, merge or drop it.
3. Is it phrased as an instruction (changes behavior) rather than background? If background, cut it or move it to `project_context.md`.
4. Is the body still under the length budget?
5. Log the change in the mirror's `## Change log` section and check the counter (protocol below).

## Change-counter protocol

The mirror file ends with a `## Change log` section. The rules:

- Each editing session that changes the mirror body appends one dated one-line entry, however many lines moved in that session.
- The section carries a counter line: `Changes since last paste into Cowork Settings: N of 7`. Each logged session increments N by one.
- When N reaches 7, the session stops and prompts Paul to paste the body into Settings > Instructions, then resets N to 0.
- Any session may prompt earlier if an edit is urgent (a hard rule changed); paste and reset then.
- The change log lives below the paste line, so it never gets pasted into Settings.
