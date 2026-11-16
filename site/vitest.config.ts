import { defineConfig } from "vitest/config";

// Unit tests for the site's own logic. Coverage writes lcov, which Git Crafter's code tab reads.
export default defineConfig({
  test: {
    include: ["src/**/*.test.ts"],
    coverage: { provider: "v8", reporter: ["text-summary", "lcov"], include: ["src/ai/**", "src/data/**", "src/lib/**", "src/mcp/**", "src/worker.ts"], exclude: ["**/*.test.ts"] },
  },
});
