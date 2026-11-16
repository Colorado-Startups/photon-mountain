import { describe, expect, it } from "vitest";
import { anchors, companies, sites } from "../data/corridor";
import { DATA, PAGES, jsonLd, llmsFull, llmsTxt, mdPath, pageFor, pageMarkdown } from "./content";

describe("llms.txt", () => {
  it("follows llmstxt.org: an H1, a blockquote, then H2 sections of links, Optional last", () => {
    const t = llmsTxt().split("\n");
    expect(t[0]).toBe("# Photon Mountain");
    expect(t[2].startsWith("> ")).toBe(true);
    const h2 = t.filter((l) => l.startsWith("## "));
    expect(h2).toEqual(["## Pages", "## Data", "## Optional"]);
  });

  it("links only to the Markdown twins and data files the site builds", () => {
    const built = new Set([...PAGES.map(mdPath), ...DATA.map((d) => d.path), "/llms-full.txt"]);
    const local = [...llmsTxt().matchAll(/\]\(https:\/\/photonmountain\.co(\/[^)]*)\)/g)].map((m) => m[1]);
    expect(local).toHaveLength(PAGES.length + DATA.length + 1);
    for (const p of local) expect(built.has(p), p).toBe(true);
  });
});

describe("the Markdown twins and the full record", () => {
  it("builds a twin for every page and finds a page by its path", () => {
    for (const p of PAGES) {
      expect(pageMarkdown(p.slug).startsWith(`# ${p.title}\n`)).toBe(true);
      expect(pageFor(p.path)).toBe(p);
    }
    expect(pageFor("/no-such-page/")).toBeUndefined();
    expect(() => pageMarkdown("nope")).toThrow();
  });

  it("names every company, anchor and site, and credits OpenStreetMap", () => {
    const full = llmsFull();
    for (const x of [...companies, ...anchors, ...sites]) expect(full, x.name).toContain(`**${x.name}**`);
    expect(full).toContain("© OpenStreetMap contributors");
    expect(pageMarkdown("map")).toContain("© OpenStreetMap contributors");
  });
});

describe("JSON-LD", () => {
  it("describes the place, the list and the dataset, and nothing on the map or world pages", () => {
    expect(jsonLd("index")).toMatchObject({ "@type": "Place", name: "Photon Mountain" });
    expect(jsonLd("explore")).toMatchObject({ "@type": "ItemList", numberOfItems: anchors.length + companies.length });
    const ds = jsonLd("data") as { "@type": string; distribution: { license: string }[] };
    expect(ds["@type"]).toBe("Dataset");
    expect(ds.distribution).toHaveLength(DATA.length);
    for (const d of ds.distribution) expect(d.license).toMatch(/^https:\/\//);
    expect(jsonLd("world")).toBeNull();
    expect(jsonLd("map")).toBeNull();
  });
});
