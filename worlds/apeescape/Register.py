from . import ApeEscapeWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import ApeEscapeWeb

"""
Ape Escape World Registration

This file contains the metadata and class references for the apeescape world.
"""

# Required metadata
WORLD_NAME = "apeescape"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ApeEscapeWorld
WEB_WORLD_CLASS = ApeEscapeWeb
CLIENT_FUNCTION = None
