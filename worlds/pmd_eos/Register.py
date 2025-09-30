from . import EOSWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import EOSWeb

"""
Pokemon Mystery Dungeon Explorers of Sky World Registration

This file contains the metadata and class references for the pmd_eos world.
"""

# Required metadata
WORLD_NAME = "pmd_eos"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = EOSWorld
WEB_WORLD_CLASS = EOSWeb
CLIENT_FUNCTION = None
