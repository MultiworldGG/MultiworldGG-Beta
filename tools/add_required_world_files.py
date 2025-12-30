#!/usr/bin/env python3
"""
Script to add pyproject.toml to existing world directories
that don't have them yet.
"""

import argparse
import sys
from pathlib import Path
from world_manifest import get_apworld_manifest

# Templates for generating pip-installable world packages
PYPROJECT_TEMPLATE = """[project]
name = "worlds.{module_name}"
version = "{version}"
description = "MultiWorld: {game_name}"
classifiers = ["Private :: Do Not Upload"]
requires-python = ">=3.12"
{authors_section}
{client_section}

[tool.setuptools.packages.find]
where = ["src"]
include = ["worlds.{module_name}"]
namespaces = true
"""


def create_world_files(module_name: str, overwrite: bool = False):
    """
    Create the three template files for an existing world directory.
    
    Args:
        module_name: Name of the world directory
        overwrite: Whether to overwrite existing files
        igdb_id: IGDB ID of the game
    """

    module_name = module_name.lower()

    src_dir = Path(__file__).parent.parent
    target_dir = src_dir / "worlds" / module_name

    # Paths
    
    # Check if target world directory exists
    if not target_dir.exists():
        print(f"Error: World directory '{target_dir}' does not exist.")
        return False
    
    manifest = get_apworld_manifest(module_name)
    game_name = manifest.get("game", "Unknown")
    authors = manifest.get("authors", ["Unknown"])
    version = manifest.get("world_version", "0.0.1")
    
    with open(target_dir / "__init__.py", "r") as f:
        init_content = f.read()
    if "launch_client" in init_content:
        client_section = f'\n[project.entry-points."mwgg.client"]\n"worlds.{module_name}.Client" = "worlds.{module_name}:launch_client"'
    else:
        client_section = ""

    target_path = target_dir / "pyproject.toml"
    
    # Check if file already exists
    if target_path.exists() and not overwrite:
        print(f"Skipping {target_path} - already exists (use --overwrite to replace)")
        return True
    
    # Replace generic with world name
    content = PYPROJECT_TEMPLATE.format(
        module_name=module_name,
        version=version,
        game_name=game_name,
        authors_section="\n".join([f'[[project.authors]]\nname = "{author}"' for author in authors]),
        client_section=client_section
    )
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

