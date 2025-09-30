from . import PhantomHourglassWorld, PhantomHourglassWeb

"""
The Legend of Zelda - Phantom Hourglass World Registration

This file contains the metadata and class references for the tloz_ph world.
"""

# Required metadata
WORLD_NAME = "tloz_ph"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PhantomHourglassWorld
WEB_WORLD_CLASS = PhantomHourglassWeb
CLIENT_FUNCTION = None
