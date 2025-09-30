from . import FF4FEWorld, FF4FEWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Final Fantasy IV Free Enterprise World Registration

This file contains the metadata and class references for the ff4fe world.
"""

# Required metadata
WORLD_NAME = "ff4fe"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FF4FEWorld
WEB_WORLD_CLASS = FF4FEWebWorld
CLIENT_FUNCTION = None
