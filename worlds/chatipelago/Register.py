from . import ChatipelagoWorld
from . import ChatipelagoWeb

"""
Chat plays MultiworldGG! World Registration

This file contains the metadata and class references for the chatipelago world.
"""

# Required metadata
WORLD_NAME = "chatipelago"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ChatipelagoWorld
WEB_WORLD_CLASS = ChatipelagoWeb
CLIENT_FUNCTION = None
