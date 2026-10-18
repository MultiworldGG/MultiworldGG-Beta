// Shared types for the Karen fuzz/scan dispatch feature.

/** One world to fuzz+scan, as it arrives in the repository_dispatch client_payload. */
export interface FuzzApworld {
  apworld: string;        // slug, e.g. "hk"
  manifest_path: string;  // "worlds/hk.json"
  game: string;
  world_version: string;
  wheel_url: string;      // https://...whl (no #fragment)
  sha256: string;         // 64 lowercase hex
}

export interface FuzzParams { runs: number; timeout_s: number; yamls: string; threads: number; }
export interface ScanParams { size_cap_mb: number; }

/** The validated client_payload of a karen-fuzz repository_dispatch. */
export interface FuzzClientPayload {
  schema_version: number;
  index_repo: string;     // "owner/name"
  pr_number: number;
  head_sha: string;       // 40 hex
  check_run_name: string; // e.g. "Karen / fuzz"
  comment_marker: string; // e.g. "<!-- karen-isolated-qa -->"
  /**
   * The Index workflow's synchronous manifest verdict ("pass"|"warn"|"fail"),
   * gating Karen's final review; "" from older dispatchers = not a clean pass.
   */
  manifest_status: string;
  fuzz: FuzzParams;
  scan: ScanParams;
  worlds: FuzzApworld[];
}

export type FuzzStatus = "pass" | "warn" | "fail";

/** A normalized, per-world unit of work the runner executes. */
export interface FuzzJob {
  slug: string;
  wheelUrl: string;
  sha256: string;
  runs: number;
  timeoutS: number;
  yamls: string;
  threads: number;
  sizeCapMb: number;
  prNumber: number;
  headSha: string;
}

/** Result of fuzzing+scanning one world (what runFuzzContainer resolves to). */
export interface FuzzWorldResult {
  slug: string;
  status: FuzzStatus;
  detail: string;                       // human summary line for the comment table
  stats?: Record<string, number>;       // success/failure/timeout/ignored/total
  scan?: Record<string, unknown>;       // bandit/pip-audit/ruff/size/rom/import findings
  fuzzerDetails?: string[];             // per-error summary ("ErrorKey (N)") for the fuzzer Findings block
  exitCode: number;
  timedOut: boolean;
}
