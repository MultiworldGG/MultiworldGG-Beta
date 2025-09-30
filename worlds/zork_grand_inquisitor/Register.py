from .world import ZorkGrandInquisitorWorld, ZorkGrandInquisitorWebWorld
from .client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Zork Grand Inquisitor World Registration

This file contains the metadata and class references for the zork_grand_inquisitor world.
"""

# Required metadata
WORLD_NAME = "zork_grand_inquisitor"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ZorkGrandInquisitorWorld
WEB_WORLD_CLASS = ZorkGrandInquisitorWebWorld
CLIENT_FUNCTION = launch
