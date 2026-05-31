#!/usr/bin/env python
"""Populate / refresh the shared worlds venv (mwgg_venv).

Installs everything that belongs in the venv: the mwgg_igdb "ao" index, every
world listed in the index, and the worlds' transitive requirements.

This is the `mwgg_upgrader` docker-compose service and the *sole writer* of the
venv bind mount. It runs once to completion; every other service mounts the venv
read-only, runs with SKIP_ALL_INSTALLS=1, and waits for this to exit 0
(`depends_on: { condition: service_completed_successfully }`).

Refresh on demand:  docker compose up mwgg_upgrader
                    docker compose run --rm mwgg_upgrader

Exit code is 0 only when the index installed and the worlds venv is populated,
so a failed run blocks the consumers from starting against a broken venv.
"""
import logging
import os
import sys

# This service is the sole writer of the venv, so installs must run here no
# matter what the image/runtime env sets for the consumer services.
os.environ.pop("SKIP_ALL_INSTALLS", None)
os.environ.pop("SKIP_REQUIREMENTS_UPDATE", None)

# Configure logging before importing ModuleUpdate, which otherwise forces DEBUG.
logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("mwgg_upgrade")

import ModuleUpdate
from BaseUtils import WORLDS_EXIST

VARIANT = "ao"


def main() -> int:
    ModuleUpdate.set_variant(VARIANT)

    logger.info("Installing mwgg_igdb (%s) index", VARIANT)
    if not ModuleUpdate.install_mwgg_igdb(upgrade=True, force=True):
        logger.error("Failed to install mwgg_igdb (%s); aborting", VARIANT)
        return 1

    ModuleUpdate.invalidate_caches()
    try:
        from mwgg_igdb import GameIndex
    except ImportError as e:
        logger.error("mwgg_igdb installed but GameIndex is unimportable (%s); aborting", e)
        return 1

    slugs = [f"worlds.{slug}" for slug in GameIndex.get_all_games()]
    logger.info("Installing/updating %d worlds (+ requirements) in the worlds venv", len(slugs))
    # with_deps=True runs `uv pip install <wheel> --upgrade` for every world, so
    # each world AND its already-installed dependencies are checked for updates
    # and upgraded when outdated. uv skips packages already current — nothing is
    # force-reinstalled. (with_deps=False would skip up-to-date worlds entirely,
    # leaving their deps unchecked.)
    ModuleUpdate.install_worlds(slugs, with_deps=True)

    state = ModuleUpdate.record_worlds_update()
    if not state & WORLDS_EXIST.HAS_WORLDS:
        logger.error("Worlds venv is empty after install; aborting")
        return 1

    logger.info("mwgg_venv ready (worlds_updated=%d)", int(state))
    return 0


if __name__ == "__main__":
    sys.exit(main())
