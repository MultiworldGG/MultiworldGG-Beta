from . import TimespinnerWebWorld, TimespinnerWorld

"""
Timespinner World Registration

This file contains the metadata and class references for the timespinner world.
"""

# Required metadata
WORLD_NAME = "timespinner"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TimespinnerWorld
WEB_WORLD_CLASS = TimespinnerWebWorld
CLIENT_FUNCTION = None
