from . import ArchipIDLEWorld, ArchipIDLEWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

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
