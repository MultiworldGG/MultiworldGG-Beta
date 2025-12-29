from . import Sims4World, Sims4Web

"""
Sims 4 World Registration

This file contains the metadata and class references for the sims4 world.
"""

# Required metadata
WORLD_NAME = "sims4"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Sims4World
WEB_WORLD_CLASS = Sims4Web
CLIENT_FUNCTION = None
