from . import Overcooked2World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import Overcooked2Web

"""
Overcooked! 2 World Registration

This file contains the metadata and class references for the overcooked2 world.
"""

# Required metadata
WORLD_NAME = "overcooked2"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Overcooked2World
WEB_WORLD_CLASS = Overcooked2Web
CLIENT_FUNCTION = None
