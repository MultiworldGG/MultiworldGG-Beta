from . import Overcooked2World
from . import Overcooked2Web

"""
Overcooked! 2 World Registration

This file contains the metadata and class references for the overcooked2 world.
"""

# Required metadata
WORLD_NAME = "overcooked2"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Overcooked2World
WEB_WORLD_CLASS = Overcooked2Web
CLIENT_FUNCTION = None
