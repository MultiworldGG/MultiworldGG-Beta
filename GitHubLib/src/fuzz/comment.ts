// Sticky-comment splicing for Karen's fuzz results: the fuzz job owns only the
// fenced region between the karen-fuzz markers inside the marker comment.
// Race-safety: re-fetch the body right before patching, and no-op when the PR
// head has moved past the SHA this run was dispatched for.

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
   * Optional `## {title}` heading written above the fence when the comment is
   * created; outside the fence, so region updates never clobber it.
   */
  title?: string;
}

/**
 * Render the fenced region: per-world heading + Check/Status/Notes table
 * mirroring Karen's review, then per-check scan rows. Pure and deterministic.
 */
export function renderFuzzRegion(results: FuzzWorldResult[]): string {
  const lines: string[] = ["### World generation (fuzzer) results", ""];

  if (results.length === 0) {
    lines.push("_No worlds were fuzzed._");
    return lines.join("\n");
  }

  // GitHub caps comments/check-runs near 65 KB. Tables always render; only the
  // collapsible Findings blocks are dropped past the budget, so the verdict survives.
  let total = charLen(lines);
  let findingsTruncated = false;

  for (const r of results) {
    const head = [
      `#### \`${r.slug}\` - ${statusLabel(r.status)}`,
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

    // Collapsible Findings: fuzzer per-error summary first, then each scan
    // check; per-section capped, whole block skipped past the budget.
    const findings = scanDetailSections(r.scan);
    const fuzzerSection = fuzzerDetailSection(r);
    if (fuzzerSection) findings.unshift(fuzzerSection);
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
 * The `fuzzer` row's Notes: stats alone when detail just restates them (the
 * `classified:` line); detail + stats when it adds something (wall-kill note);
 * detail alone when there are no stats. Caller escapes it.
 */
function fuzzerNotes(r: FuzzWorldResult): string {
  const detail = r.detail.trim();
  if (!r.stats || (r.stats.total ?? 0) <= 0) return detail || "-";
  const stats = formatStats(r.stats);
  if (!detail || detail.includes("classified:")) return stats;
  return `${detail} (${stats})`;
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
 * One [label, status, note] row per scan check; `note` is karen_review's human
 * message. A legacy bare-string value reads as the status with an empty note;
 * other shapes are JSON-encoded so they can't break a row.
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
 * Finding lines per scan check (scan[*].details) for the collapsible block;
 * each capped at MAX_DETAIL_LINES with an "…and N more" tail.
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

/** The fuzzer's per-error summary as its own Findings section (capped), or null. */
function fuzzerDetailSection(r: FuzzWorldResult): { label: string; lines: string[] } | null {
  const all = (r.fuzzerDetails ?? []).filter((d): d is string => typeof d === "string");
  if (all.length === 0) return null;
  const shown = all.slice(0, MAX_DETAIL_LINES);
  if (all.length > shown.length) shown.push(`…and ${all.length - shown.length} more`);
  return { label: "fuzzer", lines: shown };
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

  // Re-fetch immediately before patching: another job may have edited the body
  // since listComments.
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
