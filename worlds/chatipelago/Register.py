from . import ChatipelagoWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import ChatipelagoWeb

"""
Chat plays MultiworldGG! World Registration

This file contains the metadata and class references for the chatipelago world.
"""

# Required metadata
WORLD_NAME = "chatipelago"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ChatipelagoWorld
WEB_WORLD_CLASS = ChatipelagoWeb
CLIENT_FUNCTION = None
