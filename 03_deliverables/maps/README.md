# Corridor map data

The definitive Photon Mountain corridor boundary and marker atlas. Method, sources, and every locked convention are in `MAP_NOTES.md`; **read that before editing any file here.**

## Licensing and attribution (read this before reusing the data)

> Corridor boundary and marker coordinates derived from OpenStreetMap. © OpenStreetMap contributors. This derivative database is made available under the Open Data Commons Open Database License (ODbL) v1.0: https://opendatacommons.org/licenses/odbl/1-0/

The boundary was built by tracing road centerlines from OpenStreetMap through the OSRM public router, and many markers sit at OSM building centroids. That makes the data files here a **Derivative Database** under ODbL, not a Produced Work, because they are intended for extraction of the coordinates. Share-alike applies: a modified version you publish goes out under ODbL as well, with the credit intact.

The full reasoning, and the per-path scheme for the rest of the repo, is in `../../LICENSING.md`. The license text is at `../../LICENSES/ODbL-1.0.txt`.

`photon_mountain_corridor.geojson`, `felt_boundary.geojson`, and `photon_mountain_corridor.kml` each carry this notice in their own metadata, so it survives the file being copied out on its own. `corridor_ring_latlng.json` is a bare coordinate array with nowhere to put metadata, so this README is its notice.

## The files

| File | What it is |
|---|---|
| `photon_mountain_corridor.geojson` | The canonical set: 53 point markers plus the boundary polygon. |
| `photon_mountain_corridor.kml` | The same 53 markers for Google Earth and Maps. |
| `photon_mountain_boundary_map.html` | Self-contained Leaflet map, opens in a browser. |
| `PhotonMountainMap.jsx` | React component carrying the same roster. |
| `felt_boundary.geojson` | Boundary polygon only, for import into Felt. |
| `corridor_ring_latlng.json` | The boundary ring as a bare `[lat, lon]` array. |

## The invariant

All four roster files carry the same **53 markers**, name- and coordinate-identical, across seven two-word categories. `../../04_tools/marker_parity.py` checks this. Three things that look like drift but are not:

- **KML escapes XML entities.** Three names contain `&`, stored as `&amp;`. Unescape before comparing.
- **KML rounds coordinates**, to between three and six decimal places. Compare at five decimals, about 1.1 m, which passes the rounding and still catches a real move.
- **Notes differ by design between formats.** The HTML and JSX notes are `"<Category>. "` plus the GeoJSON note, because GeoJSON keeps `category` as its own property instead. The parity checker enforces that relationship rather than demanding identical strings.

Anything else that differs is real drift, and the roster is wrong somewhere.
