import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import { handleWorkflowRun } from "../src/handlers/workflow_run";
import { IndexBotData } from "../src/index-pr";

interface ReleaseFixture {
  tag_name: string;
  draft?: boolean;
  tagSha: string;
  // Assets attached to the release. `digest` is the GitHub-supplied SHA256 in
  // the form `sha256:<hex>`; null/undefined simulates an old release for which
  // the API does not expose a digest.
  assets?: Array<{
    name: string;
    browser_download_url: string;
    size: number;
    digest?: string | null;
  }>;
}

interface RepoState {
  variables: Record<string, string>;
  releases: ReleaseFixture[];
  manifestAtRef?: { game?: string; authors?: string[] };
  indexInstall?: { id: number };
  indexInstallNotFound?: boolean;
}

function makeContextOctokit(state: RepoState): any {
  return {
    request: async (route: string, params: { name: string }) => {
      if (route.includes("/actions/variables/")) {
        const v = state.variables[params.name];
        if (v == null) {
          throw Object.assign(new Error("404"), { status: 404 });
        }
        return { data: { name: params.name, value: v } };
      }
      throw new Error(`unmocked request: ${route}`);
    },
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

function makePayload(overrides: Partial<{
  name: string;
  event: string;
  conclusion: string;
  head_sha: string;
}> = {}) {
  return {
    workflow_run: {
      id: 1,
      name: overrides.name ?? "Create and Release Python Package",
      event: overrides.event ?? "release",
      conclusion: overrides.conclusion ?? "success",
      head_sha: overrides.head_sha ?? "release-sha-abc",
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

function makeContext(state: RepoState, payload: any): any {
  return {
    octokit: makeContextOctokit(state),
    payload,
    log: fakeLog,
    repo: () => ({ owner: "MultiworldGG", repo: "clique-test" }),
  };
}

let tmpDir: string;

beforeEach(() => {
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "oliver-handler-test-"));
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
  const repo = opts.repo ?? "MultiworldGG/clique-test";
  const distName = opts.slug.replace(/-/g, "_");
  const name = `${distName}-${opts.version}-py3-none-any.whl`;
  return {
    name,
    browser_download_url: `https://github.com/${repo}/releases/download/${opts.tag}/${name}`,
    size: opts.size ?? 158_720,
    digest: opts.digest === undefined ? `sha256:${"a".repeat(64)}` : opts.digest,
  };
}

describe("handleWorkflowRun", () => {
  it("ignores workflow_run for non-target workflow name", async () => {
    const state: RepoState = { variables: {}, releases: [] };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, makePayload({ name: "Some Other Workflow" }));
    await handleWorkflowRun(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    expect(probot.auth).not.toHaveBeenCalled();
    expect(readEvents()).toEqual([]);
  });

  it("ignores workflow_run not triggered by release", async () => {
    const state: RepoState = { variables: {}, releases: [] };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, makePayload({ event: "push" }));
    await handleWorkflowRun(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    expect(probot.auth).not.toHaveBeenCalled();
    expect(readEvents()).toEqual([]);
  });

  it("logs skip when workflow conclusion is failure", async () => {
    const state: RepoState = { variables: {}, releases: [] };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, makePayload({ conclusion: "failure" }));
    await handleWorkflowRun(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    const events = readEvents();
    expect(events).toHaveLength(1);
    expect(events[0].kind).toBe("skip");
    expect(events[0].reason).toBe("workflow_failure");
  });

  it("logs skip when WORLD_FOLDER_NAME is unset and release tag has no slug prefix", async () => {
    // Tag `v1.0.0` has no `-`, so neither the WORLD_FOLDER_NAME path nor the
    // tag-prefix fallback can resolve a slug.
    const state: RepoState = {
      variables: {},
      releases: [{ tag_name: "v1.0.0", tagSha: "release-sha-abc" }],
    };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, makePayload({ head_sha: "release-sha-abc" }));
    await handleWorkflowRun(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    const events = readEvents();
    expect(events[0]).toMatchObject({ kind: "skip", reason: "no_slug_resolved" });
  });

  it("resolves slug from `<slug>-<v>` release tag prefix when WORLD_FOLDER_NAME is unset", async () => {
    // Multi-world repo path: tag `mariolands-1.2.3` → slug `mariolands`.
    const state: RepoState = {
      variables: {},
      releases: [
        {
          tag_name: "mariolands-1.2.3",
          tagSha: "release-sha-abc",
          assets: [wheelAsset({ slug: "mariolands", version: "1.2.3", tag: "mariolands-1.2.3" })],
        },
      ],
      manifestAtRef: { game: "Mariolands", authors: ["TheLX5"] },
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

    const ctx = makeContext(state, makePayload({ head_sha: "release-sha-abc" }));
    await handleWorkflowRun(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    const events = readEvents();
    expect(events[0]).toMatchObject({
      kind: "ok",
      slug: "mariolands",
      release_tag: "mariolands-1.2.3",
      module_location:
        "https://github.com/MultiworldGG/clique-test/releases/download/mariolands-1.2.3/mariolands-1.2.3-py3-none-any.whl" +
        `#sha256=${"a".repeat(64)}`,
    });
  });

  it("logs skip when the release has no .whl asset", async () => {
    const state: RepoState = {
      variables: { WORLD_FOLDER_NAME: "clique" },
      releases: [{ tag_name: "v1.0.0", tagSha: "release-sha-abc", assets: [] }],
    };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, makePayload({ head_sha: "release-sha-abc" }));
    await handleWorkflowRun(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    const events = readEvents();
    expect(events[0]).toMatchObject({
      kind: "skip",
      reason: "wheel_asset_missing",
      slug: "clique",
    });
  });

  it("logs skip when the release has multiple .whl assets (ambiguous)", async () => {
    const state: RepoState = {
      variables: { WORLD_FOLDER_NAME: "clique" },
      releases: [
        {
          tag_name: "v1.0.0",
          tagSha: "release-sha-abc",
          assets: [
            wheelAsset({ slug: "clique", version: "1.0.0", tag: "v1.0.0" }),
            wheelAsset({ slug: "clique-extra", version: "1.0.0", tag: "v1.0.0" }),
          ],
        },
      ],
    };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, makePayload({ head_sha: "release-sha-abc" }));
    await handleWorkflowRun(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    const events = readEvents();
    expect(events[0]).toMatchObject({
      kind: "skip",
      reason: "wheel_asset_ambiguous",
      slug: "clique",
    });
  });

  it("logs error when Oliver is not installed on the Index", async () => {
    const state: RepoState = {
      variables: { WORLD_FOLDER_NAME: "clique" },
      releases: [
        {
          tag_name: "v1.0.0",
          tagSha: "release-sha-abc",
          assets: [wheelAsset({ slug: "clique", version: "1.0.0", tag: "v1.0.0" })],
        },
      ],
      indexInstallNotFound: true,
    };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, makePayload({ head_sha: "release-sha-abc" }));
    await handleWorkflowRun(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    const events = readEvents();
    expect(events[0]).toMatchObject({ kind: "error", reason: "index_install_missing" });
  });

  it("happy path: Karen creates branch+commit, Oliver opens PR with release-asset module_location", async () => {
    const state: RepoState = {
      variables: { WORLD_FOLDER_NAME: "clique" },
      releases: [
        {
          tag_name: "v1.0.0",
          tagSha: "release-sha-abc",
          assets: [wheelAsset({ slug: "clique", version: "1.0.0", tag: "v1.0.0" })],
        },
      ],
      manifestAtRef: { game: "Clique", authors: ["Berserker"] },
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

    const ctx = makeContext(state, makePayload({ head_sha: "release-sha-abc" }));
    await handleWorkflowRun(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    expect(probot.auth).toHaveBeenCalledWith(12345);
    expect(karenProbot.auth).toHaveBeenCalledWith(67890);
    expect(karenWrites).toContain("createRef");
    expect(karenWrites).toContain("commit");
    expect(oliverWrites).toContain("pulls.create");
    const events = readEvents();
    expect(events[0]).toMatchObject({
      kind: "ok",
      slug: "clique",
      release_tag: "v1.0.0",
      wheel_asset: "clique-1.0.0-py3-none-any.whl",
      wheel_size_bytes: 158_720,
      module_location:
        "https://github.com/MultiworldGG/clique-test/releases/download/v1.0.0/clique-1.0.0-py3-none-any.whl" +
        `#sha256=${"a".repeat(64)}`,
    });
  });

  it("logs skip when the wheel asset has no SHA256 digest from the GitHub API", async () => {
    // GitHub returns digest:null on releases predating the digest-exposure
    // rollout, or potentially on assets uploaded via certain API paths.
    // Oliver bails rather than open an Index PR pointing at unverifiable
    // bytes (the URL is otherwise mutable via gh release upload).
    const state: RepoState = {
      variables: { WORLD_FOLDER_NAME: "clique" },
      releases: [
        {
          tag_name: "v1.0.0",
          tagSha: "release-sha-abc",
          assets: [
            wheelAsset({ slug: "clique", version: "1.0.0", tag: "v1.0.0", digest: null }),
          ],
        },
      ],
    };
    const probot = makeMinimalProbot();
    const karenProbot = makeMinimalProbot();
    const ctx = makeContext(state, makePayload({ head_sha: "release-sha-abc" }));
    await handleWorkflowRun(probot, karenProbot, OLIVER_DATA, KAREN_DATA, ctx);
    expect(probot.auth).not.toHaveBeenCalled();
    const events = readEvents();
    expect(events[0]).toMatchObject({
      kind: "skip",
      reason: "asset_digest_missing",
      slug: "clique",
    });
  });
});

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
