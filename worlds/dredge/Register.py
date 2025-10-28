from . import DredgeWorld, DredgeWeb

"""
Dredge World Registration

This file contains the metadata and class references for the dredge world.
"""

# Required metadata
WORLD_NAME = "dredge"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = DredgeWorld
WEB_WORLD_CLASS = DredgeWeb
CLIENT_FUNCTION = None
