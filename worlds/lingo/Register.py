from . import LingoWorld, LingoWebWorld

"""
Lingo World Registration

This file contains the metadata and class references for the lingo world.
"""

# Required metadata
WORLD_NAME = "lingo"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = LingoWorld
WEB_WORLD_CLASS = LingoWebWorld
CLIENT_FUNCTION = None
