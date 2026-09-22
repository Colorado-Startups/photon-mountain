# Brand fonts

The three typefaces locked in `../../brand_identity.md`: Space Grotesk (display), Inter (body), Space Mono (mono). All three are SIL Open Font License 1.1, so they are free to use, embed, and redistribute. Each family's `OFL-*.txt` license sits beside the font files, as the OFL requires.

## What is here

These are exactly the weights the Typography table in `brand_identity.md` names, no more and no fewer.

| File | Family | Weight | Role |
|---|---|---|---|
| `SpaceGrotesk-Medium.ttf` | Space Grotesk | 500 | Display, headlines, wordmark |
| `SpaceGrotesk-Bold.ttf` | Space Grotesk | 700 | Display, headlines |
| `Inter-Regular.ttf` | Inter | 400 | Body and UI |
| `Inter-Medium.ttf` | Inter | 500 | Body and UI |
| `Inter-SemiBold.ttf` | Inter | 600 | Body and UI emphasis |
| `SpaceMono-Regular.ttf` | Space Mono | 400 | Data, figures, code |
| `SpaceMono-Bold.ttf` | Space Mono | 700 | Data, figures, code |

## Where they came from

All files come from Google's official font repository, `https://github.com/google/fonts`, fetched 2026-09-21 from `main`.

Space Mono ships there as static TTFs and was taken as-is. Space Grotesk and Inter ship only as variable fonts, so the static weights above were cut from those sources with `fonttools`. Space Grotesk's variable default is Light. That is why the instanced files needed their name records rewritten. Without that step both weights reported themselves as "Space Grotesk Light", and a renderer picking by family name could not tell them apart.

## How to reproduce

```bash
B="https://raw.githubusercontent.com/google/fonts/main/ofl"
curl -sSLo "SpaceGrotesk[wght].ttf" "$B/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf"
curl -sSLo "Inter[opsz,wght].ttf"   "$B/inter/Inter%5Bopsz,wght%5D.ttf"
curl -sSLo SpaceMono-Regular.ttf    "$B/spacemono/SpaceMono-Regular.ttf"
curl -sSLo SpaceMono-Bold.ttf       "$B/spacemono/SpaceMono-Bold.ttf"

python3 -m fontTools.varLib.instancer "SpaceGrotesk[wght].ttf" wght=500 -o SpaceGrotesk-Medium.ttf
python3 -m fontTools.varLib.instancer "SpaceGrotesk[wght].ttf" wght=700 -o SpaceGrotesk-Bold.ttf
python3 -m fontTools.varLib.instancer "Inter[opsz,wght].ttf" wght=400 opsz=14 -o Inter-Regular.ttf
python3 -m fontTools.varLib.instancer "Inter[opsz,wght].ttf" wght=500 opsz=14 -o Inter-Medium.ttf
python3 -m fontTools.varLib.instancer "Inter[opsz,wght].ttf" wght=600 opsz=14 -o Inter-SemiBold.ttf
```

Inter is instanced at `opsz=14`, the optical size for running text, because the build scripts set body copy, not display sizes.

Then rewrite name IDs 1, 2, 4, and 6 on the five instanced files so each reports its true family and subfamily. The variable sources are not kept here; the commands above restore them.

## Verification

After any refresh, confirm the seven files still report the right family, subfamily, and weight class, and that Bold really is heavier than Regular. Measuring glyph ink area is the reliable check, because Space Grotesk keeps the same advance widths across weights by design, so a width comparison proves nothing. At the versions fetched on 2026-09-21, Bold carried about 1.5 times the ink area of Regular in both Space Grotesk and Inter.
