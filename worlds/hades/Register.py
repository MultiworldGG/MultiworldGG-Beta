from . import HadesWorld, HadesWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from .Client import launch

"""
Hades World Registration

This file contains the metadata and class references for the hades world.
"""

# Required metadata
WORLD_NAME = "hades"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = HadesWorld
WEB_WORLD_CLASS = HadesWeb
CLIENT_FUNCTION = launch
