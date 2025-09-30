from . import WitnessWorld, WitnessWebWorld

"""
The Witness World Registration

This file contains the metadata and class references for the witness world.
"""

# Required metadata
WORLD_NAME = "witness"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WitnessWorld
WEB_WORLD_CLASS = WitnessWebWorld
CLIENT_FUNCTION = None
