#!/usr/bin/env python3
"""
Script to add archipelago.json, pyproject.toml, and Register.py to existing world directories
that don't have them yet, using the generic world as a template.
"""

import argparse
import sys
import json
from pathlib import Path


def create_world_files(module_name: str, overwrite: bool = False, igdb_id: int = 0):
    """
    Create the three template files for an existing world directory.
    
    Args:
        module_name: Name of the world directory
        overwrite: Whether to overwrite existing files
        igdb_id: IGDB ID of the game
    """

    module_name = module_name.lower()
    # Paths
    src_dir = Path(__file__).parent.parent
    template_dir = src_dir / "worlds" / "generic"
    target_dir = src_dir / "worlds" / module_name
    
    # Check if target world directory exists
    if not target_dir.exists():
        print(f"Error: World directory '{target_dir}' does not exist.")
        return False
    
    # Template files
    templates = {
        "archipelago.json": template_dir / "archipelago.json",
        "pyproject.toml": template_dir / "pyproject.toml",
        "Register.py": template_dir / "Register.py"
    }
    
    # Process each template
    for filename, template_path in templates.items():
        target_path = target_dir / filename
        
        # Check if file already exists
        if target_path.exists() and not overwrite:
            print(f"Skipping {filename} - already exists (use --overwrite to replace)")
            if filename == "archipelago.json":
                with open(target_path, "r") as f:
                    content = json.load(f)
                if igdb_id > 0:
                    content["igdb_id"] = igdb_id
                    with open(target_path, "w") as f:
                        json.dumps(content, f, indent=4)
                continue
        
        # Read template
        try:
            content = template_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading template {template_path}: {e}")
            return False
        
        # Replace generic with world name
        content = content.replace("generic", module_name)
        # Write to target
        try:
            target_path.write_text(content, encoding="utf-8")
            print(f"Created {target_path}")
        except Exception as e:
            print(f"Error writing {target_path}: {e}")
            return False
    
    print(f"\nSuccessfully created files for world '{module_name}'")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Add template files to an existing world directory"
    )
    parser.add_argument(
        "module_name",
        help="Name of the world directory (e.g., 'tloz', 'oot')"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files if they exist"
    )
    
    args = parser.parse_args()
    
    success = create_world_files(args.module_name, args.overwrite)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

