from . import MuseDashWorld, MuseDashWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Muse Dash World Registration

This file contains the metadata and class references for the musedash world.
"""

# Required metadata
WORLD_NAME = "musedash"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MuseDashWorld
WEB_WORLD_CLASS = MuseDashWebWorld
CLIENT_FUNCTION = None
