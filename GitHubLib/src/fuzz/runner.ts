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
import { createReadStream, createWriteStream } from "fs";
import * as https from "https";
import * as crypto from "crypto";
import * as path from "path";

import type { FuzzJob, FuzzStatus, FuzzWorldResult } from "./types";

export interface RunFuzzOptions {
  image: string;
  /** Host path that equals the in-container path; the FUZZ_WORK_DIR bind root. */
  workDir: string;
  cpus?: string;
  memory?: string;
  pids?: number;
  wallSeconds?: number;
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
  /**
   * Download + sha256-verify the wheel to `dest` before the container runs. The
   * container is `--network none`, so the TRUSTED bot fetches the bytes and
   * bind-mounts them in at /in. Injectable for tests; defaults to an https fetch.
   */
  fetchWheel?: (url: string, sha256: string, dest: string) => Promise<void>;
  log: (m: string) => void;
  signal?: AbortSignal;
  /**
   * Opt-in debug. When set, the container persists its full combined.log + the
   * fuzzer's per-generation worker dumps (fuzz_output/) into /out, and we KEEP
   * the per-job dir instead of deleting it — so a failing run leaves diagnostics
   * under <workDir>/<id>/ for inspection. Off by default; artifacts accumulate.
   */
  debug?: boolean;
}

const DEFAULT_WALL_SECONDS = 1200;
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

/**
 * The wheel's own filename, taken straight from the URL. `uv pip install` parses
 * the wheel FILENAME, so the staged file must keep its real PEP 427 name — a
 * fixed "world.whl" is what made every install fail ("Must have a version"). No
 * reconstruction: validateFuzzPayload already guaranteed the URL is https, ends
 * in ".whl", and is host-allow-listed, and a real release asset is named
 * correctly by `build`. `.pathname` drops any "?query" and `path.basename` drops
 * every directory component, so the result is a bare ".whl" filename that can't
 * traverse out of the bind dir.
 */
export function wheelFileName(job: FuzzJob): string {
  return path.posix.basename(new URL(job.wheelUrl).pathname);
}

/** Build the hardened `docker run` argv. Pure (no I/O) so it is trivially testable. */
export function buildDockerArgs(
  job: FuzzJob,
  opts: RunFuzzOptions,
  name: string,
  hostOutDir: string,
  hostInDir: string,
): string[] {
  const cpus = opts.cpus ?? DEFAULT_CPUS;
  const memory = opts.memory ?? DEFAULT_MEMORY;
  const pids = opts.pids ?? DEFAULT_PIDS;

  // No FUZZ_WHEEL_URL / MWGG_CORE_* / FUZZER_*: the container is offline. The
  // wheel arrives as a bind mount (/in); core, its venv, and fuzz.py are baked
  // into the image at build time. FUZZ_WHEEL_SHA256 stays for an in-container
  // re-verify of the mounted bytes (defense in depth; the bot already verified).
  const env: Record<string, string> = {
    FUZZ_SLUG: job.slug,
    FUZZ_WHEEL_SHA256: job.sha256,
    FUZZ_RUNS: String(job.runs),
    FUZZ_TIMEOUT: String(job.timeoutS),
    FUZZ_YAMLS: job.yamls,
    FUZZ_THREADS: String(job.threads),
    FUZZ_SIZE_CAP_MB: String(job.sizeCapMb),
    KIVY_NO_ARGS: "1",
    SKIP_ALL_INSTALLS: "1",
    MALLOC_ARENA_MAX: "2",
  };

  // Opt-in: tell the container to persist its full log + worker dumps to /out.
  if (opts.debug) env.FUZZ_DEBUG = "1";

  const args: string[] = [
    "run",
    "--rm",
    "--name",
    name,
    "--user",
    "65532:65532",
    "--read-only",
    // mode=1777 is REQUIRED: with explicit tmpfs options Docker does NOT inject
    // its default mode, so the kernel mounts the tmpfs root 0755 owned by root —
    // and the container runs as --user 65532, which then can't create /work/.cache
    // etc. 1777 (sticky, world-writable, like /tmp) lets the unprivileged user write.
    "--tmpfs",
    "/tmp:rw,noexec,nosuid,size=512m,mode=1777",
    // exec is REQUIRED: the trusted venv lives on /work and Python C extensions
    // there are dlopen'd (mmap PROT_EXEC). Docker's --tmpfs default is noexec, and
    // omitting it from explicit options doesn't reliably disable it (same default-
    // injection class as the mode=1777 fix), so set exec explicitly — else native
    // deps (bsdiff4, Pillow, …) fail to load with "failed to map segment".
    "--tmpfs",
    "/work:rw,exec,nosuid,size=4g,mode=1777",
    "-v",
    `${hostOutDir}:/out:rw`,
    "-v",
    `${hostInDir}:/in:ro`,
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
    // Untrusted world code gets ZERO network. Everything it needs is baked into
    // the image or bind-mounted by the trusted bot, so there's nothing to reach.
    "--network",
    "none",
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
 * daemon: invalid mount config" / "Unable to find image". Truncated for the log.
 */
function firstStderrLine(stderr: string | undefined): string {
  if (!stderr) return "";
  const line = stderr.split("\n").map((l) => l.trim()).find((l) => l.length > 0) ?? "";
  return line.length > 300 ? line.slice(0, 297) + "..." : line;
}

/**
 * Batch pre-flight: confirm FUZZ_IMAGE is usable before spawning N containers.
 * `docker image inspect` first; if it's not local, try ONE `docker pull` — so a
 * public image is fetched once (instead of N racing auto-pulls) and a missing or
 * private one fails ONCE with docker's real reason instead of N cryptic exit-125s
 * with no result.json. Resolves `{ ok }`; never throws.
 */
export function ensureImageAvailable(
  image: string,
  log: (m: string) => void,
): Promise<{ ok: boolean; detail?: string }> {
  return new Promise((resolve) => {
    execFile("docker", ["image", "inspect", image], (inspectErr) => {
      if (!inspectErr) {
        resolve({ ok: true });
        return;
      }
      log(`fuzz: image ${image} not present locally; pulling once…`);
      execFile(
        "docker",
        ["pull", image],
        { maxBuffer: 16 * 1024 * 1024 },
        (pullErr, _stdout, stderr) => {
          if (!pullErr) {
            log(`fuzz: pulled ${image}`);
            resolve({ ok: true });
            return;
          }
          const detail =
            firstStderrLine(stderr) ||
            (pullErr instanceof Error ? pullErr.message : String(pullErr));
          resolve({ ok: false, detail });
        },
      );
    });
  });
}

/**
 * Default wheel fetch: stream the URL to `dest` (following redirects — GitHub
 * release assets 302 to objects.githubusercontent.com), then sha256-verify the
 * written file. Rejects on HTTP error, redirect loop, or digest mismatch, so the
 * bot never bind-mounts unverified bytes into the sandbox.
 */
function defaultFetchWheel(url: string, expectedSha: string, dest: string): Promise<void> {
  const expected = expectedSha.toLowerCase();
  return new Promise((resolve, reject) => {
    let redirects = 0;
    const get = (u: string): void => {
      https
        .get(u, { headers: { "user-agent": "oliver-fuzz" } }, (res) => {
          const status = res.statusCode ?? 0;
          if (status >= 300 && status < 400 && res.headers.location) {
            res.resume();
            if (++redirects > 5) {
              reject(new Error("too many redirects fetching wheel"));
              return;
            }
            get(new URL(res.headers.location, u).toString());
            return;
          }
          if (status !== 200) {
            res.resume();
            reject(new Error(`wheel fetch returned HTTP ${status}`));
            return;
          }
          const out = createWriteStream(dest);
          out.on("error", reject);
          res.on("error", reject);
          res.pipe(out);
          out.on("finish", () => {
            const hash = crypto.createHash("sha256");
            const rs = createReadStream(dest);
            rs.on("data", (c) => hash.update(c));
            rs.on("error", reject);
            rs.on("end", () => {
              const actual = hash.digest("hex");
              if (actual !== expected) {
                reject(new Error(`wheel sha256 mismatch: expected ${expected}, got ${actual}`));
              } else {
                resolve();
              }
            });
          });
        })
        .on("error", reject);
    };
    get(url);
  });
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
  const hostInDir = path.join(jobDir, "in");

  // Dir creation failing is a genuine internal error — let it reject.
  await fs.mkdir(hostOutDir, { recursive: true });
  await fs.mkdir(hostInDir, { recursive: true });
  // The bot runs as root, so it just made these per-job dirs 0755/root-owned. But
  // the container runs `--user 65532:65532` and gets <out> bind-mounted rw; a 0755
  // dir is read-only to "other", so the unprivileged user can't create
  // /out/result.json — and EVERY outcome then degrades to the caller's "no readable
  // result.json", masking the container's real exit code. Make the rw out dir
  // world-writable so uid 65532 can write its result. (Same root cause as the
  // tmpfs mode=1777 mounts, but here the perms come from the host dir, not a tmpfs
  // flag; chmod, not mkdir's mode, because the latter is masked by umask. /in is
  // mounted :ro — the container only reads the wheel — so its 0755 is fine.)
  await fs.chmod(hostOutDir, 0o777);

  try {
    // The container is offline, so the (trusted) bot fetches + verifies the wheel
    // and bind-mounts it at /in. A fetch/verify failure is this world's failure,
    // not a crash.
    const fetchWheel = opts.fetchWheel ?? defaultFetchWheel;
    try {
      await fetchWheel(job.wheelUrl, job.sha256, path.join(hostInDir, wheelFileName(job)));
    } catch (err) {
      const why = err instanceof Error ? err.message : String(err);
      opts.log(`fuzz ${job.slug}: wheel fetch/verify failed: ${why}`);
      return {
        slug: job.slug,
        status: "fail",
        detail: `${job.slug}: could not fetch/verify wheel — ${why}`,
        exitCode: 1,
        timedOut: false,
      };
    }

    const args = buildDockerArgs(job, opts, name, hostOutDir, hostInDir);
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
    if (opts.debug) {
      // FUZZ_DEBUG: keep the per-job dir so the operator can read the diagnostics
      // the container persisted — <id>/out/{result.json,report.json,combined.log,
      // fuzz_output/}. These accumulate; turn FUZZ_DEBUG off and clean workDir when done.
      opts.log(`fuzz ${job.slug}: FUZZ_DEBUG on — kept artifacts at ${hostOutDir}`);
    } else {
      // Reclaim the per-job host dir regardless of outcome; never mask a real error.
      await fs.rm(jobDir, { recursive: true, force: true }).catch((err: unknown) => {
        const why = err instanceof Error ? err.message : String(err);
        opts.log(`fuzz ${job.slug}: failed to remove ${jobDir} (best effort): ${why}`);
      });
    }
  }
}
