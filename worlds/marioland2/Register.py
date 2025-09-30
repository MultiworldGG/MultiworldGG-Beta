from . import MarioLand2World, MarioLand2WebWorld

"""
Super Mario Land 2 World Registration

This file contains the metadata and class references for the marioland2 world.
"""

# Required metadata
WORLD_NAME = "marioland2"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MarioLand2World
WEB_WORLD_CLASS = MarioLand2WebWorld
CLIENT_FUNCTION = None
