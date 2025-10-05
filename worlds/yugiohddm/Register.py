from . import YGODDMWorld
from . import YGODDMWeb

"""
Yu-Gi-Oh! Dungeon Dice Monsters is a Game Boy Advance dice-based tactics game based on an original board game World Registration

This file contains the metadata and class references for the yugiohddm world.
"""

# Required metadata
WORLD_NAME = "yugiohddm"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = YGODDMWorld
WEB_WORLD_CLASS = YGODDMWeb
CLIENT_FUNCTION = None
