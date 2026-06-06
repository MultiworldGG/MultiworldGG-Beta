import type { ProbotOctokit } from "probot";

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
  karenOctokit: ProbotOctokit;   // Contents:Write — Karen creates the branch, commits the manifest, and appends CODEOWNERS on the Index.
  oliverOctokit: ProbotOctokit;  // Pull requests:Write + Issues:Write — Oliver opens/updates the PR and applies labels (review handoff line — see memory: feedback_oliver_opens_karen_approves).
  karenData: IndexBotData;
  oliverData: IndexBotData;
  indexOwner: string;
  indexName: string;
  sourceOwner: string;
  sourceRepo: string;
  slug: string;
  releaseTag: string;
  // The fully-formed module_location URL Oliver will pin into the Index
  // manifest. Today this is the release-asset wheel URL
  // (`https://github.com/<owner>/<repo>/releases/download/<release_tag>/<dist>-<v>-py3-none-any.whl`)
  // produced by the gen-pymod-release. Computed by the caller
  // (workflow_run handler) so this module doesn't need to know the action's
  // output shape.
  moduleLocation: string;
  // Wheel asset filename (e.g. `myclgm-1.0.0-py3-none-any.whl`) and size in
  // bytes, both surfaced in the PR body so reviewers see what's being pinned
  // without clicking through. Read from the GitHub release-asset object by
  // the workflow_run handler.
  wheelAssetName: string;
  wheelAssetSize: number;
  // Full parsed `worlds/<slug>/archipelago.json` from the per-world repo at the
  // release SHA. The author's archipelago.json is the canonical source of
  // truth for everything except module_location (Oliver overrides) and igdb_id
  // (preserved from the existing Index manifest unless the author explicitly
  // sets their own). Use {} when the file is missing/unreadable — Karen's
  // schema check will surface the resulting bad PR.
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

  let branchExists = true;
  try {
    await karenOctokit.rest.git.getRef({
      owner: indexOwner,
      repo: indexName,
      ref: `heads/${branchName}`,
    });
  } catch {
    branchExists = false;
  }
  if (!branchExists) {
    await karenOctokit.rest.git.createRef({
      owner: indexOwner,
      repo: indexName,
      ref: `refs/heads/${branchName}`,
      sha: baseSha,
    });
  }

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

  const prBody = [
    `Auto-opened by Oliver from \`${sourceOwner}/${sourceRepo}@${releaseTag}\`.`,
    ``,
    `**Slug:** \`${slug}\``,
    `**Release tag:** \`${releaseTag}\``,
    `**Wheel:** \`${wheelAssetName}\` (${formatWheelSize(wheelAssetSize)})`,
    `**New module_location:** \`${moduleLocation}\``,
    ``,
    `Branch was created and committed by \`${karenData.name}[bot](${karenData.html_url})\`; Karen's review workflow will run automatically.`,
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

    // Enable auto-merge so the PR squash-merges automatically once the
    // org-rulesets gates clear (3 approvals incl. Karen + required status checks).
    // Best-effort: a disabled repo toggle, an empty branch, or any transient
    // error here must not crash the workflow_run handler — the PR still exists
    // and Karen's review + manual merge still work.
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
  // Oliver holds Contents:Write on the Index for the bundle path and does the
  // whole job himself — branch, commits, PR, labels. Karen is not involved.
  oliverOctokit: ProbotOctokit;
  oliverData: IndexBotData;
  indexOwner: string;
  indexName: string;
  // Bundle source is the Beta monorepo, owned by the org — not a per-world author.
  sourceOwner: string;
  sourceRepo: string;
  // `worlds-wheels-<date>` tag of the bundled release.
  releaseTag: string;
  // One entry per changed world's wheel; caller guarantees length >= 1.
  worlds: BundleWorld[];
}

export interface BundleIndexPRResult {
  opened: boolean;
  prNumber: number;
  branchName: string;
  created: boolean;
  updatedWorldSlugs: string[];
  // Bundled worlds not yet on the Index (no manifest to copy).
  skippedSlugs: string[];
}

// Open (or update) ONE combined Index PR for a bundled multi-world release.
// Each bundled world already lives on the Index: copy its `worlds/<slug>.json`
// verbatim and rewrite only `module_location` (the new wheel URL), preserving
// every other field and the file's indentation so the diff is a single line.
// A bundled world that isn't on the Index is skipped — the Beta repo carries no
// per-world archipelago.json at the release commit, so there's nothing to seed a
// new manifest from. All Index writes use Oliver's token (Contents:Write);
// Karen's review workflow still runs once the PR is open.
export async function openOrUpdateBundleIndexPR(opts: BundleIndexPROpts): Promise<BundleIndexPRResult> {
  const {
    oliverOctokit,
    oliverData,
    indexOwner,
    indexName,
    sourceOwner,
    sourceRepo,
    releaseTag,
    worlds,
  } = opts;

  const branchName = `update/${releaseTag}`;

  const repoInfo = await oliverOctokit.rest.repos.get({ owner: indexOwner, repo: indexName });
  const defaultBranch = repoInfo.data.default_branch;

  // Only worlds already on the Index can be copy+edited; the rest are skipped.
  const updatable: BundleWorld[] = [];
  const skippedSlugs: string[] = [];
  for (const w of worlds) {
    const exists = await fileExistsOnRef(
      oliverOctokit,
      indexOwner,
      indexName,
      `worlds/${w.slug}.json`,
      defaultBranch,
    );
    if (exists) updatable.push(w);
    else skippedSlugs.push(w.slug);
  }
  if (updatable.length === 0) {
    return { opened: false, prNumber: 0, branchName, created: false, updatedWorldSlugs: [], skippedSlugs };
  }

  const baseRef = await oliverOctokit.rest.git.getRef({
    owner: indexOwner,
    repo: indexName,
    ref: `heads/${defaultBranch}`,
  });
  const baseSha = baseRef.data.object.sha;

  let branchExists = true;
  try {
    await oliverOctokit.rest.git.getRef({
      owner: indexOwner,
      repo: indexName,
      ref: `heads/${branchName}`,
    });
  } catch {
    branchExists = false;
  }
  if (!branchExists) {
    await oliverOctokit.rest.git.createRef({
      owner: indexOwner,
      repo: indexName,
      ref: `refs/heads/${branchName}`,
      sha: baseSha,
    });
  }

  let anyNeedsIgdb = false;
  const bodyWorldLines: string[] = [];
  for (const w of updatable) {
    const filePath = `worlds/${w.slug}.json`;
    const existing = await oliverOctokit.rest.repos.getContent({
      owner: indexOwner,
      repo: indexName,
      path: filePath,
      ref: branchName,
    });
    if (Array.isArray(existing.data) || existing.data.type !== "file") {
      skippedSlugs.push(w.slug);
      continue;
    }
    const raw = Buffer.from(existing.data.content, existing.data.encoding as BufferEncoding).toString("utf-8");
    const currentJson = JSON.parse(raw) as Record<string, unknown>;
    // Copy the Index manifest; rewrite only the wheel pointer. Spreading
    // currentJson first preserves every other field and module_location's
    // original key position, so the diff is just the URL line.
    const updated = { ...currentJson, module_location: w.moduleLocation };
    if (!("igdb_id" in updated)) anyNeedsIgdb = true;

    const newContent = JSON.stringify(updated, null, detectJsonIndent(raw)) + "\n";
    await oliverOctokit.rest.repos.createOrUpdateFileContents({
      owner: indexOwner,
      repo: indexName,
      path: filePath,
      branch: branchName,
      message: `[${w.slug}] Update to ${releaseTag}`,
      content: Buffer.from(newContent, "utf-8").toString("base64"),
      sha: existing.data.sha,
    });

    bodyWorldLines.push(`- \`${w.slug}\`: \`${w.wheelAssetName}\` (${formatWheelSize(w.wheelAssetSize)})`);
  }

  const updatedWorldSlugs = updatable.map((w) => w.slug).filter((s) => !skippedSlugs.includes(s));
  if (updatedWorldSlugs.length === 0) {
    return { opened: false, prNumber: 0, branchName, created: false, updatedWorldSlugs: [], skippedSlugs };
  }

  const existingPRs = await oliverOctokit.rest.pulls.list({
    owner: indexOwner,
    repo: indexName,
    head: `${indexOwner}:${branchName}`,
    state: "open",
  });

  const prBody = [
    `Auto-opened by Oliver from \`${sourceOwner}/${sourceRepo}@${releaseTag}\` (bundled multi-world release).`,
    ``,
    `**Release tag:** \`${releaseTag}\``,
    `**Worlds updated:** ${updatedWorldSlugs.length}`,
    ...(skippedSlugs.length ? [`**Skipped (not on Index):** ${skippedSlugs.join(", ")}`] : []),
    ``,
    ...bodyWorldLines,
    ``,
    `Branch created and committed by \`${oliverData.name}[bot](${oliverData.html_url})\`; Karen's review workflow will run automatically.`,
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

  const labels = [UPDATE_WORLD_LABEL];
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

// Read a JSON file on a branch, returning its parsed object + blob sha, or
// `{ json: {}, sha: undefined }` when the file is absent. A file that exists
// but holds malformed JSON keeps its sha (so the caller updates in place) with
// an empty object — matching the original inline read's behavior.
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
        // malformed manifest — treat as empty but keep the sha for an in-place update
      }
      return { json, sha };
    }
  } catch {
    // file doesn't exist on this ref yet
  }
  return { json: {}, sha: undefined };
}

// Merge order:
//   1. The per-world author's archipelago.json is canonical for every field
//      they declare (game, authors, world_version, _comment, tracker, flags,
//      anything they put there). If they remove a field from their next
//      release, it disappears from the Index manifest too.
//   2. Oliver overrides module_location with the release-asset wheel URL.
//   3. Oliver overrides disk_space_mb with ceil(wheel_size_bytes / 1MiB).
//      The author can't compute the wheel size before the build runs, so
//      Oliver stamps it from the GitHub release-asset metadata. Downstream
//      consumers (e.g. tools/regen_inno_components.py) convert MB->KB
//      themselves; the manifest stays in MB for human-readability.
//   4. igdb_id is preserved from the existing Index manifest if and only if
//      the author did not include one themselves. If they did, theirs wins.
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
