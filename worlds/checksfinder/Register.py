from . import ChecksFinderWorld, ChecksFinderWeb
from .Client import launch

"""
ChecksFinder World Registration

This file contains the metadata and class references for the checksfinder world.
"""

# Required metadata
WORLD_NAME = "checksfinder"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ChecksFinderWorld
WEB_WORLD_CLASS = ChecksFinderWeb
CLIENT_FUNCTION = launch
