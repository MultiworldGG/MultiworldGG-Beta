from . import CupheadWorld, CupheadWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Log options that are overridden from incompatible combinations to console. World Registration

This file contains the metadata and class references for the cuphead world.
"""

# Required metadata
WORLD_NAME = "cuphead"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CupheadWorld
WEB_WORLD_CLASS = CupheadWebWorld
CLIENT_FUNCTION = None
