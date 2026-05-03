# Oliver-Multiworld-Squirrel

Webhook receiver for the `Oliver-Multiworld-Squirrel` GitHub App. Listens for `release.published` events on per-world repos, builds the orphan-branch tree in-process, pushes it back to the per-world repo as `module-install/<slug>` + tag `module-install/<slug>/<world_version>`, and opens a corresponding PR on `MultiworldGG-Index`.

## How per-world authors use Oliver

1. Install the **Oliver-Multiworld-Squirrel** GitHub App on the per-world repo (one click, public install page).
2. Cut a GitHub Release. Done.

That's it. No workflow file, no secrets, no PEM. Oliver receives the webhook, figures out which world the release is for via diff-based slug discovery (see `src/slug-discovery.ts`), builds + pushes + opens the Index PR.

If Oliver can't determine the slug (e.g. the release touched multiple `worlds/<slug>/`), it posts a comment on the release **and** opens an Issue on `MultiworldGG-Index` asking maintainers to PR by hand.

## Env vars

Each secret can be supplied **inline** (`OLIVER_FOO=value`) **or via file path** (`OLIVER_FOO_FILE=/path/inside/container`). Pick whichever you prefer per-secret; if both are set, the file wins. The file pattern is recommended for the PEM (multi-line, awkward to inline) and for any operator who prefers Docker-secrets-style file mounts.

| Var | Required | Notes |
|---|---|---|
| `OLIVER_APP_ID` / `OLIVER_APP_ID_FILE` | yes | Numeric App ID from the GitHub App's General settings page. |
| `OLIVER_PRIVATE_KEY` / `OLIVER_PRIVATE_KEY_FILE` | yes | Full PEM of the App's private key. Inline form: wrap in double quotes with `\n` for newlines. File form: just point at the `.pem` and forget about escaping. |
| `OLIVER_WEBHOOK_SECRET` / `OLIVER_WEBHOOK_SECRET_FILE` | yes | Webhook secret configured on the App. |
| `OLIVER_INDEX_REPO` | no | `<owner>/<repo>` of the Index. Defaults to `lallaria/MultiworldGG-Index`. Not a secret. |
| `PORT` | no | Bind port. Defaults to `3000`. |

The compose service at `deploy/docker-compose.yml` bind-mounts `deploy/oliver-secrets/` to `/run/secrets:ro` inside the container, so `OLIVER_PRIVATE_KEY_FILE=/run/secrets/oliver_private_key.pem` resolves cleanly. Keep this directory at mode 0700 on the host; the contents are gitignored except for the `.gitkeep` placeholder.

## Local development

```
npm install
npm run build
npm test
```

To run locally against real webhooks during development, use `smee.io` to forward webhooks to `localhost:3000`. The App's webhook URL during development should be the smee channel URL.

## Production deployment (Ubuntu host)

The production host is bare Ubuntu with Docker installed. The public-facing TCP listener is **system nginx** (`/etc/nginx/`, started via `systemctl`), **not** an in-Docker nginx. Oliver runs as a Docker container; system nginx proxies `oliver.multiworld.gg` to the container's loopback-published port.

Topology:

```
internet ──TLS── system nginx (Ubuntu host, /etc/nginx/) ──127.0.0.1:3000── oliver container (docker compose)
```

Operator setup on the production host:

1. Copy + populate the env file:
   ```
   cd <repo>/deploy
   cp example_oliver.env oliver.env
   chmod 600 oliver.env
   $EDITOR oliver.env  # fill in OLIVER_APP_ID, OLIVER_PRIVATE_KEY, OLIVER_WEBHOOK_SECRET
   ```

2. Build + start the container (publishes 127.0.0.1:3000 only — not internet-reachable):
   ```
   docker compose -f docker-compose.yml up -d --build oliver
   docker compose logs oliver  # verify Probot startup banner
   ```

3. Drop the host-nginx snippet into place (or your distro's equivalent):
   ```
   sudo cp example_oliver_nginx.conf /etc/nginx/sites-available/oliver.multiworld.gg.conf
   sudo ln -s /etc/nginx/sites-available/oliver.multiworld.gg.conf /etc/nginx/sites-enabled/oliver.multiworld.gg.conf
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. Add the DNS A record for `oliver.multiworld.gg`.

5. (Optional) If TLS terminates on this host (vs. upstream Cloudflare), run:
   ```
   sudo certbot --nginx -d oliver.multiworld.gg
   ```

Verify end-to-end:
- `docker compose logs oliver` shows "Oliver listening for release.published events".
- `curl http://127.0.0.1:3000/probot` from the host returns Probot's health page.
- `curl https://oliver.multiworld.gg/probot` from anywhere returns the same.
- The GitHub App's "Recent Deliveries" panel shows 200 responses for test webhooks.

## Layout

```
GitHubLib/
├── src/
│   ├── index.ts              Probot Server bootstrap
│   ├── app.ts                Event registration
│   ├── handlers/release.ts   release.published orchestrator
│   ├── slug-discovery.ts     diff-based slug detection (the critical-correctness module)
│   ├── shape-orphan.ts       port of build-and-publish-action's shape_orphan.py
│   ├── git-ops.ts            simple-git wrapper: clone, push orphan branch + tag
│   └── templates/            Handlebars templates for pyproject.toml + README.md
├── test/                     Jest tests
├── Dockerfile                multi-stage Node 20 alpine
└── package.json
```

## Slug discovery (the design choice)

Per-world repos almost always start as forks of the MultiworldGG monorepo (which contains all 250+ worlds). Directory enumeration would publish every world. Oliver instead uses the **diff** between this release and the previous release (or the parent default branch on first-release-of-fork, or a whole-tree scan for from-scratch repos) and accepts the slug only when exactly one candidate emerges.

Multi-world repos (think Pokémon Red and Pokémon Blue from one repo) are supported by cutting **separate releases per world**. Oliver fires once per release.

Skip path: if 0 or >1 candidates, Oliver posts a release comment AND opens an Issue on the Index for human review. No silent failures.
