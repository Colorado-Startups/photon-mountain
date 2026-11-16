// Silicon Valley and Photon Mountain, core to core, at one scale. The measured diameters come from the
// comparison maps' verify script, as 03_deliverables/infographics/photon_mountain_map_README.md records them.
export const DOC = "03_deliverables/infographics/photon_mountain_map_README.md";

export const CORES = [
  { id: "sv", name: "Silicon Valley", from: "Menlo Park", to: "San Jose", miles: 18.0, element: "Si", what: "Named for the material of the last computing era", match: "Menlo Park to San Jose, 18.0 measured" },
  { id: "pm", name: "Photon Mountain", from: "Boulder", to: "Denver", miles: 24.1, element: "γ", what: "Named for the medium of the next one", match: "Boulder to Denver, 24.1 measured" },
] as const;

/** Each core's length as a share of the longer one, for bars drawn to scale. */
export function scaled(): { id: string; share: number }[] {
  const max = Math.max(...CORES.map((c) => c.miles));
  return CORES.map((c) => ({ id: c.id, share: c.miles / max }));
}
