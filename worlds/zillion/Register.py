from . import ZillionWebWorld, ZillionWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from .client import launch

"""
Zillion World Registration

This file contains the metadata and class references for the zillion world.
"""

# Required metadata
WORLD_NAME = "zillion"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ZillionWorld
WEB_WORLD_CLASS = ZillionWebWorld
CLIENT_FUNCTION = launch
