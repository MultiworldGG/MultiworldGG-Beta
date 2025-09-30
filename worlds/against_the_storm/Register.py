from . import AgainstTheStormWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import AgainstTheStormWeb

"""
Against the Storm World Registration

This file contains the metadata and class references for the against_the_storm world.
"""

# Required metadata
WORLD_NAME = "against_the_storm"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = AgainstTheStormWorld
WEB_WORLD_CLASS = AgainstTheStormWeb
CLIENT_FUNCTION = None
