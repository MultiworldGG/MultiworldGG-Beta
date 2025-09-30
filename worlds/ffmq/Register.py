from . import FFMQWorld, FFMQWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Final Fantasy Mystic Quest World Registration

This file contains the metadata and class references for the ffmq world.
"""

# Required metadata
WORLD_NAME = "ffmq"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FFMQWorld
WEB_WORLD_CLASS = FFMQWebWorld
CLIENT_FUNCTION = None
