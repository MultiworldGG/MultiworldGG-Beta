from . import FFTAWorld, FFTAWebWorld

"""
Final Fantasy Tactics Advance World Registration

This file contains the metadata and class references for the ffta world.
"""

# Required metadata
WORLD_NAME = "ffta"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FFTAWorld
WEB_WORLD_CLASS = FFTAWebWorld
CLIENT_FUNCTION = None
