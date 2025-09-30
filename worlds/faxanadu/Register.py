from . import FaxanaduWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import FaxanaduWeb

"""
Faxanadu World Registration

This file contains the metadata and class references for the faxanadu world.
"""

# Required metadata
WORLD_NAME = "faxanadu"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FaxanaduWorld
WEB_WORLD_CLASS = FaxanaduWeb
CLIENT_FUNCTION = None
