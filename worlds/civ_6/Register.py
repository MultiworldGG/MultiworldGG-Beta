from . import CivVIWorld, CivVIWeb
from .Civ6Client import launch

"""
Civilization VI World Registration

This file contains the metadata and class references for the civ_6 world.
"""

# Required metadata
WORLD_NAME = "civ_6"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = CivVIWorld
WEB_WORLD_CLASS = CivVIWeb
CLIENT_FUNCTION = launch
