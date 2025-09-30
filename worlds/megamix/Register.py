from . import MegaMixWorld, MegaMixWeb
from .Client import launch

"""
Hatsune Miku Project Diva Mega Mix+ World Registration

This file contains the metadata and class references for the megamix world.
"""

# Required metadata
WORLD_NAME = "megamix"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MegaMixWorld
WEB_WORLD_CLASS = MegaMixWeb
CLIENT_FUNCTION = launch
