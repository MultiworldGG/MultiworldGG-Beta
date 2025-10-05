from . import GSTLAWorld
from . import GSTLAWeb

"""
Golden Sun The Lost Age World Registration

This file contains the metadata and class references for the gstla world.
"""

# Required metadata
WORLD_NAME = "gstla"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = GSTLAWorld
WEB_WORLD_CLASS = GSTLAWeb
CLIENT_FUNCTION = None
