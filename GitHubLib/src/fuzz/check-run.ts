// GitHub Check-Run helpers for the Karen fuzz/scan feature.
//
// Karen surfaces each fuzz+scan run as a single Check Run pinned to the PR's
// head SHA, so the result rides the commit (and the org-ruleset required-check
// gate) rather than living only in a PR comment. The runner drives one through
// its lifecycle: create (queued) -> start (in_progress) -> complete (with a
// conclusion). `findFuzzCheckRunForHead` lets a re-dispatched run reconcile
// onto the Check Run an earlier attempt already created for the same head,
// instead of stacking duplicates.
//
// Every function takes a Karen-authed installation octokit (the same
// `ProbotOctokit` obtained via `karenProbot.auth(installId)` in
// handlers/shared.ts and threaded into index-pr.ts) plus a plain
// {owner, repo, ...} bag. The App needs the `checks:write` permission.

import type { ProbotOctokit } from "probot";

import type { FuzzWorldResult } from "./types";

/** Terminal Check Run conclusion we report. "neutral" is intentionally not red. */
export type FuzzConclusion = "success" | "failure" | "neutral";

export interface CreateFuzzCheckRunParams {
  owner: string;
  repo: string;
  /** Check Run name, e.g. "Karen / fuzz". Must match for later reconciliation. */
  name: string;
  /** 40-hex commit SHA the run is pinned to (the PR head). */
  headSha: string;
}

export interface StartFuzzCheckRunParams {
  owner: string;
  repo: string;
  checkRunId: number;
}

export interface CompleteFuzzCheckRunParams {
  owner: string;
  repo: string;
  checkRunId: number;
  conclusion: FuzzConclusion;
  /** Output title line shown in the Checks tab. */
  title: string;
  /** Short markdown summary (the table header / one-liner). */
  summary: string;
  /** Optional long-form markdown body (per-world detail). */
  text?: string;
}

export interface FindFuzzCheckRunForHeadParams {
  owner: string;
  repo: string;
  name: string;
  headSha: string;
}

/**
 * Create the Check Run for a fuzz dispatch in the `queued` state, pinned to
 * `headSha`. Returns the new check_run_id the runner threads through the rest
 * of the lifecycle.
 */
export async function createFuzzCheckRun(
  octokit: ProbotOctokit,
  { owner, repo, name, headSha }: CreateFuzzCheckRunParams,
): Promise<number> {
  const res = await octokit.rest.checks.create({
    owner,
    repo,
    name,
    head_sha: headSha,
    status: "queued",
  });
  return res.data.id;
}

/** Move an existing Check Run into `in_progress` (work has started). */
export async function startFuzzCheckRun(
  octokit: ProbotOctokit,
  { owner, repo, checkRunId }: StartFuzzCheckRunParams,
): Promise<void> {
  await octokit.rest.checks.update({
    owner,
    repo,
    check_run_id: checkRunId,
    status: "in_progress",
  });
}

/**
 * Finalize a Check Run: set `status: "completed"` with the aggregate
 * `conclusion` and an output block. GitHub requires `completed_at`/conclusion
 * together; we let the API stamp `completed_at`.
 */
export async function completeFuzzCheckRun(
  octokit: ProbotOctokit,
  { owner, repo, checkRunId, conclusion, title, summary, text }: CompleteFuzzCheckRunParams,
): Promise<void> {
  await octokit.rest.checks.update({
    owner,
    repo,
    check_run_id: checkRunId,
    status: "completed",
    conclusion,
    output: { title, summary, text },
  });
}

/**
 * Find an existing fuzz Check Run on `headSha` by name, for restart
 * reconciliation / reuse. Returns the most-recently-created match's id, or null
 * when none exists. Matching the name keeps Karen's run distinct from any other
 * App's checks on the same commit.
 */
export async function findFuzzCheckRunForHead(
  octokit: ProbotOctokit,
  { owner, repo, name, headSha }: FindFuzzCheckRunForHeadParams,
): Promise<number | null> {
  const res = await octokit.rest.checks.listForRef({
    owner,
    repo,
    ref: headSha,
    check_name: name,
  });
  const runs = res.data.check_runs;
  if (runs.length === 0) return null;
  // listForRef can page; for a single named check the count is tiny, but be
  // deterministic and prefer the newest id so a reconciling re-dispatch lands
  // on the latest attempt rather than a stale one.
  let best = runs[0];
  for (const run of runs) {
    if (run.id > best.id) best = run;
  }
  return best.id;
}

/**
 * Reduce per-world results to the Check Run conclusion + the rollup status used
 * in the PR comment. Precedence (a warn never masks a fail; neutral is never
 * red):
 *   - any "fail"            -> { conclusion: "failure", status: "fail" }
 *   - else any "warn"       -> { conclusion: "neutral", status: "warn" }
 *   - else (all pass/empty) -> { conclusion: "success", status: "pass" }
 */
export function aggregateConclusion(
  results: FuzzWorldResult[],
): { conclusion: FuzzConclusion; status: "pass" | "warn" | "fail" } {
  if (results.some((r) => r.status === "fail")) {
    return { conclusion: "failure", status: "fail" };
  }
  if (results.some((r) => r.status === "warn")) {
    return { conclusion: "neutral", status: "warn" };
  }
  return { conclusion: "success", status: "pass" };
}
