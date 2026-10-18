#!/usr/bin/env python3
"""MCP server (stdio) to trigger and inspect the MultiworldGG worlds-venv refresh.

Exposes two tools to an MCP client (e.g. Claude):
  - refresh_worlds_venv : run the ``mwgg_upgrader`` compose service (the sole
                          writer of the shared worlds venv) and return success
                          plus a bounded tail of its log.
  - worlds_venv_status  : report the current venv state sourced from runtime:
                          installed mwgg_igdb version, its install date,
                          the active variant, and whether worlds are installed.

The server never imports the upgrader; it only shells out to ``docker compose``
and calls ModuleUpdate helpers, so it runs wherever the deploy lives.

Config - CLI flag overrides env var overrides default:
  --compose-file   / MWGG_COMPOSE_FILE      docker-compose.yml
  --deploy-dir     / MWGG_DEPLOY_DIR        dir holding it (alt to --compose-file)
  --service        / MWGG_UPGRADER_SERVICE  compose service name
  --timeout        / MWGG_UPGRADE_TIMEOUT   subprocess timeout, seconds
  --docker-compose / MWGG_DOCKER_COMPOSE    compose launcher
"""
from __future__ import annotations

import argparse
import asyncio
import importlib.metadata
import os
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Ensure repo root is importable when run as tools/mcp_mwgg_upgrader.py
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import ModuleUpdate

# ---- defaults (match the deploy in deploy/docker-compose.yml) ----------------
DEFAULT_COMPOSE_FILE = _REPO_ROOT / "deploy" / "docker-compose.yml"
DEFAULT_SERVICE = "mwgg_upgrader"
DEFAULT_TIMEOUT = 1800  # 30 min; a cold refresh fetches ~200 wheels
DEFAULT_TAIL_LINES = 80
DEFAULT_DOCKER_COMPOSE = "docker compose"


@dataclass
class Config:
    compose_file: Path
    service: str
    timeout: int
    docker_compose: list[str]


cfg: Config  # populated by main() before the server loop starts
mcp = FastMCP("mwgg-upgrader")


@mcp.tool()
def worlds_venv_status() -> dict:
    """Report the current worlds-venv state from runtime sources.

    Returns the installed mwgg_igdb version, its install date, the active
    variant, and whether the worlds venv is populated. No stamp file is read;
    all data comes from the installed package and the venv directory itself.
    """
    out: dict = {"ok": True}

    # mwgg_igdb installed version
    try:
        out["mwgg_igdb_version"] = importlib.metadata.version("mwgg_igdb")
    except importlib.metadata.PackageNotFoundError:
        out["mwgg_igdb_version"] = None

    # Install date (mtime of the mwgg_igdb module file)
    install_date = ModuleUpdate._igdb_install_date()
    out["igdb_install_date"] = install_date.isoformat() if install_date is not None else None

    # Active variant
    out["variant"] = ModuleUpdate._detect_installed_variant()

    # Whether the worlds venv is populated
    has_worlds = ModuleUpdate._venv_has_worlds()
    out["has_worlds"] = has_worlds
    out["worlds_state"] = "installed" if has_worlds else "not installed"

    return out


def _run_compose(args: list[str], timeout: int) -> dict:
    """Blocking: run a compose subcommand, merging stderr into stdout."""
    cmd = cfg.docker_compose + ["-f", str(cfg.compose_file)] + args
    started = time.time()
    try:
        proc = subprocess.run(
            cmd, cwd=str(cfg.compose_file.parent),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, timeout=timeout,
        )
        output, returncode, timed_out = proc.stdout, proc.returncode, False
    except subprocess.TimeoutExpired as e:
        output = e.output if isinstance(e.output, str) else (e.output or b"").decode(errors="replace")
        returncode, timed_out = None, True
    except OSError as e:
        return {"command": shlex.join(cmd), "error": f"failed to launch docker compose: {e}"}
    return {
        "command": shlex.join(cmd),
        "duration_seconds": round(time.time() - started, 1),
        "returncode": returncode,
        "timed_out": timed_out,
        "_output": output,
    }


@mcp.tool()
async def refresh_worlds_venv(
    use_up: bool = False,
    timeout: int | None = None,
    tail_lines: int = DEFAULT_TAIL_LINES,
) -> dict:
    """Refresh the shared worlds venv by running the ``mwgg_upgrader`` service.

    The upgrader is the sole writer of the venv: it installs the mwgg_igdb
    index, every world and the worlds' requirements, then exits 0. A cold run
    can take many minutes (~200 wheels), so output is captured and only a tail
    is returned.

    Args:
      use_up: use ``docker compose up --no-deps <svc>`` instead of the default
        ``docker compose run --rm <svc>``. ``run`` (default) auto-removes the
        container and reports the upgrader's exit code faithfully.
      timeout: per-call subprocess timeout in seconds (default: server config).
      tail_lines: number of trailing log lines to return.
    """
    effective_timeout = timeout if timeout is not None else cfg.timeout
    sub = ["up", "--no-deps", cfg.service] if use_up else ["run", "--rm", cfg.service]
    res = await asyncio.to_thread(_run_compose, sub, effective_timeout)
    if "error" in res:  # launch failure
        res["ok"] = False
        return res
    lines = res.pop("_output").splitlines()
    res["ok"] = res["returncode"] == 0
    res["lines_total"] = len(lines)
    res["log_tail"] = "\n".join(lines[-tail_lines:])
    if res["timed_out"]:
        res["error"] = f"timed out after {effective_timeout}s (partial log below)"
    return res


def _resolve_config(ns: argparse.Namespace) -> Config:
    env = os.environ.get
    if ns.compose_file or env("MWGG_COMPOSE_FILE"):
        compose = Path(ns.compose_file or env("MWGG_COMPOSE_FILE"))
    elif ns.deploy_dir or env("MWGG_DEPLOY_DIR"):
        compose = Path(ns.deploy_dir or env("MWGG_DEPLOY_DIR")) / "docker-compose.yml"
    else:
        compose = DEFAULT_COMPOSE_FILE
    launcher = ns.docker_compose or env("MWGG_DOCKER_COMPOSE") or DEFAULT_DOCKER_COMPOSE
    return Config(
        compose_file=compose.expanduser().resolve(),
        service=ns.service or env("MWGG_UPGRADER_SERVICE") or DEFAULT_SERVICE,
        timeout=int(ns.timeout or env("MWGG_UPGRADE_TIMEOUT") or DEFAULT_TIMEOUT),
        docker_compose=shlex.split(launcher),
    )


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--compose-file", help="path to docker-compose.yml")
    p.add_argument("--deploy-dir", help="dir containing docker-compose.yml (alt to --compose-file)")
    p.add_argument("--service", help=f"compose service name (default {DEFAULT_SERVICE})")
    p.add_argument("--timeout", help=f"subprocess timeout in seconds (default {DEFAULT_TIMEOUT})")
    p.add_argument("--docker-compose", help=f"compose launcher (default {DEFAULT_DOCKER_COMPOSE!r})")
    global cfg
    cfg = _resolve_config(p.parse_args())
    mcp.run()  # stdio transport


if __name__ == "__main__":
    main()
