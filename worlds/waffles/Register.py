from . import WaffleWorld, WaffleWeb

"""
Spicy Mycena Waffles World Registration

This file contains the metadata and class references for the waffles world.
"""

# Required metadata
WORLD_NAME = "waffles"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WaffleWorld
WEB_WORLD_CLASS = WaffleWeb
CLIENT_FUNCTION = None
