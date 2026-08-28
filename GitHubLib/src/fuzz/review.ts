// Karen's FINAL PR review: submitted by the bot after the isolated checks
// conclude, gating on both the manifest verdict and the fuzz rollup. The Index
// workflow only reviews synchronously on the no-fuzz path.

import type { ProbotOctokit } from "probot";

export type ReviewEvent = "APPROVE" | "REQUEST_CHANGES";

export interface FuzzReviewDecision {
  event: ReviewEvent;
  body: string;
}

/**
 * Karen's final review:
 *   - fuzz "fail" OR manifest "fail"      -> REQUEST_CHANGES
 *   - manifest "pass" and fuzz pass/warn  -> APPROVE (warn = non-blocking)
 *   - otherwise                           -> null (no review)
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

  // Manifest warn/unknown with non-failing isolated checks: leave the PR unreviewed.
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
