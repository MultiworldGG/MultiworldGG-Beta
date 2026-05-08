# GitHub Actions Workflows

Automated build/test/release pipelines for MultiworldGG.

## Distribution model

Per-game worlds **are not built or published from this repo**. Each game lives in its own upstream
repo and publishes itself via [`MultiworldGG/gen-pymod-release`], which:

1. Force-pushes a `module-install/<world_version>` tag on the upstream world repo.
2. Opens a PR against [`lallaria/MultiworldGG-Index`] updating that game's manifest with the new
   `module_location` URL.

Karen-bot reviews each PR (schema, security checks); on merge, the daily-release cron rebuilds the
four orphan branches (`game_index_{nr,ao,sixteen,twelve}`) as the consumable `mwgg_igdb` package.

The monorepo bundles only **infra worlds** (`worlds/_*`, `worlds/generic/`) plus the namespace
files (`worlds/{__init__,AutoWorld,Files,LauncherComponents}.py`). Per-game worlds are pip-installed
at runtime by `ModuleUpdate.install_worlds()` from each manifest's `module_location`.

[`MultiworldGG/gen-pymod-release`]: https://github.com/MultiworldGG/gen-pymod-release
[`lallaria/MultiworldGG-Index`]: https://github.com/lallaria/MultiworldGG-Index

## Workflows

### `ci.yml` — CI (build + commit infra wheels)

Triggers on push and PR against the development branch. Four jobs:

- **`build-splashscreen`** — when `splashscreen/**` changes, builds and commits the wheel to `default_wheels/`.
- **`build-gui`** — when `gui/**` changes, builds and commits the wheel to `default_wheels/`.
- **`build-base-worlds`** — when `worlds/*.py` changes, builds the namespace wheel from those
  files and commits to `worlds_wheels/`.
- **`build-default-worlds`** — when any `worlds/_*` or `worlds/generic/` changes, builds those
  infra wheels via `tools/build_wheels.py` and commits to `worlds_wheels/`.

All jobs commit as `github-actions[bot]` and rebase before pushing.

### `release.yml` / `build-release-test.yml` — release / dry-run

Triggered by tag push (`release.yml`) or manual dispatch (`build-release-test.yml`). Builds platform
distributables (Windows installer via Inno Setup, Linux AppImage, macOS .app) by:

1. Creating a fresh venv per OS.
2. Installing `default_wheels/*.whl` and `worlds_wheels/*.whl` into the venv.
3. Running `python build_exe.py`.
4. Packaging via `setup.py bdist_appimage` / `bdist_mac` / Inno Setup.
5. Uploading per-platform artifacts (90-day retention).

Frozen builds ship without per-game worlds; users select and pip-install them on first run via the
installer's `--worlds <selection>` flow (see `inno_setup.iss`).

### Other workflows

- **`build.yml`** — legacy build path (kept for fallback testing).
- **`analyze-modified-files.yml`** — lints PR diffs.
- **`unittests.yml`** — runs the test suite.
- **`ctest.yml`** — runs C/Cython speedup tests.
- **`codeql-analysis.yml`** / **`scan-build.yml`** — security and static analysis.
- **`strict-type-check.yml`** — pyright/mypy on changed files.
- **`docker.yml`** — webhost docker image.

## Required secrets / variables

None for `ci.yml` or `release.yml` — all build artifacts ship with the repo or get installed from
the public Index repo orphan branches. (Webhost-only secrets, e.g. database creds, are documented
in webhost deployment configs, not here.)

## Common failure modes

- **`build-base-worlds` doesn't trigger** — only fires when `worlds/*.py` (top-level namespace
  files) change. Per-game worlds in `worlds/<slug>/` no longer live in this repo, so changes there
  are impossible.
- **Frozen build fails to find a world at runtime** — expected if `module_location` for that slug
  is not yet a valid `git+https://...@module-install/<ver>` URL. Each upstream world must publish
  via gen-pymod-release before the monorepo can fetch it.
