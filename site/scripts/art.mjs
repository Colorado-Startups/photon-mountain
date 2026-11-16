// Prebuild: checks every art file against art/manifest.json, then writes what the pages load into
// public/art/ (gitignored). Each image gets WebP widths with its provenance XMP kept, plus the original as
// the fallback; clips are copied unchanged. A hash mismatch stops the build: the brand repo owns the art.
import { createHash } from "node:crypto";
import { copyFile, mkdir, readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

export const WIDTHS = [480, 960, 1440];
const here = (p) => fileURLToPath(new URL(p, import.meta.url));
const ORIGINALS = here("../art/originals/");
const OUT = here("../public/art/");

const sha256 = (buf) => createHash("sha256").update(buf).digest("hex");

/** Throws when a file's bytes differ from the manifest's hash. */
export function checkHash(name, buf, expected) {
  const got = sha256(buf);
  if (got !== expected) throw new Error(`${name}: sha256 ${got} is not the brand's ${expected}`);
}

/** WebP variants of one image at each width up to its own, XMP kept. */
export async function variants(buf, width) {
  const out = [];
  for (const w of WIDTHS.filter((x) => x <= width)) {
    const data = await sharp(buf).resize({ width: w }).keepXmp().webp({ quality: 74, effort: 5 }).toBuffer();
    out.push({ width: w, data });
  }
  return out;
}

async function main() {
  const manifest = JSON.parse(await readFile(here("../art/manifest.json"), "utf8"));
  await mkdir(OUT, { recursive: true });
  for (const img of manifest.images) {
    const buf = await readFile(ORIGINALS + img.file);
    checkHash(img.file, buf, img.sha256);
    for (const v of await variants(buf, img.width)) await writeFile(`${OUT}${img.id}-${v.width}.webp`, v.data);
    await copyFile(ORIGINALS + img.file, OUT + img.file);
  }
  for (const clip of manifest.clips) {
    for (const src of clip.sources) {
      checkHash(src.file, await readFile(ORIGINALS + src.file), src.sha256);
      await copyFile(ORIGINALS + src.file, OUT + src.file);
    }
  }
  console.log(`art: ${manifest.images.length} images and ${manifest.clips.length} clip written to public/art/`);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) await main();
