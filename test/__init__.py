import pathlib
import warnings
import os

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

# Load all worlds upfront for testing
from mwgg_gui.game_index import GameIndex
all_game_names = GameIndex.get_all_game_names()
Utils.set_game_names(all_game_names)
