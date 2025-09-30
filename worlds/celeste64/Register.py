from . import Celeste64WebWorld, Celeste64World

"""
Celeste 64 World Registration

This file contains the metadata and class references for the celeste64 world.
"""

# Required metadata
WORLD_NAME = "celeste64"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Celeste64World
WEB_WORLD_CLASS = Celeste64WebWorld
CLIENT_FUNCTION = None
