from . import Spyro3World
from . import Spyro3Web

"""
Spyro 3 is a game about a purple dragon who likes eggs. World Registration

This file contains the metadata and class references for the spyro3 world.
"""

# Required metadata
WORLD_NAME = "spyro3"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Spyro3World
WEB_WORLD_CLASS = Spyro3Web
CLIENT_FUNCTION = None
