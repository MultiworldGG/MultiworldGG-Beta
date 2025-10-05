from . import OsuWorld, OsuWebWorld
from .Client import launch

"""
osu! is a free to play rhythm game featuring 4 modes, an online ranking system/statistics, World Registration

This file contains the metadata and class references for the osu world.
"""

# Required metadata
WORLD_NAME = "osu"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OsuWorld
WEB_WORLD_CLASS = OsuWebWorld
CLIENT_FUNCTION = launch
