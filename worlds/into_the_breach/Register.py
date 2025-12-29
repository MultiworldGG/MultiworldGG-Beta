from . import IntoTheBreachWorld, IntoTheBreachWeb

"""
Into The Breach World Registration

This file contains the metadata and class references for the into_the_breach world.
"""

# Required metadata
WORLD_NAME = "into_the_breach"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = IntoTheBreachWorld
WEB_WORLD_CLASS = IntoTheBreachWeb
CLIENT_FUNCTION = None
