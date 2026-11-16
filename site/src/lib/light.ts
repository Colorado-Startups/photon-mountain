// The light diagram's grouping: what the corridor builds with light, as information or as energy.
// Every roster segment must map to exactly one branch; light.test.ts fails on a new, unmapped segment.
import type { Company } from "../data/parse";

export type Branch = "information" | "energy";

export interface Segment { prefix: string; short: string; branch: Branch }

export const SEGMENTS: Segment[] = [
  { prefix: "Photonic chips", short: "Chips and interconnects", branch: "information" },
  { prefix: "Lasers", short: "Lasers", branch: "information" },
  { prefix: "Photonic and optical sensors", short: "Sensors and imaging", branch: "information" },
  { prefix: "Photonic quantum", short: "Photonic quantum", branch: "information" },
  { prefix: "Optics and photonics components", short: "Optics supply chain", branch: "information" },
  { prefix: "Solar", short: "Solar", branch: "energy" },
  { prefix: "Laser fusion", short: "Laser fusion", branch: "energy" },
];

/** The segment a roster heading belongs to, or undefined when no prefix matches. */
export function segmentOf(heading: string): Segment | undefined {
  return SEGMENTS.find((s) => heading.startsWith(s.prefix));
}

/** Each segment with its companies, in the diagram's order. */
export function branches(companies: Company[]) {
  return SEGMENTS.map((s) => ({ ...s, companies: companies.filter((c) => c.segment.startsWith(s.prefix)) }));
}
