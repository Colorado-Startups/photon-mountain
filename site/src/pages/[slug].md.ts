import type { APIRoute, GetStaticPaths } from "astro";
import { PAGES, pageMarkdown } from "../ai/content";

// One Markdown twin per page: /index.md, /map.md, /explore.md, /world.md, /data.md.
export const getStaticPaths: GetStaticPaths = () => PAGES.map((p) => ({ params: { slug: p.slug } }));

export const GET: APIRoute = ({ params }) =>
  new Response(pageMarkdown(String(params.slug)), { headers: { "content-type": "text/markdown; charset=utf-8" } });
