from . import DOOM2World
from . import DOOM2Web

"""
DOOM II World Registration

This file contains the metadata and class references for the doom_ii world.
"""

# Required metadata
WORLD_NAME = "doom_ii"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DOOM2World
WEB_WORLD_CLASS = DOOM2Web
CLIENT_FUNCTION = None
