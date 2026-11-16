import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { describe, expect, it } from "vitest";
import sharp from "sharp";
import { checkHash, variants } from "../../scripts/art.mjs";
import { clips, image, images, label, srcset, variant } from "./art";

const original = (file: string) => readFileSync(new URL(`../../art/originals/${file}`, import.meta.url));

describe("the art manifest", () => {
  it("labels every picture and clip, and describes each one", () => {
    expect(label).toBe("AI-made");
    for (const a of [...images, ...clips]) {
      expect(a.alt.length, a.id).toBeGreaterThan(40);
      expect(a.caption, a.id).not.toBe("");
      expect(a.model, a.id).toMatch(/FIBO 2\.0|LTX-2\.5/);
    }
  });

  it("holds each file byte for byte as the brand published it", () => {
    for (const i of images) expect(createHash("sha256").update(original(i.file)).digest("hex"), i.id).toBe((i as unknown as { sha256: string }).sha256);
    for (const c of clips) for (const s of c.sources) expect(createHash("sha256").update(original(s.file)).digest("hex"), s.file).toBe(s.sha256);
  });

  it("builds srcsets only up to each image's own width", () => {
    expect(srcset(image("crest"))).toBe("/art/crest-480.webp 480w");
    expect(srcset(image("boulder"))).toBe("/art/boulder-480.webp 480w, /art/boulder-960.webp 960w, /art/boulder-1440.webp 1440w");
    expect(variant(image("boulder"), 700)).toBe("/art/boulder-960.webp");
    expect(variant(image("crest"), 900)).toBe("/art/crest-480.webp");
    expect(() => image("nope")).toThrow();
  });
});

describe("the art build", () => {
  it("refuses a file whose hash moved", () => {
    expect(() => checkHash("x", Buffer.from("x"), "0".repeat(64))).toThrow(/is not the brand's/);
  });

  it("keeps the provenance XMP in every WebP it makes", async () => {
    const out = await variants(original("boulder.jpg"), 1440);
    expect(out.map((v) => v.width)).toEqual([480, 960, 1440]);
    for (const v of out) {
      const meta = await sharp(v.data).metadata();
      expect(meta.format).toBe("webp");
      expect(meta.xmp?.toString("utf8"), `${v.width}w`).toContain("FIBO 2.0 (Bria)");
    }
  });
});
