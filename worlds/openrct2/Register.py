from . import OpenRCT2World, OpenRCT2WebWorld
from .Client import launch

"""
OpenRCT2 World Registration

This file contains the metadata and class references for the openrct2 world.
"""

# Required metadata
WORLD_NAME = "openrct2"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OpenRCT2World
WEB_WORLD_CLASS = OpenRCT2WebWorld
CLIENT_FUNCTION = launch
