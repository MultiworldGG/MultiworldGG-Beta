from . import NineSolsWorld, NineSolsWebWorld

"""
Nine Sols World Registration

This file contains the metadata and class references for the nine_sols world.
"""

# Required metadata
WORLD_NAME = "nine_sols"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = NineSolsWorld
WEB_WORLD_CLASS = NineSolsWebWorld
CLIENT_FUNCTION = None
