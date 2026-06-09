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

  // Track the running size: a big multi-world PR (up to 25 worlds, some with
  // thousands of ruff diagnostics) could render a region past GitHub's ~65 KB
  // comment/check-run limit, which fails the API call outright. The per-world
  // tables are always emitted; only the collapsible Findings blocks are dropped
  // once the budget is hit, so the verdict survives even when detail can't.
  let total = charLen(lines);
  let findingsTruncated = false;

  for (const r of results) {
    const head = [
      `#### \`${r.slug}\` — ${statusLabel(r.status)}`,
      "",
      "| Check | Status | Notes |",
      "| --- | --- | --- |",
      `| \`fuzzer\` | ${statusLabel(r.status)} | ${escapeCell(fuzzerNotes(r))} |`,
      ...scanRows(r.scan).map(
        ([label, status, note]) => `| \`${label}\` | ${escapeCell(statusLabel(status))} | ${escapeCell(note)} |`,
      ),
      "",
    ];
    for (const l of head) lines.push(l);
    total += charLen(head);

    // The actual findings behind the summary counts ("8 issues" -> the 8 hits),
    // collapsed like Karen's manifest review. Per-check capped, and the whole
    // block is skipped if it would push the region past the budget.
    const findings = scanDetailSections(r.scan);
    if (findings.length === 0) continue;
    const block: string[] = ["<details><summary>Findings</summary>", ""];
    for (const sec of findings) {
      block.push(`**${sec.label}**`, "");
      for (const line of sec.lines) block.push(`- ${escapeListItem(line)}`);
      block.push("");
    }
    block.push("</details>", "");

    const blockLen = charLen(block);
    if (total + blockLen <= REGION_CHAR_BUDGET) {
      for (const l of block) lines.push(l);
      total += blockLen;
    } else {
      findingsTruncated = true;
    }
  }

  if (findingsTruncated) {
    lines.push("_Some Findings were omitted to stay within GitHub's comment size limit._", "");
  }

  return lines.join("\n");
}

/** Approximate rendered length of an array of lines (joined with newlines). */
function charLen(arr: string[]): number {
  return arr.reduce((n, l) => n + l.length + 1, 0);
}

/**
 * The `fuzzer` row's Notes. A completed run (the fuzzer wrote a report, so
 * total > 0) shows the stats breakdown ALONE — for that path `detail` is just a
 * verbose restatement of the same numbers (the `classified: …` log line), which
 * is what made the cell print the stats twice. A setup/verify failure has no
 * usable stats (total 0), so fall back to `detail`, which carries the real reason
 * (exit code, wall kill, …); an em dash when there's nothing. (Caller escapes it.)
 */
function fuzzerNotes(r: FuzzWorldResult): string {
  if (r.stats && (r.stats.total ?? 0) > 0) return formatStats(r.stats);
  return r.detail.trim() || "—";
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

/** Max finding lines rendered per check; the rest collapse to a "…and N more" tail. */
const MAX_DETAIL_LINES = 15;

/** Region char ceiling for the Findings blocks (under GitHub's ~65 KB comment limit). */
const REGION_CHAR_BUDGET = 60000;

/**
 * The actual finding lines per scan check (result.json.scan[*].details — the
 * bandit hits, ROM paths, ruff diagnostics behind each summary count), for the
 * collapsible block. Only checks that recorded findings appear; each is capped at
 * MAX_DETAIL_LINES with a "…and N more" tail so a world with thousands of
 * diagnostics (e.g. ruff on a large upstream world) can't blow the comment limit.
 */
function scanDetailSections(
  scan: Record<string, unknown> | undefined,
): Array<{ label: string; lines: string[] }> {
  if (!scan) return [];
  const sections: Array<{ label: string; lines: string[] }> = [];
  for (const [key, value] of Object.entries(scan)) {
    if (!value || typeof value !== "object" || Array.isArray(value)) continue;
    const raw = (value as Record<string, unknown>).details;
    if (!Array.isArray(raw)) continue;
    const all = raw.filter((d): d is string => typeof d === "string");
    if (all.length === 0) continue;
    const shown = all.slice(0, MAX_DETAIL_LINES);
    if (all.length > shown.length) shown.push(`…and ${all.length - shown.length} more`);
    sections.push({ label: SCAN_LABELS[key] ?? key, lines: shown });
  }
  return sections;
}

/** Flatten a finding to a single safe Markdown list-item line. */
function escapeListItem(text: string): string {
  return text.replace(/\r?\n/g, " ").trim();
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
