from . import PokemonRedBlueWorld, PokemonWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Pokemon Red and Blue World Registration

This file contains the metadata and class references for the pokemon_rb world.
"""

# Required metadata
WORLD_NAME = "pokemon_rb"
GAME_NAME = from BaseUtils import get_archipelago_json()
game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PokemonRedBlueWorld
WEB_WORLD_CLASS = PokemonWebWorld
CLIENT_FUNCTION = None
