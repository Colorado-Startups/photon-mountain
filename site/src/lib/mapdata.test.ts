import { describe, expect, it } from "vitest";
import tokens from "../styles/tokens/tokens.json";
import { geojson, sites } from "../data/corridor";
import { BUILDING_TIER, CATS, catOf, ordered, projector, ringPath } from "./mapdata";

const ring = geojson.features.find((f: { geometry: { type: string } }) => f.geometry.type === "Polygon").geometry.coordinates[0];

describe("the map's conventions", () => {
  it("knows every site's category, and every color is a token", () => {
    for (const s of sites) expect(catOf(s.category), s.name).toBeDefined();
    for (const c of CATS) {
      expect(tokens.color, c.fill).toHaveProperty(c.fill);
      expect(tokens.color, c.stroke).toHaveProperty(c.stroke);
    }
  });

  it("names only real sites in the building tier", () => {
    const names = new Set(sites.map((s) => s.name));
    for (const n of BUILDING_TIER) expect(names.has(n), n).toBe(true);
  });

  it("orders sites by legend, then name", () => {
    const o = ordered(sites);
    expect(o).toHaveLength(53);
    expect(o[0].category).toBe(CATS[0].id);
  });
});

describe("the poster projection", () => {
  it("keeps every site and the ring inside the frame", () => {
    const { width, height, xy } = projector(ring);
    for (const s of sites.filter((x) => x.lat > 39.6)) {
      const [x, y] = xy(s.lon, s.lat);
      expect(x).toBeGreaterThanOrEqual(0);
      expect(x).toBeLessThanOrEqual(width);
      expect(y).toBeGreaterThanOrEqual(0);
      expect(y).toBeLessThanOrEqual(height);
    }
    const d = ringPath(ring, xy);
    expect(d.startsWith("M")).toBe(true);
    expect(d.endsWith("Z")).toBe(true);
    expect(d.length).toBeLessThan(6000);
  });

  it("puts north up and Boulder north of Denver", () => {
    const { xy } = projector(ring);
    expect(xy(-105.27, 40.01)[1]).toBeLessThan(xy(-104.99, 39.74)[1]);
  });
});
