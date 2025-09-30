from . import LegoStarWarsTCSWorld, LegoStarWarsTCSWebWorld
from .constants import GAME_NAME as from BaseUtils import get_archipelago_json()
game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Lego Star Wars: The Complete Saga is a 2007 compilation of the all Lego Star Wars series games. World Registration

This file contains the metadata and class references for the lego_star_wars_tcs world.
"""

# Required metadata
WORLD_NAME = "lego_star_wars_tcs"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = LegoStarWarsTCSWorld
WEB_WORLD_CLASS = LegoStarWarsTCSWebWorld
CLIENT_FUNCTION = None
