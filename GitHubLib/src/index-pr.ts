import type { ProbotOctokit } from "probot";

import { fetchWheelManifest } from "./wheel-manifest";

export interface IndexBotData {
  id: number;
  client_id: string;
  slug: string;
  owner: object;
  name: string;
  description: string;
  external_url: string;
  html_url: string;
  created_at: string;
  updated_at: string;
  permissions: object;
  events: string[];
  installations_count: number;
}

export interface IndexPROpts {
  karenOctokit: ProbotOctokit;   // Contents:Write - branch, manifest commits, CODEOWNERS
  oliverOctokit: ProbotOctokit;  // Pull requests:Write + Issues:Write - opens/updates the PR, applies labels
  karenData: IndexBotData;
  oliverData: IndexBotData;
  indexOwner: string;
  indexName: string;
  sourceOwner: string;
  sourceRepo: string;
  slug: string;
  releaseTag: string;
  // Fully-formed release-asset wheel URL to pin as module_location; computed by
  // the caller so this module doesn't know the action's output shape.
  moduleLocation: string;
  // Wheel filename + size in bytes, surfaced in the PR body for reviewers.
  wheelAssetName: string;
  wheelAssetSize: number;
  // Parsed worlds/<slug>/archipelago.json at the release SHA; author-canonical
  // except module_location and igdb_id (see mergeWorldManifest). {} when
  // missing/unreadable - Karen's schema check surfaces the bad PR.
  sourceManifest: Record<string, unknown>;
}

export interface IndexPRResult {
  prNumber: number;
  branchName: string;
  created: boolean;
  worldIsNew: boolean;
  codeownersConflictWith: string | null;
}

const NEW_WORLD_LABEL = "New APWorld";
const UPDATE_WORLD_LABEL = "APWorld Update";
const NEEDS_IGDB_ID_LABEL = "Needs IGDB id";
const CODEOWNERS_PATH = ".github/CODEOWNERS";

export async function openOrUpdateIndexPR(opts: IndexPROpts): Promise<IndexPRResult> {
  const {
    karenOctokit,
    oliverOctokit,
    karenData,
    oliverData,
    indexOwner,
    indexName,
    sourceOwner,
    sourceRepo,
    slug,
    releaseTag,
    moduleLocation,
    wheelAssetName,
    wheelAssetSize,
    sourceManifest,
  } = opts;

  const branchName = `update/${slug}-${releaseTag}`;
  const filePath = `worlds/${slug}.json`;

  const repoInfo = await karenOctokit.rest.repos.get({ owner: indexOwner, repo: indexName });
  const defaultBranch = repoInfo.data.default_branch;

  const worldIsNew = !(await fileExistsOnRef(karenOctokit, indexOwner, indexName, filePath, defaultBranch));

  const baseRef = await karenOctokit.rest.git.getRef({
    owner: indexOwner,
    repo: indexName,
    ref: `heads/${defaultBranch}`,
  });
  const baseSha = baseRef.data.object.sha;

  await ensureBranch(karenOctokit, indexOwner, indexName, branchName, baseSha);

  const { json: currentJson, sha: currentSha } = await readJsonOnBranch(
    karenOctokit,
    indexOwner,
    indexName,
    filePath,
    branchName,
  );

  const updated = mergeWorldManifest(sourceManifest, currentJson, moduleLocation, wheelAssetSize);

  const newContent = JSON.stringify(updated, null, 2) + "\n";
  const encodedContent = Buffer.from(newContent, "utf-8").toString("base64");

  await karenOctokit.rest.repos.createOrUpdateFileContents({
    owner: indexOwner,
    repo: indexName,
    path: filePath,
    branch: branchName,
    message: `[${slug}] Update to ${releaseTag}`,
    content: encodedContent,
    sha: currentSha,
  });

  let codeownersConflictWith: string | null = null;
  if (worldIsNew) {
    codeownersConflictWith = await appendCodeownersForNewWorld({
      karenOctokit,
      indexOwner,
      indexName,
      branchName,
      slug,
      codeowner: deriveCodeownerHandle(sourceOwner),
    });
  }

  const existingPRs = await oliverOctokit.rest.pulls.list({
    owner: indexOwner,
    repo: indexName,
    head: `${indexOwner}:${branchName}`,
    state: "open",
  });

  // The manifest's display name lives in `game` (the author's archipelago.json
  // field); fall back to the slug so the PR body is never blank.
  const gameName = typeof updated.game === "string" ? updated.game : slug;
  const prBody = [
    `Hey folks, I found a new update for ${gameName}. I'm gonna grab some info on it for y'all.`,
    ``,
    `**APWorld:** \`${slug}\``,
    `**Location:** \`${sourceOwner}/${sourceRepo}@${releaseTag}\``,
    `**Release tag:** \`${releaseTag}\``,
    `**Wheel:** \`${wheelAssetName}\` (${formatWheelSize(wheelAssetSize)})`,
    `**New module_location:** \`${moduleLocation}\``,
    ``,
    `${karenData.name}[bot](${karenData.html_url}) is gathering the manifest for ${gameName} and cross referencing. She'll review in a moment.`,
  ].join("\n");

  let prNumber: number;
  let created: boolean;
  if (existingPRs.data.length === 0) {
    const createdPR = await oliverOctokit.rest.pulls.create({
      owner: indexOwner,
      repo: indexName,
      title: `[${slug}] Update to ${releaseTag}`,
      head: branchName,
      base: defaultBranch,
      body: prBody,
    });
    prNumber = createdPR.data.number;
    created = true;

    // Auto-squash-merge once the org-ruleset gates clear. Best-effort: an error
    // here must not crash the handler; review + manual merge still work.
    try {
      await oliverOctokit.graphql(
        `mutation($prId: ID!) {
           enablePullRequestAutoMerge(input: { pullRequestId: $prId, mergeMethod: SQUASH }) {
             pullRequest { id }
           }
         }`,
        { prId: createdPR.data.node_id },
      );
    } catch (err) {
      // eslint-disable-next-line no-console
      console.warn(
        `[oliver] enablePullRequestAutoMerge failed for #${prNumber}: ${(err as Error).message}`,
      );
    }
  } else {
    const existing = existingPRs.data[0];
    await oliverOctokit.rest.pulls.update({
      owner: indexOwner,
      repo: indexName,
      pull_number: existing.number,
      body: prBody,
    });
    prNumber = existing.number;
    created = false;
  }

  const labels = [worldIsNew ? NEW_WORLD_LABEL : UPDATE_WORLD_LABEL];
  if (!("igdb_id" in updated)) {
    labels.push(NEEDS_IGDB_ID_LABEL);
  }
  await oliverOctokit.rest.issues.addLabels({
    owner: indexOwner,
    repo: indexName,
    issue_number: prNumber,
    labels,
  });

  return { prNumber, branchName, created, worldIsNew, codeownersConflictWith };
}

export interface BundleWorld {
  slug: string;
  moduleLocation: string;
  wheelAssetName: string;
  wheelAssetSize: number;
}

export interface BundleIndexPROpts {
  // Same split as the single-world path: Karen (Contents:Write) creates the
  // branch and commits the manifests; Oliver opens and labels the PR.
  karenOctokit: ProbotOctokit;
  oliverOctokit: ProbotOctokit;
  karenData: IndexBotData;
  oliverData: IndexBotData;
  indexOwner: string;
  indexName: string;
  // Bundle source is the Beta monorepo, owned by the org (not a per-world author).
  sourceOwner: string;
  sourceRepo: string;
  // `worlds-wheels-<date>` tag of the bundled release.
  releaseTag: string;
  // One entry per changed world's wheel; caller guarantees length >= 1.
  worlds: BundleWorld[];
  // Read a world's archipelago.json out of its wheel (injected in tests). Null
  // means skip that world - the only skip reason.
  fetchManifest?: (moduleLocation: string, slug: string) => Promise<Record<string, unknown> | null>;
}

export interface BundleIndexPRResult {
  opened: boolean;
  prNumber: number;
  branchName: string;
  created: boolean;
  updatedWorldSlugs: string[];
  // Bundled worlds whose wheel carried no archipelago.json (nothing to seed from).
  skippedSlugs: string[];
}

// One combined Index PR for a bundled release: each world's manifest is seeded
// from the archipelago.json inside its wheel (new worlds included), merged via
// mergeWorldManifest. Karen commits; Oliver opens and labels.
export async function openOrUpdateBundleIndexPR(opts: BundleIndexPROpts): Promise<BundleIndexPRResult> {
  const {
    karenOctokit,
    oliverOctokit,
    karenData,
    oliverData,
    indexOwner,
    indexName,
    sourceOwner,
    sourceRepo,
    releaseTag,
    worlds,
  } = opts;
  const fetchManifest = opts.fetchManifest ?? fetchWheelManifest;

  const branchName = `update/${releaseTag}`;

  const repoInfo = await karenOctokit.rest.repos.get({ owner: indexOwner, repo: indexName });
  const defaultBranch = repoInfo.data.default_branch;

  // Plan each world from its wheel's archipelago.json. Existing manifests are
  // read from main (not the PR branch) so every run is self-healing: a prior
  // bad branch commit is overwritten.
  const planned: Array<{
    slug: string;
    wheelAssetName: string;
    wheelAssetSize: number;
    content: string;
    needsIgdb: boolean;
    isNew: boolean;
  }> = [];
  const skippedSlugs: string[] = [];
  for (const w of worlds) {
    const sourceManifest = await fetchManifest(w.moduleLocation, w.slug);
    if (sourceManifest === null) {
      skippedSlugs.push(w.slug);
      continue;
    }
    // Existing Index manifest (for igdb_id + indentation); absent/malformed → {}.
    let raw: string | null = null;
    try {
      const f = await karenOctokit.rest.repos.getContent({
        owner: indexOwner,
        repo: indexName,
        path: `worlds/${w.slug}.json`,
        ref: defaultBranch,
      });
      if (!Array.isArray(f.data) && f.data.type === "file") {
        raw = Buffer.from(f.data.content, f.data.encoding as BufferEncoding).toString("utf-8");
      }
    } catch {
      // 404 → brand-new world (seed it from the wheel).
    }
    let currentJson: Record<string, unknown> = {};
    if (raw !== null) {
      try {
        currentJson = JSON.parse(raw) as Record<string, unknown>;
      } catch {
        currentJson = {}; // malformed existing manifest: the wheel is canonical
      }
    }
    const merged = mergeWorldManifest(sourceManifest, currentJson, w.moduleLocation, w.wheelAssetSize);
    planned.push({
      slug: w.slug,
      wheelAssetName: w.wheelAssetName,
      wheelAssetSize: w.wheelAssetSize,
      // Preserve an existing manifest's indentation (small update diff); a new
      // world matches the single-world path's two-space style.
      content: JSON.stringify(merged, null, raw !== null ? detectJsonIndent(raw) : 2) + "\n",
      needsIgdb: !("igdb_id" in merged),
      isNew: raw === null,
    });
  }
  if (planned.length === 0) {
    return { opened: false, prNumber: 0, branchName, created: false, updatedWorldSlugs: [], skippedSlugs };
  }

  const baseRef = await karenOctokit.rest.git.getRef({
    owner: indexOwner,
    repo: indexName,
    ref: `heads/${defaultBranch}`,
  });
  const baseSha = baseRef.data.object.sha;

  await ensureBranch(karenOctokit, indexOwner, indexName, branchName, baseSha);

  let anyNeedsIgdb = false;
  const bodyWorldLines: string[] = [];
  for (const p of planned) {
    const filePath = `worlds/${p.slug}.json`;
    if (p.needsIgdb) anyNeedsIgdb = true;
    await karenOctokit.rest.repos.createOrUpdateFileContents({
      owner: indexOwner,
      repo: indexName,
      path: filePath,
      branch: branchName,
      message: `[${p.slug}] Update to ${releaseTag}`,
      content: Buffer.from(p.content, "utf-8").toString("base64"),
      sha: await shaOnRef(karenOctokit, indexOwner, indexName, filePath, branchName),
    });
    bodyWorldLines.push(`- \`${p.slug}\`: \`${p.wheelAssetName}\` (${formatWheelSize(p.wheelAssetSize)})`);
  }

  const updatedWorldSlugs = planned.map((p) => p.slug);

  const existingPRs = await oliverOctokit.rest.pulls.list({
    owner: indexOwner,
    repo: indexName,
    head: `${indexOwner}:${branchName}`,
    state: "open",
  });

  const prBody = [
    `Hey folks, I found a bunch of new updates for ${updatedWorldSlugs.length} worlds. I'm gonna grab some info on them for y'all.`,
    ``,
    `**Location:** \`${sourceOwner}/${sourceRepo}@${releaseTag}\``,
    `**Release tag:** \`${releaseTag}\``,
    `**APWorlds:** ${updatedWorldSlugs.map((s) => `\`${s}\``).join(", ")}`,
    ...(skippedSlugs.length ? [`**Skipped (no archipelago.json in wheel):** ${skippedSlugs.join(", ")}`] : []),
    ``,
    ...bodyWorldLines,
    ``,
    `${karenData.name} [bot](${karenData.html_url}) is gathering the manifests for ${updatedWorldSlugs.length} worlds and cross referencing. She'll review them individually in a moment.`,
  ].join("\n");

  let prNumber: number;
  let created: boolean;
  if (existingPRs.data.length === 0) {
    const createdPR = await oliverOctokit.rest.pulls.create({
      owner: indexOwner,
      repo: indexName,
      title: `[bundle] Update ${updatedWorldSlugs.length} world${updatedWorldSlugs.length === 1 ? "" : "s"} (${releaseTag})`,
      head: branchName,
      base: defaultBranch,
      body: prBody,
    });
    prNumber = createdPR.data.number;
    created = true;

    try {
      await oliverOctokit.graphql(
        `mutation($prId: ID!) {
           enablePullRequestAutoMerge(input: { pullRequestId: $prId, mergeMethod: SQUASH }) {
             pullRequest { id }
           }
         }`,
        { prId: createdPR.data.node_id },
      );
    } catch (err) {
      // eslint-disable-next-line no-console
      console.warn(
        `[oliver] enablePullRequestAutoMerge failed for #${prNumber}: ${(err as Error).message}`,
      );
    }
  } else {
    const existing = existingPRs.data[0];
    await oliverOctokit.rest.pulls.update({
      owner: indexOwner,
      repo: indexName,
      pull_number: existing.number,
      body: prBody,
    });
    prNumber = existing.number;
    created = false;
  }

  const labels: string[] = [];
  if (planned.some((p) => p.isNew)) labels.push(NEW_WORLD_LABEL);
  if (planned.some((p) => !p.isNew)) labels.push(UPDATE_WORLD_LABEL);
  if (anyNeedsIgdb) labels.push(NEEDS_IGDB_ID_LABEL);
  await oliverOctokit.rest.issues.addLabels({
    owner: indexOwner,
    repo: indexName,
    issue_number: prNumber,
    labels,
  });

  return { opened: true, prNumber, branchName, created, updatedWorldSlugs, skippedSlugs };
}

// Preserve the existing manifest's indentation so a bundle update is a one-line
// diff (only module_location changes). Falls back to two-space.
function detectJsonIndent(raw: string): string | number {
  const m = raw.match(/\n([ \t]+)"/);
  return m ? m[1] : 2;
}

function formatWheelSize(bytes: number): string {
  if (!Number.isFinite(bytes) || bytes < 0) return `${bytes} bytes`;
  if (bytes < 1024) return `${bytes} B`;
  const kb = bytes / 1024;
  if (kb < 1024) return `${kb.toFixed(kb < 10 ? 1 : 0)} KB`;
  const mb = kb / 1024;
  return `${mb.toFixed(mb < 10 ? 2 : 1)} MB`;
}

/** True for the 422 GitHub returns when `createRef` targets an existing ref. */
function isRefAlreadyExists(err: unknown): boolean {
  const e = err as { status?: number; message?: string };
  return e?.status === 422 && /reference already exists/i.test(e?.message ?? "");
}

/**
 * Ensure `branchName` exists, creating it at `baseSha` if not.
 * Create-then-tolerate-422, not check-then-create: dual release deliveries race
 * here. The branch is never reset onto baseSha, so an open PR keeps its history.
 */
async function ensureBranch(
  octokit: ProbotOctokit,
  owner: string,
  repo: string,
  branchName: string,
  baseSha: string,
): Promise<void> {
  try {
    await octokit.rest.git.createRef({
      owner,
      repo,
      ref: `refs/heads/${branchName}`,
      sha: baseSha,
    });
  } catch (err: unknown) {
    if (!isRefAlreadyExists(err)) throw err;
  }
}

async function fileExistsOnRef(
  octokit: ProbotOctokit,
  owner: string,
  repo: string,
  path: string,
  ref: string,
): Promise<boolean> {
  try {
    await octokit.rest.repos.getContent({ owner, repo, path, ref });
    return true;
  } catch (err: unknown) {
    const status = (err as { status?: number }).status;
    if (status === 404) return false;
    throw err;
  }
}

// Blob sha of `path` on `ref`, or undefined when absent (so a commit creates it).
async function shaOnRef(
  octokit: ProbotOctokit,
  owner: string,
  repo: string,
  path: string,
  ref: string,
): Promise<string | undefined> {
  try {
    const res = await octokit.rest.repos.getContent({ owner, repo, path, ref });
    if (!Array.isArray(res.data) && res.data.type === "file") return res.data.sha;
  } catch {
    // not present on this ref
  }
  return undefined;
}

// Parsed JSON + blob sha on a branch; absent = { json: {}, sha: undefined }.
// Malformed JSON keeps its sha (in-place update) with an empty object.
async function readJsonOnBranch(
  octokit: ProbotOctokit,
  owner: string,
  repo: string,
  path: string,
  ref: string,
): Promise<{ json: Record<string, unknown>; sha?: string }> {
  try {
    const existing = await octokit.rest.repos.getContent({ owner, repo, path, ref });
    if (!Array.isArray(existing.data) && existing.data.type === "file") {
      const sha = existing.data.sha;
      const decoded = Buffer.from(
        existing.data.content,
        existing.data.encoding as BufferEncoding,
      ).toString("utf-8");
      let json: Record<string, unknown> = {};
      try {
        json = JSON.parse(decoded);
      } catch {
        // malformed manifest: treat as empty but keep the sha for an in-place update
      }
      return { json, sha };
    }
  } catch {
    // file doesn't exist on this ref yet
  }
  return { json: {}, sha: undefined };
}

// Merge order: the author's archipelago.json is canonical for every field it
// declares (removed fields disappear from the Index too); Oliver overrides
// module_location and disk_space_mb (ceil of wheel bytes / 1MiB); igdb_id is
// preserved from the existing manifest only when the author didn't set one.
export function mergeWorldManifest(
  sourceManifest: Record<string, unknown>,
  currentJson: Record<string, unknown>,
  moduleLocation: string,
  wheelAssetSize: number,
): Record<string, unknown> {
  const updated: Record<string, unknown> = {
    ...sourceManifest,
    module_location: moduleLocation,
    disk_space_mb: Math.ceil(wheelAssetSize / (1024 * 1024)),
  };
  if (!("igdb_id" in sourceManifest) && "igdb_id" in currentJson) {
    updated.igdb_id = currentJson.igdb_id;
  }
  return updated;
}

async function readCodeowners(
  octokit: ProbotOctokit,
  indexOwner: string,
  indexName: string,
  branchName: string,
): Promise<{ content: string; sha?: string }> {
  try {
    const existing = await octokit.rest.repos.getContent({
      owner: indexOwner,
      repo: indexName,
      path: CODEOWNERS_PATH,
      ref: branchName,
    });
    if (!Array.isArray(existing.data) && existing.data.type === "file") {
      return {
        content: Buffer.from(
          existing.data.content,
          existing.data.encoding as BufferEncoding,
        ).toString("utf-8"),
        sha: existing.data.sha,
      };
    }
  } catch (err: unknown) {
    const status = (err as { status?: number }).status;
    if (status !== 404) throw err;
  }
  return { content: "", sha: undefined };
}

function appendCodeownersLine(content: string, line: string): string {
  if (content === "") {
    return `# CODEOWNERS\n# Per-world authors are appended automatically when a new worlds/<slug>.json is added.\n\n${line}\n`;
  }
  const sep = content.endsWith("\n") ? "" : "\n";
  return content + sep + line + "\n";
}

interface AppendCodeownersOpts {
  karenOctokit: ProbotOctokit;
  indexOwner: string;
  indexName: string;
  branchName: string;
  slug: string;
  codeowner: string;
}

async function appendCodeownersForNewWorld(opts: AppendCodeownersOpts): Promise<string | null> {
  const { karenOctokit, indexOwner, indexName, branchName, slug, codeowner } = opts;

  const targetPath = `worlds/${slug}.json`;
  const { content: existingContent, sha: existingSha } = await readCodeowners(
    karenOctokit,
    indexOwner,
    indexName,
    branchName,
  );

  const conflict = findCodeownersConflict(existingContent, targetPath, codeowner);
  if (conflict !== null) {
    return conflict;
  }
  if (containsExactLine(existingContent, targetPath, codeowner)) {
    return null;
  }

  const newContent = appendCodeownersLine(existingContent, `${targetPath} @${codeowner}`);
  await karenOctokit.rest.repos.createOrUpdateFileContents({
    owner: indexOwner,
    repo: indexName,
    path: CODEOWNERS_PATH,
    branch: branchName,
    message: `[${slug}] Add @${codeowner} as codeowner`,
    content: Buffer.from(newContent, "utf-8").toString("base64"),
    sha: existingSha,
  });

  return null;
}

function findCodeownersConflict(content: string, targetPath: string, expectedHandle: string): string | null {
  for (const raw of content.split("\n")) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    const [pattern, ...owners] = line.split(/\s+/);
    if (pattern !== targetPath) continue;
    const handles = owners.map((o) => o.replace(/^@/, ""));
    if (handles.length === 1 && handles[0] === expectedHandle) return null;
    return handles.join(",");
  }
  return null;
}

function containsExactLine(content: string, targetPath: string, expectedHandle: string): boolean {
  for (const raw of content.split("\n")) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    const [pattern, ...owners] = line.split(/\s+/);
    if (pattern !== targetPath) continue;
    const handles = owners.map((o) => o.replace(/^@/, ""));
    if (handles.length === 1 && handles[0] === expectedHandle) return true;
  }
  return false;
}

function deriveCodeownerHandle(sourceOwner: string): string {
  const prefix = process.env.OLIVER_CODEOWNER_PREFIX ?? "";
  return `${prefix}${sourceOwner}`;
}
