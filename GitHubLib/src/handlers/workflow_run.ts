import type { Context, Probot } from "probot";
import { EventLog } from "../event-log";
import { readRepoVariable } from "../repo-vars";
import { resolveReleaseTagForSha, ReleaseNotFoundError } from "../release-resolver";
import { IndexBotData, openOrUpdateIndexPR } from "../index-pr";

const INDEX_REPO_DEFAULT = "MultiworldGG/MultiworldGG-Index";
const TARGET_WORKFLOW_NAME = "Create and Release Python Package";
const SLUG_VARIABLE = "WORLD_FOLDER_NAME";

export async function handleWorkflowRun(
  oliverProbot: Probot,
  karenProbot: Probot,
  oliverData: IndexBotData,
  karenData: IndexBotData,
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

  let releaseTag: string;
  try {
    releaseTag = await resolveReleaseTagForSha(context.octokit, owner, repo, run.head_sha);
  } catch (err) {
    if (err instanceof ReleaseNotFoundError) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        release_sha: run.head_sha,
        reason: "release_not_found",
        message: `Could not find a release whose tag points to ${run.head_sha}.`,
      });
      return;
    }
    throw err;
  }

  // Slug resolution mirrors the action's logic in build.yml:
  //   1. WORLD_FOLDER_NAME repo variable wins (single-world repos).
  //   2. Else parse from `<slug>-<world_version>` release tag prefix
  //      (multi-world repos like TheLX5/Archipelago).
  const declaredSlug = await readRepoVariable(context.octokit, owner, repo, SLUG_VARIABLE);
  let slug: string | null = declaredSlug ?? null;
  if (!slug) {
    const dashIdx = releaseTag.indexOf("-");
    if (dashIdx > 0 && dashIdx < releaseTag.length - 1) {
      slug = releaseTag.slice(0, dashIdx);
    }
  }
  if (!slug) {
    oliverLog.emit({
      kind: "skip",
      source_repo: sourceRepo,
      release_sha: run.head_sha,
      release_tag: releaseTag,
      reason: "no_slug_resolved",
      message:
        `Cannot resolve slug for ${sourceRepo}: ${SLUG_VARIABLE} is unset and ` +
        `release tag '${releaseTag}' does not match '<slug>-<world_version>'.`,
    });
    return;
  }

  // Look up the wheel asset on the release. Replaces the v2 wheel-branch tag
  // lookup; module_location now pins to the asset's browser_download_url.
  let moduleLocation: string;
  let wheelAssetName: string;
  let wheelAssetSize: number;
  try {
    const release = await context.octokit.rest.repos.getReleaseByTag({
      owner,
      repo,
      tag: releaseTag,
    });
    const wheelAssets = release.data.assets.filter((a) => a.name.endsWith(".whl"));
    if (wheelAssets.length === 0) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        slug,
        release_tag: releaseTag,
        release_sha: run.head_sha,
        reason: "wheel_asset_missing",
        message: `Release ${releaseTag} on ${sourceRepo} has no .whl asset attached.`,
      });
      return;
    }
    if (wheelAssets.length > 1) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        slug,
        release_tag: releaseTag,
        release_sha: run.head_sha,
        reason: "wheel_asset_ambiguous",
        message:
          `Release ${releaseTag} on ${sourceRepo} has ${wheelAssets.length} .whl assets; ` +
          `expected exactly one.`,
      });
      return;
    }
    const wheelAsset = wheelAssets[0];
    // GitHub release-asset API exposes a `digest` field ("sha256:<hex>"). The
    // openapi-types schema bundled with this Probot/octokit pin predates the
    // field, so cast at the access site rather than bumping the dep.
    const digest = (wheelAsset as { digest?: string | null }).digest;
    if (!digest || !digest.startsWith("sha256:")) {
      // Without a SHA256, the URL would point at mutable bytes — a release-write
      // compromise on the per-world repo could swap the wheel after Karen has
      // already approved the manifest. Bail rather than open an Index PR with
      // an unverifiable module_location. The runtime relies on pip's PEP 503
      // #sha256= fragment verification.
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        slug,
        release_tag: releaseTag,
        release_sha: run.head_sha,
        reason: "asset_digest_missing",
        message:
          `Release ${releaseTag} on ${sourceRepo} wheel asset ${wheelAsset.name} ` +
          `has no SHA256 digest from the GitHub API; refusing to open an Index PR ` +
          `with an unverifiable module_location.`,
      });
      return;
    }
    const sha256 = digest.slice("sha256:".length);
    moduleLocation = `${wheelAsset.browser_download_url}#sha256=${sha256}`;
    wheelAssetName = wheelAsset.name;
    wheelAssetSize = wheelAsset.size;
  } catch (err: unknown) {
    const status = (err as { status?: number }).status;
    if (status === 404) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        slug,
        release_tag: releaseTag,
        release_sha: run.head_sha,
        reason: "release_lookup_404",
        message: `Release ${releaseTag} not found on ${sourceRepo} when fetching assets.`,
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
        wheel_asset: wheelAssetName,
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
        wheel_asset: wheelAssetName,
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

    const result = await openOrUpdateIndexPR({
      karenOctokit,
      oliverOctokit,
      karenData,
      oliverData,
      indexOwner,
      indexName,
      sourceOwner: owner,
      sourceRepo: repo,
      slug,
      releaseTag,
      moduleLocation,
      wheelAssetName,
      wheelAssetSize,
      sourceManifest: sourceManifest ?? {},
    });
    oliverLog.emit({
      kind: "ok",
      source_repo: sourceRepo,
      slug,
      release_tag: releaseTag,
      release_sha: run.head_sha,
      wheel_asset: wheelAssetName,
      wheel_size_bytes: wheelAssetSize,
      module_location: moduleLocation,
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
      wheel_asset: wheelAssetName,
      reason: "github_api_error",
      message: `Failed to open/update Index PR: ${message}`,
    });
    throw err;
  }
}

// The per-world repo's archipelago.json is the canonical source of truth for
// every manifest field except module_location (Oliver-controlled, pinned to a
// release-asset URL) and igdb_id (Index-controlled, set by the IGDB-lookup
// workflow unless the author explicitly opts in by including it themselves).
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
