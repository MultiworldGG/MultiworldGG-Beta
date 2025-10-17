# GitHub Actions Setup Guide

This guide walks you through setting up the GitHub Actions workflows for MultiworldGG.

## Prerequisites

- Admin access to the GitHub repository
- Private PyPI server with authentication token
- InnoSetup (handled automatically by workflow for Windows builds)

## Step 1: Configure Repository Secrets

Go to your repository → Settings → Secrets and variables → Actions

### Add Repository Secret

Click "New repository secret" and add:

**Name:** `PYPI_TOKEN`  
**Value:** Your PyPI authentication token (starts with `pypi-` or similar)

Example:
```
pypi-AgEIcHlwaS5vcmcyUzQ...
```

## Step 2: Configure Repository Variables

In the same section, click the "Variables" tab

### Add Repository Variable

Click "New repository variable" and add:

**Name:** `PYPI_URL`  
**Value:** Your private PyPI server URL

Example:
```
https://pypi.yourdomain.com/simple
```

or if using a specific repository:
```
https://pypi.yourdomain.com/legacy/
```

## Step 3: Verify Workflow Permissions

Go to Settings → Actions → General

### Workflow Permissions

Ensure the following are enabled:
- ✅ **Read and write permissions** (allows workflows to commit changes)
- ✅ **Allow GitHub Actions to create and approve pull requests**

This is required for the new world auto-commit feature.

## Step 4: Test the Workflows

### Test CI Workflow

1. Make a small change to any file in `src/`
2. Commit and push to `main`:
   ```bash
   git add .
   git commit -m "test: trigger CI workflow"
   git push origin main
   ```
3. Go to Actions tab and verify the workflow runs

### Test New World Detection

1. Create a new world directory:
   ```bash
   mkdir src/worlds/test_world
   echo "# Test World" > src/worlds/test_world/__init__.py
   git add src/worlds/test_world
   git commit -m "feat: add test world"
   git push origin main
   ```
2. Check Actions tab - CI should detect and create template files
3. You'll see a new commit created by `github-actions[bot]`

### Test Release Workflow (Optional)

1. Go to Actions → Release - Build Distributables
2. Click "Run workflow"
3. Enter version: `v0.0.1-test`
4. Uncheck "Create GitHub release" (for testing)
5. Click "Run workflow"
6. Check the artifacts after completion

## Step 5: Configure PyPI Upload (Optional Tweak)

If your PyPI server uses a different authentication method:

### Edit `.github/workflows/ci.yml` and `.github/workflows/game-index.yml`

Find the "Upload to private PyPI" step and modify as needed:

```yaml
- name: Upload to private PyPI
  env:
    TWINE_USERNAME: __token__  # Change if not using token auth
    TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
    TWINE_REPOSITORY_URL: ${{ vars.PYPI_URL }}
```

For basic auth:
```yaml
env:
  TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
  TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
  TWINE_REPOSITORY_URL: ${{ vars.PYPI_URL }}
```

## Troubleshooting

### Workflow doesn't trigger

**Check:**
- Branch is `main`
- Workflow file is in `.github/workflows/`
- File has `.yml` or `.yaml` extension
- YAML syntax is valid

### PyPI upload fails

**Check:**
- `PYPI_TOKEN` secret is set correctly
- `PYPI_URL` variable is correct
- PyPI server is accessible from GitHub Actions
- Token has upload permissions

**Test manually:**
```bash
pip install twine
twine upload --repository-url $PYPI_URL \
  --username __token__ \
  --password $PYPI_TOKEN \
  dist/*.whl
```

### New world files not committed

**Check:**
- Repository has "Read and write permissions" enabled
- Workflow has write access to repository
- No conflicts with branch protection rules

### Build failures

**Check:**
- Build requirements are up to date
- Dependencies are pinned in requirements files
- Platform-specific issues (check logs for specific OS)

### InnoSetup fails on Windows

**Common issues:**
- `setup.ini` file is missing or malformed
- Paths in `inno_setup.iss` are incorrect
- Build artifacts are in wrong location

## Security Considerations

- **Never commit secrets to the repository**
- PyPI token should have minimal permissions (upload only)
- Consider using environment-specific tokens (staging vs production)
- Review workflow logs carefully - they may contain sensitive paths

## Next Steps

After setup is complete:

1. **Monitor first few runs** - Check logs for any issues
2. **Adjust retention days** - Modify artifact retention if needed
3. **Set up branch protection** - Add required status checks
4. **Configure notifications** - Set up email/Slack for workflow failures
5. **Document internal processes** - Add team-specific notes

## Support

If you encounter issues:

1. Check the Actions tab for detailed logs
2. Review the workflow YAML for typos
3. Verify secrets and variables are set correctly
4. Test builds locally first using the same commands

