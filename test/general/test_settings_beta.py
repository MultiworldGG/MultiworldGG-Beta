"""Beta settings tests (lazy world-settings resolution, Group.update coercion); add new settings tests here."""

import io
import json
import os
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path
from typing import Optional, Tuple

import settings
from settings import Group, ServerOptions, Settings, _loaded_world_settings_names

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestHostYamlBackslashRepair(unittest.TestCase):
    """A hand-edited Windows path in double quotes ("C:\\Users\\...") is invalid
    YAML; the loader re-reads such values literally instead of dropping the
    whole config, and the dumper single-quotes backslash values so copied
    styles stay literal."""

    def _load(self, body: str) -> Settings:
        import tempfile
        settings.skip_autosave = True
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "host.yaml")
            with open(path, "w", encoding="utf-8") as f:
                f.write(textwrap.dedent(body))
            return Settings(path)

    @staticmethod
    def _stored(loaded: Settings, key: str) -> str:
        # Group.__getattribute__ roots non-absolute paths under user_path, so a
        # Windows path resolves to <cwd>/C:\... on POSIX; assert the stored literal.
        return vars(loaded.general_options)[key]

    def test_unescaped_backslashes_read_literally(self) -> None:
        loaded = self._load('''
            general_options:
              output_path: "C:\\Users\\x\\new\\output"  # \\n and \\U alike
        ''')
        self.assertEqual(self._stored(loaded, "output_path"), "C:\\Users\\x\\new\\output")
        self.assertIsNotNone(loaded.filename)
        self.assertTrue(loaded.changed)

    def test_valid_escapes_untouched(self) -> None:
        text = 'general_options:\n  output_path: "C:\\\\Users\\\\x"\n  player_files_path: "tab\\there"\n'
        self.assertIsNone(settings._repair_unescaped_backslashes(text))
        loaded = self._load(text)
        self.assertEqual(self._stored(loaded, "output_path"), "C:\\Users\\x")
        self.assertEqual(loaded.general_options.player_files_path, "tab\there")

    def test_other_errors_still_fall_back_to_defaults(self) -> None:
        with self.assertLogs(level="ERROR") as logs:
            loaded = self._load('general_options:\n  output_path: "unterminated\n')
        self.assertIsNone(loaded.filename)
        self.assertIn("Could not parse", logs.output[0])

    def test_dump_single_quotes_backslash_values(self) -> None:
        from Utils import parse_yaml
        settings.skip_autosave = True
        s = Settings(None)
        s.general_options.output_path = "C:\\x\\y"
        out = io.StringIO()
        s.dump(out)
        text = out.getvalue()
        self.assertIn("output_path: 'C:\\x\\y'", text)
        self.assertEqual(parse_yaml(text)["general_options"]["output_path"], "C:\\x\\y")


# --------------------------------------------------------------------------- #
# Settings must never import the `worlds` package or load a world. The
# former settings._update_cache() did `from worlds import
# AutoWorldRegister` on any unknown-key access, and Settings.dump() used it
# to force-import every world with a settings class. On user machines only
# the worlds being played may load; on the webhost an import before
# set_game_names finishes queueing truncates the catalog (worlds/__init__
# is one-shot). Settings groups resolve passively against worlds already in
# sys.modules; sections of unloaded worlds round-trip as dicts.
# --------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------- #
# settings.Group.update value coercion and change tracking: the non-obvious
# type-coercion branches (bool vs int, Optional/None, scalar upcast to the
# declared type, list -> tuple/set) and the "key missing from the supplied
# dict marks the Group as changed" semantics.
# --------------------------------------------------------------------------- #

class _Tup(Tuple[int, ...]):
    """Bare tuple subclass so the annotation resolves to a real ``type``."""


class TestGroupUpdateCoercion(unittest.TestCase):
    def test_update_preserves_bool_for_bool_field(self) -> None:
        class G(Group):
            flag: bool = False

        g = G()
        g.update({"flag": True})
        # not coerced to int, even though issubclass(int, bool) is True
        self.assertIs(type(g.flag), bool)
        self.assertIs(g.flag, True)

    def test_update_assigns_none_for_optional(self) -> None:
        class G(Group):
            opt: Optional[int] = 7

        g = G()
        g.update({"opt": None})
        self.assertIsNone(g.opt)

    def test_update_upcasts_int_to_intenum(self) -> None:
        class G(Group):
            comp: ServerOptions.Compatibility = ServerOptions.Compatibility(2)

        g = G()
        g.update({"comp": 0})
        self.assertIsInstance(g.comp, ServerOptions.Compatibility)
        self.assertIs(g.comp, ServerOptions.Compatibility.OFF)

    def test_update_converts_list_to_tuple_field(self) -> None:
        class G(Group):
            tup: _Tup = _Tup()

        g = G()
        g.update({"tup": [1, 2, 3]})
        self.assertIsInstance(g.tup, _Tup)
        self.assertEqual(g.tup, (1, 2, 3))


class TestGroupUpdateChanged(unittest.TestCase):
    def test_update_marks_changed_on_missing_key(self) -> None:
        class G(Group):
            a: int = 1
            b: int = 2

        g = G()
        self.assertFalse(g.changed)
        g.update({"a": 5})  # "b" absent from the supplied dict
        self.assertTrue(g.changed)

    def test_update_not_changed_when_all_keys_present(self) -> None:
        class G(Group):
            a: int = 1
            b: int = 2

        g = G()
        g.update({"a": 5, "b": 6})
        self.assertFalse(g.changed)
