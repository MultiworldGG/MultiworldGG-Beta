from . import AnimalWellWorld, AnimalWellWeb
from .client.client import launch

"""
ANIMAL WELL World Registration

This file contains the metadata and class references for the animal_well world.
"""

# Required metadata
WORLD_NAME = "animal_well"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = AnimalWellWorld
WEB_WORLD_CLASS = AnimalWellWeb
CLIENT_FUNCTION = launch
