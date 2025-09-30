from . import BlasphemousWorld, BlasphemousWeb
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Blasphemous World Registration

This file contains the metadata and class references for the blasphemous world.
"""

# Required metadata
WORLD_NAME = "blasphemous"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = BlasphemousWorld
WEB_WORLD_CLASS = BlasphemousWeb
CLIENT_FUNCTION = None
