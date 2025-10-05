from . import KH2World
from . import KingdomHearts2Web
from .ClientStuff.Client import launch

"""
Kingdom Hearts 2 World Registration

This file contains the metadata and class references for the kh2 world.
"""

# Required metadata
WORLD_NAME = "kh2"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = KH2World
WEB_WORLD_CLASS = KingdomHearts2Web
CLIENT_FUNCTION = launch
