# GitHub Actions Workflows

This directory contains automated workflows for building, testing, and releasing MultiworldGG.

## Workflows

### 1. CI Workflow (`ci.yml`)

**Triggers:**
- Push to `main` branch
- Pull requests to `main` branch

**What it does:**
1. **Builds core components** (only when changed):
   - Splashscreen package (`src/splashscreen`) → commits to `default_wheels/`
   - GUI package (`src/gui`) → commits to `default_wheels/`
   - Base worlds package (namespace files from `src/worlds/*.py`) → copies to `src/world_build_setuptools/src/worlds/` → builds → commits to `default_worlds/`

2. **Detects new worlds:**
   - Scans for new directories in `src/worlds/`
   - Runs `create_world_files` script (which handles file existence checks)
   - Commits the generated template files with a note about manual string replacement

3. **Builds changed worlds:**
   - Detects which world packages have changed
   - Rebuilds only those worlds using `tools/build_wheels.py`
   - Uploads to private PyPI (main branch only)

**Artifacts:**
- Core component wheels committed to repo (indefinite)
- `world-wheels` (30 days, also on PyPI)

### 2. Game Index Workflow (`game-index.yml`)

**Triggers:**
- Manual dispatch (can rebuild all or detect changes)
- Push to `main` affecting `src/game_index/` or `src/tools/game_indexing/`
- After CI workflow completes (for new worlds)

**What it does:**
1. Runs `igdb.py` (which internally calls game index generation)
2. Builds game index wheels
3. Commits wheels to `default_wheels/`

**Artifacts:**
- Game index wheels committed to repo (indefinite)

### 3. Release Workflow (`build-release-test.yml`)

**Triggers:**
- Manual dispatch with version input
- Git tag push (e.g., `v0.1.0`)

**What it does:**
1. **Build executables** on Windows, Linux, and macOS
   - Creates fresh virtual environment
   - Runs `python src/build_exe.py`

2. **Build platform packages:**
   - Linux: AppImage (`setup.py bdist_appimage`)
   - macOS: App bundle/DMG (`setup.py bdist_mac`)
   - Windows: Installer (`inno_setup.iss` via InnoSetup)

3. **Create GitHub Release:**
   - Collects all artifacts
   - Creates release as "MultiworldGG-Test" with download links
   - Marks as pre-release (alpha)

**Artifacts:**
- `windows-exe`, `linux-exe`, `macos-exe` (90 days)
- `linux-appimage` (90 days)
- `macos-bundle` (90 days)
- `windows-installer` (90 days)

## Required Secrets

Set these in repository settings → Secrets and variables → Actions:

### Secrets
- `PYPI_TOKEN`: Authentication token for private PyPI server

### Variables
- `PYPI_URL`: URL of your private PyPI server (e.g., `https://pypi.example.com/simple`)

## Usage

### For Development (CI)

Push to `main` branch:
```bash
git add .
git commit -m "feat: add new world or feature"
git push origin main
```

The CI workflow will automatically:
- Build changed components
- Detect and setup new worlds
- Upload to PyPI

### For New Worlds

1. Create a new directory in `src/worlds/your_world/`
2. Add your world code
3. Push to `main`
4. CI will auto-generate template files and commit them
5. **Manual action required**: Edit the generated files to replace placeholders:
   - Update `pyproject.toml` with correct metadata
   - Update `archipelago.json` with game info
   - Update `Register.py` with world class name

### For Releases

#### Via Git Tag:
```bash
git tag 0.1.0
git push origin 0.1.0
```

#### Via Manual Dispatch:
1. Go to Actions → Release - Build Distributables
2. Click "Run workflow"
3. Enter version (e.g., `0.1.0`)
4. Choose whether to create GitHub release
5. Click "Run workflow"

### For Game Index Rebuild

#### Manual:
1. Go to Actions → Game Index - Rebuild Indexes
2. Click "Run workflow"
3. Check "Rebuild all game indexes" if needed
4. Click "Run workflow"

#### Automatic:
- Runs automatically when new worlds are added
- Runs when game index code is modified

## Error Handling

All workflows use `continue-on-error: true` for non-critical jobs, so:
- Build failures will be reported but won't block other jobs
- Check the Actions tab for detailed logs
- Failed builds are highlighted but don't fail the entire workflow

## Notes

- All workflows use Python 3.12
- Virtual environment is created fresh for each job
- Artifacts have retention periods (30-90 days)
- Release artifacts are kept indefinitely when attached to releases
- New world detection requires manual string replacement (future enhancement: automate this)

