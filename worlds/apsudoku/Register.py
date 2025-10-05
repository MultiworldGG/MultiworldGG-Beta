from . import AP_SudokuWorld, AP_SudokuWebWorld

"""
Sudoku World Registration

This file contains the metadata and class references for the apsudoku world.
"""

# Required metadata
WORLD_NAME = "apsudoku"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = AP_SudokuWorld
WEB_WORLD_CLASS = AP_SudokuWebWorld
CLIENT_FUNCTION = None
