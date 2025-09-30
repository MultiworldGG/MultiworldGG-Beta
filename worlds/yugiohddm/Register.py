from . import YGODDMWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import YGODDMWeb

"""
Yu-Gi-Oh! Dungeon Dice Monsters is a Game Boy Advance dice-based tactics game based on an original board game World Registration

This file contains the metadata and class references for the yugiohddm world.
"""

# Required metadata
WORLD_NAME = "yugiohddm"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = YGODDMWorld
WEB_WORLD_CLASS = YGODDMWeb
CLIENT_FUNCTION = None
