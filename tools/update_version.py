#!/usr/bin/env python3
"""
Update version numbers in pyproject.toml files by auto-incrementing patch version.
Only updates splashscreen and GUI packages - worlds package version is left unchanged.
"""

import argparse
import sys
import os
from pathlib import Path
import toml
import re


def increment_patch_version(version: str) -> str:
    """
    Increment the patch version number.
    
    Examples:
        "0.0.5a" -> "0.0.6a"
        "0.1.9a2" -> "0.1.10a2"  
        "1.2.3" -> "1.2.4"
    """
    # Parse version with optional alpha/beta suffix
    # Matches patterns like: 1.2.3, 0.0.5a, 1.2.3a2, 0.1.9a2
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)([a-zA-Z]+\d*)?$', version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    
    major, minor, patch, suffix = match.groups()
    suffix = suffix or ""  # Handle None case
    
    # Increment patch version
    new_patch = str(int(patch) + 1)
    
    # Reconstruct version with suffix if it exists
    if suffix:
        return f"{major}.{minor}.{new_patch}{suffix}"
    else:
        return f"{major}.{minor}.{new_patch}"


def update_pyproject_version(pyproject_path: Path, new_version: str) -> bool:
    """Update the version in a pyproject.toml file"""
    if not pyproject_path.exists():
        print(f"Warning: {pyproject_path} not found")
        return False
    
    try:
        # Read the current pyproject.toml
        with open(pyproject_path, "r", encoding="utf-8") as f:
            pyproject_data = toml.load(f)
        
        current_version = pyproject_data.get("project", {}).get("version")
        
        if current_version == new_version:
            print(f"No change needed for {pyproject_path.name}: already {new_version}")
            return False
        
        # Update the version
        if "project" not in pyproject_data:
            pyproject_data["project"] = {}
        
        pyproject_data["project"]["version"] = new_version
        
        # Write back to file
        with open(pyproject_path, "w", encoding="utf-8") as f:
            toml.dump(pyproject_data, f)
        
        print(f"Updated {pyproject_path.name}: {current_version} -> {new_version}")
        return True
        
    except Exception as e:
        print(f"Error updating {pyproject_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Increment patch version in wheel packages")
    parser.add_argument("--package", type=str, 
                       choices=["splash", "gui"],
                       required=True,
                       help="Which package to update (splash or gui only)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be updated without making changes")
    
    args = parser.parse_args()
    
    # Get the project root (src directory)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    
    try:
        # Determine the pyproject.toml path
        if args.package == "splash":
            pyproject_path = project_root / "splashscreen" / "pyproject.toml"
        elif args.package == "gui":
            pyproject_path = project_root / "gui" / "pyproject.toml"
        
        if not pyproject_path.exists():
            print(f"Error: {pyproject_path} not found")
            sys.exit(1)
        
        # Read current version
        with open(pyproject_path, "r", encoding="utf-8") as f:
            pyproject_data = toml.load(f)
        
        current_version = pyproject_data.get("project", {}).get("version")
        if not current_version:
            print(f"Error: No version found in {pyproject_path}")
            sys.exit(1)
        
        # Increment patch version
        new_version = increment_patch_version(current_version)
        
        if args.dry_run:
            print(f"Would update {args.package} package: {current_version} -> {new_version}")
        else:
            if update_pyproject_version(pyproject_path, new_version):
                print(f"Successfully updated {args.package} package version")
            else:
                sys.exit(1)
                
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
