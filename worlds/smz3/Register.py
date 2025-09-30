from . import SMZ3World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import SMZ3Web

"""
SMZ3 World Registration

This file contains the metadata and class references for the smz3 world.
"""

# Required metadata
WORLD_NAME = "smz3"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SMZ3World
WEB_WORLD_CLASS = SMZ3Web
CLIENT_FUNCTION = None
