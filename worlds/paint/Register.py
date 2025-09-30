from . import PaintWorld, PaintWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Paint World Registration

This file contains the metadata and class references for the paint world.
"""

# Required metadata
WORLD_NAME = "paint"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PaintWorld
WEB_WORLD_CLASS = PaintWebWorld
CLIENT_FUNCTION = None
