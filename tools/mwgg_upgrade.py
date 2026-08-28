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

Exit code is 0 only when the index installed, the worlds venv is populated, and no
world regressed, so a failed run blocks the consumers from starting against a broken
venv. Individual worlds that fail to install are tolerated up to a threshold (one bad
wheel costs that one game, not the deploy), but every run logs a WORLD_INSTALL_SUMMARY
line, so failures are greppable rather than silent.
"""
import logging
import os
import sys
from pathlib import Path

# This service is the sole writer of the venv, so installs must run here no
# matter what the image/runtime env sets for the consumer services.
os.environ.pop("SKIP_ALL_INSTALLS", None)
os.environ.pop("SKIP_REQUIREMENTS_UPDATE", None)

# Configure logging before importing ModuleUpdate, which otherwise forces DEBUG.
logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("mwgg_upgrade")

# Run from a subdir as `python tools/mwgg_upgrade.py`, so the repo root isn't on
# sys.path; add it before importing repo-root modules (ModuleUpdate, BaseUtils).
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import ModuleUpdate

VARIANT = "ao"

# Fraction of the index allowed to fail before the run counts as systemic breakage
# rather than bad wheels. Override with an absolute count via MWGG_UPGRADE_MAX_WORLD_FAILURES.
FAILURE_FRACTION = 0.1


def _installed_world_slugs() -> set[str]:
    """Slugs currently unpacked in the venv worlds dir.

    A missing dir is an empty venv (first run). Any other OSError propagates so the
    failure is reported as what it is; a silently-empty result here would read as
    "every world regressed" and block the deploy with a misleading message.
    """
    try:
        return {
            entry.name for entry in ModuleUpdate._venv_worlds_dir().iterdir()
            if entry.is_dir() and not entry.name.startswith("_")
        }
    except FileNotFoundError:
        return set()


def _max_tolerated_failures(world_count: int) -> int:
    override = os.environ.get("MWGG_UPGRADE_MAX_WORLD_FAILURES")
    if override:
        try:
            return int(override)
        except ValueError:
            logger.error(
                "MWGG_UPGRADE_MAX_WORLD_FAILURES=%r is not an integer; using the default tolerance",
                override,
            )
    return int(world_count * FAILURE_FRACTION)


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
    if not slugs:
        # The venv may still hold yesterday's worlds, so the downstream checks would
        # trivially pass; an empty index is index breakage, not a clean run.
        logger.error("Game index has no worlds; aborting")
        return 1
    logger.info("Installing/updating %d worlds (+ requirements) in the worlds venv", len(slugs))
    installed_before = _installed_world_slugs()
    # with_deps=True upgrades each world AND its already-installed deps when outdated
    # (uv skips current packages); with_deps=False would leave deps unchecked.
    result = ModuleUpdate.install_worlds(slugs, with_deps=True)

    failed = sorted(result.failed)
    logger.info(
        "WORLD_INSTALL_SUMMARY requested=%d failed=%d apworld_fallback=%d",
        len(slugs), len(failed), len(result),
    )
    if failed:
        logger.error("Worlds that could not be installed (%d): %s", len(failed), ", ".join(failed))

    if not ModuleUpdate._venv_has_worlds():
        logger.error("Worlds venv is empty after install; aborting")
        return 1

    # A world that was serving before this run and is gone now is a regression however
    # few there are: the consumers would come up having lost a game the site already had.
    regressed = sorted(installed_before - _installed_world_slugs())
    if regressed:
        logger.error("Worlds lost during this run (%d): %s", len(regressed), ", ".join(regressed))
        return 1

    tolerated = _max_tolerated_failures(len(slugs))
    if len(failed) > tolerated:
        logger.error(
            "%d worlds failed to install, over the tolerance of %d; treating as systemic and aborting",
            len(failed), tolerated,
        )
        return 1

    logger.info("mwgg_venv ready")
    return 0


if __name__ == "__main__":
    sys.exit(main())
