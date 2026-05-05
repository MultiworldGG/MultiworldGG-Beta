import type { Context, Probot } from "probot";
import { EventLog } from "../event-log";
import { readRepoVariable } from "../repo-vars";
import { resolveReleaseTagForSha, ReleaseNotFoundError } from "../release-resolver";
import { openOrUpdateIndexPR } from "../index-pr";

const INDEX_REPO_DEFAULT = "lallaria/MultiworldGG-Index";
const TARGET_WORKFLOW_NAME = "Create and Release Python Package";
const SLUG_VARIABLE = "WORLD_FOLDER_NAME";

export async function handleWorkflowRun(
  oliverProbot: Probot,
  karenProbot: Probot,
  context: Context<"workflow_run.completed">,
): Promise<void> {
  const oliverLog = new EventLog(oliverProbot.log);
  const karenLog = new EventLog(karenProbot.log);
  const { owner, repo } = context.repo();
  const sourceRepo = `${owner}/${repo}`;
  const run = context.payload.workflow_run;

  if (run.name !== TARGET_WORKFLOW_NAME) {
    context.log.debug(
      { workflow_name: run.name, expected: TARGET_WORKFLOW_NAME },
      "ignoring workflow_run for non-target workflow",
    );
    return;
  }

  if (run.event !== "release") {
    context.log.debug(
      { run_id: run.id, event: run.event },
      "ignoring workflow_run not triggered by release",
    );
    return;
  }

  if (run.conclusion !== "success") {
    oliverLog.emit({
      kind: "skip",
      source_repo: sourceRepo,
      release_sha: run.head_sha,
      reason: "workflow_failure",
      message: `Workflow concluded ${run.conclusion}; skipping Index PR.`,
    });
    return;
  }

  const slug = await readRepoVariable(context.octokit, owner, repo, SLUG_VARIABLE);
  if (!slug) {
    oliverLog.emit({
      kind: "skip",
      source_repo: sourceRepo,
      release_sha: run.head_sha,
      reason: "no_world_folder_name",
      message: `Repo variable ${SLUG_VARIABLE} is not set on ${sourceRepo}; cannot determine slug.`,
    });
    return;
  }

  let releaseTag: string;
  try {
    releaseTag = await resolveReleaseTagForSha(context.octokit, owner, repo, run.head_sha);
  } catch (err) {
    if (err instanceof ReleaseNotFoundError) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        slug,
        release_sha: run.head_sha,
        reason: "release_not_found",
        message: `Could not find a release whose tag points to ${run.head_sha}.`,
      });
      return;
    }
    throw err;
  }

  const wheelTag = `wheel/worlds/${slug}/${releaseTag}`;
  let pinnedSha: string;
  try {
    const tagRef = await context.octokit.rest.git.getRef({
      owner,
      repo,
      ref: `tags/${wheelTag}`,
    });
    if (tagRef.data.object.type === "tag") {
      const annotated = await context.octokit.rest.git.getTag({
        owner,
        repo,
        tag_sha: tagRef.data.object.sha,
      });
      pinnedSha = annotated.data.object.sha;
    } else {
      pinnedSha = tagRef.data.object.sha;
    }
  } catch (err: unknown) {
    const status = (err as { status?: number }).status;
    if (status === 404) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        slug,
        release_tag: releaseTag,
        release_sha: run.head_sha,
        reason: "tag_missing",
        message: `Expected wheel tag ${wheelTag} not found on ${sourceRepo}.`,
      });
      return;
    }
    throw err;
  }

  const sourceManifest = await fetchSourceManifest(context, owner, repo, slug, run.head_sha);

  const indexRepoSpec = process.env.OLIVER_INDEX_REPO ?? INDEX_REPO_DEFAULT;
  const [indexOwner, indexName] = indexRepoSpec.split("/", 2);
  if (!indexOwner || !indexName) {
    throw new Error(`Invalid OLIVER_INDEX_REPO: ${indexRepoSpec}`);
  }

  let oliverIndexInstallId: number;
  try {
    const indexInstall = await context.octokit.rest.apps.getRepoInstallation({
      owner: indexOwner,
      repo: indexName,
    });
    oliverIndexInstallId = indexInstall.data.id;
  } catch (err: unknown) {
    const status = (err as { status?: number }).status;
    if (status === 404) {
      oliverLog.emit({
        kind: "error",
        source_repo: sourceRepo,
        slug,
        release_tag: releaseTag,
        release_sha: run.head_sha,
        wheel_sha: pinnedSha,
        reason: "index_install_missing",
        message: `Oliver is not installed on ${indexRepoSpec}; cannot open Index PR.`,
      });
      return;
    }
    throw err;
  }

  let karenIndexInstallId: number;
  try {
    const karenAppOctokit = await karenProbot.auth();
    const karenInstall = await karenAppOctokit.rest.apps.getRepoInstallation({
      owner: indexOwner,
      repo: indexName,
    });
    karenLog.emit({kind: "ok", source_repo: sourceRepo, message: JSON.stringify(karenInstall.data, null, 2)});
    karenIndexInstallId = karenInstall.data.id;
  } catch (err: unknown) {
    const status = (err as { status?: number }).status;
    if (status === 404) {
      karenLog.emit({
        kind: "error",
        source_repo: sourceRepo,
        slug,
        release_tag: releaseTag,
        release_sha: run.head_sha,
        wheel_sha: pinnedSha,
        reason: "index_install_missing",
        message: `Karen is not installed on ${indexRepoSpec}; cannot create Index branch.`,
      });
      return;
    }
    throw err;
  }

  try {
    const oliverOctokit = await oliverProbot.auth(oliverIndexInstallId);
    const karenOctokit = await karenProbot.auth(karenIndexInstallId);
    const karenUserName = "Karen the Multiworld Knight [bot]";
    const result = await openOrUpdateIndexPR({
      karenOctokit,
      oliverOctokit,
      karenUserName,
      indexOwner,
      indexName,
      sourceOwner: owner,
      sourceRepo: repo,
      slug,
      releaseTag,
      pinnedSha,
      sourceManifest: sourceManifest ?? {},
    });
    oliverLog.emit({
      kind: "ok",
      source_repo: sourceRepo,
      slug,
      release_tag: releaseTag,
      release_sha: run.head_sha,
      wheel_sha: pinnedSha,
      index_pr: result.prNumber,
      message: result.created
        ? `Opened Index PR #${result.prNumber} for ${slug}@${releaseTag}.`
        : `Updated Index PR #${result.prNumber} for ${slug}@${releaseTag}.`,
    });
    if (result.codeownersConflictWith) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        slug,
        release_tag: releaseTag,
        release_sha: run.head_sha,
        index_pr: result.prNumber,
        reason: "codeowners_conflict",
        message: `New-world PR opened, but CODEOWNERS already lists @${result.codeownersConflictWith} for worlds/${slug}.json; left untouched.`,
      });
    }
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    oliverLog.emit({
      kind: "error",
      source_repo: sourceRepo,
      slug,
      release_tag: releaseTag,
      release_sha: run.head_sha,
      wheel_sha: pinnedSha,
      reason: "github_api_error",
      message: `Failed to open/update Index PR: ${message}`,
    });
    throw err;
  }
}

// The per-world repo's archipelago.json is the canonical source of truth for
// every manifest field except module_location (Oliver-controlled, pinned to a
// wheel SHA) and igdb_id (Index-controlled, set by the IGDB-lookup workflow
// unless the author explicitly opts in by including it themselves).
//
// Returns the full parsed object so the merge in index-pr.ts can spread it.
// Returns null if the file is missing, unreadable, or unparseable — the caller
// then writes a manifest with only Oliver-controlled fields, and Karen's schema
// check will surface the missing required `game` field on the resulting PR.
async function fetchSourceManifest(
  context: Context<"workflow_run.completed">,
  owner: string,
  repo: string,
  slug: string,
  ref: string,
): Promise<Record<string, unknown> | null> {
  try {
    const res = await context.octokit.rest.repos.getContent({
      owner,
      repo,
      path: `worlds/${slug}/archipelago.json`,
      ref,
    });
    if (Array.isArray(res.data) || res.data.type !== "file") return null;
    const decoded = Buffer.from(res.data.content, res.data.encoding as BufferEncoding).toString("utf-8");
    const parsed = JSON.parse(decoded);
    if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) return null;
    return parsed as Record<string, unknown>;
  } catch {
    return null;
  }
}
