import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import { handleReleasePublished } from "../src/handlers/release_published";
import { IndexBotData } from "../src/index-pr";

// ---------------------------------------------------------------------------
// Fixture types
// ---------------------------------------------------------------------------

interface ReleaseFixture {
  tag_name: string;
  draft?: boolean;
  // SHA the lightweight tag (or the annotated tag object) points to.
  tagSha: string;
  assets?: Array<{
    name: string;
    browser_download_url: string;
    size: number;
    digest?: string | null;
  }>;
}

interface RepoState {
  releases: ReleaseFixture[];
  manifestAtRef?: { game?: string; authors?: string[] };
  indexInstall?: { id: number };
  indexInstallNotFound?: boolean;
}

// ---------------------------------------------------------------------------
// Octokit / probot stubs
// ---------------------------------------------------------------------------

function makeContextOctokit(state: RepoState): any {
  return {
    rest: {
      repos: {
        listReleases: async () => ({
          data: state.releases.map((r) => ({ tag_name: r.tag_name, draft: r.draft ?? false })),
        }),
        getReleaseByTag: async ({ tag }: { tag: string }) => {
          const r = state.releases.find((x) => x.tag_name === tag);
          if (!r) throw Object.assign(new Error("404"), { status: 404 });
          return {
            data: {
              tag_name: r.tag_name,
              assets: (r.assets ?? []).map((a) => ({
                name: a.name,
                browser_download_url: a.browser_download_url,
                size: a.size,
                digest: a.digest === undefined ? `sha256:${"a".repeat(64)}` : a.digest,
              })),
            },
          };
        },
        getContent: async ({ path: p }: { path: string }) => {
          if (p.endsWith("archipelago.json") && state.manifestAtRef) {
            const json = JSON.stringify(state.manifestAtRef);
            return {
              data: {
                type: "file",
                content: Buffer.from(json, "utf-8").toString("base64"),
                encoding: "base64",
              },
            };
          }
          throw Object.assign(new Error("404"), { status: 404 });
        },
      },
      git: {
        getRef: async ({ ref }: { ref: string }) => {
          if (ref.startsWith("tags/")) {
            const tag = ref.slice("tags/".length);
            const release = state.releases.find((r) => r.tag_name === tag);
            if (release) {
              return { data: { object: { type: "commit", sha: release.tagSha } } };
            }
            throw Object.assign(new Error("404"), { status: 404 });
          }
          throw new Error(`unmocked getRef: ${ref}`);
        },
        getTag: async () => {
          throw new Error("not annotated in fixtures");
        },
      },
      apps: {
        getRepoInstallation: async () => {
          if (state.indexInstallNotFound) {
            throw Object.assign(new Error("404"), { status: 404 });
          }
          return { data: state.indexInstall ?? { id: 999 } };
        },
      },
    },
  };
}

const fakeLog = {
  trace: () => {},
  debug: () => {},
  info: () => {},
  warn: () => {},
  error: () => {},
  fatal: () => {},
  child: () => fakeLog,
};

function makeContext(state: RepoState, releaseTag: string, draft = false): any {
  return {
    octokit: makeContextOctokit(state),
    payload: {
      release: { tag_name: releaseTag, draft },
    },
    log: fakeLog,
    repo: () => ({ owner: "MultiworldGG", repo: "myclgm-test" }),
  };
}

function makeMinimalProbot() {
  return { auth: vi.fn(), log: fakeLog } as any;
}

const KAREN_DATA: IndexBotData = {
  id: 0,
  client_id: "k",
  slug: "karen-multiworld-bot",
  owner: {},
  name: "Karen-Multiworld-Bot",
  description: "",
  external_url: "",
  html_url: "https://github.com/apps/karen-multiworld-bot",
  created_at: "",
  updated_at: "",
  permissions: {},
  events: [],
  installations_count: 0,
};
const OLIVER_DATA: IndexBotData = {
  id: 0,
  client_id: "o",
  slug: "oliver-multiworld-squirrel",
  owner: {},
  name: "Oliver-Multiworld-Squirrel",
  description: "",
  external_url: "",
  html_url: "https://github.com/apps/oliver-multiworld-squirrel",
  created_at: "",
  updated_at: "",
  permissions: {},
  events: [],
  installations_count: 0,
};

function wheelAsset(opts: {
  slug: string;
  version: string;
  tag: string;
  repo?: string;
  size?: number;
  digest?: string | null;
}) {
  const repo = opts.repo ?? "MultiworldGG/myclgm-test";
  const distName = opts.slug.replace(/-/g, "_");
  const name = `${distName}-${opts.version}-py3-none-any.whl`;
  return {
    name,
    browser_download_url: `https://github.com/${repo}/releases/download/${opts.tag}/${name}`,
    size: opts.size ?? 158_720,
    digest: opts.digest === undefined ? `sha256:${"a".repeat(64)}` : opts.digest,
  };
}

// ---------------------------------------------------------------------------
// Index-side octokit stubs (identical to workflow_run.test.ts helpers)
// ---------------------------------------------------------------------------

function makeKarenIndexOctokit(writes: string[]): any {
  return {
    rest: {
      repos: {
        get: async () => ({ data: { default_branch: "main" } }),
        getContent: async () => {
          throw Object.assign(new Error("404"), { status: 404 });
        },
        createOrUpdateFileContents: async () => {
          writes.push("commit");
          return { data: {} };
        },
      },
      git: {
        getRef: async ({ ref }: { ref: string }) => {
          if (ref.endsWith("/main")) return { data: { object: { sha: "main-sha" } } };
          throw Object.assign(new Error("404"), { status: 404 });
        },
        createRef: async () => {
          writes.push("createRef");
          return { data: {} };
        },
      },
    },
  };
}

function makeOliverIndexOctokit(writes: string[]): any {
  return {
    rest: {
      pulls: {
        list: async () => ({ data: [] }),
        create: async () => {
          writes.push("pulls.create");
          return { data: { number: 99, node_id: "PR_node_99" } };
        },
      },
      issues: {
        addLabels: async ({ labels }: { labels: string[] }) => {
          writes.push(`labels:${labels.join(",")}`);
          return { data: [] };
        },
      },
    },
    graphql: async () => {
      writes.push("graphql");
      return { enablePullRequestAutoMerge: { pullRequest: { id: "PR_node_99" } } };
    },
  };
}

// ---------------------------------------------------------------------------
// Test setup / teardown
// ---------------------------------------------------------------------------

let tmpDir: string;

beforeEach(() => {
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "oliver-release-test-"));
  process.env.OLIVER_LOG_DIR = tmpDir;
  process.env.OLIVER_INDEX_REPO = "MultiworldGG/MultiworldGG-Index";
});

afterEach(() => {
  fs.rmSync(tmpDir, { recursive: true, force: true });
  delete process.env.OLIVER_LOG_DIR;
  delete process.env.OLIVER_INDEX_REPO;
});

function readEvents(): any[] {
  const file = path.join(tmpDir, "events.jsonl");
  if (!fs.existsSync(file)) return [];
  return fs.readFileSync(file, "utf-8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe("handleReleasePublished", () => {
  it("happy path: opens Index PR with release-asset module_location", async () => {
    const tag = "myclgm-1.0.0";
    const state: RepoState = {
      releases: [
        {
          tag_name: tag,
          tagSha: "release-sha-abc",
          assets: [wheelAsset({ slug: "myclgm", version: "1.0.0", tag })],
        },
      ],
      manifestAtRef: { game: "My Cool Game", authors: ["Berserker"] },
      indexInstall: { id: 12345 },
    };

    const karenWrites: string[] = [];
    const oliverWrites: string[] = [];
    const oliverIndexOctokit = makeOliverIndexOctokit(oliverWrites);
    const karenIndexOctokit = makeKarenIndexOctokit(karenWrites);

    const probot = {
      auth: vi.fn().mockResolvedValue(oliverIndexOctokit),
      log: fakeLog,
    } as any;
    const karenAppOctokit = {
      rest: { apps: { getRepoInstallation: async () => ({ data: { id: 67890 } }) } },
    };
    const karenProbot = {
      auth: vi.fn().mockImplementation((id?: number) => {
        if (id === undefined) return Promise.resolve(karenAppOctokit);
        if (id === 67890) return Promise.resolve(karenIndexOctokit);
        throw new Error(`unexpected karen auth id: ${id}`);
      }),
      log: fakeLog,
    } as any;

    const ctx = makeContext(state, tag);
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);

    expect(probot.auth).toHaveBeenCalledWith(12345);
    expect(karenProbot.auth).toHaveBeenCalledWith(67890);
    expect(karenWrites).toContain("createRef");
    expect(karenWrites).toContain("commit");
    expect(oliverWrites).toContain("pulls.create");

    const events = readEvents();
    expect(events[0]).toMatchObject({
      kind: "ok",
      slug: "myclgm",
      release_tag: "myclgm-1.0.0",
      release_sha: "release-sha-abc",
      wheel_asset: "myclgm-1.0.0-py3-none-any.whl",
      wheel_size_bytes: 158_720,
      module_location:
        "https://github.com/MultiworldGG/myclgm-test/releases/download/myclgm-1.0.0/myclgm-1.0.0-py3-none-any.whl" +
        `#sha256=${"a".repeat(64)}`,
    });
  });

  it("skips draft releases without emitting an event", async () => {
    const state: RepoState = { releases: [] };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, "myclgm-1.0.0", /* draft= */ true);
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    expect(probot.auth).not.toHaveBeenCalled();
    expect(readEvents()).toEqual([]);
  });

  it("logs skip when the tag cannot be resolved to a commit SHA", async () => {
    // State has no matching release → git.getRef returns 404 → TagLookupError
    const state: RepoState = { releases: [] };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, "myclgm-1.0.0");
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    const events = readEvents();
    expect(events).toHaveLength(1);
    expect(events[0]).toMatchObject({
      kind: "skip",
      reason: "tag_sha_lookup_failed",
      release_tag: "myclgm-1.0.0",
    });
    expect(probot.auth).not.toHaveBeenCalled();
  });

  it("logs skip when the release tag has no slug prefix", async () => {
    const tag = "v1.0.0";
    const state: RepoState = {
      releases: [{ tag_name: tag, tagSha: "release-sha-abc" }],
    };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, tag);
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    const events = readEvents();
    expect(events[0]).toMatchObject({ kind: "skip", reason: "no_slug_resolved" });
    expect(probot.auth).not.toHaveBeenCalled();
  });

  it("logs skip when the release has no .whl asset", async () => {
    const tag = "myclgm-1.0.0";
    const state: RepoState = {
      releases: [{ tag_name: tag, tagSha: "release-sha-abc", assets: [] }],
    };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, tag);
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    const events = readEvents();
    expect(events[0]).toMatchObject({ kind: "skip", reason: "wheel_asset_missing", slug: "myclgm" });
    expect(probot.auth).not.toHaveBeenCalled();
  });

  it("logs skip when the release has multiple .whl assets", async () => {
    const tag = "myclgm-1.0.0";
    const state: RepoState = {
      releases: [
        {
          tag_name: tag,
          tagSha: "release-sha-abc",
          assets: [
            wheelAsset({ slug: "myclgm", version: "1.0.0", tag }),
            wheelAsset({ slug: "clique_extra", version: "1.0.0", tag }),
          ],
        },
      ],
    };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, tag);
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    const events = readEvents();
    expect(events[0]).toMatchObject({
      kind: "skip",
      reason: "wheel_asset_ambiguous",
      slug: "myclgm",
    });
    expect(probot.auth).not.toHaveBeenCalled();
  });

  it("logs skip when the wheel asset has no SHA256 digest", async () => {
    const tag = "myclgm-1.0.0";
    const state: RepoState = {
      releases: [
        {
          tag_name: tag,
          tagSha: "release-sha-abc",
          assets: [wheelAsset({ slug: "myclgm", version: "1.0.0", tag, digest: null })],
        },
      ],
    };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, tag);
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    const events = readEvents();
    expect(events[0]).toMatchObject({
      kind: "skip",
      reason: "asset_digest_missing",
      slug: "myclgm",
    });
    expect(probot.auth).not.toHaveBeenCalled();
  });

  it("logs skip when getReleaseByTag returns 404", async () => {
    const tag = "myclgm-1.0.0";
    // tagSha resolves fine (tag is in state.releases), but getReleaseByTag
    // would look up by tag_name — remove assets to force us to think about
    // what happens if the release disappears between event and handler.
    // Simulate by providing a state where getRef succeeds but getReleaseByTag
    // would 404: we add the release without a tag_name match for getReleaseByTag
    // by giving it a different tag_name for the asset lookup.
    const state: RepoState = {
      releases: [
        // Provide the tagSha resolution (getRef looks up by tag_name).
        // But getReleaseByTag also looks up by tag_name, so we want it to 404.
        // Trick: tagSha entry uses the real tag; the assets lookup fixture uses
        // a *different* tag so find() misses — that would need two fixtures.
        // Simpler: use a custom octokit override below.
        { tag_name: tag, tagSha: "release-sha-abc" },
      ],
    };

    // Override getReleaseByTag to always 404 for this test.
    const baseOctokit = makeContextOctokit(state);
    const octokit = {
      ...baseOctokit,
      rest: {
        ...baseOctokit.rest,
        repos: {
          ...baseOctokit.rest.repos,
          getReleaseByTag: async () => {
            throw Object.assign(new Error("404"), { status: 404 });
          },
        },
      },
    };

    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = {
      octokit,
      payload: { release: { tag_name: tag, draft: false } },
      log: fakeLog,
      repo: () => ({ owner: "MultiworldGG", repo: "myclgm-test" }),
    };
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx as any);
    const events = readEvents();
    expect(events[0]).toMatchObject({ kind: "skip", reason: "release_lookup_404", slug: "myclgm" });
    expect(probot.auth).not.toHaveBeenCalled();
  });
});
