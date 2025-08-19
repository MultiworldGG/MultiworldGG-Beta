from . import AP_SudokuWorld, AP_SudokuWebWorld
from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version

"""
Sudoku World Registration

This file contains the metadata and class references for the apsudoku world.
"""

# Required metadata
WORLD_NAME = "apsudoku"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = AP_SudokuWorld
WEB_WORLD_CLASS = AP_SudokuWebWorld
CLIENT_FUNCTION = None
