from . import KH1World, KH1Web
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from .Client import launch

"""
Kingdom Hearts World Registration

This file contains the metadata and class references for the kh1 world.
"""

# Required metadata
WORLD_NAME = "kh1"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = KH1World
WEB_WORLD_CLASS = KH1Web
CLIENT_FUNCTION = launch
