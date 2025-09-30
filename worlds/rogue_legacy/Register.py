from . import RLWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import RLWeb

"""
Rogue Legacy World Registration

This file contains the metadata and class references for the rogue_legacy world.
"""

# Required metadata
WORLD_NAME = "rogue_legacy"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = RLWorld
WEB_WORLD_CLASS = RLWeb
CLIENT_FUNCTION = None
