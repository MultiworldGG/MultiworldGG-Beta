from . import BalatroWebWorld, BalatroWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Balatro World Registration

This file contains the metadata and class references for the balatro world.
"""

# Required metadata
WORLD_NAME = "balatro"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = BalatroWorld
WEB_WORLD_CLASS = BalatroWebWorld
CLIENT_FUNCTION = None
