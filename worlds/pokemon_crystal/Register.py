from . import PokemonCrystalWorld, PokemonCrystalWebWorld

"""
Pokemon Crystal World Registration

This file contains the metadata and class references for the pokemon_crystal world.
"""

# Required metadata
WORLD_NAME = "pokemon_crystal"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = PokemonCrystalWorld
WEB_WORLD_CLASS = PokemonCrystalWebWorld
CLIENT_FUNCTION = None
