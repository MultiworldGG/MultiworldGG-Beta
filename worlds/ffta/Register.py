from . import FFTAWorld, FFTAWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Final Fantasy Tactics Advance World Registration

This file contains the metadata and class references for the ffta world.
"""

# Required metadata
WORLD_NAME = "ffta"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FFTAWorld
WEB_WORLD_CLASS = FFTAWebWorld
CLIENT_FUNCTION = None
