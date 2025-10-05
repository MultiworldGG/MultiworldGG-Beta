from . import SMMapRandoWorld
from . import SMMapRandoWeb

"""
After planet Zebes exploded, Mother Brain put it back together again but arranged it differently this time. World Registration

This file contains the metadata and class references for the sm_map_rando world.
"""

# Required metadata
WORLD_NAME = "sm_map_rando"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = SMMapRandoWorld
WEB_WORLD_CLASS = SMMapRandoWeb
CLIENT_FUNCTION = None
