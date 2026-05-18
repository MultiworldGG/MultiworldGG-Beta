import pathlib
import warnings
import os
import json

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
worlds_dir = file_path / "worlds"
for entry in sorted(worlds_dir.iterdir()):
    manifest_path = entry / "archipelago.json"
    if not entry.is_dir() or not manifest_path.exists():
        continue
    manifest = json.loads(manifest_path.read_text())
    index_entry = dict(manifest)
    index_entry["game_name"] = manifest.get("game", entry.name)
    GameIndex.add_game(entry.name, index_entry)
    Utils._worlds_to_load.append(f"worlds.{entry.name}")
