import { expect, test } from "@playwright/test";

test.describe("the map page", () => {
  test("lists all 53 sites, counts each category, and filters the list and the poster", async ({ page }) => {
    await page.goto("/map/");
    await expect(page.locator("[data-sites] li")).toHaveCount(53);
    const counts = await page.locator("[data-legend] [data-cat] ~ .count").allTextContents();
    expect(counts.map(Number).reduce((a, b) => a + b, 0)).toBe(53);
    const box = page.locator("[data-legend] input[data-cat='Transit Station']");
    const transit = page.locator("[data-sites] li[data-cat='Transit Station']");
    await expect(transit.first()).toBeVisible();
    await box.uncheck();
    await expect(transit.first()).toBeHidden();
    await expect(page.locator(".poster circle[data-cat='Transit Station']").first()).toHaveClass(/off/);
  });

  test("draws the poster without asking any tile server", async ({ page }) => {
    const tiles: string[] = [];
    page.on("request", (r) => { if (/openfreemap|mapterhorn/.test(r.url())) tiles.push(r.url()); });
    await page.goto("/map/");
    await page.waitForLoadState("networkidle");
    await expect(page.locator("svg.poster path.ring")).toBeVisible();
    expect(tiles).toEqual([]);
  });

  test("credits OpenStreetMap", async ({ page }) => {
    await page.goto("/map/");
    await expect(page.locator(".credits")).toContainText("OpenStreetMap contributors");
  });
});

test("a site in the list lights its dot on the poster", async ({ page }) => {
  await page.goto("/map/");
  const first = page.locator("[data-sites] button[data-site]:not([data-building])").first();
  const name = await first.getAttribute("data-site");
  await first.click();
  await expect(first).toHaveAttribute("aria-pressed", "true");
  await expect(page.locator(`.poster .dot[data-name="${name}"]`)).toHaveClass(/on/);
});
