#!/usr/bin/env python3
"""
Utility functions for reading world manifest files.
Standalone implementation that doesn't depend on BaseUtils.
"""

import json
from pathlib import Path
from typing import Dict, Any


def get_apworld_manifest(world: str) -> Dict[str, Any]:
    """
    Get the manifest from archipelago.json for a given world.
    
    This is a standalone version that works in CI/build environments
    where BaseUtils may not be importable.
    
    Args:
        world: Name of the world module/directory
        
    Returns:
        Dictionary containing the manifest data, or empty dict if file not found
    """
    # Get the src directory (parent of tools directory)
    src_dir = Path(__file__).parent.parent
    archipelago_json_path = src_dir / "worlds" / world / "archipelago.json"
    
    try:
        with open(archipelago_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}

