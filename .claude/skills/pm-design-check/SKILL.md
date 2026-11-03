---
name: pm-design-check
description: Run the Photon Mountain design check on a rendered deliverable. Confirms the ground, the on-light and on-dark accent variants, the one-Alpenglow rule, the mark construction, the type stack, and the Colorado AI carryover ban. Use when the user says "design check this", "run pm-design-check on X", "is this on brand", or before any deliverable ships.
---

# pm-design-check

The visual counterpart to `pm-voice-check`. That skill gates prose; this one gates
what a deliverable looks like. Rules source: `01_doctrine/brand_guidelines.md` and the
palette and type tables in `01_doctrine/brand_identity.md`. If this skill and those
files disagree, those files win.

This skill owns the part of the design gate that is Photon Mountain's own. It does not
recompute contrast ratios, and it does not re-derive the tokens. Those have owners
already, named under Handoffs below.

## When to use

- An infographic, page, deck, PDF, or map is about to ship or close.
- The Task Review step of `00_project_system/task_protocol.md` is being run on a
  deliverable that has a visual surface.
- A build script that emits a visual has changed.

Do not use for: prose files with no visual surface, data files, or the corridor atlas
geometry, which `04_tools/marker_parity.py` owns.

## Inputs

1. The target file path, or the build script that produces it. Ask if not given.
2. Nothing else. The rules come from the doctrine, not from the user.

## Pass 1: the ground

A deliverable picks one field and paints it explicitly.

- **Field.** Summit Night, or White or Snowfield. Nothing in between, and no
  transparent background that borrows whatever sits behind it.
- **The variants follow the field.** On-light and on-dark accents are different hex
  values and are not interchangeable. Violet is the trap: the on-light and on-dark
  variants look similar and measure far apart. `03_deliverables/infographics/BUILD.md`
  records the on-light violet scoring 2.37 over the dark corridor panel, well under
  the floor, and looking plausible until measured.
- **Every color traces.** Each hex in the file is a palette token, or a neutral mixed
  from palette colors the way `04_tools/brand_tokens.py` mixes them. An undocumented
  hex is a finding.

Check the field first, because every later finding depends on which one is in use.

## Pass 2: the accent rules

- **Never set body text in an accent color.** This holds at every size on every field.
- **Alpenglow and Laser Violet carry graphics and large text only.** On Snowfield,
  Alpenglow measures 2.90, so it carries no text there at any size. Accent text on a
  light field is Alpenglow Deep or Violet Deep.
- **Never place Alpenglow text on Dawn Tint.**
- **One Alpenglow moment per piece.** Alpenglow is the loud thing; everything else
  stays quiet. Two loud moments is a finding, and so is none.

## Pass 3: the mark and the type

- **Summit Sun.** The peak is always in front of the disc, and the disc's top rim stays
  visible above the apex. No rays, no gradients, no prism, no tilt, and no recolor
  outside the palette. Clear space is half the disc's diameter. Minimum size is 16 px.
- **The right lockup for the field.** Alpenglow disc with Snowfield peak on dark
  surfaces. Alpenglow disc with Summit Night peak on light surfaces.
- **Type stack.** Space Grotesk for display, Inter for body and UI, Space Mono for data
  and figures. No look-alike substitutes.
- **Captions in Granite. Data in Space Mono.**
- **The name.** Photon Mountain, two words, both capitalized, never hyphenated and
  never abbreviated.
- **The tagline.** Never both the master line and the supporting line in the same small
  space.

## Pass 4: the carryover ban

Colorado AI's identity is prohibited here. The rule stands; it is not a one-time
cleanup. Any of the following in a deliverable is a defect to fix:

- Turquoise, pine green, or flag gold.
- IBM Plex, Work Sans, or JetBrains Mono.
- The Colorado AI motto, the inverted-flag mark, or the three-pillar framing.

## Pass 5: honesty on the visual surface

The voice doctrine does not stop at prose. It governs what a picture asserts.

- **A figure set large still needs its hedge.** A source that says "on the order of 250"
  is not a deliverable that says "250" in display type. Setting a number big asserts a
  precision, and the attribution line underneath does not undo it.
- **Every piece that states a figure carries an attribution line.**
- **A rendering is labeled as one.** Do not picture a planned building as a built thing.
- **The three clocks survive compression.** What operates today, what opens in 2026, and
  what is on the horizon stay distinct in a caption as much as in a paragraph. Captions
  are where this gets lost, because captions are where words get cut.

## Handoffs

- **Token drift**: `brand_tokens.py --self-test`, in the cloud, since nothing tests on the
  MacBook Air: `gh workflow run cloud-test.yml -f ref=<branch> -f script=selftest:brand-tokens`.
  Run it first; if the tokens no longer match the identity doc, every later finding is
  unreliable.
- **Contrast math and WCAG**: the `design:accessibility-review` skill, when the session
  has it. When it does not, compute the ratios directly and say that you did.
- **Prose**: `pm-voice-check`.
- **Corridor facts and current status**: `pm-fact-guardrails`.

## Report

One consolidated report:

- Findings by pass, each with the location, the rule it breaks, and a proposed fix.
- Every hex that does not trace to a token, listed.
- Verdict: **Clean** (ship) or **Fix first** (apply the listed fixes, then re-run this
  skill).

Do not auto-apply fixes. Propose them; the designer decides.
