from . import ShapezWorld
from . import ShapezWeb

"""
shapez is an automation game about cutting, rotating, stacking, and painting shapes, that you extract from randomly World Registration

This file contains the metadata and class references for the shapez world.
"""

# Required metadata
WORLD_NAME = "shapez"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ShapezWorld
WEB_WORLD_CLASS = ShapezWeb
CLIENT_FUNCTION = None
