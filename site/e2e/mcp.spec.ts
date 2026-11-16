import { type APIRequestContext, expect, test } from "@playwright/test";
import { readRpc } from "../src/mcp/rpc";

// These run against `wrangler dev` (playwright.config.ts), so they go through the real Worker and assets.
const rpc = (request: APIRequestContext, method: string, params: object = {}) =>
  request.post("/mcp", {
    headers: { accept: "application/json, text/event-stream", "content-type": "application/json", "mcp-protocol-version": "2025-11-25" },
    data: { jsonrpc: "2.0", id: 1, method, params },
  });

test.describe("the MCP endpoint", () => {
  test("lists six tools and reads one site through the Worker", async ({ request }) => {
    const list = await readRpc(await rpc(request, "tools/list"));
    expect(list.result?.tools).toHaveLength(6);
    const first = (await (await request.get("/data/sites.json")).json()).sites[0];
    const got = await readRpc(await rpc(request, "tools/call", { name: "get_site", arguments: { name: first.name } }));
    expect(JSON.parse(got.result?.content[0].text)).toMatchObject({ name: first.name, credit: expect.stringContaining("OpenStreetMap") });
  });

  test("serves its server card and the AI catalog, and the data page shows the setup", async ({ request, page }) => {
    const card = await request.get("/mcp/server-card");
    expect(card.headers()["content-type"]).toBe("application/mcp-server-card+json");
    expect((await card.json()).remotes[0].url).toMatch(/\/mcp$/);
    const cat = await request.get("/.well-known/ai-catalog.json");
    expect((await cat.json()).entries[0].type).toBe("application/mcp-server-card+json");
    await page.goto("/data/");
    await expect(page.locator(".connect li")).toHaveCount(4);
    for (const pre of await page.locator(".connect pre").allTextContents()) expect(pre).toContain("/mcp");
  });
});
