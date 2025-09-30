from . import TetrisAttackWorld, TetrisAttackWebWorld

"""
Tetris Attack World Registration

This file contains the metadata and class references for the tetrisattack world.
"""

# Required metadata
WORLD_NAME = "tetrisattack"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TetrisAttackWorld
WEB_WORLD_CLASS = TetrisAttackWebWorld
CLIENT_FUNCTION = None
