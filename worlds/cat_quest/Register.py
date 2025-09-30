from . import CatQuestWorld, CatQuestWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Cat Quest World Registration

This file contains the metadata and class references for the cat_quest world.
"""

# Required metadata
WORLD_NAME = "cat_quest"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CatQuestWorld
WEB_WORLD_CLASS = CatQuestWeb
CLIENT_FUNCTION = None
