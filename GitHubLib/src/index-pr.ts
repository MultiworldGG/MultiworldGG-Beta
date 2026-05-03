import type { ProbotOctokit } from "probot";

export interface IndexPROpts {
  indexOctokit: ProbotOctokit;
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
}

export async function openOrUpdateIndexPR(opts: IndexPROpts): Promise<IndexPRResult> {
  const {
    indexOctokit,
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

  const repoInfo = await indexOctokit.rest.repos.get({ owner: indexOwner, repo: indexName });
  const defaultBranch = repoInfo.data.default_branch;

  const baseRef = await indexOctokit.rest.git.getRef({
    owner: indexOwner,
    repo: indexName,
    ref: `heads/${defaultBranch}`,
  });
  const baseSha = baseRef.data.object.sha;

  let branchExists = true;
  try {
    await indexOctokit.rest.git.getRef({
      owner: indexOwner,
      repo: indexName,
      ref: `heads/${branchName}`,
    });
  } catch {
    branchExists = false;
  }
  if (!branchExists) {
    await indexOctokit.rest.git.createRef({
      owner: indexOwner,
      repo: indexName,
      ref: `refs/heads/${branchName}`,
      sha: baseSha,
    });
  }

  let currentJson: Record<string, unknown> = {};
  let currentSha: string | undefined;
  try {
    const existing = await indexOctokit.rest.repos.getContent({
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

  const committer = {
    name: "oliver-multiworld-squirrel[bot]",
    email: "oliver-multiworld-squirrel[bot]@users.noreply.github.com",
  };

  await indexOctokit.rest.repos.createOrUpdateFileContents({
    owner: indexOwner,
    repo: indexName,
    path: filePath,
    branch: branchName,
    message: `[${slug}] Update to ${releaseTag}`,
    content: encodedContent,
    sha: currentSha,
    committer,
    author: committer,
  });

  const existingPRs = await indexOctokit.rest.pulls.list({
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
  ].join("\n");

  if (existingPRs.data.length === 0) {
    const created = await indexOctokit.rest.pulls.create({
      owner: indexOwner,
      repo: indexName,
      title: `[${slug}] Update to ${releaseTag}`,
      head: branchName,
      base: defaultBranch,
      body: prBody,
    });
    return { prNumber: created.data.number, branchName, created: true };
  } else {
    const existing = existingPRs.data[0];
    await indexOctokit.rest.pulls.update({
      owner: indexOwner,
      repo: indexName,
      pull_number: existing.number,
      body: prBody,
    });
    return { prNumber: existing.number, branchName, created: false };
  }
}
