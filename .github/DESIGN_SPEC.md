# GitHub Actions Workflows - Design Specification

## Overview

This document describes the automated CI/CD pipeline for MultiworldGG, an alpha-stage project with a main-branch-only workflow.

## Project Context

- **Stage**: Alpha development
- **Branch Strategy**: gui-changes branch for development (will migrate to main later)
- **Python Version**: 3.12
- **Build System**: Python build (setuptools), cx_Freeze for executables
- **Distribution**: Private PyPI server for wheels, Github for executables
- **Repository Structure**: Repository root is the project source (no src/ prefix in paths)

## Workflow Architecture

### 1. CI Workflow (`ci.yml`)

**Purpose**: Continuous integration for core components and world packages

**Triggers**:
- Push to `gui-changes` branch
- Pull requests to `gui-changes` branch

**Jobs**:

#### Job 1: `build-splashscreen`
- **Runs only when**: `splashscreen/**` changes
- Builds `splashscreen` package using Python build
- Commits wheel to `default_wheels/` directory
- Uses `github-actions[bot]` for commits
- Runs on: Ubuntu latest

#### Job 2: `build-gui`
- **Runs only when**: `gui/**` changes
- Builds `gui` package using Python build
- Commits wheel to `default_wheels/` directory
- Uses `github-actions[bot]` for commits
- Runs on: Ubuntu latest

#### Job 3: `build-base-worlds`
- **Runs only when**: `worlds/*.py` changes
- Copies `worlds/*.py` into `world_build_setuptools/src/worlds/*.py`
- Builds `worlds` package using Python Build  
- This is the namespace package that all world packages depend on
- Commits wheel to `default_worlds/` directory
- Uses `github-actions[bot]` for commits
- Runs on: Ubuntu latest

#### Job 4: `check-new-worlds`
- Detects new world directories in `worlds/` using git diff
- For each new world directory (the script will ignore if it has the files):
  - Runs `python tools/add_required_world_files.py <world_name>`
  - Creates `pyproject.toml`, `archipelago.json`, `Register.py` from templates
- **Creates and pushes a commit** with the generated files
- Commit message includes warning about manual string replacement needed
- Outputs list of new worlds for dependent jobs
- Uses `github-actions[bot]` for commits

**Detection Logic**:
```
- Compare HEAD vs HEAD~1
- Find new directories in worlds/
- Skip directories starting with _ (e.g., _bizhawk, _sni)
- Skip 'generic' directory (template source)
```

#### Job 5: `build-changed-worlds`
- **Runs only on**: Push to gui-changes (not PRs)
- Always runs regardless of previous job status
- Detects changed worlds using git diff on `worlds/*/`
- Creates virtual environment (isolated from system)
- Runs `python tools/build_wheels.py --world <comma,separated,list>`
- Uploads wheels to private PyPI using twine
- Uses `--skip-existing` to avoid conflicts
- Uploads artifacts (30-day retention)
- **Continues on error**: Won't fail the entire workflow

**PyPI Upload**:
```yaml
Environment:
  TWINE_USERNAME: __token__
  TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
  TWINE_REPOSITORY_URL: ${{ vars.PYPI_URL }}

Command:
  python -m twine upload --skip-existing dist/worlds_*.whl dist/worlds_*.tar.gz
```

---

### 2. Game Index Workflow (`game-index.yml`)

**Purpose**: Rebuild and publish game index packages

**Triggers**:
- **Manual dispatch**: Can optionally rebuild all indexes
- **Push to gui-changes**: When `game_index/**` or `tools/game_indexing/**` changes
- **Workflow run**: After CI workflow completes (catches new worlds)

**Jobs**:

#### Job 1: `rebuild-game-indexes`
- Single job, continues on error
- Detects if rebuild needed based on trigger type
- Creates virtual environment
- Installs dependencies from `tools/game_indexing/requirements.txt`
- Runs `python tools/game_indexing/igdb.py`
- Finds all game index modules with `pyproject.toml`
- Builds wheels for each module
- Uploads to private PyPI
- Commits wheel to `default_wheels/` directory
- Uses `github-actions[bot]` for commits
- Runs on: Ubuntu latest

**Detection Logic**:
```
If workflow_dispatch with rebuild_all=true: rebuild all
If workflow_run (triggered by CI): rebuild all
If push event: check git diff for game_index/ or tools/game_indexing/ changes
```

**Build Process**:
```bash
for each module in game_index/*/pyproject.toml:
  cd game_index/$module
  python -m build
  upload to PyPI
```

---

### 3. Release Workflow (`release.yml`)

**Purpose**: Build platform-specific distributables and create releases

**Triggers**:
- **Manual dispatch**: Requires version input (e.g., "v0.1.0")
- **Git tag push**: Any tag matching `v*` pattern

**Jobs**:

#### Job 1: `build-exe` (Matrix Build)
- Runs on: Windows, Linux, macOS (parallel)
- Creates **fresh virtual environment** (critical for clean builds)
- Installs from `build_requirements.txt`
- Runs `python build_exe.py`
- Outputs to `build/` directory
- Uploads platform-specific artifacts (90-day retention)
- Continues on error (won't block other platforms)

**Matrix Configuration**:
```yaml
windows-latest → windows-exe artifact
ubuntu-latest  → linux-exe artifact
macos-latest   → macos-exe artifact
```

#### Job 2: `build-linux-appimage`
- **Depends on**: `build-exe` completion
- Downloads linux-exe artifact
- Runs `python setup.py bdist_appimage`
- Uploads AppImage (90-day retention)
- Continues on error

#### Job 3: `build-mac-bundle`
- **Depends on**: `build-exe` completion
- Downloads macos-exe artifact
- Runs `python setup.py bdist_mac`
- Uploads .app/.dmg files (90-day retention)
- Continues on error

#### Job 4: `build-windows-installer`
- **Depends on**: `build-exe` completion
- Downloads windows-exe artifact
- Installs InnoSetup via Chocolatey
- Runs `iscc inno_setup.iss`
- Uploads installer to `setups/` (90-day retention)
- Continues on error

#### Job 5: `create-release`
- **Depends on**: All build jobs (runs even if some fail)
- **Runs only if**: Tag push OR manual dispatch with create_release=true
- Downloads all artifacts
- Creates release notes from template
- Creates GitHub release:
  - Tag: Input version or git tag
  - Name: MultiworldGG-Test <version>
  - Status: Pre-release (alpha)
  - Attaches all artifacts
- Uses `softprops/action-gh-release@v2`

**Release Notes Template**:
- Download instructions per platform
- Installation guides
- Alpha warning
- Manual action reminder for new worlds

---

## Configuration Requirements

### Repository Secrets (Settings → Secrets and variables → Actions)

| Name | Description | Example |
|------|-------------|---------|
| `PYPI_TOKEN` | Private PyPI authentication token | `pypi-AgEIcHlwaS...` |

### Repository Variables

| Name | Description | Example |
|------|-------------|---------|
| `PYPI_URL` | Private PyPI server URL | `https://pypi.example.com/simple` |

### Repository Permissions

**Required Settings** (Settings → Actions → General):
- ✅ Workflow permissions: **Read and write permissions**
- ✅ Allow GitHub Actions to create and approve pull requests

This is required for the auto-commit feature in new world detection.

---

## Artifact Strategy

### Retention Periods

| Artifact Type | Storage Location | Retention | Rationale |
|--------------|------------------|-----------|-----------|
| Component wheels (GUI, splash, base worlds) | Committed to repo | Indefinite | Version controlled in default_wheels/ or default_worlds/ |
| World wheels | Private PyPI + artifact | 30 days | Published to PyPI (permanent), artifacts for debugging |
| Game index wheels | Private PyPI + artifact | 30 days | Published to PyPI, artifacts for rollback |
| Game index data (JSON) | Artifact only | 90 days | Historical data for analysis |
| Executables | Artifact only | 90 days | Longer retention for testing |
| Platform packages (AppImage, DMG, installer) | Artifact only | 90 days | Release candidates |
| Release attachments | GitHub Release | Indefinite | Attached to GitHub releases |

---

## Error Handling Philosophy

### Continue-on-Error Strategy

All jobs use `continue-on-error: true` where appropriate:

**Rationale**: 
- Alpha stage - individual failures shouldn't block entire pipeline
- Platform-specific issues shouldn't prevent other platforms from building
- Developers need visibility into what succeeded vs. failed

**Implementation**:
- Build failures are logged but don't fail workflow
- GitHub Actions shows warnings for failed steps
- Artifacts are uploaded only for successful builds
- Release job runs even if some build jobs fail

### Failure Scenarios

| Scenario | Behavior | Action Required |
|----------|----------|-----------------|
| World build fails | Warning logged, other worlds continue | Review logs, fix world |
| Windows build fails | Linux/Mac continue | Check Windows-specific issue |
| PyPI upload fails | Logged, artifacts still uploaded | Check token/connectivity |
| InnoSetup fails | Release created without installer | Check setup.iss syntax |
| New world detection false positive | Manual cleanup needed | Review/revert commit |

---

## Build Optimization

### Caching Strategy

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: ${{ env.PYTHON_VERSION }}
    cache: 'pip'  # Caches pip packages based on requirements files
```

**Benefits**:
- Faster dependency installation
- Reduced bandwidth usage
- Consistent package versions within workflow run

### Virtual Environment Isolation

All workflows create fresh virtual environments:
```bash
python -m venv venv
source venv/bin/activate  # or venv/Scripts/activate on Windows
```

**Rationale**:
- Prevents system package conflicts
- Ensures reproducible builds
- Matches user's memory preference (ID: 6896947)

---

## New World Workflow

### Developer Perspective

1. **Developer creates new world**:
   ```bash
   mkdir worlds/my_new_world
   # Add world code
   git add worlds/my_new_world
   git commit -m "feat: add my new world"
   git push origin gui-changes
   ```

2. **CI detects new world**:
   - Runs template generation
   - Creates commit with files

3. **Developer receives notification**:
   - Commit from `github-actions[bot]`
   - Commit message warns about manual action needed

4. **Developer edits templates**:
   ```bash
   git pull origin gui-changes
   # Edit worlds/my_new_world/pyproject.toml
   # Edit worlds/my_new_world/archipelago.json
   # Edit worlds/my_new_world/Register.py
   git commit -m "fix: configure my_new_world templates"
   git push origin gui-changes
   ```

5. **CI builds the world**:
   - Detects changes to world directory
   - Builds and publishes wheel

### Future Enhancement

**Consideration**: Automate string replacement in templates
- Could use world directory name for class names
- Could parse existing `__init__.py` for metadata
- Would require heuristics or additional metadata file
- Marked as "eventual feature" per requirements

---

## Game Index Trigger Logic

### Automatic Triggers

1. **New world added** (via workflow_run):
   - CI workflow completes
   - Game index workflow starts
   - Rebuilds all indexes to include new world

2. **Game metadata changed**:
   - Developer updates `archipelago.json` with IGDB ID
   - Game index workflow detects change
   - Rebuilds affected indexes

3. **Indexing code changed**:
   - Developer updates `tools/game_indexing/`
   - Game index workflow rebuilds all

### Manual Trigger

Use when:
- Upstream game database updated
- Need to regenerate without code changes
- Testing index generation

---

## Release Process

### Automated (Tag-based)

```bash
# Create and push tag
git tag v0.1.0
git push origin v0.1.0

# Workflow automatically:
# 1. Builds all platforms
# 2. Creates installers/packages
# 3. Creates GitHub release
# 4. Attaches all artifacts
```

### Manual (Workflow Dispatch)

1. Go to Actions → Release - Build Distributables
2. Click "Run workflow"
3. Enter version: `v0.1.0`
4. Choose whether to create release
5. Run workflow

**Use manual when**:
- Testing builds without release
- Creating release from non-tag commit
- Re-running failed release build

---

## Platform-Specific Notes

### Windows
- Uses PowerShell for scripts
- InnoSetup installed via Chocolatey
- Virtual environment: `venv/Scripts/activate`
- Executable: `MultiworldGG.exe`

### Linux
- Uses bash for scripts
- AppImage requires executable permissions
- Virtual environment: `venv/bin/activate`
- Executable: `MultiworldGG`

### macOS
- Uses bash for scripts
- Creates .app bundle and/or .dmg
- Virtual environment: `venv/bin/activate`
- May require code signing (not implemented)

---

## Security Considerations

1. **Secret Management**:
   - PyPI token stored as repository secret
   - Never logged or exposed in workflow output
   - Twine automatically redacts credentials

2. **Permissions**:
   - Workflows have write access for commits
   - Limited to gui-changes branch operations
   - No force pushes or tag deletions

3. **Dependency Security**:
   - All dependencies pinned in requirements files
   - Consider adding dependabot for updates
   - Review dependency changes in PRs

4. **Artifact Security**:
   - Artifacts accessible only to repo collaborators
   - Release assets public (alpha product)
   - No secrets in build outputs

---

## Monitoring and Debugging

### Workflow Status

Check: Repository → Actions tab

- Green checkmark: Success
- Yellow dot: In progress
- Red X: Failed (but continue-on-error may show as warning)
- Orange exclamation: Warnings

### Common Issues

| Issue | Check | Solution |
|-------|-------|----------|
| Workflow doesn't trigger | Trigger conditions | Verify branch name, file paths |
| PyPI upload fails | Secret/variable values | Re-check PYPI_TOKEN and PYPI_URL |
| Build fails on specific OS | Platform-specific logs | Check OS-specific dependencies |
| New world not detected | Git history | May need 2+ commits in repo |
| Auto-commit fails | Repository permissions | Enable write permissions |

### Debug Tips

1. **Enable debug logging**:
   - Settings → Secrets → Add `ACTIONS_STEP_DEBUG` = `true`

2. **Check artifact contents**:
   - Download artifacts from workflow run
   - Inspect file structure

3. **Test locally**:
   - Run same commands in local venv
   - Compare output with workflow logs

4. **Review git diff**:
   - Check what workflow detected
   - Verify file path patterns

---

## Future Enhancements

### Potential Improvements

1. **Automated Template Strings**:
   - Parse world directory for metadata
   - Auto-populate class names, game titles
   - Reduce manual intervention

2. **Branch Protection**:
   - Require CI checks to pass
   - Add PR review requirements
   - Block direct pushes (use PRs)

3. **Multi-Branch Strategy**:
   - Development branch
   - Release branches
   - Feature branches with PR workflow

4. **Enhanced Testing**:
   - Add pytest step before builds
   - Linter checks (ruff, mypy)
   - Integration tests

5. **Notification Integration**:
   - Slack/Discord notifications
   - Email alerts for failures
   - Status badges in README

6. **Caching Improvements**:
   - Cache built wheels
   - Cache cx_Freeze builds
   - Reduce build times

7. **Staged Deployments**:
   - Staging PyPI server
   - Beta release channel
   - Gradual rollouts

---

## Compliance with User Requirements

### User Rules Adherence

✅ **Experience Level**: Minimal explanations, direct implementation  
✅ **Don't Guess**: All logic based on existing code structure  
✅ **Split Responses**: Design spec separate from implementation  
✅ **Python 3.12**: Hardcoded in workflows  

### Memory Alignment

✅ **Memory 7245250**: Base worlds excluded from executable (handled by build_exe.py)  
✅ **Memory 7245238**: List problems, start with likely issues (continue-on-error strategy)  
✅ **Memory 6896959**: No speculation (all based on existing scripts)  
✅ **Memory 6896947**: Use venv for commands (all workflows create venv)  

---

## Conclusion

This workflow design provides:
- **Automation**: Minimal manual intervention for common tasks
- **Flexibility**: Manual triggers for edge cases
- **Resilience**: Errors don't cascade through pipeline
- **Visibility**: Clear artifact outputs and logging
- **Scalability**: Can handle additional worlds and indexes

The alpha-stage philosophy (main-branch-only, continue-on-error, pre-release tags) allows rapid iteration while establishing CI/CD foundation for future stable releases.

