import { describe, expect, it } from "vitest";
import { anchors, companies } from "../data/corridor";
import { fromQuery, matches, matchesCard, slug, tally, toEntries } from "./explore";

const all = toEntries(companies, anchors);
const none = { q: "", kind: [], ring: [], segment: [], town: [] };

describe("the explorer", () => {
  it("holds every company and anchor once, each with a source", () => {
    expect(all).toHaveLength(companies.length + anchors.length);
    expect(new Set(all.map((e) => e.id)).size).toBe(all.length);
    for (const e of all) expect(e.source?.url, e.name).toMatch(/^https?:\/\//);
  });

  it("passes everything with no filters, and each chip's count is what its filter shows", () => {
    expect(all.filter((e) => matches(e, none))).toHaveLength(all.length);
    const towns = tally(all, "towns");
    for (const [town, n] of Object.entries(towns)) expect(all.filter((e) => matches(e, { ...none, town: [town] }))).toHaveLength(n);
    const segs = tally(all.filter((e) => e.kind === "company"), "segment");
    expect(Object.values(segs).reduce((a, b) => a + b, 0)).toBe(companies.length);
  });

  it("reads filters from the links the home page makes", () => {
    const f = fromQuery("?town=boulder&segment=lasers,solar&q=Laser");
    expect(f).toEqual({ q: "Laser", kind: [], ring: [], segment: ["lasers", "solar"], town: ["boulder"] });
    const hits = all.filter((e) => matches(e, f));
    expect(hits.length).toBeGreaterThan(0);
    for (const h of hits) expect(h.towns).toContain("boulder");
  });

  it("tests a rendered card's data attributes exactly as it tests the entry", () => {
    const filters = [fromQuery("?town=boulder"), fromQuery("?segment=lasers&q=laser"), fromQuery("?kind=anchor&ring=core"), fromQuery("")];
    for (const e of toEntries(companies, anchors)) {
      const card = { kind: e.kind, ring: slug(e.ring), segment: e.segment, towns: e.towns.join(" "), text: `${e.name} ${e.city} ${e.what}`.toLowerCase() };
      for (const f of filters) expect(matchesCard(card, f), `${e.name} ${JSON.stringify(f)}`).toBe(matches(e, f));
    }
    expect(matchesCard({}, fromQuery(""))).toBe(true);
  });

  it("makes stable slugs", () => {
    expect(slug("Chips and interconnects")).toBe("chips-and-interconnects");
    expect(slug("Roots only")).toBe("roots-only");
  });
});
