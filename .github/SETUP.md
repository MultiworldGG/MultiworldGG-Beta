# GitHub Actions Setup

Most workflows in this repo run with no extra setup beyond a vanilla GitHub repo.

## Permissions

Settings → Actions → General → Workflow permissions:

- ✅ **Read and write permissions** — required for `ci.yml`'s auto-commit of infra wheels back
  into `default_wheels/` and `worlds_wheels/`.
- ✅ **Allow GitHub Actions to create and approve pull requests** — currently unused but reserved
  for any future bot-driven PR flow.

## Secrets / variables

None required for `ci.yml` or `release.yml`. Per-game worlds are not published from this repo, so
no PyPI credentials are needed here. (Webhost deployment uses its own secrets — documented in the
webhost deploy configs.)

If you fork the repo and want CI to run on your branch, no further setup is needed: pushing to the
development branch triggers the wheel-build jobs; pushing a tag to `main` triggers `release.yml`.

## Testing the pipeline

```bash
# Trigger CI: edit any worlds/_*/file or worlds/*.py and push.
git commit -am "test: trigger CI"
git push

# Trigger release dry-run via Actions tab → "Build Release Test" → Run workflow.
# Or tag a version on main:
git tag v0.0.1-test
git push origin v0.0.1-test
```

## Troubleshooting

| Issue | Likely cause |
|-------|--------------|
| `ci.yml` doesn't fire | Only listens on the development branch; check `on:` block. |
| `build-base-worlds` doesn't run | Only triggers on `worlds/*.py` (namespace files) changes. |
| Auto-commit fails | Repo permissions: enable "Read and write permissions". |
| Frozen build fails | Most likely a stale `default_wheels/` or `worlds_wheels/` artifact — re-run the matching CI job to refresh. |
