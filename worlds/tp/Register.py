from . import TPWorld, TPWeb, run_client

"""
Join Link and Midna on their adventure through Hyrule in Twilight Princess. World Registration

This file contains the metadata and class references for the tp world.
"""

# Required metadata
WORLD_NAME = "tp"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TPWorld
WEB_WORLD_CLASS = TPWeb
CLIENT_FUNCTION = run_client
