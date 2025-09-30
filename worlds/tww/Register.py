from . import TWWWorld, TWWWeb
from .TWWClient import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Legend has it that whenever evil has appeared, a hero named Link has arisen to defeat it. The legend continues on World Registration

This file contains the metadata and class references for the tww world.
"""

# Required metadata
WORLD_NAME = "tww"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TWWWorld
WEB_WORLD_CLASS = TWWWeb
CLIENT_FUNCTION = launch
