from . import BalatroWebWorld, BalatroWorld

"""
Balatro World Registration

This file contains the metadata and class references for the balatro world.
"""

# Required metadata
WORLD_NAME = "balatro"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = BalatroWorld
WEB_WORLD_CLASS = BalatroWebWorld
CLIENT_FUNCTION = None
