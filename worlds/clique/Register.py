from . import CliqueWebWorld, CliqueWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Clique World Registration

This file contains the metadata and class references for the clique world.
"""

# Required metadata
WORLD_NAME = "clique"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CliqueWorld
WEB_WORLD_CLASS = CliqueWebWorld
CLIENT_FUNCTION = None
