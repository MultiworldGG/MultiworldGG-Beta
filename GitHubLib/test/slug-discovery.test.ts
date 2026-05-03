import { discoverSlug } from "../src/slug-discovery";

interface MockState {
  releases: Array<{ tag_name: string }>;
  fork: boolean;
  parent?: { owner: { login: string }; default_branch: string; full_name: string };
  compareFiles: Record<string, string[]>;
  treeDirs: string[];
  manifestSlugs: Set<string>;
}

function makeOctokit(state: MockState): any {
  return {
    rest: {
      repos: {
        listReleases: async () => ({ data: state.releases }),
        get: async () => ({
          data: { fork: state.fork, parent: state.parent ?? null },
        }),
        compareCommitsWithBasehead: async ({ basehead }: { basehead: string }) => ({
          data: { files: (state.compareFiles[basehead] ?? []).map((f) => ({ filename: f })) },
        }),
        getContent: async ({ path: p, ref: _ref }: { path: string; ref: string }) => {
          if (p === "worlds") {
            return {
              data: state.treeDirs.map((name) => ({ name, type: "dir" as const })),
            };
          }
          const m = /^worlds\/([^/]+)\/archipelago\.json$/.exec(p);
          if (m && state.manifestSlugs.has(m[1])) {
            return { data: { type: "file", content: "", encoding: "utf-8", sha: "x" } };
          }
          throw Object.assign(new Error("404"), { status: 404 });
        },
      },
    },
  };
}

describe("discoverSlug", () => {
  it("fork's first release that touches one world → returns that slug", async () => {
    const state: MockState = {
      releases: [{ tag_name: "v1.0.0" }],
      fork: true,
      parent: {
        owner: { login: "MultiworldGG" },
        default_branch: "main",
        full_name: "MultiworldGG/MultiworldGG",
      },
      compareFiles: {
        "MultiworldGG:main...v1.0.0": [
          "worlds/oot/__init__.py",
          "worlds/oot/archipelago.json",
          "README.md",
        ],
      },
      treeDirs: [],
      manifestSlugs: new Set(["oot"]),
    };
    const result = await discoverSlug(makeOctokit(state), "lallaria", "oot", "v1.0.0");
    expect(result.kind).toBe("ok");
    if (result.kind === "ok") {
      expect(result.slug).toBe("oot");
    }
  });

  it("second release with one world's changes → returns that slug via prev-release compare", async () => {
    const state: MockState = {
      releases: [{ tag_name: "v1.1.0" }, { tag_name: "v1.0.0" }],
      fork: false,
      compareFiles: {
        "v1.0.0...v1.1.0": ["worlds/oot/Items.py"],
      },
      treeDirs: [],
      manifestSlugs: new Set(["oot"]),
    };
    const result = await discoverSlug(makeOctokit(state), "lallaria", "oot", "v1.1.0");
    expect(result.kind).toBe("ok");
    if (result.kind === "ok") {
      expect(result.slug).toBe("oot");
      expect(result.base).toBe("v1.0.0");
    }
  });

  it("multiple worlds touched → skip with multiple_candidates", async () => {
    const state: MockState = {
      releases: [{ tag_name: "v2.0.0" }, { tag_name: "v1.0.0" }],
      fork: false,
      compareFiles: {
        "v1.0.0...v2.0.0": [
          "worlds/pokemon_red/__init__.py",
          "worlds/pokemon_blue/__init__.py",
        ],
      },
      treeDirs: [],
      manifestSlugs: new Set(["pokemon_red", "pokemon_blue"]),
    };
    const result = await discoverSlug(makeOctokit(state), "x", "y", "v2.0.0");
    expect(result.kind).toBe("skip");
    if (result.kind === "skip") {
      expect(result.reason).toBe("multiple_candidates");
      expect(result.candidates.sort()).toEqual(["pokemon_blue", "pokemon_red"]);
    }
  });

  it("only non-world files changed → skip with no_candidates", async () => {
    const state: MockState = {
      releases: [{ tag_name: "v1.1.0" }, { tag_name: "v1.0.0" }],
      fork: false,
      compareFiles: {
        "v1.0.0...v1.1.0": [".github/workflows/ci.yml", "README.md"],
      },
      treeDirs: [],
      manifestSlugs: new Set(),
    };
    const result = await discoverSlug(makeOctokit(state), "x", "y", "v1.1.0");
    expect(result.kind).toBe("skip");
    if (result.kind === "skip") {
      expect(result.reason).toBe("no_candidates");
      expect(result.candidates).toEqual([]);
    }
  });

  it("infra worlds (_bizhawk) are filtered out", async () => {
    const state: MockState = {
      releases: [{ tag_name: "v1.1.0" }, { tag_name: "v1.0.0" }],
      fork: false,
      compareFiles: {
        "v1.0.0...v1.1.0": [
          "worlds/_bizhawk/foo.py",
          "worlds/oot/Items.py",
        ],
      },
      treeDirs: [],
      manifestSlugs: new Set(["oot"]),
    };
    const result = await discoverSlug(makeOctokit(state), "x", "y", "v1.1.0");
    expect(result.kind).toBe("ok");
    if (result.kind === "ok") {
      expect(result.slug).toBe("oot");
    }
  });

  it("from-scratch repo (no fork, no prior release) with single world → tree-scan fallback", async () => {
    const state: MockState = {
      releases: [{ tag_name: "v0.1.0" }],
      fork: false,
      compareFiles: {},
      treeDirs: ["myworld"],
      manifestSlugs: new Set(["myworld"]),
    };
    const result = await discoverSlug(makeOctokit(state), "x", "y", "v0.1.0");
    expect(result.kind).toBe("ok");
    if (result.kind === "ok") {
      expect(result.slug).toBe("myworld");
      expect(result.base).toBe("(whole-tree scan)");
    }
  });

  it("changed worlds/<slug>/ but no archipelago.json → filtered out", async () => {
    const state: MockState = {
      releases: [{ tag_name: "v1.1.0" }, { tag_name: "v1.0.0" }],
      fork: false,
      compareFiles: {
        "v1.0.0...v1.1.0": ["worlds/halfbaked/notes.md"],
      },
      treeDirs: [],
      manifestSlugs: new Set(),
    };
    const result = await discoverSlug(makeOctokit(state), "x", "y", "v1.1.0");
    expect(result.kind).toBe("skip");
    if (result.kind === "skip") {
      expect(result.reason).toBe("no_candidates");
    }
  });
});
