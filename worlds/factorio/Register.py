from . import FactorioWorld, FactorioWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from .Client import launch

"""
Factorio World Registration

This file contains the metadata and class references for the factorio world.
"""

# Required metadata
WORLD_NAME = "factorio"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FactorioWorld
WEB_WORLD_CLASS = FactorioWeb
CLIENT_FUNCTION = launch
