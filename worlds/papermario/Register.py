from . import PaperMarioWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import PaperMarioWeb

"""
Paper Mario World Registration

This file contains the metadata and class references for the papermario world.
"""

# Required metadata
WORLD_NAME = "papermario"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PaperMarioWorld
WEB_WORLD_CLASS = PaperMarioWeb
CLIENT_FUNCTION = None
