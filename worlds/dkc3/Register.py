from . import DKC3World
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import DKC3Web

"""
Donkey Kong Country 3 is an action platforming game. World Registration

This file contains the metadata and class references for the dkc3 world.
"""

# Required metadata
WORLD_NAME = "dkc3"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DKC3World
WEB_WORLD_CLASS = DKC3Web
CLIENT_FUNCTION = None
