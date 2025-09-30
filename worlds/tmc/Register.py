from . import MinishCapWorld, MinishCapWebWorld
from .constants import GAME_NAME as from BaseUtils import get_archipelago_json()
game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
The Minish Cap World Registration

This file contains the metadata and class references for the tmc world.
"""

# Required metadata
WORLD_NAME = "tmc"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MinishCapWorld
WEB_WORLD_CLASS = MinishCapWebWorld
CLIENT_FUNCTION = None
