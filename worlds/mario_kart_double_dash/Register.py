from . import MkddWorld, MkddWebWorld
from .mkdd_client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Mario Kart Double Dash World Registration

This file contains the metadata and class references for the mario_kart_double_dash world.
"""

# Required metadata
WORLD_NAME = "mario_kart_double_dash"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MkddWorld
WEB_WORLD_CLASS = MkddWebWorld
CLIENT_FUNCTION = launch
