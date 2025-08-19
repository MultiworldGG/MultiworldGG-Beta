from . import FFMQWorld, FFMQWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Final Fantasy Mystic Quest World Registration

This file contains the metadata and class references for the ffmq world.
"""

# Required metadata
WORLD_NAME = "ffmq"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FFMQWorld
WEB_WORLD_CLASS = FFMQWebWorld
CLIENT_FUNCTION = None
