#!/usr/bin/env python3
"""
Independent geometry check for the Photon Mountain / Silicon Valley maps.

Reads the locked city data and the projection + blob construction from the
generator, then verifies, with its OWN point-in-polygon and containment tests:
  1. Tier labels match the locked spec (re-encoded here from scratch), and no
     city is flagged as a capital (capitals are retired).
  2. Every city sits inside the blob of its own tier and of every enclosing tier.
  3. The blobs nest: core inside greater inside outer (both the raw hulls and the
     buffered blobs).
  4. No dot is stranded outside the outermost region.
  5. Reports real core diameters in miles.

Exit code 0 only if every check passes.
"""
import math
import photon_mountain_map_generator as g

# Locked tier membership, re-encoded independently from the brief -----------
EXPECTED = {
    "SV": {
        "core": {"Palo Alto", "Mountain View", "Cupertino",
                 "Sunnyvale", "Santa Clara", "San Jose", "Menlo Park"},
        "greater": {"San Mateo", "Redwood City", "Fremont"},
        "outer": set(),
    },
    "PM": {
        "core": {"Boulder", "Golden", "Arvada", "Denver"},
        "greater": {"Louisville", "Broomfield", "Westminster",
                    "Lafayette", "Longmont"},
        "outer": set(),
    },
}
EXCLUDED = {"Castle Rock", "Colorado Springs", "Centennial", "Loveland",
            "Fort Collins", "Superior", "Oakland", "San Francisco",
            "Lakewood", "Englewood"}


def point_in_poly(pt, poly):
    """Independent ray-cast point-in-polygon (winding agnostic)."""
    x, y = pt
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and \
           (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
            inside = not inside
        j = i
    return inside


def _dist_pt_seg(p, a, b):
    px, py = p
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    if L2 == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def contained(pt, poly, tol=0.01):
    """Inside, or on the boundary within tol px. Closed-set containment, so two
    convex blobs that share a tangent edge (a shared extreme city) still nest."""
    if point_in_poly(pt, poly):
        return True
    n = len(poly)
    return any(_dist_pt_seg(pt, poly[i], poly[(i + 1) % n]) <= tol
               for i in range(n))


def poly_inside_poly(inner, outer):
    return all(contained(v, outer) for v in inner)


def miles(a, b):
    """Real distance in miles between two (lat,lon), equirectangular at mean lat."""
    ref = math.radians((a[0] + b[0]) / 2)
    dy = (a[0] - b[0]) * g.MILES_PER_DEG_LAT
    dx = (a[1] - b[1]) * g.MILES_PER_DEG_LAT * math.cos(ref)
    return math.hypot(dx, dy)


def check_map(key):
    fails = []
    cities = [dict(c) for c in g.CITIES[key]]
    g.project(cities)
    by_name = {c["n"]: c for c in cities}
    exp = EXPECTED[key]

    # 1. tier labels match the locked spec, and excluded cities are absent
    for tier in ("core", "greater", "outer"):
        got = {c["n"] for c in cities if c["t"] == tier}
        if got != exp[tier]:
            fails.append("[%s] %s tier mismatch: got %s expected %s"
                         % (key, tier, sorted(got), sorted(exp[tier])))
    for name in EXCLUDED:
        if name in by_name:
            fails.append("[%s] excluded city present: %s" % (key, name))
    caps = [c["n"] for c in cities if c.get("cap")]
    if caps:
        fails.append("[%s] capital present but capitals are retired: %s"
                     % (key, caps))

    # build the three buffered blobs
    blob = {t: g.buffered_blob(g.tier_points(cities, t))
            for t in ("core", "greater", "outer")}
    hull = {t: g.convex_hull(g.tier_points(cities, t))
            for t in ("core", "greater", "outer")}

    # 2. every city inside its own blob and every enclosing blob
    order = ["core", "greater", "outer"]
    for c in cities:
        own = c["t"]
        for t in order[g.TIER_IDX[own]:]:        # own tier and everything outside it
            if not point_in_poly((c["x"], c["y"]), blob[t]):
                fails.append("[%s] %s not inside %s blob" % (key, c["n"], t))

    # 3. nesting, buffered blobs and raw hulls
    if not poly_inside_poly(blob["core"], blob["greater"]):
        fails.append("[%s] core blob not inside greater blob" % key)
    if not poly_inside_poly(blob["greater"], blob["outer"]):
        fails.append("[%s] greater blob not inside outer blob" % key)
    if not poly_inside_poly(hull["core"], hull["greater"]):
        fails.append("[%s] core hull not inside greater hull" % key)
    if not poly_inside_poly(hull["greater"], hull["outer"]):
        fails.append("[%s] greater hull not inside outer hull" % key)

    # 4. no stranded dot (inside outermost)
    for c in cities:
        if not point_in_poly((c["x"], c["y"]), blob["outer"]):
            fails.append("[%s] STRANDED: %s outside outer blob" % (key, c["n"]))

    # 5. real core diameter in miles
    core = [c for c in cities if c["t"] == "core"]
    dmax = 0.0
    pair = ("", "")
    for i in range(len(core)):
        for j in range(i + 1, len(core)):
            d = miles((core[i]["lat"], core[i]["lon"]),
                      (core[j]["lat"], core[j]["lon"]))
            if d > dmax:
                dmax, pair = d, (core[i]["n"], core[j]["n"])
    return fails, dmax, pair


def main():
    all_fails = []
    print("=" * 64)
    print("Photon Mountain / Silicon Valley  -  independent geometry check")
    print("=" * 64)
    for key in ("SV", "PM"):
        fails, dmax, pair = check_map(key)
        all_fails += fails
        meta = g.MAP_META[key]
        print("\n%s (%s)" % (meta["title"], key))
        print("  core diameter: %.1f miles  (%s to %s)" % (dmax, pair[0], pair[1]))
        if fails:
            for f in fails:
                print("  FAIL " + f)
        else:
            print("  all geometry checks passed")
    print("\n" + "-" * 64)
    if all_fails:
        print("RESULT: FAIL  (%d issue(s))" % len(all_fails))
        raise SystemExit(1)
    print("RESULT: PASS  -  every city banded correctly, blobs nest, no strays")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
