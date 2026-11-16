import type { APIRoute } from "astro";
import { geojson } from "../../data/corridor";

// The corridor boundary and the 53 markers, as the repo holds them, with their ODbL notice.
export const GET: APIRoute = () =>
  new Response(JSON.stringify(geojson), { headers: { "content-type": "application/geo+json; charset=utf-8" } });
