import type { Context, Probot } from "probot";
import { EventLog } from "../event-log";
import {
  BundleWorld,
  IndexBotData,
  openOrUpdateBundleIndexPR,
  openOrUpdateIndexPR,
} from "../index-pr";

type Octokit = Context["octokit"];

export const INDEX_REPO_DEFAULT = "MultiworldGG/MultiworldGG-Index";
// A release whose tag begins with this prefix is the Beta monorepo's bundled
// "changed worlds" build (one wheel per changed world). It takes the
// multi-world path; every other multi-wheel release keeps the ambiguous skip.
const BUNDLE_TAG_PREFIX = "worlds-wheels-";

export interface ProcessReleaseAssetsParams {
  octokit: Octokit;
  oliverProbot: Probot;
  karenProbot: Probot;
  oliverData: IndexBotData;
  karenData: IndexBotData;
  owner: string;
  repo: string;
  releaseTag: string;
  releaseSha: string;
}

// GitHub hashes release assets asynchronously, so the webhook can beat the
// digests; re-poll until every .whl has one. Past the budget the per-asset
// guards below still refuse unhashed wheels.
const DIGEST_WAIT_ATTEMPTS_DEFAULT = 6;
const DIGEST_WAIT_MS_DEFAULT = 5000;

const sleep = (ms: number): Promise<void> => new Promise((resolve) => setTimeout(resolve, ms));

function parseEnvInt(raw: string | undefined, fallback: number, min: number): number {
  if (raw === undefined) return fallback;
  const n = Number(raw);
  return Number.isFinite(n) ? Math.max(min, Math.trunc(n)) : fallback;
}

function countWheelsMissingDigest(assets: ReadonlyArray<{ name: string }>): number {
  let missing = 0;
  for (const asset of assets) {
    if (!asset.name.endsWith(".whl")) continue;
    const digest = (asset as { digest?: string | null }).digest;
    if (!digest || !digest.startsWith("sha256:")) missing += 1;
  }
  return missing;
}

// Fetch the release, re-polling while any .whl asset still lacks its GitHub
// digest. Errors (e.g. a 404) propagate to the caller's existing handler.
async function getReleaseWaitingForDigests(octokit: Octokit, owner: string, repo: string, releaseTag: string) {
  const attempts = parseEnvInt(process.env.OLIVER_DIGEST_WAIT_ATTEMPTS, DIGEST_WAIT_ATTEMPTS_DEFAULT, 1);
  const delayMs = parseEnvInt(process.env.OLIVER_DIGEST_WAIT_MS, DIGEST_WAIT_MS_DEFAULT, 0);
  let release = await octokit.rest.repos.getReleaseByTag({ owner, repo, tag: releaseTag });
  for (let attempt = 1; attempt < attempts; attempt += 1) {
    if (countWheelsMissingDigest(release.data.assets) === 0) break;
    await sleep(delayMs);
    release = await octokit.rest.repos.getReleaseByTag({ owner, repo, tag: releaseTag });
  }
  return release;
}

// GitHub delivers release.published + release.released (~1s apart) for one
// publish; coalesce on release identity so the duplicates don't race. The key
// is held for a short grace window after success (fast paths can finish before
// the sibling arrives) but only seconds: the minutes-later workflow_run
// delivery for the same tag must still process. A rejected run is evicted at
// once so a redelivery retry is never swallowed.
const RELEASE_COALESCE_GRACE_MS_DEFAULT = 5000;

const inFlightReleases = new Map<string, Promise<void>>();

export async function processReleaseAssets(params: ProcessReleaseAssetsParams): Promise<void> {
  const { oliverProbot, owner, repo, releaseTag } = params;
  const key = `${owner}/${repo}@${releaseTag}`;

  const running = inFlightReleases.get(key);
  if (running !== undefined) {
    oliverProbot.log.debug(
      { source_repo: `${owner}/${repo}`, release_tag: releaseTag },
      "duplicate release delivery coalesced into the in-flight run",
    );
    return;
  }

  const graceMs = parseEnvInt(
    process.env.OLIVER_RELEASE_COALESCE_MS,
    RELEASE_COALESCE_GRACE_MS_DEFAULT,
    0,
  );

  const run = processReleaseAssetsUncoalesced(params).then(
    () => {
      // Hold the key briefly so a sibling delivery arriving just after a fast
      // run finishes is still recognised as the duplicate it is.
      const timer = setTimeout(() => inFlightReleases.delete(key), graceMs);
      // Don't keep the event loop alive just for the grace window.
      if (typeof timer.unref === "function") timer.unref();
    },
    (err: unknown) => {
      inFlightReleases.delete(key);
      throw err;
    },
  );
  inFlightReleases.set(key, run);
  return run;
}

/** Test-only: clear the coalescing map so cases reusing the same repo+tag start clean. */
export function resetReleaseCoalescingForTests(): void {
  inFlightReleases.clear();
}

async function processReleaseAssetsUncoalesced({
  octokit,
  oliverProbot,
  karenProbot,
  oliverData,
  karenData,
  owner,
  repo,
  releaseTag,
  releaseSha,
}: ProcessReleaseAssetsParams): Promise<void> {
  const oliverLog = new EventLog(oliverProbot.log);
  const karenLog = new EventLog(karenProbot.log);
  const sourceRepo = `${owner}/${repo}`;

  const isBundle = releaseTag.startsWith(BUNDLE_TAG_PREFIX);

  // Single-world slug: `<slug>-<world_version>` tag prefix, provisional until
  // the asset list is known (an `.apworld` asset overrides it below). Bundles
  // derive a slug per wheel instead.
  let slug: string | undefined;
  if (!isBundle) {
    slug = slugFromTagPrefix(releaseTag);
  }

  // Path-specific parse results: exactly one is populated below.
  let single: {
    moduleLocation: string;
    wheelAssetName: string;
    wheelAssetSize: number;
    sourceManifest: Record<string, unknown>;
  } | null = null;
  let bundleWorlds: BundleWorld[] = [];

  try {
    const release = await getReleaseWaitingForDigests(octokit, owner, repo, releaseTag);
    const assets = release.data.assets;
    const wheelAssets = assets.filter((a) => a.name.endsWith(".whl"));

    if (isBundle) {
      // Per-world parsing: a bad wheel (unrecognized name or missing digest)
      // drops just that world, not the whole bundle.
      bundleWorlds = buildBundleWorlds({
        releaseTag,
        releaseSha,
        wheelAssets,
        oliverLog,
        sourceRepo,
      });
      if (bundleWorlds.length === 0) {
        oliverLog.emit({
          kind: "skip",
          source_repo: sourceRepo,
          release_tag: releaseTag,
          release_sha: releaseSha,
          reason: "bundle_no_valid_worlds",
          message: `Bundle ${releaseTag} on ${sourceRepo} had no usable world wheels; no Index PR opened.`,
        });
        return;
      }
    } else {
      // An `.apworld` asset is authoritative over the tag prefix: the Basic
      // Manual flow attaches it by hand under an arbitrary tag, so a tag/asset
      // "mismatch" is expected and the asset wins.
      const apworld = slugFromApworldAsset(assets);
      if (apworld === "ambiguous") {
        oliverLog.emit({
          kind: "skip",
          source_repo: sourceRepo,
          slug,
          release_tag: releaseTag,
          release_sha: releaseSha,
          reason: "apworld_asset_ambiguous",
          message:
            `Release ${releaseTag} on ${sourceRepo} has multiple .apworld assets; ` +
            `expected at most one to identify the world.`,
        });
        return;
      }
      if (apworld) {
        slug = apworld;
      }
      if (!slug) {
        // No wheel and no apworld: not a world release (e.g. the core app's own
        // releases); debug-log and drop so /status isn't buried. A release that
        // DID ship a wheel still reports no_slug_resolved for the author to fix.
        if (wheelAssets.length === 0 && !assets.some((a) => a.name.endsWith(".apworld"))) {
          oliverProbot.log.debug(
            { source_repo: sourceRepo, release_tag: releaseTag },
            "release has no .whl or .apworld asset; not a world release, ignoring",
          );
          return;
        }
        oliverLog.emit({
          kind: "skip",
          source_repo: sourceRepo,
          release_sha: releaseSha,
          release_tag: releaseTag,
          reason: "no_slug_resolved",
          message:
            `Cannot resolve slug for ${sourceRepo}: release tag '${releaseTag}' ` +
            `does not match '<slug>-<world_version>' and no '<name>.apworld' asset is attached.`,
        });
        return;
      }

      if (wheelAssets.length === 0) {
        oliverLog.emit({
          kind: "skip",
          source_repo: sourceRepo,
          slug,
          release_tag: releaseTag,
          release_sha: releaseSha,
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
          release_sha: releaseSha,
          reason: "wheel_asset_ambiguous",
          message:
            `Release ${releaseTag} on ${sourceRepo} has ${wheelAssets.length} .whl assets; ` +
            `expected exactly one.`,
        });
        return;
      }
      const wheelAsset = wheelAssets[0];
      // The bundled openapi-types predate the asset `digest` field; cast at the access site.
      const digest = (wheelAsset as { digest?: string | null }).digest;
      if (!digest || !digest.startsWith("sha256:")) {
        // Without a sha256 the URL points at mutable bytes; refuse to pin an
        // unverifiable module_location (the runtime relies on pip's #sha256=).
        oliverLog.emit({
          kind: "skip",
          source_repo: sourceRepo,
          slug,
          release_tag: releaseTag,
          release_sha: releaseSha,
          reason: "asset_digest_missing",
          message:
            `Release ${releaseTag} on ${sourceRepo} wheel asset ${wheelAsset.name} ` +
            `has no SHA256 digest from the GitHub API; refusing to open an Index PR ` +
            `with an unverifiable module_location.`,
        });
        return;
      }
      const sha256 = digest.slice("sha256:".length);
      single = {
        moduleLocation: `${wheelAsset.browser_download_url}#sha256=${sha256}`,
        wheelAssetName: wheelAsset.name,
        wheelAssetSize: wheelAsset.size,
        sourceManifest: {},
      };
    }
  } catch (err: unknown) {
    const status = (err as { status?: number }).status;
    if (status === 404) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        slug,
        release_tag: releaseTag,
        release_sha: releaseSha,
        reason: "release_lookup_404",
        message: `Release ${releaseTag} not found on ${sourceRepo} when fetching assets.`,
      });
      return;
    }
    throw err;
  }

  if (single) {
    single.sourceManifest = (await fetchSourceManifest(octokit, owner, repo, slug!, releaseSha)) ?? {};
  }

  const indexRepoSpec = process.env.OLIVER_INDEX_REPO ?? INDEX_REPO_DEFAULT;
  const [indexOwner, indexName] = indexRepoSpec.split("/", 2);
  if (!indexOwner || !indexName) {
    throw new Error(`Invalid OLIVER_INDEX_REPO: ${indexRepoSpec}`);
  }

  let oliverIndexInstallId: number;
  try {
    const indexInstall = await octokit.rest.apps.getRepoInstallation({
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
        release_sha: releaseSha,
        wheel_asset: single?.wheelAssetName,
        reason: "index_install_missing",
        message: `Oliver is not installed on ${indexRepoSpec}; cannot open Index PR.`,
      });
      return;
    }
    throw err;
  }

  // Karen (Contents:Write) creates the branch and commits the manifests on the
  // Index for BOTH the single-world and bundle paths; Oliver only opens/labels
  // the PR. This keeps Oliver read-only on the per-world repos it's installed on.
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
        release_sha: releaseSha,
        wheel_asset: single?.wheelAssetName,
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

    if (isBundle) {
      const result = await openOrUpdateBundleIndexPR({
        karenOctokit,
        oliverOctokit,
        karenData,
        oliverData,
        indexOwner,
        indexName,
        sourceOwner: owner,
        sourceRepo: repo,
        releaseTag,
        worlds: bundleWorlds,
      });
      for (const skippedSlug of result.skippedSlugs) {
        oliverLog.emit({
          kind: "skip",
          source_repo: sourceRepo,
          slug: skippedSlug,
          release_tag: releaseTag,
          release_sha: releaseSha,
          reason: "bundle_world_no_manifest",
          message: `World '${skippedSlug}' from bundle ${releaseTag} has no archipelago.json in its wheel; skipped (nothing to seed a manifest from).`,
        });
      }
      if (!result.opened) {
        oliverLog.emit({
          kind: "skip",
          source_repo: sourceRepo,
          release_tag: releaseTag,
          release_sha: releaseSha,
          reason: "bundle_no_valid_worlds",
          message: `Bundle ${releaseTag} on ${sourceRepo} updated no Index worlds; no PR opened.`,
        });
        return;
      }
      oliverLog.emit({
        kind: "ok",
        source_repo: sourceRepo,
        release_tag: releaseTag,
        release_sha: releaseSha,
        index_pr: result.prNumber,
        message: result.created
          ? `Opened bundle Index PR #${result.prNumber} for ${releaseTag} (${result.updatedWorldSlugs.length} worlds).`
          : `Updated bundle Index PR #${result.prNumber} for ${releaseTag} (${result.updatedWorldSlugs.length} worlds).`,
      });
    } else {
      const result = await openOrUpdateIndexPR({
        karenOctokit,
        oliverOctokit,
        karenData,
        oliverData,
        indexOwner,
        indexName,
        sourceOwner: owner,
        sourceRepo: repo,
        slug: slug!,
        releaseTag,
        moduleLocation: single!.moduleLocation,
        wheelAssetName: single!.wheelAssetName,
        wheelAssetSize: single!.wheelAssetSize,
        sourceManifest: single!.sourceManifest,
      });
      oliverLog.emit({
        kind: "ok",
        source_repo: sourceRepo,
        slug,
        release_tag: releaseTag,
        release_sha: releaseSha,
        wheel_asset: single!.wheelAssetName,
        wheel_size_bytes: single!.wheelAssetSize,
        module_location: single!.moduleLocation,
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
          release_sha: releaseSha,
          index_pr: result.prNumber,
          reason: "codeowners_conflict",
          message: `New-world PR opened, but CODEOWNERS already lists @${result.codeownersConflictWith} for worlds/${slug}.json; left untouched.`,
        });
      }
    }
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    oliverLog.emit({
      kind: "error",
      source_repo: sourceRepo,
      slug,
      release_tag: releaseTag,
      release_sha: releaseSha,
      wheel_asset: single?.wheelAssetName,
      reason: "github_api_error",
      message: `Failed to open/update Index PR: ${message}`,
    });
    throw err;
  }
}

export async function fetchSourceManifest(
  octokit: Octokit,
  owner: string,
  repo: string,
  slug: string,
  ref: string,
): Promise<Record<string, unknown> | null> {
  try {
    const res = await octokit.rest.repos.getContent({
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

// A world's Index slug: lowercase module identifier. Author-controlled names
// that become paths/branches are checked against this before use.
const APWORLD_SLUG_RE = /^[a-z0-9][a-z0-9_-]{0,63}$/;

// Slug = everything before the first '-' of a `<slug>-<world_version>` tag;
// undefined when the tag has no usable prefix.
export function slugFromTagPrefix(releaseTag: string): string | undefined {
  const dashIdx = releaseTag.indexOf("-");
  if (dashIdx > 0 && dashIdx < releaseTag.length - 1) {
    return releaseTag.slice(0, dashIdx);
  }
  return undefined;
}

// Slug from an attached `<name>.apworld` asset (the Basic Manual fork flow).
// Returns the slug for exactly one valid stem, "ambiguous" for several assets,
// null for none/invalid (caller falls back to the tag prefix).
export function slugFromApworldAsset(
  assets: ReadonlyArray<{ name: string }>,
): string | "ambiguous" | null {
  const apworldAssets = assets.filter((a) => a.name.endsWith(".apworld"));
  if (apworldAssets.length === 0) return null;
  if (apworldAssets.length > 1) return "ambiguous";
  const stem = apworldAssets[0].name.slice(0, -".apworld".length);
  return APWORLD_SLUG_RE.test(stem) ? stem : null;
}

// Bundle wheels are `worlds_<module>-<version>-py3-none-any.whl`; the Index
// slug is <module>. Null for any wheel that doesn't fit.
export function slugFromBundleWheelName(name: string): string | null {
  if (!name.startsWith("worlds_") || !name.endsWith(".whl")) return null;
  const afterPrefix = name.slice("worlds_".length);
  const dash = afterPrefix.indexOf("-");
  if (dash <= 0) return null;
  return afterPrefix.slice(0, dash);
}

// Bundle wheels -> per-world entries; an unrecognized name, duplicate slug, or
// missing digest drops just that world. Manifests are read later, from the wheel.
function buildBundleWorlds(params: {
  releaseTag: string;
  releaseSha: string;
  wheelAssets: Array<{ name: string; browser_download_url: string; size: number }>;
  oliverLog: EventLog;
  sourceRepo: string;
}): BundleWorld[] {
  const { releaseTag, releaseSha, wheelAssets, oliverLog, sourceRepo } = params;
  const worlds: BundleWorld[] = [];
  const seen = new Set<string>();

  for (const asset of wheelAssets) {
    const slug = slugFromBundleWheelName(asset.name);
    if (!slug) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        release_tag: releaseTag,
        release_sha: releaseSha,
        wheel_asset: asset.name,
        reason: "bundle_wheel_unrecognized",
        message: `Wheel ${asset.name} in bundle ${releaseTag} does not match worlds_<module>-<version>; skipping.`,
      });
      continue;
    }
    if (seen.has(slug)) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        slug,
        release_tag: releaseTag,
        release_sha: releaseSha,
        wheel_asset: asset.name,
        reason: "bundle_wheel_unrecognized",
        message: `Duplicate world slug '${slug}' in bundle ${releaseTag} (wheel ${asset.name}); skipping the duplicate.`,
      });
      continue;
    }
    const digest = (asset as { digest?: string | null }).digest;
    if (!digest || !digest.startsWith("sha256:")) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        slug,
        release_tag: releaseTag,
        release_sha: releaseSha,
        wheel_asset: asset.name,
        reason: "asset_digest_missing",
        message: `Wheel ${asset.name} for ${slug} in bundle ${releaseTag} has no SHA256 digest; skipping this world.`,
      });
      continue;
    }
    const sha256 = digest.slice("sha256:".length);
    seen.add(slug);
    worlds.push({
      slug,
      moduleLocation: `${asset.browser_download_url}#sha256=${sha256}`,
      wheelAssetName: asset.name,
      wheelAssetSize: asset.size,
    });
  }

  return worlds;
}
