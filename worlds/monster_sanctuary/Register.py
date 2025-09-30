from . import MonsterSanctuaryWorld, MonsterSanctuaryWebWorld

"""
Monster Sanctuary World Registration

This file contains the metadata and class references for the monster_sanctuary world.
"""

# Required metadata
WORLD_NAME = "monster_sanctuary"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MonsterSanctuaryWorld
WEB_WORLD_CLASS = MonsterSanctuaryWebWorld
CLIENT_FUNCTION = None
