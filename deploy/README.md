# MultiworldGG — Docker deploy

This directory contains the docker-compose stack and example config files for
running a MultiworldGG webhost in production. The stack consists of these
services:

- **mwgg_upgrader** — run-once job that populates the shared worlds venv (the
  `mwgg_igdb` "ao" index + every world + the worlds' requirements), then
  exits. It is the *only* writer of the venv; every other service mounts it
  read-only and waits for this job to finish.
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

All app services share the same image (built once by the `multiworld`
service's `build:` block, or pulled from GHCR). `multiworld` and `web` run as
pure venv consumers with `SKIP_ALL_INSTALLS=1`; only `mwgg_upgrader` installs.

## Host-side prerequisites

Run these once on a fresh host before `docker compose up`. Adjust paths for
your install location.

### 1. Persistent worlds venv

The `mwgg_upgrader` job installs ~200 world wheels at first boot. To avoid
re-downloading them on every container recreate, the stack bind-mounts a host
directory into each container as the canonical `mwgg_venv` location:

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
| `karen_webhook_secret` | One-line hex string — HMAC secret for Karen's `/karen` webhook (`openssl rand -hex 32`). |

### 4. Karen fuzz sandbox (optional, for the Index PR fuzzer)

The Karen App's `/karen` webhook receives `repository_dispatch` (`karen-fuzz`)
events from the Index PR workflow and, per proposed world, spawns a short-lived
hardened container that downloads + sha256-verifies the wheel, runs the
security/quality scan (bandit, pip-audit, ruff, size/ROM/import), and fuzzes
generation — reporting back via a `Karen / fuzz` Check Run + the sticky PR
comment. To enable it:

1. **Fuzz scratch dir** (bind-mounted into the bot at the *same* host path so the
   inner `docker run -v` resolves on the host daemon):
   ```bash
   sudo mkdir -p /var/lib/mwgg-fuzz
   sudo chmod 700 /var/lib/mwgg-fuzz
   ```
2. **Build/publish the fuzz image** referenced by `FUZZ_IMAGE`. The container runs
   `--network none`, so core, its venv, and `fuzz.py` are baked in at build time —
   the *build* needs network and pins the sources via build args:
   ```bash
   docker build \
     --build-arg MWGG_CORE_REF=main \
     --build-arg FUZZER_REF=main \
     -t ghcr.io/multiworldgg/multiworldgg-fuzz:latest ../GitHubLib/fuzz-image
   ```
   (`MWGG_CORE_REPO` / `FUZZER_REPO` are also overridable. Rebuild to pick up a
   newer core/fuzzer pin — per the design, core need not be fresh every run.)
3. **No fuzz network — nothing to set up.** The fuzz container runs with
   `--network none`: the bot downloads + sha256-verifies each wheel and bind-mounts
   it read-only at `/in`, and everything else is baked into the image. There is no
   egress bridge to create or firewall; untrusted world code simply has zero
   network. (Trade-off: the `pip_audit` scan, which needs PyPI's advisory DB, is
   skipped — world wheels declare no deps, so its surface is ~empty.)
4. **Karen App config:** Webhook URL `https://karen.prismativerse.com/` (Karen's
   own subdomain — needs a DNS A record + its own Let's Encrypt cert; the host
   nginx validates the Karen HMAC and maps it to the bot's internal `/karen`),
   subscribe to `repository_dispatch`, permissions Checks:Write +
   Pull-requests:Write (plus the existing Contents:Write + Metadata:Read). Put
   `karen_webhook_secret` in `./github-bot-secrets` *and* on the host nginx at
   `/etc/github-bot/karen_webhook_secret` (see `example_github-bot_nginx.conf`).
5. **Docker access:** the `docker-socket-proxy` sidecar fronts
   `/var/run/docker.sock` (mounted read-only into the proxy only); the bot
   reaches it via `DOCKER_HOST`. Never mount the raw socket into the bot.
6. **Optional ROMs:** ROM-dependent worlds only generate if their base ROMs are
   present. Set `FUZZ_ROM_DIR` (host dir, mounted read-only at `/roms`) and
   `FUZZ_HOST_YAML` (a `host.yaml` whose `<world>_options.rom_file` entries point
   at `/roms/<file>`); both must be readable by uid 65532. Untrusted world code
   can READ (not write) the ROMs and the container has egress, so only expose
   ROMs you accept could be exfiltrated. Unset → ROM worlds warn (no-op).

Capacity note: each fuzz container clones core + builds a venv + generates
(~2-4 GB / 1-2 CPU, minutes). `FUZZ_MAX_CONCURRENCY=1` keeps it gentle on a
shared host; raise it only with headroom.

## First-run flow

```bash
docker compose build
docker compose up -d
docker compose logs --tail=300 multiworld web
```

Expected log signature for a healthy cold start:

- `mwgg_upgrader-1`: `Installing mwgg_igdb (ao)`, then ~200
  `Installing world: worlds.<slug>` lines as the venv is populated, then
  `mwgg_venv ready` and the container exits 0.
- `multiworld-1` / `web-1`: held until `mwgg_upgrader` exits successfully
  (`service_completed_successfully`). Neither installs anything
  (`SKIP_ALL_INSTALLS=1`) — they import worlds from the read-only venv.
  `web-1` boots the `gunicorn` master then two workers (`preload_app = True`);
  `multiworld-1` begins hosting.
- `nginx-1`: ready for startup.
- `mwgg-github-bot-1`: `Oliver the Multiworld Squirrel is listening … Karen Head 
   of Multiworld QA is running automations on the Index`, `Listening on
  http://0.0.0.0:3000`.

Because a single `mwgg_upgrader` job owns all writes to the venv, the old
multiworld/web install race is gone — the consumers just read the populated,
read-only venv. (The install lock at
`/var/lib/mwgg/mwgg_venv/.mwgg-install.lock` still guards concurrent manual
runs of the upgrader.)

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

### Refreshing only the worlds venv

To pull the latest `mwgg_igdb` index + world releases into the venv without
recreating the app services, re-run just the upgrader:

```bash
docker compose up mwgg_upgrader      # re-runs the populate/refresh, then exits
# or, without leaving a stopped container behind:
docker compose run --rm mwgg_upgrader
```

Each run checks every world and its dependencies for updates and applies them;
packages already current are left untouched (nothing is force-reinstalled). A
full `docker compose up -d` also re-runs it (the app services wait for it via
`service_completed_successfully`).

## Troubleshooting

- **World installs are slow on first boot.** Expected — `mwgg_upgrader`
  fetches ~200 wheels from GitHub release assets and blocks the app services
  until it finishes. Re-running it re-checks every world and its dependencies
  for updates and upgrades only what's outdated (no force-reinstall), so most
  of the time is spent on network round-trips rather than installs.
- **`Read-only file system` / venv write errors in `multiworld` or `web`.**
  Expected and harmless: those services mount the venv read-only and run with
  `SKIP_ALL_INSTALLS=1`; only `mwgg_upgrader` may write it. If a world is
  genuinely missing, re-run `mwgg_upgrader` — don't loosen the mount.
- **`gunicorn: HaltServer 'Worker failed to boot.'`** — `web` no longer
  installs anything; `preload_app = True` only imports the app in the master
  before forking workers. A worker boot error is usually downstream of a master
  import failure — check the master's logs immediately above it.
- **`AttributeError: 'str' object has no attribute 'exists'` from
  ModuleUpdate.** Should be fixed; if you see it, a caller is adding a string
  to `ModuleUpdate.requirements_files` instead of a `pathlib.Path`. Grep for
  `requirements_files.add` / `requirements_files.update`.
- **Bind mount permission errors (`PermissionError: '/root/.local/share/...'`).**
  The container runs as root by default. If you've reconfigured to run as a
  non-root user, adjust the host `chown` accordingly.
