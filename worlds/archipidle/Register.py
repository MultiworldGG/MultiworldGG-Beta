from . import ArchipIDLEWorld, ArchipIDLEWebWorld

"""
ArchipIDLE World Registration

This file contains the metadata and class references for the archipidle world.
"""

# Required metadata
WORLD_NAME = "archipidle"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ArchipIDLEWorld
WEB_WORLD_CLASS = ArchipIDLEWebWorld
CLIENT_FUNCTION = None
