from . import BlasphemousWorld, BlasphemousWeb

"""
Blasphemous World Registration

This file contains the metadata and class references for the blasphemous world.
"""

# Required metadata
WORLD_NAME = "blasphemous"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = BlasphemousWorld
WEB_WORLD_CLASS = BlasphemousWeb
CLIENT_FUNCTION = None
