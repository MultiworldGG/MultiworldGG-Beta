from . import DOOM1993World
from . import DOOM1993Web

"""
DOOM 1993 World Registration

This file contains the metadata and class references for the doom_1993 world.
"""

# Required metadata
WORLD_NAME = "doom_1993"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DOOM1993World
WEB_WORLD_CLASS = DOOM1993Web
CLIENT_FUNCTION = None
