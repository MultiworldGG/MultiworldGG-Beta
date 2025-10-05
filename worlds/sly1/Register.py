from . import Sly1World, Sly1Web
from .Sly1Client import launch

"""
Sly Cooper and the Thievius Raccoonus World Registration

This file contains the metadata and class references for the sly1 world.
"""

# Required metadata
WORLD_NAME = "sly1"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = Sly1World
WEB_WORLD_CLASS = Sly1Web
CLIENT_FUNCTION = launch
