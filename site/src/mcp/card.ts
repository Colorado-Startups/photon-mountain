// Discovery for /mcp, per the MCP Server Card extension (SEP-2127, modelcontextprotocol/experimental-ext-server-card,
// read 2026-11-16): the card lives at <endpoint>/server-card, and /.well-known/ai-catalog.json points at it.
// The card names the endpoint on the origin that served it, so the preview's card points at the preview.
import { VERSION } from "./server";

export const CARD_TYPE = "application/mcp-server-card+json";
export const CATALOG_TYPE = "application/ai-catalog+json";

export function serverCard(origin: string) {
  return {
    $schema: "https://static.modelcontextprotocol.io/schemas/v1/server-card.schema.json",
    name: "co.photonmountain/corridor",
    version: VERSION,
    title: "Photon Mountain",
    description: "Companies, labs, map sites and sourced figures for Colorado's computing-with-light corridor.",
    websiteUrl: `${origin}/`,
    repository: { source: "github", url: "https://github.com/Colorado-Startups/photon-mountain" },
    remotes: [{ type: "streamable-http", url: `${origin}/mcp`, supportedProtocolVersions: ["2025-06-18", "2025-11-25"] }],
  };
}

export function aiCatalog(origin: string) {
  return { specVersion: "1.0", entries: [{ identifier: "urn:air:photonmountain.co:mcp:corridor", type: CARD_TYPE, url: `${origin}/mcp/server-card` }] };
}
