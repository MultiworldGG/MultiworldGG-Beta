"""The mwgg_upgrader is the sole writer of the shared worlds venv and every other
compose service gates on `service_completed_successfully`. Its exit code therefore
decides whether the site comes up against an incomplete venv.
"""
import importlib.util
import os
import unittest
from pathlib import Path
from unittest import mock

import ModuleUpdate

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_upgrader():
    # tools/ is not a package; load the script by path. Importing it pops the
    # install-skip env vars, so snapshot and restore them around the load.
    saved = {k: os.environ.get(k) for k in ("SKIP_ALL_INSTALLS", "SKIP_REQUIREMENTS_UPDATE")}
    spec = importlib.util.spec_from_file_location(
        "mwgg_upgrade_under_test", REPO_ROOT / "tools" / "mwgg_upgrade.py"
    )
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    return module


class TestUpgraderExitCodes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.upgrader = _load_upgrader()

    def _run(self, index_slugs, failed, installed_before, installed_after, env=None):
        result = ModuleUpdate.WorldInstallResult()
        result.failed.extend(failed)
        games = {slug: {} for slug in index_slugs}
        slug_dirs = iter([set(installed_before), set(installed_after)])
        with mock.patch.object(ModuleUpdate, "set_variant"), \
                mock.patch.object(ModuleUpdate, "install_mwgg_igdb", return_value=True), \
                mock.patch.object(ModuleUpdate, "invalidate_caches"), \
                mock.patch.object(ModuleUpdate, "install_worlds", return_value=result), \
                mock.patch.object(ModuleUpdate, "_venv_has_worlds", return_value=True), \
                mock.patch.object(self.upgrader, "_installed_world_slugs", lambda: next(slug_dirs)), \
                mock.patch.dict(os.environ, env or {}, clear=False):
            from mwgg_igdb import GameIndex
            with mock.patch.object(GameIndex, "get_all_games", return_value=games):
                return self.upgrader.main()

    def test_clean_run_exits_zero(self):
        slugs = [f"w{i}" for i in range(20)]
        self.assertEqual(self._run(slugs, [], slugs, slugs), 0)

    def test_one_bad_world_does_not_block_the_deploy(self):
        # With the catalog no longer truncating, a single uninstallable world costs
        # that one game; blocking every other service over it is the worse outcome.
        slugs = [f"w{i}" for i in range(20)]
        self.assertEqual(self._run(slugs, ["worlds.w0"], slugs[1:], slugs[1:]), 0)

    def test_widespread_failure_blocks_the_deploy(self):
        slugs = [f"w{i}" for i in range(20)]
        failed = [f"worlds.{slug}" for slug in slugs[:5]]
        self.assertEqual(self._run(slugs, failed, slugs[5:], slugs[5:]), 1)

    def test_regression_blocks_the_deploy_however_small(self):
        slugs = [f"w{i}" for i in range(20)]
        self.assertEqual(self._run(slugs, ["worlds.w0"], slugs, slugs[1:]), 1)

    def test_failure_tolerance_is_overridable(self):
        slugs = [f"w{i}" for i in range(20)]
        failed = [f"worlds.{slug}" for slug in slugs[:5]]
        self.assertEqual(
            self._run(slugs, failed, slugs[5:], slugs[5:],
                      env={"MWGG_UPGRADE_MAX_WORLD_FAILURES": "5"}),
            0,
        )
        self.assertEqual(
            self._run(slugs, failed, slugs[5:], slugs[5:],
                      env={"MWGG_UPGRADE_MAX_WORLD_FAILURES": "0"}),
            1,
        )

    def test_empty_venv_still_blocks(self):
        slugs = [f"w{i}" for i in range(20)]
        with mock.patch.object(ModuleUpdate, "set_variant"), \
                mock.patch.object(ModuleUpdate, "install_mwgg_igdb", return_value=True), \
                mock.patch.object(ModuleUpdate, "invalidate_caches"), \
                mock.patch.object(ModuleUpdate, "install_worlds",
                                  return_value=ModuleUpdate.WorldInstallResult()), \
                mock.patch.object(ModuleUpdate, "_venv_has_worlds", return_value=False), \
                mock.patch.object(self.upgrader, "_installed_world_slugs", set):
            from mwgg_igdb import GameIndex
            with mock.patch.object(GameIndex, "get_all_games", return_value={s: {} for s in slugs}):
                self.assertEqual(self.upgrader.main(), 1)

    def test_empty_index_blocks_the_deploy(self):
        # The venv may still hold yesterday's worlds, so 0-of-0 failures must not
        # read as a clean run.
        self.assertEqual(self._run([], [], ["w0"], ["w0"]), 1)

    def test_bad_tolerance_override_falls_back_to_default(self):
        slugs = [f"w{i}" for i in range(20)]
        failed = [f"worlds.{slug}" for slug in slugs[:5]]
        self.assertEqual(
            self._run(slugs, failed, slugs[5:], slugs[5:],
                      env={"MWGG_UPGRADE_MAX_WORLD_FAILURES": "banana"}),
            1,
        )
        self.assertEqual(
            self._run(slugs, ["worlds.w0"], slugs[1:], slugs[1:],
                      env={"MWGG_UPGRADE_MAX_WORLD_FAILURES": "banana"}),
            0,
        )

    def test_installed_world_slugs_missing_dir_is_empty(self):
        with mock.patch.object(ModuleUpdate, "_venv_worlds_dir",
                               return_value=REPO_ROOT / "no_such_dir_for_this_test"):
            self.assertEqual(self.upgrader._installed_world_slugs(), set())

    def test_installed_world_slugs_filters_non_worlds(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "alpha").mkdir()
            (root / "_infra").mkdir()
            (root / "__pycache__").mkdir()
            (root / "stray.txt").write_text("x")
            with mock.patch.object(ModuleUpdate, "_venv_worlds_dir", return_value=root):
                self.assertEqual(self.upgrader._installed_world_slugs(), {"alpha"})

    def test_failed_index_install_still_blocks(self):
        with mock.patch.object(ModuleUpdate, "set_variant"), \
                mock.patch.object(ModuleUpdate, "install_mwgg_igdb", return_value=False):
            self.assertEqual(self.upgrader.main(), 1)
