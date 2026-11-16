import type { APIRoute } from "astro";
import { companies, corridorCompanies, meta } from "../../data/corridor";

// count is every row in roster sections 1 to 7; corridor_count is the Core and Ring rows only.
export const GET: APIRoute = () =>
  Response.json({ ...meta, license: "CC0-1.0", count: companies.length, corridor_count: corridorCompanies.length, companies });
