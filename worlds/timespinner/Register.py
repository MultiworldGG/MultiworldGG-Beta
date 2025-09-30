from . import TimespinnerWebWorld, TimespinnerWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Timespinner World Registration

This file contains the metadata and class references for the timespinner world.
"""

# Required metadata
WORLD_NAME = "timespinner"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TimespinnerWorld
WEB_WORLD_CLASS = TimespinnerWebWorld
CLIENT_FUNCTION = None
