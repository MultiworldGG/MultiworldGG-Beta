from . import UndertaleWorld, UndertaleWeb
from .Client import launch

"""
Undertale World Registration

This file contains the metadata and class references for the undertale world.
"""

# Required metadata
WORLD_NAME = "undertale"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = UndertaleWorld
WEB_WORLD_CLASS = UndertaleWeb
CLIENT_FUNCTION = launch
