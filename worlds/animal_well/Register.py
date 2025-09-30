from . import AnimalWellWorld, AnimalWellWeb
from .client.client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
ANIMAL WELL World Registration

This file contains the metadata and class references for the animal_well world.
"""

# Required metadata
WORLD_NAME = "animal_well"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = AnimalWellWorld
WEB_WORLD_CLASS = AnimalWellWeb
CLIENT_FUNCTION = launch
