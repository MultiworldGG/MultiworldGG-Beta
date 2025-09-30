from . import Celeste64WebWorld, Celeste64World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Celeste 64 World Registration

This file contains the metadata and class references for the celeste64 world.
"""

# Required metadata
WORLD_NAME = "celeste64"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Celeste64World
WEB_WORLD_CLASS = Celeste64WebWorld
CLIENT_FUNCTION = None
