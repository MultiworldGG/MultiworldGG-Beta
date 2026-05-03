# Oliver-Multiworld-Squirrel

Webhook receiver for the `Oliver-Multiworld-Squirrel` GitHub App. Listens for `release.published` events on per-world repos, builds the orphan-branch tree in-process, pushes it back to the per-world repo as `module-install/<slug>` + tag `module-install/<slug>/<world_version>`, and opens a corresponding PR on `MultiworldGG-Index`.

## How per-world authors use Oliver

1. Install the **Oliver-Multiworld-Squirrel** GitHub App on the per-world repo (one click, public install page).
2. Cut a GitHub Release. Done.

That's it. No workflow file, no secrets, no PEM. Oliver receives the webhook, figures out which world the release is for via diff-based slug discovery (see `src/slug-discovery.ts`), builds + pushes + opens the Index PR.

If Oliver can't determine the slug (e.g. the release touched multiple `worlds/<slug>/`), it posts a comment on the release **and** opens an Issue on `MultiworldGG-Index` asking maintainers to PR by hand.

## Env vars

| Var | Required | Notes |
|---|---|---|
| `OLIVER_APP_ID` | yes | Numeric App ID from the GitHub App's General settings page. |
| `OLIVER_PRIVATE_KEY` | yes | Full PEM of the App's private key. Newlines may be escaped as `\n`. |
| `OLIVER_WEBHOOK_SECRET` | yes | Webhook secret configured on the App. |
| `OLIVER_INDEX_REPO` | no | `<owner>/<repo>` of the Index. Defaults to `lallaria/MultiworldGG-Index`. |
| `PORT` | no | Bind port. Defaults to `3000`. |

## Local development

```
npm install
npm run build
npm test
```

To run locally against real webhooks during development, use `smee.io` to forward webhooks to `localhost:3000`. The App's webhook URL during development should be the smee channel URL.

## Production deployment

Oliver runs as the `oliver` service in `deploy/docker-compose.yml`. The image is built by `.github/workflows/docker.yml` and published to `ghcr.io/multiworldgg/multiworldgg-oliver`. nginx routes `oliver.multiworld.gg` → `oliver:3000`.

Operator setup on the production host:

```
cp deploy/example_oliver.env deploy/oliver.env
chmod 600 deploy/oliver.env
$EDITOR deploy/oliver.env  # fill in OLIVER_APP_ID, OLIVER_PRIVATE_KEY, OLIVER_WEBHOOK_SECRET
docker compose -f deploy/docker-compose.yml up -d oliver
```

Verify:
- `docker compose logs oliver` shows the Probot startup banner and "Oliver listening for release.published events".
- `curl https://oliver.multiworld.gg/probot` returns Probot's health page.
- The App's "Recent Deliveries" panel shows 200 responses for test webhooks.

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
