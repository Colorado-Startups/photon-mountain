import type { APIRoute } from "astro";
import { companies } from "../../data/corridor";
import { toCsv } from "../../data/parse";

const rows = companies.map((c) => ({ ...c, source_label: c.source?.label ?? "", source_url: c.source?.url ?? "" }));

export const GET: APIRoute = () =>
  new Response(toCsv(rows, ["name", "city", "ring", "segment", "tie", "builds", "source_label", "source_url"]), {
    headers: { "content-type": "text/csv; charset=utf-8" },
  });
