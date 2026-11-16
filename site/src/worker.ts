// The Worker in front of the static site. wrangler.jsonc runs it first only for /mcp, its server card and the
// AI catalog; every page and data file is served as a static asset without it. A path that matches no asset
// also lands here, and goes back to the asset layer for its 404 page. The MCP tools read the built /data/
// files, so the record has one copy.
import { CARD_TYPE, CATALOG_TYPE, aiCatalog, serverCard } from "./mcp/card";
import { type McpRecord, mcpHandler } from "./mcp/server";

export interface Env {
  ASSETS: { fetch(request: Request): Promise<Response> };
  MCP_LIMIT: { limit(options: { key: string }): Promise<{ success: boolean }> };
}

// public/_headers covers static assets only, so /mcp sets its own.
export const HEADERS: Record<string, string> = {
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "no-referrer",
  "Cache-Control": "no-store",
  "X-Robots-Tag": "noindex",
};

const MAX_BODY = 16_384;
let handler: Promise<ReturnType<typeof mcpHandler>> | undefined;

async function load(env: Env, base: URL): Promise<McpRecord> {
  const get = async (path: string) => {
    const res = await env.ASSETS.fetch(new Request(new URL(path, base)));
    if (!res.ok) throw new Error(`${path}: HTTP ${res.status}`);
    return res.json() as Promise<Record<string, unknown>>;
  };
  const [c, a, s, f] = await Promise.all(["/data/companies.json", "/data/anchors.json", "/data/sites.json", "/data/figures.json"].map(get));
  return { companies: c.companies, anchors: a.anchors, sites: s.sites, figures: f.figures } as McpRecord;
}

function withHeaders(res: Response): Response {
  const out = new Response(res.body, res);
  for (const [k, v] of Object.entries(HEADERS)) out.headers.set(k, v);
  return out;
}

// The card and the catalog: read-only documents any origin may fetch, cached for an hour.
function discovery(request: Request, body: () => object, type: string): Response {
  const cors = { "access-control-allow-origin": "*", "access-control-allow-methods": "GET, HEAD, OPTIONS" };
  if (request.method === "OPTIONS") return withHeaders(new Response(null, { status: 204, headers: cors }));
  if (request.method !== "GET" && request.method !== "HEAD") return withHeaders(new Response("Method not allowed.", { status: 405, headers: { allow: "GET, HEAD, OPTIONS" } }));
  const res = withHeaders(new Response(request.method === "HEAD" ? null : JSON.stringify(body(), null, 1), { headers: { ...cors, "content-type": type } }));
  res.headers.set("cache-control", "public, max-age=3600");
  return res;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const docs: Record<string, [() => object, string]> = {
      "/mcp/server-card": [() => serverCard(url.origin), CARD_TYPE],
      "/.well-known/ai-catalog.json": [() => aiCatalog(url.origin), CATALOG_TYPE],
    };
    const found = docs[url.pathname];
    if (found) return discovery(request, ...found);
    if (url.pathname !== "/mcp") return env.ASSETS.fetch(request);
    // About one call a second per address, counted per Cloudflare location (rate-limit binding docs).
    const { success } = await env.MCP_LIMIT.limit({ key: request.headers.get("cf-connecting-ip") ?? "unknown" });
    if (!success) return withHeaders(new Response("Too many requests. Try again in a minute.", { status: 429, headers: { "Retry-After": "60" } }));
    // The tools take small JSON; a large body would spend CPU before any tool runs.
    if (Number(request.headers.get("content-length") ?? 0) > MAX_BODY) return withHeaders(new Response("Request too large.", { status: 413 }));
    // One handler per isolate; a failed load is dropped so the next request tries again, and answers 503.
    handler ??= load(env, url).then(mcpHandler).catch((err) => { handler = undefined; throw err; });
    try {
      return withHeaders(await (await handler).fetch(request));
    } catch (err) {
      console.error("mcp: the record did not load", err);
      return withHeaders(new Response("The record is not available right now. Try again in a minute.", { status: 503, headers: { "Retry-After": "60" } }));
    }
  },
};
