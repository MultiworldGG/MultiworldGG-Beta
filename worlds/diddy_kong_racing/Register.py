from . import DiddyKongRacingWorld, DiddyKongRacingWeb
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
from .DKRClient import launch

"""
Diddy Kong Racing World Registration

This file contains the metadata and class references for the diddy_kong_racing world.
"""

# Required metadata
WORLD_NAME = "diddy_kong_racing"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DiddyKongRacingWorld
WEB_WORLD_CLASS = DiddyKongRacingWeb
CLIENT_FUNCTION = launch
