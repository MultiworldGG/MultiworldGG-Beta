from . import ChainedEchoesWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import ChainedEchoesWeb

"""
Chained Echoes World Registration

This file contains the metadata and class references for the chainedechoes world.
"""

# Required metadata
WORLD_NAME = "chainedechoes"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ChainedEchoesWorld
WEB_WORLD_CLASS = ChainedEchoesWeb
CLIENT_FUNCTION = None
