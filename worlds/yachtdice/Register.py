from . import YachtDiceWorld
from . import YachtDiceWeb

"""
Yacht Dice is a straightforward game, custom-made for Archipelago, World Registration

This file contains the metadata and class references for the yachtdice world.
"""

# Required metadata
WORLD_NAME = "yachtdice"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = YachtDiceWorld
WEB_WORLD_CLASS = YachtDiceWeb
CLIENT_FUNCTION = None
