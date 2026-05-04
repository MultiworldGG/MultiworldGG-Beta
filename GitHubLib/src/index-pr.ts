import type { ProbotOctokit } from "probot";

export interface IndexPROpts {
  karenOctokit: ProbotOctokit;   // Contents:Write + Pull requests:Write + Issues:Write — does branch, commit, PR, label, CODEOWNERS on the Index
  karenSlug: string;             // for the committer identity
  indexOwner: string;
  indexName: string;
  sourceOwner: string;
  sourceRepo: string;
  slug: string;
  releaseTag: string;
  pinnedSha: string;
  game: string | null;
  authors: string[] | null;
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
const CODEOWNERS_PATH = ".github/CODEOWNERS";

export async function openOrUpdateIndexPR(opts: IndexPROpts): Promise<IndexPRResult> {
  const {
    karenOctokit,
    karenSlug,
    indexOwner,
    indexName,
    sourceOwner,
    sourceRepo,
    slug,
    releaseTag,
    pinnedSha,
    game,
    authors,
  } = opts;

  const moduleLocation = `git+https://github.com/${sourceOwner}/${sourceRepo}.git@${pinnedSha}`;
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

  const updated: Record<string, unknown> = {
    ...currentJson,
    module_location: moduleLocation,
    world_version: releaseTag,
  };
  if (game) updated.game = game;
  if (authors) updated.authors = authors;

  const newContent = JSON.stringify(updated, null, 2) + "\n";
  const encodedContent = Buffer.from(newContent, "utf-8").toString("base64");

  const karenCommitter = {
    name: `${karenSlug}[bot]`,
    email: `${karenSlug}[bot]@users.noreply.github.com`,
  };

  await karenOctokit.rest.repos.createOrUpdateFileContents({
    owner: indexOwner,
    repo: indexName,
    path: filePath,
    branch: branchName,
    message: `[${slug}] Update to ${releaseTag}`,
    content: encodedContent,
    sha: currentSha,
    committer: karenCommitter,
    author: karenCommitter,
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
      karenCommitter,
    });
  }

  const existingPRs = await karenOctokit.rest.pulls.list({
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
    `Branch was created and committed by \`${karenSlug}[bot]\`; Karen's review workflow will run automatically.`,
  ].join("\n");

  let prNumber: number;
  let created: boolean;
  if (existingPRs.data.length === 0) {
    const createdPR = await karenOctokit.rest.pulls.create({
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
    await karenOctokit.rest.pulls.update({
      owner: indexOwner,
      repo: indexName,
      pull_number: existing.number,
      body: prBody,
    });
    prNumber = existing.number;
    created = false;
  }

  await karenOctokit.rest.issues.addLabels({
    owner: indexOwner,
    repo: indexName,
    issue_number: prNumber,
    labels: [worldIsNew ? NEW_WORLD_LABEL : UPDATE_WORLD_LABEL],
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
  karenCommitter: { name: string; email: string };
}

async function appendCodeownersForNewWorld(opts: AppendCodeownersOpts): Promise<string | null> {
  const { karenOctokit, indexOwner, indexName, branchName, slug, sourceOwner, karenCommitter } = opts;

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
    committer: karenCommitter,
    author: karenCommitter,
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
