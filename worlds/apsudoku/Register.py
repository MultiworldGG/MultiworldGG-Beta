from . import AP_SudokuWorld, AP_SudokuWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

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
