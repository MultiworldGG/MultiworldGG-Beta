from . import TPWorld, TPWeb, run_client
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Join Link and Midna on their adventure through Hyrule in Twilight Princess. World Registration

This file contains the metadata and class references for the tp world.
"""

# Required metadata
WORLD_NAME = "tp"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TPWorld
WEB_WORLD_CLASS = TPWeb
CLIENT_FUNCTION = run_client
