from . import DKC2World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import DKC2Web

"""
Donkey Kong Country 2 World Registration

This file contains the metadata and class references for the dkc2 world.
"""

# Required metadata
WORLD_NAME = "dkc2"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DKC2World
WEB_WORLD_CLASS = DKC2Web
CLIENT_FUNCTION = None
