// GitHub-bot: nginx-edge HMAC validation for GitHub webhooks.
//
// Loaded by deploy/example_github-bot_nginx.conf via:
//   js_path "/etc/nginx/njs/";
//   js_import hmac.js;
// then invoked from the request location with `js_content hmac.validate`.
//
// What this does:
//   - The bot fronts TWO signed webhooks, one per GitHub App, each on its OWN
//     hostname with its OWN secret:
//       oliver.multiworld.gg    → Oliver, secret OLIVER_SECRET_FILE → @bot_backend
//       karen.prismativerse.com → Karen,  secret KAREN_SECRET_FILE  → @karen_backend
//     Each server sets `$webhook_app` ("oliver" | "karen"); we pick the secret
//     + the internal backend from THAT (not the path, since both arrive at "/").
//     We read the body, compute HMAC-SHA256, and compare to X-Hub-Signature-256
//     in constant time. On mismatch, returns 401 *before* any proxy_pass.
//   - Oliver's GET /status pages pass through unauthenticated (the bot's
//     failure-log status page).
//   - All other methods → 405; missing/malformed signatures → 401.
//
// Probot/@octokit/webhooks inside the container ALSO validate HMAC (each against
// its own secret). This nginx layer is defense-in-depth: bogus traffic is
// rejected at the edge without spinning up an event-loop tick in the app.

import crypto from "crypto";
import fs from "fs";

// Operator: place each webhook secret here, mode 0640, owner root, group
// www-data (or whichever user nginx runs as on this host).
//   sudo mkdir -p /etc/github-bot
//   sudo cp deploy/github-bot-secrets/oliver_webhook_secret /etc/github-bot/webhook_secret
//   sudo cp deploy/github-bot-secrets/karen_webhook_secret  /etc/github-bot/karen_webhook_secret
//   sudo chgrp www-data /etc/github-bot/webhook_secret /etc/github-bot/karen_webhook_secret
//   sudo chmod 0640 /etc/github-bot/webhook_secret /etc/github-bot/karen_webhook_secret
const OLIVER_SECRET_FILE = "/etc/github-bot/webhook_secret";
const KAREN_SECRET_FILE = "/etc/github-bot/karen_webhook_secret";

// One cache slot per secret file; each is read once on first use.
const secretCache = {};

function readSecretFile(file) {
    if (secretCache[file] !== undefined) return secretCache[file];
    let value;
    try {
        value = fs.readFileSync(file).toString().replace(/\s+$/, "");
    } catch (err) {
        value = null;
    }
    secretCache[file] = value;
    return value;
}

// Per-server identity, set via `set $webhook_app …;` ahead of js_content.
// Karen → her secret + the @karen_backend (which rewrites "/" → "/karen");
// anything else (default) → Oliver's secret + @bot_backend.
function configForApp(r) {
    if (r.variables.webhook_app === "karen") {
        return { app: "karen", secretFile: KAREN_SECRET_FILE, backend: "@karen_backend" };
    }
    return { app: "oliver", secretFile: OLIVER_SECRET_FILE, backend: "@bot_backend" };
}

function constantTimeEqual(a, b) {
    if (a.length !== b.length) return false;
    let result = 0;
    for (let i = 0; i < a.length; i++) {
        result |= a.charCodeAt(i) ^ b.charCodeAt(i);
    }
    return result === 0;
}

function validate(r) {
    const cfg = configForApp(r);

    // Oliver's info/status pages are GET and unauthenticated:
    //   /status, /status/, /status/.json: bot's identity + failure-log page.
    if (cfg.app === "oliver" && r.method === "GET" && (
        r.uri === "/status" ||
        r.uri.startsWith("/status/")
    )) {
        r.internalRedirect(cfg.backend);
        return;
    }

    if (r.method !== "POST") {
        r.return(405, "method not allowed\n");
        return;
    }

    const secret = readSecretFile(cfg.secretFile);
    if (!secret) {
        r.error("mwgg_hmac: " + cfg.app + " webhook secret unreadable at " + cfg.secretFile);
        r.return(503, "service misconfigured\n");
        return;
    }

    const sigHeader = r.headersIn["X-Hub-Signature-256"];
    if (!sigHeader) {
        r.return(401, "missing X-Hub-Signature-256\n");
        return;
    }
    if (!sigHeader.startsWith("sha256=")) {
        r.return(401, "malformed X-Hub-Signature-256\n");
        return;
    }
    const expected = sigHeader.substring("sha256=".length);

    const body = r.requestText;
    if (!body) {
        r.return(401, "empty body\n");
        return;
    }

    const hmac = crypto.createHmac("sha256", secret);
    hmac.update(body);
    const computed = hmac.digest("hex");

    if (!constantTimeEqual(computed, expected)) {
        r.return(401, "bad signature\n");
        return;
    }

    r.internalRedirect(cfg.backend);
}

export default { validate };
