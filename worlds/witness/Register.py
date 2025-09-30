from . import WitnessWorld, WitnessWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

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
