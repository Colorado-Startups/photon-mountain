# Photon Mountain vs Silicon Valley, true-scale region maps

Corridor positioning asset. Two HTML maps that put Silicon Valley and Photon
Mountain side by side from real coordinates at one shared scale, so their true
sizes are honest. The whole point of the asset is the honest comparison, so the
locked decisions below exist to stop the next session from re-deriving them.

## Files

- `photon_mountain_vs_silicon_valley.html`, Cut 1, the full two-ring map (core and greater) for general use.
- `photon_mountain_vs_silicon_valley_core.html`, Cut 2, core only, the Boulder, Golden, Arvada, and Denver core against Palo Alto to San Jose. The version for candidate rooms, where the core is the comparison that wins.
- `photon_mountain_map_generator.py`, builds both HTML files and a PNG preview of each. Run it to regenerate.
- `photon_mountain_map_verify.py`, independent numeric geometry check. Run it after any edit.
- `photon_mountain_vs_silicon_valley_preview.png` and `..._core_preview.png`, reference renders of each cut (the repo has no browser, so these are how you eyeball the maps without opening the HTML).

## Regenerate and verify

```
python3 photon_mountain_map_generator.py .   # writes both HTML + both previews
python3 photon_mountain_map_verify.py        # exits 0 only if all checks pass
```

## Locked decisions

1. **Name.** "Photon Mountain" is locked. A photon is the quantum particle of light, so one word holds both the photonic chips Colorado can manufacture and the quantum science Colorado can run. It names a real thing the way silicon did. Carry the rationale in any caption.
2. **Scale.** `K = 8` pixels per mile, identical on both maps. This is what makes the cross-map size comparison honest. Never rescale one panel to fit.
3. **Projection.** Equirectangular per map. `refLat` = mean latitude of that map's cities. `x = (lon - lonMin) * 69 * cos(refLat) * K + PAD`, `y = (latMax - lat) * 69 * K + PAD`, `PAD = 72`.
4. **Nested regions, buffered convex hulls.** The maps now use two rings, a core and a greater ring. The method supports a third, an outer ring, used in earlier versions. Each region is the **buffered convex hull** of its tier's cities. The buffer is built as the convex hull of a ring of points placed around every city (a Minkowski sum of the hull with a disk, `BUFFER_PX = 8`, which is 1 mile). Hulls of nested city sets nest automatically, and the same buffer on each keeps the nesting, so the rings never cross or balloon. This is why hulls are used and ellipses were dropped. Note on the buffer size: it started at 18 px, but that 2.25-mile cushion reached towns just outside a tier and made them read one ring too high (Superior and Westminster, about 1.6 and 2.2 miles outside the core, looked core). At 8 px the blobs hug their true cities, so a dot's shading matches its tier.
5. **Sequential blue, one hue.** All three bands are the SAME translucent blue stacked, so the overlap darkens toward the core. One hue is colorblind-safe and on-theme, since a photon is light. **No capital.** Every city is a proportional symbol: dot area scales with 2020 Census population (radius with the square root of population), so each city reads at its true weight and no single city is crowned. The most populous city, San Jose, sets the max dot radius (`DOT_R_MAX = 15` px) and a `DOT_R_MIN = 4` px floor keeps the smallest towns legible. A size key on each cut gives reference dots at 100k, 500k, and 1M. The gold capital star is retired.
6. **Labels.** JetBrains Mono, pushed radially outward from each map's centroid, with a paper-colored halo. Shared 10-mile scale bar (80 px).
7. **City data and tiers.** See the `CITIES` table in the generator (each city now carries a `pop` field, 2020 Census). Both maps have two rings, a core and a greater ring, no outer (the title, subhead, and legend all say "two rings"). Silicon Valley core is Palo Alto, Mountain View, Sunnyvale, Cupertino, Santa Clara, San Jose, and Menlo Park; greater is San Mateo, Redwood City, Fremont. That is 10 dots. Menlo Park is in the core because it anchors the Sand Hill Road venture corridor (and carries Meta and SLAC photon science); adding it stretches the Valley core to about 18 miles, Menlo Park to San Jose. Photon Mountain core is Boulder, Golden, Arvada, and Denver; greater is Louisville, Lafayette, Broomfield, Westminster, Longmont. That is 9 dots, four core and five greater. There is no capital on either map. Denver is in the core as the metro anchor, the San Jose of the set: with population-scaled dots the core needed a heavyweight to sit opposite San Jose, and Denver is it. Denver anchors by metro gravity, not as the photonics research crown, which is still Boulder (NIST, JILA, CU). Adding Denver widens the Photon Mountain core to about 24 miles, Boulder to Denver, so it now runs wider than the Valley's 18; the population anchor is the point, not size parity. Englewood (Lightwave Logic photonic chips) is left out to keep the dot set readable. Intentionally excluded: San Francisco and Oakland on the California side, and Englewood, Lakewood, Superior, Centennial, Loveland, Fort Collins, Castle Rock, and Colorado Springs on the Colorado side.

## The honest framing (the point of the asset)

The two cores each have a major-city anchor, which is the comparison the asset now
leads with: San Jose for Silicon Valley, Denver for Photon Mountain. Measured core
diameters (max pairwise distance, printed by the verify script): Silicon Valley
about 18 miles (Menlo Park to San Jose, 18.0 measured), Photon Mountain about 24
miles (Boulder to Denver, 24.1 measured). With Denver in the core the Photon
Mountain core now runs wider than the Valley's; that is a deliberate choice to give
the core a population anchor, not a size brag. Beyond the core the shapes differ:
Silicon Valley stays a compact peninsula knot, while Photon Mountain fans up the
Front Range from Boulder down to Denver.

The population dots carry the real point. Each core is now anchored by a heavyweight
city, San Jose (about 1.0M) and Denver (about 716k), so neither core reads as a
cluster of small towns. Silicon Valley's core is still more populous in total (about
1.5M across its cities versus about 0.97M for Photon Mountain's), so the captions do
not claim Colorado has caught up on people; they say Colorado already has the core
and the city to anchor it. Honesty guardrail: Denver anchors by metro gravity, not
as the photonics research center, which is Boulder. Do not imply the full sprawl
rivals the Valley, and do not present Denver as the corridor's research crown.

Core-definition note: Denver's placement has flipped over the project's life. It was
in the core (Boulder-Golden-Denver-Arvada, about 24 miles), then moved to the greater
ring to make the cores size-peers (Boulder-Golden-Arvada, about 18 miles), and is now
back in the core as the deliberate metro anchor, the San Jose of the set, accepting
that this widens the Photon Mountain core to about 24 miles again. The trade is
explicit: a population anchor in the core is worth more to this asset than exact size
parity with the Valley. Capitals are retired on both maps; no single city is crowned
by a star.

## Voice

Photon Mountain voice for any prose, per `01_doctrine/voice.md`: plain and
direct, one idea per sentence, no em dashes ever, every figure attributed or
labeled a goal. The master tagline is "Build with light."

## Revisions

- 2026-06-20, first build: two cuts, hull method, verified.
- 2026-06-20, revision: Photon Mountain core made a three-city triangle (Golden joins Boulder and Denver), Louisville added to the greater ring, Centennial removed. Silicon Valley labels rebuilt with a force-directed layout (labels never overlap each other or the dots, with hairline leader lines when a label has to move). Both cuts re-verified.
- 2026-06-20, revision: Photon Mountain membership reset. Core now Boulder, Golden, Denver, Arvada. Greater now Louisville, Broomfield, Lakewood. Outer now Longmont. Fort Collins, Loveland, and Englewood dropped. Both cuts re-verified.
- 2026-06-20, revision: Broomfield promoted to core (Quantinuum's largest site), Westminster added to the greater ring (Maxar Intelligence), Longmont kept in outer. Photon Mountain core is now five cities. Both cuts re-verified.
- 2026-06-20, revision: Broomfield reverted to the greater ring (per Paul). Westminster stays greater, Longmont stays outer. Core is back to four cities (Boulder, Golden, Denver, Arvada). Both cuts re-verified.
- 2026-06-20, revision: Superior and Lafayette added to the greater ring, bringing Photon Mountain to 11 dots to match Silicon Valley. Both cuts re-verified.
- 2026-06-20, revision: blob buffer tightened from 18 px to 8 px (1 mile) so the core blob hugs its true cities. Fixes Superior and Westminster reading as core when they are about 1.6 and 2.2 miles outside it. Tiers unchanged, scale unchanged. Both cuts re-verified.
- 2026-06-20, revision: Oakland removed from Silicon Valley and Superior removed from Photon Mountain, both on the merits (Oakland is East Bay rather than the peninsula and South Bay heartland; Superior had no anchor institution of its own). Each map now carries 10 dots, with San Francisco and Longmont as the matching lone outer dots. Both cuts re-verified.
- 2026-06-20, revision: Menlo Park added to the Silicon Valley core (Meta, Sand Hill Road, SLAC photon science) and Englewood added to the Photon Mountain greater ring (Lightwave Logic photonic chips). Each map back to 11 dots. The Silicon Valley core diameter grew to 18.0 miles (Menlo Park to San Jose), so both captions now read "about 18." Both cuts re-verified.
- 2026-06-20, revision: Menlo Park moved from core to greater (per Paul). Silicon Valley core diameter returns to 15.8 miles (Palo Alto to San Jose) and captions go back to "about 16." Fremont and Englewood confirmed as greater on a distance-from-capital basis (about 15.5 and 6 miles from their capitals, versus 30-plus for the outer dots). Both cuts re-verified.
- 2026-06-21, revision: Denver moved from core to the greater ring and the Photon Mountain core is now the tight Boulder-Golden-Arvada triangle, about 18 miles (Boulder to Golden) versus the Valley's 16, so the two cores are peers (the old Boulder-to-Denver core was 24 miles). The capital star moved from Denver to Boulder, chosen on research strength (NIST, JILA, CU). Both captions reworked to the new "about 18" framing. Both cuts re-verified.
- 2026-06-21, revision: Longmont moved from outer to greater (with Boulder as capital, Longmont is only about 14 miles out, greater-range). Photon Mountain now has no outer dot and renders as two bands; Silicon Valley keeps San Francisco as its lone outer. Each map still carries 11 dots. Both cuts re-verified.
- 2026-06-21, revision: dropped to a two-ring model on both maps (core and greater, no outer). Removed San Francisco from Silicon Valley (now 10 dots) and Lakewood and Englewood from Photon Mountain (now 9 dots). Title, subhead, and legend updated to "two rings"; the legend now shows Core and Greater only (and a one-swatch Core legend on the core-only cut). Also fixed a latent legend bug where the swatch shades were inverted relative to the map. Both cuts re-verified.
- 2026-06-21, revision: the full-cut caption was reworked around the real thesis, density of people: Silicon Valley's footprint wraps the south end of San Francisco Bay (open water, no people) while Photon Mountain is solid Front Range, so Photon Mountain reading a touch bigger is honest. Englewood was briefly re-added and then removed again at Paul's direction, deliberately kept out so Photon Mountain does not read too large; it stays 9 dots, Silicon Valley 10. Both cuts re-verified.
- 2026-06-21, revision (per Paul): capitals retired on both maps (no gold star, no singled-out city) and every dot is now a proportional symbol scaled to 2020 Census population, so each city reads at its true weight. Menlo Park moved from the Silicon Valley greater ring into the core (it anchors Sand Hill Road), which grows the Valley core to about 18 miles (Menlo Park to San Jose), the same size as Photon Mountain's core (Boulder to Golden, 18.1). Silicon Valley is 10 dots (7 core, 3 greater), Photon Mountain 9 dots (3 core, 6 greater). Added a population size key (100k / 500k / 1M) to both cuts; captions reworked to name the population gap honestly ("fill Colorado's core with that density"). The generator now writes the canonical `_preview.png` filenames directly. Both cuts re-verified, cores measured at 18.0 (SV) and 18.1 (PM) miles.
- 2026-06-21, revision (per Paul): Denver moved from the greater ring back into the Photon Mountain core, to give the core a major-city anchor opposite Silicon Valley's San Jose (the population-scaled dots had left the Colorado core without a heavyweight). Photon Mountain core is now Boulder, Golden, Arvada, Denver (4); greater is Louisville, Lafayette, Broomfield, Westminster, Longmont (5); still 9 dots. This widens the Photon Mountain core to about 24 miles (Boulder to Denver) versus the Valley's 18, reversing the earlier "cores are the same size" framing; the captions and honest-framing section now lead with the anchor-city parallel and flag that Denver anchors by metro gravity, not as the photonics research crown (still Boulder). Both cuts re-verified, cores 18.0 (SV) and 24.1 (PM) miles.
