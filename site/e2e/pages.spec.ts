import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";
import { routes } from "./routes";

for (const path of routes) {
  test(`${path} renders one h1, a main landmark and no axe violations`, async ({ page }) => {
    const res = await page.goto(path);
    expect(res?.status()).toBeLessThan(400);
    await expect(page.locator("h1")).toHaveCount(1);
    await expect(page.locator("main#main")).toBeVisible();
    const axe = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]).analyze();
    expect(axe.violations.map((v) => `${v.id}: ${v.nodes.length}`)).toEqual([]);
  });
}

test("the footer carries the endorsement line, then the joint effort", async ({ page }) => {
  await page.goto("/");
  const lines = page.locator("footer .line");
  await expect(lines.nth(0)).toHaveText("a Colorado Startups project");
  await expect(lines.nth(0).locator("a")).toHaveAttribute("href", "https://coloradostartups.org/");
  await expect(lines.nth(1)).toHaveText("A joint effort with Colorado Compute");
});

test("a missing page answers 404 with the site's own page", async ({ page }) => {
  const res = await page.goto("/no-such-page/");
  expect(res?.status()).toBe(404);
  await expect(page.locator("h1")).toHaveText("That page is off the map.");
});

test("the data files parse and hold the whole record", async ({ request }) => {
  const sites = await (await request.get("/data/sites.json")).json();
  expect(sites.count).toBe(53);
  expect(sites.license).toBe("ODbL-1.0");
  const companies = await (await request.get("/data/companies.json")).json();
  expect(companies.count).toBe(companies.companies.length);
  const csv = await (await request.get("/data/companies.csv")).text();
  expect(csv.trimEnd().split("\r\n")).toHaveLength(companies.count + 1);
  const figures = await (await request.get("/data/figures.json")).json();
  for (const f of figures.figures) expect(f.source).toMatch(/^https:\/\//);
});
