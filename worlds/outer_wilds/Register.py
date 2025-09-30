from . import OuterWildsWorld, OuterWildsWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Outer Wilds World Registration

This file contains the metadata and class references for the outer_wilds world.
"""

# Required metadata
WORLD_NAME = "outer_wilds"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OuterWildsWorld
WEB_WORLD_CLASS = OuterWildsWebWorld
CLIENT_FUNCTION = None
