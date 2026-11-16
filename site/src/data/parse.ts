// Pure parsers for the repo's own records: the roster's Markdown tables and the corridor GeoJSON.
// No file access here, so every function is unit-tested with plain strings (parse.test.ts).

export type Ring = "Core" | "Ring" | "Statewide" | "Roots only" | "Other";

export interface Link { label: string; url: string }

export interface Company {
  name: string;
  city: string;
  ring: Ring;
  tie: string;
  builds: string;
  source: Link | null;
  segment: string;
}

export interface Anchor { name: string; city: string; relevance: string; source: Link | null }

export interface Site { name: string; category: string; note: string; lon: number; lat: number }

const LINK = /\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/;

/** The first Markdown link in a cell, or null. */
export function firstLink(cell: string): Link | null {
  const m = LINK.exec(cell);
  return m ? { label: m[1], url: m[2] } : null;
}

/** A cell as plain text: links keep their label, bold and code marks go. */
export function plain(cell: string): string {
  return cell
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/\*\*|`/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

/** "Boulder (Core)" to the city and its corridor ring. A company in two places ("Core and Ring",
    "Statewide/Ring") takes the more central one. */
export function splitCity(cell: string): { city: string; ring: Ring } {
  const m = /^(.*?)\s*\(([^)]+)\)\s*$/.exec(plain(cell));
  if (!m) return { city: plain(cell), ring: "Other" };
  const tag = m[2].toLowerCase();
  const ring: Ring = tag.includes("core")
    ? "Core"
    : /\bring\b/.test(tag)
      ? "Ring"
      : tag.includes("statewide")
        ? "Statewide"
        : tag.includes("roots")
          ? "Roots only"
          : "Other";
  return { city: m[1], ring };
}

/** The cells of one Markdown table row, or null for a line that is not a row. */
export function cells(line: string): string[] | null {
  const t = line.trim();
  if (!t.startsWith("|") || !t.endsWith("|")) return null;
  return t.slice(1, -1).split("|").map((c) => c.trim());
}

interface Table { heading: string; header: string[]; rows: string[][] }

/** Every table under a "## " heading, with the heading it sits under. */
export function tables(md: string): Table[] {
  const out: Table[] = [];
  let heading = "";
  let current: Table | null = null;
  for (const line of md.split("\n")) {
    if (line.startsWith("## ")) heading = line.slice(3).trim();
    const row = cells(line);
    if (!row) { current = null; continue; }
    if (row.every((c) => /^:?-{3,}:?$/.test(c))) continue;
    if (!current) { current = { heading, header: row, rows: [] }; out.push(current); continue; }
    current.rows.push(row);
  }
  return out;
}

/** The numbered roster sections 1 to 7: one company per row. */
export function parseCompanies(md: string): Company[] {
  return tables(md)
    .filter((t) => /^[1-7]\. /.test(t.heading) && t.header[0] === "Company")
    .flatMap((t) =>
      t.rows.map((r) => {
        const { city, ring } = splitCity(r[1] ?? "");
        return {
          name: plain(r[0] ?? ""),
          city,
          ring,
          tie: plain(r[2] ?? ""),
          builds: plain(r[3] ?? ""),
          source: firstLink(r[4] ?? ""),
          segment: t.heading.replace(/^\d+\.\s*/, ""),
        };
      }),
    );
}

/** The anchor research institutions table. */
export function parseAnchors(md: string): Anchor[] {
  const t = tables(md).find((x) => x.heading.startsWith("Anchor research institutions") && x.header[0] === "Institution");
  return (t?.rows ?? []).map((r) => ({ name: plain(r[0]), city: plain(r[1]), relevance: plain(r[2]), source: firstLink(r[3] ?? "") }));
}

interface Feature { geometry: { type: string; coordinates: number[] }; properties: Record<string, unknown> }

/** The point markers of the corridor GeoJSON. */
export function parseSites(geojson: { features: Feature[] }): Site[] {
  return geojson.features
    .filter((f) => f.geometry.type === "Point")
    .map((f) => ({
      name: String(f.properties.name),
      category: String(f.properties.category),
      note: String(f.properties.note ?? ""),
      lon: f.geometry.coordinates[0],
      lat: f.geometry.coordinates[1],
    }));
}

/** One CSV field, quoted when it holds a comma, quote or line break (RFC 4180). */
export function csvField(value: unknown): string {
  const s = value === null || value === undefined ? "" : String(value);
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

/** Rows of objects to CSV with the given columns. */
export function toCsv<T extends object>(rows: T[], columns: (keyof T & string)[]): string {
  const lines = [columns.join(",")];
  for (const row of rows) lines.push(columns.map((c) => csvField(row[c])).join(","));
  return lines.join("\r\n") + "\r\n";
}

/** Counts of items by a key, largest first. */
export function countBy<T>(items: T[], key: (item: T) => string): [string, number][] {
  const m = new Map<string, number>();
  for (const it of items) m.set(key(it), (m.get(key(it)) ?? 0) + 1);
  return [...m.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
}
