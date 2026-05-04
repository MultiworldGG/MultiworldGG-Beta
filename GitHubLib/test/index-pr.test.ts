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

// Karen has Contents:Write only — branch + commit operations on the Index.
function makeKarenOctokit(state: FakeIndex): any {
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
    },
  };
}

// Oliver has Pull requests:Write + Issues:Write — opens the PR and applies labels.
function makeOliverOctokit(state: FakeIndex, indexOwner: string): any {
  let prCounter = 100;
  return {
    rest: {
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

const INDEX_OWNER = "lallaria";
const INDEX_NAME = "MultiworldGG-Index";

function makeOctokits(state: FakeIndex) {
  return {
    karenOctokit: makeKarenOctokit(state),
    oliverOctokit: makeOliverOctokit(state, INDEX_OWNER),
  };
}

const baseOpts = (overrides: Partial<IndexPROpts> = {}): Omit<IndexPROpts, "karenOctokit" | "oliverOctokit"> => ({
  karenSlug: "karen-multiworld-bot",
  indexOwner: INDEX_OWNER,
  indexName: INDEX_NAME,
  sourceOwner: "alice",
  sourceRepo: "alice-clique",
  slug: "clique",
  releaseTag: "v1.0.0",
  pinnedSha: "wheel-sha-aaa",
  sourceManifest: {
    game: "Clique",
    authors: ["Alice"],
    world_version: "v1.0.0",
    minimum_ap_version: "0.6.3",
  },
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
    const octokits = makeOctokits(state);
    const result = await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

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
    const octokits = makeOctokits(state);
    const result = await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

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
    const octokits = makeOctokits(state);
    const result = await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

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
    const octokits = makeOctokits(state);
    const result = await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

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
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

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
    const octokits = makeOctokits(state);
    const result = await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

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
    const octokits = makeOctokits(state);
    const result = await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

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
    const octokits = makeOctokits(state);
    const result = await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

    expect(result.codeownersConflictWith).toBeNull();
    const coWrite = state.writes.find(
      (w) => w.kind === "file" && w.payload.path === ".github/CODEOWNERS",
    );
    expect(coWrite).toBeUndefined();
  });

  it("honors OLIVER_CODEOWNER_PREFIX and writes the prefixed handle", async () => {
    process.env.OLIVER_CODEOWNER_PREFIX = "MWGGTESTING-";
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

    const coWrite = state.writes.find(
      (w) => w.kind === "file" && w.payload.path === ".github/CODEOWNERS",
    );
    expect(coWrite).toBeDefined();
    expect(coWrite!.payload.content).toContain("worlds/clique.json @MWGGTESTING-alice");
    expect(coWrite!.payload.content).not.toMatch(/@alice\b(?!-|TEST)/);
  });
});

describe("openOrUpdateIndexPR — manifest merge (author-canonical, Oliver-pinned)", () => {
  function readManifest(state: FakeIndex): Record<string, unknown> {
    const write = state.writes.find(
      (w) => w.kind === "file" && w.payload.path === "worlds/clique.json",
    );
    if (!write) throw new Error("manifest was not written");
    return JSON.parse(write.payload.content);
  }

  it("preserves igdb_id from main when the author did not set their own", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/clique.json": {
            content: JSON.stringify({
              game: "Clique",
              authors: ["Alice"],
              module_location: "git+old",
              world_version: "v0.9.0",
              igdb_id: 117525,
            }),
            sha: "old",
          },
        },
      },
    });
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

    const m = readManifest(state);
    expect(m.igdb_id).toBe(117525);
    expect(m.module_location).toMatch(/^git\+https:\/\/github\.com\/alice\/alice-clique\.git@/);
  });

  it("lets the author override igdb_id by setting it in their archipelago.json", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/clique.json": {
            content: JSON.stringify({ game: "Clique", igdb_id: 999 }),
            sha: "old",
          },
        },
      },
    });
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({
      ...baseOpts({
        sourceManifest: {
          game: "Clique",
          authors: ["Alice"],
          world_version: "v1.0.0",
          igdb_id: 117525,
        },
      }),
      ...octokits,
    });

    const m = readManifest(state);
    expect(m.igdb_id).toBe(117525);
  });

  it("passes arbitrary author-declared fields (tracker, _comment) through unchanged", async () => {
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({
      ...baseOpts({
        sourceManifest: {
          game: "Clique",
          authors: ["Alice"],
          world_version: "v1.0.0",
          tracker: "https://tracker.example/clique",
          flags: ["ROM"],
          _comment: "PR-time IGDB lookup happens after this commit",
        },
      }),
      ...octokits,
    });

    const m = readManifest(state);
    expect(m.tracker).toBe("https://tracker.example/clique");
    expect(m.flags).toEqual(["ROM"]);
    expect(m._comment).toBe("PR-time IGDB lookup happens after this commit");
  });

  it("drops fields the author removed from their archipelago.json (their file is canonical)", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/clique.json": {
            content: JSON.stringify({
              game: "Clique",
              authors: ["Alice"],
              tracker: "https://tracker.example/clique",
              flags: ["ROM"],
            }),
            sha: "old",
          },
        },
      },
    });
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({
      ...baseOpts({
        sourceManifest: {
          game: "Clique",
          authors: ["Alice"],
          world_version: "v1.0.0",
          // tracker and flags intentionally absent
        },
      }),
      ...octokits,
    });

    const m = readManifest(state);
    expect(m).not.toHaveProperty("tracker");
    expect(m).not.toHaveProperty("flags");
  });

  it("always pins module_location to the wheel SHA, ignoring whatever the author's archipelago.json says", async () => {
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({
      ...baseOpts({
        sourceManifest: {
          game: "Clique",
          authors: ["Alice"],
          world_version: "v1.0.0",
          // Author tries to set a non-pinned location; Oliver must override.
          module_location: "https://github.com/alice/alice-clique/tree/main/worlds/clique",
        },
        pinnedSha: "wheel-sha-zzz",
      }),
      ...octokits,
    });

    const m = readManifest(state);
    expect(m.module_location).toBe(
      "git+https://github.com/alice/alice-clique.git@wheel-sha-zzz",
    );
  });
});
