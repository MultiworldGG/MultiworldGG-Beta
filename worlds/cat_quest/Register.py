from . import CatQuestWorld, CatQuestWeb

"""
Cat Quest World Registration

This file contains the metadata and class references for the cat_quest world.
"""

# Required metadata
WORLD_NAME = "cat_quest"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CatQuestWorld
WEB_WORLD_CLASS = CatQuestWeb
CLIENT_FUNCTION = None
