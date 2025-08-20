from .world import ZorkGrandInquisitorWorld, ZorkGrandInquisitorWebWorld
from .client import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

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
