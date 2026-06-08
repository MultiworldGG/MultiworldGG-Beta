// Strict validator for the karen-fuzz repository_dispatch client_payload.
//
// The dispatch is GitHub-signed, but we validate defensively anyway: the slug
// flows into a container `--name` and the fuzzer's `-g` flag, and the wheel_url
// is fetched server-side. A malformed (or malicious-if-the-signer-is-tricked)
// payload must be rejected with errors, never executed and never thrown out of
// the handler — callers branch on { ok }.

import type {
  FuzzApworld,
  FuzzClientPayload,
  FuzzJob,
  FuzzParams,
  ScanParams,
} from "./types";

export type FuzzPayloadResult =
  | { ok: true; value: FuzzClientPayload }
  | { ok: false; errors: string[] };

const SLUG_RE = /^[a-z0-9][a-z0-9_-]{0,63}$/;
const WHEEL_URL_RE = /^https:\/\/[^\s]+\.whl(\?[^\s]*)?$/;
const SHA256_RE = /^[0-9a-f]{64}$/;
const HEAD_SHA_RE = /^[0-9a-f]{40}$/;
const INDEX_REPO_RE = /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/;
const YAMLS_RE = /^[0-9]+(-[0-9]+)?$/;

const DEFAULT_WHEEL_HOSTS = ["github.com", "objects.githubusercontent.com"];

const MIN_WORLDS = 1;
const MAX_WORLDS = 25;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

/** Comma-separated FUZZ_WHEEL_HOSTS override, falling back to the built-in allow-list. */
function allowedWheelHosts(): string[] {
  const raw = process.env.FUZZ_WHEEL_HOSTS;
  if (!raw) return DEFAULT_WHEEL_HOSTS;
  const hosts = raw
    .split(",")
    .map((h) => h.trim().toLowerCase())
    .filter((h) => h.length > 0);
  return hosts.length > 0 ? hosts : DEFAULT_WHEEL_HOSTS;
}

/**
 * Clamp a numeric field into [min, max], substituting `def` when the value is
 * missing or not a finite number. Non-numbers are treated as "use default"
 * rather than an error so a slightly-off dispatcher still produces a safe run.
 */
function clampNumber(value: unknown, min: number, max: number, def: number): number {
  if (typeof value !== "number" || !Number.isFinite(value)) return def;
  const n = Math.trunc(value);
  if (n < min) return min;
  if (n > max) return max;
  return n;
}

function validateWheelUrl(url: string, errors: string[], where: string): void {
  if (!WHEEL_URL_RE.test(url)) {
    errors.push(`${where}.wheel_url must be an https://…​.whl URL`);
    return;
  }
  let host: string;
  try {
    host = new URL(url).hostname.toLowerCase();
  } catch {
    errors.push(`${where}.wheel_url is not a parseable URL`);
    return;
  }
  if (!allowedWheelHosts().includes(host)) {
    errors.push(`${where}.wheel_url host "${host}" is not in the allow-list`);
  }
}

function validateWorld(raw: unknown, idx: number, errors: string[]): FuzzApworld | null {
  const where = `worlds[${idx}]`;
  if (!isRecord(raw)) {
    errors.push(`${where} must be an object`);
    return null;
  }

  const apworld = raw.apworld;
  const manifestPath = raw.manifest_path;
  const game = raw.game;
  const worldVersion = raw.world_version;
  const wheelUrl = raw.wheel_url;
  const sha256 = raw.sha256;

  let ok = true;
  if (typeof apworld !== "string" || !SLUG_RE.test(apworld)) {
    errors.push(`${where}.apworld must match ${SLUG_RE.source}`);
    ok = false;
  }
  if (typeof manifestPath !== "string" || manifestPath.length === 0) {
    errors.push(`${where}.manifest_path must be a non-empty string`);
    ok = false;
  }
  if (typeof game !== "string" || game.length === 0) {
    errors.push(`${where}.game must be a non-empty string`);
    ok = false;
  }
  if (typeof worldVersion !== "string" || worldVersion.length === 0) {
    errors.push(`${where}.world_version must be a non-empty string`);
    ok = false;
  }
  if (typeof wheelUrl !== "string") {
    errors.push(`${where}.wheel_url must be a string`);
    ok = false;
  } else {
    validateWheelUrl(wheelUrl, errors, where);
  }
  if (typeof sha256 !== "string" || !SHA256_RE.test(sha256)) {
    errors.push(`${where}.sha256 must be 64 lowercase hex chars`);
    ok = false;
  }

  if (!ok) return null;
  return {
    apworld: apworld as string,
    manifest_path: manifestPath as string,
    game: game as string,
    world_version: worldVersion as string,
    wheel_url: wheelUrl as string,
    sha256: sha256 as string,
  };
}

function validateFuzzParams(raw: unknown): FuzzParams {
  const obj = isRecord(raw) ? raw : {};
  const yamls = typeof obj.yamls === "string" && YAMLS_RE.test(obj.yamls) ? obj.yamls : "1-3";
  return {
    runs: clampNumber(obj.runs, 1, 500, 50),
    timeout_s: clampNumber(obj.timeout_s, 5, 300, 30),
    yamls,
    threads: clampNumber(obj.threads, 1, 16, 10),
  };
}

function validateScanParams(raw: unknown): ScanParams {
  const obj = isRecord(raw) ? raw : {};
  return { size_cap_mb: clampNumber(obj.size_cap_mb, 1, 2048, 250) };
}

/**
 * Parse an unknown repository_dispatch client_payload into a FuzzClientPayload.
 * Never throws — returns a discriminated { ok } result so the handler can log
 * the errors and skip rather than crash.
 */
export function validateFuzzPayload(action: string, clientPayload: unknown): FuzzPayloadResult {
  const errors: string[] = [];

  if (action !== "karen-fuzz") {
    errors.push(`unexpected action "${action}"; expected "karen-fuzz"`);
  }

  if (!isRecord(clientPayload)) {
    errors.push("client_payload must be an object");
    return { ok: false, errors };
  }

  const {
    schema_version: schemaVersion,
    index_repo: indexRepo,
    pr_number: prNumber,
    head_sha: headSha,
    check_run_name: checkRunName,
    comment_marker: commentMarker,
    worlds: rawWorlds,
  } = clientPayload;

  if (typeof schemaVersion !== "number" || !Number.isInteger(schemaVersion)) {
    errors.push("schema_version must be an integer");
  }
  if (typeof indexRepo !== "string" || !INDEX_REPO_RE.test(indexRepo)) {
    errors.push("index_repo must be \"owner/name\"");
  }
  if (typeof prNumber !== "number" || !Number.isInteger(prNumber) || prNumber <= 0) {
    errors.push("pr_number must be a positive integer");
  }
  if (typeof headSha !== "string" || !HEAD_SHA_RE.test(headSha)) {
    errors.push("head_sha must be 40 hex chars");
  }
  if (typeof checkRunName !== "string" || checkRunName.length === 0) {
    errors.push("check_run_name must be a non-empty string");
  }
  if (typeof commentMarker !== "string" || commentMarker.length === 0) {
    errors.push("comment_marker must be a non-empty string");
  }

  const fuzz = validateFuzzParams(clientPayload.fuzz);
  const scan = validateScanParams(clientPayload.scan);

  const worlds: FuzzApworld[] = [];
  if (!Array.isArray(rawWorlds)) {
    errors.push("worlds must be an array");
  } else {
    if (rawWorlds.length < MIN_WORLDS) {
      errors.push(`worlds must contain at least ${MIN_WORLDS} entry`);
    }
    if (rawWorlds.length > MAX_WORLDS) {
      errors.push(`worlds must contain at most ${MAX_WORLDS} entries`);
    }
    rawWorlds.forEach((w, i) => {
      const parsed = validateWorld(w, i, errors);
      if (parsed) worlds.push(parsed);
    });
  }

  if (errors.length > 0) {
    return { ok: false, errors };
  }

  return {
    ok: true,
    value: {
      schema_version: schemaVersion as number,
      index_repo: indexRepo as string,
      pr_number: prNumber as number,
      head_sha: headSha as string,
      check_run_name: checkRunName as string,
      comment_marker: commentMarker as string,
      fuzz,
      scan,
      worlds,
    },
  };
}

/** Flatten a validated payload + one of its worlds into the runner's work unit. */
export function toFuzzJob(p: FuzzClientPayload, w: FuzzApworld): FuzzJob {
  return {
    slug: w.apworld,
    wheelUrl: w.wheel_url,
    sha256: w.sha256,
    runs: p.fuzz.runs,
    timeoutS: p.fuzz.timeout_s,
    yamls: p.fuzz.yamls,
    threads: p.fuzz.threads,
    sizeCapMb: p.scan.size_cap_mb,
    prNumber: p.pr_number,
    headSha: p.head_sha,
  };
}
