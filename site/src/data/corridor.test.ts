// The live record, checked at build: the invariants the site's numbers rest on.
import { describe, expect, it } from "vitest";
import factsMd from "../../../02_substance/corridor_facts_and_sources.md?raw";
import { anchors, companies, figures, sites } from "./corridor";

const CATEGORIES = ["National Lab", "University Lab", "Fabrication Facility", "Innovation Campus", "University Campus", "Government Hall", "Transit Station"];

describe("the corridor record", () => {
  it("has the 53 map sites in the seven categories", () => {
    expect(sites).toHaveLength(53);
    expect(new Set(sites.map((s) => s.category))).toEqual(new Set(CATEGORIES));
    for (const s of sites) {
      expect(s.lat).toBeGreaterThan(39);
      expect(s.lat).toBeLessThan(41);
    }
  });

  it("gives every company a name, a city, a ring and a source", () => {
    expect(companies.length).toBeGreaterThan(50);
    expect(new Set(companies.map((c) => c.segment)).size).toBe(7);
    for (const c of companies) {
      expect(c.name, "a company name").not.toBe("");
      expect(c.city, `${c.name} city`).not.toBe("");
      expect(c.ring, `${c.name} ring`).not.toBe("Other");
      expect(c.source?.url, `${c.name} source`).toMatch(/^https:\/\//);
    }
  });

  it("gives every anchor institution a source", () => {
    expect(anchors.length).toBeGreaterThanOrEqual(10);
    for (const a of anchors) expect(a.source?.url, a.name).toMatch(/^https:\/\//);
  });

  it("attributes every headline figure and finds it in the doc it cites", () => {
    expect(figures.length).toBeGreaterThan(0);
    for (const f of figures) {
      expect(f.doc, f.id).toBe("02_substance/corridor_facts_and_sources.md");
      expect(factsMd, `${f.id}: "${f.match}"`).toContain(f.match);
      expect(f.source, f.id).toMatch(/^https:\/\//);
      expect(f.read, f.id).toMatch(/^\d{4}-\d{2}-\d{2}$/);
      expect(["today", "2026", "horizon"], f.id).toContain(f.clock);
    }
  });
});
