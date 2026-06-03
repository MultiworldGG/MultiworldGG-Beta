// Sticky-comment splicing for Karen's fuzz results.
//
// Karen's Index PR review posts a single sticky comment marked with
// `<!-- karen-pr-review -->`. The fuzz runner (a separate repository_dispatch
// job) wants to publish its own world-generation table into that same comment
// WITHOUT clobbering the rest of Karen's review. It does so by owning a fenced
// region delimited by `<!-- karen-fuzz:start -->` / `<!-- karen-fuzz:end -->`:
// only the bytes between those markers are ever rewritten.
//
// Race-safety: the runner can finish long after the PR head has moved on (a new
// push supersedes this run). We re-fetch the comment body immediately before
// patching it to splice against the freshest text, and we no-op entirely when
// pulls.get reports a head SHA other than the one this run was dispatched for —
// a stale run must never stomp the comment a newer run is writing.

import type { ProbotOctokit } from "probot";
import type { FuzzWorldResult } from "./types";

export const FUZZ_REGION_START = "<!-- karen-fuzz:start -->";
export const FUZZ_REGION_END = "<!-- karen-fuzz:end -->";

const STATUS_GLYPH: Record<FuzzWorldResult["status"], string> = {
  pass: "✅",
  warn: "⚠️",
  fail: "❌",
};

// Legend wording mirrors `.github/workflows/karen-pr-review.yml` so the fenced
// region reads identically whether the workflow or this code authored it.
const LEGEND =
  "_Legend: ✅ generated · ⚠️ no-op (all option-rejected, or ROM/output unavailable on CI) · ❌ failed._";

export interface UpsertFuzzCommentParams {
  owner: string;
  repo: string;
  prNumber: number;
  /** Sticky-comment marker, e.g. "<!-- karen-pr-review -->". */
  marker: string;
  /** The PR head SHA this fuzz run was dispatched for; patch is skipped if it moved. */
  headSha: string;
  /** Caller-built markdown to place between the fuzz region markers. */
  region: string;
}

/**
 * Render the fenced fuzz region body (markers + a per-world table + legend) for
 * a set of results. Pure: no I/O, deterministic, safe to unit-test directly.
 */
export function renderFuzzRegion(results: FuzzWorldResult[]): string {
  const lines: string[] = ["### World generation (fuzzer) results", ""];

  if (results.length === 0) {
    lines.push("_No worlds were fuzzed._");
  } else {
    lines.push("| World | Verdict | Details |", "| --- | :---: | --- |");
    for (const r of results) {
      lines.push(`| \`${r.slug}\` | ${STATUS_GLYPH[r.status]} | ${formatDetail(r)} |`);
    }
    lines.push("", LEGEND);
  }

  return lines.join("\n");
}

/**
 * Prefer the explicit per-world stats line; fall back to the human `detail`
 * summary; otherwise emit an em dash so the table cell is never blank.
 */
function formatDetail(r: FuzzWorldResult): string {
  const statsLine = r.stats ? formatStats(r.stats) : "";
  const detail = r.detail.trim();
  if (statsLine && detail) return `${escapeCell(detail)} (${escapeCell(statsLine)})`;
  if (statsLine) return escapeCell(statsLine);
  if (detail) return escapeCell(detail);
  return "—";
}

function formatStats(stats: Record<string, number>): string {
  const parts = Object.entries(stats).map(([k, v]) => `${k}=${v}`);
  return parts.join(" ");
}

/** Keep table-breaking characters from leaking into a Markdown cell. */
function escapeCell(text: string): string {
  return text.replace(/\|/g, "\\|").replace(/\r?\n/g, " ");
}

/**
 * Replace the fuzz region inside `body` with `region`, returning the new body.
 * - Both markers present: splice the content between them (markers preserved).
 * - Markers absent: append a fresh fenced region after the existing body.
 */
function spliceRegion(body: string, region: string): string {
  const start = body.indexOf(FUZZ_REGION_START);
  const end = body.indexOf(FUZZ_REGION_END);

  if (start !== -1 && end !== -1 && end > start) {
    const before = body.slice(0, start + FUZZ_REGION_START.length);
    const after = body.slice(end);
    return `${before}\n${region}\n${after}`;
  }

  const fenced = `${FUZZ_REGION_START}\n${region}\n${FUZZ_REGION_END}`;
  const sep = body.length === 0 || body.endsWith("\n") ? "" : "\n";
  return `${body}${sep}\n${fenced}\n`;
}

/** A brand-new sticky comment: marker line followed by the fenced fuzz region. */
function freshComment(marker: string, region: string): string {
  return `${marker}\n\n${FUZZ_REGION_START}\n${region}\n${FUZZ_REGION_END}\n`;
}

/**
 * Upsert Karen's fuzz region into the PR's sticky comment.
 *
 * Finds the first issue comment whose body starts with `marker`, then rewrites
 * ONLY its fenced fuzz region with `region`. If the marker comment is missing
 * one, the region is appended; if no marker comment exists at all, a minimal
 * one is created. No-ops when the PR head has advanced past `headSha`.
 */
export async function upsertFuzzComment(
  octokit: ProbotOctokit,
  params: UpsertFuzzCommentParams,
): Promise<void> {
  const { owner, repo, prNumber, marker, headSha, region } = params;

  // Bail before any write if this run is stale: the head moved, so a newer run
  // owns the comment now.
  const pull = await octokit.rest.pulls.get({ owner, repo, pull_number: prNumber });
  if (pull.data.head.sha !== headSha) {
    return;
  }

  const comments = await octokit.rest.issues.listComments({
    owner,
    repo,
    issue_number: prNumber,
  });
  const sticky = comments.data.find((c) => (c.body ?? "").startsWith(marker));

  if (!sticky) {
    await octokit.rest.issues.createComment({
      owner,
      repo,
      issue_number: prNumber,
      body: freshComment(marker, region),
    });
    return;
  }

  // Re-fetch the comment immediately before patching so we splice against the
  // freshest body — another job may have edited it since listComments.
  const fresh = await octokit.rest.issues.getComment({
    owner,
    repo,
    comment_id: sticky.id,
  });
  const currentBody = fresh.data.body ?? "";

  await octokit.rest.issues.updateComment({
    owner,
    repo,
    comment_id: sticky.id,
    body: spliceRegion(currentBody, region),
  });
}
