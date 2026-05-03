import { describe, it, expect, beforeEach, afterEach } from "vitest";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import { EventLog } from "../src/event-log";

const fakeLogger = {
  trace: () => {},
  debug: () => {},
  info: () => {},
  warn: () => {},
  error: () => {},
  fatal: () => {},
  child: () => fakeLogger,
} as any;

let tmpDir: string;

beforeEach(() => {
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "oliver-event-log-"));
  process.env.OLIVER_LOG_DIR = tmpDir;
});

afterEach(() => {
  fs.rmSync(tmpDir, { recursive: true, force: true });
  delete process.env.OLIVER_LOG_DIR;
});

describe("EventLog", () => {
  it("appends events to events.jsonl with ts + structured fields", () => {
    const log = new EventLog(fakeLogger);
    log.emit({
      kind: "ok",
      source_repo: "lallaria/clique",
      release_tag: "v1.0.0",
      slug: "clique",
      message: "Opened Index PR #42",
    });
    const raw = fs.readFileSync(path.join(tmpDir, "events.jsonl"), "utf-8");
    const ev = JSON.parse(raw.trim());
    expect(ev.kind).toBe("ok");
    expect(ev.slug).toBe("clique");
    expect(ev.ts).toMatch(/^\d{4}-\d{2}-\d{2}T/);
  });

  it("read returns most recent first, with optional kind filter", () => {
    const log = new EventLog(fakeLogger);
    log.emit({ kind: "ok", source_repo: "a/b", message: "first" });
    log.emit({ kind: "skip", source_repo: "a/b", reason: "workflow_failure", message: "second" });
    log.emit({ kind: "error", source_repo: "a/b", reason: "github_api_error", message: "third" });
    const all = log.read(10);
    expect(all.map((e) => e.message)).toEqual(["third", "second", "first"]);
    const failures = log.read(10, ["skip", "error"]);
    expect(failures.map((e) => e.message)).toEqual(["third", "second"]);
  });

  it("countSince returns counts per kind", () => {
    const log = new EventLog(fakeLogger);
    log.emit({ kind: "ok", source_repo: "a/b", message: "1" });
    log.emit({ kind: "ok", source_repo: "a/b", message: "2" });
    log.emit({ kind: "skip", source_repo: "a/b", reason: "workflow_failure", message: "3" });
    const counts = log.countSince(60_000);
    expect(counts).toEqual({ ok: 2, skip: 1, error: 0 });
  });
});
