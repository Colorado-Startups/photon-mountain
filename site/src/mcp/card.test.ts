import { describe, expect, it } from "vitest";
import { CARD_TYPE, aiCatalog, serverCard } from "./card";
import { VERSION } from "./server";

describe("the server card and the AI catalog", () => {
  it("fills the card's required fields within the schema's limits, and names the serving origin", () => {
    const card = serverCard("https://photonmountain.co");
    expect(card.$schema).toBe("https://static.modelcontextprotocol.io/schemas/v1/server-card.schema.json");
    expect(card.name).toMatch(/^[a-zA-Z0-9.-]+\/[a-zA-Z0-9._-]+$/);
    expect(card.version).toBe(VERSION);
    expect(card.description.length).toBeLessThanOrEqual(100);
    expect(card.remotes[0]).toMatchObject({ type: "streamable-http", url: "https://photonmountain.co/mcp" });
    expect(serverCard("https://x.workers.dev").remotes[0].url).toBe("https://x.workers.dev/mcp");
  });

  it("points the catalog at the card", () => {
    const entry = aiCatalog("https://photonmountain.co").entries[0];
    expect(entry).toEqual({ identifier: "urn:air:photonmountain.co:mcp:corridor", type: CARD_TYPE, url: "https://photonmountain.co/mcp/server-card" });
  });
});
