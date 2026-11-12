# Licensing

Photon Mountain carries three kinds of material, and they cannot all sit under one license. This file says which license applies where, and why.

The short version: the writing is CC BY 4.0, the code is MIT, the corridor map **data** is ODbL 1.0 because it derives from OpenStreetMap, and the name and mark are reserved.

## The per-path scheme

| Path | License | Notes |
|---|---|---|
| `01_doctrine/`, `02_substance/`, `00_project_system/`, root `.md` | **CC BY 4.0** | The doctrine, the corridor substance, the project system. Reuse freely with attribution. |
| `03_deliverables/maps/*.geojson`, `*.kml`, `*.json` | **ODbL 1.0** | Derivative Database of OpenStreetMap. Share-alike applies. |
| `03_deliverables/maps/*.html`, `*.jsx` | **CC BY 4.0** for the code; the OSM data they carry stays ODbL | Each file credits OpenStreetMap for its basemap tiles already. |
| `03_deliverables/infographics/*.png`, `*.pdf`, `*.html` | **CC BY 4.0** | Rendered images are ODbL "Produced Works", so they are free to license. |
| `04_tools/*.py`, `03_deliverables/infographics/*.py` | **MIT** | |
| `01_doctrine/brand_assets/fonts/*.ttf` | **SIL Open Font License 1.1** | Not ours. Each family's OFL text sits beside the fonts. |
| `CODE_OF_CONDUCT.md` | **CC BY-SA 4.0** | Adapted from the Contributor Covenant 3.0, whose license is share-alike. Not CC BY like the rest of the prose. |
| The name, wordmark, Summit Sun mark, and palette | **Reserved** | See `TRADEMARKS.md`. No content license grants trademark rights. |

Full texts: `LICENSE` (CC BY 4.0), `LICENSES/MIT.txt`, `LICENSES/ODbL-1.0.txt`, `LICENSES/CC-BY-4.0.txt`.

## Why the map data is different

`03_deliverables/maps/MAP_NOTES.md` records how the corridor boundary was built: road centerlines traced from **OpenStreetMap** via the OSRM public router, and dozens of markers placed at OSM building centroids. OpenStreetMap is published under the Open Database License 1.0, which is share-alike.

The OSM Foundation's Produced Work guideline draws the line by intent: if the published result is intended for extraction of the original data, it is a database; otherwise it is a Produced Work. The `.geojson`, `.kml`, and coordinate `.json` files in this repo **are** intended for extraction. They are queryable coordinate data, which is the whole point of shipping them. So they are a Derivative Database, they stay under ODbL, and they cannot be relicensed CC BY.

The rendered images are the other side of that line. A `.png` or `.pdf` of the map is a Produced Work: nobody extracts the source data from it. Those are licensed CC BY 4.0 with an OpenStreetMap credit.

### What this means if you reuse the map data

- **Credit OpenStreetMap.** "© OpenStreetMap contributors" is the accepted form.
- **Keep the license with it.** ODbL requires the license text or a link to it to travel with a derivative database, placed where a user would look for it: a readme, or the data's own metadata.
- **Share alike.** If you publish a modified version of the database, it goes out under ODbL too.

Each data file in `03_deliverables/maps/` carries this notice in its own metadata, so the obligation survives the file being copied out of the repo on its own.

## Attribution

For the writing and the images:

> Photon Mountain, a Colorado Startups project in collaboration with Colorado AI. CC BY 4.0.

For the map data:

> Corridor boundary and marker coordinates derived from OpenStreetMap. © OpenStreetMap contributors. ODbL 1.0.

## A note on the honesty guardrails

The substance documents carry per-file honesty guardrails: what operates today versus what opens in 2026 versus what is on the horizon, and which figures belong to which source. Those guardrails are part of the work, not decoration. If you reuse the substance, reuse the framing with it. Stripping the guardrails and keeping the claims produces something this project would not stand behind.
