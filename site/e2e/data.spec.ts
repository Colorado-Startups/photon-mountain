import { expect, test } from "@playwright/test";

test.describe("the data page", () => {
  test("links every data file and every text twin, and each one answers", async ({ page, request }) => {
    await page.goto("/data/");
    const hrefs = await page.locator("table a, .texts a").evaluateAll((as) => as.map((a) => a.getAttribute("href") ?? ""));
    expect(hrefs).toHaveLength(6 + 2 + 5);
    for (const href of hrefs) expect((await request.get(href)).status(), href).toBe(200);
  });

  test("copies the prompt, which points at llms-full.txt", async ({ page, context }) => {
    await context.grantPermissions(["clipboard-read", "clipboard-write"]);
    await page.goto("/data/");
    await expect(page.locator("#prompt-text")).toContainText("/llms-full.txt");
    await page.getByRole("button", { name: "Copy the prompt" }).click();
    await expect(page.getByRole("status")).toHaveText("Copied. Paste it into your assistant.");
    expect(await page.evaluate(() => navigator.clipboard.readText())).toContain("/llms-full.txt");
  });
});
