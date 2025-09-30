from . import Rac2World, Rac2Web
from .Rac2Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Ratchet & Clank 2 World Registration

This file contains the metadata and class references for the rac2 world.
"""

# Required metadata
WORLD_NAME = "rac2"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Rac2World
WEB_WORLD_CLASS = Rac2Web
CLIENT_FUNCTION = launch
