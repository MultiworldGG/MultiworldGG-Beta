import { describe, it, expect, beforeEach, afterEach } from "vitest";
import {
  openOrUpdateIndexPR,
  openOrUpdateBundleIndexPR,
  mergeWorldManifest,
  IndexPROpts,
} from "../src/index-pr";

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
          if (state.branches[head]) {
            // GitHub's response when the ref is already there — the shape the
            // caller's already-exists tolerance keys on.
            throw Object.assign(new Error("Reference already exists"), { status: 422 });
          }
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
function makeOliverOctokit(
  state: FakeIndex,
  indexOwner: string,
  opts: { graphqlThrows?: Error } = {},
): any {
  let prCounter = 100;
  return {
    rest: {
      pulls: {
        list: async ({ head }: { head: string }) => {
          const branchHead = head.replace(`${indexOwner}:`, "");
          const matches = state.openPRs.filter((p) => p.head === branchHead);
          return { data: matches };
        },
        create: async ({ head, title, body }: any) => {
          const number = prCounter++;
          const nodeId = `PR_node_${number}`;
          state.openPRs.push({ number, head });
          state.writes.push({
            kind: "pulls.create",
            payload: { number, head, title, body, node_id: nodeId },
          });
          return { data: { number, node_id: nodeId } };
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
    graphql: async (query: string, vars: Record<string, unknown>) => {
      state.writes.push({ kind: "graphql", payload: { query, vars } });
      if (opts.graphqlThrows) {
        throw opts.graphqlThrows;
      }
      return { enablePullRequestAutoMerge: { pullRequest: { id: vars.prId } } };
    },
  };
}

const INDEX_OWNER = "MultiworldGG";
const INDEX_NAME = "MultiworldGG-Index";

function makeOctokits(state: FakeIndex) {
  return {
    karenOctokit: makeKarenOctokit(state),
    oliverOctokit: makeOliverOctokit(state, INDEX_OWNER),
  };
}

const KAREN_DATA: any = {
  name: "Karen-Head-of-Multiworld-QA",
  html_url: "https://github.com/apps/karen-head-of-multiworld-qa",
};
const OLIVER_DATA: any = {
  name: "Oliver-the-Multiworld-Squirrel",
  html_url: "https://github.com/apps/oliver-the-multiworld-squirrel",
};

const baseOpts = (overrides: Partial<IndexPROpts> = {}): Omit<IndexPROpts, "karenOctokit" | "oliverOctokit"> => ({
  karenData: KAREN_DATA,
  oliverData: OLIVER_DATA,
  indexOwner: INDEX_OWNER,
  indexName: INDEX_NAME,
  sourceOwner: "alice",
  sourceRepo: "alice-myclgm",
  slug: "myclgm",
  releaseTag: "v1.0.0",
  moduleLocation:
    "https://github.com/alice/alice-myclgm/releases/download/v1.0.0/alice_clique-1.0.0-py3-none-any.whl",
  wheelAssetName: "alice_clique-1.0.0-py3-none-any.whl",
  wheelAssetSize: 158_720,
  sourceManifest: {
    game: "My Cool Game",
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
  // Fixtures here include igdb_id so these tests stay focused on the
  // New/Update label rule. The Needs-IGDB-id label rule is covered separately.
  const optsWithIgdb = {
    sourceManifest: {
      game: "My Cool Game",
      authors: ["Alice"],
      world_version: "v1.0.0",
      minimum_ap_version: "0.6.3",
      igdb_id: 117525,
    },
  };

  it("applies 'New APWorld' label when worlds/<slug>.json is brand-new", async () => {
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    const result = await openOrUpdateIndexPR({ ...baseOpts(optsWithIgdb), ...octokits });

    expect(result.worldIsNew).toBe(true);
    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["New APWorld"]);
    expect(label?.payload.issue_number).toBe(result.prNumber);
  });

  it("applies 'APWorld Update' label when worlds/<slug>.json already exists on main", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/myclgm.json": {
            content: JSON.stringify({
              module_location: "git+old",
              world_version: "v0.9.0",
              igdb_id: 117525,
            }),
            sha: "old-manifest-sha",
          },
        },
      },
    });
    const octokits = makeOctokits(state);
    const result = await openOrUpdateIndexPR({ ...baseOpts(optsWithIgdb), ...octokits });

    expect(result.worldIsNew).toBe(false);
    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["APWorld Update"]);
  });

  it("labels both on PR create and on subsequent PR update", async () => {
    const state = makeFakeIndex({
      branches: { main: "main-sha", "update/myclgm-v1.0.0": "branch-sha" },
      files: {
        main: {},
        "update/myclgm-v1.0.0": {
          "worlds/myclgm.json": { content: "{}", sha: "existing" },
          ".github/CODEOWNERS": { content: "worlds/myclgm.json @alice\n", sha: "co-sha" },
        },
      },
      openPRs: [{ number: 42, head: "update/myclgm-v1.0.0" }],
    });
    const octokits = makeOctokits(state);
    const result = await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

    expect(result.created).toBe(false);
    expect(result.prNumber).toBe(42);
    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["New APWorld", "Needs IGDB id"]);
    expect(label?.payload.issue_number).toBe(42);
  });
});

describe("openOrUpdateIndexPR — Needs IGDB id label", () => {
  it("applies 'Needs IGDB id' when source manifest lacks igdb_id and main has none either", async () => {
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    const result = await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["New APWorld", "Needs IGDB id"]);
    expect(label?.payload.issue_number).toBe(result.prNumber);
  });

  it("does NOT apply 'Needs IGDB id' when source manifest already has igdb_id", async () => {
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({
      ...baseOpts({
        sourceManifest: {
          game: "My Cool Game",
          authors: ["Alice"],
          world_version: "v1.0.0",
          igdb_id: 117525,
        },
      }),
      ...octokits,
    });

    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["New APWorld"]);
  });

  it("does NOT apply 'Needs IGDB id' when source omits igdb_id but main preserves one (update flow)", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/myclgm.json": {
            content: JSON.stringify({
              game: "My Cool Game",
              authors: ["Alice"],
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

    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["APWorld Update"]);
  });

  it("applies 'Needs IGDB id' on an update flow when neither source nor existing main has igdb_id", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/myclgm.json": {
            content: JSON.stringify({
              game: "My Cool Game",
              authors: ["Alice"],
              world_version: "v0.9.0",
            }),
            sha: "old",
          },
        },
      },
    });
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["APWorld Update", "Needs IGDB id"]);
  });

  it("treats igdb_id: null as 'present' (does not relabel)", async () => {
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({
      ...baseOpts({
        sourceManifest: {
          game: "My Cool Game",
          authors: ["Alice"],
          world_version: "v1.0.0",
          igdb_id: null,
        },
      }),
      ...octokits,
    });

    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["New APWorld"]);
  });
});

describe("openOrUpdateIndexPR — PR body game name", () => {
  it("names the game from the manifest's `game` field in the PR body", async () => {
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

    const body = state.writes.find((w) => w.kind === "pulls.create")?.payload.body as string;
    expect(body).toContain("I found a new update for My Cool Game.");
    expect(body).toContain("gathering the manifest for My Cool Game and cross referencing");
    expect(body).not.toContain("for .");
  });

  it("falls back to the slug when the manifest has no `game` field", async () => {
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({
      ...baseOpts({ sourceManifest: { authors: ["Alice"], world_version: "v1.0.0" } }),
      ...octokits,
    });

    const body = state.writes.find((w) => w.kind === "pulls.create")?.payload.body as string;
    expect(body).toContain("I found a new update for myclgm.");
    expect(body).not.toContain("for .");
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
    expect(co!.payload.content).toContain("worlds/myclgm.json @alice");
  });

  it("appends a new line to existing CODEOWNERS without overwriting", async () => {
    const existing = "* @MultiworldGG\nworlds/khddd.json @bob\n";
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
    expect(coWrite!.payload.content).toContain("* @MultiworldGG");
    expect(coWrite!.payload.content).toContain("worlds/khddd.json @bob");
    expect(coWrite!.payload.content).toContain("worlds/myclgm.json @alice");
  });

  it("does NOT touch CODEOWNERS when world already exists on main (update flow)", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/myclgm.json": { content: "{}", sha: "old" },
          ".github/CODEOWNERS": { content: "worlds/myclgm.json @alice\n", sha: "co" },
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
            content: "worlds/myclgm.json @someone-else\n",
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
      branches: { main: "main-sha", "update/myclgm-v1.0.0": "branch-sha" },
      files: {
        main: {},
        "update/myclgm-v1.0.0": {
          ".github/CODEOWNERS": { content: "worlds/myclgm.json @alice\n", sha: "co-sha" },
        },
      },
      openPRs: [{ number: 42, head: "update/myclgm-v1.0.0" }],
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
    expect(coWrite!.payload.content).toContain("worlds/myclgm.json @MWGGTESTING-alice");
    expect(coWrite!.payload.content).not.toMatch(/@alice\b(?!-|TEST)/);
  });
});

describe("openOrUpdateIndexPR — manifest merge (author-canonical, Oliver-pinned)", () => {
  function readManifest(state: FakeIndex): Record<string, unknown> {
    const write = state.writes.find(
      (w) => w.kind === "file" && w.payload.path === "worlds/myclgm.json",
    );
    if (!write) throw new Error("manifest was not written");
    return JSON.parse(write.payload.content);
  }

  it("preserves igdb_id from main when the author did not set their own", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/myclgm.json": {
            content: JSON.stringify({
              game: "My Cool Game",
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
    expect(m.module_location).toBe(
      "https://github.com/alice/alice-myclgm/releases/download/v1.0.0/alice_clique-1.0.0-py3-none-any.whl",
    );
  });

  it("lets the author override igdb_id by setting it in their archipelago.json", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/myclgm.json": {
            content: JSON.stringify({ game: "My Cool Game", igdb_id: 999 }),
            sha: "old",
          },
        },
      },
    });
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({
      ...baseOpts({
        sourceManifest: {
          game: "My Cool Game",
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
          game: "My Cool Game",
          authors: ["Alice"],
          world_version: "v1.0.0",
          tracker: "https://tracker.example/myclgm",
          flags: ["ROM"],
          _comment: "PR-time IGDB lookup happens after this commit",
        },
      }),
      ...octokits,
    });

    const m = readManifest(state);
    expect(m.tracker).toBe("https://tracker.example/myclgm");
    expect(m.flags).toEqual(["ROM"]);
    expect(m._comment).toBe("PR-time IGDB lookup happens after this commit");
  });

  it("drops fields the author removed from their archipelago.json (their file is canonical)", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/myclgm.json": {
            content: JSON.stringify({
              game: "My Cool Game",
              authors: ["Alice"],
              tracker: "https://tracker.example/myclgm",
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
          game: "My Cool Game",
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

  it("always pins module_location to the Oliver-provided URL, ignoring whatever the author's archipelago.json says", async () => {
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    const overrideUrl =
      "https://github.com/alice/alice-myclgm/releases/download/v1.0.0/alice_clique-1.0.0-py3-none-any.whl";
    await openOrUpdateIndexPR({
      ...baseOpts({
        sourceManifest: {
          game: "My Cool Game",
          authors: ["Alice"],
          world_version: "v1.0.0",
          // Author tries to set a non-pinned location; Oliver must override.
          module_location: "https://github.com/alice/alice-myclgm/tree/main/worlds/myclgm",
        },
        moduleLocation: overrideUrl,
      }),
      ...octokits,
    });

    const m = readManifest(state);
    expect(m.module_location).toBe(overrideUrl);
  });
});

describe("openOrUpdateIndexPR — PR body wheel info", () => {
  it("includes the wheel filename and a human-readable size", async () => {
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({
      ...baseOpts({
        wheelAssetName: "alice_clique-1.0.0-py3-none-any.whl",
        wheelAssetSize: 158_720, // 155.0 KB
      }),
      ...octokits,
    });

    const create = state.writes.find((w) => w.kind === "pulls.create");
    expect(create).toBeDefined();
    expect(create!.payload.body).toContain("**Wheel:**");
    expect(create!.payload.body).toContain("alice_clique-1.0.0-py3-none-any.whl");
    expect(create!.payload.body).toContain("KB");
  });

  it("formats megabyte-scale wheels with MB suffix", async () => {
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({
      ...baseOpts({
        wheelAssetName: "big_world-1.0.0-py3-none-any.whl",
        wheelAssetSize: 5 * 1024 * 1024, // 5.00 MB
      }),
      ...octokits,
    });

    const create = state.writes.find((w) => w.kind === "pulls.create");
    expect(create!.payload.body).toContain("MB");
    expect(create!.payload.body).not.toContain("KB)");
  });
});

describe("openOrUpdateIndexPR — auto-merge enable on create", () => {
  it("calls enablePullRequestAutoMerge with the new PR's node_id and SQUASH method", async () => {
    const state = makeFakeIndex();
    const octokits = makeOctokits(state);
    const result = await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

    const gql = state.writes.find((w) => w.kind === "graphql");
    expect(gql).toBeDefined();
    expect(gql!.payload.query).toContain("enablePullRequestAutoMerge");
    expect(gql!.payload.query).toContain("mergeMethod: SQUASH");
    expect(gql!.payload.vars.prId).toBe(`PR_node_${result.prNumber}`);
  });

  it("does NOT call graphql on the update path (PR already exists)", async () => {
    const state = makeFakeIndex({
      branches: { main: "main-sha", "update/myclgm-v1.0.0": "branch-sha" },
      files: {
        main: {},
        "update/myclgm-v1.0.0": {
          "worlds/myclgm.json": { content: "{}", sha: "existing" },
          ".github/CODEOWNERS": { content: "worlds/myclgm.json @alice\n", sha: "co-sha" },
        },
      },
      openPRs: [{ number: 42, head: "update/myclgm-v1.0.0" }],
    });
    const octokits = makeOctokits(state);
    await openOrUpdateIndexPR({ ...baseOpts(), ...octokits });

    const gql = state.writes.find((w) => w.kind === "graphql");
    expect(gql).toBeUndefined();
  });

  it("swallows graphql errors so the PR-open flow still completes", async () => {
    const state = makeFakeIndex();
    const oliverOctokit = makeOliverOctokit(state, INDEX_OWNER, {
      graphqlThrows: new Error("auto_merge disabled on this repository"),
    });
    const karenOctokit = makeKarenOctokit(state);

    const result = await openOrUpdateIndexPR({
      ...baseOpts(),
      karenOctokit,
      oliverOctokit,
    });

    expect(result.created).toBe(true);
    expect(result.prNumber).toBeGreaterThanOrEqual(100);

    const gql = state.writes.find((w) => w.kind === "graphql");
    expect(gql).toBeDefined();

    const label = state.writes.find((w) => w.kind === "labels");
    expect(label).toBeDefined();
  });
});

// ---------------------------------------------------------------------------
// Bundled multi-world release: openOrUpdateBundleIndexPR
// ---------------------------------------------------------------------------

const BUNDLE_TAG = "worlds-wheels-2026-06-06";

function bundleWorld(slug: string) {
  return {
    slug,
    moduleLocation:
      `https://github.com/MultiworldGG/MultiworldGG-Beta/releases/download/${BUNDLE_TAG}/` +
      `worlds_${slug}-1.0.0-py3-none-any.whl#sha256=${"b".repeat(64)}`,
    wheelAssetName: `worlds_${slug}-1.0.0-py3-none-any.whl`,
    wheelAssetSize: 158_720,
  };
}

const bundleBaseOpts = (worlds: ReturnType<typeof bundleWorld>[]) => ({
  karenData: KAREN_DATA,
  oliverData: OLIVER_DATA,
  indexOwner: INDEX_OWNER,
  indexName: INDEX_NAME,
  sourceOwner: "MultiworldGG",
  sourceRepo: "MultiworldGG-Beta",
  releaseTag: BUNDLE_TAG,
  worlds,
});

function manifestPaths(state: FakeIndex): string[] {
  return state.writes
    .filter((w) => w.kind === "file" && /^worlds\/.*\.json$/.test(w.payload.path))
    .map((w) => w.payload.path);
}

function manifestWrite(state: FakeIndex, path: string) {
  const w = state.writes.find((x) => x.kind === "file" && x.payload.path === path);
  return w ? JSON.parse(w.payload.content) : undefined;
}

// Same split as single-world: Karen for repo/git/commits, Oliver for
// pulls/issues/graphql — two clients over one shared FakeIndex state.
function makeBundleOctokits(state: FakeIndex, opts: { graphqlThrows?: Error } = {}) {
  return {
    karenOctokit: makeKarenOctokit(state),
    oliverOctokit: makeOliverOctokit(state, INDEX_OWNER, opts),
  };
}

// A rich existing Index manifest, like the real worlds/<slug>.json entries.
function indexManifest(game: string, extra: Record<string, unknown> = {}) {
  return JSON.stringify(
    {
      minimum_ap_version: "0.6.5",
      world_version: "1.5.7",
      authors: ["Dev One", "Dev Two"],
      igdb_id: 1096,
      game,
      module_location: `https://example/old/${game}.whl#sha256=${"0".repeat(64)}`,
      ...extra,
    },
    null,
    2,
  );
}

// The author's archipelago.json, as read from inside the world's wheel.
function wheelManifest(game: string, extra: Record<string, unknown> = {}): Record<string, unknown> {
  return { minimum_ap_version: "0.6.5", world_version: "2.0.0", authors: ["A"], game, ...extra };
}

// Stand in for the real download+unzip: serve a manifest per slug, null otherwise
// (null = "wheel has no archipelago.json" = the only skip path).
function fetchFor(bySlug: Record<string, Record<string, unknown> | null>) {
  return async (_moduleLocation: string, slug: string): Promise<Record<string, unknown> | null> =>
    slug in bySlug ? bySlug[slug] : null;
}

describe("openOrUpdateBundleIndexPR", () => {
  it("seeds each world's manifest from its wheel, preserving igdb_id from the Index", async () => {
    const state = makeFakeIndex({
      files: {
        main: {
          "worlds/dk64.json": { content: indexManifest("Donkey Kong 64"), sha: "dk" },
          "worlds/oot.json": { content: indexManifest("Ocarina of Time"), sha: "oot" },
        },
      },
    });
    const octokits = makeBundleOctokits(state);
    const result = await openOrUpdateBundleIndexPR({
      ...bundleBaseOpts([bundleWorld("dk64"), bundleWorld("oot")]),
      ...octokits,
      fetchManifest: fetchFor({
        dk64: wheelManifest("Donkey Kong 64"),
        oot: wheelManifest("Ocarina of Time"),
      }),
    });

    expect(result.opened).toBe(true);
    expect(result.created).toBe(true);
    expect(result.updatedWorldSlugs).toEqual(["dk64", "oot"]);
    expect(result.skippedSlugs).toEqual([]);
    expect(manifestPaths(state)).toEqual(["worlds/dk64.json", "worlds/oot.json"]);

    const dk = manifestWrite(state, "worlds/dk64.json");
    // Wheel is canonical (world_version 2.0.0, not the Index's 1.5.7); module_location
    // + disk_space_mb stamped; igdb_id preserved from the existing Index manifest.
    expect(dk).toMatchObject({
      game: "Donkey Kong 64",
      world_version: "2.0.0",
      authors: ["A"],
      igdb_id: 1096,
    });
    expect(dk.module_location).toBe(bundleWorld("dk64").moduleLocation);
    expect(dk.disk_space_mb).toBe(1);

    expect(state.writes.filter((w) => w.kind === "branch")).toHaveLength(1);
    expect(state.writes.filter((w) => w.kind === "pulls.create")).toHaveLength(1);
    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["APWorld Update"]); // both already on the Index
    // The bundle never touches CODEOWNERS.
    expect(
      state.writes.find((w) => w.kind === "file" && w.payload.path === ".github/CODEOWNERS"),
    ).toBeUndefined();
  });

  it("preserves an existing manifest's indentation", async () => {
    const fourSpace = JSON.stringify({ game: "G", igdb_id: 1, module_location: "old" }, null, 4);
    const state = makeFakeIndex({
      files: { main: { "worlds/dk64.json": { content: fourSpace, sha: "dk" } } },
    });
    const octokits = makeBundleOctokits(state);
    await openOrUpdateBundleIndexPR({
      ...bundleBaseOpts([bundleWorld("dk64")]),
      ...octokits,
      fetchManifest: fetchFor({ dk64: wheelManifest("Donkey Kong 64") }),
    });

    const write = state.writes.find((w) => w.kind === "file" && w.payload.path === "worlds/dk64.json");
    expect(write?.payload.content).toContain('\n    "'); // 4-space indent retained
  });

  it("seeds a brand-new world (not on the Index) from its wheel alongside an update", async () => {
    const state = makeFakeIndex({
      files: { main: { "worlds/dk64.json": { content: indexManifest("Donkey Kong 64"), sha: "dk" } } },
    });
    const octokits = makeBundleOctokits(state);
    const result = await openOrUpdateBundleIndexPR({
      ...bundleBaseOpts([bundleWorld("dk64"), bundleWorld("newbie")]),
      ...octokits,
      fetchManifest: fetchFor({
        dk64: wheelManifest("Donkey Kong 64"),
        newbie: wheelManifest("New Game", { igdb_id: 555 }),
      }),
    });

    expect(result.opened).toBe(true);
    expect(result.updatedWorldSlugs).toEqual(["dk64", "newbie"]);
    expect(result.skippedSlugs).toEqual([]);
    expect(manifestPaths(state)).toEqual(["worlds/dk64.json", "worlds/newbie.json"]);

    const newbie = manifestWrite(state, "worlds/newbie.json");
    expect(newbie).toMatchObject({ game: "New Game", igdb_id: 555 });
    expect(newbie.module_location).toBe(bundleWorld("newbie").moduleLocation);

    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["New APWorld", "APWorld Update"]);
  });

  it("skips only the world whose wheel has no archipelago.json", async () => {
    const state = makeFakeIndex({
      files: { main: { "worlds/dk64.json": { content: indexManifest("Donkey Kong 64"), sha: "dk" } } },
    });
    const octokits = makeBundleOctokits(state);
    const result = await openOrUpdateBundleIndexPR({
      ...bundleBaseOpts([bundleWorld("dk64"), bundleWorld("broken")]),
      ...octokits,
      fetchManifest: fetchFor({ dk64: wheelManifest("Donkey Kong 64"), broken: null }),
    });

    expect(result.opened).toBe(true);
    expect(result.updatedWorldSlugs).toEqual(["dk64"]);
    expect(result.skippedSlugs).toEqual(["broken"]);
    expect(manifestPaths(state)).toEqual(["worlds/dk64.json"]);
    expect(state.writes.find((w) => w.kind === "pulls.create")).toBeDefined();
  });

  it("opens no PR when no wheel carries an archipelago.json", async () => {
    const state = makeFakeIndex(); // empty main
    const octokits = makeBundleOctokits(state);
    const result = await openOrUpdateBundleIndexPR({
      ...bundleBaseOpts([bundleWorld("alpha"), bundleWorld("beta")]),
      ...octokits,
      fetchManifest: fetchFor({ alpha: null, beta: null }),
    });

    expect(result.opened).toBe(false);
    expect(result.skippedSlugs).toEqual(["alpha", "beta"]);
    expect(state.writes.find((w) => w.kind === "branch")).toBeUndefined();
    expect(state.writes.find((w) => w.kind === "pulls.create")).toBeUndefined();
  });

  it("re-runs self-healing: re-seeds from the wheel + main's igdb, updates the existing PR", async () => {
    const branch = `update/${BUNDLE_TAG}`;
    const stripped = JSON.stringify({ module_location: "stale" }, null, 2); // a prior bad commit
    const state = makeFakeIndex({
      branches: { main: "main-sha", [branch]: "branch-sha" },
      files: {
        main: { "worlds/dk64.json": { content: indexManifest("Donkey Kong 64"), sha: "m" } },
        [branch]: { "worlds/dk64.json": { content: stripped, sha: "b" } },
      },
      openPRs: [{ number: 42, head: branch }],
    });
    const octokits = makeBundleOctokits(state);
    const result = await openOrUpdateBundleIndexPR({
      ...bundleBaseOpts([bundleWorld("dk64")]),
      ...octokits,
      fetchManifest: fetchFor({ dk64: wheelManifest("Donkey Kong 64") }),
    });

    expect(result.created).toBe(false);
    expect(result.prNumber).toBe(42);
    expect(result.updatedWorldSlugs).toEqual(["dk64"]);
    // Re-seeded from the wheel (world_version 2.0.0); igdb_id restored from main.
    const dk = manifestWrite(state, "worlds/dk64.json");
    expect(dk).toMatchObject({ game: "Donkey Kong 64", world_version: "2.0.0", igdb_id: 1096 });
    expect(dk.module_location).toBe(bundleWorld("dk64").moduleLocation);
    expect(state.writes.find((w) => w.kind === "pulls.create")).toBeUndefined();
    expect(state.writes.find((w) => w.kind === "pulls.update")).toBeDefined();
  });

  it("labels 'Needs IGDB id' when neither the wheel nor the Index manifest has one", async () => {
    const noIgdb = JSON.stringify({ game: "G", world_version: "1.0.0", module_location: "old" }, null, 2);
    const state = makeFakeIndex({
      files: { main: { "worlds/alpha.json": { content: noIgdb, sha: "a" } } },
    });
    const octokits = makeBundleOctokits(state);
    await openOrUpdateBundleIndexPR({
      ...bundleBaseOpts([bundleWorld("alpha")]),
      ...octokits,
      fetchManifest: fetchFor({ alpha: wheelManifest("G") }), // wheel has no igdb_id either
    });

    const label = state.writes.find((w) => w.kind === "labels");
    expect(label?.payload.labels).toEqual(["APWorld Update", "Needs IGDB id"]);
  });

  it("swallows a graphql auto-merge error and still completes", async () => {
    const state = makeFakeIndex({
      files: { main: { "worlds/dk64.json": { content: indexManifest("Donkey Kong 64"), sha: "dk" } } },
    });
    const octokits = makeBundleOctokits(state, { graphqlThrows: new Error("auto_merge disabled") });
    const result = await openOrUpdateBundleIndexPR({
      ...bundleBaseOpts([bundleWorld("dk64")]),
      ...octokits,
      fetchManifest: fetchFor({ dk64: wheelManifest("Donkey Kong 64") }),
    });

    expect(result.created).toBe(true);
    expect(state.writes.find((w) => w.kind === "labels")).toBeDefined();
  });
});

describe("mergeWorldManifest", () => {
  it("stamps module_location and disk_space_mb and keeps author fields", () => {
    const m = mergeWorldManifest({ game: "G", flags: ["ROM"] }, {}, "url#sha256=x", 2 * 1024 * 1024);
    expect(m.module_location).toBe("url#sha256=x");
    expect(m.disk_space_mb).toBe(2);
    expect(m.game).toBe("G");
    expect(m.flags).toEqual(["ROM"]);
  });

  it("preserves igdb_id from the current Index manifest when the author omits it", () => {
    const m = mergeWorldManifest({ game: "G" }, { igdb_id: 42 }, "u", 1);
    expect(m.igdb_id).toBe(42);
  });

  it("lets the author's igdb_id win over the current Index manifest", () => {
    const m = mergeWorldManifest({ igdb_id: 7 }, { igdb_id: 42 }, "u", 1);
    expect(m.igdb_id).toBe(7);
  });
});
