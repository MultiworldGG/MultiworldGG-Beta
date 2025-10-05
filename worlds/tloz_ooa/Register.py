from . import OracleOfAgesWorld
from . import OracleOfAgesWeb

"""
The Legend of Zelda - Oracle of Ages World Registration

This file contains the metadata and class references for the tloz_ooa world.
"""

# Required metadata
WORLD_NAME = "tloz_ooa"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = OracleOfAgesWorld
WEB_WORLD_CLASS = OracleOfAgesWeb
CLIENT_FUNCTION = None
