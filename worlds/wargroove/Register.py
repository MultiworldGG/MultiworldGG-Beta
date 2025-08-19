from . import WargrooveWorld, WargrooveWeb
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
from .Client import launch

"""
Wargroove World Registration

This file contains the metadata and class references for the wargroove world.
"""

# Required metadata
WORLD_NAME = "wargroove"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = WargrooveWorld
WEB_WORLD_CLASS = WargrooveWeb
CLIENT_FUNCTION = launch
