from . import Hylics2World
from . import Hylics2Web

"""
Hylics 2 is a surreal and unusual RPG, with a bizarre yet unique visual style. Play as Wayne, World Registration

This file contains the metadata and class references for the hylics2 world.
"""

# Required metadata
WORLD_NAME = "hylics2"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Hylics2World
WEB_WORLD_CLASS = Hylics2Web
CLIENT_FUNCTION = None
