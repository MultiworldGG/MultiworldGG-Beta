import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import { handleReleasePublished } from "../src/handlers/release_published";
import { IndexBotData } from "../src/index-pr";

// The bundle path reads each world's archipelago.json out of its wheel (a real
// download+unzip). Mock that boundary: by default every recognized world has a
// seedable manifest; a test sets a slug to null to exercise the no-manifest skip.
const { wheelManifests } = vi.hoisted(() => ({
  wheelManifests: new Map<string, Record<string, unknown> | null>(),
}));
vi.mock("../src/wheel-manifest", () => ({
  fetchWheelManifest: async (_moduleLocation: string, slug: string) =>
    wheelManifests.has(slug)
      ? wheelManifests.get(slug)
      : { game: slug, world_version: "1.0.0", igdb_id: 1 },
}));
beforeEach(() => wheelManifests.clear());

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
  slug: "karen-head-of-multiworld-qa",
  owner: {},
  name: "Karen-Head-of-Multiworld-QA",
  description: "",
  external_url: "",
  html_url: "https://github.com/apps/karen-head-of-multiworld-qa",
  created_at: "",
  updated_at: "",
  permissions: {},
  events: [],
  installations_count: 0,
};
const OLIVER_DATA: IndexBotData = {
  id: 0,
  client_id: "o",
  slug: "oliver-the-multiworld-squirrel",
  owner: {},
  name: "Oliver-The-Multiworld-Squirrel",
  description: "",
  external_url: "",
  html_url: "https://github.com/apps/oliver-the-multiworld-squirrel",
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

// A `<name>.apworld` release asset (the Basic Manual fork flow attaches one by
// hand). Identifies the world; not pinned with a sha256, so its digest is null.
// Pass `name` directly to test a raw asset filename (e.g. an invalid stem).
function apworldAsset(opts: { slug?: string; name?: string; tag: string; repo?: string; size?: number }) {
  const repo = opts.repo ?? "MultiworldGG/myclgm-test";
  const name = opts.name ?? `${opts.slug}.apworld`;
  return {
    name,
    browser_download_url: `https://github.com/${repo}/releases/download/${opts.tag}/${name}`,
    size: opts.size ?? 64_000,
    digest: null,
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
  // Make the asset-digest wait instant in tests (no real backoff sleeps).
  process.env.OLIVER_DIGEST_WAIT_MS = "0";
});

afterEach(() => {
  fs.rmSync(tmpDir, { recursive: true, force: true });
  delete process.env.OLIVER_LOG_DIR;
  delete process.env.OLIVER_INDEX_REPO;
  delete process.env.OLIVER_DIGEST_WAIT_MS;
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

// ---------------------------------------------------------------------------
// World identification from a `<name>.apworld` release asset
// (the Basic Manual fork flow — author attaches the .whl and .apworld by hand
// under an arbitrary release tag, with no CI and no `<slug>-<version>` tag).
// ---------------------------------------------------------------------------

// Index-side probots wired so Karen commits and Oliver opens — mirrors the
// single-world happy-path setup above, shared across the apworld-asset tests.
function makeOpeningProbots(karenWrites: string[], oliverWrites: string[]) {
  const oliverIndexOctokit = makeOliverIndexOctokit(oliverWrites);
  const karenIndexOctokit = makeKarenIndexOctokit(karenWrites);
  const probot = { auth: vi.fn().mockResolvedValue(oliverIndexOctokit), log: fakeLog } as any;
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
  return { probot, karenProbot };
}

describe("handleReleasePublished — .apworld-asset identification", () => {
  it("uses the <name>.apworld asset as the slug under an arbitrary tag, pinning the wheel sha256", async () => {
    // Arbitrary tag with no usable `<slug>-<version>` prefix: only the .apworld
    // asset can identify the world.
    const tag = "v1.0.0";
    const state: RepoState = {
      releases: [
        {
          tag_name: tag,
          tagSha: "manual-sha",
          assets: [
            wheelAsset({ slug: "myclgm", version: "1.0.0", tag }),
            apworldAsset({ slug: "myclgm", tag }),
          ],
        },
      ],
      manifestAtRef: { game: "My Cool Game", authors: ["Berserker"] },
      indexInstall: { id: 12345 },
    };

    const karenWrites: string[] = [];
    const oliverWrites: string[] = [];
    const { probot, karenProbot } = makeOpeningProbots(karenWrites, oliverWrites);

    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, makeContext(state, tag));

    expect(karenWrites).toContain("createRef");
    expect(karenWrites).toContain("commit");
    expect(oliverWrites).toContain("pulls.create");

    const events = readEvents();
    expect(events[0]).toMatchObject({
      kind: "ok",
      slug: "myclgm",
      release_tag: "v1.0.0",
      release_sha: "manual-sha",
      wheel_asset: "myclgm-1.0.0-py3-none-any.whl",
      module_location:
        "https://github.com/MultiworldGG/myclgm-test/releases/download/v1.0.0/myclgm-1.0.0-py3-none-any.whl" +
        `#sha256=${"a".repeat(64)}`,
    });
  });

  it("the .apworld asset wins over a disagreeing <slug>-<version> tag prefix", async () => {
    // Tag prefix says `wrongslug`; the attached asset says `rightslug`. The
    // asset is authoritative.
    const tag = "wrongslug-9.9.9";
    const state: RepoState = {
      releases: [
        {
          tag_name: tag,
          tagSha: "manual-sha",
          assets: [
            wheelAsset({ slug: "rightslug", version: "9.9.9", tag }),
            apworldAsset({ slug: "rightslug", tag }),
          ],
        },
      ],
      manifestAtRef: { game: "Right Game" },
      indexInstall: { id: 12345 },
    };

    const { probot, karenProbot } = makeOpeningProbots([], []);
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, makeContext(state, tag));

    const events = readEvents();
    expect(events[0]).toMatchObject({ kind: "ok", slug: "rightslug", release_tag: "wrongslug-9.9.9" });
  });

  it("logs skip when more than one .apworld asset is attached", async () => {
    const tag = "myclgm-1.0.0";
    const state: RepoState = {
      releases: [
        {
          tag_name: tag,
          tagSha: "manual-sha",
          assets: [
            wheelAsset({ slug: "myclgm", version: "1.0.0", tag }),
            apworldAsset({ slug: "myclgm", tag }),
            apworldAsset({ slug: "extra", tag }),
          ],
        },
      ],
    };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, makeContext(state, tag));

    const events = readEvents();
    expect(events[0]).toMatchObject({
      kind: "skip",
      reason: "apworld_asset_ambiguous",
      slug: "myclgm", // provisional, from the tag prefix
    });
    expect(probot.auth).not.toHaveBeenCalled();
  });

  it("falls back to the tag prefix when the .apworld stem is not a valid slug", async () => {
    // GitHub turns spaces into dots, so a display-name apworld lands as
    // `My.Game.apworld` — an invalid slug. The `<slug>-<version>` tag prefix
    // still identifies the world (keeps the CI path working when both exist).
    const tag = "myclgm-1.0.0";
    const state: RepoState = {
      releases: [
        {
          tag_name: tag,
          tagSha: "manual-sha",
          assets: [
            wheelAsset({ slug: "myclgm", version: "1.0.0", tag }),
            apworldAsset({ name: "My.Game.apworld", tag }),
          ],
        },
      ],
      manifestAtRef: { game: "My Cool Game" },
      indexInstall: { id: 12345 },
    };

    const { probot, karenProbot } = makeOpeningProbots([], []);
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, makeContext(state, tag));

    const events = readEvents();
    expect(events[0]).toMatchObject({ kind: "ok", slug: "myclgm" });
  });

  it("logs no_slug_resolved when the only signal is an invalidly-named .apworld asset", async () => {
    // Arbitrary tag (no prefix) AND an invalid apworld stem → nothing trustworthy
    // to use as a folder name. Refuse rather than treat the raw asset name as a
    // path.
    const tag = "v1.0.0";
    const state: RepoState = {
      releases: [
        {
          tag_name: tag,
          tagSha: "manual-sha",
          assets: [
            wheelAsset({ slug: "myclgm", version: "1.0.0", tag }),
            apworldAsset({ name: "Bad.Name.apworld", tag }),
          ],
        },
      ],
    };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, makeContext(state, tag));

    const events = readEvents();
    expect(events[0]).toMatchObject({ kind: "skip", reason: "no_slug_resolved" });
    expect(probot.auth).not.toHaveBeenCalled();
  });

  it("logs skip when the .apworld identifies the world but no .whl is attached", async () => {
    const tag = "v1.0.0";
    const state: RepoState = {
      releases: [
        {
          tag_name: tag,
          tagSha: "manual-sha",
          assets: [apworldAsset({ slug: "myclgm", tag })],
        },
      ],
    };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, makeContext(state, tag));

    const events = readEvents();
    expect(events[0]).toMatchObject({ kind: "skip", reason: "wheel_asset_missing", slug: "myclgm" });
    expect(probot.auth).not.toHaveBeenCalled();
  });
});

// ---------------------------------------------------------------------------
// Bundled multi-world release (tag `worlds-wheels-<date>`)
// ---------------------------------------------------------------------------

const BUNDLE_TAG = "worlds-wheels-2026-06-06";

// A bundle wheel is `worlds_<module>-<version>-py3-none-any.whl`; the Index slug
// is <module>.
function bundleWheel(module: string, opts: { digest?: string | null } = {}) {
  return wheelAsset({ slug: `worlds_${module}`, version: "1.0.0", tag: BUNDLE_TAG, digest: opts.digest });
}

function bundleIndexManifest(game: string): string {
  return JSON.stringify({ game, world_version: "1.0.0", igdb_id: 1, module_location: "old" }, null, 2);
}

// Karen-token Index client for the bundle path: repo/git ops over a tiny
// present-manifests map. `present[path]` decides whether a world is on the Index
// (copy+edit) or skipped.
function makeBundleKarenIndexOctokit(present: Record<string, string>, writes: string[]): any {
  return {
    rest: {
      repos: {
        get: async () => ({ data: { default_branch: "main" } }),
        getContent: async ({ path }: { path: string }) => {
          if (present[path] !== undefined) {
            return {
              data: {
                type: "file",
                sha: `sha-${path}`,
                content: Buffer.from(present[path], "utf-8").toString("base64"),
                encoding: "base64",
              },
            };
          }
          throw Object.assign(new Error("404"), { status: 404 });
        },
        createOrUpdateFileContents: async ({ path }: { path: string }) => {
          writes.push(`commit:${path}`);
          return { data: {} };
        },
      },
      git: {
        getRef: async ({ ref }: { ref: string }) => {
          if (ref === "heads/main") return { data: { object: { sha: "main-sha", type: "commit" } } };
          throw Object.assign(new Error("404"), { status: 404 }); // branch absent → createRef
        },
        createRef: async () => {
          writes.push("createRef");
          return { data: {} };
        },
      },
    },
  };
}

// Same split as single-world: Karen commits, Oliver opens. Both share one writes
// log so assertions can check createRef/commit (Karen) and pulls.create (Oliver).
function makeBundleProbots(present: Record<string, string>, writes: string[]) {
  const oliverIndexOctokit = makeOliverIndexOctokit(writes);
  const karenIndexOctokit = makeBundleKarenIndexOctokit(present, writes);
  const probot = { auth: vi.fn().mockResolvedValue(oliverIndexOctokit), log: fakeLog } as any;
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
  return { probot, karenProbot };
}

describe("handleReleasePublished — bundled multi-world release", () => {
  it("opens one combined Index PR (Oliver token) for worlds already on the Index", async () => {
    const state: RepoState = {
      releases: [
        {
          tag_name: BUNDLE_TAG,
          tagSha: "bundle-sha",
          assets: [bundleWheel("dk64"), bundleWheel("oot"), bundleWheel("crosscode")],
        },
      ],
      indexInstall: { id: 12345 },
    };
    const present = {
      "worlds/dk64.json": bundleIndexManifest("Donkey Kong 64"),
      "worlds/oot.json": bundleIndexManifest("Ocarina of Time"),
      "worlds/crosscode.json": bundleIndexManifest("CrossCode"),
    };
    const writes: string[] = [];
    const { probot, karenProbot } = makeBundleProbots(present, writes);

    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, makeContext(state, BUNDLE_TAG));

    expect(writes).toContain("createRef");
    expect(writes.filter((w) => w.startsWith("commit:worlds/")).length).toBe(3);
    expect(writes).toContain("pulls.create");

    const events = readEvents();
    expect(events.find((e) => e.kind === "ok")).toMatchObject({
      kind: "ok",
      release_tag: BUNDLE_TAG,
      index_pr: 99,
    });
    expect(events.filter((e) => e.kind === "ok")).toHaveLength(1);
  });

  it("skips a wheel missing a digest but still opens the PR for the rest", async () => {
    const state: RepoState = {
      releases: [
        {
          tag_name: BUNDLE_TAG,
          tagSha: "bundle-sha",
          assets: [bundleWheel("dk64"), bundleWheel("oot", { digest: null })],
        },
      ],
      indexInstall: { id: 12345 },
    };
    const writes: string[] = [];
    const { probot, karenProbot } = makeBundleProbots(
      { "worlds/dk64.json": bundleIndexManifest("Donkey Kong 64") },
      writes,
    );

    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, makeContext(state, BUNDLE_TAG));

    const events = readEvents();
    expect(events).toContainEqual(
      expect.objectContaining({
        kind: "skip",
        reason: "asset_digest_missing",
        slug: "oot",
        wheel_asset: "worlds_oot-1.0.0-py3-none-any.whl",
      }),
    );
    expect(events.find((e) => e.kind === "ok")).toBeDefined();
    expect(writes).toContain("pulls.create");
  });

  it("skips an unrecognized wheel name and opens the PR for the recognized worlds", async () => {
    const state: RepoState = {
      releases: [
        {
          tag_name: BUNDLE_TAG,
          tagSha: "bundle-sha",
          // The second asset has no `worlds_` dist prefix → unrecognized.
          assets: [bundleWheel("dk64"), wheelAsset({ slug: "random", version: "1.0.0", tag: BUNDLE_TAG })],
        },
      ],
      indexInstall: { id: 12345 },
    };
    const writes: string[] = [];
    const { probot, karenProbot } = makeBundleProbots(
      { "worlds/dk64.json": bundleIndexManifest("Donkey Kong 64") },
      writes,
    );

    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, makeContext(state, BUNDLE_TAG));

    const events = readEvents();
    expect(events).toContainEqual(
      expect.objectContaining({
        kind: "skip",
        reason: "bundle_wheel_unrecognized",
        wheel_asset: "random-1.0.0-py3-none-any.whl",
      }),
    );
    expect(events.find((e) => e.kind === "ok")).toBeDefined();
    expect(writes).toContain("pulls.create");
  });

  it("seeds a brand-new world (not on the Index) from its wheel alongside an update", async () => {
    const state: RepoState = {
      releases: [
        {
          tag_name: BUNDLE_TAG,
          tagSha: "bundle-sha",
          assets: [bundleWheel("dk64"), bundleWheel("ghost")],
        },
      ],
      indexInstall: { id: 12345 },
    };
    const writes: string[] = [];
    // Only dk64 is on the Index; ghost is new — both wheels carry archipelago.json
    // (the mock default), so both are committed.
    const { probot, karenProbot } = makeBundleProbots(
      { "worlds/dk64.json": bundleIndexManifest("Donkey Kong 64") },
      writes,
    );

    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, makeContext(state, BUNDLE_TAG));

    const events = readEvents();
    expect(events.some((e) => e.reason === "bundle_world_no_manifest")).toBe(false);
    expect(events.find((e) => e.kind === "ok")).toBeDefined();
    expect(writes.filter((w) => w.startsWith("commit:worlds/")).sort()).toEqual([
      "commit:worlds/dk64.json",
      "commit:worlds/ghost.json",
    ]);
    expect(writes).toContain("pulls.create");
  });

  it("skips a world whose wheel has no archipelago.json, still opening the PR for the rest", async () => {
    wheelManifests.set("ghost", null); // ghost's wheel carries no manifest → skipped
    const state: RepoState = {
      releases: [
        {
          tag_name: BUNDLE_TAG,
          tagSha: "bundle-sha",
          assets: [bundleWheel("dk64"), bundleWheel("ghost")],
        },
      ],
      indexInstall: { id: 12345 },
    };
    const writes: string[] = [];
    const { probot, karenProbot } = makeBundleProbots(
      { "worlds/dk64.json": bundleIndexManifest("Donkey Kong 64") },
      writes,
    );

    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, makeContext(state, BUNDLE_TAG));

    const events = readEvents();
    expect(events).toContainEqual(
      expect.objectContaining({ kind: "skip", reason: "bundle_world_no_manifest", slug: "ghost" }),
    );
    expect(events.find((e) => e.kind === "ok")).toBeDefined();
    expect(writes.filter((w) => w.startsWith("commit:worlds/"))).toEqual(["commit:worlds/dk64.json"]);
  });

  it("opens no PR when no wheel carries an archipelago.json", async () => {
    wheelManifests.set("ghost1", null);
    wheelManifests.set("ghost2", null);
    const state: RepoState = {
      releases: [
        {
          tag_name: BUNDLE_TAG,
          tagSha: "bundle-sha",
          assets: [bundleWheel("ghost1"), bundleWheel("ghost2")],
        },
      ],
      indexInstall: { id: 12345 },
    };
    const writes: string[] = [];
    const { probot, karenProbot } = makeBundleProbots({}, writes);

    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, makeContext(state, BUNDLE_TAG));

    const events = readEvents();
    expect(events).toContainEqual(
      expect.objectContaining({ kind: "skip", reason: "bundle_no_valid_worlds" }),
    );
    expect(writes).not.toContain("pulls.create");
  });

  it("waits for a lagging asset digest, then includes that world once GitHub finishes hashing", async () => {
    const validDigest = `sha256:${"a".repeat(64)}`;
    const dl = (name: string) =>
      `https://github.com/MultiworldGG/myclgm-test/releases/download/${BUNDLE_TAG}/${name}`;
    let releaseFetches = 0;

    const state: RepoState = {
      releases: [{ tag_name: BUNDLE_TAG, tagSha: "bundle-sha" }],
      indexInstall: { id: 12345 },
    };
    const octokit = makeContextOctokit(state);
    // oot's digest is still being computed on the first read; it lands on the second.
    octokit.rest.repos.getReleaseByTag = async () => {
      releaseFetches += 1;
      const ootDigest = releaseFetches >= 2 ? validDigest : null;
      return {
        data: {
          tag_name: BUNDLE_TAG,
          assets: [
            {
              name: "worlds_dk64-1.0.0-py3-none-any.whl",
              browser_download_url: dl("worlds_dk64-1.0.0-py3-none-any.whl"),
              size: 158_720,
              digest: validDigest,
            },
            {
              name: "worlds_oot-1.0.0-py3-none-any.whl",
              browser_download_url: dl("worlds_oot-1.0.0-py3-none-any.whl"),
              size: 158_720,
              digest: ootDigest,
            },
          ],
        },
      };
    };

    const writes: string[] = [];
    const { probot, karenProbot } = makeBundleProbots(
      {
        "worlds/dk64.json": bundleIndexManifest("Donkey Kong 64"),
        "worlds/oot.json": bundleIndexManifest("Ocarina of Time"),
      },
      writes,
    );

    const ctx = {
      octokit,
      payload: { release: { tag_name: BUNDLE_TAG, draft: false } },
      log: fakeLog,
      repo: () => ({ owner: "MultiworldGG", repo: "myclgm-test" }),
    };
    await handleReleasePublished(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx as any);

    expect(releaseFetches).toBeGreaterThanOrEqual(2); // re-fetched after the lagging digest
    const events = readEvents();
    expect(events.some((e) => e.reason === "asset_digest_missing")).toBe(false); // oot not dropped
    expect(writes.filter((w) => w.startsWith("commit:worlds/")).sort()).toEqual([
      "commit:worlds/dk64.json",
      "commit:worlds/oot.json",
    ]);
    expect(writes).toContain("pulls.create");
  });
});
