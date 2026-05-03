// GitHub-bot — nginx-edge HMAC validation for GitHub webhooks.
//
// Loaded by deploy/example_github-bot_nginx.conf via:
//   js_path "/etc/nginx/njs/";
//   js_import hmac.js;
// then invoked from the request location with `js_content hmac.validate`.
//
// What this does:
//   - On POST / (the GitHub webhook URL), reads the request body, computes
//     HMAC-SHA256 with the secret loaded from SECRET_FILE, compares to
//     X-Hub-Signature-256 in constant time. On mismatch, returns 401 *before*
//     nginx ever proxies to the bot container.
//   - On GET /probot or /status, lets the request through unauthenticated —
//     Probot's built-in info page and the bot's failure-log status page.
//   - All other methods → 405; missing/malformed signatures → 401.
//
// Probot inside the container ALSO validates HMAC. This nginx layer is
// defense-in-depth: bogus traffic is rejected at the edge without spinning
// up an event-loop tick in the app.

import crypto from "crypto";
import fs from "fs";

// Operator: place the webhook secret here, mode 0640, owner root, group
// www-data (or whichever user nginx runs as on this host).
//   sudo mkdir -p /etc/github-bot
//   sudo cp deploy/github-bot-secrets/oliver_webhook_secret /etc/github-bot/webhook_secret
//   sudo chgrp www-data /etc/github-bot/webhook_secret
//   sudo chmod 0640 /etc/github-bot/webhook_secret
const SECRET_FILE = "/etc/github-bot/webhook_secret";

let cachedSecret = null;

function getSecret() {
    if (cachedSecret !== null) return cachedSecret;
    try {
        cachedSecret = fs.readFileSync(SECRET_FILE).toString().replace(/\s+$/, "");
    } catch (err) {
        return null;
    }
    return cachedSecret;
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

    const secret = getSecret();
    if (!secret) {
        r.error("oliver_hmac: webhook secret unreadable at " + SECRET_FILE);
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
