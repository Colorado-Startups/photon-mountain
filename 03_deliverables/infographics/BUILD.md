# Building the infographics

Replaces `RESKIN_NEEDED.md`, which was retired 2026-09-22 when the re-skin landed. Everything here renders in the locked Photon Mountain identity; nothing in this folder carries Colorado AI's palette, fonts, motto, or pillar framing any more.

## What builds what

| Script | Writes | Needs |
|---|---|---|
| `photon_mountain_build.py` | `photon_mountain.pdf` | reportlab |
| `photon_mountain_map_generator.py` | both `..._vs_silicon_valley*.html` and their `_preview.png` | matplotlib |
| `photon_mountain_map_verify.py` | nothing; exits 0 only if the geometry is sound | matplotlib, via the generator it imports |

`photon_mountain.html` is hand-authored, not generated. Edit it directly. It mirrors the PDF's content and reads its palette from CSS variables at the top of the file.

## Setup

Both scripts are stdlib plus one third-party library each, pinned in `requirements.txt` at the repo root.

```bash
python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt
```

Brand colors and fonts come from `04_tools/brand_tokens.py`. Neither script hardcodes a hex value or a font name. Confirm the tokens still agree with the identity doc before a build:

```bash
python3 04_tools/brand_tokens.py --self-test
```

The seven brand TTFs live in `01_doctrine/brand_assets/fonts/`, with their provenance and the commands that cut them in the README there. If a font file is missing, `photon_mountain_build.py` prints `brand_fonts= False` and silently falls back to core PDF fonts, so check that line on every run.

## Regenerate

```bash
cd 03_deliverables/infographics
../../.venv/bin/python photon_mountain_build.py
../../.venv/bin/python photon_mountain_map_generator.py .
../../.venv/bin/python photon_mountain_map_verify.py
```

Then rasterize the PDF, since the repo has no browser:

```bash
pdftoppm -png -r 200 -singlefile photon_mountain.pdf photon_mountain
```

## What to check on every build

- **`brand_fonts= True`** in the build script's output. False means it rendered in fallback fonts.
- **`OVERFLOW none`**. The page is US Letter and the layout is tight; a text change can push content past the bottom margin. A wider font pushes harder, which is how the re-skin first overflowed by 7pt.
- **`RESULT: PASS`** from the verifier, with core diameters 18.0 miles (Silicon Valley) and 24.1 miles (Photon Mountain). Those numbers are the locked ones in `photon_mountain_map_README.md`; if they move, the geometry changed and the README has to change with it.
- **Contrast.** `brand_tokens.check_pairing` raises on a pairing below WCAG AA. The trap to watch is violet: the on-light and on-dark variants look similar and are not interchangeable. Setting the on-light violet over the dark corridor panel scores 2.37, well under the 4.5 floor, and it looks plausible until measured.

## What the verifier does and does not cover

`photon_mountain_map_verify.py` checks the **comparison maps** in this folder. It confirms city tier membership, that every city sits inside its own blob and every enclosing blob, that the blobs nest, and the real core diameters. It is a pure geometry check, indifferent to styling, which makes it a good re-skin regression test.

It does **not** touch the corridor atlas in `../maps/`. That one is guarded by `04_tools/marker_parity.py`.
