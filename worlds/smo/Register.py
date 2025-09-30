from . import SMOWorld, SMOWebWorld
from .Connector.Client import launch

"""
Super Mario Odyssey World Registration

This file contains the metadata and class references for the smo world.
"""

# Required metadata
WORLD_NAME = "smo"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SMOWorld
WEB_WORLD_CLASS = SMOWebWorld
CLIENT_FUNCTION = launch
