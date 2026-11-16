import { describe, expect, it } from "vitest";
import { anchors, companies, figures, sites } from "../data/corridor";
import { mcpHandler, tools } from "./server";

const record = { companies, anchors, sites, figures };
const t = tools(record);

describe("the MCP tools", () => {
  it("search finds a lab, a company and a site, and caps the list", () => {
    expect(t.search("NIST").results.some((x) => x.kind === "research anchor")).toBe(true);
    expect(t.search("laser").results.some((x) => x.kind === "company")).toBe(true);
    const all = t.search("ar", 3);
    expect(all.results).toHaveLength(3);
    expect(all.total).toBeGreaterThan(3);
  });

  it("lists what each filter says, and every site carries the OpenStreetMap credit", () => {
    const golden = t.listAnchors("Golden");
    expect(golden.count).toBeGreaterThan(0);
    for (const a of golden.anchors) expect(a.city).toMatch(/Golden/);
    expect(t.listCompanies({}).count).toBe(companies.length);
    for (const c of t.listCompanies({ ring: "Core" }).companies) expect(c.ring).toBe("Core");
    expect(t.listCompanies({ segment: "Solar" }).count).toBeGreaterThan(0);
    expect(t.listSites().count).toBe(53);
    expect(t.listSites("National Lab").sites.every((s) => s.category === "National Lab")).toBe(true);
    expect(t.listSites().credit).toContain("OpenStreetMap");
  });

  it("gets one site by name, any case, and nothing for an unknown name", () => {
    const first = sites[0];
    expect(t.getSite(first.name.toUpperCase())).toMatchObject({ name: first.name, lat: first.lat });
    expect(t.getSite("No Such Place")).toBeNull();
  });

  it("gives every figure its owner, source, date and clock", () => {
    for (const f of t.getFigures().figures) {
      expect(f.source).toMatch(/^https:\/\//);
      expect(f.read).toMatch(/^\d{4}-\d{2}-\d{2}$/);
      expect(["today", "2026", "horizon"]).toContain(f.clock);
    }
  });
});

describe("the /mcp endpoint", () => {
  const handler = mcpHandler(record);
  const rpc = (body: object, host = "localhost") =>
    handler.fetch(new Request(`http://${host}/mcp`, {
      method: "POST",
      // The handler reads the Host header, which a Worker always has; Node's Request does not add it.
      headers: { host, "content-type": "application/json", accept: "application/json, text/event-stream", "mcp-protocol-version": "2025-11-25" },
      body: JSON.stringify({ jsonrpc: "2.0", id: 1, ...body }),
    }));

  it("initializes, lists the six read-only tools, and answers a call", async () => {
    const init = await rpc({ method: "initialize", params: { protocolVersion: "2025-11-25", capabilities: {}, clientInfo: { name: "test", version: "1" } } });
    expect(init.status).toBe(200);
    expect((await init.json()).result.serverInfo.name).toBe("photon-mountain");

    const list = await (await rpc({ method: "tools/list" })).json();
    const names = list.result.tools.map((x: { name: string }) => x.name).sort();
    expect(names).toEqual(["get_figures", "get_site", "list_anchors", "list_companies", "list_sites", "search"]);
    for (const tool of list.result.tools) expect(tool.annotations.readOnlyHint).toBe(true);

    const call = await (await rpc({ method: "tools/call", params: { name: "list_anchors", arguments: { town: "Golden" } } })).json();
    expect(JSON.parse(call.result.content[0].text).count).toBeGreaterThan(0);
  });

  it("refuses a Host it does not serve", async () => {
    const res = await rpc({ method: "tools/list" }, "evil.example");
    expect(res.status).toBeGreaterThanOrEqual(400);
  });
});
