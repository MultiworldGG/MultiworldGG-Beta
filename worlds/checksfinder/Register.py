from . import ChecksFinderWorld, ChecksFinderWeb
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
from .Client import launch

"""
ChecksFinder World Registration

This file contains the metadata and class references for the checksfinder world.
"""

# Required metadata
WORLD_NAME = "checksfinder"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ChecksFinderWorld
WEB_WORLD_CLASS = ChecksFinderWeb
CLIENT_FUNCTION = launch
