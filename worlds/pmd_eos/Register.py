from . import EOSWorld
from . import EOSWeb

"""
Pokemon Mystery Dungeon Explorers of Sky World Registration

This file contains the metadata and class references for the pmd_eos world.
"""

# Required metadata
WORLD_NAME = "pmd_eos"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = EOSWorld
WEB_WORLD_CLASS = EOSWeb
CLIENT_FUNCTION = None
