from . import ALBWWebWorld, ALBWWorld 
from .Client import launch

"""
File name of your decrypted North American A Link Between Worlds ROM World Registration

This file contains the metadata and class references for the albw world.
"""

# Required metadata
WORLD_NAME = "albw"

from BaseUtils import get_archipelago_json
game_name, author, minimum_ap_version, version = get_archipelago_json(WORLD_NAME)

GAME_NAME = game_name
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = ALBWWorld
WEB_WORLD_CLASS = ALBWWebWorld
CLIENT_FUNCTION = launch


def post_install():
    """Move albwrandomizer data files to lib directory after installation"""
    import os
    import shutil
    from pathlib import Path
    
    try:
        from BaseUtils import local_path
        
        # Source and destination paths using the established pattern
        source_dir = Path(local_path("worlds", "albw", "data", "albwrandomizer"))
        dest_dir = Path(local_path("lib", "albwrandomizer"))
        
        if source_dir.exists():
            # Create destination directory if it doesn't exist
            dest_dir.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy the albwrandomizer directory to lib
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(source_dir, dest_dir)
            
            print(f"Successfully moved albwrandomizer data to {dest_dir}")
        else:
            print(f"Warning: Source directory {source_dir} not found")
            
    except Exception as e:
        print(f"Error in post-install script: {e}")
        # Don't fail the installation if post-install fails
        return False
    
    return True