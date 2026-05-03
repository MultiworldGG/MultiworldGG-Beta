# Oliver-Multiworld-Squirrel

Webhook receiver for the `Oliver-Multiworld-Squirrel` GitHub App. Watches per-world repos for the `Create and Release Python Package` workflow to finish (i.e. `MultiworldGG/build-and-publish-action` has shaped + pushed the wheel branch + tag), then opens a corresponding PR on `MultiworldGG-Index` updating `worlds/<slug>.json` to point at the new tag's pinned SHA.

Oliver does NOT clone, build, or push to per-world repos. The build is done by the per-world repo's own workflow under its own `GITHUB_TOKEN`.

## Two Apps: Oliver + Karen

GitHub Apps have one global permission set per App. To keep the per-world install prompt strictly non-scary while still letting the bot write to the Index, Oliver is split into two App identities:

- **Oliver-Multiworld-Squirrel** — installed on per-world repos AND the Index.
  - Permissions: `Contents: Read`, `Actions: Read`, `Pull requests: Read and write`, `Metadata: Read`.
  - **Subscribe to events:** **Workflow run** *only* (NOT "Release" — Oliver doesn't act on `release.*` payloads, only on `workflow_run.completed`).
  - The PR-write grant on per-world repos is unused but visible at install time (acceptable trade-off).
- **Karen** — installed on **the Index only**.
  - Permissions: `Contents: Read and write`, `Metadata: Read`.
  - **Subscribe to events:** none (no webhook). Does the branch-create + manifest-commit on the Index when Oliver tells her to.

The Oliver service holds both Apps' PEMs. On a webhook from a per-world repo, the service:

1. Authenticates as Oliver (via the webhook's installation) to read per-world repo data.
2. Authenticates as Karen (via Karen's app-level JWT → installation token on the Index) to create the `update/<slug>-<release_tag>` branch and commit the manifest change.
3. Authenticates as Oliver again (Oliver's installation on the Index) to open the PR.
4. Karen's existing PR-review workflow (`MultiworldGG-Index/.github/workflows/karen-pr-review.yml`) auto-fires when Oliver opens the PR and posts review checks.

## How per-world authors use Oliver

1. Install the **Oliver-Multiworld-Squirrel** GitHub App on the per-world repo (one click; only requests read permissions on the repo).
2. Set a repository variable: Settings → Secrets and variables → Actions → Variables → New: `WORLD_FOLDER_NAME=<slug>` (e.g. `WORLD_FOLDER_NAME=clique`).
3. Add `.github/workflows/make_pyproject.yml`:

   ```yaml
   name: Create and Release Python Package
   on:
     release:
       types: [published]
     workflow_dispatch: {}

   permissions:
     contents: write   # for the wheel branch + tag push to this repo

   jobs:
     publish:
       uses: MultiworldGG/build-and-publish-action/.github/workflows/build.yml@v3
       # No `with:` — slug comes from vars.WORLD_FOLDER_NAME
       # No `secrets:` — no Oliver secrets needed
   ```

4. Cut a GitHub Release.

That's it. Within ~30s of the workflow finishing, Oliver opens a PR on the Index.

## What Oliver does on each event

1. Receives `workflow_run.completed` webhook from the per-world repo.
2. Filters on workflow name (`Create and Release Python Package`), event (`release`), and conclusion (`success`).
3. Reads the `WORLD_FOLDER_NAME` repo variable to find the slug.
4. Resolves `workflow_run.head_sha` to the matching release tag name.
5. Resolves the `wheel/worlds/<slug>/<release_tag>` tag (created by build-and-publish-action) to a commit SHA.
6. Authenticates as the App for `lallaria/MultiworldGG-Index`, opens or updates a PR on `update/<slug>-<release_tag>` with `module_location = git+https://github.com/<owner>/<repo>.git@<sha>`.
7. Logs the outcome (success / skip / error) to `/var/lib/oliver/events.jsonl`.

If any step 2–6 fails (no `WORLD_FOLDER_NAME` set, workflow concluded `failure`, wheel tag missing, Oliver not installed on Index, etc.), Oliver writes a `skip` or `error` record to the JSONL log and returns 200 to GitHub. No issues are opened on the per-world repo or the Index — failures surface only on the `/status` page.

## Env vars

Each secret can be supplied **inline** (`OLIVER_FOO=value`) **or via file path** (`OLIVER_FOO_FILE=/path/inside/container`). Pick whichever you prefer per-secret; if both are set, the file wins. The file pattern is recommended for the PEM (multi-line, awkward to inline).

| Var | Required | Notes |
|---|---|---|
| `OLIVER_APP_ID` / `OLIVER_APP_ID_FILE` | yes | Numeric App ID from Oliver's General settings page. |
| `OLIVER_PRIVATE_KEY` / `OLIVER_PRIVATE_KEY_FILE` | yes | Full PEM of Oliver's private key. Inline form: wrap in double quotes with `\n` for newlines. File form: just point at the `.pem`. |
| `OLIVER_WEBHOOK_SECRET` / `OLIVER_WEBHOOK_SECRET_FILE` | yes | Webhook secret configured on Oliver. |
| `KAREN_APP_ID` / `KAREN_APP_ID_FILE` | yes | Numeric App ID from Karen's General settings page. |
| `KAREN_PRIVATE_KEY` / `KAREN_PRIVATE_KEY_FILE` | yes | Full PEM of Karen's private key. |
| `OLIVER_INDEX_REPO` | no | `<owner>/<repo>` of the Index. Defaults to `lallaria/MultiworldGG-Index`. Not a secret. |
| `OLIVER_LOG_DIR` | no | Where `events.jsonl` is written. Defaults to `/var/lib/oliver`. |
| `PORT` | no | Bind port. Defaults to `3000`. |

The compose service at `deploy/docker-compose.yml` bind-mounts `deploy/github-bot-secrets/` to `/run/secrets:ro` inside the container, so `OLIVER_PRIVATE_KEY_FILE=/run/secrets/oliver_private_key.pem` resolves cleanly. Keep that directory at mode 0700 on the host; the contents are gitignored except for the `.gitkeep` placeholder.

## Status / monitoring

One surface: **`GET /status`**.

Top of the page shows the bot's two App identities (Oliver + Karen). Below that, a 24h ok/skip/error count summary, then a table of the last 50 skip/error entries from `events.jsonl`. JSON form at `/status/.json` returns the same data plus the last 200 events of all kinds.

`/status` and `/status/*` pass through the nginx-edge HMAC validation as unauthenticated GET requests; POST traffic still requires a valid GitHub webhook signature.

In-process runtime logs go to stdout via Probot's bundled pino logger — `docker compose logs mwgg-github-bot` for live tailing.

## Local development

```
npm install
npm run build
npm test
```

To run locally against real webhooks during development, use `smee.io` to forward webhooks to `localhost:3000`. The App's webhook URL during development should be the smee channel URL.

## Production deployment (Ubuntu host)

The production host is bare Ubuntu with Docker installed. The public-facing TCP listener is **system nginx** (`/etc/nginx/`), **not** an in-Docker nginx. nginx terminates TLS using a Let's Encrypt cert and proxies `oliver.multiworld.gg` to the container's loopback-published port.

Topology:

```
internet ─HTTPS:443─ system nginx (Ubuntu host, TLS terminates here) ─HTTP─127.0.0.1:3000─▶ container
```

Operator setup on the production host:

1. Copy + populate the env file:
   ```
   cd <repo>/deploy
   cp example_github-bot.env github-bot.env
   chmod 600 github-bot.env
   $EDITOR github-bot.env  # fill in OLIVER_* + KAREN_* (inline or _FILE form)
   ```

2. Drop secret files into the bind-mount dir (if using `_FILE` form):
   ```
   mkdir -m 700 github-bot-secrets
   cp ~/protected/oliver_private_key.pem github-bot-secrets/oliver_private_key.pem
   cp ~/protected/karen_private_key.pem  github-bot-secrets/karen_private_key.pem
   echo "12345" > github-bot-secrets/oliver_app_id
   echo "67890" > github-bot-secrets/karen_app_id
   openssl rand -hex 32 > github-bot-secrets/oliver_webhook_secret
   chmod 600 github-bot-secrets/*
   ```

3. Build + start the container (publishes 127.0.0.1:3000 only — not internet-reachable):
   ```
   docker compose -f docker-compose.yml up -d --build mwgg-github-bot
   docker compose logs mwgg-github-bot  # verify "Oliver listening for workflow_run.completed events"
   ```

4. Install the njs module + drop the validation script + webhook secret into place for nginx-edge HMAC validation:
   ```
   sudo apt install libnginx-mod-http-js
   sudo mkdir -p /etc/nginx/njs /etc/github-bot
   sudo cp github-bot-nginx-njs/hmac.js /etc/nginx/njs/
   sudo cp github-bot-secrets/oliver_webhook_secret /etc/github-bot/webhook_secret
   sudo chgrp www-data /etc/github-bot/webhook_secret
   sudo chmod 0640 /etc/github-bot/webhook_secret
   sudo chmod 0750 /etc/github-bot
   ```

5. Add a DNS A record for `oliver.multiworld.gg` pointing at this host.

6. Provision the Let's Encrypt cert:
   ```
   sudo certbot certonly --nginx -d oliver.multiworld.gg
   ```

7. Drop the host-nginx snippet into place:
   ```
   sudo cp example_github-bot_nginx.conf /etc/nginx/sites-available/oliver.multiworld.gg.conf
   sudo ln -s /etc/nginx/sites-available/oliver.multiworld.gg.conf /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

   The snippet listens on 443 with TLS, redirects 80→443, validates HMAC at the edge via njs, and proxies to `127.0.0.1:3000`.

Verify end-to-end:
- `docker compose logs mwgg-github-bot` shows "Oliver listening for workflow_run.completed events".
- `curl https://oliver.multiworld.gg/probot` returns Probot's stock info page.
- `curl https://oliver.multiworld.gg/status` returns the HTML status page (initially empty: "0 events in last 24h").
- The GitHub App's "Recent Deliveries" panel shows 200 responses for test webhooks.

## Layout

```
GitHubLib/
├── src/
│   ├── index.ts                Probot Server bootstrap (env loading, port binding)
│   ├── app.ts                  Event registration; mounts /status route
│   ├── handlers/workflow_run.ts  workflow_run.completed orchestrator (the main flow)
│   ├── release-resolver.ts     resolves head_sha → release tag name
│   ├── repo-vars.ts            reads `WORLD_FOLDER_NAME` repo variable
│   ├── index-pr.ts             opens or updates the Index PR
│   ├── event-log.ts            JSONL append-only logger + pino fan-out
│   └── status-page.ts          GET /status HTML + JSON renderer
├── test/                       Vitest tests
├── Dockerfile                  multi-stage Node 20 alpine
└── package.json
```
