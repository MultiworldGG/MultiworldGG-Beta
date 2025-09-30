from . import WordipelagoWebWorld, WordipelagoWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Wordipelago World Registration

This file contains the metadata and class references for the wordipelago world.
"""

# Required metadata
WORLD_NAME = "wordipelago"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WordipelagoWorld
WEB_WORLD_CLASS = WordipelagoWebWorld
CLIENT_FUNCTION = None
