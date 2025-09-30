from . import GOIWorld, GOIWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Getting Over It World Registration

This file contains the metadata and class references for the getting_over_it world.
"""

# Required metadata
WORLD_NAME = "getting_over_it"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = GOIWorld
WEB_WORLD_CLASS = GOIWeb
CLIENT_FUNCTION = None
