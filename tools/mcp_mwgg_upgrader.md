# MCP server: worlds-venv refresh (`mcp_mwgg_upgrader.py`)

A small, user-owned [MCP](https://modelcontextprotocol.io) server (stdio) that lets
an operator trigger and inspect the MultiworldGG webhost's **worlds venv** refresh
from an MCP client (e.g. Claude) instead of SSHing in.

It does not import the upgrader - it only shells out to `docker compose` and calls
ModuleUpdate helpers, so it can run anywhere the deploy lives.

## Tools

| Tool | What it does |
|---|---|
| `refresh_worlds_venv(use_up=False, timeout=None, tail_lines=80)` | Runs the `mwgg_upgrader` service - the sole writer of the shared venv. Default `docker compose run --rm mwgg_upgrader`; pass `use_up=true` for `up --no-deps`. Returns `ok`, `returncode`, `duration_seconds`, `timed_out`, `lines_total`, and a `log_tail`. |
| `worlds_venv_status()` | Reports the current venv state from runtime: `mwgg_igdb_version`, `igdb_install_date`, `variant`, `has_worlds`, and `worlds_state` ("installed" or "not installed"). No stamp file is read. |

A cold refresh fetches ~200 wheels and can take many minutes; the default timeout
is **1800s** and only a bounded log tail is returned.

## Install

```bash
# Use the host's Python (3.10+). A dedicated venv is fine.
pip install -r tools/requirements-mcp.txt      # or: pip install mcp
```

## Configuration

CLI flag overrides env var overrides default. Defaults match `deploy/docker-compose.yml`.

| Flag | Env var | Default |
|---|---|---|
| `--compose-file` | `MWGG_COMPOSE_FILE` | `<repo>/deploy/docker-compose.yml` |
| `--deploy-dir` | `MWGG_DEPLOY_DIR` | (alternative to `--compose-file`) |
| `--service` | `MWGG_UPGRADER_SERVICE` | `mwgg_upgrader` |
| `--timeout` | `MWGG_UPGRADE_TIMEOUT` | `1800` |
| `--docker-compose` | `MWGG_DOCKER_COMPOSE` | `docker compose` |

## Register in an MCP client

Use absolute paths and point at the deploy. The stdio `command` + `args` shape is
the same across clients; only the wrapping config key differs.

### Claude Code

```bash
claude mcp add mwgg-upgrader -- /opt/mwgg/venv/bin/python \
  /opt/mwgg/tools/mcp_mwgg_upgrader.py --deploy-dir /opt/mwgg/deploy
```

### VS Code

```bash
code --add-mcp "{\"name\":\"mwgg-upgrader\",\"command\":\"/opt/mwgg/venv/bin/python\",\"args\":[\"/opt/mwgg/tools/mcp_mwgg_upgrader.py\",\"--deploy-dir\",\"/opt/mwgg/deploy\"]}"
```

Or commit it to the workspace as `.vscode/mcp.json` (VS Code nests servers under
`servers`, not `mcpServers`):

```json
{
  "servers": {
    "mwgg-upgrader": {
      "type": "stdio",
      "command": "/opt/mwgg/venv/bin/python",
      "args": ["/opt/mwgg/tools/mcp_mwgg_upgrader.py", "--deploy-dir", "/opt/mwgg/deploy"]
    }
  }
}
```

### Other clients (Claude Desktop, Cursor, …)

Add a stdio entry under the client's `mcpServers` key:

```jsonc
{
  "mcpServers": {
    "mwgg-upgrader": {
      "command": "/opt/mwgg/venv/bin/python",
      "args": ["/opt/mwgg/tools/mcp_mwgg_upgrader.py", "--deploy-dir", "/opt/mwgg/deploy"]
    }
  }
}
```

The operator running this server needs permission to talk to the Docker daemon
(same as running `docker compose` by hand).

## Smoke test (no client needed)

```bash
python -c "import asyncio, tools.mcp_mwgg_upgrader as m; \
print([t.name for t in asyncio.run(m.mcp.list_tools())])"
# -> ['worlds_venv_status', 'refresh_worlds_venv']
```
