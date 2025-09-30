from . import FF4FEWorld, FF4FEWebWorld

"""
Final Fantasy IV Free Enterprise World Registration

This file contains the metadata and class references for the ff4fe world.
"""

# Required metadata
WORLD_NAME = "ff4fe"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FF4FEWorld
WEB_WORLD_CLASS = FF4FEWebWorld
CLIENT_FUNCTION = None
