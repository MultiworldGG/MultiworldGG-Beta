from . import PhoaWorld, PhoaWebWorld

"""
Phoenotopia: Awakening World Registration

This file contains the metadata and class references for the phoa world.
"""

# Required metadata
WORLD_NAME = "phoa"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PhoaWorld
WEB_WORLD_CLASS = PhoaWebWorld
CLIENT_FUNCTION = None
