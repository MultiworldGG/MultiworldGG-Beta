from . import SMOWorld, SMOWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
from .Connector.Client import launch

"""
Super Mario Odyssey World Registration

This file contains the metadata and class references for the smo world.
"""

# Required metadata
WORLD_NAME = "smo"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SMOWorld
WEB_WORLD_CLASS = SMOWebWorld
CLIENT_FUNCTION = launch
