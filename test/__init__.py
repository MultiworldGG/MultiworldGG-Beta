import pathlib
import sys
import warnings
import os
import json

# Mount the in-repo mwgg_igdb stub for EVERY entrypoint that imports this package
# (pytest collection AND a direct `python test/...` run such as the hosting job,
# which never loads the pytest-only rootdir conftest.py). Must run before any
# `from mwgg_igdb import ...` below or in settings/Utils/WebHost imports. Mirrors
# (and supersedes) conftest.py; both guards are idempotent. See test/_stubs/mwgg_igdb.py.
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

# In test mode we use a stub mwgg_igdb (see test/_stubs/mwgg_igdb.py, mounted on
# sys.path by src/conftest.py) and skip Utils.set_game_names — its pip-install
# path doesn't apply to worlds that live as source directories in the repo.
# Instead, register every world physically present under worlds/ that ships an
# archipelago.json (infra worlds like _debug, _manual, _bizhawk, etc.) with the
# stub GameIndex and append them to the loader's _worlds_to_load list directly,
# so worlds/__init__.py picks them up.
from mwgg_igdb import GameIndex

# AP_TEST_WORLDS (pytest only) scopes the bootstrap to the named worlds; the suite's
# fixture worlds are always registered for shared fixtures but aren't themselves worlds
# under test (_debug backs the item-link unit tests; generic and tracker are additionally
# always loaded via the Utils._worlds_to_load baseline).
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

# Load the registered worlds and snapshot the worlds under test (a copy, so tests
# reassigning world_types can't leak in), dropping the force-loaded fixtures unless they
# were explicitly requested. Upstream defines AutoWorldRegister.testable_worlds in
# worlds/AutoWorld.py + worlds/__init__.py; beta's loader is driven by the
# _worlds_to_load list this bootstrap populates, so the snapshot lives here instead.
from worlds.AutoWorld import AutoWorldRegister

if _requested_worlds:
    AutoWorldRegister.testable_worlds = {
        game: world for game, world in AutoWorldRegister.world_types.items()
        if pathlib.Path(world.__file__).parent.name in _requested_worlds
    }
else:
    AutoWorldRegister.testable_worlds = dict(AutoWorldRegister.world_types)
