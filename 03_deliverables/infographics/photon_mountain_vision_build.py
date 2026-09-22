#!/usr/bin/env python3
"""Build the Photon Mountain vision infographic (one self-contained HTML page).

Light build. The page runs on Snowfield, because the corridor's subject is light
and the field should be light too. Every accent uses the on-light variant from
the palette table in 01_doctrine/brand_identity.md, so nothing here relies on a
dark ground to reach contrast. Measured against Snowfield (#F6F7FB):

    Summit Night   16.04   body text
    Granite         6.36   secondary text, rules
    Violet Deep     6.78   accent text
    Alpenglow Deep  4.89   accent text
    Laser Violet    4.07   large text and graphics only
    Violet Bright   3.19   graphics only
    Alpenglow       2.90   graphics only, never text at any size

Every graphic is drawn from project data, never hand-placed:
  - the corridor map, from 03_deliverables/maps/photon_mountain_corridor.geojson
  - the true-scale core comparison, from the CITIES table and the locked K px/mile
    method in 03_deliverables/infographics/photon_mountain_map_README.md
  - the unit-chart legend, from the same 53-marker roster
  - the timeline, from the dated milestones in 02_substance and MAP_NOTES.md

Standard library only.

Usage, from this folder:
  python3 photon_mountain_vision_build.py            # build
  python3 photon_mountain_vision_build.py --check    # build, then audit the result

--check re-parses the generated page and reports what a silent layout bug looks
like: a label pushed past its viewBox edge, two labels overlapping, an accent
color used as text where it cannot carry text, or a hex that traces to no token.
None of those raise on their own, so the check is the only thing that catches them.
"""

import json
import math
import os
import sys

# Brand values come from 04_tools/brand_tokens.py, never from a hex typed here,
# so this script obeys the same rule as the other two builds in this folder.
# brand_tokens self-tests against 01_doctrine/brand_identity.md.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "04_tools"))
import brand_tokens as bt  # noqa: E402

SUMMIT_NIGHT = bt.COLOR["summit_night"]
SNOWFIELD = bt.COLOR["snowfield"]
WHITE = bt.COLOR["white"]
GRANITE = bt.COLOR["granite"]
ALPENGLOW = bt.COLOR["alpenglow"]
ALPENGLOW_DEEP = bt.COLOR["alpenglow_deep"]
LASER_VIOLET = bt.COLOR["laser_violet"]
VIOLET_BRIGHT = bt.COLOR["violet_bright"]
VIOLET_DEEP = bt.COLOR["violet_deep"]
DAWN_TINT = bt.COLOR["dawn_tint"]

# Derived neutrals, mixed from palette colors the way brand_tokens.py mixes them.
HAIRLINE = bt.mix(GRANITE, WHITE, 0.78)
RULE_SOFT = bt.mix(GRANITE, WHITE, 0.88)

FONT_DISPLAY, FONT_BODY, FONT_MONO = bt.FONT_DISPLAY, bt.FONT_BODY, bt.FONT_MONO

# Semantic roles for this build.
GROUND = SNOWFIELD
PAPER = WHITE
INK = SUMMIT_NIGHT
MUTED = GRANITE
ACCENT_TEXT = ALPENGLOW_DEEP
ACCENT2_TEXT = VIOLET_DEEP
ACCENT_GFX = ALPENGLOW

# Marker styling on a white map panel: fill, stroke, radius, stroke width.
# Fills are the on-light variants; the hairline stroke is paper, so dots stay
# separate where they cluster instead of merging into one blob.
CAT = {
    "Fabrication Facility": (ALPENGLOW, SUMMIT_NIGHT, 10.0, 2.6),
    "National Lab":         (ALPENGLOW_DEEP, WHITE, 6.5, 1.3),
    "University Lab":       (LASER_VIOLET, WHITE, 6.5, 1.3),
    "Innovation Campus":    (VIOLET_DEEP, WHITE, 6.0, 1.3),
    "University Campus":    (VIOLET_BRIGHT, SUMMIT_NIGHT, 6.0, 1.3),
    "Transit Station":      (GRANITE, WHITE, 4.6, 1.2),
    "Government Hall":      (SUMMIT_NIGHT, WHITE, 5.0, 1.2),
}
DRAW_ORDER = ["Transit Station", "Government Hall", "University Campus",
              "Innovation Campus", "University Lab", "National Lab",
              "Fabrication Facility"]
LEGEND_ORDER = ["Fabrication Facility", "National Lab", "University Lab",
                "Innovation Campus", "University Campus", "Transit Station",
                "Government Hall"]

# ------------------------------------------------------------ geo helpers --

def merc(lon, lat):
    return lon, math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


def simplify(pts, tol):
    sys.setrecursionlimit(20000)

    def d2(p, a, b):
        px, py = p[0] - a[0], p[1] - a[1]
        bx, by = b[0] - a[0], b[1] - a[1]
        L = bx * bx + by * by
        if L == 0:
            return px * px + py * py
        t = max(0.0, min(1.0, (px * bx + py * by) / L))
        dx, dy = px - t * bx, py - t * by
        return dx * dx + dy * dy

    def dp(ps):
        if len(ps) < 3:
            return ps
        dm, idx = 0.0, 0
        for i in range(1, len(ps) - 1):
            v = d2(ps[i], ps[0], ps[-1])
            if v > dm:
                dm, idx = v, i
        if dm > tol * tol:
            return dp(ps[:idx + 1])[:-1] + dp(ps[idx:])
        return [ps[0], ps[-1]]

    return dp(pts)


def hull(points):
    """Andrew monotone chain convex hull."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def buffered_hull(points, r, n=24):
    """Minkowski sum of the hull with a disk, per the locked comparison method."""
    ring = []
    for x, y in points:
        for k in range(n):
            a = 2 * math.pi * k / n
            ring.append((round(x + r * math.cos(a), 3), round(y + r * math.sin(a), 3)))
    return hull(ring)


def poly_path(pts, close=True):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return d + (" Z" if close else "")


# ----------------------------------------------------------- corridor map --

def corridor_map(geojson_path):
    data = json.load(open(geojson_path))
    ring = None
    sites = []
    for f in data["features"]:
        if f["geometry"]["type"] == "Polygon":
            ring = f["geometry"]["coordinates"][0]
        else:
            p = f["properties"]
            sites.append((p["name"], p["category"], f["geometry"]["coordinates"]))

    lons = [c[0] for c in ring] + [s[2][0] for s in sites]
    lats = [c[1] for c in ring] + [s[2][1] for s in sites]
    x0, y0 = merc(min(lons), min(lats))
    x1, y1 = merc(max(lons), max(lats))
    W, PAD = 1000.0, 50.0
    k = (W - 2 * PAD) / (x1 - x0)
    H = (y1 - y0) * k + 2 * PAD

    def proj(lon, lat):
        x, y = merc(lon, lat)
        return round((x - x0) * k + PAD, 1), round(H - PAD - (y - y0) * k, 1)

    rp = simplify([proj(*c) for c in ring], 1.1)
    if rp[0] != rp[-1]:
        rp.append(rp[0])

    counts = {}
    for _, cat, _ in sites:
        counts[cat] = counts.get(cat, 0) + 1

    o = [f'<svg class="corridor" viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
         f'aria-label="Map of the Photon Mountain corridor from Boulder to Denver with '
         f'{len(sites)} mapped sites in seven categories">']
    # a warm dawn wash inside the line, the light the corridor is named for
    o.append('<defs><radialGradient id="dawn" cx="50%" cy="50%" r="50%">'
             f'<stop offset="0%" stop-color="{ALPENGLOW}" stop-opacity="0.13"/>'
             f'<stop offset="100%" stop-color="{ALPENGLOW}" stop-opacity="0"/>'
             '</radialGradient></defs>')
    xs = [p[0] for p in rp]; ys = [p[1] for p in rp]
    o.append(f'<ellipse cx="{sum(xs)/len(xs):.0f}" cy="{sum(ys)/len(ys):.0f}" '
             f'rx="{(max(xs)-min(xs))*0.85:.0f}" ry="{(max(ys)-min(ys))*0.62:.0f}" fill="url(#dawn)"/>')
    o.append(f'<path d="{poly_path(rp)}" fill="rgba(86,54,214,0.05)" '
             f'stroke="{VIOLET_DEEP}" stroke-width="2.2" stroke-linejoin="round"/>')

    cities = [("BOULDER", 40.0150, -105.2705, "middle", 0, -26),
              ("GOLDEN", 39.7555, -105.2211, "end", -16, 4),
              ("ARVADA", 39.8028, -105.0875, "start", 16, 4),
              ("DENVER", 39.7392, -104.9903, "middle", -12, 36)]
    for nm, lat, lon, anchor, dx, dy in cities:
        x, y = proj(lon, lat)
        o.append(f'<text class="city" x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{anchor}">{nm}</text>')

    groups = {}
    for nm, cat, c in sites:
        groups.setdefault(cat, []).append((nm, c))
    for cat in DRAW_ORDER:
        fill, stroke, r, sw = CAT[cat]
        o.append(f'<g fill="{fill}" stroke="{stroke}" stroke-width="{sw}">')
        for nm, c in groups[cat]:
            x, y = proj(c[0], c[1])
            safe = nm.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
            o.append(f'<circle class="site" cx="{x}" cy="{y}" r="{r}" tabindex="0" '
                     f'role="button" data-name="{safe}" data-cat="{cat}">'
                     f'<title>{safe}</title></circle>')
        o.append("</g>")

    mi = 5.0
    _, ya = proj(-105.1, 39.75)
    _, yb = proj(-105.1, 39.75 + mi / 69.0)
    px = abs(ya - yb)
    bx, by = W - PAD - px, H - 26
    o.append(f'<g stroke="{MUTED}" stroke-width="2" fill="none">'
             f'<path d="M{bx:.0f},{by} L{bx+px:.0f},{by}"/>'
             f'<path d="M{bx:.0f},{by-6} L{bx:.0f},{by+6}"/>'
             f'<path d="M{bx+px:.0f},{by-6} L{bx+px:.0f},{by+6}"/></g>')
    o.append(f'<text class="scale" x="{bx+px/2:.0f}" y="{by-12}" text-anchor="middle">5 MILES</text>')
    o.append("</svg>")
    return "\n      ".join(o), counts, len(sites)


# -------------------------------------------------- true-scale comparison --

SV = [("Palo Alto", 37.4419, -122.1430, 68572), ("Mountain View", 37.3861, -122.0839, 82376),
      ("Sunnyvale", 37.3688, -122.0363, 155805), ("Cupertino", 37.3230, -122.0322, 60381),
      ("Santa Clara", 37.3541, -121.9552, 127647), ("San Jose", 37.3382, -121.8863, 1013240),
      ("Menlo Park", 37.4530, -122.1817, 33780)]
PM = [("Boulder", 40.0150, -105.2705, 108250), ("Golden", 39.7555, -105.2211, 20399),
      ("Arvada", 39.8028, -105.0875, 124402), ("Denver", 39.7392, -104.9903, 715522)]
K = 13.0          # px per mile, identical on both panels
MPD = 69.0
POP_MAX = 1013240
R_MAX, R_MIN = 17.0, 5.0


def comparison():
    def place(cities):
        lats = [c[1] for c in cities]
        lons = [c[2] for c in cities]
        ref = sum(lats) / len(lats)
        mpdlon = MPD * math.cos(math.radians(ref))
        return [{"n": n, "pop": pop,
                 "x": (lo - min(lons)) * mpdlon * K,
                 "y": (max(lats) - la) * MPD * K} for n, la, lo, pop in cities]

    a, b = place(SV), place(PM)
    aw = max(c["x"] for c in a); ah = max(c["y"] for c in a)
    bw = max(c["x"] for c in b); bh = max(c["y"] for c in b)
    PAD, GAP, TOP = 96.0, 150.0, 62.0
    H = TOP + max(ah, bh) + 108
    ay = TOP + (max(ah, bh) - ah) / 2
    by = TOP + (max(ah, bh) - bh) / 2
    for c in a:
        c["x"] += PAD; c["y"] += ay
    bx0 = PAD + aw + GAP
    for c in b:
        c["x"] += bx0; c["y"] += by
    W = bx0 + bw + PAD

    def radius(p):
        return max(R_MIN, R_MAX * math.sqrt(p / POP_MAX))

    body, extents = [], []

    def text(cls, x, y, anchor, s, extra="", w_per=7.35):
        w = len(s) * w_per
        lo, hi = ((x - w, x) if anchor == "end" else
                  (x, x + w) if anchor == "start" else (x - w / 2, x + w / 2))
        extents.append((lo, hi))
        body.append(f'<text class="{cls}" x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}"{extra}>{s}</text>')

    for group, is_pm, title, dia in ((a, False, "SILICON VALLEY", "18.0 mi"),
                                     (b, True, "PHOTON MOUNTAIN", "24.1 mi")):
        cx = (bx0 + bw / 2) if is_pm else (PAD + aw / 2)
        line = VIOLET_DEEP if is_pm else GRANITE
        fill = "rgba(86,54,214,0.13)" if is_pm else "rgba(84,91,107,0.12)"
        dotfill = VIOLET_DEEP if is_pm else SUMMIT_NIGHT
        pts = [(c["x"], c["y"]) for c in group]
        hp = buffered_hull(pts, 1.0 * K)
        body.append(f'<path d="{poly_path(hp)}" fill="{fill}" stroke="{line}" stroke-width="1.6"/>')
        extents.append((min(p[0] for p in hp), max(p[0] for p in hp)))
        text("panel-title", cx, 32, "middle", title, w_per=8.6)
        text("panel-dia", cx, H - 62, "middle", dia,
             f' fill="{ACCENT_TEXT if is_pm else MUTED}"', w_per=17.0)
        text("panel-sub", cx, H - 42, "middle", "CORE DIAMETER", w_per=7.6)
        for c in group:
            body.append(f'<circle cx="{c["x"]:.1f}" cy="{c["y"]:.1f}" r="{radius(c["pop"]):.1f}" '
                        f'fill="{dotfill}" stroke="{WHITE}" stroke-width="1.2"/>')
        # Three Silicon Valley cities sit closer together than one line of label
        # at this scale, so their pins get a hand-set vertical nudge. Every value
        # here is guarded by --check, which fails if a nudge stops working.
        PIN_DY = {"Menlo Park": -10.0, "Palo Alto": 6.0, "Santa Clara": -10.0}
        for c in group:
            side = "start" if c["x"] >= cx else "end"
            dx = 10 + radius(c["pop"]) if side == "start" else -(10 + radius(c["pop"]))
            text("pin", c["x"] + dx, c["y"] + 4 + PIN_DY.get(c["n"], 0.0), side, c["n"])

    sb = 10 * K
    body.append(f'<g stroke="{MUTED}" stroke-width="2" fill="none">'
                f'<path d="M{PAD:.0f},{H-18:.0f} L{PAD+sb:.0f},{H-18:.0f}"/>'
                f'<path d="M{PAD:.0f},{H-24:.0f} L{PAD:.0f},{H-12:.0f}"/>'
                f'<path d="M{PAD+sb:.0f},{H-24:.0f} L{PAD+sb:.0f},{H-12:.0f}"/></g>')
    text("scale", PAD + sb + 12, H - 14, "start", "10 MILES, SAME SCALE ON BOTH", w_per=7.4)

    lo = min(e[0] for e in extents); hi = max(e[1] for e in extents)
    x_min = min(0.0, lo - 8); vw = max(W, hi + 8) - x_min
    o = [f'<svg class="compare" viewBox="{x_min:.0f} 0 {vw:.0f} {H:.0f}" role="img" '
         'aria-label="The Silicon Valley core and the Photon Mountain core drawn at the same scale, '
         '18.0 miles and 24.1 miles across, city dots sized by population">']
    o.extend(body)
    o.append("</svg>")
    return "\n      ".join(o)


# ----------------------------------------------------------------- timeline --

MILESTONES = [
    (2023.37, "RAIL opens", "NLR wet labs", "now"),
    (2024.26, "Beck Venture Center", "Mines incubator", "now"),
    (2024.54, "$40.5M Tech Hubs award", "per the EDA", "now"),
    (2024.96, "Flatirons Control Center", "per Mortenson", "now"),
    (2025.04, "Quantum Incubator opens", "Boulder", "now"),
    (2025.62, "Quantum Commons opens", "first building", "now"),
    (2025.92, "NREL becomes NLR", "per energy.gov", "now"),
    (2026.45, "Phoenix laser", "start announced by Xcimer", "soon"),
    (2026.95, "Photonic-IC fab, phase one", "per Elevate Quantum", "soon"),
    (2027.60, "EMAPS completes", "$224M, NLR", "horizon"),
    (2028.80, "National Quantum Nanofab", "$20M NSF award", "horizon"),
]
FRAME_COLOR = {"now": ALPENGLOW_DEEP, "soon": VIOLET_DEEP, "horizon": GRANITE}


def timeline():
    """Milestones on a real time axis, alternating above and below, lane-packed
    from measured label widths so nothing overlaps."""
    x0, x1 = 2023.0, 2029.0
    W = 1040.0
    L, R = 52.0, 30.0
    LAB_W, SUB_W = 7.7, 6.9
    LANE, STEP0 = 44.0, 44.0

    def px(y):
        return L + (y - x0) / (x1 - x0) * (W - L - R)

    placed, up = [], True
    for yr, label, sub, frame in MILESTONES:
        x = px(yr)
        w = max(len(label) * LAB_W, len(sub) * SUB_W)
        tx = min(max(x, L + w / 2 + 4), W - R - w / 2 - 4)
        lo, hi = tx - w / 2 - 10, tx + w / 2 + 10
        side = "up" if up else "dn"
        lane = 0
        while any(s == side and l == lane and not (hi < plo or lo > phi)
                  for s, l, plo, phi, *_ in placed):
            lane += 1
        placed.append((side, lane, lo, hi, x, tx, label, sub, frame))
        up = not up

    up_lanes = max([p[1] for p in placed if p[0] == "up"], default=0) + 1
    dn_lanes = max([p[1] for p in placed if p[0] == "dn"], default=0) + 1
    AX = 30 + STEP0 + (up_lanes - 1) * LANE
    H = AX + 34 + STEP0 + (dn_lanes - 1) * LANE + 26

    o = [f'<svg class="timeline" viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
         'aria-label="Timeline of corridor milestones from 2023 to 2029, each dot colored by '
         'whether it is operating, opening in 2026, or on the horizon">']
    o.append(f'<rect x="{px(2026):.0f}" y="8" width="{px(2027)-px(2026):.0f}" height="{H-34:.0f}" '
             f'fill="{DAWN_TINT}"/>')
    o.append(f'<path d="M{L},{AX:.0f} L{W-R},{AX:.0f}" stroke="{MUTED}" stroke-width="1.5"/>')
    for yr in range(2023, 2030):
        x = px(yr)
        o.append(f'<path d="M{x:.0f},{AX-5:.0f} L{x:.0f},{AX+5:.0f}" stroke="{MUTED}" stroke-width="1.5"/>')
        o.append(f'<text class="yr" x="{x:.0f}" y="{AX+24:.0f}" text-anchor="middle">{yr}</text>')

    for side, lane, lo, hi, x, tx, label, sub, frame in placed:
        c = FRAME_COLOR[frame]
        step = STEP0 + lane * LANE
        if side == "up":
            ylab, ysub, tip = AX - step - 14, AX - step + 2, AX - step - 24
        else:
            ylab, ysub, tip = AX + step + 28, AX + step + 44, AX + step + 18
        o.append(f'<path d="M{x:.0f},{AX:.0f} L{x:.0f},{tip:.0f}" stroke="{c}" '
                 f'stroke-width="1.2" stroke-opacity="0.45"/>')
        if abs(tx - x) > 1:
            o.append(f'<path d="M{x:.0f},{tip:.0f} L{tx:.0f},{tip:.0f}" stroke="{c}" '
                     f'stroke-width="1.2" stroke-opacity="0.45"/>')
        o.append(f'<circle cx="{x:.0f}" cy="{AX:.0f}" r="5.5" fill="{c}" stroke="{WHITE}" stroke-width="2"/>')
        o.append(f'<text class="ms" x="{tx:.0f}" y="{ylab:.0f}" text-anchor="middle" fill="{c}">{label}</text>')
        o.append(f'<text class="ms-sub" x="{tx:.0f}" y="{ysub:.0f}" text-anchor="middle">{sub}</text>')
    o.append("</svg>")
    return "\n      ".join(o)


# ---------------------------------------------------------------- page bits --

ICONS = {
    "chip": ('<rect x="14" y="14" width="28" height="28" rx="4"/>'
             '<rect x="23" y="23" width="10" height="10" rx="1.5"/>'
             '<path d="M23 8v6M33 8v6M23 42v6M33 42v6M8 23h6M8 33h6M42 23h6M42 33h6"/>'),
    "fiber": ('<path d="M6 42c10 0 12-16 22-16s12 10 22 10"/>'
              '<circle cx="50" cy="36" r="4.5"/>'
              '<path d="M44 20l5 5M56 20l-5 5M50 14v7"/>'),
    "solar": ('<circle cx="28" cy="20" r="8"/>'
              '<path d="M28 4v5M28 31v5M12 20h5M39 20h5M17 9l3 3M39 9l-3 3"/>'
              '<path d="M10 50h36l-6-14H16z"/><path d="M22 36l-3 14M34 36l3 14M14 43h28"/>'),
    "fusion": ('<circle cx="28" cy="28" r="6"/>'
               '<path d="M6 28h12M38 28h12M28 6v12M28 38v12"/>'
               '<path d="M12 12l7 7M44 12l-7 7M12 44l7-7M44 44l-7-7"/>'),
}


def icon(name):
    return (f'<svg class="ico" viewBox="0 0 56 56" aria-hidden="true">'
            f'<g fill="none" stroke="{ACCENT_TEXT}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g></svg>')


RIDGE = ("M0 210 L120 138 L188 168 L286 96 L372 150 L452 112 L548 172 L640 120 "
         "L724 164 L812 108 L900 158 L986 122 L1070 170 L1140 140 L1200 178")


def ridge():
    """Dawn on the Front Range: the sun up behind a ridge drawn as a line, so the
    masthead stays a light field instead of a dark mass."""
    return (f'<svg class="ridge" viewBox="0 0 1200 220" aria-hidden="true" preserveAspectRatio="none">'
            f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{DAWN_TINT}" stop-opacity="0"/>'
            f'<stop offset="100%" stop-color="{DAWN_TINT}" stop-opacity="1"/></linearGradient></defs>'
            f'<circle cx="905" cy="152" r="92" fill="{ALPENGLOW}" fill-opacity="0.16"/>'
            f'<path d="{RIDGE} L1200 220 L0 220 Z" fill="url(#sky)"/>'
            f'<path d="{RIDGE}" fill="none" stroke="{VIOLET_DEEP}" stroke-opacity="0.45" stroke-width="1.6"/>'
            f'</svg>')


def unit_row(cat, n):
    fill, stroke, _, _ = CAT[cat]
    ring = SUMMIT_NIGHT if fill in (ALPENGLOW, VIOLET_BRIGHT) else fill
    dots = "".join(f'<span class="u" style="background:{fill};box-shadow:0 0 0 1px {ring}"></span>'
                   for _ in range(n))
    return (f'<li><span class="u-name">{cat}</span>'
            f'<span class="u-dots">{dots}</span>'
            f'<span class="u-n">{n}</span></li>')


# ----------------------------------------------------------------- the check --

# Approximate advance width per character, as a fraction of font size, plus the
# tracking each class carries. Used to bound a label without rendering it.
_METRICS = {
    "city": (22, 0.60, 0.18), "scale": (15, 0.60, 0.12),
    "panel-title": (14, 0.60, 0.14), "panel-dia": (30, 0.58, -0.02),
    "panel-sub": (10, 0.60, 0.16), "pin": (12, 0.60, 0.0),
    "yr": (14, 0.60, 0.08), "ms": (14, 0.545, 0.0), "ms-sub": (11, 0.60, 0.0),
}
_TOKENS = {SUMMIT_NIGHT, SNOWFIELD, WHITE, GRANITE, ALPENGLOW, ALPENGLOW_DEEP,
           LASER_VIOLET, VIOLET_BRIGHT, VIOLET_DEEP, DAWN_TINT, HAIRLINE, RULE_SOFT}
# Accents that cannot carry text on Snowfield: Alpenglow 2.90, Violet Bright 3.19.
_NEVER_TEXT = {ALPENGLOW, VIOLET_BRIGHT}


def _box(x, w, anchor):
    if anchor == "end":
        return x - w, x
    if anchor == "start":
        return x, x + w
    return x - w / 2, x + w / 2


def check(path):
    import re
    s = open(path).read()
    fails = []

    for m in re.finditer(r'<svg class="([\w-]+)"[^>]*viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', s):
        cls = m.group(1)
        x0, y0, w, h = (float(m.group(i)) for i in range(2, 6))
        seg = s[m.end():s.index("</svg>", m.end())]
        boxes = []
        for t in re.finditer(r'<text class="([\w-]+)" x="([-\d.]+)" y="([-\d.]+)" text-anchor="(\w+)"[^>]*>([^<]*)</text>', seg):
            c, x, y, anchor, txt = t.group(1), float(t.group(2)), float(t.group(3)), t.group(4), t.group(5)
            fs, adv, ls = _METRICS.get(c, (12, 0.6, 0.0))
            lo, hi = _box(x, len(txt) * (fs * adv + fs * ls), anchor)
            if lo < x0 - 1 or hi > x0 + w + 1 or y > y0 + h:
                fails.append(f"{cls}: label {txt!r} falls outside the viewBox")
            boxes.append((lo, hi, y - fs, y + fs * 0.3, txt, c))
        for i, a in enumerate(boxes):
            for b in boxes[i + 1:]:
                if a[5] != b[5]:
                    continue
                if not (a[1] < b[0] or a[0] > b[1] or a[3] < b[2] or a[2] > b[3]):
                    fails.append(f"{cls}: labels {a[4]!r} and {b[4]!r} overlap")

    for hexv in set(re.findall(r'#[0-9A-Fa-f]{6}', s)):
        if hexv.upper() not in {t.upper() for t in _TOKENS}:
            fails.append(f"hex {hexv} traces to no palette token")

    for bad in _NEVER_TEXT:
        if re.search(r'<text[^>]*fill="%s"' % bad, s) or re.search(r'fill:\s*%s' % bad, s):
            fails.append(f"{bad} is set as text; on Snowfield it cannot carry text at any size")

    for line in fails:
        print("  FAIL", line)
    print("check: PASS" if not fails else f"check: {len(fails)} FAIL")
    return 0 if not fails else 1


def build(root, out):
    cmap, counts, total = corridor_map(
        f"{root}/03_deliverables/maps/photon_mountain_corridor.geojson")
    legend = "\n        ".join(unit_row(c, counts[c]) for c in LEGEND_ORDER)

    html = f"""<title>Photon Mountain</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={FONT_DISPLAY.replace(" ", "+")}:wght@500;700&family={FONT_BODY.replace(" ", "+")}:wght@400;500;600&family={FONT_MONO.replace(" ", "+")}:wght@400;700&display=swap">
<style>
  /* Locked Photon Mountain palette, on-light variants.
     Canonical: 01_doctrine/brand_identity.md. Single light theme on purpose:
     the corridor's subject is light, so the field is light. */
  :root {{
    --summit-night: {SUMMIT_NIGHT};
    --snowfield: {SNOWFIELD};
    --paper: {WHITE};
    --granite: {GRANITE};
    --alpenglow: {ALPENGLOW};
    --alpenglow-deep: {ALPENGLOW_DEEP};
    --laser-violet: {LASER_VIOLET};
    --violet-bright: {VIOLET_BRIGHT};
    --violet-deep: {VIOLET_DEEP};
    --dawn-tint: {DAWN_TINT};
    --hairline: {HAIRLINE};
    --rule-soft: {RULE_SOFT};
    --display: "{FONT_DISPLAY}", "Helvetica Neue", Arial, sans-serif;
    --body: "{FONT_BODY}", "Helvetica Neue", Arial, sans-serif;
    --mono: "{FONT_MONO}", ui-monospace, Menlo, monospace;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: var(--snowfield); color: var(--summit-night);
    font-family: var(--body); font-size: 16px; line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }}
  .page {{ width: 100%; max-width: 1140px; margin: 0 auto; padding-inline: 20px; }}
  a {{ color: var(--violet-deep); }}
  a:focus-visible, .site:focus-visible {{ outline: 2px solid var(--alpenglow-deep); outline-offset: 3px; }}
  h2 {{ margin: 0; font-family: var(--display); font-weight: 700; }}

  .band {{ padding-block: 40px; border-top: 1px solid var(--hairline); }}
  .band:first-of-type {{ border-top: 0; }}
  .kicker {{
    font-family: var(--mono); font-size: 11px; letter-spacing: 0.2em;
    text-transform: uppercase; color: var(--granite); margin: 0 0 6px;
  }}
  .band > h2 {{ font-size: clamp(20px, 3vw, 26px); letter-spacing: -0.015em; margin-bottom: 22px; }}

  /* masthead */
  .hero {{ position: relative; padding-block: 52px 34px; overflow: hidden; }}
  .ridge {{
    position: absolute; left: -20px; right: -20px; bottom: 0; width: calc(100% + 40px);
    height: 216px; pointer-events: none;
  }}
  .hero-in {{ position: relative; }}
  .lockup {{ display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }}
  .lockup svg {{ width: 50px; height: 40px; flex: none; }}
  .lockup .nm {{
    font-family: var(--display); font-weight: 500; font-size: clamp(26px, 5vw, 38px);
    letter-spacing: -0.02em; line-height: 1;
  }}
  .tag {{
    font-family: var(--display); font-weight: 700; margin: 0;
    font-size: clamp(46px, 11vw, 112px); line-height: 0.95; letter-spacing: -0.04em;
    color: var(--alpenglow-deep);
  }}
  .tag span {{ color: var(--summit-night); }}
  .place {{
    font-family: var(--mono); font-size: 12px; letter-spacing: 0.16em;
    text-transform: uppercase; color: var(--granite); margin: 16px 0 0;
  }}

  /* big numbers */
  .figs {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1px;
           background: var(--hairline); border: 1px solid var(--hairline); }}
  .fig {{ background: var(--paper); padding: 20px 18px 16px; }}
  .fig .v {{
    font-family: var(--display); font-weight: 700; font-size: clamp(32px, 5vw, 46px);
    line-height: 1; letter-spacing: -0.03em; color: var(--alpenglow-deep);
    font-variant-numeric: tabular-nums;
  }}
  .fig .l {{ font-size: 14px; margin-top: 8px; }}
  .fig .s {{ font-family: var(--mono); font-size: 10.5px; color: var(--granite); margin-top: 6px;
             letter-spacing: 0.06em; text-transform: uppercase; }}

  /* map */
  .map-grid {{ display: grid; grid-template-columns: minmax(0,1fr) 300px; gap: 28px; align-items: start; }}
  .map-box {{ margin: 0; padding: 14px 14px 0; border: 1px solid var(--hairline); background: var(--paper); }}
  .corridor {{ display: block; width: 100%; height: clamp(440px, 72vh, 860px); }}
  .corridor .city {{ font-family: var(--mono); font-size: 22px; letter-spacing: 0.18em; fill: {GRANITE}; }}
  .corridor .scale {{ font-family: var(--mono); font-size: 15px; letter-spacing: 0.12em; fill: {GRANITE}; }}
  .corridor .site {{ cursor: pointer; }}
  .corridor .site:hover, .corridor .site.on {{ stroke: {SUMMIT_NIGHT}; stroke-width: 3; }}
  .cap {{
    font-family: var(--mono); font-size: 11.5px; color: var(--granite);
    border-top: 1px solid var(--rule-soft); margin-top: 10px; padding: 10px 2px 12px;
    min-height: 3.4em;
  }}
  .cap b {{ display: block; font-family: var(--body); font-size: 14px; color: var(--summit-night); }}

  .units {{ list-style: none; margin: 0 0 18px; padding: 0; display: flex; flex-direction: column; gap: 12px; }}
  .units li {{ display: grid; grid-template-columns: 1fr auto; gap: 4px 10px; }}
  .u-name {{ font-size: 13px; font-weight: 500; }}
  .u-n {{ font-family: var(--mono); font-size: 13px; color: var(--granite); font-variant-numeric: tabular-nums; }}
  .u-dots {{ grid-column: 1 / -1; display: flex; flex-wrap: wrap; gap: 5px; }}
  .u {{ width: 9px; height: 9px; border-radius: 50%; display: block; }}
  .go {{
    display: inline-block; font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--alpenglow-deep); border: 1px solid var(--alpenglow-deep);
    padding: 10px 14px; text-decoration: none;
  }}
  .go:hover {{ background: var(--alpenglow-deep); color: var(--paper); }}

  /* comparison + timeline */
  .compare, .timeline {{ display: block; width: 100%; height: auto; max-width: 100%; }}
  .compare .panel-title {{ font-family: var(--mono); font-size: 14px; letter-spacing: 0.14em; fill: {GRANITE}; }}
  .compare .panel-dia {{ font-family: var(--display); font-weight: 700; font-size: 30px; letter-spacing: -0.02em; }}
  .compare .panel-sub {{ font-family: var(--mono); font-size: 10px; letter-spacing: 0.16em; fill: {GRANITE}; }}
  .compare .pin {{ font-family: var(--mono); font-size: 12px; fill: {GRANITE}; }}
  .compare .scale {{ font-family: var(--mono); font-size: 11px; letter-spacing: 0.1em; fill: {GRANITE}; }}
  .timeline .yr {{ font-family: var(--mono); font-size: 14px; letter-spacing: 0.08em; fill: {GRANITE}; }}
  .timeline .ms {{ font-family: var(--body); font-weight: 600; font-size: 14px; }}
  .timeline .ms-sub {{ font-family: var(--mono); font-size: 11px; fill: {GRANITE}; }}
  .scroller {{ overflow-x: auto; }}
  .scroller > svg {{ min-width: 660px; }}

  .keys {{ display: flex; flex-wrap: wrap; gap: 18px; margin-top: 14px; }}
  .key {{ display: flex; align-items: center; gap: 8px; font-family: var(--mono);
          font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--granite); }}
  .key i {{ width: 10px; height: 10px; border-radius: 50%; display: block; }}

  /* pillars */
  .pills {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 26px; }}
  .ico {{ width: 52px; height: 52px; display: block; margin-bottom: 12px; }}
  .pill h3 {{ margin: 0 0 4px; font-family: var(--display); font-size: 17px; font-weight: 700; }}
  .pill p {{ margin: 0; font-size: 13.5px; color: var(--granite); }}

  /* footer */
  .foot {{ padding-block: 34px 56px; border-top: 1px solid var(--hairline); }}
  .foot .guard {{ margin: 0; max-width: 60ch; font-size: 15px; color: var(--summit-night); }}
  .foot .src {{ font-family: var(--mono); font-size: 11px; line-height: 1.7; color: var(--granite); margin: 18px 0 0; }}
  .foot .src b {{ color: var(--summit-night); font-weight: 400; }}

  @media (max-width: 760px) {{
    .map-grid {{ grid-template-columns: 1fr; }}
    .corridor {{ height: clamp(420px, 78vh, 640px); }}
    .corridor .city {{ font-size: 28px; }}
  }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; transition: none !important; }} }}
</style>

<div class="page">

  <header class="hero">
    {ridge()}
    <div class="hero-in">
      <div class="lockup">
        <svg viewBox="0 0 200 160" role="img" aria-label="Photon Mountain Summit Sun mark">
          <circle cx="100" cy="100" r="40" fill="{ALPENGLOW}"></circle>
          <polygon points="100,90 150.8,150 49.2,150" fill="{SUMMIT_NIGHT}"></polygon>
        </svg>
        <div class="nm">Photon Mountain</div>
      </div>
      <p class="tag">Build<br><span>with</span> light.</p>
      <p class="place">Colorado Front Range &nbsp;/&nbsp; Boulder &middot; Golden &middot; Arvada &middot; Denver</p>
    </div>
  </header>

  <section class="band">
    <div class="figs">
      <div class="fig"><div class="v">{total}</div><div class="l">sites mapped in the corridor</div><div class="s">7 categories</div></div>
      <div class="fig"><div class="v">24.1</div><div class="l">miles across the core</div><div class="s">Boulder to Denver, measured</div></div>
      <div class="fig"><div class="v">~250</div><div class="l">photonics companies statewide</div><div class="s">on the order of 250, per CPIA</div></div>
      <div class="fig"><div class="v">~8,000</div><div class="l">photonics workers statewide</div><div class="s">roughly 8,000, per CPIA</div></div>
    </div>
  </section>

  <section class="band" aria-labelledby="m">
    <p class="kicker">The corridor</p>
    <h2 id="m">Where the light work is</h2>
    <div class="map-grid">
      <figure class="map-box">
      {cmap}
      <figcaption class="cap" id="cap" aria-live="polite">Select a dot to name it.</figcaption>
      </figure>
      <div>
        <ul class="units">
        {legend}
        </ul>
        <a class="go" href="https://felt.com/map/Photon-Mountain-the-corridor-built-with-light-OSOsyDNWTDe1acx9BDkkJ4D" target="_blank" rel="noopener">Open the live map</a>
      </div>
    </div>
  </section>

  <section class="band" aria-labelledby="c">
    <p class="kicker">True scale, one shared ruler</p>
    <h2 id="c">The core, against the other one</h2>
    <div class="scroller">
      {comparison()}
    </div>
  </section>

  <section class="band" aria-labelledby="t">
    <p class="kicker">Dated, sourced, one dot each</p>
    <h2 id="t">What opened, what opens, what is ahead</h2>
    <div class="scroller">
      {timeline()}
    </div>
    <div class="keys">
      <span class="key"><i style="background:{ALPENGLOW_DEEP}"></i>Operating</span>
      <span class="key"><i style="background:{VIOLET_DEEP}"></i>Opening 2026</span>
      <span class="key"><i style="background:{GRANITE}"></i>Horizon</span>
    </div>
  </section>

  <section class="band" aria-labelledby="p">
    <p class="kicker">Four proof areas</p>
    <h2 id="p">What the corridor builds</h2>
    <div class="pills">
      <div class="pill">{icon("chip")}<h3>Photonic chips</h3><p>Compute and interconnect on photons.</p></div>
      <div class="pill">{icon("fiber")}<h3>Sensors and fiber</h3><p>Measure the world with light.</p></div>
      <div class="pill">{icon("solar")}<h3>Solar</h3><p>Light as energy.</p></div>
      <div class="pill">{icon("fusion")}<h3>Laser fusion</h3><p>Light as ignition.</p></div>
    </div>
  </section>

  <section class="foot">
    <p class="kicker">Honesty guardrail</p>
    <p class="guard">Photonic compute is emerging, not shipping at scale. Boulder is the research anchor, not Denver.</p>
    <p class="src">
      <b>Sources.</b> Core diameters measured by the project's geometry verifier. CPIA is the Colorado Photonics Industry Association; the company and workforce counts are its figures. Tech Hubs award per the EDA. Fab phase one per Elevate Quantum and the Denver Gazette, 2025-08-29. Lab renaming per energy.gov. Control Center per Mortenson. EMAPS per the design-build team's topping-out release. Nanofab award per CU Boulder. Corridor claims verified 2026-07-06; re-verify before external use.<br>
      <b>Map data.</b> Boundary and marker coordinates derived from OpenStreetMap. &copy; OpenStreetMap contributors, ODbL 1.0. Boundary drawn simplified.<br>
      <b>Status.</b> Internal draft. Nothing external-facing ships without Paul's sign-off.
    </p>
  </section>

</div>

<script>
  (function () {{
    var cap = document.getElementById('cap');
    var rest = cap.innerHTML, on = null;
    function show(el) {{
      if (on) on.classList.remove('on');
      on = el; el.classList.add('on');
      cap.innerHTML = '<b></b><span></span>';
      cap.querySelector('b').textContent = el.getAttribute('data-name');
      cap.querySelector('span').textContent = el.getAttribute('data-cat');
    }}
    function clear() {{ if (on) {{ on.classList.remove('on'); on = null; }} cap.innerHTML = rest; }}
    document.querySelectorAll('.corridor .site').forEach(function (el) {{
      el.addEventListener('click', function () {{ show(el); }});
      el.addEventListener('mouseenter', function () {{ show(el); }});
      el.addEventListener('focus', function () {{ show(el); }});
      el.addEventListener('keydown', function (e) {{ if (e.key === 'Escape') {{ clear(); el.blur(); }} }});
    }});
    var svg = document.querySelector('.corridor');
    if (svg) svg.addEventListener('mouseleave', function () {{
      var a = document.activeElement;
      if (!a || !a.classList || !a.classList.contains('site')) clear();
    }});
  }}());
</script>
"""
    open(out, "w").write(html)
    print("wrote", out, len(html), "bytes; sites:", total, counts)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--check"]
    root = args[0] if len(args) > 0 else REPO_ROOT
    out = args[1] if len(args) > 1 else "photon_mountain_vision.html"
    build(root, out)
    if "--check" in sys.argv:
        sys.exit(check(out))
