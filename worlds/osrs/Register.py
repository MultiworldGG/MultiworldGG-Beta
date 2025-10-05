from . import OSRSWorld
from . import OSRSWeb

"""
Old School Runescape World Registration

This file contains the metadata and class references for the osrs world.
"""

# Required metadata
WORLD_NAME = "osrs"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OSRSWorld
WEB_WORLD_CLASS = OSRSWeb
CLIENT_FUNCTION = None
