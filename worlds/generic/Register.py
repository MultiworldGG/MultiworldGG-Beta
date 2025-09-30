from . import GenericWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import GenericWeb

"""
Generic World Registration

This file contains the metadata and class references for the generic world.
"""

# Required metadata
WORLD_NAME = "generic"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = GenericWorld
WEB_WORLD_CLASS = GenericWeb
CLIENT_FUNCTION = None
