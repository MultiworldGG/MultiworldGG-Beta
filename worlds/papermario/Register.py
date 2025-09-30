from . import PaperMarioWorld
from . import PaperMarioWeb

"""
Paper Mario World Registration

This file contains the metadata and class references for the papermario world.
"""

# Required metadata
WORLD_NAME = "papermario"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PaperMarioWorld
WEB_WORLD_CLASS = PaperMarioWeb
CLIENT_FUNCTION = None
