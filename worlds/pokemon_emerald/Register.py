from . import PokemonEmeraldWorld, PokemonEmeraldWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Pokemon Emerald World Registration

This file contains the metadata and class references for the pokemon_emerald world.
"""

# Required metadata
WORLD_NAME = "pokemon_emerald"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PokemonEmeraldWorld
WEB_WORLD_CLASS = PokemonEmeraldWebWorld
CLIENT_FUNCTION = None
