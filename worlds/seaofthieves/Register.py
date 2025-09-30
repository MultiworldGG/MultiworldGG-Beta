from . import SOTWorld, SOTWebWorld

"""
Sea of Thieves World Registration

This file contains the metadata and class references for the seaofthieves world.
"""

# Required metadata
WORLD_NAME = "seaofthieves"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SOTWorld
WEB_WORLD_CLASS = SOTWebWorld
CLIENT_FUNCTION = None
