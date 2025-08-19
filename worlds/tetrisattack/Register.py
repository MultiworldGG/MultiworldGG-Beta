from . import TetrisAttackWorld, TetrisAttackWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Tetris Attack World Registration

This file contains the metadata and class references for the tetrisattack world.
"""

# Required metadata
WORLD_NAME = "tetrisattack"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = TetrisAttackWorld
WEB_WORLD_CLASS = TetrisAttackWebWorld
CLIENT_FUNCTION = None
