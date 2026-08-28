import { describe, it, expect } from "vitest";
import {
  upsertFuzzComment,
  renderFuzzRegion,
  FUZZ_REGION_START,
  FUZZ_REGION_END,
} from "../src/fuzz/comment";
import type { FuzzWorldResult } from "../src/fuzz/types";

const MARKER = "<!-- karen-pr-review -->";
const HEAD_SHA = "a".repeat(40);

interface FakeComment {
  id: number;
  body: string;
}

interface FakeState {
  headSha: string;
  comments: FakeComment[];
  created: Array<{ issue_number: number; body: string }>;
  updated: Array<{ comment_id: number; body: string }>;
  // call ordering, so we can assert getComment runs immediately before update
  calls: string[];
}

function makeState(init: Partial<FakeState> = {}): FakeState {
  return {
    headSha: init.headSha ?? HEAD_SHA,
    comments: init.comments ?? [],
    created: init.created ?? [],
    updated: init.updated ?? [],
    calls: init.calls ?? [],
  };
}

// Minimal octokit mock mirroring the rest.* surface upsertFuzzComment uses.
function makeOctokit(state: FakeState): any {
  return {
    rest: {
      pulls: {
        get: async ({ pull_number }: { pull_number: number }) => {
          state.calls.push("pulls.get");
          return { data: { number: pull_number, head: { sha: state.headSha } } };
        },
      },
      issues: {
        listComments: async () => {
          state.calls.push("listComments");
          return { data: state.comments.map((c) => ({ ...c })) };
        },
        getComment: async ({ comment_id }: { comment_id: number }) => {
          state.calls.push("getComment");
          const found = state.comments.find((c) => c.id === comment_id);
          if (!found) throw Object.assign(new Error("404"), { status: 404 });
          return { data: { ...found } };
        },
        createComment: async ({ issue_number, body }: { issue_number: number; body: string }) => {
          state.calls.push("createComment");
          state.created.push({ issue_number, body });
          const created: FakeComment = { id: 9000 + state.comments.length, body };
          state.comments.push(created);
          return { data: { ...created } };
        },
        updateComment: async ({ comment_id, body }: { comment_id: number; body: string }) => {
          state.calls.push("updateComment");
          state.updated.push({ comment_id, body });
          const target = state.comments.find((c) => c.id === comment_id);
          if (target) target.body = body;
          return { data: { id: comment_id, body } };
        },
      },
    },
  };
}

function result(overrides: Partial<FuzzWorldResult> = {}): FuzzWorldResult {
  return {
    slug: "hk",
    status: "pass",
    detail: "fuzzed clean",
    exitCode: 0,
    timedOut: false,
    ...overrides,
  };
}

const run = (octokit: any, region: string, extra: Record<string, unknown> = {}) =>
  upsertFuzzComment(octokit, {
    owner: "MultiworldGG",
    repo: "MultiworldGG-Index",
    prNumber: 42,
    marker: MARKER,
    headSha: HEAD_SHA,
    region,
    ...extra,
  });

describe("upsertFuzzComment — splice into an existing fenced region", () => {
  it("replaces only the bytes between the markers, preserving surrounding review text", async () => {
    const body = [
      MARKER,
      "## Karen: Quality Assurance Manager",
      "Some review prose Karen wrote.",
      "",
      FUZZ_REGION_START,
      "OLD fuzz table that must be overwritten",
      FUZZ_REGION_END,
      "",
      "Trailing footer Karen owns.",
    ].join("\n");
    const state = makeState({ comments: [{ id: 1, body }] });
    const octokit = makeOctokit(state);

    await run(octokit, "NEW REGION CONTENT");

    expect(state.updated).toHaveLength(1);
    expect(state.created).toHaveLength(0);
    const out = state.updated[0].body;
    expect(out).toContain("NEW REGION CONTENT");
    expect(out).not.toContain("OLD fuzz table");
    // Everything outside the fence is untouched.
    expect(out).toContain("## Karen: Quality Assurance Manager");
    expect(out).toContain("Some review prose Karen wrote.");
    expect(out).toContain("Trailing footer Karen owns.");
    // Markers themselves survive and stay in order.
    expect(out.indexOf(FUZZ_REGION_START)).toBeLessThan(out.indexOf(FUZZ_REGION_END));
    expect(out.split(FUZZ_REGION_START)).toHaveLength(2); // exactly one region
  });

  it("re-fetches the comment immediately before patching (race-safety)", async () => {
    const body = `${MARKER}\n${FUZZ_REGION_START}\nold\n${FUZZ_REGION_END}\n`;
    const state = makeState({ comments: [{ id: 7, body }] });
    const octokit = makeOctokit(state);

    await run(octokit, "fresh");

    // getComment must run after listComments and right before updateComment.
    expect(state.calls).toEqual(["pulls.get", "listComments", "getComment", "updateComment"]);
    expect(state.updated[0].comment_id).toBe(7);
  });

  it("splices against the re-fetched body, not the one from listComments", async () => {
    const stale = `${MARKER}\n${FUZZ_REGION_START}\nstale\n${FUZZ_REGION_END}\n`;
    const state = makeState({ comments: [{ id: 3, body: stale }] });
    const octokit = makeOctokit(state);
    // Simulate a concurrent edit landing between listComments and getComment.
    const fresher = `${MARKER}\nEDITED BY ANOTHER JOB\n${FUZZ_REGION_START}\nstale\n${FUZZ_REGION_END}\n`;
    const origGet = octokit.rest.issues.getComment;
    octokit.rest.issues.getComment = async (args: { comment_id: number }) => {
      state.comments[0].body = fresher;
      return origGet(args);
    };

    await run(octokit, "newest");

    expect(state.updated[0].body).toContain("EDITED BY ANOTHER JOB");
    expect(state.updated[0].body).toContain("newest");
    expect(state.updated[0].body).not.toContain("stale");
  });
});

describe("upsertFuzzComment — append when markers absent", () => {
  it("appends a fresh fenced region to a marker comment that has none", async () => {
    const body = `${MARKER}\n## Karen: Quality Assurance Manager\n\nNo fuzz region yet.`;
    const state = makeState({ comments: [{ id: 5, body }] });
    const octokit = makeOctokit(state);

    await run(octokit, "appended region");

    expect(state.created).toHaveLength(0);
    expect(state.updated).toHaveLength(1);
    const out = state.updated[0].body;
    // Original content retained...
    expect(out).toContain("No fuzz region yet.");
    // ...and exactly one fenced region was added.
    expect(out).toContain(FUZZ_REGION_START);
    expect(out).toContain(FUZZ_REGION_END);
    expect(out).toContain("appended region");
    expect(out.split(FUZZ_REGION_START)).toHaveLength(2);
    expect(out.indexOf(FUZZ_REGION_START)).toBeLessThan(out.indexOf(FUZZ_REGION_END));
  });

  it("treats an end-marker-only body as 'markers absent' and appends", async () => {
    const body = `${MARKER}\nstray ${FUZZ_REGION_END} with no start`;
    const state = makeState({ comments: [{ id: 6, body }] });
    const octokit = makeOctokit(state);

    await run(octokit, "R");

    const out = state.updated[0].body;
    expect(out).toContain(FUZZ_REGION_START);
    // Now there is a real start marker plus the appended region content.
    expect(out).toContain("R");
  });
});

describe("upsertFuzzComment — create when no marker comment", () => {
  it("creates a minimal sticky comment with the marker line and a fenced region", async () => {
    const state = makeState({
      comments: [{ id: 1, body: "an unrelated comment from a human" }],
    });
    const octokit = makeOctokit(state);

    await run(octokit, "created region");

    expect(state.updated).toHaveLength(0);
    expect(state.created).toHaveLength(1);
    const out = state.created[0].body;
    expect(out.startsWith(MARKER)).toBe(true);
    expect(out).toContain(FUZZ_REGION_START);
    expect(out).toContain(FUZZ_REGION_END);
    expect(out).toContain("created region");
    expect(state.created[0].issue_number).toBe(42);
  });

  it("creates one when there are no comments at all", async () => {
    const state = makeState();
    const octokit = makeOctokit(state);

    await run(octokit, "x");

    expect(state.created).toHaveLength(1);
    expect(state.created[0].body.startsWith(MARKER)).toBe(true);
  });

  it("writes the optional title heading above the fence when creating", async () => {
    const state = makeState();
    const octokit = makeOctokit(state);

    await run(octokit, "created region", { title: "Karen: Isolated QA Checks" });

    expect(state.created).toHaveLength(1);
    const out = state.created[0].body;
    expect(out.startsWith(MARKER)).toBe(true);
    expect(out).toContain("## Karen: Isolated QA Checks");
    // The heading sits ABOVE the fence so later region splices never clobber it.
    expect(out.indexOf("## Karen: Isolated QA Checks")).toBeLessThan(out.indexOf(FUZZ_REGION_START));
    expect(out).toContain("created region");
  });
});

describe("upsertFuzzComment — no-op when head moved", () => {
  it("does not list, create, or update when pull head != headSha", async () => {
    const body = `${MARKER}\n${FUZZ_REGION_START}\nold\n${FUZZ_REGION_END}\n`;
    const state = makeState({ headSha: "b".repeat(40), comments: [{ id: 1, body }] });
    const octokit = makeOctokit(state);

    await run(octokit, "should-not-be-written");

    expect(state.calls).toEqual(["pulls.get"]);
    expect(state.created).toHaveLength(0);
    expect(state.updated).toHaveLength(0);
    expect(state.comments[0].body).toBe(body); // untouched
  });
});

describe("renderFuzzRegion — Karen-style per-world tables", () => {
  it("renders a per-world Check/Status/Notes table with glyph+word status and per-check notes", () => {
    const md = renderFuzzRegion([
      result({
        slug: "hk",
        status: "pass",
        detail: "fuzzed clean",
        stats: { success: 10, total: 10 },
        scan: {
          bandit: { status: "pass", note: "Bandit found nothing worth mentioning." },
          size_sanity: { status: "pass", note: "a very reasonable 5.2MB / cap 250MB" },
          no_rom_files: { status: "pass", note: "no illegal games here" },
          no_network_at_import: { status: "pass", note: "" },
          ruff: { status: "captured", note: "3 lint findings" },
        },
      }),
      result({ slug: "z3", status: "fail", detail: "unparseable report.json" }),
    ]);

    expect(md).toContain("### World generation (fuzzer) results");
    // per-world headings mirror Karen's slug + glyph + status shape
    expect(md).toContain("#### `hk` — ✅ pass");
    expect(md).toContain("#### `z3` — ❌ fail");
    // Karen's columns
    expect(md).toContain("| Check | Status | Notes |");
    // a completed run keeps a meaningful detail next to the stats;
    // a setup failure with no stats falls back to the detail reason.
    expect(md).toContain("| `fuzzer` | ✅ pass | fuzzed clean (success=10 total=10) |");
    expect(md).toContain("| `fuzzer` | ❌ fail | unparseable report.json |");
    // scan checks become their own rows with glyph+word, short labels, and the
    // human note karen_review recorded in the Notes column
    expect(md).toContain("| `bandit` | ✅ pass | Bandit found nothing worth mentioning. |");
    expect(md).toContain("| `size` | ✅ pass | a very reasonable 5.2MB / cap 250MB |");
    expect(md).toContain("| `net` | ✅ pass |  |"); // empty note -> blank cell
    expect(md).toContain("| `ruff` | captured | 3 lint findings |"); // no glyph for "captured"
  });

  it("tolerates legacy bare-string scan statuses (renders an empty note)", () => {
    const md = renderFuzzRegion([
      result({ slug: "hk", status: "pass", detail: "ok", scan: { bandit: "pass", ruff: "captured" } }),
    ]);
    expect(md).toContain("| `bandit` | ✅ pass |  |");
    expect(md).toContain("| `ruff` | captured |  |");
  });

  it("shows the fuzzer stats alone for a completed run, not the duplicated detail", () => {
    const md = renderFuzzRegion([
      result({
        slug: "dk64",
        status: "warn",
        // the verbose classified line that used to get appended on top of the stats
        detail: "dk64: warn — classified: status=warn success=0 failure=50 rom=50 real=0 total=50",
        stats: { success: 0, failure: 50, timeout: 0, ignored: 0, rom: 50, real: 0, total: 50 },
      }),
    ]);
    expect(md).toContain("| `fuzzer` | ⚠️ warn | success=0 failure=50 timeout=0 ignored=0 rom=50 real=0 total=50 |");
    expect(md).not.toContain("classified:"); // the duplicated detail is gone
  });

  it("keeps a non-classifier detail (e.g. the wall-kill salvage note) next to the stats", () => {
    const md = renderFuzzRegion([
      result({
        slug: "oot",
        status: "warn",
        detail: "oot: warn — wall-killed after 4/10 generations — partial stats salvaged (host too slow for this world within 1080s)",
        stats: { success: 0, failure: 2, timeout: 2, ignored: 0, rom: 0, real: 2, total: 4 },
      }),
    ]);
    expect(md).toContain(
      "| `fuzzer` | ⚠️ warn | oot: warn — wall-killed after 4/10 generations — partial stats salvaged " +
        "(host too slow for this world within 1080s) (success=0 failure=2 timeout=2 ignored=0 rom=0 real=2 total=4) |",
    );
  });

  it("renders sha256 mismatch (with note) as a scan row, and no scan rows when scan is absent", () => {
    const md = renderFuzzRegion([
      result({
        slug: "hk",
        status: "fail",
        detail: "",
        scan: { sha256: { status: "mismatch", note: "expected abc…, got def…" } },
      }),
      result({ slug: "sm", status: "pass", detail: "ok" }), // no scan
    ]);
    expect(md).toContain("| `sha256` | mismatch | expected abc…, got def… |");
    const smSection = md.slice(md.indexOf("#### `sm`"));
    expect(smSection).toContain("| `fuzzer` | ✅ pass | ok |");
    expect(smSection).not.toContain("| `bandit`"); // no scan -> fuzzer row only
  });

  it("renders a collapsible Findings block from each check's details", () => {
    const md = renderFuzzRegion([
      result({
        slug: "hk",
        status: "warn",
        detail: "scanned",
        scan: {
          bandit: {
            status: "fail",
            note: "2 issues(s), we should look it over.",
            details: [
              "worlds/hk/x.py:5 [B602/high] subprocess with shell=True",
              "worlds/hk/y.py:9 [B101/low] assert used",
            ],
          },
          ruff: { status: "captured", note: "1 lint finding", details: ["worlds/hk/x.py:1 F401  unused import"] },
          no_rom_files: { status: "pass", note: "no illegal games here", details: [] },
        },
      }),
    ]);

    expect(md).toContain("<details><summary>Findings</summary>");
    expect(md).toContain("**bandit**");
    expect(md).toContain("- worlds/hk/x.py:5 [B602/high] subprocess with shell=True");
    expect(md).toContain("**ruff**");
    expect(md).toContain("- worlds/hk/x.py:1 F401  unused import");
    // a check whose details are empty contributes no section
    expect(md).not.toContain("**rom**");
    expect(md).toContain("</details>");
  });

  it("caps findings per check with a '…and N more' tail", () => {
    const many = Array.from({ length: 20 }, (_, i) => `finding ${i}`);
    const md = renderFuzzRegion([
      result({ slug: "hk", status: "fail", detail: "x", scan: { bandit: { status: "fail", note: "20", details: many } } }),
    ]);
    expect(md).toContain("- finding 0");
    expect(md).toContain("- finding 14"); // 15th line shown (0-indexed)
    expect(md).not.toContain("- finding 15");
    expect(md).toContain("…and 5 more");
  });

  it("renders no Findings block when no check has details", () => {
    const md = renderFuzzRegion([
      result({ slug: "hk", status: "pass", detail: "ok", scan: { bandit: { status: "pass", note: "clean", details: [] } } }),
    ]);
    expect(md).not.toContain("<details><summary>Findings</summary>");
  });

  it("leads the Findings block with the fuzzer's per-error summary", () => {
    const md = renderFuzzRegion([
      result({
        slug: "papermario",
        status: "fail",
        detail: "fuzzed",
        stats: { success: 1, failure: 49, timeout: 0, ignored: 0, rom: 0, real: 49, total: 50 },
        fuzzerDetails: ["FillError: no room for item (37)", "KeyError: 'foo' (12)"],
        scan: { bandit: { status: "pass", note: "clean", details: [] } },
      }),
    ]);
    expect(md).toContain("<details><summary>Findings</summary>");
    expect(md).toContain("**fuzzer**");
    expect(md).toContain("- FillError: no room for item (37)");
    expect(md).toContain("- KeyError: 'foo' (12)");
    // the fuzzer section leads the block (before any scan section)
    expect(md.indexOf("**fuzzer**")).toBeLessThan(md.indexOf("</details>"));
  });

  it("drops Findings blocks (keeping every table) past the region size budget", () => {
    const long = "x".repeat(400);
    const worlds = Array.from({ length: 20 }, (_, i) =>
      result({
        slug: `w${i}`,
        status: "fail",
        detail: "d",
        scan: { bandit: { status: "fail", note: "many", details: Array.from({ length: 15 }, () => long) } },
      }),
    );
    const md = renderFuzzRegion(worlds);
    // every world's table survives...
    expect(md).toContain("#### `w0`");
    expect(md).toContain("#### `w19`");
    // ...but findings are capped with a note, and the region stays under GitHub's limit
    expect(md).toContain("_Some Findings were omitted to stay within GitHub's comment size limit._");
    expect(md.length).toBeLessThan(65536);
  });

  it("emits a placeholder (not a table) when there are no results", () => {
    const md = renderFuzzRegion([]);
    expect(md).toContain("### World generation (fuzzer) results");
    expect(md).toContain("_No worlds were fuzzed._");
    expect(md).not.toContain("| Check | Status | Notes |");
  });

  it("escapes pipe characters so a detail string cannot break the table", () => {
    const md = renderFuzzRegion([result({ slug: "hk", status: "fail", detail: "a | b | c" })]);
    expect(md).toContain("a \\| b \\| c");
  });

  it("renders an em dash in the fuzzer Notes when there are no stats or detail", () => {
    const md = renderFuzzRegion([result({ slug: "hk", status: "pass", detail: "" })]);
    expect(md).toContain("| `fuzzer` | ✅ pass | — |");
  });
});
