from . import MM3WebWorld, MM3World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Mega Man 3 World Registration

This file contains the metadata and class references for the mm3 world.
"""

# Required metadata
WORLD_NAME = "mm3"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MM3World
WEB_WORLD_CLASS = MM3WebWorld
CLIENT_FUNCTION = None
