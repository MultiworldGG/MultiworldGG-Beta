from . import ZillionWebWorld, ZillionWorld
from .client import launch

"""
Zillion World Registration

This file contains the metadata and class references for the zillion world.
"""

# Required metadata
WORLD_NAME = "zillion"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ZillionWorld
WEB_WORLD_CLASS = ZillionWebWorld
CLIENT_FUNCTION = launch
