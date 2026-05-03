import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import { handleWorkflowRun } from "../src/handlers/workflow_run";

interface RepoState {
  variables: Record<string, string>;
  releases: Array<{ tag_name: string; draft?: boolean; tagSha: string }>;
  wheelTags: Record<string, string>;
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
            const wheelSha = state.wheelTags[tag];
            if (wheelSha) {
              return { data: { object: { type: "commit", sha: wheelSha } } };
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
    repo: () => ({ owner: "lallaria", repo: "clique-test" }),
  };
}

let tmpDir: string;

beforeEach(() => {
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "oliver-handler-test-"));
  process.env.OLIVER_LOG_DIR = tmpDir;
  process.env.OLIVER_INDEX_REPO = "lallaria/MultiworldGG-Index";
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

describe("handleWorkflowRun", () => {
  it("ignores workflow_run for non-target workflow name", async () => {
    const state: RepoState = { variables: {}, releases: [], wheelTags: {} };
    const probot = { auth: vi.fn(), log: fakeLog } as any;
    const ctx = makeContext(state, makePayload({ name: "Some Other Workflow" }));
    await handleWorkflowRun(probot, ctx);
    expect(probot.auth).not.toHaveBeenCalled();
    expect(readEvents()).toEqual([]);
  });

  it("ignores workflow_run not triggered by release", async () => {
    const state: RepoState = { variables: {}, releases: [], wheelTags: {} };
    const probot = { auth: vi.fn(), log: fakeLog } as any;
    const ctx = makeContext(state, makePayload({ event: "push" }));
    await handleWorkflowRun(probot, ctx);
    expect(probot.auth).not.toHaveBeenCalled();
    expect(readEvents()).toEqual([]);
  });

  it("logs skip when workflow conclusion is failure", async () => {
    const state: RepoState = { variables: {}, releases: [], wheelTags: {} };
    const probot = { auth: vi.fn(), log: fakeLog } as any;
    const ctx = makeContext(state, makePayload({ conclusion: "failure" }));
    await handleWorkflowRun(probot, ctx);
    const events = readEvents();
    expect(events).toHaveLength(1);
    expect(events[0].kind).toBe("skip");
    expect(events[0].reason).toBe("workflow_failure");
  });

  it("logs skip when WORLD_FOLDER_NAME is missing", async () => {
    const state: RepoState = { variables: {}, releases: [], wheelTags: {} };
    const probot = { auth: vi.fn(), log: fakeLog } as any;
    const ctx = makeContext(state, makePayload());
    await handleWorkflowRun(probot, ctx);
    const events = readEvents();
    expect(events[0]).toMatchObject({ kind: "skip", reason: "no_world_folder_name" });
  });

  it("logs skip when wheel tag is missing", async () => {
    const state: RepoState = {
      variables: { WORLD_FOLDER_NAME: "clique" },
      releases: [{ tag_name: "v1.0.0", tagSha: "release-sha-abc" }],
      wheelTags: {},
    };
    const probot = { auth: vi.fn(), log: fakeLog } as any;
    const ctx = makeContext(state, makePayload({ head_sha: "release-sha-abc" }));
    await handleWorkflowRun(probot, ctx);
    const events = readEvents();
    expect(events[0]).toMatchObject({ kind: "skip", reason: "tag_missing", slug: "clique" });
  });

  it("logs error when Oliver is not installed on the Index", async () => {
    const state: RepoState = {
      variables: { WORLD_FOLDER_NAME: "clique" },
      releases: [{ tag_name: "v1.0.0", tagSha: "release-sha-abc" }],
      wheelTags: { "wheel/worlds/clique/v1.0.0": "wheel-sha-def" },
      indexInstallNotFound: true,
    };
    const probot = { auth: vi.fn(), log: fakeLog } as any;
    const ctx = makeContext(state, makePayload({ head_sha: "release-sha-abc" }));
    await handleWorkflowRun(probot, ctx);
    const events = readEvents();
    expect(events[0]).toMatchObject({ kind: "error", reason: "index_install_missing" });
  });

  it("happy path: opens Index PR and logs ok", async () => {
    const state: RepoState = {
      variables: { WORLD_FOLDER_NAME: "clique" },
      releases: [{ tag_name: "v1.0.0", tagSha: "release-sha-abc" }],
      wheelTags: { "wheel/worlds/clique/v1.0.0": "wheel-sha-def" },
      manifestAtRef: { game: "Clique", authors: ["Berserker"] },
      indexInstall: { id: 12345 },
    };

    const indexOctokit = {
      rest: {
        repos: {
          get: async () => ({ data: { default_branch: "main" } }),
          getContent: async () => {
            throw Object.assign(new Error("404"), { status: 404 });
          },
          createOrUpdateFileContents: async () => ({ data: {} }),
        },
        git: {
          getRef: async ({ ref }: { ref: string }) => {
            if (ref.endsWith("/main")) {
              return { data: { object: { sha: "main-sha" } } };
            }
            throw Object.assign(new Error("404"), { status: 404 });
          },
          createRef: async () => ({ data: {} }),
        },
        pulls: {
          list: async () => ({ data: [] }),
          create: async () => ({ data: { number: 99 } }),
        },
      },
    };

    const probot = {
      auth: vi.fn().mockResolvedValue(indexOctokit),
      log: fakeLog,
    } as any;
    const ctx = makeContext(state, makePayload({ head_sha: "release-sha-abc" }));
    await handleWorkflowRun(probot, ctx);
    expect(probot.auth).toHaveBeenCalledWith(12345);
    const events = readEvents();
    expect(events[0]).toMatchObject({
      kind: "ok",
      slug: "clique",
      release_tag: "v1.0.0",
      wheel_sha: "wheel-sha-def",
      index_pr: 99,
    });
  });
});
