from . import SimpsonsHitAndRunWorld, SimpsonsHitAndRunWeb

"""
The Simpsons Hit And Run World Registration

This file contains the metadata and class references for the simpsonshitnrun world.
"""

# Required metadata
WORLD_NAME = "simpsonshitnrun"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SimpsonsHitAndRunWorld
WEB_WORLD_CLASS = SimpsonsHitAndRunWeb
CLIENT_FUNCTION = None
