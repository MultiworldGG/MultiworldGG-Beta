from . import OracleOfAgesWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()
from . import OracleOfAgesWeb

"""
The Legend of Zelda - Oracle of Ages World Registration

This file contains the metadata and class references for the tloz_ooa world.
"""

# Required metadata
WORLD_NAME = "tloz_ooa"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OracleOfAgesWorld
WEB_WORLD_CLASS = OracleOfAgesWeb
CLIENT_FUNCTION = None
