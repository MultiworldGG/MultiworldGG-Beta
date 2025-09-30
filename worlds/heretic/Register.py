from . import HereticWorld, HereticWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Heretic World Registration

This file contains the metadata and class references for the heretic world.
"""

# Required metadata
WORLD_NAME = "heretic"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = HereticWorld
WEB_WORLD_CLASS = HereticWeb
CLIENT_FUNCTION = None
