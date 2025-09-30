from . import HatInTimeWorld, AWebInTime
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from .Client import launch

"""
A Hat in Time World Registration

This file contains the metadata and class references for the ahit world.
"""

# Required metadata
WORLD_NAME = "ahit"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = HatInTimeWorld
WEB_WORLD_CLASS = AWebInTime
CLIENT_FUNCTION = main
