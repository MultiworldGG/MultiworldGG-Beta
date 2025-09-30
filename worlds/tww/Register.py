from . import TWWWorld, TWWWeb
from .TWWClient import launch

"""
Legend has it that whenever evil has appeared, a hero named Link has arisen to defeat it. The legend continues on World Registration

This file contains the metadata and class references for the tww world.
"""

# Required metadata
WORLD_NAME = "tww"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TWWWorld
WEB_WORLD_CLASS = TWWWeb
CLIENT_FUNCTION = launch
