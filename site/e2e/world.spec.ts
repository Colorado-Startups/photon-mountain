import { expect, test } from "@playwright/test";

test("the world page labels every picture and clip AI-made and names what each painting kept", async ({ page }) => {
  await page.goto("/world/");
  const figures = page.locator("figure");
  await expect(figures).toHaveCount(5);
  for (const f of await figures.all()) await expect(f.locator("figcaption")).toContainText("AI-made");
  await expect(page.locator(".gallery figcaption")).toHaveCount(3);
  for (const c of await page.locator(".gallery figcaption").all()) await expect(c).toContainText("Kept:");
  await expect(page.locator(".loop video")).toHaveAttribute("controls", "");
});

test("the Golden painting credits its CC BY photographer", async ({ page }) => {
  await page.goto("/world/");
  await expect(page.locator(".gallery figcaption", { hasText: "Golden" })).toContainText("James St. John, CC BY 2.0");
});
