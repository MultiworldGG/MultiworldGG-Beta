from . import MadouWorld, MadouWeb

"""
Madou World Registration

This file contains the metadata and class references for the madou world.
"""

# Required metadata
WORLD_NAME = "madou"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MadouWorld
WEB_WORLD_CLASS = MadouWeb
CLIENT_FUNCTION = None
