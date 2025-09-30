from . import MZMWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import MZMWeb

"""
Metroid: Zero Mission is a retelling of the first Metroid on NES. Relive Samus' first adventure on planet Zebes with World Registration

This file contains the metadata and class references for the mzm world.
"""

# Required metadata
WORLD_NAME = "mzm"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MZMWorld
WEB_WORLD_CLASS = MZMWeb
CLIENT_FUNCTION = None
