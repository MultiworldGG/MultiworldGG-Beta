import * as fs from "fs";
import * as path from "path";
import type { Logger } from "probot";

const ROTATE_BYTES = 10 * 1024 * 1024;

function logDir(): string {
  return process.env.OLIVER_LOG_DIR ?? "/var/lib/oliver";
}
function logFile(): string {
  return path.join(logDir(), "events.jsonl");
}

export type EventKind = "ok" | "skip" | "error";

export type EventReason =
  | "no_world_folder_name"
  | "no_slug_resolved"
  | "workflow_failure"
  | "branch_missing"
  | "tag_missing"
  | "wheel_asset_missing"
  | "wheel_asset_ambiguous"
  | "asset_digest_missing"
  | "release_lookup_404"
  | "release_not_found"
  | "index_install_missing"
  | "github_api_error"
  | "codeowners_conflict";

export interface OliverEvent {
  kind: EventKind;
  source_repo: string;
  release_tag?: string;
  slug?: string;
  release_sha?: string;
  wheel_sha?: string;
  wheel_asset?: string;
  wheel_size_bytes?: number;
  module_location?: string;
  index_pr?: number;
  reason?: EventReason;
  message: string;
}

export interface StoredEvent extends OliverEvent {
  ts: string;
}

export class EventLog {
  constructor(private readonly logger: Logger) {}

  emit(event: OliverEvent): void {
    const stored: StoredEvent = { ts: new Date().toISOString(), ...event };
    this.writeToDisk(stored);
    const fields = { ...stored, msg: undefined };
    if (event.kind === "ok") this.logger.info(fields, event.message);
    else if (event.kind === "skip") this.logger.warn(fields, event.message);
    else this.logger.error(fields, event.message);
  }

  read(limit: number, kindFilter?: EventKind[]): StoredEvent[] {
    if (!fs.existsSync(logFile())) return [];
    const raw = fs.readFileSync(logFile(), "utf-8");
    const lines = raw.split("\n").filter((l) => l.length > 0);
    const out: StoredEvent[] = [];
    for (let i = lines.length - 1; i >= 0 && out.length < limit; i--) {
      try {
        const ev = JSON.parse(lines[i]) as StoredEvent;
        if (!kindFilter || kindFilter.includes(ev.kind)) out.push(ev);
      } catch {
        continue;
      }
    }
    return out;
  }

  countSince(sinceMs: number): { ok: number; skip: number; error: number } {
    if (!fs.existsSync(logFile())) return { ok: 0, skip: 0, error: 0 };
    const cutoff = Date.now() - sinceMs;
    const counts = { ok: 0, skip: 0, error: 0 };
    const raw = fs.readFileSync(logFile(), "utf-8");
    for (const line of raw.split("\n")) {
      if (!line) continue;
      try {
        const ev = JSON.parse(line) as StoredEvent;
        if (new Date(ev.ts).getTime() < cutoff) continue;
        counts[ev.kind]++;
      } catch {
        continue;
      }
    }
    return counts;
  }

  private writeToDisk(event: StoredEvent): void {
    try {
      fs.mkdirSync(logDir(), { recursive: true });
      this.rotateIfNeeded();
      fs.appendFileSync(logFile(), JSON.stringify(event) + "\n");
    } catch (err) {
      this.logger.error({ err }, "failed to write event to disk");
    }
  }

  private rotateIfNeeded(): void {
    try {
      const stat = fs.statSync(logFile());
      if (stat.size < ROTATE_BYTES) return;
      const archive = logFile() + ".1";
      fs.renameSync(logFile(), archive);
    } catch (err: unknown) {
      const code = (err as { code?: string }).code;
      if (code === "ENOENT") return;
      throw err;
    }
  }
}
