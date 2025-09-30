from . import Yugioh06World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import Yugioh06Web

"""
Yu-Gi-Oh! 2006 World Registration

This file contains the metadata and class references for the yugioh06 world.
"""

# Required metadata
WORLD_NAME = "yugioh06"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Yugioh06World
WEB_WORLD_CLASS = Yugioh06Web
CLIENT_FUNCTION = None
