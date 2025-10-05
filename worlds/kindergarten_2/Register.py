from . import Kindergarten2World, Kindergarten2WebWorld

"""
Kindergarten 2 World Registration

This file contains the metadata and class references for the kindergarten_2 world.
"""

# Required metadata
WORLD_NAME = "kindergarten_2"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Kindergarten2World
WEB_WORLD_CLASS = Kindergarten2WebWorld
CLIENT_FUNCTION = None
