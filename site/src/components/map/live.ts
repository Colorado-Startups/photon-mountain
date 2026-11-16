// The live corridor map, loaded only when the reader asks: MapLibre GL JS from npm, the OpenFreeMap Positron
// basemap, Mapterhorn relief, and the repo's GeoJSON, styled per MAP_NOTES.md revisions 7x, 7s and 8.
// Every color is a token from tokens.json; popups are built with textContent, never HTML.
import tokens from "../../styles/tokens/tokens.json";
import { BUILDING_TIER, CATS, TIER_ZOOM } from "../../lib/mapdata";

type Color = keyof typeof tokens.color;
const c = (k: string) => tokens.color[k as Color];
const STYLE = "https://tiles.openfreemap.org/styles/positron";

interface Feature { geometry: { type: string; coordinates: unknown }; properties?: Record<string, unknown> }
type Point = Feature & { geometry: { type: "Point"; coordinates: [number, number] } };
type Polygon = Feature & { geometry: { type: "Polygon"; coordinates: [number, number][][] } };
const BOUNDARY = ["boundary-fill", "boundary-glow", "boundary-casing", "boundary-line"];

export interface LiveMap {
  filter(cats: string[], boundary: boolean): void;
  flyTo(name: string): void;
  fit(): void;
}

// The stylesheet comes in as a URL and a <link> made on request: a plain CSS import here would be hoisted into
// the page's <head> by Astro, so every visit would fetch it before anyone opens the map.
async function loadStyles(): Promise<void> {
  const { default: href } = await import("maplibre-gl/dist/maplibre-gl.css?url");
  if (document.querySelector(`link[href="${href}"]`)) return;
  await new Promise<void>((resolve, reject) => {
    const link = Object.assign(document.createElement("link"), { rel: "stylesheet", href });
    link.onload = () => resolve();
    link.onerror = () => { link.remove(); reject(new Error("the map's styles did not load")); };
    document.head.append(link);
  });
}

export async function openLiveMap(container: HTMLElement, say: (msg: string) => void): Promise<LiveMap> {
  const [gl, data] = await Promise.all([
    // MapLibre looks for its worker next to its own module, which bundling moves; hand it the emitted file.
    Promise.all([import("maplibre-gl"), import("maplibre-gl/dist/maplibre-gl-worker.mjs?url"), loadStyles()]).then(([m, worker]) => {
      m.setWorkerUrl(worker.default);
      return m;
    }),
    fetch("/data/corridor.geojson").then((r) => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); }),
  ]);
  const points = (data.features as Feature[]).filter((f) => f.geometry.type === "Point") as Point[];
  const ring = (data.features as Feature[]).find((f) => f.geometry.type === "Polygon") as Polygon;
  let visible = CATS.map((x) => x.id);
  let boundaryOn = true;

  const map = new gl.Map({ container, style: STYLE, center: [-105.14, 39.87], zoom: 9.6, attributionControl: { compact: true } });
  map.addControl(new gl.NavigationControl({ showCompass: false }), "top-left");
  map.addControl(new gl.ScaleControl({ unit: "imperial" }), "bottom-left");
  map.on("error", (e) => { if (/tiles|style|Failed to fetch/i.test(String(e?.error?.message))) say("Some map tiles did not load. The site list still works."); });

  const match = (field: (x: (typeof CATS)[number]) => unknown, fallback: unknown) => ["match", ["get", "category"], ...CATS.flatMap((x) => [x.id, field(x)]), fallback];
  const tier = ["in", ["get", "name"], ["literal", BUILDING_TIER]];
  const pointFilter = (building: boolean) => ["all", ["==", ["geometry-type"], "Point"], building ? tier : ["!", tier], ["in", ["get", "category"], ["literal", visible]]];

  map.on("style.load", () => {
    const layers = map.getStyle().layers;
    const before = layers.find((l) => l.type === "symbol" && "source-layer" in l && l["source-layer"] === "place")?.id;
    map.addSource("dem", { type: "raster-dem", tiles: ["https://tiles.mapterhorn.com/{z}/{x}/{y}.webp"], encoding: "terrarium", tileSize: 512, maxzoom: 14, attribution: '<a href="https://mapterhorn.com/attribution">© Mapterhorn</a>' });
    map.addLayer({ id: "hillshade", type: "hillshade", source: "dem", paint: { "hillshade-exaggeration": 0.35, "hillshade-shadow-color": c("granite"), "hillshade-highlight-color": c("white"), "hillshade-accent-color": c("granite") } }, before);
    map.addSource("pm", { type: "geojson", data, attribution: 'Corridor data © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>, ODbL' });
    const isRing = ["==", ["geometry-type"], "Polygon"] as never;
    const join = { "line-join": "round", "line-cap": "round" } as const;
    map.addLayer({ id: "boundary-fill", type: "fill", source: "pm", filter: isRing, paint: { "fill-color": c("laser_violet"), "fill-opacity": 0.18 } }, before);
    map.addLayer({ id: "boundary-glow", type: "line", source: "pm", filter: isRing, layout: join, paint: { "line-color": c("laser_violet"), "line-width": 14, "line-blur": 6, "line-opacity": 0.45 } }, before);
    map.addLayer({ id: "boundary-casing", type: "line", source: "pm", filter: isRing, layout: join, paint: { "line-color": c("summit_night"), "line-width": 5.5, "line-opacity": 0.6 } }, before);
    map.addLayer({ id: "boundary-line", type: "line", source: "pm", filter: isRing, layout: join, paint: { "line-color": c("laser_violet"), "line-width": 3 } }, before);
    for (const id of BOUNDARY) map.setLayoutProperty(id, "visibility", boundaryOn ? "visible" : "none");
    const paint = {
      "circle-radius": ["interpolate", ["linear"], ["zoom"], 9, match((x) => (x.big ? 7 : 5), 5), 14, match((x) => (x.big ? 10 : 7.5), 7.5), 17, match((x) => (x.big ? 13 : 10), 10)],
      "circle-color": match((x) => c(x.fill), c("granite")),
      "circle-stroke-color": match((x) => c(x.stroke), c("white")),
      "circle-stroke-width": match((x) => x.ring, 1.5),
    } as never;
    map.addLayer({ id: "sites", type: "circle", source: "pm", filter: pointFilter(false) as never, paint });
    map.addLayer({ id: "sites-building", type: "circle", source: "pm", minzoom: TIER_ZOOM, filter: pointFilter(true) as never, paint });
    fit();
  });

  let popup: InstanceType<typeof gl.Popup> | null = null;
  const open = (f: Point) => {
    const p = f.properties ?? {};
    const el = document.createElement("div");
    const rows: [string, unknown][] = [["pop-cat", p.category], ["pop-name", p.name], ["pop-note", p.note]];
    for (const [cls, text] of rows) {
      const line = document.createElement("p");
      line.className = cls;
      line.textContent = String(text ?? "");
      el.append(line);
    }
    popup?.remove();
    popup = new gl.Popup({ offset: 12, maxWidth: "20rem" }).setLngLat(f.geometry.coordinates).setDOMContent(el).addTo(map);
  };
  for (const id of ["sites", "sites-building"]) {
    map.on("click", id, (e) => e.features?.[0] && open(e.features[0] as unknown as Point));
    map.on("mouseenter", id, () => (map.getCanvas().style.cursor = "pointer"));
    map.on("mouseleave", id, () => (map.getCanvas().style.cursor = ""));
  }

  function fit() {
    const b = new gl.LngLatBounds();
    for (const xy of ring.geometry.coordinates[0]) b.extend(xy);
    map.fitBounds(b, { padding: 36, duration: 600 });
  }

  // Resolve once the style is in and the corridor layers sit on it (the style.load handler above runs first);
  // tiles stream in after. A tile or source error is never fatal. Only a style or network failure before
  // then, or 20 seconds with no style, rejects: the map is removed and the page keeps its poster.
  let styled = false;
  await new Promise<void>((resolve, reject) => {
    const fail = (err: unknown) => {
      if (styled) return;
      styled = true;
      clearTimeout(timer);
      map.remove();
      reject(err instanceof Error ? err : new Error("the map could not draw"));
    };
    const timer = setTimeout(() => fail(new Error("the map took too long to load")), 20_000);
    map.once("style.load", () => { if (styled) return; styled = true; clearTimeout(timer); resolve(); });
    map.on("error", (e: { error?: unknown; sourceId?: string; tile?: unknown }) => { if (!e.sourceId && !e.tile) fail(e.error); });
  });

  return {
    filter(cats, boundary) {
      visible = cats;
      boundaryOn = boundary;
      if (map.getLayer("sites")) {
        map.setFilter("sites", pointFilter(false) as never);
        map.setFilter("sites-building", pointFilter(true) as never);
      }
      for (const id of BOUNDARY) if (map.getLayer(id)) map.setLayoutProperty(id, "visibility", boundary ? "visible" : "none");
    },
    flyTo(name) {
      const f = points.find((x) => x.properties?.name === name);
      if (!f) return;
      const building = BUILDING_TIER.includes(name);
      map.flyTo({ center: f.geometry.coordinates, zoom: Math.max(map.getZoom(), building ? TIER_ZOOM + 1 : 12.5), speed: 1.4 });
      open(f);
    },
    fit,
  };
}

