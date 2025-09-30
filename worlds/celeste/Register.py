from . import CelesteWebWorld, CelesteWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Celeste World Registration

This file contains the metadata and class references for the celeste world.
"""

# Required metadata
WORLD_NAME = "celeste"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CelesteWorld
WEB_WORLD_CLASS = CelesteWebWorld
CLIENT_FUNCTION = None
