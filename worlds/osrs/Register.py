from . import OSRSWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import OSRSWeb

"""
Old School Runescape World Registration

This file contains the metadata and class references for the osrs world.
"""

# Required metadata
WORLD_NAME = "osrs"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OSRSWorld
WEB_WORLD_CLASS = OSRSWeb
CLIENT_FUNCTION = None
