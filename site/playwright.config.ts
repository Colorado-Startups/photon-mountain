import { defineConfig, devices } from "@playwright/test";

// End-to-end checks against the built site (site/dist) and its Worker, at desktop and phone width. CI runs them in the
// standard job after `npm run build`; nothing here runs on the Mac (rules/compute.md).
export default defineConfig({
  testDir: "e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: "line",
  use: { baseURL: "http://127.0.0.1:3305" },
  // wrangler dev serves dist/ through the real Worker, assets config and _headers, so /mcp is tested too.
  webServer: {
    command: "npx wrangler dev --ip 127.0.0.1 --port 3305",
    env: { WRANGLER_SEND_METRICS: "false" },
    url: "http://127.0.0.1:3305/",
    reuseExistingServer: false,
    timeout: 60_000,
  },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"] } },
    { name: "phone", use: { ...devices["Pixel 7"] } },
  ],
});
