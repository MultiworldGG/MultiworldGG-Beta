from . import ChecksFinderWorld, ChecksFinderWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from .Client import launch

"""
ChecksFinder World Registration

This file contains the metadata and class references for the checksfinder world.
"""

# Required metadata
WORLD_NAME = "checksfinder"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ChecksFinderWorld
WEB_WORLD_CLASS = ChecksFinderWeb
CLIENT_FUNCTION = launch
