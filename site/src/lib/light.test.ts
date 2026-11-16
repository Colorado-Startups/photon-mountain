import { describe, expect, it } from "vitest";
import { companies, corridorCompanies } from "../data/corridor";
import { branches, segmentOf, SEGMENTS } from "./light";

describe("the light diagram", () => {
  it("maps every roster segment to one branch", () => {
    for (const heading of new Set(companies.map((c) => c.segment))) expect(segmentOf(heading), heading).toBeDefined();
  });

  it("splits light into information and energy, and counts every corridor company once", () => {
    const b = branches(corridorCompanies);
    expect(new Set(SEGMENTS.map((s) => s.branch))).toEqual(new Set(["information", "energy"]));
    expect(b.reduce((n, s) => n + s.companies.length, 0)).toBe(corridorCompanies.length);
    expect(b.find((s) => s.short === "Solar")?.branch).toBe("energy");
  });
});
