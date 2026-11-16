import { describe, expect, it } from "vitest";
import { anchors, companies, figures, sites } from "./data/corridor";
import { readRpc } from "./mcp/rpc";
import worker, { type Env, HEADERS } from "./worker";

const files: Record<string, object> = {
  "/data/companies.json": { companies }, "/data/anchors.json": { anchors }, "/data/sites.json": { sites }, "/data/figures.json": { figures },
};
const env = (allow = true, seen: string[] = []): Env => ({
  ASSETS: { fetch: async (r) => { const p = new URL(r.url).pathname; seen.push(p); return files[p] ? Response.json(files[p]) : new Response("page", { status: p === "/" ? 200 : 404 }); } },
  MCP_LIMIT: { limit: async () => ({ success: allow }) },
});
const call = (e: Env, path = "/mcp") => worker.fetch(new Request(`https://photonmountain.co${path}`, {
  method: "POST",
  headers: { host: "photonmountain.co", "content-type": "application/json", accept: "application/json, text/event-stream", "mcp-protocol-version": "2025-11-25" },
  body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/list" }),
}), e);

describe("the Worker", () => {
  it("hands every path but /mcp to the static assets", async () => {
    const seen: string[] = [];
    expect((await worker.fetch(new Request("https://photonmountain.co/no-such-page/"), env(true, seen))).status).toBe(404);
    expect(seen).toEqual(["/no-such-page/"]);
  });

  it("answers 429 with its own headers when the rate limit says no", async () => {
    const res = await call(env(false));
    expect(res.status).toBe(429);
    expect(res.headers.get("retry-after")).toBe("60");
    expect(res.headers.get("x-content-type-options")).toBe("nosniff");
  });

  it("answers 503 with its headers when the data files do not load, then 413 for an oversized body", async () => {
    const broken: Env = { ...env(), ASSETS: { fetch: async () => new Response("gone", { status: 500 }) } };
    const res = await call(broken);
    expect(res.status).toBe(503);
    expect(res.headers.get("retry-after")).toBe("60");
    const big = await worker.fetch(new Request("https://photonmountain.co/mcp", { method: "POST", headers: { "content-length": "20000" }, body: "x" }), env());
    expect(big.status).toBe(413);
  });

  it("serves the MCP tools from the built data files, with the security headers", async () => {
    const seen: string[] = [];
    const res = await call(env(true, seen));
    expect(res.status).toBe(200);
    expect((await readRpc(res)).result?.tools).toHaveLength(6);
    expect(seen.sort()).toEqual(Object.keys(files).sort());
    for (const [k, v] of Object.entries(HEADERS)) expect(res.headers.get(k)).toBe(v);
  });
});
