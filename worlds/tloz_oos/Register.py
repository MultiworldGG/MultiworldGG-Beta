from . import OracleOfSeasonsWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import OracleOfSeasonsWeb

"""
The Legend of Zelda - Oracle of Seasons World Registration

This file contains the metadata and class references for the tloz_oos world.
"""

# Required metadata
WORLD_NAME = "tloz_oos"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OracleOfSeasonsWorld
WEB_WORLD_CLASS = OracleOfSeasonsWeb
CLIENT_FUNCTION = None
