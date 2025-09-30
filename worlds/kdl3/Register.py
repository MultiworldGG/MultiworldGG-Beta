from . import KDL3World,KDL3WebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Kirby World Registration

This file contains the metadata and class references for the kdl3 world.
"""

# Required metadata
WORLD_NAME = "kdl3"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = KDL3World
WEB_WORLD_CLASS = KDL3WebWorld
CLIENT_FUNCTION = None
