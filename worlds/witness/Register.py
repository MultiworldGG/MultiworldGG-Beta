from . import WitnessWorld, WitnessWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
The Witness World Registration

This file contains the metadata and class references for the witness world.
"""

# Required metadata
WORLD_NAME = "witness"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WitnessWorld
WEB_WORLD_CLASS = WitnessWebWorld
CLIENT_FUNCTION = None
