from . import PokemonFRLGWorld, PokemonFRLGWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Pokemon FireRed and LeafGreen World Registration

This file contains the metadata and class references for the pokemon_frlg world.
"""

# Required metadata
WORLD_NAME = "pokemon_frlg"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PokemonFRLGWorld
WEB_WORLD_CLASS = PokemonFRLGWebWorld
CLIENT_FUNCTION = None
