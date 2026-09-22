#!/usr/bin/env python3
"""
Photon Mountain vs Silicon Valley, true-scale region maps.
Photon Mountain identity (see 01_doctrine/brand_identity.md).

Locked decisions (see README):
  - Name "Photon Mountain" is locked.
  - Scale K = 8 px per mile, identical on both maps, so true sizes are honest.
  - Up to three nested regions per map (core, greater, outer); the current maps
    use two, core and greater (the outer tier is empty).
  - Regions are buffered convex hulls (Minkowski sum of the tier's cities with a
    disk of radius BUFFER_PX), computed as the convex hull of a ring of sample
    points placed around every city. Nested city sets give nested blobs, always.
  - One hue, Laser Violet. Bands are the SAME translucent violet stacked, so
    the overlap darkens toward the core. No capital; every city is a dot scaled
    to its 2020 population, so each city reads at its true weight.

This generator writes two self-contained HTML files (a full cut and a core-only
cut) with the clip-path polygons baked in, plus a pixel-faithful PNG preview of
each, drawn from the identical polygon data so the look-test matches the HTML.
"""
import math
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
from matplotlib.patches import Polygon as MplPolygon

# Brand values come from 04_tools/brand_tokens.py, never hardcoded here.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "04_tools"))
import brand_tokens as BT

# Register the brand TTFs with matplotlib so the PNG previews match the HTML.
for _role in ("display_medium", "display_bold", "body_regular", "body_medium",
              "body_semibold", "mono_regular", "mono_bold"):
    try:
        _fm.fontManager.addfont(BT.font_path(_role))
    except Exception:
        pass
BRAND_FONTS_OK = all(
    os.path.isfile(BT.font_path(r))
    for r in ("display_medium", "body_regular", "mono_regular"))

# ---------------------------------------------------------------- constants
K = 8.0                     # pixels per mile, shared by both maps (LOCKED)
MILES_PER_DEG_LAT = 69.0
PAD = 72.0                  # px padding around each map's content
BUFFER_PX = 8.0             # shared blob buffer radius, same for every tier/map
# (tightened from 18 so the core blob hugs its true cities; at 18 the cushion
#  reached Superior and Westminster, ~1.6 and ~2.2 mi outside the core, and made
#  them read as core. 8 px = 1 mile keeps the blobs readable and honest.)
CIRCLE_SAMPLES = 72         # points sampled around each city for the blob hull

# Sequential single hue, composited by translucent overlap. Laser Violet is
# the brand's data-and-secondary accent, which is what these bands are; using
# Alpenglow here would fight the "one loud thing per piece" rule, since the
# bands are the whole field. One hue keeps the overlap readable and the
# nesting legible, and stays colorblind-safe.
def _rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

BAND_BASE = _rgb(BT.COLOR_LASER_VIOLET)
BLUE_BASE = BAND_BASE       # retained name: the compositing code reads this
BAND_ALPHA = 0.22
PAPER = _rgb(BT.COLOR_SNOWFIELD)    # the compositing background
SLATE = BT.COLOR_SUMMIT_NIGHT       # uniform dark dots
SLATE_RGB = _rgb(BT.COLOR_SUMMIT_NIGHT)
GOLD = BT.COLOR_ALPENGLOW           # accent marks (the capital star is retired)
GOLD_INK = BT.COLOR_ALPENGLOW_DEEP  # accent as a stroke or small mark
INK = BT.COLOR_SUMMIT_NIGHT
STONE = BT.COLOR_GRANITE
PAPER_HEX = BT.COLOR_SNOWFIELD   # same value as PAPER, as a hex string

# ---------------------------------------------------------------- city data (LOCKED)
# t = innermost tier the city belongs to. Castle Rock and Colorado Springs are
# intentionally excluded from Photon Mountain.
CITIES = {
    "SV": [
        {"n": "Palo Alto",     "lat": 37.4419, "lon": -122.1430, "t": "core",    "pop": 68572},
        {"n": "Mountain View", "lat": 37.3861, "lon": -122.0839, "t": "core",    "pop": 82376},
        {"n": "Sunnyvale",     "lat": 37.3688, "lon": -122.0363, "t": "core",    "pop": 155805},
        {"n": "Cupertino",     "lat": 37.3230, "lon": -122.0322, "t": "core",    "pop": 60381},
        {"n": "Santa Clara",   "lat": 37.3541, "lon": -121.9552, "t": "core",    "pop": 127647},
        {"n": "San Jose",      "lat": 37.3382, "lon": -121.8863, "t": "core",    "pop": 1013240},
        {"n": "Menlo Park",    "lat": 37.4530, "lon": -122.1817, "t": "core",    "pop": 33780},
        {"n": "San Mateo",     "lat": 37.5630, "lon": -122.3255, "t": "greater", "pop": 105661},
        {"n": "Redwood City",  "lat": 37.4852, "lon": -122.2364, "t": "greater", "pop": 84292},
        {"n": "Fremont",       "lat": 37.5485, "lon": -121.9886, "t": "greater", "pop": 230504},
    ],
    "PM": [
        {"n": "Boulder",         "lat": 40.0150, "lon": -105.2705, "t": "core",    "pop": 108250},
        {"n": "Golden",          "lat": 39.7555, "lon": -105.2211, "t": "core",    "pop": 20399},
        {"n": "Arvada",          "lat": 39.8028, "lon": -105.0875, "t": "core",    "pop": 124402},
        {"n": "Denver",          "lat": 39.7392, "lon": -104.9903, "t": "core",    "pop": 715522},
        {"n": "Lafayette",       "lat": 39.9936, "lon": -105.0897, "t": "greater", "pop": 30411},
        {"n": "Louisville",      "lat": 39.9778, "lon": -105.1319, "t": "greater", "pop": 21226},
        {"n": "Broomfield",      "lat": 39.9205, "lon": -105.0867, "t": "greater", "pop": 74112},
        {"n": "Westminster",     "lat": 39.8366, "lon": -105.0372, "t": "greater", "pop": 116317},
        {"n": "Longmont",        "lat": 40.1672, "lon": -105.1019, "t": "greater", "pop": 98885},
    ],
}
TIER_IDX = {"core": 0, "greater": 1, "outer": 2}
TIER_LIST = ["core", "greater", "outer"]

MAP_META = {
    "SV": {"title": "Silicon Valley", "sub": "California"},
    "PM": {"title": "Photon Mountain", "sub": "Colorado Front Range"},
}

# ---------------------------------------------------------------- dot sizing (LOCKED)
# Every city is a proportional symbol: dot AREA is proportional to 2020 Census
# population, so radius scales with sqrt(population). No capital; the most populous
# city sets the max radius and a floor keeps the smallest towns legible.
POP_MAX = max(c["pop"] for group in CITIES.values() for c in group)
DOT_R_MAX = 15.0    # px radius of the most populous city (San Jose)
DOT_R_MIN = 4.0     # px floor so small towns stay legible


def dot_radius(pop):
    return max(DOT_R_MIN, DOT_R_MAX * math.sqrt(pop / POP_MAX))

# ---------------------------------------------------------------- geometry
def project(cities):
    """Equirectangular, K px per mile. Mutates cities, adds x,y. Returns w,h."""
    lats = [c["lat"] for c in cities]
    lons = [c["lon"] for c in cities]
    ref_lat = sum(lats) / len(lats)
    mpd_lon = MILES_PER_DEG_LAT * math.cos(math.radians(ref_lat))
    lon_min, lon_max = min(lons), max(lons)
    lat_min, lat_max = min(lats), max(lats)
    for c in cities:
        c["x"] = (c["lon"] - lon_min) * mpd_lon * K + PAD
        c["y"] = (lat_max - c["lat"]) * MILES_PER_DEG_LAT * K + PAD
    w = (lon_max - lon_min) * mpd_lon * K + 2 * PAD
    h = (lat_max - lat_min) * MILES_PER_DEG_LAT * K + 2 * PAD
    return w, h


def convex_hull(points):
    """Andrew's monotone chain, returns CCW hull (no repeat of first point)."""
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


def buffered_blob(city_pts, r=BUFFER_PX, n=CIRCLE_SAMPLES):
    """Minkowski sum of the cities' convex hull with a disk of radius r, built as
    the convex hull of a ring of points around every city. Rounds corners for
    free, handles 1 or 2 cities (circle / capsule), and nests: if set A is a
    subset of set B then blob A is contained in blob B."""
    samples = []
    for (px, py) in city_pts:
        for i in range(n):
            a = 2 * math.pi * i / n
            samples.append((px + r * math.cos(a), py + r * math.sin(a)))
    return convex_hull(samples)


def tier_points(cities, tier):
    """All city (x,y) whose tier index <= this tier's index (nested set)."""
    ti = TIER_IDX[tier]
    return [(c["x"], c["y"]) for c in cities if TIER_IDX[c["t"]] <= ti]


def composite(base, alpha, layers, bg=PAPER):
    c = list(bg)
    for _ in range(layers):
        c = [alpha * base[i] + (1 - alpha) * c[i] for i in range(3)]
    return tuple(int(round(v)) for v in c)


def hexc(rgb):
    return "#%02X%02X%02X" % rgb

# ---------------------------------------------------------------- HTML helpers
FONT_IMPORT = (
    "@import url('https://cdn.jsdelivr.net/npm/@fontsource/space-grotesk@5/index.css');"
    "@import url('https://cdn.jsdelivr.net/npm/@fontsource/inter@5/index.css');"
    "@import url('https://cdn.jsdelivr.net/npm/@fontsource/space-mono@5/index.css');"
)


def clip_path(poly):
    return "polygon(" + ", ".join("%.2fpx %.2fpx" % (x, y) for (x, y) in poly) + ")"


def centroid(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def label_box(c):
    """Estimated label bounding box (px) for monospace label text."""
    cap = c.get("cap")
    cw = 7.2 if cap else 6.1      # Space Mono char width at 11.5 / 10 px
    h = 16.0 if cap else 14.0
    w = len(c["n"]) * cw + 6
    return w, h


def layout_labels(cities, cen, base_off=16.0, iters=340, margin=5.0):
    """Force-directed label placement: seed each label radially outward from the
    map centroid, then iteratively push labels apart, push them off every dot, and
    spring them back toward their radial anchor. Returns name -> dict with final
    center, box size, the dot it belongs to, and whether a leader line is needed.
    Used by BOTH the HTML and the PNG preview so the two always match."""
    L = {}
    for c in cities:
        dx, dy = c["x"] - cen[0], c["y"] - cen[1]
        d = math.hypot(dx, dy) or 1.0
        ux, uy = dx / d, dy / d
        w, h = label_box(c)
        dot_r = dot_radius(c["pop"])
        off = dot_r + base_off + h / 2
        L[c["n"]] = {"x": c["x"] + ux * off, "y": c["y"] + uy * off,
                     "ax": c["x"] + ux * off, "ay": c["y"] + uy * off,
                     "w": w, "h": h, "dx": c["x"], "dy": c["y"], "dot_r": dot_r}
    names = [c["n"] for c in cities]
    # avoidance radius per marker = its population dot radius
    dots = [(c["x"], c["y"], dot_radius(c["pop"])) for c in cities]
    for _ in range(iters):
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = L[names[i]], L[names[j]]
                dx, dy = b["x"] - a["x"], b["y"] - a["y"]
                ox = (a["w"] + b["w"]) / 2 + margin - abs(dx)
                oy = (a["h"] + b["h"]) / 2 + margin - abs(dy)
                if ox > 0 and oy > 0:
                    if ox < oy:
                        s = ox / 2 * (1 if dx >= 0 else -1)
                        a["x"] -= s; b["x"] += s
                    else:
                        s = oy / 2 * (1 if dy >= 0 else -1)
                        a["y"] -= s; b["y"] += s
        for nm in names:
            a = L[nm]
            for (px, py, dr) in dots:
                ddx, ddy = a["x"] - px, a["y"] - py
                ox = (a["w"] / 2 + dr + 3) - abs(ddx)
                oy = (a["h"] / 2 + dr + 3) - abs(ddy)
                if ox > 0 and oy > 0:
                    if ox < oy:
                        a["x"] += ox * (1 if ddx >= 0 else -1)
                    else:
                        a["y"] += oy * (1 if ddy >= 0 else -1)
        for nm in names:
            a = L[nm]
            a["x"] += (a["ax"] - a["x"]) * 0.02
            a["y"] += (a["ay"] - a["y"]) * 0.02
    out = {}
    for nm in names:
        a = L[nm]
        dist = math.hypot(a["x"] - a["dx"], a["y"] - a["dy"])
        leader = dist > (a["dot_r"] + a["h"] / 2 + 12)
        out[nm] = {"x": a["x"], "y": a["y"], "w": a["w"], "h": a["h"],
                   "dx": a["dx"], "dy": a["dy"], "leader": leader,
                   "dot_r": a["dot_r"]}
    return out


def leader_endpoint(lab):
    """Point on the label box edge facing the dot, so a leader line stops at the
    text box instead of crossing it."""
    cx, cy = lab["x"], lab["y"]
    dx, dy = lab["dx"] - cx, lab["dy"] - cy
    if dx == 0 and dy == 0:
        return cx, cy
    hw, hh = lab["w"] / 2 + 1, lab["h"] / 2 + 1
    sx = hw / abs(dx) if dx else float("inf")
    sy = hh / abs(dy) if dy else float("inf")
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s


def map_html(cities, tiers, solid_fill=None):
    """Render one map panel's inner HTML (regions, population dots, labels).
    solid_fill: hex string used as an opaque band fill for the single-band core
    cut, so its one ring reads at the core shade rather than the lightest layer."""
    w, h = project(cities)
    cen = centroid([(c["x"], c["y"]) for c in cities])
    parts = ['<div class="map" style="width:%.1fpx;height:%.1fpx">' % (w, h)]
    # regions, outer first so core is on top and overlaps darken inward
    fill = "rgba(%d,%d,%d,%.3f)" % (BLUE_BASE[0], BLUE_BASE[1], BLUE_BASE[2], BAND_ALPHA)
    for tier in [t for t in ["outer", "greater", "core"] if t in tiers]:
        blob = buffered_blob(tier_points(cities, tier))
        edge = composite(BLUE_BASE, min(0.9, BAND_ALPHA + 0.18), TIER_IDX[tier] + 1)
        bg = solid_fill if solid_fill else fill
        parts.append(
            '<div class="rgn" style="clip-path:%s;background:%s;'
            'box-shadow:inset 0 0 0 1px %s"></div>'
            % (clip_path(blob), bg, hexc(edge) + "55")
        )
    # dots, scaled to 2020 population (no capital; each city reads at its weight)
    for c in cities:
        r = dot_radius(c["pop"])
        bw = 1.0 if r < 6 else 1.5
        parts.append(
            '<div class="dot" style="left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx;'
            'border-width:%.1fpx"></div>'
            % (c["x"], c["y"], 2 * r, 2 * r, bw))
    # labels, force-laid-out so they do not overlap each other or the dots
    labs = layout_labels(cities, cen)
    leaders, texts = [], []
    for c in cities:
        lab = labs[c["n"]]
        if lab["leader"]:
            ex, ey = leader_endpoint(lab)
            dx, dy = ex - lab["dx"], ey - lab["dy"]
            length = math.hypot(dx, dy)
            ang = math.degrees(math.atan2(dy, dx))
            leaders.append(
                '<div class="leader" style="left:%.1fpx;top:%.1fpx;width:%.1fpx;'
                'transform:rotate(%.2fdeg)"></div>' % (lab["dx"], lab["dy"], length, ang))
        cls = "label cap" if c.get("cap") else "label"
        texts.append('<div class="%s" style="left:%.1fpx;top:%.1fpx">%s</div>'
                     % (cls, lab["x"], lab["y"], c["n"]))
    parts += leaders + texts          # leaders under labels
    parts.append("</div>")
    return "".join(parts), w, h


def legend_html(tiers=("core", "greater")):
    # rendered layer counts: core sits under 3 stacked fills (darkest), greater
    # under 2. (With no outer cities, the outer blob coincides with greater, which
    # is what keeps the core at its full dark shade.)
    layers = {"core": 3, "greater": 2}
    swatches = []
    for tier in tiers:
        col = composite(BLUE_BASE, BAND_ALPHA, layers[tier])
        swatches.append(
            '<div class="it"><span class="sw" style="background:%s"></span>%s</div>'
            % (hexc(col), tier.capitalize()))
    return "".join(swatches)


def sizekey_html(pops=(100000, 500000, 1000000), labels=("100k", "500k", "1M")):
    """A proportional-symbol size key: reference dots for a few populations so a
    reader can decode dot size back to people."""
    items = ['<span class="szlab">Dot size = city population (2020 Census):</span>']
    for p, lab in zip(pops, labels):
        r = dot_radius(p)
        items.append(
            '<div class="it"><span class="szc" style="width:%.1fpx;height:%.1fpx">'
            '</span>%s</div>' % (2 * r, 2 * r, lab))
    return '<div class="sizekey">' + "".join(items) + "</div>"


# Built from brand_tokens so the stylesheet carries no hardcoded hex either.
# Band colors for the rule gradient are sampled from the same composited
# stack the maps use, so the rule reads as a miniature of the legend.
_RULE_MID = BT.mix(BT.COLOR_SNOWFIELD, BT.COLOR_LASER_VIOLET, 0.35)
_RULE_LO = BT.mix(BT.COLOR_SNOWFIELD, BT.COLOR_LASER_VIOLET, 0.15)

PAGE_CSS = """
*{box-sizing:border-box;}
body{margin:0;background:%(paper)s;color:%(ink)s;
  font-family:'Inter',system-ui,'Segoe UI',Arial,sans-serif;-webkit-font-smoothing:antialiased;}
.wrap{padding:34px 40px 46px;}
h1{font-family:'Space Grotesk',Georgia,serif;font-size:27px;font-weight:700;
  letter-spacing:-0.3px;margin:0;line-height:1.18;}
.sub{color:%(stone)s;font-size:14px;margin-top:8px;max-width:760px;line-height:1.5;}
.rule{height:3px;width:140px;border-radius:2px;margin:18px 0 28px;
  background:linear-gradient(90deg,%(rule_lo)s,%(rule_mid)s,%(violet)s);}
.maps{display:flex;gap:48px;align-items:flex-start;flex-wrap:wrap;}
.phead{font-family:'Inter',sans-serif;font-size:12px;letter-spacing:1.4px;
  text-transform:uppercase;font-weight:600;margin-bottom:12px;color:%(ink)s;}
.phead .s{display:block;font-size:11px;letter-spacing:0.3px;text-transform:none;
  color:%(stone)s;font-weight:400;margin-top:3px;}
.map{position:relative;}
.rgn{position:absolute;inset:0;pointer-events:none;}
.dot{position:absolute;width:9px;height:9px;border-radius:50%%;background:%(ink)s;
  border:1.5px solid %(paper)s;transform:translate(-50%%,-50%%);
  box-shadow:0 0 0 1px rgba(19,26,51,0.25);}
.dot.big{width:12px;height:12px;}
.star{position:absolute;transform:translate(-50%%,-50%%);color:%(accent)s;font-size:23px;
  line-height:1;-webkit-text-stroke:0.6px %(accent_ink)s;}
.label{position:absolute;transform:translate(-50%%,-50%%);
  font-family:'Space Mono','SF Mono',Consolas,monospace;font-size:10px;color:%(stone)s;
  white-space:nowrap;pointer-events:none;
  text-shadow:0 0 3px %(paper)s,0 0 3px %(paper)s,0 0 2px %(paper)s,0 0 2px %(paper)s;}
.label.cap{font-size:11.5px;font-weight:700;color:%(violet_deep)s;}
.leader{position:absolute;height:1px;background:%(stone)s;opacity:0.5;
  transform-origin:0 50%%;pointer-events:none;}
.footer{margin-top:40px;max-width:880px;}
.sbwrap{display:flex;align-items:center;gap:12px;margin-bottom:20px;}
.sbar{height:9px;border-left:2px solid %(ink)s;border-right:2px solid %(ink)s;
  border-bottom:2px solid %(ink)s;}
.sblab{font-family:'Space Mono',Consolas,monospace;font-size:12px;color:%(stone)s;}
.legend{display:flex;gap:24px;flex-wrap:wrap;margin-bottom:20px;font-size:13px;}
.legend .it{display:flex;align-items:center;gap:8px;}
.sw{width:15px;height:15px;border-radius:50%%;border:1.5px solid %(paper)s;
  box-shadow:0 0 0 1px rgba(0,0,0,0.10);}
.star-lg{color:%(accent)s;font-size:17px;line-height:1;-webkit-text-stroke:0.5px %(accent_ink)s;}
.caption{font-size:14px;line-height:1.66;color:%(ink)s;max-width:880px;}
.caption b{color:%(ink)s;}
.note{margin-top:18px;font-size:12.5px;line-height:1.6;color:%(stone)s;max-width:880px;}
.note b{color:%(ink)s;}
.tagline{margin-top:26px;font-family:'Space Grotesk',sans-serif;font-size:13px;
  font-weight:700;letter-spacing:0.3px;color:%(ink)s;}
.method{font-family:'Space Mono',Consolas,monospace;font-size:10.5px;color:%(stone)s;margin-top:5px;}
.sizekey{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin:2px 0 20px;font-size:13px;}
.sizekey .it{display:flex;align-items:center;gap:7px;}
.szc{display:inline-block;border-radius:50%%;background:%(ink)s;border:1.2px solid %(paper)s;
  box-shadow:0 0 0 1px rgba(19,26,51,0.25);vertical-align:middle;}
.szlab{color:%(stone)s;font-size:12px;}
""" % {
    "paper": BT.COLOR_SNOWFIELD,
    "ink": BT.COLOR_SUMMIT_NIGHT,
    "stone": BT.COLOR_GRANITE,
    "accent": BT.COLOR_ALPENGLOW,
    "accent_ink": BT.COLOR_ALPENGLOW_DEEP,
    "violet": BT.COLOR_LASER_VIOLET,
    "violet_deep": BT.COLOR_VIOLET_DEEP,
    "rule_mid": _RULE_MID,
    "rule_lo": _RULE_LO,
}


def build_full(path_html, path_png):
    cities_sv = [dict(c) for c in CITIES["SV"]]
    cities_pm = [dict(c) for c in CITIES["PM"]]
    sv_html, sw, sh = map_html(cities_sv, ["outer", "greater", "core"])
    pm_html, pw, ph = map_html(cities_pm, ["outer", "greater", "core"])
    caption = (
        "Read the cores against each other first. Each one is anchored by a major city, "
        "San Jose for the Valley and Denver for Photon Mountain, ringed by the towns "
        "where the labs and fabs sit. The dots are scaled to population, so the two "
        "anchors are the big circles you see first. Photon Mountain's core runs a little "
        "wider, Boulder down to Denver, because Denver anchors it the way San Jose "
        "anchors the Valley. A bigger ring is not a better region, and the outlines hide "
        "something. Silicon Valley wraps the south end of San Francisco Bay, so part of "
        "its footprint is open water with no one on it. Photon Mountain is solid Front "
        "Range. <b>The measure that matters is people, not acres, and Colorado already "
        "has the core and the city to anchor it.</b>")
    note = (
        "<b>Why Photon Mountain.</b> A photon is the quantum particle of light, so "
        "one word holds both the photonic chips Colorado can manufacture and the "
        "quantum science Colorado can run. It names a real thing the way silicon "
        "did. Colorado's answer to the Valley.")
    html = _page(
        "Silicon Valley and Photon Mountain, two rings to true scale",
        "Both maps are drawn from real coordinates at the same scale, 8 pixels per "
        "mile. Two nested rings each: a dense core and a greater ring around it. Each "
        "ring is the buffered outline of the cities it holds, so the rings nest "
        "honestly and the overlap darkens toward the core.",
        sv_html, pm_html, caption, note)
    with open(path_html, "w") as f:
        f.write(html)
    render_preview([("SILICON VALLEY", cities_sv, ["outer", "greater", "core"], sw, sh),
                    ("PHOTON MOUNTAIN", cities_pm, ["outer", "greater", "core"], pw, ph)],
                   path_png, "Two rings to true scale  (8 px / mile, shared)")
    return sw, sh, pw, ph


def build_core(path_html, path_png):
    cities_sv = [dict(c) for c in CITIES["SV"] if c["t"] == "core"]
    cities_pm = [dict(c) for c in CITIES["PM"] if c["t"] == "core"]
    core_solid = hexc(composite(BLUE_BASE, BAND_ALPHA, 3))  # match cut-1 core shade
    sv_html, sw, sh = map_html(cities_sv, ["core"], solid_fill=core_solid)
    pm_html, pw, ph = map_html(cities_pm, ["core"], solid_fill=core_solid)
    caption = (
        "This is the comparison that counts. Strip away the suburbs and two cores are "
        "left, drawn at the same scale, each anchored by a major city. Silicon Valley "
        "has San Jose. Photon Mountain has Denver, with Boulder, Golden, and Arvada "
        "around it. The dots are scaled to population, so the anchors read at a glance. "
        "<b>Colorado already has a core and a city to anchor it. The work ahead is to "
        "fill in the density between.</b>")
    note = (
        "<b>Why Photon Mountain.</b> A photon is the quantum particle of light, one "
        "word for the photonic chips Colorado can make and the quantum science "
        "Colorado can run. Colorado's answer to the Valley.")
    html = _page(
        "The cores, side by side",
        "Just the core of each region, the Boulder, Golden, Arvada, and Denver core against "
        "Palo Alto to San Jose, at the same scale, 8 pixels per mile.",
        sv_html, pm_html, caption, note, legend_tiers=("core",))
    with open(path_html, "w") as f:
        f.write(html)
    render_preview([("SILICON VALLEY core", cities_sv, ["core"], sw, sh),
                    ("PHOTON MOUNTAIN core", cities_pm, ["core"], pw, ph)],
                   path_png, "The cores, side by side  (8 px / mile, shared)",
                   solid_rgba=composite(BLUE_BASE, BAND_ALPHA, 3))
    return sw, sh, pw, ph


def _page(title, sub, sv_html, pm_html, caption, note, legend_tiers=("core", "greater")):
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>%s
%s</style></head><body><div class="wrap">
<h1>%s</h1>
<div class="sub">%s</div>
<div class="rule"></div>
<div class="maps">
  <div class="panel"><div class="phead">Silicon Valley<span class="s">California</span></div>%s</div>
  <div class="panel"><div class="phead">Photon Mountain<span class="s">Colorado Front Range</span></div>%s</div>
</div>
<div class="footer">
  <div class="sbwrap"><div class="sbar" style="width:%.0fpx"></div><span class="sblab">10 miles, same scale on both maps</span></div>
  <div class="legend">%s</div>
  %s
  <p class="caption">%s</p>
  <p class="note">%s</p>
  <div class="tagline">Build with light.</div>
  <div class="method">Photon Mountain, a Colorado Startups project in collaboration with Colorado AI  /  built to scale, 8 pixels per mile, buffered convex-hull regions</div>
</div></div></body></html>""" % (
        title, FONT_IMPORT, PAGE_CSS, title, sub, sv_html, pm_html,
        10 * K, legend_html(legend_tiers), sizekey_html(), caption, note)


# ---------------------------------------------------------------- PNG preview
def render_preview(panels, out_png, suptitle, solid_rgba=None):
    """Draw both panels in a single axes at one shared pixel scale, so the PNG is
    a faithful, honest mirror of the HTML (same projection, same blob polygons)."""
    gap = 90.0
    # lay panels left to right, tops aligned at y=0
    widths = [p[3] for p in panels]
    heights = [p[4] for p in panels]
    x_off = 0.0
    fig_h = max(heights)
    total_w = sum(widths) + gap * (len(panels) - 1)

    fig, ax = plt.subplots(figsize=(total_w / 80.0, (fig_h + 120) / 80.0), dpi=150)
    ax.set_facecolor(PAPER_HEX)
    fig.patch.set_facecolor(PAPER_HEX)

    fill = (BLUE_BASE[0] / 255, BLUE_BASE[1] / 255, BLUE_BASE[2] / 255, BAND_ALPHA)
    if solid_rgba:
        fill = (solid_rgba[0] / 255, solid_rgba[1] / 255, solid_rgba[2] / 255, 1.0)
    for (name, cities, tiers, w, h) in panels:
        project(cities)  # ensure x,y present
        cen = centroid([(c["x"], c["y"]) for c in cities])
        for tier in [t for t in ["outer", "greater", "core"] if t in tiers]:
            blob = buffered_blob(tier_points(cities, tier))
            poly = [(x + x_off, y) for (x, y) in blob]
            ax.add_patch(MplPolygon(poly, closed=True, facecolor=fill,
                                    edgecolor=(0.10, 0.36, 0.69, 0.35), linewidth=0.8))
        labs = layout_labels(cities, cen)
        for c in cities:
            cx, cy = c["x"] + x_off, c["y"]
            lab = labs[c["n"]]
            if lab["leader"]:
                ex, ey = leader_endpoint(lab)
                ax.plot([lab["dx"] + x_off, ex + x_off], [lab["dy"], ey],
                        color=STONE, lw=0.7, alpha=0.5, zorder=4)
            r = dot_radius(c["pop"])
            ax.plot(cx, cy, marker="o", markersize=1.52 * r, color=SLATE,
                    markeredgecolor=PAPER_HEX, markeredgewidth=1.0, zorder=5)
            ax.annotate(c["n"], (lab["x"] + x_off, lab["y"]), ha="center", va="center",
                        fontsize=7.5, family="Space Mono", zorder=7,
                        color=STONE, path_effects=_halo())
        ax.text(x_off + w / 2, -34, name, ha="center", va="center",
                fontsize=10, fontweight="bold", color=INK)
        x_off += w + gap

    # shared 10-mile scale bar, bottom left, in the same pixel units
    sb_y = fig_h + 48
    ax.plot([0, 10 * K], [sb_y, sb_y], color=INK, lw=2)
    ax.plot([0, 0], [sb_y - 6, sb_y + 6], color=INK, lw=2)
    ax.plot([10 * K, 10 * K], [sb_y - 6, sb_y + 6], color=INK, lw=2)
    ax.text(10 * K + 12, sb_y, "10 miles, same scale on both", ha="left", va="center",
            fontsize=9, family="Space Mono", color=STONE)

    # population size key, a row of reference dots so dot size decodes to people
    key_y = fig_h + 94
    ax.text(6.0, key_y, "Dot size = 2020 population:", ha="left", va="center",
            fontsize=8.5, family="Space Mono", color=STONE)
    kx = 285.0
    for p, lab in [(100000, "100k"), (500000, "500k"), (1000000, "1M")]:
        r = dot_radius(p)
        ax.plot(kx, key_y, marker="o", markersize=1.52 * r, color=SLATE,
                markeredgecolor=PAPER_HEX, markeredgewidth=1.0, zorder=5)
        ax.text(kx, key_y + 26, lab, ha="center", va="center", fontsize=8,
                family="Space Mono", color=STONE)
        kx += 80

    ax.set_xlim(-PAD * 0.4, total_w + PAD * 0.4)
    ax.set_ylim(fig_h + 128, -70)   # inverted y, screen-style
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(suptitle, fontsize=12, color=INK, pad=14,
                 fontfamily="Space Grotesk", loc="left")
    fig.tight_layout()
    fig.savefig(out_png, dpi=150, facecolor=PAPER_HEX, bbox_inches="tight")
    plt.close(fig)


def _halo():
    import matplotlib.patheffects as pe
    return [pe.withStroke(linewidth=2.4, foreground=PAPER_HEX)]


if __name__ == "__main__":
    import sys
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    a = build_full(outdir + "/photon_mountain_vs_silicon_valley.html",
                   outdir + "/photon_mountain_vs_silicon_valley_preview.png")
    b = build_core(outdir + "/photon_mountain_vs_silicon_valley_core.html",
                   outdir + "/photon_mountain_vs_silicon_valley_core_preview.png")
    print("full panel px  SV=%.0fx%.0f  PM=%.0fx%.0f" % a)
    print("core panel px  SV=%.0fx%.0f  PM=%.0fx%.0f" % b)
    print("wrote HTML + previews to", outdir)
