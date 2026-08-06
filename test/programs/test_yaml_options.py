# Contract tests for Generate's --yaml-options mode, the data source for
# mwgg-gui's YAML creator (yaml_creator/world_data.py).
#
# Pins the surface the GUI depends on across the repo split: the descriptor
# type strings its widget factories switch on, the payload schema, the
# EXIT_NEEDS_RELOAD retry convention, and the stdout-purity guarantee (a
# single JSON document on stdout, everything else on stderr).

import importlib.util
import io
import json
import os
import subprocess
import sys
import unittest

from pathlib import Path
from unittest import mock

import Generate
import ModuleUpdate
import Options
import Utils
from worlds.AutoWorld import AutoWorldRegister

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Synthetic subclasses, one per branch of Generate._y_describe_option.

class _Toggle(Options.Toggle):
    """Synthetic toggle."""
    display_name = "Synthetic Toggle"


class _TextChoice(Options.TextChoice):
    option_alpha = 0
    option_beta = 1
    default = 0


class _Choice(Options.Choice):
    option_alpha = 0
    option_beta = 1
    default = 0


class _NamedRange(Options.NamedRange):
    range_start = 5
    range_end = 25
    default = 5
    special_range_names = {"special": 7}


class _Range(Options.Range):
    range_start = 5
    range_end = 25
    default = 5


class _FreeText(Options.FreeText):
    pass


class _ItemSet(Options.ItemSet):
    valid_keys = frozenset({"Sword", "Shield"})


class _LocationSet(Options.LocationSet):
    valid_keys = frozenset({"Boss", "Chest"})


class _OptionCounter(Options.OptionCounter):
    valid_keys = frozenset({"Bomb"})


class _ItemDict(Options.ItemDict):
    pass


class _OptionSet(Options.OptionSet):
    valid_keys = frozenset({"A", "B"})


class _OptionList(Options.OptionList):
    valid_keys = frozenset({"A", "B"})


class _OptionDict(Options.OptionDict):
    default = {"key": 1}


class _Unmodeled(Options.Option):
    """An Option base _y_describe_option has no branch for."""
    default = ""


_ALL_BRANCH_CLASSES = (
    _Toggle, _TextChoice, _Choice, _NamedRange, _Range, _FreeText, _ItemSet,
    _LocationSet, _OptionCounter, _ItemDict, _OptionSet, _OptionList,
    _OptionDict, _Unmodeled,
)

# The full set of type strings --yaml-options can emit. Both GUI widget
# factories switch on these exact strings:
#   mwgg_gui/yaml_creator/option_widgets.py   widget_for_option
#   mwgg_gui/yaml_creator/weighted_widgets.py weight_widget_for_option
# Additions need a matching GUI fallback; renames are a breaking change
# (bump the payload's schema_version).
EMITTED_TYPES = frozenset({
    "toggle", "text_choice", "choice", "named_range", "range", "free_text",
    "item_set", "location_set", "option_counter", "option_set", "option_dict",
})

_DESCRIPTOR_REQUIRED_KEYS = {"name", "display_name", "docstring", "default", "type", "supports_weighting"}


class TestDescribeOptionBranches(unittest.TestCase):
    """Every branch of Generate._y_describe_option, including the subclass-order
    guards: the issubclass chain checks subclasses before their bases
    (TextChoice before Choice, NamedRange before Range, ItemSet/LocationSet/
    OptionCounter before OptionSet/OptionDict), so reordering it silently
    downgrades descriptors."""

    def describe(self, option_class):
        return Generate._y_describe_option("synthetic", option_class)

    def test_base_keys_present_on_every_descriptor(self):
        for option_class in _ALL_BRANCH_CLASSES:
            desc = self.describe(option_class)
            self.assertEqual(_DESCRIPTOR_REQUIRED_KEYS - set(desc), set(), option_class.__name__)

    def test_toggle(self):
        desc = self.describe(_Toggle)
        self.assertEqual(desc["type"], "toggle")
        self.assertEqual(desc["display_name"], "Synthetic Toggle")
        self.assertTrue(desc["supports_weighting"])

    def test_text_choice_not_downgraded_to_choice(self):
        desc = self.describe(_TextChoice)
        self.assertEqual(desc["type"], "text_choice")
        self.assertEqual(desc["choices"], {"0": "alpha", "1": "beta"})
        self.assertEqual(desc["display_names"], {"0": "Alpha", "1": "Beta"})

    def test_choice(self):
        desc = self.describe(_Choice)
        self.assertEqual(desc["type"], "choice")
        self.assertEqual(desc["choices"], {"0": "alpha", "1": "beta"})
        self.assertEqual(desc["display_names"], {"0": "Alpha", "1": "Beta"})

    def test_named_range_not_downgraded_to_range(self):
        desc = self.describe(_NamedRange)
        self.assertEqual(desc["type"], "named_range")
        self.assertEqual(desc["range_start"], 5)
        self.assertEqual(desc["range_end"], 25)
        self.assertEqual(desc["special_range_names"], {"special": 7})

    def test_range(self):
        desc = self.describe(_Range)
        self.assertEqual(desc["type"], "range")
        self.assertEqual(desc["range_start"], 5)
        self.assertEqual(desc["range_end"], 25)

    def test_free_text(self):
        self.assertEqual(self.describe(_FreeText)["type"], "free_text")

    def test_item_set_not_downgraded_to_option_set(self):
        desc = self.describe(_ItemSet)
        self.assertEqual(desc["type"], "item_set")
        self.assertEqual(desc["valid_keys"], ["Shield", "Sword"])
        self.assertFalse(desc["supports_weighting"])

    def test_location_set_not_downgraded_to_option_set(self):
        desc = self.describe(_LocationSet)
        self.assertEqual(desc["type"], "location_set")
        self.assertEqual(desc["valid_keys"], ["Boss", "Chest"])

    def test_option_counter_not_downgraded_to_option_dict(self):
        desc = self.describe(_OptionCounter)
        self.assertEqual(desc["type"], "option_counter")
        self.assertEqual(desc["valid_keys"], ["Bomb"])
        self.assertFalse(desc["verify_item_name"])
        self.assertFalse(desc["verify_location_name"])

    def test_item_dict_reports_option_counter_with_item_verification(self):
        desc = self.describe(_ItemDict)
        self.assertEqual(desc["type"], "option_counter")
        self.assertTrue(desc["verify_item_name"])

    def test_option_set_and_option_list_share_option_set(self):
        for option_class in (_OptionSet, _OptionList):
            desc = self.describe(option_class)
            self.assertEqual(desc["type"], "option_set")
            self.assertEqual(desc["valid_keys"], ["A", "B"])

    def test_option_dict(self):
        desc = self.describe(_OptionDict)
        self.assertEqual(desc["type"], "option_dict")
        self.assertEqual(desc["default"], {"key": 1})
        self.assertFalse(desc["supports_weighting"])

    def test_unmodeled_subclass_falls_back_to_free_text(self):
        self.assertEqual(self.describe(_Unmodeled)["type"], "free_text")


class TestEmittedTypeSetPinned(unittest.TestCase):
    def test_emitted_type_set_is_pinned(self):
        emitted = {
            Generate._y_describe_option("synthetic", option_class)["type"]
            for option_class in _ALL_BRANCH_CLASSES
        }
        self.assertEqual(emitted, EMITTED_TYPES)


class TestApquestPayloadSchema(unittest.TestCase):
    """Schema of the building blocks dump_yaml_options assembles, in-process
    against a real world (APQuest), at both GUI visibility levels."""

    def test_payload_schema_both_visibilities(self):
        world = AutoWorldRegister.world_types["APQuest"]
        for visibility in (Options.Visibility.simple_ui, Options.Visibility.complex_ui):
            with self.subTest(visibility=visibility.name):
                option_groups = Options.get_option_groups(world, visibility_level=visibility)
                groups_out = {}
                for group_name, options in option_groups.items():
                    descs = [Generate._y_describe_option(option_name, option_class)
                             for option_name, option_class in (options or {}).items()]
                    if descs:
                        groups_out[group_name] = descs
                payload = {
                    "ok": True,
                    "schema_version": 1,
                    "generator_version": Utils.__version__,
                    "world_version": world.world_version.as_simple_string(),
                    "game_name": "APQuest",
                    "world": Generate._y_describe_world(world),
                    "groups": groups_out,
                    "presets": Generate._y_describe_presets(world),
                }
                self.assertIn("Gameplay Options", groups_out)
                self.assertIn("Aesthetic Options", groups_out)
                for group_name, descs in groups_out.items():
                    for desc in descs:
                        self.assertEqual(_DESCRIPTOR_REQUIRED_KEYS - set(desc), set(),
                                         f"{group_name}/{desc.get('name')}")
                by_name = {desc["name"]: desc for descs in groups_out.values() for desc in descs}
                self.assertEqual(by_name["hard_mode"]["type"], "toggle")
                self.assertEqual(by_name["trap_chance"]["type"], "range")
                self.assertEqual(by_name["player_sprite"]["type"], "choice")
                self.assertEqual(set(payload["world"]),
                                 {"item_names", "location_names", "item_name_groups", "location_name_groups"})
                self.assertEqual(set(payload["presets"]), {"boring", "the true way to play"})
                # The whole payload must survive a JSON round-trip unchanged.
                self.assertEqual(json.loads(json.dumps(payload)), payload)


class TestDumpYamlOptions(unittest.TestCase):
    """dump_yaml_options against the bootstrap-loaded APQuest world.

    The monkeypatches are mandatory, not convenience: in-tree worlds have no
    pip dist-info, so the real _y_world_installed/install path would reach
    ModuleUpdate's network plumbing from a test."""

    def _dump_with(self, *, installed, install_result=None):
        buf = io.StringIO()
        with mock.patch.object(Generate, "_JSON_OUT", buf), \
                mock.patch.object(Generate, "_y_world_installed", lambda module: installed), \
                mock.patch.object(Generate, "set_game_names", lambda games, strict=False: None), \
                mock.patch.object(Generate, "_y_custom_world_entry", lambda module: None), \
                mock.patch.object(ModuleUpdate, "install_worlds",
                                  lambda worlds, update=False, with_deps=False: list(install_result or [])):
            rv = Generate.dump_yaml_options("APQuest", "simple")
        return rv, buf.getvalue()

    def test_happy_path_emits_single_ok_payload(self):
        rv, out = self._dump_with(installed=True)
        self.assertEqual(rv, 0)
        payload = json.loads(out)  # exactly one JSON document
        self.assertTrue(payload["ok"], msg=payload.get("error"))
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["generator_version"], Utils.__version__)
        world = AutoWorldRegister.world_types["APQuest"]
        self.assertEqual(payload["world_version"], world.world_version.as_simple_string())
        self.assertEqual(payload["game_name"], "APQuest")
        self.assertIn("boring", payload["presets"])
        for descs in payload["groups"].values():
            for desc in descs:
                self.assertIn("supports_weighting", desc)

    def test_install_branch_returns_exit_needs_reload_with_marker(self):
        rv, out = self._dump_with(installed=False, install_result=["worlds.apquest"])
        # Pin the literal too: the GUI wheel only retries on 10
        # (world_data._EXIT_NEEDS_RELOAD).
        self.assertEqual(Generate.EXIT_NEEDS_RELOAD, 10)
        self.assertEqual(rv, Generate.EXIT_NEEDS_RELOAD)
        marker = json.loads(out)
        self.assertFalse(marker["ok"])
        self.assertTrue(marker["needs_reload"])
        self.assertEqual(marker["reason"], "world-installed")

    def test_install_branch_failed_install_reports_error(self):
        rv, out = self._dump_with(installed=False, install_result=[])
        self.assertEqual(rv, 0)
        payload = json.loads(out)
        self.assertFalse(payload["ok"])
        self.assertIn("Could not install", payload["error"])


# The child mirrors the real `Generate --yaml-options` flow: sys.argv is set
# BEFORE `import Generate` so the import-time sniff (Generate.py top) diverts
# stdout->stderr and stashes the real stdout — untestable in-process. Generate's
# own import chain pulls in Utils, whose import-time init_logging banner must
# land on the already-diverted stdout (stderr). The world is queued onto
# Utils._worlds_to_load before any `import worlds` (the load loop runs at the
# first one, inside dump_yaml_options), so APQuest genuinely loads in-child.
_STDOUT_PURITY_CHILD = """\
import sys
sys.argv = ["Generate.py", "--yaml-options", "--game", "APQuest",
            "--module", "apquest", "--visibility", "simple"]
import Generate
import Utils
assert "worlds" not in sys.modules, "import Generate must not import the worlds package"
Utils._worlds_to_load.append("worlds.apquest")
# Same mandatory monkeypatches as the in-process tests (in-tree worlds have no
# pip dist-info; the real path would hit the network), minus _JSON_OUT: the
# emit must go to the child's real stdout.
Generate._y_world_installed = lambda module: True
Generate.set_game_names = lambda games, strict=False: None
sys.exit(Generate.dump_yaml_options("APQuest", "simple", "apquest"))
"""


class TestStdoutPuritySubprocess(unittest.TestCase):
    def test_stdout_is_exactly_one_ok_json_document(self):
        env = {
            **os.environ,
            # Short-circuit ModuleUpdate at Generate import: SKIP_REQUIREMENTS_UPDATE
            # gates the requirements refresh (update_ran), SKIP_ALL_INSTALLS also the
            # mwgg_igdb pull — a test must never touch the network or mutate the venv.
            "SKIP_REQUIREMENTS_UPDATE": "1",
            "SKIP_ALL_INSTALLS": "1",
            # `from mwgg_igdb import GameIndex` in the child resolves the test stub
            # (CI does not install the real package).
            "PYTHONPATH": os.pathsep.join(
                [os.path.join(REPO_ROOT, "test", "_stubs")]
                + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else [])),
        }
        result = subprocess.run(
            [sys.executable, "-c", _STDOUT_PURITY_CHILD],
            cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=300,
        )
        self.assertEqual(result.returncode, 0, msg=f"STDERR:\n{result.stderr[-2000:]}")
        # json.loads over the FULL stdout: any stray byte (logging banner, world
        # print) fails the parse, so this asserts "exactly one document" too.
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"], msg=payload.get("error"))
        self.assertEqual(payload["game_name"], "APQuest")
        self.assertTrue(payload["groups"], "world did not genuinely load (empty groups)")


def _load_gui_world_data():
    """Load mwgg_gui/yaml_creator/world_data.py BY FILE PATH.

    Never import the package: any `import mwgg_gui.x` executes the package
    __init__, which pulls in the full Kivy GUI including window creation.
    find_spec locates the installed package without executing it, and
    world_data.py itself imports zero Kivy. Returns None (-> skip) when the
    GUI wheel isn't available, e.g. in unittests.yml CI."""
    spec = importlib.util.find_spec("mwgg_gui")
    if spec is None or not spec.submodule_search_locations:
        return None
    world_data_path = Path(next(iter(spec.submodule_search_locations)), "yaml_creator", "world_data.py")
    if not world_data_path.is_file():
        return None
    file_spec = importlib.util.spec_from_file_location("_gui_world_data_for_pin", world_data_path)
    module = importlib.util.module_from_spec(file_spec)
    file_spec.loader.exec_module(module)
    return module


class TestExitNeedsReloadConstantsMatch(unittest.TestCase):
    def test_exit_needs_reload_constants_match(self):
        gui_world_data = _load_gui_world_data()
        if gui_world_data is None:
            self.skipTest("mwgg_gui not available (unittests.yml CI does not install the GUI wheel)")
        self.assertEqual(Generate.EXIT_NEEDS_RELOAD, 10)
        self.assertEqual(gui_world_data._EXIT_NEEDS_RELOAD, Generate.EXIT_NEEDS_RELOAD)


if __name__ == "__main__":
    unittest.main()
