from . import PokemonEmeraldWorld, PokemonEmeraldWebWorld

"""
Pokemon Emerald World Registration

This file contains the metadata and class references for the pokemon_emerald world.
"""

# Required metadata
WORLD_NAME = "pokemon_emerald"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PokemonEmeraldWorld
WEB_WORLD_CLASS = PokemonEmeraldWebWorld
CLIENT_FUNCTION = None
