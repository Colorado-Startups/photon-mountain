import { expect, test } from "@playwright/test";

test.describe("the home page", () => {
  test("keeps the painting still under reduced motion, and plays and pauses on request", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto("/");
    const frame = page.locator("[data-loop]");
    await page.waitForLoadState("load");
    await expect(frame.locator("video")).toBeHidden();
    await expect(frame.locator("picture img")).toBeVisible();
    const button = frame.getByRole("button", { name: "Play the light" });
    await button.click();
    await expect(frame.getByRole("button", { name: "Pause the light" })).toHaveAttribute("aria-pressed", "true");
    await frame.getByRole("button", { name: "Pause the light" }).click();
    await expect(frame.getByRole("button", { name: "Play the light" })).toHaveAttribute("aria-pressed", "false");
  });

  test("loads no video bytes before the page is done under reduced motion", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "reduce" });
    const media: string[] = [];
    page.on("request", (r) => { if (/\.(webm|mp4)$/.test(r.url())) media.push(r.url()); });
    await page.goto("/");
    await page.waitForLoadState("networkidle");
    expect(media).toEqual([]);
  });

  test("shows every counter with a source line, and labels every painting AI-made", async ({ page }) => {
    await page.goto("/");
    const counters = page.getByRole("list", { name: "The corridor in numbers" }).locator("li");
    await expect(counters).toHaveCount(6);
    for (const li of await counters.all()) {
      await expect(li.locator(".n")).not.toBeEmpty();
      await expect(li.locator(".s")).not.toBeEmpty();
    }
    const captions = page.locator("figure figcaption");
    for (const c of await captions.all()) await expect(c).toContainText("AI-made");
  });

  test("shows the four towns, with Arvada's fab on the 2026 clock", async ({ page }) => {
    await page.goto("/");
    const towns = page.locator("[data-section=towns] h3");
    await expect(towns).toHaveText(["Boulder", "Golden", "Arvada", "Denver"]);
    await expect(page.locator("[data-section=towns] .clock")).toContainText("targeted for 2026");
  });
});
