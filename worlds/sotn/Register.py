from . import SotnWorld
from . import SotnWeb

"""
Symphony of the Night is a metroidvania developed by Konami World Registration

This file contains the metadata and class references for the sotn world.
"""

# Required metadata
WORLD_NAME = "sotn"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SotnWorld
WEB_WORLD_CLASS = SotnWeb
CLIENT_FUNCTION = None
