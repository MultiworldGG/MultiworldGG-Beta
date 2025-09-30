from . import WargrooveWorld, WargrooveWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from .Client import launch

"""
Wargroove World Registration

This file contains the metadata and class references for the wargroove world.
"""

# Required metadata
WORLD_NAME = "wargroove"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WargrooveWorld
WEB_WORLD_CLASS = WargrooveWeb
CLIENT_FUNCTION = launch
