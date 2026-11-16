import { describe, expect, it } from "vitest";
import { anchors, companies } from "../data/corridor";
import type { Anchor } from "../data/parse";
import { corridorAnchors, inTown, TOWNS, townStats } from "./home";

const a = (city: string): Anchor => ({ name: city, city, relevance: "", source: null });

describe("towns", () => {
  it("matches a town as a whole word", () => {
    expect(inTown("Boulder and Louisville", "Boulder")).toBe(true);
    expect(inTown("Arvada (Quantum Commons)", "Arvada")).toBe(true);
    expect(inTown("Goldenrod", "Golden")).toBe(false);
  });

  it("keeps only anchors in the four core towns", () => {
    expect(corridorAnchors([a("Boulder"), a("Fort Collins"), a("Statewide"), a("Arvada (Quantum Commons)")]).map((x) => x.city)).toEqual(["Boulder", "Arvada (Quantum Commons)"]);
  });

  it("finds the real anchors in the record", () => {
    const boulder = townStats(TOWNS[0], companies, anchors);
    expect(boulder.anchors.map((x) => x.name)).toContain("NIST Boulder");
    expect(boulder.companies.length).toBeGreaterThan(10);
    const golden = townStats(TOWNS[1], companies, anchors);
    expect(golden.anchors.map((x) => x.name).join(" ")).toMatch(/Mines/);
    expect(corridorAnchors(anchors).every((x) => !/Fort Collins|Colorado Springs|Statewide/.test(x.city))).toBe(true);
  });

  it("keeps the fab in the 2026 clock", () => {
    expect(TOWNS.find((t) => t.id === "arvada")).toMatchObject({ clock: "2026", art: null });
  });
});
