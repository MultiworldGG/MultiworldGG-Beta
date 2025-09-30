from . import PokemonCrystalWorld, PokemonCrystalWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Pokemon Crystal World Registration

This file contains the metadata and class references for the pokemon_crystal world.
"""

# Required metadata
WORLD_NAME = "pokemon_crystal"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PokemonCrystalWorld
WEB_WORLD_CLASS = PokemonCrystalWebWorld
CLIENT_FUNCTION = None
