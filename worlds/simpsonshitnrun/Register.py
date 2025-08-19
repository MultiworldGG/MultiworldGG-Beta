from . import SimpsonsHitAndRunWorld, SimpsonsHitAndRunWeb
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
The Simpsons Hit And Run World Registration

This file contains the metadata and class references for the simpsonshitnrun world.
"""

# Required metadata
WORLD_NAME = "simpsonshitnrun"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SimpsonsHitAndRunWorld
WEB_WORLD_CLASS = SimpsonsHitAndRunWeb
CLIENT_FUNCTION = None
