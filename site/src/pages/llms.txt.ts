import type { APIRoute } from "astro";
import { llmsTxt } from "../ai/content";

export const GET: APIRoute = () => new Response(llmsTxt(), { headers: { "content-type": "text/markdown; charset=utf-8" } });
