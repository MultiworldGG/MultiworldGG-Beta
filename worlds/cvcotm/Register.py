from . import CVCotMWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import CVCotMWeb

"""
Castlevania - Circle of the Moon World Registration

This file contains the metadata and class references for the cvcotm world.
"""

# Required metadata
WORLD_NAME = "cvcotm"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CVCotMWorld
WEB_WORLD_CLASS = CVCotMWeb
CLIENT_FUNCTION = None
