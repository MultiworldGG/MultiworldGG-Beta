#!/usr/bin/env python3
"""
Build wheels for all worlds or a specific world.
This script moves each world's pyproject.toml to the project root directory,
builds the wheel, then moves it back to the original location.

Usage:
    python build_wheels.py                    # Build all worlds
    python build_wheels.py --world kh2        # Build only the kh2 world
    python build_wheels.py --verbose          # Build all with verbose output
    python build_wheels.py --world kh2 --clean # Build kh2 with clean option
"""

import argparse
import shutil
import subprocess
import sys
import json
import toml
from pathlib import Path


def print_colored(message, color="white"):
    """Print colored output (simplified for cross-platform compatibility)"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "gray": "\033[90m",
    }
    reset = "\033[0m"
    print(f"{colors.get(color, '')}{message}{reset}")


def main():
    parser = argparse.ArgumentParser(description="Build wheels for worlds")
    parser.add_argument("--clean", action="store_true", help="Clean build")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--world", type=str, help="Build list of worlds only")
    args = parser.parse_args()

    # Get the script directory (src/tools)
    script_dir = Path(__file__).resolve().parents[2]
    
    # Change to script directory
    import os
    os.chdir(script_dir)

    import sys
    # Check for virtual environment (informational only - Python is already running)
    venv_path = Path(sys.executable)
    if "venv" not in venv_path.parts:
        print_colored(f"You are not running this from the virtual environment", "red")
        print_colored(f"Please activate the virtual environment before running this script", "red")
        sys.exit(1)

    # Find all pyproject.toml files in subdirectories or specific world
    worlds_dir = script_dir / "src" / "worlds"

    worlds_with_pyproject = []

    # Default worlds are those that start with _ or are named generic
    # These don't require archipelago.json
    default_worlds = set()
    for world_dir in worlds_dir.iterdir():
        if world_dir.is_dir():
            world_name = world_dir.name
            if world_name.startswith("_") or world_name == "generic":
                default_worlds.add(world_name)
    
    if args.world:
        # Build only the specified world
        worlds_to_build = args.world.split(",")
        print(worlds_to_build)

        for world in worlds_to_build:
            world_path = worlds_dir / world
            pyproject_path = world_path / "pyproject.toml"
            archipelago_json_path = world_path / "archipelago.json"

            if not world_path.exists():
                print_colored(f"Error: World directory '{world}' not found in {worlds_dir}", "red")
                sys.exit(1)

            if not pyproject_path.exists():
                print_colored(f"Error: pyproject.toml not found in {world} directory", "red")
                sys.exit(1)

            if not archipelago_json_path.exists() and world not in default_worlds:
                print_colored(f"Error: archipelago.json not found in {world} directory", "red")
                sys.exit(1)

            worlds_with_pyproject.append(world)
            print_colored(f"Building specific world: {world}", "green")
    else:
        # Build all worlds with pyproject.toml files
        pyproject_files = list(worlds_dir.glob("*/pyproject.toml"))
        worlds_with_pyproject = sorted([p.parent.name for p in pyproject_files])

        print_colored(f"Found {len(worlds_with_pyproject)} worlds with pyproject.toml files", "green")

    # Track successful and failed builds
    successful_builds = []
    failed_builds = []
    skipped_builds = []

    for world in worlds_with_pyproject:
        world_path = worlds_dir / world
        pyproject_path = world_path / "pyproject.toml"
        archipelago_json_path = world_path / "archipelago.json"

        print_colored(f"Processing world: {world}", "yellow")

        # Check if pyproject.toml exists
        if not pyproject_path.exists():
            print_colored(f"  Skipping {world} - no pyproject.toml found", "red")
            failed_builds.append(f"{world} (no pyproject.toml)")
            continue

        if not archipelago_json_path.exists() and world not in default_worlds:
            print_colored(f"  Skipping {world} - no archipelago.json found", "red")
            failed_builds.append(f"{world} (no archipelago.json)")
            continue

        # Check if wheel already exists in dist directory (only when building all worlds)
        if not args.world:
            dist_dir = script_dir / "dist"
            if dist_dir.exists():
                existing_wheels = list(dist_dir.glob(f"worlds_{world}-*.whl"))
                if existing_wheels:
                    print_colored(f"  Skipping {world} - wheel already exists in dist/", "blue")
                    skipped_builds.append(world)
                    continue

        # Create MANIFEST.in for this world.
        # The exclude pattern is *.py[co] (not *.py[cod]) — [cod] would also
        # match `.pyd`, i.e. Windows native extensions, which we want to ship.
        manifest_content = f"""global-exclude *
graft src/worlds/{world}
global-exclude *~ *.py[co]
include pyproject.toml
"""
        manifest_path = script_dir / "MANIFEST.in"
        manifest_path.write_text(manifest_content)

        try:
            # Move pyproject.toml to script directory
            shutil.move(str(pyproject_path), str(script_dir / "pyproject.toml"))
            pyproject_in_root = script_dir / "pyproject.toml"

            if args.verbose:
                print_colored("  Moved pyproject.toml to project root directory", "gray")

            # Only update version/authors from archipelago.json for non-default worlds
            if world not in default_worlds and archipelago_json_path.exists():
                with open(archipelago_json_path, "r") as f:
                    archipelago_json = json.load(f)
                world_version: str = archipelago_json.get("world_version")
                authors: list[str] = archipelago_json.get("authors")
                with open(pyproject_in_root, "r") as f:
                    pyproject = toml.load(f)
                
                # Update version if present
                if world_version:
                    pyproject["project"]["version"] = world_version
                
                # Update authors if present
                if authors:
                    pyproject["project"]["authors"] = [{"name": author} for author in authors]
                
                with open(pyproject_in_root, "w") as f:
                    toml.dump(pyproject, f)

            # Run build command
            print_colored("  Building wheel...", "cyan")
            result = subprocess.run(
                [sys.executable, "-m", "build"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print_colored(f"  [OK] Build successful for {world}", "green")
                successful_builds.append(world)
            else:
                print_colored(f"  [FAILED] Build failed for {world}", "red")
                print_colored("  Build output:", "gray")
                for line in result.stderr.split("\n"):
                    if line.strip():
                        print_colored(f"    {line}", "gray")
                failed_builds.append(world)

            # Move pyproject.toml back to original location
            if pyproject_in_root.exists():
                shutil.move(str(pyproject_in_root), str(pyproject_path))
                if args.verbose:
                    print_colored(f"  Moved pyproject.toml back to {world}/", "gray")
            else:
                print_colored("  Warning: pyproject.toml not found in root directory after build", "yellow")

        except Exception as e:
            print_colored(f"  [FAILED] Error processing {world}: {e}", "red")
            failed_builds.append(f"{world} (error: {e})")
            if pyproject_in_root.exists() and pyproject_path.exists():
                shutil.move(str(pyproject_in_root), str(pyproject_path))
                if args.verbose:
                    print_colored(f"  Restored pyproject.toml to {world}/", "gray")
                else:
                    print_colored(f"  Warning: pyproject.toml not found in {world}/ directory after build", "yellow")

    # Remove MANIFEST.in if it exists
    manifest_path = script_dir / "MANIFEST.in"
    if manifest_path.exists():
        manifest_path.unlink()

    # Summary
    print_colored("\nBuild Summary:", "magenta")
    print_colored("=============", "magenta")
    print_colored(f"Skipped builds: {len(skipped_builds)}", "yellow")
    print_colored(f"Successful builds: {len(successful_builds)}", "green")
    print_colored(f"Failed builds: {len(failed_builds)}", "red")

    if skipped_builds:
        print_colored("\nSkipped builds:", "yellow")
        for build in skipped_builds:
            print_colored(f"  [SKIP] {build}", "yellow")

    if successful_builds:
        print_colored("\nSuccessful builds:", "green")
        for build in successful_builds:
            print_colored(f"  [OK] {build}", "green")

    if failed_builds:
        print_colored("\nFailed builds:", "red")
        for build in failed_builds:
            print_colored(f"  [FAILED] {build}", "red")

    print_colored("\nBuild process completed!", "green")


if __name__ == "__main__":
    main()

