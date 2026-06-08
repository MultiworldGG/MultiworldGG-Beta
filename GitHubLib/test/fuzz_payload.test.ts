import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { validateFuzzPayload, toFuzzJob } from "../src/fuzz/payload";
import type { FuzzApworld, FuzzClientPayload } from "../src/fuzz/types";

const VALID_WHEEL =
  "https://github.com/alice/hk/releases/download/hk-1.0.0/hk-1.0.0-py3-none-any.whl";
const VALID_SHA256 = "a".repeat(64);
const VALID_HEAD_SHA = "b".repeat(40);

function world(overrides: Partial<FuzzApworld> = {}): Record<string, unknown> {
  return {
    apworld: "hk",
    manifest_path: "worlds/hk.json",
    game: "Hollow Knight",
    world_version: "1.0.0",
    wheel_url: VALID_WHEEL,
    sha256: VALID_SHA256,
    ...overrides,
  };
}

function payload(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    schema_version: 1,
    index_repo: "MultiworldGG/MultiworldGG-Index",
    pr_number: 42,
    head_sha: VALID_HEAD_SHA,
    check_run_name: "Karen's Isolated QA Checks",
    comment_marker: "<!-- karen-pr-review -->",
    fuzz: { runs: 50, timeout_s: 30, yamls: "1-10", threads: 10 },
    scan: { size_cap_mb: 250 },
    worlds: [world()],
    ...overrides,
  };
}

beforeEach(() => {
  delete process.env.FUZZ_WHEEL_HOSTS;
});

afterEach(() => {
  delete process.env.FUZZ_WHEEL_HOSTS;
});

describe("validateFuzzPayload — happy path", () => {
  it("accepts a well-formed karen-fuzz payload", () => {
    const res = validateFuzzPayload("karen-fuzz", payload());
    expect(res.ok).toBe(true);
    if (!res.ok) return; // narrows for TS
    expect(res.value.worlds).toHaveLength(1);
    expect(res.value.worlds[0].apworld).toBe("hk");
    expect(res.value.fuzz.runs).toBe(50);
    expect(res.value.scan.size_cap_mb).toBe(250);
  });

  it("rejects a non-karen-fuzz action", () => {
    const res = validateFuzzPayload("something-else", payload());
    expect(res.ok).toBe(false);
    if (res.ok) return;
    expect(res.errors.some((e) => e.includes("action"))).toBe(true);
  });
});

describe("validateFuzzPayload — field validation failures", () => {
  it("rejects a slug with path-traversal / arg-injection characters", () => {
    const res = validateFuzzPayload("karen-fuzz", payload({ worlds: [world({ apworld: "../etc" })] }));
    expect(res.ok).toBe(false);
    if (res.ok) return;
    expect(res.errors.some((e) => e.includes("apworld"))).toBe(true);
  });

  it("rejects a slug starting with a dash (would look like a flag)", () => {
    const res = validateFuzzPayload("karen-fuzz", payload({ worlds: [world({ apworld: "-rf" })] }));
    expect(res.ok).toBe(false);
  });

  it("rejects a non-https wheel_url", () => {
    const res = validateFuzzPayload(
      "karen-fuzz",
      payload({ worlds: [world({ wheel_url: "http://github.com/x/y.whl" })] }),
    );
    expect(res.ok).toBe(false);
    if (res.ok) return;
    expect(res.errors.some((e) => e.includes("wheel_url"))).toBe(true);
  });

  it("rejects a wheel_url whose host is not in the allow-list (anti-SSRF)", () => {
    const res = validateFuzzPayload(
      "karen-fuzz",
      payload({ worlds: [world({ wheel_url: "https://evil.example.com/x.whl" })] }),
    );
    expect(res.ok).toBe(false);
    if (res.ok) return;
    expect(res.errors.some((e) => e.includes("allow-list"))).toBe(true);
  });

  it("honors FUZZ_WHEEL_HOSTS to extend the allow-list", () => {
    process.env.FUZZ_WHEEL_HOSTS = "github.com, files.internal.example";
    const res = validateFuzzPayload(
      "karen-fuzz",
      payload({ worlds: [world({ wheel_url: "https://files.internal.example/x.whl" })] }),
    );
    expect(res.ok).toBe(true);
  });

  it("rejects a non-default host once FUZZ_WHEEL_HOSTS narrows the list", () => {
    process.env.FUZZ_WHEEL_HOSTS = "files.internal.example";
    const res = validateFuzzPayload("karen-fuzz", payload());
    expect(res.ok).toBe(false);
  });

  it("rejects a bad sha256 (wrong length / uppercase)", () => {
    const tooShort = validateFuzzPayload("karen-fuzz", payload({ worlds: [world({ sha256: "abc" })] }));
    expect(tooShort.ok).toBe(false);
    const upper = validateFuzzPayload(
      "karen-fuzz",
      payload({ worlds: [world({ sha256: "A".repeat(64) })] }),
    );
    expect(upper.ok).toBe(false);
  });

  it("rejects a bad head_sha", () => {
    const res = validateFuzzPayload("karen-fuzz", payload({ head_sha: "xyz" }));
    expect(res.ok).toBe(false);
    if (res.ok) return;
    expect(res.errors.some((e) => e.includes("head_sha"))).toBe(true);
  });

  it("rejects a malformed index_repo", () => {
    const res = validateFuzzPayload("karen-fuzz", payload({ index_repo: "not-a-repo" }));
    expect(res.ok).toBe(false);
    if (res.ok) return;
    expect(res.errors.some((e) => e.includes("index_repo"))).toBe(true);
  });

  it("rejects a non-object client_payload without throwing", () => {
    expect(validateFuzzPayload("karen-fuzz", null).ok).toBe(false);
    expect(validateFuzzPayload("karen-fuzz", "nope").ok).toBe(false);
    expect(validateFuzzPayload("karen-fuzz", 123).ok).toBe(false);
  });
});

describe("validateFuzzPayload — worlds array bounds", () => {
  it("rejects an empty worlds array", () => {
    const res = validateFuzzPayload("karen-fuzz", payload({ worlds: [] }));
    expect(res.ok).toBe(false);
    if (res.ok) return;
    expect(res.errors.some((e) => e.includes("at least"))).toBe(true);
  });

  it("rejects an oversized worlds array (> 25)", () => {
    const many = Array.from({ length: 26 }, () => world());
    const res = validateFuzzPayload("karen-fuzz", payload({ worlds: many }));
    expect(res.ok).toBe(false);
    if (res.ok) return;
    expect(res.errors.some((e) => e.includes("at most"))).toBe(true);
  });

  it("rejects when worlds is not an array", () => {
    const res = validateFuzzPayload("karen-fuzz", payload({ worlds: "hk" }));
    expect(res.ok).toBe(false);
  });
});

describe("validateFuzzPayload — numeric clamps and defaults", () => {
  it("fills in defaults when fuzz/scan params are missing", () => {
    const res = validateFuzzPayload("karen-fuzz", payload({ fuzz: {}, scan: {} }));
    expect(res.ok).toBe(true);
    if (!res.ok) return;
    expect(res.value.fuzz).toEqual({ runs: 50, timeout_s: 30, yamls: "1-3", threads: 10 });
    expect(res.value.scan).toEqual({ size_cap_mb: 250 });
  });

  it("clamps out-of-range numerics into their bounds", () => {
    const res = validateFuzzPayload(
      "karen-fuzz",
      payload({
        fuzz: { runs: 99999, timeout_s: 1, yamls: "3", threads: 999 },
        scan: { size_cap_mb: 999999 },
      }),
    );
    expect(res.ok).toBe(true);
    if (!res.ok) return;
    expect(res.value.fuzz.runs).toBe(500); // max
    expect(res.value.fuzz.timeout_s).toBe(5); // min
    expect(res.value.fuzz.threads).toBe(16); // max
    expect(res.value.fuzz.yamls).toBe("3");
    expect(res.value.scan.size_cap_mb).toBe(2048); // max
  });

  it("falls back to default yamls on a malformed range", () => {
    const res = validateFuzzPayload("karen-fuzz", payload({ fuzz: { yamls: "1-2-3" } }));
    expect(res.ok).toBe(true);
    if (!res.ok) return;
    expect(res.value.fuzz.yamls).toBe("1-3");
  });
});

describe("toFuzzJob", () => {
  it("flattens a payload + world into a runner work unit", () => {
    const res = validateFuzzPayload("karen-fuzz", payload());
    expect(res.ok).toBe(true);
    if (!res.ok) return;
    const value: FuzzClientPayload = res.value;
    const job = toFuzzJob(value, value.worlds[0]);
    expect(job).toEqual({
      slug: "hk",
      wheelUrl: VALID_WHEEL,
      sha256: VALID_SHA256,
      runs: 50,
      timeoutS: 30,
      yamls: "1-10",
      threads: 10,
      sizeCapMb: 250,
      prNumber: 42,
      headSha: VALID_HEAD_SHA,
    });
  });
});
