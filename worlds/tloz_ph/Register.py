from . import PhantomHourglassWorld, PhantomHourglassWeb
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
The Legend of Zelda - Phantom Hourglass World Registration

This file contains the metadata and class references for the tloz_ph world.
"""

# Required metadata
WORLD_NAME = "tloz_ph"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PhantomHourglassWorld
WEB_WORLD_CLASS = PhantomHourglassWeb
CLIENT_FUNCTION = None
