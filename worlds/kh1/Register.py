from . import KH1World, KH1Web
from .Client import launch

"""
Kingdom Hearts World Registration

This file contains the metadata and class references for the kh1 world.
"""

# Required metadata
WORLD_NAME = "kh1"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = KH1World
WEB_WORLD_CLASS = KH1Web
CLIENT_FUNCTION = launch
