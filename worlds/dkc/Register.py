from . import DKCWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import DKCWeb

"""
Donkey Kong Country World Registration

This file contains the metadata and class references for the dkc world.
"""

# Required metadata
WORLD_NAME = "dkc"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DKCWorld
WEB_WORLD_CLASS = DKCWeb
CLIENT_FUNCTION = None
