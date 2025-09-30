from . import FFTAWorld, FFTAWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

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
