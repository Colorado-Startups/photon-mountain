import type { APIRoute } from "astro";
import { meta, sites } from "../../data/corridor";

// Coordinates derive from OpenStreetMap, so this file carries the ODbL and its credit (LICENSING.md).
export const GET: APIRoute = () =>
  Response.json({ ...meta, license: "ODbL-1.0", attribution: "© OpenStreetMap contributors", count: sites.length, sites });
