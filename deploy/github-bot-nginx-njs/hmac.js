// GitHub-bot — nginx-edge HMAC validation for GitHub webhooks.
//
// Loaded by deploy/example_github-bot_nginx.conf via:
//   js_path "/etc/nginx/njs/";
//   js_import hmac.js;
// then invoked from the request location with `js_content hmac.validate`.
//
// What this does:
//   - The bot serves TWO signed webhooks, each with its own secret:
//       POST /        → Oliver (GitHub App events), secret OLIVER_SECRET_FILE.
//       POST /karen…  → Karen (repository_dispatch / karen-fuzz), secret
//                       KAREN_SECRET_FILE. Any path starting with "/karen"
//                       (the bot mounts its verifier at the /karen router root).
//     We pick the secret by request path, read the body, compute HMAC-SHA256,
//     and compare to X-Hub-Signature-256 in constant time. On mismatch, returns
//     401 *before* nginx ever proxies to the bot container.
//   - On GET /probot or /status, lets the request through unauthenticated —
//     Probot's built-in info page and the bot's failure-log status page.
//   - All other methods → 405; missing/malformed signatures → 401.
//
// Probot/Octokit inside the container ALSO validate HMAC (each against its own
// secret). This nginx layer is defense-in-depth: bogus traffic is rejected at
// the edge without spinning up an event-loop tick in the app.

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

// Select the secret file by request path: /karen… → Karen, everything else
// (i.e. the "/" webhook) → Oliver.
function secretFileForPath(uri) {
    return uri.startsWith("/karen") ? KAREN_SECRET_FILE : OLIVER_SECRET_FILE;
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
    // Allow these GET path prefixes through unauthenticated:
    //   /status, /status/, /status/.json — bot's identity + failure-log page
    if (r.method === "GET" && (
        r.uri === "/status" ||
        r.uri.startsWith("/status/")
    )) {
        r.internalRedirect("@bot_backend");
        return;
    }

    if (r.method !== "POST") {
        r.return(405, "method not allowed\n");
        return;
    }

    const secretFile = secretFileForPath(r.uri);
    const secret = readSecretFile(secretFile);
    if (!secret) {
        r.error("oliver_hmac: webhook secret unreadable at " + secretFile);
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

    r.internalRedirect("@bot_backend");
}

export default { validate };
