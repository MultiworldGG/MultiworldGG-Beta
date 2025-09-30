from . import TetrisAttackWorld, TetrisAttackWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Tetris Attack World Registration

This file contains the metadata and class references for the tetrisattack world.
"""

# Required metadata
WORLD_NAME = "tetrisattack"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TetrisAttackWorld
WEB_WORLD_CLASS = TetrisAttackWebWorld
CLIENT_FUNCTION = None
