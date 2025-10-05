from . import CVCotMWorld
from . import CVCotMWeb

"""
Castlevania - Circle of the Moon World Registration

This file contains the metadata and class references for the cvcotm world.
"""

# Required metadata
WORLD_NAME = "cvcotm"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CVCotMWorld
WEB_WORLD_CLASS = CVCotMWeb
CLIENT_FUNCTION = None
