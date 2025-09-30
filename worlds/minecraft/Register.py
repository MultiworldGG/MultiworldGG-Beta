from . import MinecraftWorld, MinecraftWebWorld

"""
Minecraft World Registration

This file contains the metadata and class references for the minecraft world.
"""

# Required metadata
WORLD_NAME = "minecraft"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = MinecraftWorld
WEB_WORLD_CLASS = MinecraftWebWorld
CLIENT_FUNCTION = None
