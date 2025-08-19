from . import OriBlindForestWorld, OriBlindForestWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Ori and the Blind Forest World Registration

This file contains the metadata and class references for the oribf world.
"""

# Required metadata
WORLD_NAME = "oribf"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OriBlindForestWorld
WEB_WORLD_CLASS = OriBlindForestWebWorld
CLIENT_FUNCTION = None
