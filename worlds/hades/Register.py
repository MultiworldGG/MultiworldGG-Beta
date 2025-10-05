from . import HadesWorld, HadesWeb
from .Client import launch

"""
Hades World Registration

This file contains the metadata and class references for the hades world.
"""

# Required metadata
WORLD_NAME = "hades"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = HadesWorld
WEB_WORLD_CLASS = HadesWeb
CLIENT_FUNCTION = launch
