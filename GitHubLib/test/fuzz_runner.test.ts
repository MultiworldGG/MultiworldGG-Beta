import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import type { ChildProcess } from "child_process";

// child_process.execFile is the one external boundary we mock; everything else
// (fs/promises, the wall-clock timer) runs for real against a tmp work dir, the
// same real-fs style the other handler tests use.
const execFileMock = vi.fn();
vi.mock("child_process", () => ({
  execFile: (...args: unknown[]) => execFileMock(...args),
}));

import {
  runFuzzContainer,
  buildDockerArgs,
  ensureImageAvailable,
  type RunFuzzOptions,
} from "../src/fuzz/runner";
import type { FuzzJob } from "../src/fuzz/types";

const VALID_WHEEL =
  "https://github.com/alice/hk/releases/download/hk-1.0.0/hk-1.0.0-py3-none-any.whl";

function job(overrides: Partial<FuzzJob> = {}): FuzzJob {
  return {
    slug: "hk",
    wheelUrl: VALID_WHEEL,
    sha256: "a".repeat(64),
    runs: 50,
    timeoutS: 30,
    yamls: "1-10",
    threads: 10,
    sizeCapMb: 250,
    prNumber: 42,
    headSha: "b".repeat(40),
    ...overrides,
  };
}

let tmpDir: string;
const logs: string[] = [];

function options(overrides: Partial<RunFuzzOptions> = {}): RunFuzzOptions {
  return {
    image: "ghcr.io/multiworldgg/fuzz:latest",
    workDir: tmpDir,
    // Offline runner fetches the wheel itself; inject a no-network fake that just
    // writes the bind file so runFuzzContainer tests never touch the network.
    fetchWheel: async (_url: string, _sha: string, dest: string) => {
      fs.writeFileSync(dest, "wheel-bytes");
    },
    log: (m: string) => logs.push(m),
    ...overrides,
  };
}

/** Find the path argument of the `-v <host>:/out:rw` bind in a docker argv. */
function outBindHostPath(args: string[]): string {
  const vIdx = args.indexOf("-v");
  expect(vIdx).toBeGreaterThanOrEqual(0);
  const bind = args[vIdx + 1];
  const marker = ":/out:rw";
  expect(bind.endsWith(marker)).toBe(true);
  return bind.slice(0, -marker.length);
}

/** Collect every `-e KEY=VALUE` pair from a docker argv into a map. */
function envPairs(args: string[]): Record<string, string> {
  const out: Record<string, string> = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "-e") {
      const eq = args[i + 1].indexOf("=");
      out[args[i + 1].slice(0, eq)] = args[i + 1].slice(eq + 1);
    }
  }
  return out;
}

/**
 * Drive the execFile mock: when `docker run …` is invoked, write `result.json`
 * into the bind's host out dir (using whatever `produce` returns) and then invoke
 * the callback to simulate the container exiting with `exitCode`. `docker rm …`
 * (and any non-run call) just succeeds. Returns the fake ChildProcess.
 */
function mockRun(produce: () => unknown, exitCode = 0, stderr = ""): void {
  execFileMock.mockImplementation(
    (_file: string, args: string[], a3?: unknown, a4?: unknown) => {
      const cb = (typeof a3 === "function" ? a3 : a4) as
        | ((err: Error | null, stdout: string, stderr: string) => void)
        | undefined;
      const child = { kill: vi.fn() } as unknown as ChildProcess;

      if (args[0] === "run") {
        const hostOut = outBindHostPath(args);
        const value = produce();
        if (value !== undefined) {
          fs.mkdirSync(hostOut, { recursive: true });
          fs.writeFileSync(
            path.join(hostOut, "result.json"),
            typeof value === "string" ? value : JSON.stringify(value),
          );
        }
        const err =
          exitCode === 0
            ? null
            : (Object.assign(new Error(`exit ${exitCode}`), { code: exitCode }) as Error);
        queueMicrotask(() => cb?.(err, "", stderr));
      } else {
        queueMicrotask(() => cb?.(null, "", ""));
      }
      return child;
    },
  );
}

beforeEach(() => {
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "mwgg-fuzz-runner-"));
  logs.length = 0;
  execFileMock.mockReset();
});

afterEach(() => {
  vi.useRealTimers();
  fs.rmSync(tmpDir, { recursive: true, force: true });
});

describe("buildDockerArgs — hardening flags", () => {
  it("emits every required hardening flag", () => {
    const args = buildDockerArgs(job(), options(), "mwgg-fuzz-42-hk-x", "/work/out", "/work/in");

    expect(args[0]).toBe("run");
    expect(args).toContain("--rm");
    expect(args).toContain("--read-only");
    expect(args).toContain("--cap-drop");
    expect(args).toContain("ALL");
    expect(args).toContain("--security-opt");
    expect(args).toContain("no-new-privileges");

    // value-bearing flags: assert the adjacent value, not just presence.
    const pairAfter = (flag: string): string => args[args.indexOf(flag) + 1];
    expect(pairAfter("--name")).toBe("mwgg-fuzz-42-hk-x");
    expect(pairAfter("--user")).toBe("65532:65532");
    expect(pairAfter("--pids-limit")).toBe("512");
    expect(pairAfter("--cpus")).toBe("2");
    expect(pairAfter("--memory")).toBe("4g");
    expect(pairAfter("--memory-swap")).toBe("4g");
    expect(pairAfter("--ulimit")).toBe("nofile=4096:4096");
    expect(pairAfter("--network")).toBe("none");
    // wheel arrives as a read-only bind mount at /in.
    expect(args).toContain("/work/in:/in:ro");

    // both tmpfs mounts present
    const tmpfs = args.filter((_, i) => args[i - 1] === "--tmpfs");
    expect(tmpfs).toContain("/tmp:rw,noexec,nosuid,size=512m,mode=1777");
    expect(tmpfs).toContain("/work:rw,nosuid,size=4g,mode=1777");

    // the out bind and the image come last (image is the final arg).
    expect(outBindHostPath(args)).toBe("/work/out");
    expect(args[args.length - 1]).toBe("ghcr.io/multiworldgg/fuzz:latest");
  });

  it("adds READ-ONLY rom + host.yaml mounts only when romDir/hostYaml are set", () => {
    const vmounts = (a: string[]): string[] => a.filter((_, i) => a[i - 1] === "-v");

    const without = buildDockerArgs(job(), options(), "n", "/work/out", "/work/in");
    expect(vmounts(without).some((m) => m.includes(":/roms:ro"))).toBe(false);
    expect(vmounts(without).some((m) => m.includes("/opt/fuzz/host.yaml:ro"))).toBe(false);

    const withRoms = buildDockerArgs(
      job(),
      options({ romDir: "/var/lib/mwgg-fuzz-roms", hostYaml: "/var/lib/host.yaml" }),
      "n",
      "/work/out",
      "/work/in",
    );
    expect(vmounts(withRoms)).toContain("/var/lib/mwgg-fuzz-roms:/roms:ro");
    expect(vmounts(withRoms)).toContain("/var/lib/host.yaml:/opt/fuzz/host.yaml:ro");
  });

  it("passes the scan size cap through as FUZZ_SIZE_CAP_MB", () => {
    const env = envPairs(buildDockerArgs(job({ sizeCapMb: 512 }), options(), "n", "/work/out", "/work/in"));
    expect(env.FUZZ_SIZE_CAP_MB).toBe("512");
  });

  it("passes one -e per documented input with the job/opts values", () => {
    const args = buildDockerArgs(
      job({ slug: "rop", runs: 7, timeoutS: 11, yamls: "2-3", threads: 4 }),
      options(),
      "n",
      "/work/out",
      "/work/in",
    );
    const env = envPairs(args);

    expect(env.FUZZ_SLUG).toBe("rop");
    expect(env.FUZZ_WHEEL_SHA256).toBe("a".repeat(64));
    expect(env.FUZZ_RUNS).toBe("7");
    expect(env.FUZZ_TIMEOUT).toBe("11");
    expect(env.FUZZ_YAMLS).toBe("2-3");
    expect(env.FUZZ_THREADS).toBe("4");
    expect(env.KIVY_NO_ARGS).toBe("1");
    expect(env.SKIP_ALL_INSTALLS).toBe("1");
    expect(env.MALLOC_ARENA_MAX).toBe("2");
    // Offline container: no fetch URL / core / fuzzer env is passed.
    expect(env.FUZZ_WHEEL_URL).toBeUndefined();
    expect(env.MWGG_CORE_REPO).toBeUndefined();
    expect(env.FUZZER_REPO).toBeUndefined();
  });

  it("honors resource overrides", () => {
    const args = buildDockerArgs(
      job(),
      options({ cpus: "1", memory: "2g", pids: 128 }),
      "n",
      "/work/out",
      "/work/in",
    );
    const pairAfter = (flag: string): string => args[args.indexOf(flag) + 1];
    expect(pairAfter("--network")).toBe("none");
    expect(pairAfter("--cpus")).toBe("1");
    expect(pairAfter("--memory")).toBe("2g");
    expect(pairAfter("--memory-swap")).toBe("2g");
    expect(pairAfter("--pids-limit")).toBe("128");
  });

  it("sanitizes the container name to a lowercase docker-safe token", async () => {
    mockRun(() => ({ slug: "hk", status: "pass", exit_code: 0 }));
    await runFuzzContainer(job({ slug: "hk", prNumber: 42 }), options());

    const runArgs = execFileMock.mock.calls.find((c) => (c[1] as string[])[0] === "run")![1] as string[];
    const name = runArgs[runArgs.indexOf("--name") + 1];
    expect(name).toMatch(/^mwgg-fuzz-42-hk-[a-z0-9-]+$/);
    expect(name).toBe(name.toLowerCase());
  });
});

describe("runFuzzContainer — result.json mapping", () => {
  it("maps a passing result.json to a FuzzWorldResult and cleans up the job dir", async () => {
    mockRun(() => ({
      slug: "hk",
      status: "pass",
      stats: { success: 50, failure: 0, timeout: 0, ignored: 0, total: 50 },
      scan: { bandit: { high: 0 }, size_mb: 3 },
      exit_code: 0,
      log_tail: "all good\nfuzz complete",
    }));

    const res = await runFuzzContainer(job(), options());

    expect(res.slug).toBe("hk");
    expect(res.status).toBe("pass");
    expect(res.timedOut).toBe(false);
    expect(res.exitCode).toBe(0);
    expect(res.stats).toEqual({ success: 50, failure: 0, timeout: 0, ignored: 0, total: 50 });
    expect(res.scan).toEqual({ bandit: { high: 0 }, size_mb: 3 });
    expect(res.detail).toContain("fuzz complete");

    // per-job dir was reclaimed (workDir is left containing nothing).
    expect(fs.readdirSync(tmpDir)).toHaveLength(0);
  });

  it("makes the rw out dir writable by the unprivileged container user before running", async () => {
    // The (root) bot creates the per-job out dir 0755/root-owned, but the
    // container runs --user 65532:65532 and bind-mounts it rw. Capture the dir's
    // mode at `docker run` time and assert "other" has the write bit, else uid
    // 65532 can't write /out/result.json. POSIX-only: Windows fs doesn't model
    // these bits, but the chmod call still runs there.
    let outMode = -1;
    execFileMock.mockImplementation(
      (_file: string, args: string[], a3?: unknown, a4?: unknown) => {
        const cb = (typeof a3 === "function" ? a3 : a4) as
          | ((err: Error | null, stdout: string, stderr: string) => void)
          | undefined;
        const child = { kill: vi.fn() } as unknown as ChildProcess;
        if (args[0] === "run") {
          const hostOut = outBindHostPath(args);
          outMode = fs.statSync(hostOut).mode & 0o777;
          fs.writeFileSync(
            path.join(hostOut, "result.json"),
            JSON.stringify({ slug: "hk", status: "pass", exit_code: 0 }),
          );
        }
        queueMicrotask(() => cb?.(null, "", ""));
        return child;
      },
    );

    const res = await runFuzzContainer(job(), options());
    expect(res.status).toBe("pass");
    expect(outMode).toBeGreaterThanOrEqual(0); // the run actually happened
    if (process.platform !== "win32") {
      expect(outMode & 0o002).toBe(0o002); // world-writable: 65532 can write /out
    }
  });

  it("carries a warn verdict through", async () => {
    mockRun(() => ({
      slug: "hk",
      status: "warn",
      stats: { success: 0, failure: 0, timeout: 0, ignored: 10, total: 10 },
      exit_code: 0,
      log_tail: "all ignored (no-op)",
    }));
    const res = await runFuzzContainer(job(), options());
    expect(res.status).toBe("warn");
    expect(res.detail).toContain("ignored");
  });

  it("forces fail when the container exit_code is non-zero (e.g. sha256 mismatch)", async () => {
    mockRun(
      () => ({ slug: "hk", status: "pass", exit_code: 3, log_tail: "sha256 mismatch on wheel" }),
      3,
    );
    const res = await runFuzzContainer(job(), options());
    expect(res.status).toBe("fail");
    expect(res.exitCode).toBe(3);
    expect(res.detail).toContain("sha256 mismatch");
    expect(fs.readdirSync(tmpDir)).toHaveLength(0);
  });

  it("fails (without throwing) when result.json is missing", async () => {
    mockRun(() => undefined); // produce nothing → no result.json written
    const res = await runFuzzContainer(job(), options());
    expect(res.status).toBe("fail");
    expect(res.detail).toContain("result.json");
  });

  it("fails (without throwing) when result.json is unparseable", async () => {
    mockRun(() => "{ not json");
    const res = await runFuzzContainer(job(), options());
    expect(res.status).toBe("fail");
    expect(res.detail).toContain("result.json");
  });

  it("surfaces docker's stderr when `docker run` itself fails (exit 125, no result.json)", async () => {
    mockRun(
      () => undefined, // container never starts → no result.json
      125,
      "docker: Error response from daemon: network mwgg-fuzz-egress not found.\nSee 'docker run --help'.",
    );
    const res = await runFuzzContainer(job(), options());
    expect(res.status).toBe("fail");
    expect(res.exitCode).toBe(125);
    expect(res.detail).toContain("network mwgg-fuzz-egress not found");
    expect(logs.some((l) => l.includes("docker exit 125"))).toBe(true);
  });

  it("fails (without throwing) when the wheel fetch/verify fails", async () => {
    mockRun(() => ({ slug: "hk", status: "pass", exit_code: 0 }));
    const res = await runFuzzContainer(
      job(),
      options({
        fetchWheel: async () => {
          throw new Error("wheel sha256 mismatch");
        },
      }),
    );
    expect(res.status).toBe("fail");
    expect(res.detail).toContain("fetch/verify wheel");
    // The container must not run if the wheel couldn't be fetched/verified.
    expect(execFileMock.mock.calls.some((c) => (c[1] as string[])[0] === "run")).toBe(false);
  });
});

describe("runFuzzContainer — wall-clock timeout", () => {
  it("force-removes the container and returns a timed-out fail", async () => {
    // Real timer, tiny wall budget: `docker run` never calls back, so only the
    // Node wall-clock timer can resolve the run. `docker rm -f` succeeds.
    let rmName: string | undefined;
    execFileMock.mockImplementation(
      (_file: string, args: string[], a3?: unknown, a4?: unknown) => {
        const cb = (typeof a3 === "function" ? a3 : a4) as
          | ((err: Error | null, stdout: string, stderr: string) => void)
          | undefined;
        const child = { kill: vi.fn() } as unknown as ChildProcess;
        if (args[0] === "rm") {
          rmName = args[args.indexOf("-f") + 1];
          queueMicrotask(() => cb?.(null, "", ""));
        }
        // `run`: intentionally never call cb.
        return child;
      },
    );

    const res = await runFuzzContainer(
      job({ slug: "hk", prNumber: 42 }),
      options({ wallSeconds: 0.05 }),
    );

    expect(res.status).toBe("fail");
    expect(res.timedOut).toBe(true);
    expect(res.detail).toContain("timed out");

    // a `docker rm -f mwgg-fuzz-42-hk-…` was issued.
    const rmCall = execFileMock.mock.calls.find((c) => (c[1] as string[])[0] === "rm");
    expect(rmCall).toBeDefined();
    expect(rmName).toMatch(/^mwgg-fuzz-42-hk-/);
  });
});

describe("runFuzzContainer — abort signal", () => {
  it("force-removes the container and returns a fail when aborted mid-run", async () => {
    const controller = new AbortController();
    let rmIssued = false;
    execFileMock.mockImplementation(
      (_file: string, args: string[], a3?: unknown, a4?: unknown) => {
        const cb = (typeof a3 === "function" ? a3 : a4) as
          | ((err: Error | null, stdout: string, stderr: string) => void)
          | undefined;
        const child = { kill: vi.fn() } as unknown as ChildProcess;
        if (args[0] === "run") {
          // abort shortly after the run starts; never call the run callback.
          queueMicrotask(() => controller.abort());
        } else if (args[0] === "rm") {
          rmIssued = true;
          queueMicrotask(() => cb?.(null, "", ""));
        }
        return child;
      },
    );

    const res = await runFuzzContainer(job(), options({ signal: controller.signal }));
    expect(res.status).toBe("fail");
    expect(res.timedOut).toBe(false);
    expect(res.detail).toContain("aborted");
    expect(rmIssued).toBe(true);
  });
});

describe("ensureImageAvailable — batch image pre-flight", () => {
  // execFile callback is the 3rd arg for `image inspect` (no opts) and the 4th
  // for `pull` (opts present); pick whichever is a function.
  function wire(handler: (args: string[]) => { err: Error | null; stderr?: string }): void {
    execFileMock.mockImplementation((_file: string, args: string[], a3?: unknown, a4?: unknown) => {
      const cb = (typeof a3 === "function" ? a3 : a4) as
        | ((err: Error | null, stdout: string, stderr: string) => void)
        | undefined;
      const { err, stderr } = handler(args);
      queueMicrotask(() => cb?.(err, "", stderr ?? ""));
      return { kill: vi.fn() } as unknown as ChildProcess;
    });
  }
  const fail = (msg: string) => Object.assign(new Error(msg), { code: 1 }) as Error;

  it("returns ok without pulling when the image is already present", async () => {
    wire((args) => (args[0] === "image" ? { err: null } : { err: fail("should not pull") }));
    const res = await ensureImageAvailable("img:tag", (m) => logs.push(m));
    expect(res.ok).toBe(true);
    expect(execFileMock.mock.calls.some((c) => (c[1] as string[])[0] === "pull")).toBe(false);
  });

  it("pulls once when absent and returns ok on a successful pull", async () => {
    wire((args) => (args[0] === "image" ? { err: fail("No such image") } : { err: null }));
    const res = await ensureImageAvailable("img:tag", (m) => logs.push(m));
    expect(res.ok).toBe(true);
    expect(execFileMock.mock.calls.some((c) => (c[1] as string[])[0] === "pull")).toBe(true);
  });

  it("reports docker's pull error when the image is absent and unpullable", async () => {
    wire((args) =>
      args[0] === "image"
        ? { err: fail("No such image") }
        : { err: fail("exit 1"), stderr: "Error response from daemon: manifest unknown" },
    );
    const res = await ensureImageAvailable("img:tag", (m) => logs.push(m));
    expect(res.ok).toBe(false);
    expect(res.detail).toContain("manifest unknown");
  });
});

describe("runFuzzContainer — docker not spawnable", () => {
  it("returns a fail result instead of throwing when execFile errors without a code", async () => {
    execFileMock.mockImplementation(
      (_file: string, _args: string[], a3?: unknown, a4?: unknown) => {
        const cb = (typeof a3 === "function" ? a3 : a4) as
          | ((err: Error | null, stdout: string, stderr: string) => void)
          | undefined;
        const child = { kill: vi.fn() } as unknown as ChildProcess;
        queueMicrotask(() => cb?.(Object.assign(new Error("spawn docker ENOENT")), "", ""));
        return child;
      },
    );

    const res = await runFuzzContainer(job(), options());
    expect(res.status).toBe("fail");
    expect(res.detail).toContain("could not start");
  });
});
