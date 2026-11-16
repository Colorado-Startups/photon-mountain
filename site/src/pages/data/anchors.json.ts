import type { APIRoute } from "astro";
import { anchors, meta } from "../../data/corridor";

export const GET: APIRoute = () => Response.json({ ...meta, license: "CC0-1.0", count: anchors.length, anchors });
