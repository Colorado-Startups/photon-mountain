import type { APIRoute } from "astro";
import { figures, repo } from "../../data/corridor";

export const GET: APIRoute = () =>
  Response.json({ source: `${repo}/blob/main/02_substance/figures.json`, license: "CC0-1.0", figures });
