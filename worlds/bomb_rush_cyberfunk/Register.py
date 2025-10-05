from . import BombRushCyberfunkWorld
from . import BombRushCyberfunkWeb

"""
Bomb Rush Cyberfunk World Registration

This file contains the metadata and class references for the bomb_rush_cyberfunk world.
"""

# Required metadata
WORLD_NAME = "bomb_rush_cyberfunk"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = BombRushCyberfunkWorld
WEB_WORLD_CLASS = BombRushCyberfunkWeb
CLIENT_FUNCTION = None
