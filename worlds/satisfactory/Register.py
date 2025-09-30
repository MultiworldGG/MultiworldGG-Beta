from . import SatisfactoryWorld, SatisfactoryWebWorld

"""
Satisfactory World Registration

This file contains the metadata and class references for the satisfactory world.
"""

# Required metadata
WORLD_NAME = "satisfactory"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SatisfactoryWorld
WEB_WORLD_CLASS = SatisfactoryWebWorld
CLIENT_FUNCTION = None
