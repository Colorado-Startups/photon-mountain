import type { APIRoute } from "astro";
import { llmsFull } from "../ai/content";

export const GET: APIRoute = () => new Response(llmsFull(), { headers: { "content-type": "text/markdown; charset=utf-8" } });
