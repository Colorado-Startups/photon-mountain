import { defineConfig, devices } from "@playwright/test";

// End-to-end checks against the built site (site/dist), at desktop and phone width. CI runs them in the
// standard job after `npm run build`; nothing here runs on the Mac (rules/compute.md).
export default defineConfig({
  testDir: "e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: "line",
  use: { baseURL: "http://127.0.0.1:3305" },
  webServer: {
    command: "npx astro preview --host 127.0.0.1 --port 3305",
    url: "http://127.0.0.1:3305/",
    reuseExistingServer: false,
    timeout: 60_000,
  },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"] } },
    { name: "phone", use: { ...devices["Pixel 7"] } },
  ],
});
