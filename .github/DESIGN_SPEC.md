# CI/CD Design Specification

## Overview

MultiworldGG's build pipeline produces three things:

1. **Infra wheels** committed back to the repo (`default_wheels/`, `worlds_wheels/`) on each push.
2. **Per-platform distributables** (Windows installer, Linux AppImage, macOS .app) on each tagged
   release.
3. **Webhost docker image** on each push to the deploy branch.

Per-game worlds **are not built here**. Each game's upstream repo publishes itself via
`MultiworldGG/build-and-publish-action`, which opens a PR against `lallaria/MultiworldGG-Index`
with a `module_location` pointing at an immutable `module-install/<world_version>` tag on the
upstream repo. The monorepo's runtime (`ModuleUpdate.install_worlds`) fetches these URLs into
`mwgg_venv` at first run.

## Pipeline architecture

```
┌──────────────────┐  push  ┌────────┐
│ src/             │───────▶│ ci.yml │  builds infra wheels, commits to repo
└──────────────────┘        └────────┘
        │
        │ tag push
        ▼
┌──────────────────┐
│ release.yml      │  fresh venv per OS → install wheels → build_exe.py
│                  │  → setup.py bdist_* / inno_setup.iss → GH release
└──────────────────┘

┌──────────────────────────────────┐    PR     ┌────────────────────────────┐
│ <upstream world repo>            │──────────▶│ lallaria/MultiworldGG-Index│
│ build-and-publish-action runs:   │           │ Greg-bot reviews → merge   │
│   force-push module-install/<ver>│           │ daily-release.yml cron     │
│   tag                            │           │   rebuilds 4 orphan        │
└──────────────────────────────────┘           │   branches as mwgg_igdb    │
                                               └────────────────────────────┘
                                                            │
                                                            │ git+https
                                                            ▼
                                                  ┌──────────────────────┐
                                                  │ mwgg_venv (runtime)  │
                                                  │ ModuleUpdate.update  │
                                                  └──────────────────────┘
```

## What's in this repo

- **Infra worlds** (`worlds/_bizhawk`, `_debug`, `_manual`, `_sni`, `_tracker`, `generic`) — bundled
  in the frozen build.
- **Namespace files** (`worlds/__init__.py`, `AutoWorld.py`, `Files.py`, `LauncherComponents.py`) —
  the shared API every per-game world consumes; bundled in frozen.
- **Build infrastructure** — `build_exe.py`, `setup.py`, `world_build_setuptools/`, `inno_setup.iss`,
  `tools/build_wheels.py`.
- **Server / generator / patcher** — Python services in the frozen bundle.
- **Webhost** — separate Flask app in `WebHostLib/`, deploys from source.

## What's not in this repo

- Per-game world source code (lives in each upstream repo).
- Game index data (`game_index/`, `tools/game_indexing/` — moved to `lallaria/MultiworldGG-Index`'s
  `scripts/`).

## Branch model

- **Development branch** — current focus of CI.
- **`main`** — release target; tags here trigger `release.yml`.
- Long-running feature branches OK; CI runs on PR to dev branch.

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
| `pip install` fails on a `module_location` URL | Upstream hasn't published a real tag yet (`module_location` still points at `worlds-mirror` placeholder) | Wait for upstream's build-and-publish-action run. |
| Variant install fails | `lallaria/MultiworldGG-Index` orphan branch unreachable (private repo + no auth) | Make repo public or add PAT-based auth in `MWGG_IGDB_GIT_URL`. |
| Frozen build's `lib/worlds/` missing namespace files | `worlds/*.py` not packaged by cx_Freeze | Verify `setup.py` has `"packages": ["worlds", ...]`. |
| `AutoWorldRegister.world_types` empty | `set_game_names()` not called before first `import worlds` | Audit the entry-point script; add `set_game_names()` before any `from worlds import` cascade. |

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
