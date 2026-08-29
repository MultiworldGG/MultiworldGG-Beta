# Tests for Generate.py (MultiworldGGGenerate.exe)

import importlib.util
import io
import json
import os
import os.path
import subprocess
import sys
import unittest

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import Generate
import ModuleUpdate
import Options
import Utils
# NOTE: `import Main` and `worlds.*` imports are deferred into each test: both
# import `worlds`, whose one-shot load loop must run after Generate.main()
# queues the player files' worlds.

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGenerateMain(unittest.TestCase):
    """This tests Generate.py (MultiworldGGGenerate.exe) main"""

    generate_dir = Path(Generate.__file__).parent
    run_dir = generate_dir / "test"  # reproducible cwd that's neither __file__ nor Generate.__file__
    abs_input_dir = Path(__file__).parent / 'data' / 'one_player'
    rel_input_dir = abs_input_dir.relative_to(run_dir)  # directly supplied relative paths are relative to cwd
    yaml_input_dir = abs_input_dir.relative_to(generate_dir)  # yaml paths are relative to user_path

    def assertOutput(self, output_dir: str):
        output_path = Path(output_dir)
        output_files = list(output_path.glob('*.zip'))
        if len(output_files) == 1:
            return True
        self.fail(f"Expected {output_dir} to contain one zip, but has {len(output_files)}: "
                  f"{list(output_path.glob('*'))}")

    def setUp(self):
        self.original_argv = sys.argv.copy()
        self.original_cwd = os.getcwd()
        self.original_local_path = Generate.Utils.local_path.cached_path
        self.original_user_path = Generate.Utils.user_path.cached_path

        # Force both user_path and local_path to a specific path. They have independent caches.
        Generate.Utils.user_path.cached_path = Generate.Utils.local_path.cached_path = str(self.generate_dir)
        os.chdir(self.run_dir)
        self.output_tempdir = TemporaryDirectory(prefix='AP_out_')

    def tearDown(self):
        self.output_tempdir.cleanup()
        os.chdir(self.original_cwd)
        sys.argv = self.original_argv
        Generate.Utils.local_path.cached_path = self.original_local_path
        Generate.Utils.user_path.cached_path = self.original_user_path

    def test_paths(self):
        # Pin the path-resolution contract the relative-path tests below depend on.
        self.assertEqual(os.getcwd(), str(self.run_dir))
        self.assertEqual(Generate.Utils.user_path(), str(self.generate_dir))

        # rel_input_dir resolves against cwd -- how a relative --player_files_path is consumed.
        self.assertFalse(os.path.isabs(self.rel_input_dir))
        self.assertEqual(Path(self.rel_input_dir).resolve(), self.abs_input_dir)

        # yaml_input_dir is user_path-relative (host.yaml's player_files_path): it must NOT
        # resolve against cwd and must round-trip through settings.PlayerFilesPath.resolve().
        self.assertFalse(os.path.isabs(self.yaml_input_dir))
        self.assertNotEqual(Path(self.yaml_input_dir).resolve(), self.abs_input_dir)
        self.assertFalse(os.path.exists(self.yaml_input_dir))  # relative to user_path, not cwd

        from settings import get_settings
        resolved = get_settings().generator.PlayerFilesPath(str(self.yaml_input_dir)).resolve()
        self.assertEqual(Path(resolved), self.abs_input_dir)
        self.assertTrue(os.path.exists(resolved))

    def test_generate_absolute(self):
        sys.argv = [sys.argv[0], '--seed', '0',
                    '--player_files_path', str(self.abs_input_dir),
                    '--outputpath', self.output_tempdir.name]
        print(f'Testing Generate.py {sys.argv} in {os.getcwd()}')
        erargs = Generate.main()
        import Main  # deferred: see top-of-file note
        Main.main(*erargs)

        self.assertOutput(self.output_tempdir.name)

    def test_generate_relative(self):
        sys.argv = [sys.argv[0], '--seed', '0',
                    '--player_files_path', str(self.rel_input_dir),
                    '--outputpath', self.output_tempdir.name]
        print(f'Testing Generate.py {sys.argv} in {os.getcwd()}')
        erargs = Generate.main()
        import Main  # deferred: see top-of-file note
        Main.main(*erargs)

        self.assertOutput(self.output_tempdir.name)

    def test_generate_yaml(self):
        # override host.yaml
        from settings import get_settings
        from Utils import user_path, local_path
        settings = get_settings()
        # NOTE: until/unless we override settings.Group's setattr, we have to upcast the input dir here
        settings.generator.player_files_path = settings.generator.PlayerFilesPath(self.yaml_input_dir)
        settings.generator.players = 0
        settings._filename = None  # don't write to disk
        user_path_backup = user_path.cached_path
        user_path.cached_path = local_path()  # test yaml is actually in local_path
        try:
            sys.argv = [sys.argv[0], '--seed', '0',
                        '--outputpath', self.output_tempdir.name]
            print(f'Testing Generate.py {sys.argv} in {os.getcwd()}, player_files_path={self.yaml_input_dir}')
            erargs = Generate.main()
            import Main  # deferred: see top-of-file note
            Main.main(*erargs)
        finally:
            user_path.cached_path = user_path_backup

        self.assertOutput(self.output_tempdir.name)


class TestGenerateWeights(TestGenerateMain):
    """Tests Generate.py using a weighted file to generate for multiple players."""

    # this test will probably break if something in generation is changed that affects the seed before the weights get processed
    # can be fixed by changing the expected_results dict
    generate_dir = TestGenerateMain.generate_dir
    run_dir = TestGenerateMain.run_dir
    abs_input_dir = Path(__file__).parent / "data" / "weights"
    rel_input_dir = abs_input_dir.relative_to(run_dir)  # directly supplied relative paths are relative to cwd
    yaml_input_dir = abs_input_dir.relative_to(generate_dir)  # yaml paths are relative to user_path

    # don't need to run these tests
    test_generate_absolute = None
    test_generate_relative = None

    def test_generate_yaml(self):
        from settings import get_settings
        from Utils import user_path, local_path
        settings = get_settings()
        settings.generator.player_files_path = settings.generator.PlayerFilesPath(self.yaml_input_dir)
        settings.generator.players = 5  # arbitrary number, should be enough
        settings.generator.race = 0 # make sure race mode is disabled so the below seed is actually respected
        settings._filename = None
        user_path_backup = user_path.cached_path
        user_path.cached_path = local_path()
        try:
            sys.argv = [sys.argv[0], "--seed", "1"]
            namespace, seed = Generate.main()
        finally:
            user_path.cached_path = user_path_backup

        # there's likely a better way to do this, but hardcode the results from seed 1 to ensure they're always this
        expected_results = {
            "accessibility": [0, 2, 0, 2, 2],
            "progression_balancing": [0, 50, 99, 0, 50],
        }

        self.assertEqual(seed, 1)
        for option_name, results in expected_results.items():
            for player, result in enumerate(results, 1):
                self.assertEqual(
                    result, getattr(namespace, option_name)[player].value,
                    "Generated results from weights file did not match expected value."
                )


class TestGenerateArgAliases(unittest.TestCase):
    """Multi-word generator CLI flags accept both the hyphen and underscore form."""

    def test_hyphen_and_underscore_parse_equally(self):
        hyphen = Generate.mystery_argparse(
            ['--player-files-path', 'pfp', '--weights-file-path', 'w', '--meta-file-path', 'm',
             '--allow-quantity', '--skip-output', '--csv-output', '--skip-prog-balancing'])
        underscore = Generate.mystery_argparse(
            ['--player_files_path', 'pfp', '--weights_file_path', 'w', '--meta_file_path', 'm',
             '--allow_quantity', '--skip_output', '--csv_output', '--skip_prog_balancing'])
        self.assertEqual(vars(hyphen), vars(underscore))
        self.assertEqual(underscore.player_files_path, 'pfp')
        self.assertTrue(underscore.allow_quantity)
        self.assertTrue(underscore.skip_output)


# --yaml-options contract: the data source for mwgg-gui's YAML creator
# (yaml_creator/world_data.py) -- descriptor type strings, payload schema, the
# EXIT_NEEDS_RELOAD retry convention, and stdout purity.

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

# Both GUI widget factories (yaml_creator's option_widgets/weighted_widgets)
# switch on these exact type strings; a rename is a schema_version bump.
EMITTED_TYPES = frozenset({
    "toggle", "text_choice", "choice", "named_range", "range", "free_text",
    "item_set", "location_set", "option_counter", "option_set", "option_dict",
})

_DESCRIPTOR_REQUIRED_KEYS = {"name", "display_name", "docstring", "default", "type", "supports_weighting"}


class TestDescribeOptionBranches(unittest.TestCase):
    """Every _y_describe_option branch, incl. the subclass-order guards: the
    issubclass chain checks subclasses before their bases, so reordering it
    silently downgrades descriptors."""

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
    """Payload building blocks in-process against a real world (APQuest), at
    both GUI visibility levels."""

    def test_payload_schema_both_visibilities(self):
        from worlds.AutoWorld import AutoWorldRegister  # deferred: see top-of-file note
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
                # the whole payload must survive a JSON round-trip unchanged
                self.assertEqual(json.loads(json.dumps(payload)), payload)


class TestDumpYamlOptions(unittest.TestCase):
    """dump_yaml_options against the bootstrap-loaded APQuest world. The
    monkeypatches are mandatory: in-tree worlds have no pip dist-info, so the
    real installed/install path would reach the network from a test."""

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
        from worlds.AutoWorld import AutoWorldRegister  # deferred: see top-of-file note
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
        # the GUI wheel only retries on the literal 10 (world_data._EXIT_NEEDS_RELOAD)
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


# sys.argv is set BEFORE `import Generate` so the import-time sniff diverts
# stdout->stderr (untestable in-process); the world is queued before any
# `import worlds` so APQuest genuinely loads in-child.
_STDOUT_PURITY_CHILD = """\
import sys
sys.argv = ["Generate.py", "--yaml-options", "--game", "APQuest",
            "--module", "apquest", "--visibility", "simple"]
import Generate
import Utils
assert "worlds" not in sys.modules, "import Generate must not import the worlds package"
Utils._worlds_to_load.append("worlds.apquest")
# mandatory monkeypatches (no pip dist-info in-tree); no _JSON_OUT patch: the
# emit must reach the child's real stdout
Generate._y_world_installed = lambda module: True
Generate.set_game_names = lambda games, strict=False: None
sys.exit(Generate.dump_yaml_options("APQuest", "simple", "apquest"))
"""


class TestStdoutPuritySubprocess(unittest.TestCase):
    def test_stdout_is_exactly_one_ok_json_document(self):
        env = {
            **os.environ,
            # no network, no venv mutation from a test
            "SKIP_REQUIREMENTS_UPDATE": "1",
            "SKIP_ALL_INSTALLS": "1",
            # the child resolves the mwgg_igdb test stub (CI has no real package)
            "PYTHONPATH": os.pathsep.join(
                [os.path.join(REPO_ROOT, "test", "_stubs")]
                + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else [])),
        }
        result = subprocess.run(
            [sys.executable, "-c", _STDOUT_PURITY_CHILD],
            cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=300,
        )
        self.assertEqual(result.returncode, 0, msg=f"STDERR:\n{result.stderr[-2000:]}")
        # parsing the FULL stdout also asserts "exactly one document": any
        # stray byte (logging banner, world print) fails the parse
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"], msg=payload.get("error"))
        self.assertEqual(payload["game_name"], "APQuest")
        self.assertTrue(payload["groups"], "world did not genuinely load (empty groups)")


def _load_gui_world_data():
    """Load mwgg_gui/yaml_creator/world_data.py by file path; importing the
    package would boot the full Kivy GUI. None (-> skip) when the GUI wheel
    isn't installed (e.g. unittests.yml CI)."""
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
