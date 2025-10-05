from . import MomodoraWorld
from . import MomodoraWeb

"""
Momodora Moonlit Farewell World Registration

This file contains the metadata and class references for the momodoramoonlitfarewell world.
"""

# Required metadata
WORLD_NAME = "momodoramoonlitfarewell"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MomodoraWorld
WEB_WORLD_CLASS = MomodoraWeb
CLIENT_FUNCTION = None
