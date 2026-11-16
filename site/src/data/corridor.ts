// The corridor record, read from the repo's own files at build time. The repo stays the one source:
// 02_substance/ for the roster, the anchors and the figures, 03_deliverables/maps/ for the 53 sites.
import rosterMd from "../../../02_substance/colorado_photonics_companies.md?raw";
import geoRaw from "../../../03_deliverables/maps/photon_mountain_corridor.geojson?raw";
import figuresFile from "../../../02_substance/figures.json";
import clocksFile from "../../../02_substance/clocks.json";
import { parseAnchors, parseCompanies, parseSites } from "./parse";

export interface Figure {
  id: string; value: string; label: string; whose: string; source: string; read: string;
  clock: "today" | "2026" | "horizon"; doc: string; match: string;
}

export const geojson = JSON.parse(geoRaw);
export const sites = parseSites(geojson);
export const companies = parseCompanies(rosterMd);
/** The companies inside the corridor (Core and Ring). Statewide and "roots only" rows stay listed but never count here. */
export const corridorCompanies = companies.filter((c) => c.ring === "Core" || c.ring === "Ring");
export const anchors = parseAnchors(rosterMd);
export const figures = figuresFile.figures as Figure[];

export interface ClockItem {
  id: string; clock: "today" | "2026" | "horizon"; when: string; title: string; text: string; place: string; doc: string; match: string;
}
/** The three clocks: operating today, opening or targeted in 2026, and on the horizon. */
export const clocks = clocksFile.items as ClockItem[];

export const repo = "https://github.com/Colorado-Startups/photon-mountain";
export const meta = {
  publisher: "Photon Mountain, a Colorado Startups project",
  repository: repo,
  roster_source: `${repo}/blob/main/02_substance/colorado_photonics_companies.md`,
  sites_source: `${repo}/blob/main/03_deliverables/maps/photon_mountain_corridor.geojson`,
};
