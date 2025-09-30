from . import YachtDiceWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import YachtDiceWeb

"""
Yacht Dice is a straightforward game, custom-made for Archipelago, World Registration

This file contains the metadata and class references for the yachtdice world.
"""

# Required metadata
WORLD_NAME = "yachtdice"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = YachtDiceWorld
WEB_WORLD_CLASS = YachtDiceWeb
CLIENT_FUNCTION = None
