from . import OracleOfSeasonsWorld
from . import OracleOfSeasonsWeb

"""
The Legend of Zelda - Oracle of Seasons World Registration

This file contains the metadata and class references for the tloz_oos world.
"""

# Required metadata
WORLD_NAME = "tloz_oos"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OracleOfSeasonsWorld
WEB_WORLD_CLASS = OracleOfSeasonsWeb
CLIENT_FUNCTION = None
