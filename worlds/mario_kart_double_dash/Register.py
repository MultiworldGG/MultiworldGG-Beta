from . import MkddWorld, MkddWebWorld
from .mkdd_client import launch

"""
Mario Kart Double Dash World Registration

This file contains the metadata and class references for the mario_kart_double_dash world.
"""

# Required metadata
WORLD_NAME = "mario_kart_double_dash"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MkddWorld
WEB_WORLD_CLASS = MkddWebWorld
CLIENT_FUNCTION = launch
