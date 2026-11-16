import type { APIRoute } from "astro";
import { companies, meta } from "../../data/corridor";

export const GET: APIRoute = () =>
  Response.json({ ...meta, license: "CC0-1.0", count: companies.length, companies });
