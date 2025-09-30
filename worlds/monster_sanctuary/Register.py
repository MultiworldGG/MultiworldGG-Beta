from . import MonsterSanctuaryWorld, MonsterSanctuaryWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Monster Sanctuary World Registration

This file contains the metadata and class references for the monster_sanctuary world.
"""

# Required metadata
WORLD_NAME = "monster_sanctuary"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MonsterSanctuaryWorld
WEB_WORLD_CLASS = MonsterSanctuaryWebWorld
CLIENT_FUNCTION = None
