// The art manifest, as the pages use it: a srcset for each painting and the sources for each clip.
import manifest from "../../art/manifest.json";

export const WIDTHS = [480, 960, 1440];

export interface ArtImage {
  id: string; file: string; width: number; height: number; place: string; alt: string; caption: string; model: string;
}

export const images = manifest.images as ArtImage[];
export const clips = manifest.clips;
export const label = manifest.label;

export function image(id: string): ArtImage {
  const found = images.find((i) => i.id === id);
  if (!found) throw new Error(`no art named ${id}`);
  return found;
}

/** The WebP srcset for an image, every width up to its own. */
export function srcset(img: ArtImage): string {
  return WIDTHS.filter((w) => w <= img.width).map((w) => `/art/${img.id}-${w}.webp ${w}w`).join(", ");
}

/** The smallest variant at or above a target width, for a poster or a preload. */
export function variant(img: ArtImage, target: number): string {
  const w = WIDTHS.filter((x) => x <= img.width).find((x) => x >= target) ?? Math.min(img.width, WIDTHS[WIDTHS.length - 1]);
  return `/art/${img.id}-${w}.webp`;
}
