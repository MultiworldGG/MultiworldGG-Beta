# CI/CD Design Specification

## Overview

MultiworldGG's build pipeline produces three things:

1. **Infra wheels** committed back to the repo (`default_wheels/`, `worlds_wheels/`) on each push.
2. **Per-platform distributables** (Windows installer, Linux AppImage, macOS .app) on each tagged
   release.
3. **Two docker images** — the webhost (`ghcr.io/<owner>/<repo>`) and the GitHub-bot service
   (`ghcr.io/<owner>/mwgg-github-bot`) — on each push to `main` (as `:nightly`) and on version tags
   (as `:latest` + semver). See "Docker images" below.

Per-game worlds **are not built here**. Each game's upstream repo publishes itself via
`MultiworldGG/gen-pymod-release`, which opens a PR against `lallaria/MultiworldGG-Index`
with a `module_location` pointing at an immutable `module-install/<world_version>` tag on the
upstream repo. The monorepo's runtime (`ModuleUpdate.install_worlds`) fetches these URLs into
`mwgg_venv` at first run.

## Pipeline architecture

```
┌──────────┐
│ src/     │─┐
└──────────┘ │
             │ push                ┌────────────┐
             ├────────────────────▶│ ci.yml     │   builds infra wheels, commits back to repo
             │                     └────────────┘
             │
             │ push main / tag     ┌────────────────────────────────────────┐
             ├────────────────────▶│ docker.yml: builds + pushes to GHCR    │
             │                     │   ghcr.io/<owner>/<repo>               │  webhost
             │                     │   ghcr.io/<owner>/mwgg-github-bot      │  Probot bot
             │                     └────────────────────────────────────────┘
             │
             │ tag push            ┌──────────────────────────────────────────────────────────────────┐
             └────────────────────▶│ release.yml: fresh venv per OS → install wheels → build_exe.py   │
                                   │              → setup.py bdist_* / inno_setup.iss → GH release    │
                                   └──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────┐  workflow_run.completed  ┌──────────────────────────────┐
│ <upstream world repo>            │─────────────────────────▶│ mwgg-github-bot (Probot)     │
│ make_pyproject.yml runs:         │                          │ Oliver: opens Index PR       │
│   force-push module-install/<ver>│                          │ Karen: writes manifest       │
│   tag                            │                          │         + branch on Index    │
└──────────────────────────────────┘                          └──────────────┬───────────────┘
                                                                             │ PR
                                                                             ▼
                                                              ┌──────────────────────────────┐
                                                              │ lallaria/MultiworldGG-Index  │
                                                              │ karen-pr-review.yml checks   │
                                                              │ daily-release.yml cron       │
                                                              │   rebuilds 4 orphan branches │
                                                              │   as mwgg_igdb               │
                                                              └──────────────┬───────────────┘
                                                                             │ git+https
                                                                             ▼
                                                              ┌──────────────────────────────┐
                                                              │ mwgg_venv (runtime)          │
                                                              │ ModuleUpdate.update          │
                                                              └──────────────────────────────┘
```

## What's in this repo

- **Infra worlds** (`worlds/_bizhawk`, `_debug`, `_manual`, `_sni`, `_tracker`, `generic`) — bundled
  in the frozen build.
- **Namespace files** (`worlds/__init__.py`, `AutoWorld.py`, `Files.py`, `LauncherComponents.py`) —
  the shared API every per-game world consumes; bundled in frozen.
- **Build infrastructure** — `build_exe.py`, `setup.py`, `world_build_setuptools/`, `inno_setup.iss`,
  `tools/build_wheels.py`.
- **Server / generator / patcher** — Python services in the frozen bundle.
- **Webhost** — separate Flask app in `WebHostLib/`, packaged into the `ghcr.io/<owner>/<repo>` docker image.
- **GitHub bot service** (`GitHubLib/`) — Probot/TypeScript service that runs the Oliver and Karen
  GitHub Apps in one container. Image built by `docker.yml`'s `build-bot` job, deployed via
  `deploy/docker-compose.yml`'s `mwgg-github-bot` service.

## What's not in this repo

- Per-game world source code (lives in each upstream repo).
- Game index data (`game_index/`, `tools/game_indexing/` — moved to `lallaria/MultiworldGG-Index`'s
  `scripts/`).

## Docker images

`docker.yml` builds two multi-arch (amd64 + arm64) images and pushes to GHCR:

| Image | Built from | Run by |
|---|---|---|
| `ghcr.io/<owner>/<repo>` | `./Dockerfile` | `deploy/docker-compose.yml` services `multiworld` + `web` (Flask app via gunicorn, generator/server processes) |
| `ghcr.io/<owner>/mwgg-github-bot` | `./GitHubLib/Dockerfile` | `deploy/docker-compose.yml` service `mwgg-github-bot` (Probot/Oliver+Karen) |

**Tag scheme** (both images): `:nightly` on every push to `main`; `{major}.{minor}.{patch}`,
`{major}.{minor}`, and `:latest` on each `v?.?.?` tag.

**Operator workflow:** `docker compose pull && docker compose up -d` to deploy the published images.
**Dev workflow:** `docker compose build && docker compose up -d` to rebuild locally from source.
The image refs in `docker-compose.yml` are env-overridable (`MULTIWORLD_IMAGE`,
`MWGG_GITHUB_BOT_IMAGE`) for operators on forks or with non-`lallaria` registries.

## Branch model

- **Development branch** — current focus of CI.
- **`main`** — release target; tags here trigger `release.yml`. `docker.yml` also fires on every
  push to `main` (publishing `:nightly`) and on version tags (publishing `:latest` + semver).
- Long-running feature branches OK; CI runs on PR to dev branch.

## GitHub bot service

The GitHub-bot image (`mwgg-github-bot`) runs two GitHub Apps inside one Probot/TypeScript process
under `GitHubLib/`. Authoritative operator runbook lives at `GitHubLib/README.md`; this section
gives the architectural overview.

- **Two Apps, one process.** **Oliver** receives `workflow_run.completed` webhooks from per-world
  repos; **Karen** does branch + manifest writes on the Index. Both authenticate via app-level JWT
  → installation token inside `GitHubLib/src/index.ts`. The split exists so per-world repos see a
  read-shaped install prompt; Oliver has no write permissions on the Index, only Karen does.
- **Trigger contract.** Oliver only acts on workflows named `Create and Release Python Package`
  with `event=release` and `conclusion=success`. The per-world repo must set the
  `WORLD_FOLDER_NAME` repository variable; the bot uses it as the slug for `worlds/<slug>.json`.
- **PR shape.** Branch `update/<slug>-<release_tag>`, manifest sets
  `module_location = git+https://github.com/<owner>/<repo>.git@<wheel_sha>`, label `New APWorld` or
  `APWorld Update`. CODEOWNERS gets a line appended for new worlds.
- **Image build.** `docker.yml` jobs `prepare-bot` → `build-bot` (matrix amd64 + arm64) →
  `manifest-bot` push to `ghcr.io/<owner>/mwgg-github-bot`. Multi-arch manifest stitched in
  `manifest-bot`. Triggers: push to `main` (`:nightly`), version tags (`:latest` + semver).
- **Deploy footprint.** `deploy/docker-compose.yml` service `mwgg-github-bot` exposes only loopback
  `127.0.0.1:3000`; host-side nginx (`deploy/example_github-bot_nginx.conf`) terminates TLS and
  runs `deploy/github-bot-nginx-njs/hmac.js` to validate `X-Hub-Signature-256` at the edge before
  proxying. Probot validates HMAC again inside the container (defense-in-depth). State (event
  JSONL) lives in the `mwgg_github_bot_state` named volume mounted at `/var/lib/oliver`.
- **Runtime.** Node 22 LTS, Probot 13, TypeScript compiled to `dist/`.

## Runtime contract

The frozen exe ships with an empty `worlds/` directory under `lib/` apart from infra. On first run
(via `inno_setup.iss [Run]` step or `MultiWorld --update-modules --worlds <selection>`):

1. Inno Setup hands the user's selected variant + slug list to `MultiWorld.py:--update-modules`.
2. `MultiWorld.py` calls `ModuleUpdate.install_worlds(worlds=<list>)`.
3. `install_worlds` partitions the list:
   - Variant token (`mwgg_igdb_<variant>`) → switches `MWGG_IGDB_VARIANT`, installs the orphan
     branch package via `install_mwgg_igdb(upgrade=True)`.
   - `worlds.<slug>` entries → resolves each slug's `module_location` from `GameIndex.get_all_games()`
     and pip-installs into `mwgg_venv/Lib/site-packages/worlds/<slug>/`.
4. Subsequent launches load the slug list explicitly via `Utils.set_game_names()` before any
   `import worlds` — which forces the narrow loader to populate only the requested slugs (and not
   every world the index knows about).

## Failure modes and recovery

| Symptom | Cause | Recovery |
|---------|-------|----------|
| `pip install` fails on a `module_location` URL | Upstream hasn't published a real tag yet (`module_location` still points at `worlds-mirror` placeholder) | Wait for upstream's gen-pymod-release run. |
| Variant install fails | `lallaria/MultiworldGG-Index` orphan branch unreachable (private repo + no auth) | Make repo public or add PAT-based auth in `MWGG_IGDB_GIT_URL`. |
| Frozen build's `lib/worlds/` missing namespace files | `worlds/*.py` not packaged by cx_Freeze | Verify `setup.py` has `"packages": ["worlds", ...]`. |
| `AutoWorldRegister.world_types` empty | `set_game_names()` not called before first `import worlds` | Audit the entry-point script; add `set_game_names()` before any `from worlds import` cascade. |
| `workflow_run.completed` arrives but no PR on Index | Per-world repo missing `WORLD_FOLDER_NAME` repo variable, or workflow name not `Create and Release Python Package` | Check `/status` on the bot host; set the variable per `GitHubLib/README.md`. |
| Bot rejects webhook with 401 at edge | `X-Hub-Signature-256` mismatch — webhook secret on GitHub App side ≠ `/etc/github-bot/webhook_secret` | Re-sync the secret; both njs and Probot read the same value. |
| PR opens but Karen never lands the manifest | Karen App not installed on the Index, or `KAREN_PRIVATE_KEY` mounted wrong | Verify Index install + secrets bind-mount in `deploy/docker-compose.yml`. |

## Why per-game worlds left the monorepo

Pre-split, every world subclassed `World` and was registered via `AutoWorldRegister` metaclass at
import time. With ~229 worlds in-tree, every launch loaded ~2 GB of world code. The split:

- Pulls each world out of the monorepo to its own upstream repo.
- Lets each world version and release independently.
- At runtime, only loads the slugs the user actually selected for the current generation.
- Reduces resident memory by orders of magnitude.

## Migration history

The split is implemented in phases (see `lallaria/MultiworldGG-Index` repo for full record). Phase 4
(this repo's cutover from `pypi.multiworld.gg` to `mwgg_igdb`) is in progress; end-to-end runtime
testing is gated on each upstream world's first published tag.
