// Container runner for the Karen fuzz/scan feature.
//
// Given one normalized FuzzJob, build a HARDENED `docker run` argv and execute
// it with execFile (array args, NO shell — the slug/urls/shas already passed the
// payload validator, but we still never interpolate them into a command string).
// The container fetches+verifies the wheel, fuzzes the world, scans it, and writes
// /out/result.json; we read that back, map it to FuzzWorldResult, and clean up.
//
// Contract with the image: every job-specific input is passed as an environment
// variable; the only host mount is <workDir>/<unique>/out → /out (rw). The bot
// talks to a docker-socket-proxy, so DOCKER_HOST is honored from the environment
// and we never pass -H.
//
// This function NEVER throws for an expected container failure (non-zero exit,
// missing/garbage result.json, sha256 mismatch, timeout, abort) — those resolve
// to a status:"fail" FuzzWorldResult. It only rejects on truly unexpected internal
// errors (e.g. the out dir cannot be created).

import { execFile } from "child_process";
import * as fs from "fs/promises";
import * as path from "path";

import type { FuzzJob, FuzzStatus, FuzzWorldResult } from "./types";

export interface RunFuzzOptions {
  image: string;
  /** Host path that equals the in-container path; the FUZZ_WORK_DIR bind root. */
  workDir: string;
  net?: string;
  cpus?: string;
  memory?: string;
  pids?: number;
  wallSeconds?: number;
  mwggCoreRepo: string;
  mwggCoreRef: string;
  fuzzerRepo: string;
  fuzzerRef: string;
  /**
   * Optional HOST path to a base-ROM directory, bind-mounted READ-ONLY at /roms
   * so ROM-dependent worlds can actually generate. Resolved by the host daemon,
   * so it must be a real host path; the bot never reads it. Unset → no mount and
   * ROM worlds report a no-op (the legacy CI behavior).
   */
  romDir?: string;
  /**
   * Optional HOST path to a host.yaml, bind-mounted READ-ONLY; the in-container
   * run script installs it where get_settings() looks. Its <world>_options
   * .rom_file entries should point at /roms/<file>.
   */
  hostYaml?: string;
  log: (m: string) => void;
  signal?: AbortSignal;
}

const DEFAULT_WALL_SECONDS = 1200;
const DEFAULT_NET = "bridge";
const DEFAULT_CPUS = "2";
const DEFAULT_MEMORY = "4g";
const DEFAULT_PIDS = 512;

/** A valid container/dir token: lowercase alnum and dashes, never leading/trailing dash. */
function sanitizeToken(raw: string): string {
  const cleaned = raw
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return cleaned.length > 0 ? cleaned : "x";
}

/**
 * Deterministic per-job suffix. Derived purely from job fields + process.pid —
 * NO wall-clock and NO randomness (the surrounding harness forbids both, and a
 * deterministic name lets `docker rm -f` target the exact container on timeout).
 * Two concurrent jobs differ by slug/pr; the same job retried in a fresh process
 * differs by pid.
 */
function jobSuffix(job: FuzzJob): string {
  const headPrefix = job.headSha.slice(0, 12);
  return sanitizeToken(`${job.prNumber}-${job.slug}-${headPrefix}-${process.pid}`);
}

function containerName(suffix: string): string {
  // suffix already encodes pr-slug-sha-pid; don't repeat pr-slug in the name.
  return sanitizeToken(`mwgg-fuzz-${suffix}`);
}

/** Build the hardened `docker run` argv. Pure (no I/O) so it is trivially testable. */
export function buildDockerArgs(
  job: FuzzJob,
  opts: RunFuzzOptions,
  name: string,
  hostOutDir: string,
): string[] {
  const net = opts.net ?? DEFAULT_NET;
  const cpus = opts.cpus ?? DEFAULT_CPUS;
  const memory = opts.memory ?? DEFAULT_MEMORY;
  const pids = opts.pids ?? DEFAULT_PIDS;

  const env: Record<string, string> = {
    FUZZ_SLUG: job.slug,
    FUZZ_WHEEL_URL: job.wheelUrl,
    FUZZ_WHEEL_SHA256: job.sha256,
    FUZZ_RUNS: String(job.runs),
    FUZZ_TIMEOUT: String(job.timeoutS),
    FUZZ_YAMLS: job.yamls,
    FUZZ_THREADS: String(job.threads),
    FUZZ_SIZE_CAP_MB: String(job.sizeCapMb),
    MWGG_CORE_REPO: opts.mwggCoreRepo,
    MWGG_CORE_REF: opts.mwggCoreRef,
    FUZZER_REPO: opts.fuzzerRepo,
    FUZZER_REF: opts.fuzzerRef,
    KIVY_NO_ARGS: "1",
    SKIP_ALL_INSTALLS: "1",
    MALLOC_ARENA_MAX: "2",
  };

  const args: string[] = [
    "run",
    "--rm",
    "--name",
    name,
    "--user",
    "65532:65532",
    "--read-only",
    "--tmpfs",
    "/tmp:rw,noexec,nosuid,size=512m",
    "--tmpfs",
    "/work:rw,nosuid,size=4g",
    "-v",
    `${hostOutDir}:/out:rw`,
    "--cap-drop",
    "ALL",
    "--security-opt",
    "no-new-privileges",
    "--pids-limit",
    String(pids),
    "--cpus",
    cpus,
    "--memory",
    memory,
    "--memory-swap",
    memory,
    "--ulimit",
    "nofile=4096:4096",
    "--network",
    net,
  ];

  // Optional READ-ONLY mounts for ROM-dependent worlds. Both resolve on the host
  // daemon (the `:ro` keeps untrusted world code from modifying them). The host
  // .yaml lands on /opt/fuzz/host.yaml; the run script copies it to where
  // get_settings() looks and its rom_file paths reference /roms/<file>.
  if (opts.romDir) {
    args.push("-v", `${opts.romDir}:/roms:ro`);
  }
  if (opts.hostYaml) {
    args.push("-v", `${opts.hostYaml}:/opt/fuzz/host.yaml:ro`);
  }

  for (const [key, value] of Object.entries(env)) {
    args.push("-e", `${key}=${value}`);
  }

  args.push(opts.image);
  return args;
}

/** Map the raw FuzzStatus from result.json onto our union, defaulting to "fail". */
function coerceStatus(raw: unknown): FuzzStatus {
  return raw === "pass" || raw === "warn" || raw === "fail" ? raw : "fail";
}

function coerceStats(raw: unknown): Record<string, number> | undefined {
  if (typeof raw !== "object" || raw === null) return undefined;
  const out: Record<string, number> = {};
  for (const [key, value] of Object.entries(raw as Record<string, unknown>)) {
    if (typeof value === "number" && Number.isFinite(value)) out[key] = value;
  }
  return out;
}

function coerceScan(raw: unknown): Record<string, unknown> | undefined {
  if (typeof raw !== "object" || raw === null || Array.isArray(raw)) return undefined;
  return raw as Record<string, unknown>;
}

/** A short, single-line excerpt of the container's tail log for the comment detail. */
function summarizeTail(logTail: unknown): string {
  if (typeof logTail !== "string" || logTail.length === 0) return "";
  const lastLine = logTail
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l.length > 0)
    .pop();
  return lastLine ?? "";
}

/**
 * First non-empty line of docker's own stderr — the actionable bit when
 * `docker run` itself fails (exit 125): e.g. "docker: Error response from
 * daemon: network mwgg-fuzz-egress not found." Truncated for the comment/log.
 */
function firstStderrLine(stderr: string | undefined): string {
  if (!stderr) return "";
  const line = stderr.split("\n").map((l) => l.trim()).find((l) => l.length > 0) ?? "";
  return line.length > 300 ? line.slice(0, 297) + "..." : line;
}

interface ContainerResult {
  status: FuzzStatus;
  stats?: Record<string, number>;
  scan?: Record<string, unknown>;
  exitCode: number;
  detail: string;
}

/**
 * Read and map <hostOutDir>/result.json. A missing/garbage file, or an exit_code
 * that signals a sha256 mismatch / internal container failure, yields status:"fail"
 * with an explanatory detail rather than throwing.
 */
async function readContainerResult(
  job: FuzzJob,
  hostOutDir: string,
  dockerExitCode: number,
  dockerStderr?: string,
): Promise<ContainerResult> {
  const resultPath = path.join(hostOutDir, "result.json");

  let parsed: Record<string, unknown>;
  try {
    const raw = await fs.readFile(resultPath, "utf-8");
    const json: unknown = JSON.parse(raw);
    if (typeof json !== "object" || json === null || Array.isArray(json)) {
      throw new Error("result.json is not an object");
    }
    parsed = json as Record<string, unknown>;
  } catch (err) {
    const why = err instanceof Error ? err.message : String(err);
    // No result.json + a non-zero docker exit usually means `docker run` itself
    // failed (missing network/image, bad mount) — surface docker's own stderr so
    // the operator sees the real reason instead of a bare exit code.
    const hint = dockerExitCode !== 0 ? firstStderrLine(dockerStderr) : "";
    return {
      status: "fail",
      exitCode: dockerExitCode,
      detail:
        `${job.slug}: no readable result.json (${why}); container exit ${dockerExitCode}` +
        (hint ? ` — ${hint}` : ""),
    };
  }

  const exitCode =
    typeof parsed.exit_code === "number" && Number.isFinite(parsed.exit_code)
      ? Math.trunc(parsed.exit_code)
      : dockerExitCode;
  const status = coerceStatus(parsed.status);
  const stats = coerceStats(parsed.stats);
  const scan = coerceScan(parsed.scan);
  const tail = summarizeTail(parsed.log_tail);

  // A non-zero in-container exit means the wheel sha256 check (or another guard)
  // failed before the verdict was meaningful — force fail regardless of `status`.
  if (exitCode !== 0) {
    const reason = tail.length > 0 ? tail : "wheel verification or setup failed";
    return {
      status: "fail",
      stats,
      scan,
      exitCode,
      detail: `${job.slug}: container failed (exit ${exitCode}): ${reason}`,
    };
  }

  const detail =
    tail.length > 0 ? `${job.slug}: ${status} — ${tail}` : `${job.slug}: ${status}`;
  return { status, stats, scan, exitCode, detail };
}

/** Best-effort forced removal of a container by name; never rejects. */
function dockerRemove(name: string, log: (m: string) => void): Promise<void> {
  return new Promise((resolve) => {
    execFile("docker", ["rm", "-f", name], (err) => {
      if (err) log(`docker rm -f ${name} failed (best effort): ${err.message}`);
      resolve();
    });
  });
}

interface DockerRunOutcome {
  kind: "exited" | "timeout" | "aborted";
  exitCode: number;
  /** docker's own stderr on an `exited` outcome (the reason for a 125, etc.). */
  stderr?: string;
}

/**
 * Run `docker run …` to completion, racing it against the Node-side wall clock
 * and opts.signal. On timeout/abort we force-remove the container so it cannot
 * outlive the bot. Resolves with the outcome; rejects only on a spawn-level error
 * (docker missing, etc.).
 */
function runDocker(
  args: string[],
  name: string,
  wallSeconds: number,
  opts: RunFuzzOptions,
): Promise<DockerRunOutcome> {
  return new Promise((resolve, reject) => {
    let settled = false;
    const finish = (outcome: DockerRunOutcome): void => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      if (opts.signal) opts.signal.removeEventListener("abort", onAbort);
      resolve(outcome);
    };

    const child = execFile(
      "docker",
      args,
      { maxBuffer: 16 * 1024 * 1024 },
      (err, _stdout, stderr) => {
        if (settled) return; // already torn down by timeout/abort
        // execFile reports non-zero exits as an error carrying `.code`. A numeric
        // code is an ordinary container failure, not a spawn error.
        const code = (err as { code?: unknown } | null)?.code;
        if (err && typeof code !== "number") {
          settled = true;
          clearTimeout(timer);
          if (opts.signal) opts.signal.removeEventListener("abort", onAbort);
          reject(err);
          return;
        }
        finish({
          kind: "exited",
          exitCode: typeof code === "number" ? code : 0,
          stderr: typeof stderr === "string" ? stderr : undefined,
        });
      },
    );

    const tearDown = (kind: "timeout" | "aborted"): void => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      if (opts.signal) opts.signal.removeEventListener("abort", onAbort);
      child.kill("SIGKILL");
      void dockerRemove(name, opts.log).then(() => resolve({ kind, exitCode: 124 }));
    };

    const onAbort = (): void => {
      opts.log(`fuzz ${name}: aborted; removing container`);
      tearDown("aborted");
    };

    const timer = setTimeout(() => {
      opts.log(`fuzz ${name}: wall-clock timeout after ${wallSeconds}s; removing container`);
      tearDown("timeout");
    }, wallSeconds * 1000);

    if (opts.signal) {
      if (opts.signal.aborted) {
        onAbort();
      } else {
        opts.signal.addEventListener("abort", onAbort, { once: true });
      }
    }
  });
}

/**
 * Fuzz + scan one world in a hardened container. Resolves a FuzzWorldResult for
 * every outcome the harness expects (pass/warn/fail, timeout, abort); rejects only
 * on unexpected internal errors (out-dir creation, docker not spawnable).
 */
export async function runFuzzContainer(
  job: FuzzJob,
  opts: RunFuzzOptions,
): Promise<FuzzWorldResult> {
  const wallSeconds = opts.wallSeconds ?? DEFAULT_WALL_SECONDS;
  const suffix = jobSuffix(job);
  const name = containerName(suffix);
  const jobDir = path.join(opts.workDir, suffix);
  const hostOutDir = path.join(jobDir, "out");

  // Out-dir creation failing is a genuine internal error — let it reject.
  await fs.mkdir(hostOutDir, { recursive: true });

  try {
    const args = buildDockerArgs(job, opts, name, hostOutDir);
    opts.log(`fuzz ${job.slug}: docker run (${name}, wall ${wallSeconds}s)`);

    let outcome: DockerRunOutcome;
    try {
      outcome = await runDocker(args, name, wallSeconds, opts);
    } catch (err) {
      // Spawn-level failure (e.g. docker binary missing): surface as a fail result
      // rather than throwing — a single unrunnable world must not crash the batch.
      const why = err instanceof Error ? err.message : String(err);
      opts.log(`fuzz ${job.slug}: docker run could not start: ${why}`);
      return {
        slug: job.slug,
        status: "fail",
        detail: `${job.slug}: could not start container: ${why}`,
        exitCode: 1,
        timedOut: false,
      };
    }

    if (outcome.kind !== "exited") {
      const what = outcome.kind === "timeout" ? `timed out after ${wallSeconds}s` : "was aborted";
      return {
        slug: job.slug,
        status: "fail",
        detail: `${job.slug}: container ${what} and was force-removed`,
        exitCode: outcome.exitCode,
        timedOut: outcome.kind === "timeout",
      };
    }

    if (outcome.exitCode !== 0 && outcome.stderr) {
      opts.log(`fuzz ${job.slug}: docker exit ${outcome.exitCode}: ${firstStderrLine(outcome.stderr)}`);
    }
    const result = await readContainerResult(job, hostOutDir, outcome.exitCode, outcome.stderr);
    return {
      slug: job.slug,
      status: result.status,
      detail: result.detail,
      stats: result.stats,
      scan: result.scan,
      exitCode: result.exitCode,
      timedOut: false,
    };
  } finally {
    // Reclaim the per-job host dir regardless of outcome; never mask a real error.
    await fs.rm(jobDir, { recursive: true, force: true }).catch((err: unknown) => {
      const why = err instanceof Error ? err.message : String(err);
      opts.log(`fuzz ${job.slug}: failed to remove ${jobDir} (best effort): ${why}`);
    });
  }
}
