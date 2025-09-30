from . import NoitaWorld, NoitaWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Noita World Registration

This file contains the metadata and class references for the noita world.
"""

# Required metadata
WORLD_NAME = "noita"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = NoitaWorld
WEB_WORLD_CLASS = NoitaWeb
CLIENT_FUNCTION = None
