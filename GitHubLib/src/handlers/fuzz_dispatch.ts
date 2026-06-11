// repository_dispatch handler for the Karen fuzz/scan feature.
//
// A karen-fuzz repository_dispatch (Karen-signed, delivered to /karen by the
// dedicated webhook in karen-webhook.ts) asks the bot to fuzz+scan one or more
// apworlds for a PR head and report the verdict as a Check Run + sticky comment
// region on the Index PR.
//
// This handler validates the (defensively-untrusted) client_payload, authes as
// Karen against the Index, creates/reuses the head-pinned Check Run, then
// ENQUEUES the long fuzz on the in-process FuzzQueue and RETURNS immediately so
// the webhook HTTP response is not held open past GitHub's ~10s timeout. The
// queued task drives the worlds through runFuzzContainer, aggregates the
// conclusion, completes the Check Run, and upserts the comment region — all
// asynchronously. Nothing in here is allowed to throw: a bad payload, a wrong
// repo, or a container crash is logged via EventLog and swallowed.

import type { Probot, ProbotOctokit } from "probot";

import { EventLog } from "../event-log";
import { INDEX_REPO_DEFAULT } from "./shared";
import {
  aggregateConclusion,
  completeFuzzCheckRun,
  createFuzzCheckRun,
  findFuzzCheckRunForHead,
  startFuzzCheckRun,
  type FuzzConclusion,
} from "../fuzz/check-run";
import { renderFuzzRegion, upsertFuzzComment } from "../fuzz/comment";
import { decideFuzzReview, submitFuzzReview } from "../fuzz/review";
import { toFuzzJob, validateFuzzPayload } from "../fuzz/payload";
import { getFuzzQueue } from "../fuzz/queue";
import { ensureImageAvailable, runFuzzContainer, type RunFuzzOptions } from "../fuzz/runner";
import type { FuzzClientPayload, FuzzWorldResult } from "../fuzz/types";

export interface HandleRepositoryDispatchArgs {
  karenProbot: Probot;
  oliverData: any;
  karenData: any;
  payload: any;
  log: any;
}

/** Wrap a Probot logger into the plain `(message) => void` the runner expects. */
function asRunnerLog(log: any): (m: string) => void {
  return (m: string) => {
    if (log && typeof log.info === "function") log.info(m);
  };
}

/** Read a string env var (FUZZ_, MWGG_, FUZZER_), falling back to `def` when unset/blank. */
function envStr(name: string, def: string): string {
  const raw = process.env[name];
  return raw !== undefined && raw.trim() !== "" ? raw : def;
}

function envNum(name: string, def: number): number {
  const raw = process.env[name];
  if (raw === undefined || raw.trim() === "") return def;
  const parsed = Number.parseInt(raw, 10);
  return Number.isFinite(parsed) ? parsed : def;
}

/** Optional string env var: undefined when unset/blank (so the mount is omitted). */
function envOpt(name: string): string | undefined {
  const raw = process.env[name];
  return raw !== undefined && raw.trim() !== "" ? raw : undefined;
}

/** Optional int env var: undefined when unset/blank/non-numeric (so the cap is off). */
function envOptNum(name: string): number | undefined {
  const raw = process.env[name];
  if (raw === undefined || raw.trim() === "") return undefined;
  const parsed = Number.parseInt(raw, 10);
  return Number.isFinite(parsed) ? parsed : undefined;
}

/** Truthy env flag: 1/true/yes/on (case-insensitive) → true; otherwise `def`. */
function envBool(name: string, def: boolean): boolean {
  const raw = process.env[name];
  if (raw === undefined || raw.trim() === "") return def;
  return /^(1|true|yes|on)$/i.test(raw.trim());
}

/** Assemble the runner options for one batch from the process environment. */
function runnerOptionsFromEnv(
  log: (m: string) => void,
  signal: AbortSignal,
): RunFuzzOptions {
  return {
    // Defaults mirror deploy/docker-compose.yml's github-bots env so a missing
    // var falls back to the same value prod sets explicitly. The container is
    // `--network none`: core/fuzzer/deps are baked into FUZZ_IMAGE at build time,
    // so there's no FUZZ_NET / MWGG_CORE_* / FUZZER_* to pass.
    image: envStr("FUZZ_IMAGE", "ghcr.io/multiworldgg/multiworldgg-fuzz:latest"),
    workDir: envStr("FUZZ_WORK_DIR", "/var/lib/mwgg-fuzz"),
    cpus: envStr("FUZZ_CPUS", "2"),
    memory: envStr("FUZZ_MEMORY", "4g"),
    pids: envNum("FUZZ_PIDS", 512),
    // Operator ceilings on the fuzzer -j / -r so a small host bounds resource use
    // no matter what the Index dispatch asked for. Unset → use the payload value.
    maxThreads: envOptNum("FUZZ_MAX_THREADS"),
    maxRuns: envOptNum("FUZZ_MAX_RUNS"),
    wallSeconds: envNum("FUZZ_WALL_SECONDS", 1200),
    // Optional RO mounts so ROM-dependent worlds can generate; unset → no mount.
    romDir: envOpt("FUZZ_ROM_DIR"),
    hostYaml: envOpt("FUZZ_HOST_YAML"),
    // Opt-in: persist each container's full log + worker dumps and keep the
    // per-job dir for inspection. Off by default; see deploy/docker-compose.yml.
    debug: envBool("FUZZ_DEBUG", false),
    log,
    signal,
  };
}

/**
 * Handle a repository_dispatch delivery. Silently ignores non-karen-fuzz
 * actions; for karen-fuzz it validates, authes, creates the Check Run, and
 * enqueues the fuzz, then returns promptly. Never throws.
 */
export async function handleRepositoryDispatch(args: HandleRepositoryDispatchArgs): Promise<void> {
  const { karenProbot, payload, log } = args;
  const eventLog = new EventLog(karenProbot.log);

  if (payload?.action !== "karen-fuzz") {
    // Other repository_dispatch types are not ours; ignore without noise.
    return;
  }

  const parsed = validateFuzzPayload(payload.action, payload.client_payload);
  if (!parsed.ok) {
    eventLog.emit({
      kind: "error",
      source_repo: String(payload?.repository?.full_name ?? "unknown"),
      reason: "fuzz_bad_payload",
      message: `Rejected karen-fuzz dispatch: ${parsed.errors.join("; ")}`,
    });
    return;
  }
  const fuzz = parsed.value;

  const indexRepoSpec = process.env.OLIVER_INDEX_REPO ?? INDEX_REPO_DEFAULT;
  const deliveredRepo = payload?.repository?.full_name;
  if (fuzz.index_repo !== indexRepoSpec || (deliveredRepo && deliveredRepo !== indexRepoSpec)) {
    eventLog.emit({
      kind: "error",
      source_repo: String(deliveredRepo ?? fuzz.index_repo),
      pr_number: fuzz.pr_number,
      reason: "fuzz_not_index_repo",
      message:
        `karen-fuzz dispatch targets ${fuzz.index_repo} (delivered from ` +
        `${deliveredRepo ?? "?"}); expected ${indexRepoSpec}. Ignoring.`,
    });
    return;
  }

  const [owner, repo] = indexRepoSpec.split("/", 2);
  if (!owner || !repo) {
    eventLog.emit({
      kind: "error",
      source_repo: indexRepoSpec,
      pr_number: fuzz.pr_number,
      reason: "fuzz_not_index_repo",
      message: `Invalid OLIVER_INDEX_REPO: ${indexRepoSpec}`,
    });
    return;
  }

  // Auth as Karen against the Index (shared.ts pattern): app JWT -> installation
  // id for owner/repo -> installation-scoped octokit.
  let octokit: ProbotOctokit;
  try {
    const karenApp = await karenProbot.auth();
    const install = await karenApp.rest.apps.getRepoInstallation({ owner, repo });
    octokit = await karenProbot.auth(install.data.id);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    eventLog.emit({
      kind: "error",
      source_repo: indexRepoSpec,
      pr_number: fuzz.pr_number,
      reason: "fuzz_check_run_error",
      message: `Karen could not auth against ${indexRepoSpec}: ${message}`,
    });
    return;
  }

  // Create (or reuse) the head-pinned Check Run before enqueueing so the PR
  // shows a queued check even while the batch waits for a slot.
  let checkRunId: number;
  try {
    const existing = await findFuzzCheckRunForHead(octokit, {
      owner,
      repo,
      name: fuzz.check_run_name,
      headSha: fuzz.head_sha,
    });
    checkRunId =
      existing ??
      (await createFuzzCheckRun(octokit, {
        owner,
        repo,
        name: fuzz.check_run_name,
        headSha: fuzz.head_sha,
      }));
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    eventLog.emit({
      kind: "error",
      source_repo: indexRepoSpec,
      pr_number: fuzz.pr_number,
      reason: "fuzz_check_run_error",
      message: `Failed to create/reuse fuzz Check Run on ${fuzz.head_sha}: ${message}`,
    });
    return;
  }

  eventLog.emit({
    kind: "ok",
    source_repo: indexRepoSpec,
    pr_number: fuzz.pr_number,
    release_sha: fuzz.head_sha,
    message: `Enqueued karen-fuzz for PR #${fuzz.pr_number} (${fuzz.worlds.length} world(s)) on ${fuzz.head_sha}.`,
  });

  const runnerLog = asRunnerLog(log);
  const key = `${fuzz.pr_number}:${fuzz.head_sha}`;

  // Enqueue and DO NOT await: the webhook response must not be held open for the
  // duration of the fuzz. The queue finalizes the Check Run + comment itself.
  void getFuzzQueue()
    .run(key, (signal) =>
      runFuzzBatch({ octokit, owner, repo, fuzz, checkRunId, eventLog, runnerLog, signal }),
    )
    .catch((err: unknown) => {
      // A superseded batch (newer push) or any unexpected queue error lands here.
      // It is already accounted for inside runFuzzBatch on the run path; this only
      // catches pre-start supersede/close so the rejection is never unhandled.
      const message = err instanceof Error ? err.message : String(err);
      karenProbot.log.warn(
        { pr_number: fuzz.pr_number, head_sha: fuzz.head_sha },
        `karen-fuzz batch for ${key} did not run: ${message}`,
      );
    });
}

interface RunFuzzBatchArgs {
  octokit: ProbotOctokit;
  owner: string;
  repo: string;
  fuzz: FuzzClientPayload;
  checkRunId: number;
  eventLog: EventLog;
  runnerLog: (m: string) => void;
  signal: AbortSignal;
}

/** Conclusion-title text for the completed Check Run. */
function conclusionTitle(status: "pass" | "warn" | "fail", count: number): string {
  if (status === "fail") return `Fuzz failed for ${count} world(s)`;
  if (status === "warn") return `Fuzz passed with warnings for ${count} world(s)`;
  return `Fuzz passed for ${count} world(s)`;
}

/**
 * The enqueued unit of work: mark the Check Run in_progress, fuzz every world
 * (each container call isolated so one crash never aborts the batch), aggregate,
 * complete the Check Run, and upsert the comment region. Resolves regardless of
 * per-world outcome; only re-raises nothing — all errors are logged here.
 */
async function runFuzzBatch(a: RunFuzzBatchArgs): Promise<void> {
  const { octokit, owner, repo, fuzz, checkRunId, eventLog, runnerLog, signal } = a;
  const indexRepoSpec = `${owner}/${repo}`;

  try {
    await startFuzzCheckRun(octokit, { owner, repo, checkRunId });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    eventLog.emit({
      kind: "error",
      source_repo: indexRepoSpec,
      pr_number: fuzz.pr_number,
      reason: "fuzz_check_run_error",
      message: `Could not move fuzz Check Run to in_progress: ${message}`,
    });
    // Keep going — we still want to attempt the fuzz and the final completion.
  }

  const options = runnerOptionsFromEnv(runnerLog, signal);
  const results: FuzzWorldResult[] = [];

  // One-time pre-flight: a missing FUZZ_IMAGE would 125 every world with a
  // cryptic "no result.json". Inspect-or-pull once; if it's truly unavailable,
  // every world fails fast below with one actionable reason instead of N 125s.
  const preflight = await ensureImageAvailable(options.image, runnerLog);
  if (!preflight.ok) {
    eventLog.emit({
      kind: "error",
      source_repo: indexRepoSpec,
      pr_number: fuzz.pr_number,
      reason: "fuzz_image_unavailable",
      message:
        `FUZZ_IMAGE ${options.image} is not available on the host (${preflight.detail ?? "not present"}); ` +
        `pull or build it — see deploy/README.md. Failing all ${fuzz.worlds.length} world(s).`,
    });
  }

  for (const world of fuzz.worlds) {
    const job = toFuzzJob(fuzz, world);
    if (!preflight.ok) {
      results.push({
        slug: job.slug,
        status: "fail",
        detail: `${job.slug}: FUZZ_IMAGE ${options.image} unavailable — ${preflight.detail ?? "not present"}`,
        exitCode: 125,
        timedOut: false,
      });
      continue;
    }
    try {
      const result = await runFuzzContainer(job, options);
      results.push(result);
      if (result.timedOut) {
        eventLog.emit({
          kind: "skip",
          source_repo: indexRepoSpec,
          pr_number: fuzz.pr_number,
          slug: job.slug,
          reason: "fuzz_timeout",
          message: `Fuzz container for ${job.slug} timed out and was force-removed.`,
        });
      }
    } catch (err: unknown) {
      // runFuzzContainer only rejects on truly-unexpected internal errors; record
      // a synthetic fail so the world still appears in the table and the batch
      // continues.
      const message = err instanceof Error ? err.message : String(err);
      eventLog.emit({
        kind: "error",
        source_repo: indexRepoSpec,
        pr_number: fuzz.pr_number,
        slug: job.slug,
        reason: "fuzz_container_error",
        message: `Fuzz container for ${job.slug} crashed unexpectedly: ${message}`,
      });
      results.push({
        slug: job.slug,
        status: "fail",
        detail: `${job.slug}: internal error: ${message}`,
        exitCode: 1,
        timedOut: false,
      });
    }
  }

  const { conclusion, status } = aggregateConclusion(results);

  await completeBatchCheckRun(octokit, owner, repo, checkRunId, conclusion, status, results, eventLog, fuzz);

  try {
    await upsertFuzzComment(octokit, {
      owner,
      repo,
      prNumber: fuzz.pr_number,
      marker: fuzz.comment_marker,
      headSha: fuzz.head_sha,
      region: renderFuzzRegion(results),
      // Karen's isolated checks live in their OWN sticky comment, separate from
      // her manifest review; this heading titles it when the bot creates it.
      title: "Karen: Isolated QA Checks",
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    eventLog.emit({
      kind: "error",
      source_repo: indexRepoSpec,
      pr_number: fuzz.pr_number,
      reason: "fuzz_check_run_error",
      message: `Failed to upsert fuzz comment region: ${message}`,
    });
  }

  // Karen's FINAL verdict lands AFTER the isolated checks — the whole reason they
  // run in the bot. Approve only when the manifest checks (verdict from the
  // dispatch payload) AND these isolated checks are green; request changes when
  // either is red. (The workflow only reviews synchronously on the no-fuzz path.)
  // Guard on the PR head exactly like the comment splice: a batch that finished
  // after a newer push must NOT land a stale APPROVE on now-superseded code — the
  // newer batch owns the review (the queue keys on head_sha, so it ran separately).
  try {
    const decision = decideFuzzReview(fuzz.manifest_status, status);
    if (decision) {
      const pull = await octokit.rest.pulls.get({ owner, repo, pull_number: fuzz.pr_number });
      if (pull.data.head.sha === fuzz.head_sha) {
        await submitFuzzReview(octokit, {
          owner,
          repo,
          prNumber: fuzz.pr_number,
          event: decision.event,
          body: decision.body,
        });
      } else {
        eventLog.emit({
          kind: "skip",
          source_repo: indexRepoSpec,
          pr_number: fuzz.pr_number,
          release_sha: fuzz.head_sha,
          message: "Skipped Karen's final review: PR head moved since dispatch.",
        });
      }
    }
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    eventLog.emit({
      kind: "error",
      source_repo: indexRepoSpec,
      pr_number: fuzz.pr_number,
      reason: "fuzz_check_run_error",
      message: `Failed to submit Karen's final review: ${message}`,
    });
  }

  eventLog.emit({
    kind: status === "fail" ? "error" : "ok",
    source_repo: indexRepoSpec,
    pr_number: fuzz.pr_number,
    release_sha: fuzz.head_sha,
    fuzz_status: status,
    reason: status === "fail" ? "fuzz_overall_fail" : undefined,
    message: `karen-fuzz verdict for PR #${fuzz.pr_number}: ${status} (${results.length} world(s)).`,
  });
}

/** Complete the Check Run, logging (never throwing) on failure. */
async function completeBatchCheckRun(
  octokit: ProbotOctokit,
  owner: string,
  repo: string,
  checkRunId: number,
  conclusion: FuzzConclusion,
  status: "pass" | "warn" | "fail",
  results: FuzzWorldResult[],
  eventLog: EventLog,
  fuzz: FuzzClientPayload,
): Promise<void> {
  try {
    await completeFuzzCheckRun(octokit, {
      owner,
      repo,
      checkRunId,
      conclusion,
      title: conclusionTitle(status, results.length),
      summary: renderFuzzRegion(results),
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    eventLog.emit({
      kind: "error",
      source_repo: `${owner}/${repo}`,
      pr_number: fuzz.pr_number,
      reason: "fuzz_check_run_error",
      message: `Failed to complete fuzz Check Run: ${message}`,
    });
  }
}
