from . import DLCqworld, DLCqwebworld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Dlcquest World Registration

This file contains the metadata and class references for the dlcquest world.
"""

# Required metadata
WORLD_NAME = "dlcquest"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DLCqworld
WEB_WORLD_CLASS = DLCqwebworld
CLIENT_FUNCTION = None
