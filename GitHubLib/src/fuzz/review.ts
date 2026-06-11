// Karen's FINAL PR review for the fuzz/scan feature.
//
// The manifest checks run synchronously in the Index workflow, but the isolated
// checks (fuzz/scan) finish asynchronously here in the bot. So Karen's
// APPROVE / REQUEST_CHANGES is submitted by the bot AFTER the isolated checks
// conclude — gating on BOTH the manifest verdict (passed in via the dispatch
// payload's manifest_status) and the fuzz rollup. The Index workflow only
// reviews synchronously on the no-fuzz path (schema-only / non-wheel worlds),
// where there are no isolated checks to wait for.
//
// Authed as Karen (the same installation octokit the rest of the feature uses);
// submitting a review needs the App's pull_requests:write permission — already
// held, since the workflow's Karen token submits reviews today.

import type { ProbotOctokit } from "probot";

export type ReviewEvent = "APPROVE" | "REQUEST_CHANGES";

export interface FuzzReviewDecision {
  event: ReviewEvent;
  body: string;
}

/**
 * Decide Karen's final review from the manifest verdict + the fuzz rollup.
 * Mirrors the workflow's old gate (approve only on a clean manifest "pass"), but
 * now also requires the isolated checks to be non-failing:
 *   - fuzz "fail" OR manifest "fail"      -> REQUEST_CHANGES (cite what's red)
 *   - manifest "pass" and fuzz pass/warn  -> APPROVE (warn = non-blocking)
 *   - otherwise (manifest warn/unknown,
 *     fuzz not failing)                   -> null: no review, matching the old
 *                                            "neither approve nor block" behavior
 */
export function decideFuzzReview(
  manifestStatus: string,
  fuzzStatus: "pass" | "warn" | "fail",
): FuzzReviewDecision | null {
  const manifestFail = manifestStatus === "fail";
  const fuzzFail = fuzzStatus === "fail";

  if (fuzzFail || manifestFail) {
    const reasons: string[] = [];
    if (manifestFail) reasons.push("the manifest checks");
    if (fuzzFail) reasons.push("the isolated QA checks (fuzz/scan)");
    return {
      event: "REQUEST_CHANGES",
      body:
        `Karen can't sign off yet — ${reasons.join(" and ")} did not pass. ` +
        `See Karen's review and the Isolated QA Checks comment for the breakdown.`,
    };
  }

  if (manifestStatus === "pass") {
    const warnNote =
      fuzzStatus === "warn"
        ? " The isolated checks passed with warnings worth a glance, but nothing blocking."
        : "";
    return {
      event: "APPROVE",
      body: `APPROVED: the manifest checks and the isolated QA checks (fuzz/scan) are both green, awesome job!${warnNote}`,
    };
  }

  // Manifest is warn/unknown and the isolated checks aren't failing: leave the PR
  // unreviewed, exactly as the synchronous workflow used to on a non-pass-non-fail.
  return null;
}

export interface SubmitFuzzReviewParams {
  owner: string;
  repo: string;
  prNumber: number;
  event: ReviewEvent;
  body: string;
}

/** Submit Karen's review on the PR. The App needs pull_requests:write. */
export async function submitFuzzReview(
  octokit: ProbotOctokit,
  { owner, repo, prNumber, event, body }: SubmitFuzzReviewParams,
): Promise<void> {
  await octokit.rest.pulls.createReview({
    owner,
    repo,
    pull_number: prNumber,
    event,
    body,
  });
}
