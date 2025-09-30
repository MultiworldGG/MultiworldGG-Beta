from . import MomodoraWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import MomodoraWeb

"""
Momodora Moonlit Farewell World Registration

This file contains the metadata and class references for the momodoramoonlitfarewell world.
"""

# Required metadata
WORLD_NAME = "momodoramoonlitfarewell"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MomodoraWorld
WEB_WORLD_CLASS = MomodoraWeb
CLIENT_FUNCTION = None
