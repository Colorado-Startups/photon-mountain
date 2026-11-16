// @ts-check
// photonmountain.co: a static Astro build served from Cloudflare Workers static assets (launch plan step 1.3).
import { defineConfig, fontProviders } from "astro/config";
import sitemap from "@astrojs/sitemap";

// Keep every hoisted <script> an external /_astro/*.js file, so the CSP in public/_headers can stay
// `script-src 'self'` with no 'unsafe-inline'. Non-JS assets keep Vite's default inlining.
const assetsInlineLimit = (/** @type {string} */ filePath) => (filePath.endsWith(".js") ? false : undefined);

export default defineConfig({
  site: "https://photonmountain.co",
  output: "static",
  trailingSlash: "always",
  // This Mac account's port block is 3300 to 3349 (managed Mac policy, Ports); strictPort exits if it is taken.
  server: { port: 3304 },
  vite: { build: { assetsInlineLimit }, server: { strictPort: true } },
  integrations: [sitemap()],
  // The three brand faces (01_doctrine/brand_identity.md), self-hosted at build time through Fontsource,
  // all SIL OFL 1.1. Astro sizes each fallback from the font's own metrics, so the swap moves little.
  fonts: [
    { provider: fontProviders.fontsource(), name: "Space Grotesk", cssVariable: "--font-display", weights: [500, 700], styles: ["normal"], subsets: ["latin"], fallbacks: ["system-ui", "sans-serif"] },
    { provider: fontProviders.fontsource(), name: "Inter", cssVariable: "--font-body", weights: [400, 500, 600], styles: ["normal"], subsets: ["latin"], fallbacks: ["system-ui", "sans-serif"] },
    { provider: fontProviders.fontsource(), name: "Space Mono", cssVariable: "--font-mono", weights: [400, 700], styles: ["normal"], subsets: ["latin"], fallbacks: ["ui-monospace", "monospace"] },
  ],
});
