import { describe, expect, it } from "vitest";
import readme from "../../../03_deliverables/infographics/photon_mountain_map_README.md?raw";
import { CORES, scaled } from "./versus";

describe("the comparison", () => {
  it("quotes each measured diameter from the maps' README", () => {
    for (const c of CORES) expect(readme, c.id).toContain(c.match);
  });
  it("draws both cores to one scale", () => {
    const s = Object.fromEntries(scaled().map((x) => [x.id, x.share]));
    expect(s.pm).toBe(1);
    expect(s.sv).toBeCloseTo(18 / 24.1, 3);
  });
});
