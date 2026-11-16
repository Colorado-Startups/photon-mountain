// The corridor map's conventions (03_deliverables/maps/MAP_NOTES.md, revisions 7k, 7s and 7x, on-light variants
// per revision 8) and the projection for the map's still poster. Pure functions; mapdata.test.ts holds them.
import type { Site } from "../data/parse";

export interface Category { id: string; key: string; ring: number; big?: boolean; fill: string; stroke: string }

/** The seven locked categories. fill and stroke name tokens in tokens.json `color`. */
export const CATS: Category[] = [
  { id: "National Lab", key: "natlab", ring: 1.5, fill: "alpenglow_deep", stroke: "white" },
  { id: "University Lab", key: "univlab", ring: 1.5, fill: "laser_violet", stroke: "white" },
  { id: "Fabrication Facility", key: "fab", ring: 3, big: true, fill: "dawn_tint", stroke: "alpenglow_deep" },
  { id: "Innovation Campus", key: "innov", ring: 1.5, fill: "violet_bright", stroke: "white" },
  { id: "University Campus", key: "campus", ring: 2, fill: "violet_deep", stroke: "violet_bright" },
  { id: "Government Hall", key: "gov", ring: 2, fill: "snowfield", stroke: "summit_night" },
  { id: "Transit Station", key: "transit", ring: 2, fill: "granite", stroke: "snowfield" },
];

/** The building tier: dots on lab campuses that show at zoom 14 and closer (revision 7s). */
export const BUILDING_TIER = [
  "NIST Precision Measurement Laboratory (BMF)",
  "NIST Building 1 (Radio Building)",
  "NIST Communications Technology Laboratory (Building 3)",
  "NLR Energy Systems Integration Facility (ESIF)",
  "NLR Solar Energy Research Facility (SERF)",
  "NLR Research and Innovation Laboratory (RAIL)",
  "NLR Science and Technology Facility (S&TF)",
  "NLR Solar Radiation Research Laboratory (SRRL)",
  "NLR High-Flux Solar Furnace",
  "NLR Solar Industrial Mesa Test Area (SIMTA)",
  "NLR Outdoor Test Facility (OTF)",
  "NLR Thermal Test Facility (TTF)",
  "NLR EMAPS (under construction)",
  "NLR Flatirons Control Center",
];
export const TIER_ZOOM = 14;

export const catOf = (id: string) => CATS.find((c) => c.id === id);

/** Sites in the legend's order, then by name. */
export function ordered(sites: Site[]): Site[] {
  const rank = Object.fromEntries(CATS.map((c, i) => [c.id, i]));
  return [...sites].sort((a, b) => rank[a.category] - rank[b.category] || a.name.localeCompare(b.name));
}

type Ring = number[][];

/** An equirectangular projection fitted to a ring, x scaled by the cosine of the middle latitude. */
export function projector(ring: Ring, width = 1000, pad = 24) {
  const lons = ring.map((p) => p[0]);
  const lats = ring.map((p) => p[1]);
  const [w, e, s, n] = [Math.min(...lons), Math.max(...lons), Math.min(...lats), Math.max(...lats)];
  const k = Math.cos((((s + n) / 2) * Math.PI) / 180);
  const scale = (width - 2 * pad) / ((e - w) * k);
  const height = Math.round((n - s) * scale + 2 * pad);
  const xy = (lon: number, lat: number): [number, number] => [
    Math.round((pad + (lon - w) * k * scale) * 10) / 10,
    Math.round((pad + (n - lat) * scale) * 10) / 10,
  ];
  return { width, height, xy };
}

/** The ring as an SVG path, every step-th vertex, so the poster stays small. */
export function ringPath(ring: Ring, xy: (lon: number, lat: number) => [number, number], step = 6): string {
  const pts = ring.filter((_, i) => i % step === 0).map((p) => xy(p[0], p[1]));
  return "M" + pts.map((p) => p.join(",")).join("L") + "Z";
}
