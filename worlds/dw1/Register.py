from . import DigimonWorldWorld
from . import DigimonWorldWeb

"""
Digimon World is a game about raising digital monsters and recruiting allies to save the digital world. World Registration

This file contains the metadata and class references for the dw1 world.
"""

# Required metadata
WORLD_NAME = "dw1"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DigimonWorldWorld
WEB_WORLD_CLASS = DigimonWorldWeb
CLIENT_FUNCTION = None
