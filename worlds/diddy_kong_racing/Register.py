from . import DiddyKongRacingWorld, DiddyKongRacingWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from .DKRClient import launch

"""
Diddy Kong Racing World Registration

This file contains the metadata and class references for the diddy_kong_racing world.
"""

# Required metadata
WORLD_NAME = "diddy_kong_racing"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DiddyKongRacingWorld
WEB_WORLD_CLASS = DiddyKongRacingWeb
CLIENT_FUNCTION = launch
