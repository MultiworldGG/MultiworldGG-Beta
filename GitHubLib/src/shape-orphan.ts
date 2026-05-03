import * as fs from "fs/promises";
import * as path from "path";
import Handlebars from "handlebars";

export interface Manifest {
  game: string;
  world_version: string;
  authors: string[];
  [k: string]: unknown;
}

export async function readManifest(cloneDir: string, slug: string): Promise<Manifest> {
  const manifestPath = path.join(cloneDir, "worlds", slug, "archipelago.json");
  const raw = await fs.readFile(manifestPath, "utf-8");
  const parsed = JSON.parse(raw);
  const game = parsed.game;
  const world_version = parsed.world_version;
  const authors = parsed.authors;
  if (typeof game !== "string" || typeof world_version !== "string" || !Array.isArray(authors)) {
    throw new Error(
      `worlds/${slug}/archipelago.json missing required fields: game (string), world_version (string), authors (array)`,
    );
  }
  return { ...parsed, game, world_version, authors };
}

export interface ShapeContext {
  slug: string;
  manifest: Manifest;
  cloneDir: string;
  outDir: string;
  templatesDir: string;
}

export async function shapeOrphan(ctx: ShapeContext): Promise<void> {
  await fs.mkdir(ctx.outDir, { recursive: true });

  const worldSrc = path.join(ctx.cloneDir, "worlds", ctx.slug);
  const worldDest = path.join(ctx.outDir, "src", "worlds", ctx.slug);
  await fs.mkdir(path.dirname(worldDest), { recursive: true });
  await copyDir(worldSrc, worldDest);

  const callerPyproject = path.join(worldSrc, "pyproject.toml");
  let pyprojectContent: string;
  if (await fileExists(callerPyproject)) {
    pyprojectContent = await fs.readFile(callerPyproject, "utf-8");
    pyprojectContent = injectIfMissing(pyprojectContent, "version", `"${ctx.manifest.world_version}"`);
    pyprojectContent = injectIfMissing(
      pyprojectContent,
      "authors",
      `[${ctx.manifest.authors.map((a) => `{ name = "${escapeToml(a)}" }`).join(", ")}]`,
    );
  } else {
    pyprojectContent = await render(path.join(ctx.templatesDir, "pyproject.toml.hbs"), {
      slug: ctx.slug,
      ...ctx.manifest,
    });
  }
  await fs.writeFile(path.join(ctx.outDir, "pyproject.toml"), pyprojectContent);

  const readmeContent = await render(path.join(ctx.templatesDir, "README.md.hbs"), {
    slug: ctx.slug,
    ...ctx.manifest,
  });
  await fs.writeFile(path.join(ctx.outDir, "README.md"), readmeContent);
}

async function render(templatePath: string, ctx: object): Promise<string> {
  const tmpl = Handlebars.compile(await fs.readFile(templatePath, "utf-8"));
  return tmpl(ctx);
}

function injectIfMissing(toml: string, key: string, valueExpr: string): string {
  const re = new RegExp(`^\\s*${key}\\s*=`, "m");
  if (re.test(toml)) return toml;
  return toml.replace(/\[project\]/, `[project]\n${key} = ${valueExpr}`);
}

async function fileExists(p: string): Promise<boolean> {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

async function copyDir(src: string, dest: string): Promise<void> {
  await fs.mkdir(dest, { recursive: true });
  const entries = await fs.readdir(src, { withFileTypes: true });
  for (const e of entries) {
    const s = path.join(src, e.name);
    const d = path.join(dest, e.name);
    if (e.isDirectory()) {
      await copyDir(s, d);
    } else if (e.isFile()) {
      await fs.copyFile(s, d);
    }
  }
}

function escapeToml(s: string): string {
  return s.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}
