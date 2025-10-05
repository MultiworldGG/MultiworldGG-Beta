from . import WordipelagoWebWorld, WordipelagoWorld

"""
Wordipelago World Registration

This file contains the metadata and class references for the wordipelago world.
"""

# Required metadata
WORLD_NAME = "wordipelago"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WordipelagoWorld
WEB_WORLD_CLASS = WordipelagoWebWorld
CLIENT_FUNCTION = None
