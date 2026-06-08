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

// Same glyphs Karen's review uses, so the fuzz region reads identically. Includes
// scan-only statuses (skip); a status with no glyph renders as the bare word.
const STATUS_GLYPH: Record<string, string> = {
  pass: "✅",
  warn: "⚠️",
  fail: "❌",
  skip: "⏭️",
};

/** "{glyph} {status}" cell like Karen's review; bare word when no glyph maps. */
function statusLabel(status: string): string {
  const glyph = STATUS_GLYPH[status];
  return glyph ? `${glyph} ${status}` : status;
}

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
  /**
   * Optional `## {title}` heading written ABOVE the fenced region when the bot
   * has to CREATE the sticky comment (the isolated-checks comment is Karen's own,
   * separate from her manifest review). It lives outside the fence, so region
   * updates never clobber it. Omitted → no heading (legacy splice-into-Karen mode).
   */
  title?: string;
}

/**
 * Render the fenced fuzz region as per-world sections that mirror Karen's review
 * tables: a `#### \`slug\` — {glyph} {status}` heading then a
 * `| Check | Status | Notes |` table with glyph+word status cells. Each world
 * lists its generation verdict (with stats) plus the per-check scan statuses.
 * Pure: no I/O, deterministic, safe to unit-test directly.
 */
export function renderFuzzRegion(results: FuzzWorldResult[]): string {
  const lines: string[] = ["### World generation (fuzzer) results", ""];

  if (results.length === 0) {
    lines.push("_No worlds were fuzzed._");
    return lines.join("\n");
  }

  for (const r of results) {
    lines.push(`#### \`${r.slug}\` — ${statusLabel(r.status)}`, "");
    lines.push("| Check | Status | Notes |", "| --- | --- | --- |");
    lines.push(`| \`fuzzer\` | ${statusLabel(r.status)} | ${escapeCell(fuzzerNotes(r))} |`);
    for (const [label, status, note] of scanRows(r.scan)) {
      lines.push(`| \`${label}\` | ${escapeCell(statusLabel(status))} | ${escapeCell(note)} |`);
    }
    lines.push("");
  }

  return lines.join("\n");
}

/**
 * The `fuzzer` row's Notes: the stats line (success=… total=…) and/or the
 * human `detail` tail; an em dash when neither is present. (Caller escapes it.)
 */
function fuzzerNotes(r: FuzzWorldResult): string {
  const statsLine = r.stats ? formatStats(r.stats) : "";
  const detail = r.detail.trim();
  if (statsLine && detail) return `${detail} (${statsLine})`;
  return statsLine || detail || "—";
}

function formatStats(stats: Record<string, number>): string {
  const parts = Object.entries(stats).map(([k, v]) => `${k}=${v}`);
  return parts.join(" ");
}

// Short check labels (no_network_at_import -> net, …) for the scan rows.
const SCAN_LABELS: Record<string, string> = {
  bandit: "bandit",
  pip_audit: "pip-audit",
  size_sanity: "size",
  no_rom_files: "rom",
  no_network_at_import: "net",
  ruff: "ruff",
  sha256: "sha256",
};

/**
 * One [label, status, note] row per scan check, mirroring Karen's per-check rows.
 * The container records each check in result.json.scan as `{status, note}`, where
 * `note` is karen_review's human message (e.g. "a very reasonable 5.2MB / cap
 * 250MB") — the raw scan.json/ruff.json findings themselves aren't available
 * bot-side (they live in the /out dir, reclaimed after the run). A legacy
 * bare-string value is read as the status with an empty note; any other shape is
 * JSON-encoded so it can't break a row. An absent scan yields no rows.
 */
function scanRows(scan: Record<string, unknown> | undefined): Array<[string, string, string]> {
  if (!scan) return [];
  return Object.entries(scan).map(([key, value]) => {
    const label = SCAN_LABELS[key] ?? key;
    if (value && typeof value === "object" && !Array.isArray(value)) {
      const v = value as Record<string, unknown>;
      const status = typeof v.status === "string" ? v.status : JSON.stringify(v);
      const note = typeof v.note === "string" ? v.note : "";
      return [label, status, note];
    }
    return [label, typeof value === "string" ? value : JSON.stringify(value), ""];
  });
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

/**
 * A brand-new sticky comment: marker line, an optional `## {title}` heading, then
 * the fenced fuzz region. The heading sits OUTSIDE the fence so later region
 * splices preserve it.
 */
function freshComment(marker: string, region: string, title?: string): string {
  const header = title ? `${marker}\n\n## ${title}\n\n` : `${marker}\n\n`;
  return `${header}${FUZZ_REGION_START}\n${region}\n${FUZZ_REGION_END}\n`;
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
  const { owner, repo, prNumber, marker, headSha, region, title } = params;

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
      body: freshComment(marker, region, title),
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
