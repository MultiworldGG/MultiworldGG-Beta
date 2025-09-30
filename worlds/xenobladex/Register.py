from . import XenobladeXWorld, XenobladeXWeb
from .Client import launch

"""
Xenoblade X World Registration

This file contains the metadata and class references for the xenobladex world.
"""

# Required metadata
WORLD_NAME = "xenobladex"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = XenobladeXWorld
WEB_WORLD_CLASS = XenobladeXWeb
CLIENT_FUNCTION = launch
