"""Settings must never import the `worlds` package or load a world.

The former settings._update_cache() did `from worlds import AutoWorldRegister` on
any unknown-key access, and Settings.dump() used it to force-import every world
with a settings class. On user machines only the worlds being played may load;
on the webhost an import before set_game_names finishes queueing truncates the
catalog (worlds/__init__ is one-shot). Settings groups resolve passively against
worlds already in sys.modules; sections of unloaded worlds round-trip as dicts.
"""
import io
import json
import os
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

import settings
from settings import Group, Settings, _loaded_world_settings_names

REPO_ROOT = Path(__file__).resolve().parents[2]

CHILD = textwrap.dedent("""
    import io, json, sys
    sys.path.insert(0, {stubs!r})
    sys.path.insert(0, {root!r})

    import settings
    settings.no_gui = True
    settings.skip_autosave = True

    s = settings.Settings(None)
    s.update({{"fake_world_options": {{"alpha": 1}}}})
    missing = hasattr(s, "nonexistent_key_xyz")
    out = io.StringIO()
    s.dump(out)
    text = out.getvalue()

    print("@@RESULT@@" + json.dumps({{
        "worlds_imported": "worlds" in sys.modules,
        "section_kept": "fake_world_options" in text and "alpha: 1" in text,
        "missing_attr": missing,
    }}))
""")


class TestSettingsNeverImportWorlds(unittest.TestCase):
    """Subprocess: the suite's own bootstrap has already imported `worlds`."""

    @classmethod
    def setUpClass(cls):
        env = dict(os.environ)
        env.update(
            SKIP_ALL_INSTALLS="1",
            SKIP_REQUIREMENTS_UPDATE="1",
            KIVY_NO_CONSOLELOG="1",
            KIVY_NO_ARGS="1",
            PYTHONIOENCODING="utf-8",
        )
        env.pop("MWGG_USE_WORLDS_VENV", None)
        source = CHILD.format(stubs=str(REPO_ROOT / "test" / "_stubs"), root=str(REPO_ROOT))
        proc = subprocess.run(
            [sys.executable, "-c", source],
            cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=600,
        )
        marker = "@@RESULT@@"
        for line in proc.stdout.splitlines():
            if line.startswith(marker):
                cls.result = json.loads(line[len(marker):])
                return
        raise AssertionError(
            f"child produced no result (rc={proc.returncode})\n"
            f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
        )

    def test_dump_and_attribute_access_do_not_import_worlds(self):
        self.assertFalse(
            self.result["worlds_imported"],
            "Settings imported the `worlds` package as a side effect",
        )

    def test_unloaded_world_section_round_trips_as_dict(self):
        self.assertTrue(self.result["section_kept"])

    def test_unknown_key_stays_missing(self):
        self.assertFalse(self.result["missing_attr"])


class TestLoadedWorldSettingsNames(unittest.TestCase):
    """In-suite: `worlds` is loaded, so resolution must actually work."""

    def test_loaded_world_resolves(self):
        names = _loaded_world_settings_names()
        self.assertIn("universal_tracker", names)

    def test_settings_group_materializes_for_loaded_world(self):
        s = Settings(None)
        group = s.universal_tracker
        self.assertIsInstance(group, Group)
        self.assertEqual(type(group).__name__, "TrackerSettings")

    def test_dump_keeps_unloaded_section_alongside_loaded_groups(self):
        s = Settings(None)
        s.update({"totally_unloaded_world_options": {"alpha": 1}})
        out = io.StringIO()
        s.dump(out)
        text = out.getvalue()
        self.assertIn("totally_unloaded_world_options", text)
        self.assertIn("alpha: 1", text)
        self.assertIn("universal_tracker", text)
