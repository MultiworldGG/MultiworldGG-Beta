from . import LandstalkerWorld, LandstalkerWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Landstalker - The Treasures of King Nole World Registration

This file contains the metadata and class references for the landstalker world.
"""

# Required metadata
WORLD_NAME = "landstalker"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = LandstalkerWorld
WEB_WORLD_CLASS = LandstalkerWeb
CLIENT_FUNCTION = None
