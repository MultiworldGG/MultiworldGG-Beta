import * as fs from "fs/promises";
import * as os from "os";
import * as path from "path";
import { shapeOrphan, readManifest } from "../src/shape-orphan";

const TEMPLATES_DIR = path.join(__dirname, "..", "src", "templates");

async function makeFixture(): Promise<{ cloneDir: string; outDir: string; cleanup: () => Promise<void> }> {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "shape-orphan-test-"));
  const cloneDir = path.join(root, "clone");
  const outDir = path.join(root, "out");
  await fs.mkdir(path.join(cloneDir, "worlds", "clique"), { recursive: true });
  await fs.writeFile(
    path.join(cloneDir, "worlds", "clique", "archipelago.json"),
    JSON.stringify({
      game: "Clique",
      world_version: "1.2.3",
      authors: ["Berserker"],
    }),
  );
  await fs.writeFile(
    path.join(cloneDir, "worlds", "clique", "__init__.py"),
    "# clique world stub\n",
  );
  return {
    cloneDir,
    outDir,
    cleanup: () => fs.rm(root, { recursive: true, force: true }),
  };
}

describe("shape-orphan", () => {
  it("readManifest reads the required fields", async () => {
    const f = await makeFixture();
    try {
      const m = await readManifest(f.cloneDir, "clique");
      expect(m.game).toBe("Clique");
      expect(m.world_version).toBe("1.2.3");
      expect(m.authors).toEqual(["Berserker"]);
    } finally {
      await f.cleanup();
    }
  });

  it("readManifest throws when required fields are missing", async () => {
    const root = await fs.mkdtemp(path.join(os.tmpdir(), "shape-orphan-bad-"));
    const cloneDir = path.join(root, "clone");
    await fs.mkdir(path.join(cloneDir, "worlds", "broken"), { recursive: true });
    await fs.writeFile(
      path.join(cloneDir, "worlds", "broken", "archipelago.json"),
      JSON.stringify({ game: "Broken" }),
    );
    try {
      await expect(readManifest(cloneDir, "broken")).rejects.toThrow();
    } finally {
      await fs.rm(root, { recursive: true, force: true });
    }
  });

  it("shapeOrphan produces pyproject.toml, README.md, and copies worlds/<slug>/", async () => {
    const f = await makeFixture();
    try {
      const manifest = await readManifest(f.cloneDir, "clique");
      await shapeOrphan({
        slug: "clique",
        manifest,
        cloneDir: f.cloneDir,
        outDir: f.outDir,
        templatesDir: TEMPLATES_DIR,
      });

      const pyproject = await fs.readFile(path.join(f.outDir, "pyproject.toml"), "utf-8");
      expect(pyproject).toContain('name = "worlds_clique"');
      expect(pyproject).toContain('version = "1.2.3"');
      expect(pyproject).toContain('"Berserker"');

      const readme = await fs.readFile(path.join(f.outDir, "README.md"), "utf-8");
      expect(readme).toContain("Clique");
      expect(readme).toContain("1.2.3");

      const copied = await fs.readFile(
        path.join(f.outDir, "src", "worlds", "clique", "__init__.py"),
        "utf-8",
      );
      expect(copied).toBe("# clique world stub\n");
    } finally {
      await f.cleanup();
    }
  });
});
