#!/usr/bin/env python3
"""marker_parity.py: the corridor atlas's cross-file invariant, checked.

The Photon Mountain corridor map ships as four files that must carry the same
roster: a GeoJSON, a KML, a self-contained HTML map, and a React component.
MAP_NOTES.md records that parity being confirmed by hand on every revision
("rosters name- and coordinate-identical, notes byte-identical, KML
well-formed"). This script does that check, so a revision cannot quietly land
with the four files out of step.

It is NOT the same thing as 03_deliverables/infographics/photon_mountain_map_verify.py,
which checks the Silicon Valley comparison maps' geometry. This one checks the
corridor atlas's roster. Both exist; neither covers the other.

Three format differences are expected, and normalised rather than reported:

  1. KML escapes XML entities. Three marker names contain "&", stored as
     "&amp;". Names are unescaped before comparison.
  2. KML rounds coordinates, to between three and six decimal places. Exact
     comparison fails today on one marker by 4e-7 degrees, about 4 cm, which
     is rounding and not a move. Coordinates are compared at PLACES decimals
     (default 5, about 1.1 m), which absorbs the rounding and still catches
     any real repositioning.
  3. Notes are not identical across formats, by design. The HTML and JSX notes
     are "<Category>. " + the GeoJSON note, because GeoJSON carries `category`
     as its own property instead. The script enforces that relationship, which
     is stronger than either ignoring notes or demanding identical strings: it
     catches a category and a note drifting apart.

Standard library only, matching voice_lint.py and brand_tokens.py.

Usage:
  python3 marker_parity.py [--maps-dir DIR] [--places N]
  python3 marker_parity.py --self-test

Exit codes: 0 = the four files agree, 1 = drift, 2 = usage or read error.
"""

import argparse
import html
import json
import os
import re
import sys

DEFAULT_PLACES = 5

# The seven locked categories, per MAP_NOTES.md. HTML and JSX notes are
# prefixed with one of these followed by ". ".
CATEGORIES = (
    "Government Hall",
    "Transit Station",
    "University Campus",
    "National Lab",
    "University Lab",
    "Fabrication Facility",
    "Innovation Campus",
)

_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MAPS_DIR = os.path.join(os.path.dirname(_HERE), "03_deliverables", "maps")

FILES = {
    "geojson": "photon_mountain_corridor.geojson",
    "kml": "photon_mountain_corridor.kml",
    "html": "photon_mountain_boundary_map.html",
    "jsx": "PhotonMountainMap.jsx",
}


# ------------------------------------------------------------- extraction ---
def from_geojson(path):
    """{name: (lat, lon, category, note)} from the Point features."""
    data = json.loads(open(path, encoding="utf-8").read())
    out = {}
    for feat in data["features"]:
        if feat["geometry"]["type"] != "Point":
            continue
        lon, lat = feat["geometry"]["coordinates"][:2]
        props = feat["properties"]
        out[props["name"]] = (lat, lon, props.get("category"), props.get("note"))
    return out


def from_kml(path):
    """{name: (lat, lon, None, description)} from the Point placemarks."""
    text = open(path, encoding="utf-8").read()
    out = {}
    for block in re.findall(r"<Placemark>(.*?)</Placemark>", text, re.S):
        if "<Point>" not in block:
            continue
        name = re.search(r"<name>(.*?)</name>", block, re.S)
        coord = re.search(r"<coordinates>\s*([-\d.]+),([-\d.]+)", block, re.S)
        if not (name and coord):
            continue
        desc = re.search(r"<description>(.*?)</description>", block, re.S)
        out[_clean_xml(name.group(1))] = (
            float(coord.group(2)), float(coord.group(1)),
            None, _clean_xml(desc.group(1)) if desc else None)
    return out


def _clean_xml(s):
    s = re.sub(r"^\s*<!\[CDATA\[|\]\]>\s*$", "", s.strip())
    return html.unescape(s).strip()


def from_js(path, var="MARKERS"):
    """{name: (lat, lon, category, note)} from an HTML or JSX marker array.

    Handles both shapes the project uses: the HTML's positional arrays
    ([name, lat, lon, cat, note, inside]) and the JSX's objects
    ({name, ll: [lat, lon], cat, note}).
    """
    text = open(path, encoding="utf-8").read()
    match = re.search(r"\b%s\s*=\s*(\[)" % re.escape(var), text)
    if not match:
        raise ValueError("no %s array found in %s" % (var, os.path.basename(path)))
    raw = _balanced_array(text, match.start(1))
    out = {}
    for row in json.loads(raw):
        if isinstance(row, dict):
            out[row["name"]] = (row["ll"][0], row["ll"][1],
                                row.get("cat"), row.get("note"))
        else:
            out[row[0]] = (row[1], row[2],
                           row[3] if len(row) > 3 else None,
                           row[4] if len(row) > 4 else None)
    return out


def _balanced_array(text, start):
    """Slice the JSON array beginning at `start`, respecting strings."""
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise ValueError("unterminated array")


# ------------------------------------------------------------- comparison ---
def split_prefix(note):
    """('Category', 'rest') if note starts with a locked category, else (None, note)."""
    if not note:
        return None, note
    for cat in CATEGORIES:
        prefix = cat + ". "
        if note.startswith(prefix):
            return cat, note[len(prefix):]
    return None, note


def compare(rosters, places=DEFAULT_PLACES):
    """Return a list of human-readable drift findings. Empty means parity."""
    findings = []
    ref_name = "geojson"
    ref = rosters[ref_name]

    counts = {k: len(v) for k, v in rosters.items()}
    if len(set(counts.values())) != 1:
        findings.append("marker counts differ: %s"
                        % ", ".join("%s=%d" % kv for kv in sorted(counts.items())))

    for name, roster in sorted(rosters.items()):
        if name == ref_name:
            continue
        missing = sorted(set(ref) - set(roster))
        extra = sorted(set(roster) - set(ref))
        for n in missing:
            findings.append("%s: missing marker %r" % (name, n))
        for n in extra:
            findings.append("%s: unexpected marker %r" % (name, n))

        for n in sorted(set(ref) & set(roster)):
            a, b = ref[n], roster[n]
            if (round(a[0], places), round(a[1], places)) != \
               (round(b[0], places), round(b[1], places)):
                findings.append(
                    "%s: %r coordinates differ beyond %d decimals: "
                    "geojson=(%s, %s) %s=(%s, %s)"
                    % (name, n, places, a[0], a[1], name, b[0], b[1]))

    # The note-prefix rule, for the two formats that carry it.
    for name in ("html", "jsx"):
        roster = rosters.get(name)
        if not roster:
            continue
        for n in sorted(set(ref) & set(roster)):
            ref_note = (ref[n][3] or "").strip()
            cat = ref[n][2]
            prefix_cat, body = split_prefix((roster[n][3] or "").strip())
            if body != ref_note:
                findings.append(
                    "%s: %r note body differs from the geojson note" % (name, n))
            elif prefix_cat is None:
                findings.append(
                    "%s: %r note does not start with a locked category prefix"
                    % (name, n))
            elif cat and prefix_cat.lower() != str(cat).lower():
                findings.append(
                    "%s: %r note prefix %r does not match the geojson category %r"
                    % (name, n, prefix_cat, cat))
    return findings


# ------------------------------------------------------------------ tests ---
def self_test():
    ok = True
    ref = {"A": (40.0, -105.0, "National Lab", "A note."),
           "B & C": (39.5, -105.5, "Transit Station", "Another note.")}

    good = {
        "geojson": ref,
        "kml": {"A": (40.000000, -105.000000, None, "A note."),
                # 4e-7 of rounding, the real-world KML case
                "B & C": (39.4999996, -105.5, None, "Another note.")},
        "html": {"A": (40.0, -105.0, "natlab", "National Lab. A note."),
                 "B & C": (39.5, -105.5, "transit", "Transit Station. Another note.")},
    }
    found = compare(good, places=DEFAULT_PLACES)
    if found:
        ok = False
        print("self-test: clean roster reported drift: FAIL")
        for f in found:
            print("   ", f)
    else:
        print("self-test: clean roster passes, KML rounding absorbed: OK")

    moved = {k: dict(v) for k, v in good.items()}
    moved["kml"]["A"] = (40.01, -105.0, None, "A note.")   # ~1.1 km
    if any("coordinates differ" in f for f in compare(moved)):
        print("self-test: a real coordinate move is caught: OK")
    else:
        ok = False
        print("self-test: a real coordinate move was NOT caught: FAIL")

    # Unescaping is the KML reader's job, not compare()'s, so test that layer.
    cases = [("B &amp; C", "B & C"),
             ("<![CDATA[NLR S&amp;TF]]>", "NLR S&TF"),
             ("  Plain Name  ", "Plain Name")]
    bad = [(raw, want, _clean_xml(raw)) for raw, want in cases
           if _clean_xml(raw) != want]
    if bad:
        ok = False
        for raw, want, got in bad:
            print("self-test: _clean_xml(%r) gave %r, wanted %r: FAIL"
                  % (raw, got, want))
    else:
        print("self-test: KML entity and CDATA unescaping: OK")

    dropped = {k: dict(v) for k, v in good.items()}
    del dropped["html"]["A"]
    if any("missing marker" in f for f in compare(dropped)):
        print("self-test: a dropped marker is caught: OK")
    else:
        ok = False
        print("self-test: a dropped marker was NOT caught: FAIL")

    crossed = {k: dict(v) for k, v in good.items()}
    crossed["html"]["A"] = (40.0, -105.0, "natlab", "Transit Station. A note.")
    if any("prefix" in f for f in compare(crossed)):
        print("self-test: a category/note mismatch is caught: OK")
    else:
        ok = False
        print("self-test: a category/note mismatch was NOT caught: FAIL")

    print("self-test:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


# ------------------------------------------------------------------- main ---
def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check the corridor atlas's four files for roster parity")
    parser.add_argument("--maps-dir", default=DEFAULT_MAPS_DIR,
                        help="directory holding the four map files")
    parser.add_argument("--places", type=int, default=DEFAULT_PLACES,
                        help="decimal places for coordinate comparison "
                             "(default %d, about 1.1 m)" % DEFAULT_PLACES)
    parser.add_argument("--self-test", action="store_true",
                        help="verify the checker against synthetic rosters")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    readers = {"geojson": from_geojson, "kml": from_kml,
               "html": from_js, "jsx": from_js}
    rosters = {}
    for key, filename in FILES.items():
        path = os.path.join(args.maps_dir, filename)
        if not os.path.isfile(path):
            print("marker-parity: missing %s" % path, file=sys.stderr)
            return 2
        try:
            rosters[key] = readers[key](path)
        except Exception as exc:
            print("marker-parity: could not read %s: %s" % (filename, exc),
                  file=sys.stderr)
            return 2

    findings = compare(rosters, places=args.places)
    for key in sorted(rosters):
        print("  %-8s %d markers" % (key, len(rosters[key])))
    if findings:
        print()
        for f in findings:
            print("  DRIFT %s" % f)
        print("\nmarker-parity: FAIL (%d finding%s)"
              % (len(findings), "" if len(findings) == 1 else "s"))
        return 1
    print("\nmarker-parity: PASS, all four files agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
