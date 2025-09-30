from . import XenobladeXWorld, XenobladeXWeb
from .Client import launch
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Xenoblade X World Registration

This file contains the metadata and class references for the xenobladex world.
"""

# Required metadata
WORLD_NAME = "xenobladex"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = XenobladeXWorld
WEB_WORLD_CLASS = XenobladeXWeb
CLIENT_FUNCTION = launch
