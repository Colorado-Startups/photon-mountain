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


def _count_findings(rosters):
    counts = {k: len(v) for k, v in rosters.items()}
    if len(set(counts.values())) == 1:
        return []
    return ["marker counts differ: %s"
            % ", ".join("%s=%d" % kv for kv in sorted(counts.items()))]


def _roster_findings(name, roster, ref, places):
    """Markers missing from or extra in one copy, and coordinates that moved."""
    findings = ["%s: missing marker %r" % (name, n) for n in sorted(set(ref) - set(roster))]
    findings += ["%s: unexpected marker %r" % (name, n) for n in sorted(set(roster) - set(ref))]
    for n in sorted(set(ref) & set(roster)):
        a, b = ref[n], roster[n]
        if (round(a[0], places), round(a[1], places)) != (round(b[0], places), round(b[1], places)):
            findings.append(
                "%s: %r coordinates differ beyond %d decimals: "
                "geojson=(%s, %s) %s=(%s, %s)"
                % (name, n, places, a[0], a[1], name, b[0], b[1]))
    return findings


def _note_finding(name, n, ref_entry, entry):
    """The note-prefix rule for one marker: the copy's note is its category, then the geojson note."""
    ref_note, cat = (ref_entry[3] or "").strip(), ref_entry[2]
    prefix_cat, body = split_prefix((entry[3] or "").strip())
    if body != ref_note:
        return "%s: %r note body differs from the geojson note" % (name, n)
    if prefix_cat is None:
        return "%s: %r note does not start with a locked category prefix" % (name, n)
    if cat and prefix_cat.lower() != str(cat).lower():
        return ("%s: %r note prefix %r does not match the geojson category %r"
                % (name, n, prefix_cat, cat))
    return None


def compare(rosters, places=DEFAULT_PLACES):
    """Return a list of human-readable drift findings. Empty means parity."""
    ref = rosters["geojson"]
    findings = _count_findings(rosters)
    for name, roster in sorted(rosters.items()):
        if name != "geojson":
            findings += _roster_findings(name, roster, ref, places)
    # The note-prefix rule, for the two formats that carry it.
    for name in ("html", "jsx"):
        roster = rosters.get(name) or {}
        found = (_note_finding(name, n, ref[n], roster[n]) for n in sorted(set(ref) & set(roster)))
        findings += [f for f in found if f]
    return findings


# ------------------------------------------------------------------ tests ---
def _good_rosters():
    ref = {"A": (40.0, -105.0, "National Lab", "A note."),
           "B & C": (39.5, -105.5, "Transit Station", "Another note.")}
    return {
        "geojson": ref,
        "kml": {"A": (40.000000, -105.000000, None, "A note."),
                # 4e-7 of rounding, the real-world KML case
                "B & C": (39.4999996, -105.5, None, "Another note.")},
        "html": {"A": (40.0, -105.0, "natlab", "National Lab. A note."),
                 "B & C": (39.5, -105.5, "transit", "Transit Station. Another note.")},
    }


def _changed(name, marker, entry):
    """The good rosters with one marker replaced (entry) or dropped (None)."""
    rosters = {k: dict(v) for k, v in _good_rosters().items()}
    if entry is None:
        del rosters[name][marker]
    else:
        rosters[name][marker] = entry
    return rosters


def _caught(rosters, needle, what):
    if any(needle in f for f in compare(rosters)):
        return True, "self-test: %s is caught: OK" % what
    return False, "self-test: %s was NOT caught: FAIL" % what


def _check_clean():
    found = compare(_good_rosters(), places=DEFAULT_PLACES)
    if found:
        return False, "\n".join(["self-test: clean roster reported drift: FAIL"] + ["    " + f for f in found])
    return True, "self-test: clean roster passes, KML rounding absorbed: OK"


def _check_unescape():
    """Unescaping is the KML reader's job, not compare()'s, so test that layer."""
    cases = [("B &amp; C", "B & C"),
             ("<![CDATA[NLR S&amp;TF]]>", "NLR S&TF"),
             ("  Plain Name  ", "Plain Name")]
    bad = ["self-test: _clean_xml(%r) gave %r, wanted %r: FAIL" % (raw, _clean_xml(raw), want)
           for raw, want in cases if _clean_xml(raw) != want]
    return (False, "\n".join(bad)) if bad else (True, "self-test: KML entity and CDATA unescaping: OK")


def self_test():
    results = [
        _check_clean(),
        _caught(_changed("kml", "A", (40.01, -105.0, None, "A note.")),   # ~1.1 km
                "coordinates differ", "a real coordinate move"),
        _check_unescape(),
        _caught(_changed("html", "A", None), "missing marker", "a dropped marker"),
        _caught(_changed("html", "A", (40.0, -105.0, "natlab", "Transit Station. A note.")),
                "prefix", "a category/note mismatch"),
    ]
    for _, line in results:
        print(line)
    ok = all(passed for passed, _ in results)
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
