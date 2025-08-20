from . import MetroidPrimeWorld, MetroidPrimeWeb
from .MetroidPrimeClient import launch
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Metroid Prime World Registration

This file contains the metadata and class references for the metroidprime world.
"""

# Required metadata
WORLD_NAME = "metroidprime"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MetroidPrimeWorld
WEB_WORLD_CLASS = MetroidPrimeWeb
CLIENT_FUNCTION = launch
