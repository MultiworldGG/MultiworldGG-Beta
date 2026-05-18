# MultiworldGG — Docker deploy

This directory contains the docker-compose stack and example config files for
running a MultiworldGG webhost in production. The stack consists of four
services:

- **multiworld** — game-hosting process (`python WebHost.py
  --config_override selflaunch.yaml`). Uses host networking for the dynamic
  port range games bind to.
- **web** — Flask app under gunicorn, serving the lobby / generate /
  tracker / room views.
- **nginx** — front proxy, serves static files and reverse-proxies the web
  service.
- **mwgg-github-bot** — Probot service running the Oliver + Karen GitHub
  Apps. Loopback-only; exposed to the public internet via the host's nginx,
  not this compose stack.

The `multiworld` and `web` services share the same image (built once by the
`multiworld` service's `build:` block, or pulled from GHCR).

## Host-side prerequisites

Run these once on a fresh host before `docker compose up`. Adjust paths for
your install location.

### 1. Persistent worlds venv

The webhost installs ~200 world wheels at first boot. To avoid re-downloading
them on every container recreate, the stack bind-mounts a host directory into
each container as the canonical `mwgg_venv` location:

```bash
sudo mkdir -p /var/lib/mwgg/mwgg_venv
sudo chown -R root:root /var/lib/mwgg/mwgg_venv   # container user is root
sudo chmod 755 /var/lib/mwgg
```

**Why a bind mount, not a named volume?** Bind mounts survive
`docker compose down -v` and arbitrary image rebuilds. Named volumes do not.
This directory is the source of truth for "installed worlds on this host" —
it should outlive any individual container.

**Backup:**
```bash
sudo tar -czf "mwgg-worlds-$(date +%F).tgz" -C /var/lib/mwgg mwgg_venv
```

**Restore on a new host:** rsync the directory to the same host path, then
`docker compose up -d`. The webhost will discover the installed worlds and
skip the cold install pass.

### 2. Config files

Copy each `example_*` file to its production name and edit:

| Example file | Production name | What it configures |
| --- | --- | --- |
| `example_config.yaml` | `config.yaml` | Webhost config: room limits, public hostname, DB credentials, etc. |
| `example_gunicorn.conf.py` | `gunicorn.conf.py` | Gunicorn workers, threads, log format. |
| `example_selflaunch.yaml` | `selflaunch.yaml` | Multiworld service config (game-hosting side). |
| `example_nginx.conf` | `nginx.conf` | The in-stack nginx config (front proxy). |
| `example_github-bot.env` | `github-bot.env` | GitHub App IDs, webhook secret paths, etc. `chmod 0600`. |
| `example_github-bot_nginx.conf` | (host nginx) | Snippet for the *host's* nginx (not this stack) — terminates TLS for `oliver.multiworld.gg` and proxies to `127.0.0.1:3000`. |

### 3. GitHub bot secrets directory

Create the secrets directory on the host (bind-mounted read-only into the bot
container at `/run/secrets`):

```bash
sudo mkdir -p ./github-bot-secrets
sudo chmod 700 ./github-bot-secrets
```

Place these files under it, then point the `*_FILE` env vars in
`github-bot.env` at `/run/secrets/<filename>`:

| File | Contents |
| --- | --- |
| `oliver_app_id` | One-line numeric App ID for the Oliver GitHub App. |
| `oliver_private_key.pem` | Full PEM private key for the Oliver App. |
| `oliver_webhook_secret` | One-line hex string used as the webhook HMAC secret. |
| `karen_app_id` | One-line numeric App ID for the Karen GitHub App. |
| `karen_private_key.pem` | Full PEM private key for the Karen App. |

## First-run flow

```bash
docker compose build
docker compose up -d
docker compose logs --tail=300 multiworld web
```

Expected log signature for a healthy cold start:

- `multiworld-1`: `Installing mwgg_igdb (ao) from game_index_ao`, followed by
  ~200 `Installing world: worlds.<slug>` lines as the worlds venv is populated.
  Eventually settles.
- `web-1`: `gunicorn` master starts, runs the same install pipeline once
  (workers do not re-import because `preload_app = True`), then two
  `gunicorn: worker` processes boot and stay up.
- `nginx-1`: ready for startup.
- `mwgg-github-bot-1`: `Oliver the Multiworld Squirrel is listening … Karen the
  Multiworld Knight is running automations on the Index`, `Listening on
  http://0.0.0.0:3000`.

Concurrent installs from multiworld and web are serialized by a POSIX file
lock at `/var/lib/mwgg/mwgg_venv/.mwgg-install.lock` — the second service to
arrive blocks until the first completes its `update()` pass, then sees the
venv already populated and exits the install loop fast.

## Upgrade flow

For routine updates (new world releases, mwgg_igdb refresh, code changes):

```bash
cd /opt/mwgg
git pull
docker compose down
docker compose build
docker compose up -d
```

`docker compose down` (no `-v`) keeps named volumes — the `app_volume`
shared between multiworld/web/nginx for logs/seeds/static assets stays.

If you need to nuke `app_volume` (rare — e.g., to reset all log history),
add `-v`:

```bash
docker compose down -v
```

This is **destructive to `app_volume`** but **not to
`/var/lib/mwgg/mwgg_venv`** — the latter is a host bind mount, not a managed
volume. Worlds installed there survive every compose command.

## Troubleshooting

- **World installs are slow on first boot.** Expected — ~200 wheels are
  fetched from GitHub release assets. Subsequent boots should be near-instant
  because `check_for_updates(worlds_only=True)` short-circuits when the
  installed version matches the index tag.
- **`gunicorn: HaltServer 'Worker failed to boot.'`** — workers boot before
  the install lock releases? No — `preload_app = True` runs the install in
  the master, before any worker is forked. If you still see this, check the
  master's logs immediately above the worker error; the worker boot error is
  usually downstream of a master import failure.
- **`AttributeError: 'str' object has no attribute 'exists'` from
  ModuleUpdate.** Should be fixed; if you see it, a caller is adding a string
  to `ModuleUpdate.requirements_files` instead of a `pathlib.Path`. Grep for
  `requirements_files.add` / `requirements_files.update`.
- **Bind mount permission errors (`PermissionError: '/root/.local/share/...'`).**
  The container runs as root by default. If you've reconfigured to run as a
  non-root user, adjust the host `chown` accordingly.
