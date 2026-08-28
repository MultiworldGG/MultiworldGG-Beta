import { describe, it, expect } from "vitest";
import {
  createFuzzCheckRun,
  startFuzzCheckRun,
  completeFuzzCheckRun,
  findFuzzCheckRunForHead,
  aggregateConclusion,
} from "../src/fuzz/check-run";
import type { FuzzStatus, FuzzWorldResult } from "../src/fuzz/types";

interface CheckRunRow {
  id: number;
  name: string;
  head_sha: string;
}

interface FakeChecks {
  runs: CheckRunRow[];
  calls: Array<{ kind: string; payload: any }>;
  nextId: number;
}

function makeFakeChecks(init: Partial<FakeChecks> = {}): FakeChecks {
  return {
    runs: init.runs ?? [],
    calls: init.calls ?? [],
    nextId: init.nextId ?? 1000,
  };
}

// Karen has checks:write: create/update Check Runs and list them for a ref.
function makeOctokit(state: FakeChecks): any {
  return {
    rest: {
      checks: {
        create: async ({ owner, repo, name, head_sha, status }: any) => {
          const id = state.nextId++;
          state.runs.push({ id, name, head_sha });
          state.calls.push({
            kind: "create",
            payload: { owner, repo, name, head_sha, status },
          });
          return { data: { id } };
        },
        update: async ({ check_run_id, status, conclusion, output }: any) => {
          state.calls.push({
            kind: "update",
            payload: { check_run_id, status, conclusion, output },
          });
          return { data: { id: check_run_id } };
        },
        listForRef: async ({ ref, check_name }: any) => {
          const matches = state.runs.filter(
            (r) => r.head_sha === ref && (check_name === undefined || r.name === check_name),
          );
          return { data: { total_count: matches.length, check_runs: matches } };
        },
      },
    },
  };
}

const OWNER = "MultiworldGG";
const REPO = "MultiworldGG-Index";
const NAME = "Karen's Isolated QA Checks";
const HEAD = "a".repeat(40);

function result(status: FuzzStatus, slug = status): FuzzWorldResult {
  return { slug, status, detail: `${slug} ${status}`, exitCode: 0, timedOut: false };
}

describe("createFuzzCheckRun", () => {
  it("creates a queued check run on the head SHA and returns its id", async () => {
    const state = makeFakeChecks();
    const octokit = makeOctokit(state);

    const id = await createFuzzCheckRun(octokit, {
      owner: OWNER,
      repo: REPO,
      name: NAME,
      headSha: HEAD,
    });

    expect(id).toBe(1000);
    const create = state.calls.find((c) => c.kind === "create");
    expect(create).toBeDefined();
    expect(create!.payload.owner).toBe(OWNER);
    expect(create!.payload.repo).toBe(REPO);
    expect(create!.payload.name).toBe(NAME);
    expect(create!.payload.head_sha).toBe(HEAD);
    expect(create!.payload.status).toBe("queued");
  });
});

describe("startFuzzCheckRun", () => {
  it("updates the check run to in_progress", async () => {
    const state = makeFakeChecks();
    const octokit = makeOctokit(state);

    await startFuzzCheckRun(octokit, { owner: OWNER, repo: REPO, checkRunId: 1000 });

    const update = state.calls.find((c) => c.kind === "update");
    expect(update).toBeDefined();
    expect(update!.payload.check_run_id).toBe(1000);
    expect(update!.payload.status).toBe("in_progress");
    expect(update!.payload.conclusion).toBeUndefined();
  });
});

describe("completeFuzzCheckRun", () => {
  it("completes the check run with conclusion and output block", async () => {
    const state = makeFakeChecks();
    const octokit = makeOctokit(state);

    await completeFuzzCheckRun(octokit, {
      owner: OWNER,
      repo: REPO,
      checkRunId: 1000,
      conclusion: "failure",
      title: "Karen's Isolated QA Checks — 1 failing",
      summary: "1 world failed",
      text: "| world | status |\n| hk | fail |",
    });

    const update = state.calls.find((c) => c.kind === "update");
    expect(update).toBeDefined();
    expect(update!.payload.check_run_id).toBe(1000);
    expect(update!.payload.status).toBe("completed");
    expect(update!.payload.conclusion).toBe("failure");
    expect(update!.payload.output.title).toBe("Karen's Isolated QA Checks — 1 failing");
    expect(update!.payload.output.summary).toBe("1 world failed");
    expect(update!.payload.output.text).toContain("hk");
  });

  it("omits text when not provided", async () => {
    const state = makeFakeChecks();
    const octokit = makeOctokit(state);

    await completeFuzzCheckRun(octokit, {
      owner: OWNER,
      repo: REPO,
      checkRunId: 7,
      conclusion: "success",
      title: "ok",
      summary: "all good",
    });

    const update = state.calls.find((c) => c.kind === "update");
    expect(update!.payload.output.text).toBeUndefined();
  });
});

describe("createFuzzCheckRun + lifecycle round-trip", () => {
  it("threads the created id through start and complete", async () => {
    const state = makeFakeChecks();
    const octokit = makeOctokit(state);

    const id = await createFuzzCheckRun(octokit, {
      owner: OWNER,
      repo: REPO,
      name: NAME,
      headSha: HEAD,
    });
    await startFuzzCheckRun(octokit, { owner: OWNER, repo: REPO, checkRunId: id });
    await completeFuzzCheckRun(octokit, {
      owner: OWNER,
      repo: REPO,
      checkRunId: id,
      conclusion: "neutral",
      title: "t",
      summary: "s",
    });

    expect(state.calls.map((c) => c.kind)).toEqual(["create", "update", "update"]);
    expect(state.calls[1].payload.check_run_id).toBe(id);
    expect(state.calls[2].payload.check_run_id).toBe(id);
    expect(state.calls[2].payload.status).toBe("completed");
  });
});

describe("findFuzzCheckRunForHead", () => {
  it("returns null when no matching run exists on the head", async () => {
    const state = makeFakeChecks();
    const octokit = makeOctokit(state);

    const found = await findFuzzCheckRunForHead(octokit, {
      owner: OWNER,
      repo: REPO,
      name: NAME,
      headSha: HEAD,
    });
    expect(found).toBeNull();
  });

  it("finds an existing run created for the same head + name (reuse path)", async () => {
    const state = makeFakeChecks();
    const octokit = makeOctokit(state);

    const id = await createFuzzCheckRun(octokit, {
      owner: OWNER,
      repo: REPO,
      name: NAME,
      headSha: HEAD,
    });
    const found = await findFuzzCheckRunForHead(octokit, {
      owner: OWNER,
      repo: REPO,
      name: NAME,
      headSha: HEAD,
    });
    expect(found).toBe(id);
  });

  it("does not match a run with a different name on the same head", async () => {
    const state = makeFakeChecks({
      runs: [{ id: 1, name: "some-other-check", head_sha: HEAD }],
    });
    const octokit = makeOctokit(state);

    const found = await findFuzzCheckRunForHead(octokit, {
      owner: OWNER,
      repo: REPO,
      name: NAME,
      headSha: HEAD,
    });
    expect(found).toBeNull();
  });

  it("prefers the newest (highest id) when an earlier attempt left a duplicate", async () => {
    const state = makeFakeChecks({
      runs: [
        { id: 100, name: NAME, head_sha: HEAD },
        { id: 250, name: NAME, head_sha: HEAD },
        { id: 175, name: NAME, head_sha: HEAD },
      ],
    });
    const octokit = makeOctokit(state);

    const found = await findFuzzCheckRunForHead(octokit, {
      owner: OWNER,
      repo: REPO,
      name: NAME,
      headSha: HEAD,
    });
    expect(found).toBe(250);
  });
});

describe("aggregateConclusion", () => {
  it("returns success/pass when every world passed (and on empty input)", () => {
    expect(aggregateConclusion([])).toEqual({ conclusion: "success", status: "pass" });
    expect(aggregateConclusion([result("pass"), result("pass")])).toEqual({
      conclusion: "success",
      status: "pass",
    });
  });

  it("returns neutral/warn when there is a warn but no fail (warn is never red)", () => {
    expect(aggregateConclusion([result("pass"), result("warn")])).toEqual({
      conclusion: "neutral",
      status: "warn",
    });
  });

  it("returns failure/fail when any world failed (a warn never masks a fail)", () => {
    expect(aggregateConclusion([result("warn"), result("fail"), result("pass")])).toEqual({
      conclusion: "failure",
      status: "fail",
    });
  });
});
