// The read-only MCP server at /mcp: six tools over the same record the pages and /data/ files carry.
// Stateless, per MCP's Streamable HTTP transport: createMcpHandler builds a fresh server for each request.
// Every answer names its source; site rows carry the OpenStreetMap credit their ODbL licence asks for.
import { McpServer } from "@modelcontextprotocol/server";
import { createMcpHandler } from "agents/mcp/server";
import { z } from "zod";
import type { Figure } from "../data/corridor";
import type { Anchor, Company, Site } from "../data/parse";
import { TOWNS, inTown } from "../lib/home";
import { SEGMENTS } from "../lib/light";
import { CATS } from "../lib/mapdata";

export const VERSION = "1.0.0";

export interface McpRecord { companies: Company[]; anchors: Anchor[]; sites: Site[]; figures: Figure[] }

/** Hosts the handler answers on; any other Host header is refused (DNS-rebinding guard). */
export const HOSTS = ["photonmountain.co", "www.photonmountain.co", "photon-mountain-site.coloradostartups.workers.dev", "localhost", "127.0.0.1"];
const OSM = "Site data © OpenStreetMap contributors, ODbL 1.0";
const RINGS = ["Core", "Ring", "Statewide", "Roots only"] as const;
const lower = (s: string) => s.toLowerCase();
const company = (c: Company) => ({ name: c.name, city: c.city, ring: c.ring, tie: c.tie, segment: c.segment, builds: c.builds, source: c.source?.url ?? null });
const anchor = (a: Anchor) => ({ name: a.name, city: a.city, relevance: a.relevance, source: a.source?.url ?? null });
const site = (s: Site) => ({ name: s.name, category: s.category, lat: s.lat, lon: s.lon, note: s.note });

/** What each tool returns, as plain data. Exported so the tests can read it without the protocol. */
export function tools(r: McpRecord) {
  return {
    search(query: string, limit = 10) {
      const q = lower(query.trim());
      const hit = (...fields: string[]) => fields.some((f) => lower(f).includes(q));
      const rows = [
        ...r.anchors.filter((a) => hit(a.name, a.city, a.relevance)).map((a) => ({ kind: "research anchor", ...anchor(a) })),
        ...r.companies.filter((c) => hit(c.name, c.city, c.builds, c.segment)).map((c) => ({ kind: "company", ...company(c) })),
        ...r.sites.filter((s) => hit(s.name, s.category, s.note)).map((s) => ({ kind: "map site", ...site(s), credit: OSM })),
      ];
      return { query, total: rows.length, results: rows.slice(0, limit) };
    },
    listCompanies(f: { town?: string; segment?: string; ring?: string }) {
      const seg = SEGMENTS.find((s) => s.short === f.segment);
      const rows = r.companies.filter((c) => (!f.town || inTown(c.city, f.town)) && (!seg || c.segment.startsWith(seg.prefix)) && (!f.ring || c.ring === f.ring));
      return { count: rows.length, companies: rows.map(company) };
    },
    listAnchors(town?: string) {
      const rows = r.anchors.filter((a) => !town || inTown(a.city, town));
      return { count: rows.length, anchors: rows.map(anchor) };
    },
    listSites(category?: string) {
      const rows = r.sites.filter((s) => !category || s.category === category);
      return { count: rows.length, credit: OSM, sites: rows.map(site) };
    },
    getSite(name: string) {
      const s = r.sites.find((x) => lower(x.name) === lower(name.trim()));
      return s ? { ...site(s), credit: OSM } : null;
    },
    getFigures() {
      return { figures: r.figures.map((f) => ({ value: f.value, label: f.label, whose: f.whose, source: f.source, read: f.read, clock: f.clock })) };
    },
  };
}

const text = (data: unknown) => ({ content: [{ type: "text" as const, text: JSON.stringify(data, null, 1) }] });
const readOnly = { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false };
const town = z.enum(TOWNS.map((t) => t.name) as [string, ...string[]]).optional().describe("One of the four core towns");

export function createServer(r: McpRecord): McpServer {
  const t = tools(r);
  const server = new McpServer(
    { name: "photon-mountain", version: VERSION },
    { instructions: "Photon Mountain is Colorado's Front Range corridor for computing with light: Boulder, Golden, Arvada and Denver. Cite a row's source link when it gives one. A company's tie says whether the town holds its headquarters or a facility. Figures carry a clock: today (operating now), 2026 (targeted this year) or horizon (later). Keep them apart." },
  );
  server.registerTool("search", { title: "Search the record", description: "Find companies, research anchors and map sites by name, city or what they build.", annotations: readOnly,
    inputSchema: z.object({ query: z.string().min(2).max(100), limit: z.number().int().min(1).max(50).optional() }) },
    async ({ query, limit }) => text(t.search(query, limit)));
  server.registerTool("list_companies", { title: "List companies", description: "Companies on the roster, filtered by town, what they build, or ring (Core and Ring are the corridor).", annotations: readOnly,
    inputSchema: z.object({ town, segment: z.enum(SEGMENTS.map((s) => s.short) as [string, ...string[]]).optional(), ring: z.enum(RINGS).optional() }) },
    async (f) => text(t.listCompanies(f)));
  server.registerTool("list_anchors", { title: "List research anchors", description: "The labs, universities and institutions that anchor the corridor, optionally in one town.", annotations: readOnly,
    inputSchema: z.object({ town }) },
    async ({ town }) => text(t.listAnchors(town)));
  server.registerTool("list_sites", { title: "List map sites", description: "The sites on the corridor map, optionally in one category.", annotations: readOnly,
    inputSchema: z.object({ category: z.enum(CATS.map((c) => c.id) as [string, ...string[]]).optional() }) },
    async ({ category }) => text(t.listSites(category)));
  server.registerTool("get_site", { title: "Get one map site", description: "One map site by its exact name, with its coordinates and note.", annotations: readOnly,
    inputSchema: z.object({ name: z.string().min(2).max(120) }) },
    async ({ name }) => {
      const s = t.getSite(name);
      return s ? text(s) : { ...text({ error: `No site named "${name}". Try the search tool.` }), isError: true };
    });
  server.registerTool("get_figures", { title: "Get the headline figures", description: "The headline figures, each with whose figure it is, its source, the date it was read, and its clock.", annotations: readOnly },
    async () => text(t.getFigures()));
  return server;
}

/** The /mcp handler for one record. Any origin may call it: it is public, read-only and keyless. JSON responses
 * apply to clients on the 2026 protocol; 2025 clients get one server-sent event per answer (src/mcp/rpc.ts). */
export const mcpHandler = (r: McpRecord) =>
  createMcpHandler(() => createServer(r), { route: "/mcp", allowedHostnames: HOSTS, allowedOriginHostnames: "*", responseMode: "json" });
