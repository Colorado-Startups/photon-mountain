# The "Why and How" Guide

*The structure standard for Photon Mountain's technology explainers. Rewritten 2026-09-22 from a Colorado AI original: that version governed a three-pillar candidate framework, carried Colorado AI's motto, and pointed at eight files that do not exist in this project. This version governs the corridor's own substance docs. Voice is governed by `voice.md`, brand by `brand_identity.md` and `brand_guidelines.md`, corridor facts and their guardrails by `../02_substance/corridor_facts_and_sources.md`. The working exemplars are `../02_substance/photonics_why_and_how.md` and `../02_substance/energy_why_and_how.md`.*

---

## What a "Why and How" is for

One subject, one document, many uses. It answers the two questions a reader actually has, in this order: why does this matter, and how does it work. It is the single source a web page, a one-pager, or a briefing all draw from, so the corridor's story stays the same wherever it appears. It is not a research dump and not a pitch.

Keep them siblings: same structure, same density, same voice, so the set reads as one system.

## Who you are writing for

Builders first, per the audience rank in `brand_identity.md`. That means an engineer, founder, or researcher deciding where to do their work, plus the people who fund and site that work. Write so the least-expert reader who will ever open it can follow, usually a curious non-specialist. An expert can skim down; a newcomer cannot skim up. Adapt depth, never accuracy. The guardrails section is the one place you write for the team instead of the reader.

## The five principles

1. **Bottom line first.** Lead with the conclusion, then support it. The reader should know the subject's role in the corridor from the first line, before any mechanism.
2. **Outcomes before mechanics.** A non-specialist cares what the technology does before how it works. Open with the stakes, then explain the machine.
3. **Progressive disclosure.** Reveal complexity in layers: the one-line role, the why, the plain-language how, then the detail. Let the reader build a mental model before you add weight.
4. **Story and analogy over jargon.** Translate every abstract category into a concrete image. Use one good analogy per hard idea.
5. **No hype, ever.** The corridor's story is true and does not need overselling. Concise, scannable, plain, and honest reads as more credible, not less. Every sentence must survive a literal read.

## The structure (nine parts, in order)

Use these section names so every "Why and How" matches. The first line and the last two sections are non-negotiable.

1. **The role, in one line.** A single bold sentence naming the subject's job in the corridor. Then two or three sentences placing it against the corridor's other work.
2. **WHY [subject].** The wall this technology breaks through and why that matters. Lead with the human outcome and the stakes, not the engineering.
3. **HOW it works, in plain language.** The mechanism a non-specialist can follow, built on one clear analogy. Include the honest near-term version of how it actually gets used, because the realistic path is usually more convincing than the dream.
4. **What it unlocks.** Three or four concrete, forward-looking wins, each a visible image, not an abstract category. Keep speculative wins in the future tense.
5. **How fast (the honest timeline).** What is real today, what opens in 2026, and what is still on the horizon, kept distinct. Name the destination with conviction and the clock with honesty.
6. **WHY this corridor.** The verified local assets that make the claim credible: the science base, the companies, the federal and state investment, the labs. Every figure cited or labeled a goal. State the honest version and refuse the overclaim.
7. **The lines (ready to use).** A short hero or section-lead paragraph plus three or four short forms, clean enough to lift straight onto a page. The master tagline is "Build with light."
8. **Internal honesty guardrails.** A numbered list of the specific claims a critic will test, and the honest line to hold on each. This is what keeps the piece trustworthy. Every "Why and How" must have one.
9. **Sources (searched and verified [date]).** A dated list, one line per claim, naming the source. The date is the day the claims were actually searched, not the day the file was edited.

## Voice and evidence rules (inherited, not restated)

These bind every "Why and How". The full doctrine lives where noted; do not re-litigate it here.

- **No em dashes, ever.** Use commas, semicolons, periods, or parentheses. Enforced mechanically by `../04_tools/voice_lint.py`. (`voice.md`)
- **Plain and direct, one idea per sentence.** As meaning, not word count. A short sentence carrying two claims still fails. (`voice.md`)
- **Every figure is attributed or labeled a goal.** Name a credible source, or say plainly that the number is a target. (`voice.md`, `../02_substance/corridor_facts_and_sources.md`)
- **Search before stating** any current status, number, or company fact. The corridor moves in real time, and a stale status is the most common way one of these documents goes wrong.
- **Both gates pass before ship.** Run pm-voice-check and pm-fact-guardrails on the file. For anything external-facing, re-run the fact gate the day it ships.

## The honesty discipline

The guardrails section is the signature of a Photon Mountain "Why and How". Frontier technologies invite overclaiming, and one false-sounding line discredits the whole piece. So every "Why and How" names, in writing, the claims a fact-checker would test and the honest line to hold on each.

The recurring traps, and the standing corridor guardrails they map onto:

- **Three clocks, kept apart.** What operates today, what opens in 2026, and what is on the horizon are three different claims. Blurring them is the corridor's easiest and most damaging mistake. NIST Boulder's cleanroom operates. The Arvada photonic-IC fab opens. Photonic compute is emerging, not shipping at scale.
- **Tense.** Keep anything not yet delivered in the future tense. "Will build" and "can accelerate" are true; "has built", stated as done, may not be.
- **Attribution.** Do not credit a win to this subject that belongs to another. Association figures are the association's figures, not independent ones.
- **Naming.** NLR is "formerly NREL" on first reference. A "photonic quantum chip" usually means a chip for building a quantum computer, not a photonic AI chip; keep the two uses distinct.
- **No monopoly.** Claim the corridor's real, defensible edge, not one it does not have. The honest version is almost always more persuasive than the overclaim.

If a "Why and How" cannot pass its own guardrails, the copy is wrong, not the guardrails.

## Copy-paste skeleton

```
# [Subject]: Why and How

*[One-line standfirst: what this file is, and the date its claims were verified.]*

## The role, in one line
**[One bold sentence: this subject's job in the corridor.]**
[Two or three sentences placing it against the corridor's other work.]

## WHY [subject]
[The wall it breaks through. Stakes first.]

## HOW it works, in plain language
[The mechanism, one analogy, the honest near-term version of how it is used.]

## What it unlocks
- **[Concrete image].** [Forward-looking, honest.]
- **[Concrete image].** [...]
- **[Concrete image].** [...]

## How fast (the honest timeline)
[Operating today. Opening in 2026. On the horizon. Kept distinct.]

## WHY this corridor
- **[Asset].** [Verified, cited.]
- **[Asset].** [...]
[The honest version of the claim, and the overclaim refused.]

## The lines (ready to use)
> **[Hero paragraph.]**
- [Short form]
- [Short form]
- Build with light.

## Internal honesty guardrails
1. **[The trap.]** [The claim a critic will test, and the honest line to hold.]
2. [...]

## Sources (searched and verified [date])
- [Claim]: [figure or status], per [source].
- [...]
```

*Before drafting a new one, read this guide and both exemplars. Before shipping one, run pm-voice-check and pm-fact-guardrails.*
