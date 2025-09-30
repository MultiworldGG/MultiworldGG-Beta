from . import MLSSWorld, MLSSWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

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
