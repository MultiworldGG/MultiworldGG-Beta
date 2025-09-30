from . import SimpsonsHitAndRunWorld, SimpsonsHitAndRunWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
The Simpsons Hit And Run World Registration

This file contains the metadata and class references for the simpsonshitnrun world.
"""

# Required metadata
WORLD_NAME = "simpsonshitnrun"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SimpsonsHitAndRunWorld
WEB_WORLD_CLASS = SimpsonsHitAndRunWeb
CLIENT_FUNCTION = None
