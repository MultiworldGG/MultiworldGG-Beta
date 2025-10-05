from . import DiddyKongRacingWorld, DiddyKongRacingWeb
from .DKRClient import launch

"""
Diddy Kong Racing World Registration

This file contains the metadata and class references for the diddy_kong_racing world.
"""

# Required metadata
WORLD_NAME = "diddy_kong_racing"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DiddyKongRacingWorld
WEB_WORLD_CLASS = DiddyKongRacingWeb
CLIENT_FUNCTION = launch
