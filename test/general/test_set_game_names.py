"""set_game_names must not import the `worlds` package.

worlds/__init__.py is one-shot: on import it snapshots Utils._worlds_to_load,
loads exactly those entries and builds network_data_package. If set_game_names
imports it while still queueing, every game queued afterwards is silently
dropped from the catalog. A single uninstallable world once cost the site 236 of
244 games this way.
"""
import json
import os
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

import Utils

REPO_ROOT = Path(__file__).resolve().parents[2]

# Real worlds that live as source directories in the repo, so they have no pip
# metadata and take the same code path the missing world took. The bogus entry
# sits in the middle: everything after it must still reach the loader.
ON_DISK_SLUGS = ["_debug", "apquest", "mwquest"]
MISSING_SLUG = "world_that_is_not_installed_anywhere"

CHILD = textwrap.dedent("""
    import json, os, sys
    sys.path.insert(0, {stubs!r})
    sys.path.insert(0, {root!r})

    import settings
    settings.no_gui = True
    settings.skip_autosave = True

    import Utils
    import ModuleUpdate
    import tempfile
    from pathlib import Path
    # Hermetic: set_game_names scans custom_worlds_dir at call time; the machine's
    # real directory may hold arbitrary (or corrupt) apworlds.
    ModuleUpdate.custom_worlds_dir = Path(tempfile.mkdtemp())
    from mwgg_igdb import GameIndex

    on_disk = {on_disk!r}
    missing = {missing!r}
    games = []
    for slug in on_disk[:1] + [missing] + on_disk[1:]:
        name = f"Game {{slug}}"
        GameIndex.add_game(slug, {{"game_name": name}})
        games.append(name)

    Utils.set_game_names(games, strict=False)

    imported_early = "worlds" in sys.modules
    queued = [e for e in Utils.game_names() if isinstance(e, str)]

    import worlds
    loaded = [s.game_module for s in worlds.world_sources if isinstance(s.game_module, str)]

    print("@@RESULT@@" + json.dumps({{
        "imported_early": imported_early,
        "queued": queued,
        "loaded": loaded,
        "served": sorted(worlds.network_data_package["games"]),
        "failed_loads": worlds.failed_world_loads,
    }}))
""")


def _run_child() -> dict:
    env = dict(os.environ)
    env.update(
        SKIP_ALL_INSTALLS="1",
        SKIP_REQUIREMENTS_UPDATE="1",
        KIVY_NO_CONSOLELOG="1",
        KIVY_NO_ARGS="1",
        PYTHONIOENCODING="utf-8",
    )
    env.pop("AP_TEST_WORLDS", None)
    # If set (e.g. inside the Docker image), ModuleUpdate would rank the worlds-venv
    # site-packages ahead of the stub dir on the child's sys.path.
    env.pop("MWGG_USE_WORLDS_VENV", None)
    source = CHILD.format(
        stubs=str(REPO_ROOT / "test" / "_stubs"),
        root=str(REPO_ROOT),
        on_disk=ON_DISK_SLUGS,
        missing=MISSING_SLUG,
    )
    proc = subprocess.run(
        [sys.executable, "-c", source],
        cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=600,
    )
    marker = "@@RESULT@@"
    for line in proc.stdout.splitlines():
        if line.startswith(marker):
            return json.loads(line[len(marker):])
    raise AssertionError(
        f"child produced no result (rc={proc.returncode})\n"
        f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
    )


class TestSetGameNamesDoesNotImportWorlds(unittest.TestCase):
    """Runs in a subprocess: the suite's own bootstrap has already imported `worlds`."""

    @classmethod
    def setUpClass(cls):
        cls.result = _run_child()

    def test_worlds_not_imported_while_queueing(self):
        self.assertFalse(
            self.result["imported_early"],
            "set_game_names imported the `worlds` package, freezing the catalog mid-queue",
        )

    def test_missing_world_does_not_truncate_the_catalog(self):
        loaded = set(self.result["loaded"])
        for slug in ON_DISK_SLUGS:
            self.assertIn(
                f"worlds.{slug}", loaded,
                f"worlds.{slug} was queued but never reached the loader; a missing "
                f"world truncated the catalog",
            )
        self.assertNotIn(f"worlds.{MISSING_SLUG}", loaded)

    def test_missing_world_does_not_abort_queueing(self):
        queued = set(self.result["queued"])
        for slug in ON_DISK_SLUGS:
            self.assertIn(f"worlds.{slug}", queued)

    def test_missing_world_costs_exactly_one_game(self):
        # What the site actually serves. The outage shipped 8 of 244 entries here.
        served = set(self.result["served"])
        self.assertEqual(self.result["failed_loads"], [])
        self.assertTrue(
            {"Archipelago", "Universal Tracker"} <= served,
            f"baseline worlds missing from the data package: {sorted(served)}",
        )
        self.assertEqual(
            len(served), len(ON_DISK_SLUGS) + 2,
            f"expected every on-disk world plus the two baseline entries, got {sorted(served)}",
        )


class TestWorldModuleOnDisk(unittest.TestCase):
    def test_absent_world_is_not_on_disk(self):
        self.assertFalse(Utils._world_module_on_disk(MISSING_SLUG))

    def test_present_world_is_on_disk(self):
        self.assertTrue(Utils._world_module_on_disk("generic"))

    def test_worlds_dir_itself_is_not_a_world(self):
        # A bare directory matches as a namespace package; only real packages count.
        self.assertFalse(Utils._world_module_on_disk("__pycache__"))
