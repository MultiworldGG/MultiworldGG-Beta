from . import FaxanaduWorld
from . import FaxanaduWeb

"""
Faxanadu World Registration

This file contains the metadata and class references for the faxanadu world.
"""

# Required metadata
WORLD_NAME = "faxanadu"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = FaxanaduWorld
WEB_WORLD_CLASS = FaxanaduWeb
CLIENT_FUNCTION = None
