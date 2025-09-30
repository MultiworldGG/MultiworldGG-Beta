from . import BombRushCyberfunkWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import BombRushCyberfunkWeb

"""
Bomb Rush Cyberfunk World Registration

This file contains the metadata and class references for the bomb_rush_cyberfunk world.
"""

# Required metadata
WORLD_NAME = "bomb_rush_cyberfunk"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = BombRushCyberfunkWorld
WEB_WORLD_CLASS = BombRushCyberfunkWeb
CLIENT_FUNCTION = None
