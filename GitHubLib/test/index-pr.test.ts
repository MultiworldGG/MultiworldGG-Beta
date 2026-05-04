import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { openOrUpdateIndexPR, IndexPROpts } from "../src/index-pr";

interface FileEntry {
  content: string;
  sha: string;
}

interface FakeIndex {
  defaultBranch: string;
  branches: Record<string, string>; // ref → sha
  files: Record<string, Record<string, FileEntry>>; // ref → path → entry
  openPRs: Array<{ number: number; head: string }>;
  writes: Array<{ kind: string; payload: any }>;
}

function makeFakeIndex(init: Partial<FakeIndex> = {}): FakeIndex {
  return {
    defaultBranch: init.defaultBranch ?? "main",
    branches: init.branches ?? { main: "main-sha" },
    files: init.files ?? { main: {} },
    openPRs: init.openPRs ?? [],
    writes: init.writes ?? [],
  };
}

function makeKarenOctokit(state: FakeIndex, indexOwner: string, indexName: string): any {
  let prCounter = 100;
  return {
    rest: {
      repos: {
        get: async () => ({ data: { default_branch: state.defaultBranch } }),
        getContent: async ({ path, ref }: { path: string; ref: string }) => {
          const filesOnRef = state.files[ref];
          if (!filesOnRef || !filesOnRef[path]) {
            throw Object.assign(new Error("404"), { status: 404 });
          }
          const entry = filesOnRef[path];
          return {
            data: {
              type: "file",
              sha: entry.sha,
              content: Buffer.from(entry.content, "utf-8").toString("base64"),
              encoding: "base64",
            },
          };
        },
        createOrUpdateFileContents: async ({ path, branch, content, message }: any) => {
          const decoded = Buffer.from(content, "base64").toString("utf-8");
          state.files[branch] = state.files[branch] ?? {};
          const newSha = `sha-${path}-${state.writes.length}`;
          state.files[branch][path] = { content: decoded, sha: newSha };
          state.writes.push({ kind: "file", payload: { path, branch, message, content: decoded } });
          return { data: {} };
        },
      },
      git: {
        getRef: async ({ ref }: { ref: string }) => {
          const head = ref.replace(/^heads\//, "");
          const sha = state.branches[head];
          if (!sha) throw Object.assign(new Error("404"), { status: 404 });
          return { data: { object: { sha, type: "commit" } } };
        },
        createRef: async ({ ref, sha }: { ref: string; sha: string }) => {
          const head = ref.replace(/^refs\/heads\//, "");
          state.branches[head] = sha;
          // Inherit files from main (simulate branch-from-main)
          state.files[head] = { ...state.files[state.defaultBranch] };
          state.writes.push({ kind: "branch", payload: { head, sha } });
          return { data: {} };
        },
      },
      pulls: {
        list: async ({ head }: { head: string }) => {
          const branchHead = head.replace(`${indexOwner}:`, "");
          const matches = state.openPRs.filter((p) => p.head === branchHead);
          return { data: matches };
        },
        create: async ({ head, title }: any) => {
          const number = prCounter++;
          state.openPRs.push({ number, head });
          state.writes.push({ kind: "pulls.create", payload: { number, head, title } });
          return { data: { number } };
        },
        update: async ({ pull_number, body }: any) => {
          state.writes.push({ kind: "pulls.update", payload: { pull_number, body } });
          return { data: {} };
        },
      },
      issues: {
        addLabels: async ({ issue_number, labels }: any) => {
          state.writes.push({ kind: "labels", payload: { issue_number, labels } });
          return { data: [] };
        },
      },
    },
  };
}

const baseOpts = (overrides: Partial<IndexPROpts> = {}): Omit<IndexPROpts, "karenOctokit"> => ({
  karenSlug: "karen-multiworld-bot",
  indexOwner: "lallaria",
  indexName: "MultiworldGG-Index",
  sourceOwner: "alice",
  sourceRepo: "alice-clique",
  slug: "clique",
  releaseTag: "v1.0.0",
  pinnedSha: "wheel-sha-aaa",
  game: "Clique",
  authors: ["Alice"],
  ...overrides,
});

beforeEach(() => {
  delete process.env.OLIVER_CODEOWNER_PREFIX;
});

afterEach(() => {
  delete process.env.OLIVER_CODEOWNER_PREFIX;
});

describe("openOrUpdateIndexPR — labels (Phase C)", () => {
  it("applies 'New APWorld' label when worlds/<slug>.json is brand-new", async () => {
    const state = makeFakeIndex();
    const octokit = makeKarenOctokit(state, "lallaria", "MultiworldGG-Index");
    const result = await openOrUpdateIndexPR({ ...baseOpts(), karenOctokit: octokit });

    expect(result.worldIsNew).toBe(true);
    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["New APWorld"]);
    expect(label?.payload.issue_number).toBe(result.prNumber);
  });

  it("applies 'APWorld Update' label when worlds/<slug>.json already exists on main", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/clique.json": {
            content: JSON.stringify({ module_location: "git+old", world_version: "v0.9.0" }),
            sha: "old-manifest-sha",
          },
        },
      },
    });
    const octokit = makeKarenOctokit(state, "lallaria", "MultiworldGG-Index");
    const result = await openOrUpdateIndexPR({ ...baseOpts(), karenOctokit: octokit });

    expect(result.worldIsNew).toBe(false);
    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["APWorld Update"]);
  });

  it("labels both on PR create and on subsequent PR update", async () => {
    const state = makeFakeIndex({
      branches: { main: "main-sha", "update/clique-v1.0.0": "branch-sha" },
      files: {
        main: {},
        "update/clique-v1.0.0": {
          "worlds/clique.json": { content: "{}", sha: "existing" },
          ".github/CODEOWNERS": { content: "worlds/clique.json @alice\n", sha: "co-sha" },
        },
      },
      openPRs: [{ number: 42, head: "update/clique-v1.0.0" }],
    });
    const octokit = makeKarenOctokit(state, "lallaria", "MultiworldGG-Index");
    const result = await openOrUpdateIndexPR({ ...baseOpts(), karenOctokit: octokit });

    expect(result.created).toBe(false);
    expect(result.prNumber).toBe(42);
    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["New APWorld"]);
    expect(label?.payload.issue_number).toBe(42);
  });
});

describe("openOrUpdateIndexPR — CODEOWNERS append (Phase E)", () => {
  it("creates CODEOWNERS with header when file does not exist", async () => {
    const state = makeFakeIndex();
    const octokit = makeKarenOctokit(state, "lallaria", "MultiworldGG-Index");
    const result = await openOrUpdateIndexPR({ ...baseOpts(), karenOctokit: octokit });

    expect(result.codeownersConflictWith).toBeNull();
    const co = state.writes.find(
      (w) => w.kind === "file" && w.payload.path === ".github/CODEOWNERS",
    );
    expect(co).toBeDefined();
    expect(co!.payload.content).toContain("# CODEOWNERS");
    expect(co!.payload.content).toContain("worlds/clique.json @alice");
  });

  it("appends a new line to existing CODEOWNERS without overwriting", async () => {
    const existing = "* @lallaria\nworlds/khddd.json @bob\n";
    const state = makeFakeIndex({
      files: {
        main: {
          ".github/CODEOWNERS": { content: existing, sha: "co-main-sha" },
        },
      },
    });
    const octokit = makeKarenOctokit(state, "lallaria", "MultiworldGG-Index");
    await openOrUpdateIndexPR({ ...baseOpts(), karenOctokit: octokit });

    const coWrite = state.writes.find(
      (w) => w.kind === "file" && w.payload.path === ".github/CODEOWNERS",
    );
    expect(coWrite).toBeDefined();
    expect(coWrite!.payload.content).toContain("* @lallaria");
    expect(coWrite!.payload.content).toContain("worlds/khddd.json @bob");
    expect(coWrite!.payload.content).toContain("worlds/clique.json @alice");
  });

  it("does NOT touch CODEOWNERS when world already exists on main (update flow)", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/clique.json": { content: "{}", sha: "old" },
          ".github/CODEOWNERS": { content: "worlds/clique.json @alice\n", sha: "co" },
        },
      },
    });
    const octokit = makeKarenOctokit(state, "lallaria", "MultiworldGG-Index");
    const result = await openOrUpdateIndexPR({ ...baseOpts(), karenOctokit: octokit });

    expect(result.worldIsNew).toBe(false);
    const coWrite = state.writes.find(
      (w) => w.kind === "file" && w.payload.path === ".github/CODEOWNERS",
    );
    expect(coWrite).toBeUndefined();
  });

  it("returns codeownersConflictWith when an existing line names a different owner", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          ".github/CODEOWNERS": {
            content: "worlds/clique.json @someone-else\n",
            sha: "co-sha",
          },
        },
      },
    });
    const octokit = makeKarenOctokit(state, "lallaria", "MultiworldGG-Index");
    const result = await openOrUpdateIndexPR({ ...baseOpts(), karenOctokit: octokit });

    expect(result.codeownersConflictWith).toBe("someone-else");
    const coWrite = state.writes.find(
      (w) => w.kind === "file" && w.payload.path === ".github/CODEOWNERS",
    );
    expect(coWrite).toBeUndefined();
  });

  it("does not write CODEOWNERS when the desired line is already present (idempotent on PR update)", async () => {
    const state = makeFakeIndex({
      branches: { main: "main-sha", "update/clique-v1.0.0": "branch-sha" },
      files: {
        main: {},
        "update/clique-v1.0.0": {
          ".github/CODEOWNERS": { content: "worlds/clique.json @alice\n", sha: "co-sha" },
        },
      },
      openPRs: [{ number: 42, head: "update/clique-v1.0.0" }],
    });
    const octokit = makeKarenOctokit(state, "lallaria", "MultiworldGG-Index");
    const result = await openOrUpdateIndexPR({ ...baseOpts(), karenOctokit: octokit });

    expect(result.codeownersConflictWith).toBeNull();
    const coWrite = state.writes.find(
      (w) => w.kind === "file" && w.payload.path === ".github/CODEOWNERS",
    );
    expect(coWrite).toBeUndefined();
  });

  it("honors OLIVER_CODEOWNER_PREFIX and writes the prefixed handle", async () => {
    process.env.OLIVER_CODEOWNER_PREFIX = "MWGGTESTING-";
    const state = makeFakeIndex();
    const octokit = makeKarenOctokit(state, "lallaria", "MultiworldGG-Index");
    await openOrUpdateIndexPR({ ...baseOpts(), karenOctokit: octokit });

    const coWrite = state.writes.find(
      (w) => w.kind === "file" && w.payload.path === ".github/CODEOWNERS",
    );
    expect(coWrite).toBeDefined();
    expect(coWrite!.payload.content).toContain("worlds/clique.json @MWGGTESTING-alice");
    expect(coWrite!.payload.content).not.toMatch(/@alice\b(?!-|TEST)/);
  });
});
