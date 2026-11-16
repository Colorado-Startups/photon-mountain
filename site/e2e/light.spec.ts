import { expect, test } from "@playwright/test";

test("the light diagram splits into information and energy and links each segment", async ({ page }) => {
  await page.goto("/");
  const light = page.locator("[data-section=light]");
  await expect(light.locator(".bname")).toHaveText(["Information", "Energy"]);
  const links = light.locator(".branch a");
  await expect(links).toHaveCount(7);
  for (const a of await links.all()) await expect(a).toHaveAttribute("href", /^\/explore\/\?segment=/);
});

test("the comparison draws Photon Mountain's core longer than Silicon Valley's", async ({ page }) => {
  await page.goto("/");
  const bars = page.locator("[data-section=versus] .bar");
  const [sv, pm] = await Promise.all([bars.nth(0).boundingBox(), bars.nth(1).boundingBox()]);
  expect(sv && pm && sv.width < pm.width).toBe(true);
});
