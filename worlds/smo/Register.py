from . import SMOWorld, SMOWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from .Connector.Client import launch

"""
Super Mario Odyssey World Registration

This file contains the metadata and class references for the smo world.
"""

# Required metadata
WORLD_NAME = "smo"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SMOWorld
WEB_WORLD_CLASS = SMOWebWorld
CLIENT_FUNCTION = launch
