import { expect, test } from "@playwright/test";

test.describe("the explorer", () => {
  test("shows every record, and each town chip's count is what it shows", async ({ page }) => {
    await page.goto("/explore/");
    const cards = page.locator("[data-cards] > li");
    const total = await cards.count();
    await expect(page.locator("[data-shown]")).toHaveText(`Showing all ${total}`);
    const chip = page.locator(".chip[data-key=town][data-val=golden]");
    const n = Number(await chip.locator(".cn").textContent());
    await chip.click();
    await expect(chip).toHaveAttribute("aria-pressed", "true");
    await expect(page.locator("[data-cards] > li:not([hidden])")).toHaveCount(n);
    await expect(page).toHaveURL(/town=golden/);
  });

  test("opens filtered from a home-page link", async ({ page }) => {
    await page.goto("/explore/?segment=lasers");
    await expect(page.locator(".chip[data-key=segment][data-val=lasers]")).toHaveAttribute("aria-pressed", "true");
    for (const c of await page.locator("[data-cards] > li:not([hidden])").all()) await expect(c).toHaveAttribute("data-segment", "lasers");
  });

  test("searches by text, and every visible card links its source", async ({ page }) => {
    await page.goto("/explore/");
    await page.getByLabel("Search").fill("NIST");
    const visible = page.locator("[data-cards] > li:not([hidden])");
    expect(await visible.count()).toBeGreaterThan(0);
    for (const c of await visible.all()) await expect(c.locator("a.src")).toHaveAttribute("href", /^https?:\/\//);
  });
});
