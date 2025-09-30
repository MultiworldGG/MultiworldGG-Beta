from . import BrotatoWorld
from .constants import GAME_NAME as from BaseUtils import get_archipelago_json()
game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version
from . import BrotatoWeb

"""
Brotato is a top-down arena shooter roguelite where you play a potato wielding up to World Registration

This file contains the metadata and class references for the brotato world.
"""

# Required metadata
WORLD_NAME = "brotato"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = BrotatoWorld
WEB_WORLD_CLASS = BrotatoWeb
CLIENT_FUNCTION = None
