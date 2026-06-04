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

describe("renderFuzzRegion — formatting", () => {
  it("renders a markdown table with verdict glyphs and a stats/detail cell", () => {
    const md = renderFuzzRegion([
      result({ slug: "hk", status: "pass", detail: "fuzzed clean", stats: { success: 10, total: 10 } }),
      result({ slug: "sm", status: "warn", detail: "no clean generation", stats: { success: 0, total: 8 } }),
      result({ slug: "z3", status: "fail", detail: "unparseable report.json" }),
    ]);

    expect(md).toContain("### World generation (fuzzer) results");
    expect(md).toContain("| World | Verdict | Details |");
    expect(md).toContain("| `hk` | ✅ ");
    expect(md).toContain("| `sm` | ⚠️ ");
    expect(md).toContain("| `z3` | ❌ ");
    // stats expand into k=v pairs
    expect(md).toContain("success=10");
    expect(md).toContain("total=10");
    // detail-only row falls back to the human summary
    expect(md).toContain("unparseable report.json");
    // legend matches the workflow wording
    expect(md).toContain("✅ generated");
    expect(md).toContain("⚠️ no-op");
    expect(md).toContain("❌ failed");
  });

  it("emits a placeholder (not an empty table) when there are no results", () => {
    const md = renderFuzzRegion([]);
    expect(md).toContain("### World generation (fuzzer) results");
    expect(md).toContain("_No worlds were fuzzed._");
    expect(md).not.toContain("| World | Verdict |");
  });

  it("escapes pipe characters so a detail string cannot break the table", () => {
    const md = renderFuzzRegion([result({ slug: "hk", status: "fail", detail: "a | b | c" })]);
    expect(md).toContain("a \\| b \\| c");
  });

  it("renders an em dash when a row has neither stats nor detail", () => {
    const md = renderFuzzRegion([result({ slug: "hk", status: "pass", detail: "" })]);
    const row = md.split("\n").find((l) => l.startsWith("| `hk`"));
    expect(row).toBeDefined();
    expect(row).toContain("—");
  });
});
