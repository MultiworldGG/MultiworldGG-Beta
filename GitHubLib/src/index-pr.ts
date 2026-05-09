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
  // produced by the build-and-publish-action. Computed by the caller
  // (workflow_run handler) so this module doesn't need to know the action's
  // output shape.
  moduleLocation: string;
  // Wheel asset filename (e.g. `clique-1.0.0-py3-none-any.whl`) and size in
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
  //   2. Oliver overrides module_location with the release-asset wheel URL
  //      computed by the workflow_run handler.
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
