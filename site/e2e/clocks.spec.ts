import { expect, test } from "@playwright/test";

test("keeps the three clocks apart and filters to one", async ({ page }) => {
  await page.goto("/");
  const section = page.locator("[data-section=clocks]");
  await expect(section.locator("[data-lane]")).toHaveCount(3);
  await section.getByRole("button", { name: "Targeted for 2026" }).click();
  await expect(section.locator("[data-lane=today]")).toBeHidden();
  await expect(section.locator("[data-lane='2026']")).toBeVisible();
  await expect(section.locator("[data-lane='2026']")).toContainText("Arvada");
  await section.getByRole("button", { name: "All" }).click();
  await expect(section.locator("[data-lane=horizon]")).toBeVisible();
});
