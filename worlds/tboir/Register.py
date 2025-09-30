from . import TheBindingOfIsaacRepentanceWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import TheBindingOfIsaacRepentanceWeb

"""
The Binding of Isaac Repentance World Registration

This file contains the metadata and class references for the tboir world.
"""

# Required metadata
WORLD_NAME = "tboir"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TheBindingOfIsaacRepentanceWorld
WEB_WORLD_CLASS = TheBindingOfIsaacRepentanceWeb
CLIENT_FUNCTION = None
