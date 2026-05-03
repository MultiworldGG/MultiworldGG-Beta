import type { Request, Response, Router } from "express";
import type { Probot } from "probot";
import { EventLog, StoredEvent } from "./event-log";

const ONE_DAY_MS = 24 * 60 * 60 * 1000;

export function mountStatusRoutes(router: Router, probot: Probot): void {
  const log = new EventLog(probot.log);

  router.get("/", (_req: Request, res: Response) => {
    const counts = log.countSince(ONE_DAY_MS);
    const failures = log.read(50, ["skip", "error"]);
    res.setHeader("Content-Type", "text/html; charset=utf-8");
    res.send(renderHtml(counts, failures));
  });

  router.get("/.json", (_req: Request, res: Response) => {
    res.json({
      counts_24h: log.countSince(ONE_DAY_MS),
      events: log.read(200),
    });
  });
}

function renderHtml(
  counts: { ok: number; skip: number; error: number },
  failures: StoredEvent[],
): string {
  const rows = failures.length
    ? failures.map(failureRow).join("\n")
    : `<tr><td colspan="5" style="text-align:center;color:#888;padding:1.5em">no failures recorded</td></tr>`;
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Oliver status</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 2em; color: #222; }
  h1 { margin-bottom: 0.2em; }
  .summary { display: flex; gap: 1em; margin-bottom: 2em; }
  .badge { padding: 0.5em 1em; border-radius: 6px; font-weight: 600; }
  .ok { background: #d4edda; color: #155724; }
  .skip { background: #fff3cd; color: #856404; }
  .error { background: #f8d7da; color: #721c24; }
  table { border-collapse: collapse; width: 100%; }
  th, td { padding: 0.5em 0.75em; border-bottom: 1px solid #eee; text-align: left; vertical-align: top; font-size: 0.9em; }
  th { background: #f5f5f5; }
  tr.skip td:first-child { border-left: 4px solid #ffc107; }
  tr.error td:first-child { border-left: 4px solid #dc3545; }
  code { background: #f4f4f4; padding: 0.1em 0.3em; border-radius: 3px; font-size: 0.85em; }
</style>
</head>
<body>
<h1>Oliver status</h1>
<p style="color:#666;margin-top:0">Webhook receiver for the Oliver-Multiworld-Squirrel GitHub App.</p>

<h2>Last 24 hours</h2>
<div class="summary">
  <span class="badge ok">${counts.ok} ok</span>
  <span class="badge skip">${counts.skip} skip</span>
  <span class="badge error">${counts.error} error</span>
</div>

<h2>Recent failures (last ${failures.length} of skip/error)</h2>
<table>
  <thead>
    <tr><th>When</th><th>Source</th><th>Reason</th><th>Tag</th><th>Message</th></tr>
  </thead>
  <tbody>
${rows}
  </tbody>
</table>

<p style="color:#888;font-size:0.8em;margin-top:2em">
  Live tail: <code>docker compose logs -f oliver</code>.
  JSON: <a href="/status/.json">/status/.json</a>.
</p>
</body>
</html>`;
}

function failureRow(ev: StoredEvent): string {
  return `    <tr class="${esc(ev.kind)}">
      <td>${esc(ev.ts)}</td>
      <td>${esc(ev.source_repo)}</td>
      <td><code>${esc(ev.reason ?? "")}</code></td>
      <td>${esc(ev.release_tag ?? "")}</td>
      <td>${esc(ev.message)}</td>
    </tr>`;
}

function esc(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
