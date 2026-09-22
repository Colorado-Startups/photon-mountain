---
name: pm-fact-guardrails
description: Walk the Photon Mountain honesty and freshness gate against a named file, with a web search for every current-status claim. Use when the user says "fact gate this", "run pm-fact-guardrails on X", "check the guardrails", or before any corridor fact ships externally.
---

# pm-fact-guardrails

The honesty and freshness checks from `00_project_system/task_protocol.md` phase 3, run against one named file. Guardrails source: `02_substance/corridor_facts_and_sources.md` and `01_doctrine/voice.md`. If this skill and those files disagree, those files win.

## When to use

- A file states corridor facts, figures, or institutional statuses and is headed for external use.
- The Task Review honesty or freshness check is being run on new or edited substance.

Do not use for: pure process docs with no factual claims. For voice mechanics, use `pm-voice-check`.

## Inputs

1. The target file path. Ask if not given.

## Step 1: inventory the claims

Read the file and list every checkable claim in two groups:

- **Figures.** Any number presented as fact: counts, dollars, percentages, dates.
- **Current-status claims.** Anything true only as of now: who operates what, what opened, what a program funds, what stage a facility is at.

## Step 2: search every current-status claim

For each current-status claim, run a web search in this session. Recall does not count; the facts move. Record for each:

- The claim as written.
- What the search found, with the source and its date.
- Verdict: confirmed, changed (with the correction), or unverifiable (flag for removal or a goal label).

## Step 3: the guardrail checklist

Check each item against the file:

- Every figure is attributed to a named credible source, or labeled a goal.
- Operating today, opening in 2026, and horizon stay distinct; nothing operating is implied where it is not.
- An operating fab is not framed as one opening in 2026, and the reverse.
- NLR is "formerly NREL" on first reference.
- Colorado Photonics Industry Association figures are presented as the association's figures.
- Photonic compute is framed as emerging, not shipping at scale.
- Boulder is the research anchor; Denver is never framed as the research center.
- The corridor-relevant fusion path is laser (inertial) fusion; magnetic confinement is not claimed as an in-state strength.

## Report

One consolidated report:

- The claim table from steps 1 and 2 (claim, search result, source, verdict).
- Guardrail findings, each with location and a proposed rewrite.
- Verdict: **Clean** (the file holds) or **Fix first** (apply the listed fixes, then re-run this skill).

Do not auto-apply fixes. Propose them; the writer decides. Never soften a finding to make a claim survive; the corridor's credibility is its honesty.
