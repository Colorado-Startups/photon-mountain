// The home page's numbers and towns, from the corridor record. Pure functions, unit-tested in home.test.ts.
import type { Anchor, Company } from "../data/parse";

export interface Town { id: string; name: string; role: string; art: string | null; clock: "today" | "2026" }

/** The four core towns, in the facts doc's order and with its roles. */
export const TOWNS: Town[] = [
  { id: "boulder", name: "Boulder", role: "The research anchor", art: "boulder", clock: "today" },
  { id: "golden", name: "Golden", role: "The school and the national energy lab", art: "golden", clock: "today" },
  { id: "arvada", name: "Arvada", role: "The fab: planned, targeted for 2026, not yet operating", art: null, clock: "2026" },
  { id: "denver", name: "Denver", role: "The metro anchor", art: "denver", clock: "today" },
];

/** True when a roster place names the town as a whole word ("Boulder and Louisville" names Boulder). */
export function inTown(place: string, town: string): boolean {
  return new RegExp(`(^|[^A-Za-z])${town}([^A-Za-z]|$)`).test(place);
}

/** The anchor institutions in one of the four core towns. */
export function corridorAnchors(anchors: Anchor[]): Anchor[] {
  return anchors.filter((a) => TOWNS.some((t) => inTown(a.city, t.name)));
}

/** One town's companies and anchors. */
export function townStats(town: Town, companies: Company[], anchors: Anchor[]) {
  return {
    companies: companies.filter((c) => inTown(c.city, town.name)),
    anchors: anchors.filter((a) => inTown(a.city, town.name)),
  };
}
