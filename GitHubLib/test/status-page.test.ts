import { describe, it, expect, beforeEach, afterEach } from "vitest";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";
import { mountStatusRoutes } from "../src/status-page";

const fakeLogger = {
  trace: () => {},
  debug: () => {},
  info: () => {},
  warn: () => {},
  error: () => {},
  fatal: () => {},
  child: () => fakeLogger,
} as any;

const fakeProbot = { log: fakeLogger } as any;

type Handler = (req: any, res: any) => void;

function botData(name: string) {
  return {
    name,
    installations_count: 1,
  } as any;
}

function makeRouter() {
  const handlers: Record<string, Handler> = {};
  return {
    get: (route: string, handler: Handler) => {
      handlers[route] = handler;
    },
    handlers,
  };
}

function captureHtml(handler: Handler): { body: string; headers: Record<string, string> } {
  const headers: Record<string, string> = {};
  let body = "";
  const res = {
    setHeader: (k: string, v: string) => {
      headers[k] = v;
    },
    send: (s: string) => {
      body = s;
    },
    json: (o: any) => {
      body = JSON.stringify(o);
      headers["Content-Type"] = "application/json";
    },
  };
  handler({}, res);
  return { body, headers };
}

let tmpDir: string;

beforeEach(() => {
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "oliver-status-page-"));
  process.env.OLIVER_LOG_DIR = tmpDir;
});

afterEach(() => {
  fs.rmSync(tmpDir, { recursive: true, force: true });
  delete process.env.OLIVER_LOG_DIR;
});

describe("status page (TODO #1 hardening)", () => {
  it("renders the new title and h1 and does not leak service-internal strings", () => {
    const router = makeRouter();
    mountStatusRoutes(router as any, fakeProbot, botData("oliver-multiworld-squirrel"), botData("karen-multiworld-bot"));
    const { body, headers } = captureHtml(router.handlers["/"]);

    expect(headers["Content-Type"]).toMatch(/text\/html/);
    expect(body).toContain("<title>Karen & Oliver MWGG Status</title>");
    expect(body).toContain("<h1>Karen & Oliver MWGG Status</h1>");

    expect(body).not.toMatch(/MWGG GitHub-bot/i);
    expect(body).not.toMatch(/docker compose/i);
    expect(body).not.toMatch(/mwgg-github-bot/);
    expect(body).not.toMatch(/Webhook receiver/i);
  });

  it("still renders the dynamic Oliver and Karen slugs", () => {
    const router = makeRouter();
    mountStatusRoutes(router as any, fakeProbot, botData("some-oliver-slug"), botData("some-karen-slug"));
    const { body } = captureHtml(router.handlers["/"]);
    expect(body).toContain("some-oliver-slug");
    expect(body).toContain("some-karen-slug");
  });

  it("still exposes the JSON endpoint with counts and events", () => {
    const router = makeRouter();
    mountStatusRoutes(router as any, fakeProbot, botData("o"), botData("k"));
    const { body, headers } = captureHtml(router.handlers["/.json"]);
    expect(headers["Content-Type"]).toBe("application/json");
    const parsed = JSON.parse(body);
    expect(parsed).toHaveProperty("counts_24h");
    expect(parsed).toHaveProperty("events");
  });
});
