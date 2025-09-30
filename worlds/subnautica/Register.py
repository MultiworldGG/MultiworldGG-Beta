from . import SubnauticaWorld, SubnauticaWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Subnautica World Registration

This file contains the metadata and class references for the subnautica world.
"""

# Required metadata
WORLD_NAME = "subnautica"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SubnauticaWorld
WEB_WORLD_CLASS = SubnauticaWeb
CLIENT_FUNCTION = None
