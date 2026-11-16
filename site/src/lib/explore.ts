// The explorer's records and filters: companies and anchor institutions as one list, filtered by kind, ring,
// segment, town and free text. Pure, so the same rules run at build (counts) and in the browser (filtering).
import type { Anchor, Company } from "../data/parse";
import { TOWNS, inTown } from "./home";
import { segmentOf } from "./light";

export interface Entry {
  id: string; kind: "company" | "anchor"; name: string; city: string; ring: string; segment: string;
  what: string; tie: string; source: { label: string; url: string } | null; towns: string[];
}

export interface Filters { q: string; kind: string[]; ring: string[]; segment: string[]; town: string[] }

export const slug = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");

const townsOf = (place: string) => TOWNS.filter((t) => inTown(place, t.name)).map((t) => t.id);

export function toEntries(companies: Company[], anchors: Anchor[]): Entry[] {
  const c = companies.map((x, i) => ({
    id: `c${i}`, kind: "company" as const, name: x.name, city: x.city, ring: x.ring,
    segment: slug(segmentOf(x.segment)?.short ?? x.segment), what: x.builds, tie: x.tie, source: x.source, towns: townsOf(x.city),
  }));
  const a = anchors.map((x, i) => ({
    id: `a${i}`, kind: "anchor" as const, name: x.name, city: x.city, ring: townsOf(x.city).length ? "Core" : "Statewide",
    segment: "", what: x.relevance, tie: "Research institution", source: x.source, towns: townsOf(x.city),
  }));
  return [...a, ...c];
}

/** True when an entry passes every filter group; an empty group passes everything. */
export function matches(e: Entry, f: Filters): boolean {
  const any = (want: string[], have: string | string[]) => want.length === 0 || (Array.isArray(have) ? have.some((h) => want.includes(h)) : want.includes(have));
  const q = f.q.trim().toLowerCase();
  return (
    any(f.kind, e.kind) && any(f.ring, slug(e.ring)) && any(f.segment, e.segment) && any(f.town, e.towns) &&
    (!q || `${e.name} ${e.city} ${e.what}`.toLowerCase().includes(q))
  );
}

/** Filters from a URL query: ?town=boulder&segment=lasers&q=laser (comma lists allowed). */
export function fromQuery(search: string): Filters {
  const p = new URLSearchParams(search);
  const list = (k: string) => (p.get(k) ?? "").split(",").map((x) => x.trim()).filter(Boolean);
  return { q: p.get("q") ?? "", kind: list("kind"), ring: list("ring"), segment: list("segment"), town: list("town") };
}

/** Counts per value of one key, for the chips. */
export function tally(entries: Entry[], key: "kind" | "ring" | "segment" | "towns"): Record<string, number> {
  const out: Record<string, number> = {};
  for (const e of entries) {
    const vals = key === "towns" ? e.towns : [key === "ring" ? slug(e.ring) : e[key]];
    for (const v of vals) if (v) out[v] = (out[v] ?? 0) + 1;
  }
  return out;
}
