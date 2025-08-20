from . import FactorioWorld, FactorioWeb
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
from .Client import launch

"""
Factorio Saws World Registration

This file contains the metadata and class references for the factorio_saws world.
"""

# Required metadata
WORLD_NAME = "factorio_saws"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FactorioWorld
WEB_WORLD_CLASS = FactorioWeb
CLIENT_FUNCTION = launch
