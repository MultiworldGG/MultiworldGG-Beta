from . import MLSSWorld, MLSSWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Mario & Luigi Superstar Saga World Registration

This file contains the metadata and class references for the mlss world.
"""

# Required metadata
WORLD_NAME = "mlss"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MLSSWorld
WEB_WORLD_CLASS = MLSSWebWorld
CLIENT_FUNCTION = None
