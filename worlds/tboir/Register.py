from . import TheBindingOfIsaacRepentanceWorld
from . import TheBindingOfIsaacRepentanceWeb

"""
The Binding of Isaac Repentance World Registration

This file contains the metadata and class references for the tboir world.
"""

# Required metadata
WORLD_NAME = "tboir"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TheBindingOfIsaacRepentanceWorld
WEB_WORLD_CLASS = TheBindingOfIsaacRepentanceWeb
CLIENT_FUNCTION = None
