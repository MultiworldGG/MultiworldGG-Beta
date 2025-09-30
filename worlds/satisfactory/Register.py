from . import SatisfactoryWorld, SatisfactoryWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Satisfactory World Registration

This file contains the metadata and class references for the satisfactory world.
"""

# Required metadata
WORLD_NAME = "satisfactory"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SatisfactoryWorld
WEB_WORLD_CLASS = SatisfactoryWebWorld
CLIENT_FUNCTION = None
