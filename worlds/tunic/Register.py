from . import TunicWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import TunicWeb

"""
TUNIC World Registration

This file contains the metadata and class references for the tunic world.
"""

# Required metadata
WORLD_NAME = "tunic"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TunicWorld
WEB_WORLD_CLASS = TunicWeb
CLIENT_FUNCTION = None
