import type { Context, Probot } from "probot";
import * as os from "os";
import * as path from "path";
import * as fs from "fs/promises";
import { discoverSlug, DiscoveryResult } from "../slug-discovery";
import { shapeOrphan, readManifest, Manifest } from "../shape-orphan";
import { cloneAtTag, pushOrphan, TagImmutabilityError } from "../git-ops";

const INDEX_REPO_DEFAULT = "lallaria/MultiworldGG-Index";

const TEMPLATES_DIR = path.join(__dirname, "..", "templates");

export async function handleRelease(
  probot: Probot,
  context: Context<"release.published">,
): Promise<void> {
  const { owner, repo } = context.repo();
  const tag = context.payload.release.tag_name;
  const releaseId = context.payload.release.id;

  context.log.info({ owner, repo, tag }, "release.published received");

  const discovery = await discoverSlug(context.octokit, owner, repo, tag);

  if (discovery.kind === "skip") {
    context.log.warn({ discovery }, "slug discovery skipped");
    await postReleaseComment(context, owner, repo, releaseId, discovery.message);
    await openIndexFallbackIssue(probot, context, owner, repo, tag, discovery);
    return;
  }

  const slug = discovery.slug;
  context.log.info({ slug, base: discovery.base }, "slug discovery ok");

  const auth = (await context.octokit.auth({ type: "installation" })) as { token: string };
  const perWorldToken = auth.token;

  const tmpRoot = await fs.mkdtemp(path.join(os.tmpdir(), "oliver-"));
  const cloneDir = path.join(tmpRoot, "clone");
  const treeDir = path.join(tmpRoot, "tree");

  try {
    const cloneUrl = `https://x-access-token:${perWorldToken}@github.com/${owner}/${repo}.git`;
    await cloneAtTag(cloneUrl, tag, cloneDir);

    const manifest = await readManifest(cloneDir, slug);
    await shapeOrphan({ slug, manifest, cloneDir, outDir: treeDir, templatesDir: TEMPLATES_DIR });

    const orphanBranch = `module-install/${slug}`;
    const orphanTag = `module-install/${slug}/${manifest.world_version}`;

    try {
      await pushOrphan({
        treeDir,
        branchName: orphanBranch,
        tagName: orphanTag,
        authorName: "oliver-multiworld-squirrel[bot]",
        authorEmail: "oliver-multiworld-squirrel[bot]@users.noreply.github.com",
        remoteUrl: cloneUrl,
      });
      context.log.info({ slug, tag: orphanTag }, "pushed orphan branch + tag");
    } catch (err) {
      if (err instanceof TagImmutabilityError) {
        context.log.warn({ err: err.message }, "tag already exists at different SHA — skipping");
        await postReleaseComment(
          context,
          owner,
          repo,
          releaseId,
          `Oliver: \`${orphanTag}\` already exists at a different SHA. Refusing to overwrite the immutable tag. ` +
            `Bump \`world_version\` in \`worlds/${slug}/archipelago.json\` and cut a new release.`,
        );
        return;
      }
      throw err;
    }

    const indexRepoSpec = process.env.OLIVER_INDEX_REPO ?? INDEX_REPO_DEFAULT;
    const [indexOwner, indexName] = indexRepoSpec.split("/", 2);
    if (!indexOwner || !indexName) {
      throw new Error(`Invalid OLIVER_INDEX_REPO: ${indexRepoSpec}`);
    }

    const indexInstall = await context.octokit.rest.apps.getRepoInstallation({
      owner: indexOwner,
      repo: indexName,
    });
    const indexOctokit = await probot.auth(indexInstall.data.id);

    await openOrUpdateIndexPR({
      indexOctokit,
      indexOwner,
      indexName,
      sourceOwner: owner,
      sourceRepo: repo,
      slug,
      manifest,
      orphanTag,
    });
    context.log.info({ slug, tag: orphanTag, indexRepo: indexRepoSpec }, "opened/updated Index PR");
  } finally {
    await fs.rm(tmpRoot, { recursive: true, force: true }).catch(() => undefined);
  }
}

async function postReleaseComment(
  context: Context<"release.published">,
  owner: string,
  repo: string,
  _releaseId: number,
  message: string,
): Promise<void> {
  // Releases API doesn't support comments directly; use an Issue comment if the release has a discussion,
  // else fall back to creating an Issue on the source repo. For now, log the message and use the
  // release's body via PATCH to append a footer. (TODO: confirm best surface; this is a v0 placeholder.)
  const body = context.payload.release.body ?? "";
  const footer = `\n\n---\n_Oliver:_ ${message}`;
  if (!body.includes("_Oliver:_")) {
    try {
      await context.octokit.rest.repos.updateRelease({
        owner,
        repo,
        release_id: context.payload.release.id,
        body: body + footer,
      });
    } catch (err) {
      context.log.warn({ err }, "failed to append Oliver footer to release body");
    }
  }
}

async function openIndexFallbackIssue(
  probot: Probot,
  context: Context<"release.published">,
  sourceOwner: string,
  sourceRepo: string,
  tag: string,
  discovery: Extract<DiscoveryResult, { kind: "skip" }>,
): Promise<void> {
  const indexRepoSpec = process.env.OLIVER_INDEX_REPO ?? INDEX_REPO_DEFAULT;
  const [indexOwner, indexName] = indexRepoSpec.split("/", 2);
  try {
    const indexInstall = await context.octokit.rest.apps.getRepoInstallation({
      owner: indexOwner,
      repo: indexName,
    });
    const indexOctokit = await probot.auth(indexInstall.data.id);

    const releaseUrl = context.payload.release.html_url;
    const candidatesText = discovery.candidates.length
      ? discovery.candidates.map((s) => `- \`${s}\``).join("\n")
      : "_(none — no `worlds/<slug>/archipelago.json` was touched)_";

    const title = `[oliver] Manual PR needed: ${sourceOwner}/${sourceRepo}@${tag}`;
    const body = [
      `Oliver couldn't determine which world to publish from the release at ${releaseUrl}.`,
      ``,
      `**Source repo:** \`${sourceOwner}/${sourceRepo}\``,
      `**Tag:** \`${tag}\``,
      `**Diff base used:** \`${discovery.base}\``,
      `**Reason:** ${discovery.reason === "no_candidates" ? "no candidate worlds detected" : "multiple candidate worlds detected"}`,
      ``,
      `**Candidate slugs:**`,
      candidatesText,
      ``,
      `### Action requested`,
      `- [ ] Decide the correct slug for this release`,
      `- [ ] Open the Index PR by hand updating \`worlds/<slug>.json\` with the new \`module_location\``,
      `- [ ] Close this issue`,
      ``,
      `_Oliver was reached via webhook from the source repo's installation. The Index installation receives this issue. The skip message has been appended to the source release body._`,
    ].join("\n");

    await indexOctokit.rest.issues.create({
      owner: indexOwner,
      repo: indexName,
      title,
      body,
    });
  } catch (err) {
    context.log.error({ err }, "failed to open Index fallback issue — manual intervention required");
  }
}

interface IndexPROpts {
  indexOctokit: Awaited<ReturnType<Probot["auth"]>>;
  indexOwner: string;
  indexName: string;
  sourceOwner: string;
  sourceRepo: string;
  slug: string;
  manifest: Manifest;
  orphanTag: string;
}

async function openOrUpdateIndexPR(opts: IndexPROpts): Promise<void> {
  const {
    indexOctokit,
    indexOwner,
    indexName,
    sourceOwner,
    sourceRepo,
    slug,
    manifest,
    orphanTag,
  } = opts;

  const moduleLocation = `git+https://github.com/${sourceOwner}/${sourceRepo}.git@${orphanTag}`;
  const branchName = `update/${slug}-${manifest.world_version}`;
  const filePath = `worlds/${slug}.json`;

  const baseRef = await indexOctokit.rest.repos.get({ owner: indexOwner, repo: indexName });
  const defaultBranch = baseRef.data.default_branch;

  const baseBranchRef = await indexOctokit.rest.git.getRef({
    owner: indexOwner,
    repo: indexName,
    ref: `heads/${defaultBranch}`,
  });
  const baseSha = baseBranchRef.data.object.sha;

  try {
    await indexOctokit.rest.git.getRef({
      owner: indexOwner,
      repo: indexName,
      ref: `heads/${branchName}`,
    });
  } catch {
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
      const decoded = Buffer.from(existing.data.content, existing.data.encoding as BufferEncoding).toString("utf-8");
      currentJson = JSON.parse(decoded);
    }
  } catch {
    // file doesn't exist on this branch; we'll create it
  }

  const updated = {
    ...currentJson,
    game: manifest.game,
    module_location: moduleLocation,
    world_version: manifest.world_version,
    authors: manifest.authors,
  };
  const newContent = JSON.stringify(updated, null, 2) + "\n";
  const encodedContent = Buffer.from(newContent, "utf-8").toString("base64");

  await indexOctokit.rest.repos.createOrUpdateFileContents({
    owner: indexOwner,
    repo: indexName,
    path: filePath,
    branch: branchName,
    message: `[${slug}] Update to ${manifest.world_version}`,
    content: encodedContent,
    sha: currentSha,
    committer: {
      name: "oliver-multiworld-squirrel[bot]",
      email: "oliver-multiworld-squirrel[bot]@users.noreply.github.com",
    },
    author: {
      name: "oliver-multiworld-squirrel[bot]",
      email: "oliver-multiworld-squirrel[bot]@users.noreply.github.com",
    },
  });

  const existingPRs = await indexOctokit.rest.pulls.list({
    owner: indexOwner,
    repo: indexName,
    head: `${indexOwner}:${branchName}`,
    state: "open",
  });

  const prBody = [
    `Auto-opened by Oliver from \`${sourceOwner}/${sourceRepo}@${orphanTag}\`.`,
    ``,
    `**Slug:** \`${slug}\``,
    `**World version:** \`${manifest.world_version}\``,
    `**New module_location:** \`${moduleLocation}\``,
  ].join("\n");

  if (existingPRs.data.length === 0) {
    await indexOctokit.rest.pulls.create({
      owner: indexOwner,
      repo: indexName,
      title: `[${slug}] Update to ${manifest.world_version}`,
      head: branchName,
      base: defaultBranch,
      body: prBody,
    });
  } else {
    await indexOctokit.rest.pulls.update({
      owner: indexOwner,
      repo: indexName,
      pull_number: existingPRs.data[0].number,
      body: prBody,
    });
  }
}
