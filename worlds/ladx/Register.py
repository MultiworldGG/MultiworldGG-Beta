from . import LinksAwakeningWorld, LinksAwakeningWebWorld
from .LinksAwakeningClient import launch

"""
Link World Registration

This file contains the metadata and class references for the ladx world.
"""

# Required metadata
WORLD_NAME = "ladx"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = LinksAwakeningWorld
WEB_WORLD_CLASS = LinksAwakeningWebWorld
CLIENT_FUNCTION = launch
