from . import SpireWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import SpireWeb

"""
Slay the Spire World Registration

This file contains the metadata and class references for the spire world.
"""

# Required metadata
WORLD_NAME = "spire"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SpireWorld
WEB_WORLD_CLASS = SpireWeb
CLIENT_FUNCTION = None
