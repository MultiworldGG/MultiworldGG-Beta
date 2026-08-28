import pathlib
import sys
import warnings
import os
import json

# Mount the test mwgg_igdb stub before any mwgg_igdb import; direct `python
# test/...` runs (the hosting job) never load the pytest-only conftest.py.
_stub_dir = str(pathlib.Path(__file__).parent / "_stubs")
if _stub_dir not in sys.path:
    sys.path.insert(0, _stub_dir)

# Set Kivy environment variables before any imports to prevent GUI initialization
os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_LOG_ENABLE"] = "0"
os.environ["KIVY_WINDOW"] = "sdl2,headless"

import settings

warnings.simplefilter("always")
warnings.filterwarnings(action="ignore", category=DeprecationWarning, module="s2clientprotocol")
settings.no_gui = True
settings.skip_autosave = True

import ModuleUpdate

ModuleUpdate.update_ran = True  # don't upgrade

import Utils

file_path = pathlib.Path(__file__).parent.parent
Utils.local_path.cached_path = file_path
Utils.user_path()  # initialize cached_path

# set_game_names' pip-install path doesn't apply to in-repo source worlds; register
# each worlds/ dir with an archipelago.json into the stub GameIndex and _worlds_to_load.
from mwgg_igdb import GameIndex

# AP_TEST_WORLDS (pytest only) scopes the bootstrap; fixture worlds are always
# registered for shared fixtures but aren't themselves under test.
_SUITE_FIXTURE_WORLDS = {"generic", "apquest", "_debug"}
_test_worlds_env = os.environ.get("AP_TEST_WORLDS") if "pytest" in sys.modules else None
_requested_worlds = {name.strip() for name in _test_worlds_env.split(",") if name.strip()} if _test_worlds_env else None
test_worlds_filter = _requested_worlds | _SUITE_FIXTURE_WORLDS if _requested_worlds else None

worlds_dir = file_path / "worlds"
for entry in sorted(worlds_dir.iterdir()):
    manifest_path = entry / "archipelago.json"
    if not entry.is_dir() or not manifest_path.exists():
        continue
    if test_worlds_filter is not None and entry.name not in test_worlds_filter:
        continue
    manifest = json.loads(manifest_path.read_text())
    index_entry = dict(manifest)
    index_entry["game_name"] = manifest.get("game", entry.name)
    GameIndex.add_game(entry.name, index_entry)
    Utils._worlds_to_load.append(f"worlds.{entry.name}")

# Snapshot testable_worlds (a copy: world_types reassignment can't leak). pytest-only:
# importing worlds in the hosting job's MultiHoster children trips customserver's
# "Worlds system should not be loaded" guard.
if "pytest" in sys.modules:
    from worlds.AutoWorld import AutoWorldRegister

    if _requested_worlds:
        AutoWorldRegister.testable_worlds = {
            game: world for game, world in AutoWorldRegister.world_types.items()
            if pathlib.Path(world.__file__).parent.name in _requested_worlds
        }
    else:
        AutoWorldRegister.testable_worlds = dict(AutoWorldRegister.world_types)
