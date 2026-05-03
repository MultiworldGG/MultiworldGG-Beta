import type { Context } from "probot";

const INFRA_PREFIX = "_";
const EXCLUDE_SLUGS = new Set(["generic"]);

export type DiscoveryResult =
  | { kind: "ok"; slug: string; base: string }
  | { kind: "skip"; message: string; candidates: string[]; base: string; reason: "no_candidates" | "multiple_candidates" };

type Octokit = Context["octokit"];

type Base =
  | { kind: "compare"; ref: string }
  | { kind: "tree-scan" };

export async function discoverSlug(
  octokit: Octokit,
  owner: string,
  repo: string,
  tag: string,
): Promise<DiscoveryResult> {
  const base = await resolveBase(octokit, owner, repo, tag);

  let candidateSlugs: string[];
  if (base.kind === "compare") {
    candidateSlugs = await getChangedSlugsViaCompare(octokit, owner, repo, base.ref, tag);
  } else {
    candidateSlugs = await getSlugsViaTreeScan(octokit, owner, repo, tag);
  }

  const validatedSlugs: string[] = [];
  for (const slug of candidateSlugs) {
    if (await manifestExistsAtTag(octokit, owner, repo, tag, slug)) {
      validatedSlugs.push(slug);
    }
  }

  const baseRef = base.kind === "compare" ? base.ref : "(whole-tree scan)";

  if (validatedSlugs.length === 1) {
    return { kind: "ok", slug: validatedSlugs[0], base: baseRef };
  }
  if (validatedSlugs.length === 0) {
    return {
      kind: "skip",
      reason: "no_candidates",
      candidates: [],
      base: baseRef,
      message:
        `Oliver couldn't determine which world to publish from this release. The diff between \`${baseRef}\` and \`${tag}\` touched no \`worlds/<slug>/archipelago.json\`. ` +
        `If this release wasn't intended to publish a world, you can ignore this message. Otherwise, an Index maintainer has been notified to review.`,
    };
  }
  return {
    kind: "skip",
    reason: "multiple_candidates",
    candidates: validatedSlugs,
    base: baseRef,
    message:
      `Oliver detected changes in multiple worlds: ${validatedSlugs.map((s) => "`" + s + "`").join(", ")}. ` +
      `Please cut a separate release per world to publish them independently. (Pokémon Red and Pokémon Blue, for example, would be two releases at the same SHA.) An Index maintainer has been notified.`,
  };
}

async function resolveBase(octokit: Octokit, owner: string, repo: string, tag: string): Promise<Base> {
  const releases = await octokit.rest.repos.listReleases({ owner, repo, per_page: 10 });
  const list = releases.data;
  const idx = list.findIndex((r) => r.tag_name === tag);
  if (idx >= 0 && idx + 1 < list.length) {
    return { kind: "compare", ref: list[idx + 1].tag_name };
  }
  const repoInfo = await octokit.rest.repos.get({ owner, repo });
  if (repoInfo.data.fork && repoInfo.data.parent) {
    const parent = repoInfo.data.parent;
    return { kind: "compare", ref: `${parent.owner.login}:${parent.default_branch}` };
  }
  return { kind: "tree-scan" };
}

async function getChangedSlugsViaCompare(
  octokit: Octokit,
  owner: string,
  repo: string,
  base: string,
  head: string,
): Promise<string[]> {
  const cmp = await octokit.rest.repos.compareCommitsWithBasehead({
    owner,
    repo,
    basehead: `${base}...${head}`,
  });
  const slugs = new Set<string>();
  for (const f of cmp.data.files ?? []) {
    const m = /^worlds\/([^/]+)\//.exec(f.filename);
    if (!m) continue;
    const slug = m[1];
    if (slug.startsWith(INFRA_PREFIX) || EXCLUDE_SLUGS.has(slug)) continue;
    slugs.add(slug);
  }
  return [...slugs];
}

async function getSlugsViaTreeScan(
  octokit: Octokit,
  owner: string,
  repo: string,
  tag: string,
): Promise<string[]> {
  try {
    const res = await octokit.rest.repos.getContent({ owner, repo, path: "worlds", ref: tag });
    if (!Array.isArray(res.data)) return [];
    const out: string[] = [];
    for (const entry of res.data) {
      if (entry.type !== "dir") continue;
      const slug = entry.name;
      if (slug.startsWith(INFRA_PREFIX) || EXCLUDE_SLUGS.has(slug)) continue;
      out.push(slug);
    }
    return out;
  } catch {
    return [];
  }
}

async function manifestExistsAtTag(
  octokit: Octokit,
  owner: string,
  repo: string,
  tag: string,
  slug: string,
): Promise<boolean> {
  try {
    await octokit.rest.repos.getContent({
      owner,
      repo,
      path: `worlds/${slug}/archipelago.json`,
      ref: tag,
    });
    return true;
  } catch {
    return false;
  }
}
