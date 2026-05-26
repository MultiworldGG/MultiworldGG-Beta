#!/usr/bin/env bash
# Cron-friendly: hard-reinstall game_index/ao, verify import, then upgrade all deps (+ transitive) via uv.
#
# Crontab example (every day at 04:00):
#   0 4 * * *  /path/to/MultiworldGG/tools/cron_update_mwgg_igdb_ao.sh >> /var/log/mwgg_igdb_ao.log 2>&1

set -euo pipefail

# ---- Config: edit these to match your environment ----------------------------
REPO_ROOT="${MWGG_REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
MWGG_VENV="${MWGG_VENV:-/path/to/mwgg_venv}"        # <-- set this to your specific mwgg_venv
REQUIREMENTS="${MWGG_REQUIREMENTS:-$REPO_ROOT/requirements.txt}"
# ------------------------------------------------------------------------------

VENV_PY="$MWGG_VENV/bin/python"
AO_SRC="$REPO_ROOT/game_index/ao"

log() { printf '[%s] %s\n' "$(date -Iseconds)" "$*"; }

[[ -x "$VENV_PY"     ]] || { log "ERROR: venv python not found at $VENV_PY"; exit 1; }
[[ -d "$AO_SRC"      ]] || { log "ERROR: game_index/ao not found at $AO_SRC"; exit 1; }
[[ -f "$REQUIREMENTS" ]] || { log "ERROR: requirements file not found at $REQUIREMENTS"; exit 1; }

command -v uv >/dev/null || { log "ERROR: 'uv' not on PATH"; exit 1; }

log "Activating venv: $MWGG_VENV"
# shellcheck disable=SC1091
source "$MWGG_VENV/bin/activate"
export VIRTUAL_ENV="$MWGG_VENV"

log "Step 1/3: force-reinstalling mwgg_igdb (ao) from $AO_SRC"
uv pip install --python "$VENV_PY" --force-reinstall --no-deps --upgrade "$AO_SRC"

log "Step 2/3: verifying import"
"$VENV_PY" -c 'from mwgg_igdb import GAMES_DATA, GameIndex; print(f"mwgg_igdb OK: {len(GAMES_DATA)} games")'

log "Step 3/3: upgrading project deps (+ transitive) from $REQUIREMENTS"
# --upgrade resolves to latest compatible versions for everything in the file,
# and the resolver pulls in (and upgrades) transitive dependencies as a matter
# of course. --reinstall forces a clean install so stale transitive pins from
# a prior partial run don't linger.
uv pip install --python "$VENV_PY" --upgrade --reinstall -r "$REQUIREMENTS"

log "Done."