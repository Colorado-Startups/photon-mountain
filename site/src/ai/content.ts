// What the site says to AI assistants and crawlers, built from the same record as the pages: llms.txt
// (llmstxt.org), a Markdown twin of each page, the whole record in one file, and JSON-LD (schema.org).
// Pure functions; content.test.ts checks that every link points at a file the site builds.
import { anchors, clocks, companies, corridorCompanies, figures, repo, sites } from "../data/corridor";
import { images, label } from "../lib/art";
import { TOWNS, corridorAnchors, townStats } from "../lib/home";
import { SEGMENTS } from "../lib/light";
import { CATS } from "../lib/mapdata";

export const SITE = "https://photonmountain.co";
const ABOUT = "Colorado's Front Range corridor for computing with light, from Boulder through Golden and Arvada to Denver. A Colorado Startups project, a joint effort with Colorado Compute. Every figure names its source, and what operates today, what opens in 2026 and what sits on the horizon are kept apart.";

export interface Page { slug: string; path: string; title: string; summary: string }

export const PAGES: Page[] = [
  { slug: "index", path: "/", title: "Photon Mountain", summary: "The thesis, the headline figures, the four towns and the three clocks." },
  { slug: "map", path: "/map/", title: "The corridor map", summary: `The corridor boundary and its ${sites.length} sites, in ${CATS.length} categories.` },
  { slug: "explore", path: "/explore/", title: "Labs, universities and companies", summary: `${companies.length} companies and ${anchors.length} research anchors, each with its city, what it builds and its source.` },
  { slug: "world", path: "/world/", title: "The world of Photon Mountain", summary: "The AI-made paintings of Boulder, Golden and Denver, what each kept from the real place, and the photo each began as." },
  { slug: "data", path: "/data/", title: "Connect your AI", summary: "The data files, their licenses, and how to point an assistant at the record." },
];

const LICENSES: Record<string, string> = {
  "CC0-1.0": "https://creativecommons.org/publicdomain/zero/1.0/",
  "ODbL-1.0": "https://opendatacommons.org/licenses/odbl/1-0/",
};

export const DATA = [
  { path: "/data/companies.json", title: "Companies (JSON)", license: "CC0-1.0", type: "application/json" },
  { path: "/data/companies.csv", title: "Companies (CSV)", license: "CC0-1.0", type: "text/csv" },
  { path: "/data/anchors.json", title: "Research anchors (JSON)", license: "CC0-1.0", type: "application/json" },
  { path: "/data/figures.json", title: "Headline figures with sources (JSON)", license: "CC0-1.0", type: "application/json" },
  { path: "/data/sites.json", title: "Map sites (JSON)", license: "ODbL-1.0", type: "application/json" },
  { path: "/data/corridor.geojson", title: "Boundary and sites (GeoJSON)", license: "ODbL-1.0", type: "application/geo+json" },
];

export const mdPath = (p: Page) => `/${p.slug}.md`;
export const pageFor = (path: string) => PAGES.find((p) => p.path === path);
const link = (text: string, path: string) => `[${text}](${SITE}${path})`;
const src = (s: { url: string } | null) => (s ? ` Source: ${s.url}` : "");
const OSM = "Map data © OpenStreetMap contributors, ODbL 1.0. Everything else is CC0 1.0.";

export function llmsTxt(): string {
  return [
    "# Photon Mountain", "", `> ${ABOUT}`, "",
    `The whole record in one Markdown file: ${link("llms-full.txt", "/llms-full.txt")}.`, "",
    "## Pages", "", ...PAGES.map((p) => `- ${link(p.title, mdPath(p))}: ${p.summary}`), "",
    "## Data", "", ...DATA.map((d) => `- ${link(d.title, d.path)}: ${d.license}`), "",
    "## Optional", "",
    `- [Source repository](${repo}): the substance docs and every dated source`,
    `- [Map notes](${repo}/blob/main/03_deliverables/maps/MAP_NOTES.md): how the boundary and the sites were drawn`, "",
  ].join("\n");
}

const figuresMd = () => figures.map((f) => `- **${f.value}** ${f.label}. ${f.whose}, read ${f.read}: ${f.source}`);
const anchorsMd = () => anchors.map((a) => `- **${a.name}**, ${a.city}: ${a.relevance}${src(a.source)}`);

function clocksMd(): string[] {
  const lanes = [["today", "Operating today"], ["2026", "Targeted for 2026"], ["horizon", "On the horizon"]] as const;
  return lanes.flatMap(([id, name]) => [`### ${name}`, "", ...clocks.filter((c) => c.clock === id).map((c) => `- **${c.title}** (${c.when}, ${c.place}): ${c.text}`), ""]);
}

function companiesMd(): string[] {
  return SEGMENTS.flatMap((s) => {
    const rows = companies.filter((c) => c.segment.startsWith(s.prefix));
    return [`### ${s.short} (${rows.length})`, "", ...rows.map((c) => `- **${c.name}**, ${c.city} (${c.ring}): ${c.builds}${src(c.source)}`), ""];
  });
}

const sitesMd = () => CATS.flatMap((c) => [`### ${c.id}`, "", ...sites.filter((s) => s.category === c.id).map((s) => `- **${s.name}** (${s.lat.toFixed(5)}, ${s.lon.toFixed(5)}): ${s.note}`), ""]);

function body(slug: string): string[] {
  switch (slug) {
    case "index":
      return ["## The corridor in numbers", "",
        `- **${corridorCompanies.length}** companies in the corridor's core and ring towns, from the roster`,
        `- **${corridorAnchors(anchors).length}** research anchors in the four core towns`,
        `- **${sites.length}** sites on the map`, ...figuresMd(), "",
        "## Four towns", "",
        ...TOWNS.map((t) => { const s = townStats(t, companies, anchors); return `- **${t.name}**: ${t.role}. ${s.companies.length} companies, ${s.anchors.length} research anchors.`; }), "",
        "## Three clocks", "", ...clocksMd()];
    case "map":
      return ["## Sites by category", "", ...sitesMd(), OSM, ""];
    case "explore":
      return ["## Research anchors", "", ...anchorsMd(), "", "## Companies", "", ...companiesMd()];
    case "world":
      return [`Every picture is ${label}, made with FIBO 2.0 from a photo of the real place, and keeps its provenance metadata.`, "",
        ...images.filter((i) => i.landmark).flatMap((i) => [`## ${i.place}`, "", `- Keeps: ${i.landmark}`, `- Painted: ${i.alt}`, `- Photo: ${i.photo?.by}, ${i.photo?.licence}, ${i.photo?.url}`, ""])];
    default:
      return ["## Read it", "", `- ${link("llms.txt", "/llms.txt")}`, `- ${link("llms-full.txt", "/llms-full.txt")}`, "",
        "## Download it", "", ...DATA.map((d) => `- ${link(d.title, d.path)} (${d.license})`), ""];
  }
}

export function pageMarkdown(slug: string): string {
  const p = PAGES.find((x) => x.slug === slug);
  if (!p) throw new Error(`no page ${slug}`);
  return [`# ${p.title}`, "", `> ${p.summary}`, "", `Page: ${SITE}${p.path}`, "", ...body(slug)].join("\n");
}

export function llmsFull(): string {
  return ["# Photon Mountain", "", `> ${ABOUT}`, "",
    "## Headline figures", "", ...figuresMd(), "", "## Three clocks", "", ...clocksMd(),
    "## Research anchors", "", ...anchorsMd(), "", "## Companies", "", ...companiesMd(),
    "## Map sites", "", ...sitesMd(), OSM, ""].join("\n");
}

const publisher = { "@type": "Organization", name: "Colorado Startups", url: "https://coloradostartups.org/" };

/** The page's schema.org description, or null where none fits. */
export function jsonLd(slug: string): object | null {
  const ctx = "https://schema.org";
  if (slug === "index") return { "@context": ctx, "@type": "Place", name: "Photon Mountain", description: ABOUT, url: `${SITE}/`,
    containsPlace: TOWNS.map((t) => ({ "@type": "City", name: `${t.name}, Colorado` })) };
  if (slug === "explore") return { "@context": ctx, "@type": "ItemList", name: "Photon Mountain labs, universities and companies", numberOfItems: anchors.length + companies.length,
    itemListElement: [...anchors, ...companies].map((x, i) => ({ "@type": "ListItem", position: i + 1, item: { "@type": "Organization", name: x.name, ...(x.source ? { url: x.source.url } : {}) } })) };
  if (slug === "data" || slug === "map") return { "@context": ctx, "@type": "Dataset", name: "The Photon Mountain record",
    description: "Companies, research anchors, map sites and headline figures for Colorado's computing-with-light corridor, each with its source.",
    url: `${SITE}/data/`, creator: publisher, isAccessibleForFree: true,
    spatialCoverage: { "@type": "Place", name: "Boulder, Golden, Arvada and Denver, Colorado" },
    distribution: DATA.map((d) => ({ "@type": "DataDownload", name: d.title, contentUrl: SITE + d.path, encodingFormat: d.type, license: LICENSES[d.license] })) };
  return null;
}
