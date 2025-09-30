from . import SotnWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import SotnWeb

"""
Symphony of the Night is a metroidvania developed by Konami World Registration

This file contains the metadata and class references for the sotn world.
"""

# Required metadata
WORLD_NAME = "sotn"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SotnWorld
WEB_WORLD_CLASS = SotnWeb
CLIENT_FUNCTION = None
