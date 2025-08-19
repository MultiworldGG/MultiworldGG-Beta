from . import ArchipIDLEWorld, ArchipIDLEWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
ArchipIDLE World Registration

This file contains the metadata and class references for the archipidle world.
"""

# Required metadata
WORLD_NAME = "archipidle"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ArchipIDLEWorld
WEB_WORLD_CLASS = ArchipIDLEWebWorld
CLIENT_FUNCTION = None
