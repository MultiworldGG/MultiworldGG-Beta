from . import MMX3World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import MMX3Web

"""
Mega Man X3 World Registration

This file contains the metadata and class references for the mmx3 world.
"""

# Required metadata
WORLD_NAME = "mmx3"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MMX3World
WEB_WORLD_CLASS = MMX3Web
CLIENT_FUNCTION = None
