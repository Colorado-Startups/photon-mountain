import { describe, expect, it } from "vitest";
import { countBy, csvField, firstLink, parseAnchors, parseCompanies, parseSites, plain, splitCity, tables, toCsv } from "./parse";

const md = `# Roster

## 1. Photonic chips

| Company | City (corridor) | Colorado tie | What they build with light | Source |
|---|---|---|---|---|
| **Acme Light** | Boulder (Core) | HQ | Chips, with a [paper](https://a.example/p). | [acme.example](https://acme.example/) |
| Far Co | San Jose, CA (roots only) | Roots only | Optical I/O | none |

## Anchor research institutions

| Institution | City | Photonics relevance | Source |
|---|---|---|---|
| NIST Boulder | Boulder | Clocks | [nist.gov](https://www.nist.gov/) |

## 9. Checked and excluded

| Company | City (corridor) | Colorado tie | What they build with light | Source |
|---|---|---|---|---|
| Gone Inc | Denver (Core) | none | none | none |
`;

describe("roster parsing", () => {
  it("reads sections 1 to 7 only", () => {
    const c = parseCompanies(md);
    expect(c.map((x) => x.name)).toEqual(["Acme Light", "Far Co"]);
    expect(c[0]).toMatchObject({ city: "Boulder", ring: "Core", segment: "Photonic chips", source: { url: "https://acme.example/" } });
    expect(c[1]).toMatchObject({ city: "San Jose, CA", ring: "Roots only", source: null });
  });
  it("reads the anchors", () => {
    expect(parseAnchors(md)).toEqual([{ name: "NIST Boulder", city: "Boulder", relevance: "Clocks", source: { label: "nist.gov", url: "https://www.nist.gov/" } }]);
  });
  it("keeps headings and skips divider rows", () => {
    expect(tables(md).map((t) => [t.heading, t.rows.length])).toEqual([["1. Photonic chips", 2], ["Anchor research institutions", 1], ["9. Checked and excluded", 1]]);
  });
});

describe("cell helpers", () => {
  it("strips Markdown", () => expect(plain("**Bold** and [a link](https://x.example)")).toBe("Bold and a link"));
  it("finds the first link", () => expect(firstLink("see [one](https://1.example) [two](https://2.example)")).toEqual({ label: "one", url: "https://1.example" }));
  it("splits city and ring", () => {
    expect(splitCity("Longmont (Ring)")).toEqual({ city: "Longmont", ring: "Ring" });
    expect(splitCity("Thornton (Statewide)")).toEqual({ city: "Thornton", ring: "Statewide" });
    expect(splitCity("Somewhere")).toEqual({ city: "Somewhere", ring: "Other" });
    expect(splitCity("Boulder and Louisville (Core and Ring)")).toEqual({ city: "Boulder and Louisville", ring: "Core" });
    expect(splitCity("Centennial / Louisville (Statewide/Ring)")).toEqual({ city: "Centennial / Louisville", ring: "Ring" });
    expect(splitCity("Golden (Quantum Commons)")).toEqual({ city: "Golden", ring: "Other" });
  });
});

describe("sites", () => {
  it("keeps points and drops the boundary", () => {
    const s = parseSites({ features: [
      { geometry: { type: "Point", coordinates: [-105.2, 40] }, properties: { name: "Lab", category: "National Lab" } },
      { geometry: { type: "Polygon", coordinates: [] }, properties: { name: "Boundary" } },
    ] });
    expect(s).toEqual([{ name: "Lab", category: "National Lab", note: "", lon: -105.2, lat: 40 }]);
  });
});

describe("CSV", () => {
  it("quotes only when needed", () => {
    expect(csvField("plain")).toBe("plain");
    expect(csvField('a, "b"')).toBe('"a, ""b"""');
    expect(csvField(null)).toBe("");
  });
  it("writes a header and CRLF rows", () => {
    expect(toCsv([{ a: 1, b: "x,y" }], ["a", "b"])).toBe('a,b\r\n1,"x,y"\r\n');
  });
  it("counts largest first", () => {
    expect(countBy(["b", "a", "b"], (x) => x)).toEqual([["b", 2], ["a", 1]]);
  });
});
