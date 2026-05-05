import type { ProbotOctokit } from "probot";

export interface IndexPROpts {
  karenOctokit: ProbotOctokit;   // Contents:Write — Karen creates the branch, commits the manifest, and appends CODEOWNERS on the Index.
  oliverOctokit: ProbotOctokit;  // Pull requests:Write + Issues:Write — Oliver opens/updates the PR and applies labels (review handoff line — see memory: feedback_oliver_opens_karen_approves).
  indexOwner: string;
  indexName: string;
  sourceOwner: string;
  sourceRepo: string;
  slug: string;
  releaseTag: string;
  pinnedSha: string;
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
    indexOwner,
    indexName,
    sourceOwner,
    sourceRepo,
    slug,
    releaseTag,
    pinnedSha,
    sourceManifest,
  } = opts;

  const moduleLocation = `git+https://github.com/${sourceOwner}/${sourceRepo}.git@${pinnedSha}`;
  const branchName = `update/${slug}-${releaseTag}`;
  const filePath = `worlds/${slug}.json`;

  const repoInfo = await karenOctokit.rest.repos.get({ owner: indexOwner, repo: indexName });
  const karenUserName = (await karenOctokit.rest.users.getAuthenticated()).data.name ?? "";
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

  let currentJson: Record<string, unknown> = {};
  let currentSha: string | undefined;
  try {
    const existing = await karenOctokit.rest.repos.getContent({
      owner: indexOwner,
      repo: indexName,
      path: filePath,
      ref: branchName,
    });
    if (!Array.isArray(existing.data) && existing.data.type === "file") {
      currentSha = existing.data.sha;
      const decoded = Buffer.from(
        existing.data.content,
        existing.data.encoding as BufferEncoding,
      ).toString("utf-8");
      currentJson = JSON.parse(decoded);
    }
  } catch {
    // file doesn't exist on this branch yet
  }

  // Merge order:
  //   1. The per-world author's archipelago.json is canonical for every field
  //      they declare (game, authors, world_version, _comment, tracker, flags,
  //      anything they put there). If they remove a field from their next
  //      release, it disappears from the Index manifest too.
  //   2. Oliver overrides module_location with the pinned-wheel-SHA URL.
  //   3. igdb_id is preserved from the existing Index manifest if and only if
  //      the author did not include one themselves. If they did, theirs wins
  //      (explicit override).
  const updated: Record<string, unknown> = {
    ...sourceManifest,
    module_location: moduleLocation,
  };
  if (!("igdb_id" in sourceManifest) && "igdb_id" in currentJson) {
    updated.igdb_id = currentJson.igdb_id;
  }

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
      sourceOwner,
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
    `**Pinned SHA:** \`${pinnedSha}\``,
    `**New module_location:** \`${moduleLocation}\``,
    ``,
    `Branch was created and committed by \`${karenUserName}\`; Karen's review workflow will run automatically.`,
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

interface AppendCodeownersOpts {
  karenOctokit: ProbotOctokit;
  indexOwner: string;
  indexName: string;
  branchName: string;
  slug: string;
  sourceOwner: string;
}

async function appendCodeownersForNewWorld(opts: AppendCodeownersOpts): Promise<string | null> {
  const { karenOctokit, indexOwner, indexName, branchName, slug, sourceOwner } = opts;

  const codeowner = deriveCodeownerHandle(sourceOwner);
  const targetPath = `worlds/${slug}.json`;
  const newLine = `${targetPath} @${codeowner}`;

  let existingContent = "";
  let existingSha: string | undefined;
  try {
    const existing = await karenOctokit.rest.repos.getContent({
      owner: indexOwner,
      repo: indexName,
      path: CODEOWNERS_PATH,
      ref: branchName,
    });
    if (!Array.isArray(existing.data) && existing.data.type === "file") {
      existingSha = existing.data.sha;
      existingContent = Buffer.from(
        existing.data.content,
        existing.data.encoding as BufferEncoding,
      ).toString("utf-8");
    }
  } catch (err: unknown) {
    const status = (err as { status?: number }).status;
    if (status !== 404) throw err;
  }

  const conflict = findCodeownersConflict(existingContent, targetPath, codeowner);
  if (conflict !== null) {
    return conflict;
  }
  if (containsExactLine(existingContent, targetPath, codeowner)) {
    return null;
  }

  let newContent: string;
  if (existingContent === "") {
    newContent = `# CODEOWNERS\n# Per-world authors are appended automatically when a new worlds/<slug>.json is added.\n\n${newLine}\n`;
  } else {
    const sep = existingContent.endsWith("\n") ? "" : "\n";
    newContent = existingContent + sep + newLine + "\n";
  }
  const encoded = Buffer.from(newContent, "utf-8").toString("base64");

  await karenOctokit.rest.repos.createOrUpdateFileContents({
    owner: indexOwner,
    repo: indexName,
    path: CODEOWNERS_PATH,
    branch: branchName,
    message: `[${slug}] Add @${codeowner} as codeowner`,
    content: encoded,
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
