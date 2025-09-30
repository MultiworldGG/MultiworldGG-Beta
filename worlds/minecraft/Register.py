from . import MinecraftWorld, MinecraftWebWorld
from BaseUtils import get_archipelago_json()
game_name, author, version, ap_version = get_archipelago_json()

"""
Minecraft World Registration

This file contains the metadata and class references for the minecraft world.
"""

# Required metadata
WORLD_NAME = "minecraft"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MinecraftWorld
WEB_WORLD_CLASS = MinecraftWebWorld
CLIENT_FUNCTION = None
