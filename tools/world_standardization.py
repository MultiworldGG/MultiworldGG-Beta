#!/usr/bin/env python3
"""
World Plugin Standardization Tool

This script automates the process of standardizing all world plugins by generating
pyproject.toml, Constants.py, and Register.py files for each world in the worlds/ directory.

Features:
- Search for worlds missing standardization files (--search-missing)
- Process only worlds missing pyproject.toml files (--missing-pyproject-only)
- Generate files for all worlds (default behavior)
- Dry-run mode to preview changes (--dry-run)
- Report-only mode for analysis (--report-only)
- Automatically excludes system directories (lib, wheels, __pycache__, etc.)
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class WorldMetadata:
    """Container for world metadata extracted from __init__.py files."""
    plugin_name: str
    game_name: str
    author: str
    version: str
    igdb_id: int
    world_class: str
    web_world_class: Optional[str]
    client_function: Optional[str]
    description: str
    requirements: List[str]


class WorldMetadataExtractor:
    """Extracts metadata from world __init__.py files."""
    
    def __init__(self, worlds_dir: str = "worlds"):
        self.worlds_dir = Path(worlds_dir)
        
    def extract_from_init_py(self, world_path: str) -> WorldMetadata:
        """Extract metadata from world's __init__.py file."""
        init_file = Path(world_path) / "__init__.py"
        
        if not init_file.exists():
            raise FileNotFoundError(f"__init__.py not found in {world_path}")
            
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract plugin name from directory
        plugin_name = Path(world_path).name
        
        # Extract metadata using various methods
        game_name = self._extract_game_name(content, plugin_name)
        author = self._extract_author(content)
        version = self._extract_version(content)
        igdb_id = self._extract_igdb_id(content)
        world_class = self._extract_world_class(content)
        web_world_class = self._extract_web_world_class(content)
        client_function = self._extract_client_function(content)
        description = self._extract_description(content, game_name)
        requirements = self._extract_requirements(world_path)
        
        return WorldMetadata(
            plugin_name=plugin_name,
            game_name=game_name,
            author=author,
            version=version,
            igdb_id=igdb_id,
            world_class=world_class,
            web_world_class=web_world_class,
            client_function=client_function,
            description=description,
            requirements=requirements
        )
    
    def _extract_game_name(self, content: str, plugin_name: str) -> str:
        """Extract game name from class attributes or docstring."""
        # Try to find game attribute in World class
        game_pattern = r'class\s+\w+World.*?game\s*=\s*["\']([^"\']+)["\']'
        match = re.search(game_pattern, content, re.DOTALL)
        if match:
            return match.group(1)
            
        # Try to find in docstring
        docstring_pattern = r'class\s+\w+World.*?"""(.*?)"""'
        match = re.search(docstring_pattern, content, re.DOTALL)
        if match:
            docstring = match.group(1).strip()
            # Extract first line as game name
            first_line = docstring.split('\n')[0].strip()
            if first_line:
                return first_line
                
        # Fallback: convert plugin name to title case
        return plugin_name.replace('_', ' ').title()
    
    def _extract_author(self, content: str) -> str:
        """Extract author from class attributes."""
        # Handle type-annotated assignments like "author: str = "beauxq""
        author_pattern = r'author\s*:?\s*\w*\s*[:=]\s*["\']([^"\']+)["\']'
        match = re.search(author_pattern, content)
        if match:
            return match.group(1)
            
        # Try alternative patterns
        author_patterns = [
            r'authors\s*=\s*\[["\']([^"\']+)["\']\]',
            r'author\s*=\s*["\']([^"\']+)["\']',
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)
                
        return "Unknown"
    
    def _extract_version(self, content: str) -> str:
        """Extract version from various possible locations."""
        version_patterns = [
            r'version\s*[:=]\s*["\']([^"\']+)["\']',
            r'__version__\s*[:=]\s*["\']([^"\']+)["\']',
            r'world_version\s*[:=]\s*["\']([^"\']+)["\']',
            r'ap_world_version\s*[:=]\s*["\']([^"\']+)["\']',
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, content)
            if match:
                version = match.group(1)
                # Ensure it's a valid semver
                if re.match(r'^\d+\.\d+\.\d+', version):
                    return version
                    
        return "1.0.0"
    
    def _extract_igdb_id(self, content: str) -> int:
        """Extract IGDB ID from class attributes."""
        igdb_pattern = r'igdb_id\s*[:=]\s*(\d+)'
        match = re.search(igdb_pattern, content)
        if match:
            return int(match.group(1))
        return 0
    
    def _extract_world_class(self, content: str) -> str:
        """Extract main World class name."""
        # Look for class that inherits from World
        world_class_pattern = r'class\s+(\w+World)\s*\(.*World.*\):'
        match = re.search(world_class_pattern, content)
        if match:
            return match.group(1)
            
        # Fallback: look for any class ending with World
        fallback_pattern = r'class\s+(\w*World)\s*[:\(]'
        match = re.search(fallback_pattern, content)
        if match:
            return match.group(1)
            
        return "World"
    
    def _extract_web_world_class(self, content: str) -> Optional[str]:
        """Extract WebWorld class name if present."""
        web_world_pattern = r'class\s+(\w+Web)\s*\(.*WebWorld.*\):'
        match = re.search(web_world_pattern, content)
        if match:
            return match.group(1)
        return None
    
    def _extract_client_function(self, content: str) -> Optional[str]:
        """Extract client launch function if present."""
        # Look for launch_client function
        client_pattern = r'def\s+(launch_client)\s*\('
        match = re.search(client_pattern, content)
        if match:
            return match.group(1)
        return None
    
    def _extract_description(self, content: str, game_name: str) -> str:
        """Extract description from class docstring."""
        docstring_pattern = r'class\s+\w+World.*?"""(.*?)"""'
        match = re.search(docstring_pattern, content, re.DOTALL)
        if match:
            docstring = match.group(1).strip()
            # Join all non-empty lines in the docstring
            lines = [line.strip() for line in docstring.split('\n') if line.strip()]
            if lines:
                return ' '.join(lines)
        return f"{game_name} randomizer for MultiworldGG"
    
    def _extract_requirements(self, world_path: str) -> List[str]:
        """Extract requirements from requirements.txt if present."""
        req_file = Path(world_path) / "requirements.txt"
        if req_file.exists():
            with open(req_file, 'r') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return []


class WorldFileGenerator:
    """Generates pyproject.toml and Register.py files from metadata."""
    
    def __init__(self, write_files: bool = True):
        self.write_files = write_files

    def generate_pyproject_toml(self, metadata: WorldMetadata) -> str:
        """Generate pyproject.toml content from metadata."""
        template = f'''[build-system]
requires = ["setuptools", "setuptools-scm"]
build-backend = "setuptools.build_meta"

[project]
name = "worlds.{metadata.plugin_name}"
dynamic = ["version"]
description = "MultiWorld: {metadata.game_name}"
authors = [
    {{name = "{metadata.author}"}}
]
classifiers = [
    "Private :: Do Not Upload"
]
requires-python = ">=3.12"
'''
        
        if metadata.requirements:
            template += f'\ndependencies = [\n'
            for req in metadata.requirements:
                template += f'    "{req}",\n'
            template += ']\n'
        
        template += f'''
[tool.setuptools.packages.find]
where = ["src/"]
include = ["worlds.{metadata.plugin_name}"]
namespaces = true

[tool.setuptools.dynamic]
version = {{attr = "worlds.{metadata.plugin_name}.Constants.VERSION"}}
'''
        
        return template
    
    def generate_constants_py(self, metadata: WorldMetadata) -> str:
        """Generate Constants.py content from metadata."""
        return f'''GAME_NAME: str = "{metadata.game_name}"
AUTHOR: str = "{metadata.author}"
IGDB_ID: int = {metadata.igdb_id}
VERSION: str = "{metadata.version}"
'''

    def generate_register_py(self, metadata: WorldMetadata) -> str:
        """Generate Register.py content from metadata."""
        imports = [f"from . import {metadata.world_class}"]
        imports.append("from .Constants import GAME_NAME as game_name, AUTHOR as author, IGDB_ID as igdb_id, VERSION as version")
        if metadata.web_world_class:
            imports.append(f"from . import {metadata.web_world_class}")
        
        template = f'''{"\n".join(imports)}

"""
{metadata.game_name} World Registration

This file contains the metadata and class references for the {metadata.plugin_name} world.
"""

# Required metadata
WORLD_NAME = "{metadata.plugin_name}"
GAME_NAME = game_name
IGDB_ID = igdb_id
AUTHOR = author
VERSION = version

# Plugin entry points
WORLD_CLASS = {metadata.world_class}
'''
        
        if metadata.web_world_class:
            template += f"WEB_WORLD_CLASS = {metadata.web_world_class}\n"
        else:
            template += "WEB_WORLD_CLASS = None\n"
            
        template += "CLIENT_FUNCTION = None\n"
        
        return template
    
    def _append_constants_to_existing_file(self, constants_file: Path, metadata: WorldMetadata) -> None:
        """Append standardization constants to an existing constants file."""
        # Read existing file content
        with open(constants_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # Check if standardization constants already exist
        standardization_constants = [
            'GAME_NAME',
            'AUTHOR', 
            'IGDB_ID',
            'VERSION'
        ]
        
        missing_constants = []
        for const in standardization_constants:
            # Check if the constant is already defined (allowing for various assignment patterns)
            if not re.search(rf'^{const}\s*[:=]', existing_content, re.MULTILINE):
                missing_constants.append(const)
        
        if not missing_constants:
            logger.info(f"All standardization constants already exist in {constants_file}")
            return
            
        # Generate the missing constants
        new_constants = []
        if 'GAME_NAME' in missing_constants:
            new_constants.append(f'GAME_NAME: str = "{metadata.game_name}"')
        if 'AUTHOR' in missing_constants:
            new_constants.append(f'AUTHOR: str = "{metadata.author}"')
        if 'IGDB_ID' in missing_constants:
            new_constants.append(f'IGDB_ID: int = {metadata.igdb_id}')
        if 'VERSION' in missing_constants:
            new_constants.append(f'VERSION: str = "{metadata.version}"')
        
        # Add a comment and the new constants
        append_content = f"\n\n# Standardization constants added by world_standardization.py\n"
        append_content += "\n".join(new_constants) + "\n"
        
        # Write the updated content
        with open(constants_file, 'a', encoding='utf-8') as f:
            f.write(append_content)
        
        logger.info(f"Appended {len(missing_constants)} standardization constants to {constants_file}")
    
    def generate_for_world(self, world_path: str, metadata: WorldMetadata) -> None:
        """Generate all standardization files for a single world."""
        world_path = Path(world_path)
        
        # Generate content for all files
        pyproject_content = self.generate_pyproject_toml(metadata)
        constants_content = self.generate_constants_py(metadata)
        register_content = self.generate_register_py(metadata)
        
        # Define file paths
        pyproject_file = world_path / "pyproject.toml"
        register_file = world_path / "Register.py"
        
        # Handle constants file - check for existing files
        constants_file_cap = world_path / "Constants.py"
        constants_file_lower = world_path / "constants.py" 
        
        existing_constants_file = None
        if constants_file_cap.exists():
            existing_constants_file = constants_file_cap
        elif constants_file_lower.exists():
            existing_constants_file = constants_file_lower
        
        if self.write_files:
            # Generate pyproject.toml
            with open(pyproject_file, 'w', encoding='utf-8') as f:
                f.write(pyproject_content)
            logger.info(f"Generated {pyproject_file}")
            
            # Handle constants file
            if existing_constants_file:
                self._append_constants_to_existing_file(existing_constants_file, metadata)
            else:
                # Create new Constants.py file
                with open(constants_file_cap, 'w', encoding='utf-8') as f:
                    f.write(constants_content)
                logger.info(f"Generated {constants_file_cap}")
            
            # Generate Register.py
            with open(register_file, 'w', encoding='utf-8') as f:
                f.write(register_content)
            logger.info(f"Generated {register_file}")
        else:
            logger.info(f"[DRY-RUN] Would generate {pyproject_file}")
            if existing_constants_file:
                logger.info(f"[DRY-RUN] Would append constants to existing {existing_constants_file}")
            else:
                logger.info(f"[DRY-RUN] Would generate {constants_file_cap}")
            logger.info(f"[DRY-RUN] Would generate {register_file}")


class WorldBatchProcessor:
    """Processes all worlds in batch."""
    
    # Directories to exclude from world processing
    EXCLUDED_DIRS = {'_', '.', 'Lib', 'Wheels', '__pycache__'}
    
    def __init__(self, worlds_dir: str = "worlds", write_files: bool = True):
        self.worlds_dir = Path(worlds_dir)
        self.extractor = WorldMetadataExtractor(worlds_dir)
        self.generator = WorldFileGenerator(write_files=write_files)
        self.results = []
        self.write_files = write_files
        
    def _get_valid_world_dirs(self) -> List[Path]:
        """Get list of valid world directories, excluding system/utility directories."""
        return [d for d in self.worlds_dir.iterdir() 
                if d.is_dir() and not any(d.name.startswith(prefix) for prefix in self.EXCLUDED_DIRS) 
                and d.name.lower() not in self.EXCLUDED_DIRS]
        
    def find_worlds_missing_pyproject(self) -> List[str]:
        """Find all worlds that don't have a pyproject.toml file."""
        world_dirs = self._get_valid_world_dirs()
        
        missing_pyproject = []
        for world_dir in world_dirs:
            pyproject_file = world_dir / "pyproject.toml"
            if not pyproject_file.exists():
                missing_pyproject.append(world_dir.name)
        
        return missing_pyproject
    
    def find_worlds_missing_register(self) -> List[str]:
        """Find all worlds that don't have a Register.py file."""
        world_dirs = self._get_valid_world_dirs()
        
        missing_register = []
        for world_dir in world_dirs:
            register_file = world_dir / "Register.py"
            if not register_file.exists():
                missing_register.append(world_dir.name)
        
        return missing_register
    
    def find_worlds_missing_constants(self) -> List[str]:
        """Find all worlds that don't have a Constants.py file."""
        world_dirs = self._get_valid_world_dirs()
        
        missing_constants = []
        for world_dir in world_dirs:
            constants_file = world_dir / "Constants.py"
            if not constants_file.exists():
                missing_constants.append(world_dir.name)
        
        return missing_constants
    
    def search_missing_files(self) -> Dict[str, List[str]]:
        """Search for all worlds missing standardization files."""
        logger.info("Searching for worlds with missing standardization files...")
        
        missing_pyproject = self.find_worlds_missing_pyproject()
        missing_register = self.find_worlds_missing_register()
        missing_constants = self.find_worlds_missing_constants()
        
        results = {
            'missing_pyproject': missing_pyproject,
            'missing_register': missing_register,
            'missing_constants': missing_constants,
            'total_worlds': len(self._get_valid_world_dirs())
        }
        
        logger.info(f"Found {len(missing_pyproject)} worlds missing pyproject.toml")
        logger.info(f"Found {len(missing_register)} worlds missing Register.py")
        logger.info(f"Found {len(missing_constants)} worlds missing Constants.py")
        
        return results
        
    def process_all_worlds(self) -> None:
        """Process all worlds in parallel."""
        world_dirs = self._get_valid_world_dirs()
        logger.info(f"Found {len(world_dirs)} worlds to process")
        self._process_world_list(world_dirs)
    
    def process_worlds_missing_pyproject(self) -> None:
        """Process only worlds that are missing pyproject.toml files."""
        missing_worlds = self.find_worlds_missing_pyproject()
        world_dirs = [self.worlds_dir / world_name for world_name in missing_worlds]
        logger.info(f"Found {len(world_dirs)} worlds missing pyproject.toml to process")
        self._process_world_list(world_dirs)
    
    def _process_world_list(self, world_dirs: List[Path]) -> None:
        """Process a specific list of world directories."""
        for world_dir in world_dirs:
            try:
                logger.info(f"Processing {world_dir.name}...")
                metadata = self.extractor.extract_from_init_py(str(world_dir))
                self.generator.generate_for_world(str(world_dir), metadata)
                self.results.append({
                    'world': world_dir.name,
                    'status': 'success',
                    'metadata': metadata
                })
            except Exception as e:
                logger.error(f"Failed to process {world_dir.name}: {e}")
                self.results.append({
                    'world': world_dir.name,
                    'status': 'error',
                    'error': str(e)
                })
    
    def validate_generated_files(self) -> List[str]:
        """Validate all generated files and return errors."""
        errors = []
        
        for result in self.results:
            if result['status'] == 'success':
                world_dir = self.worlds_dir / result['world']
                
                # Check if files exist
                pyproject_file = world_dir / "pyproject.toml"
                constants_file = world_dir / "Constants.py"
                register_file = world_dir / "Register.py"
                
                if not pyproject_file.exists():
                    errors.append(f"{result['world']}: pyproject.toml not found")
                if not constants_file.exists():
                    errors.append(f"{result['world']}: Constants.py not found")
                if not register_file.exists():
                    errors.append(f"{result['world']}: Register.py not found")
                
                # Validate metadata
                metadata = result['metadata']
                if not metadata.game_name:
                    errors.append(f"{result['world']}: Missing game name")
                if not metadata.author or metadata.author == "Unknown":
                    errors.append(f"{result['world']}: Missing or unknown author")
                if not metadata.world_class:
                    errors.append(f"{result['world']}: Missing world class")
        
        return errors
    
    def create_migration_report(self) -> str:
        """Generate report of migration results including missing metadata list."""
        successful = [r for r in self.results if r['status'] == 'success']
        failed = [r for r in self.results if r['status'] == 'error']
        
        # Get current missing files status
        missing_files = self.search_missing_files() if not self.results else {}
        
        # Identify worlds with missing metadata
        missing_metadata = []
        for result in successful:
            metadata = result['metadata']
            if metadata.author == "Unknown" or not metadata.game_name or metadata.game_name == metadata.plugin_name.replace('_', ' ').title():
                missing_metadata.append(result['world'])
        
        report = f"""
World Standardization Migration Report
====================================

Summary:
- Total worlds processed: {len(self.results)}
- Successful: {len(successful)}
- Failed: {len(failed)}
- Worlds with missing metadata: {len(missing_metadata)}
"""

        # Add missing files information if available
        if missing_files:
            report += f"- Total worlds in directory: {missing_files['total_worlds']}\n"
            report += f"- Worlds still missing pyproject.toml: {len(missing_files['missing_pyproject'])}\n"
            report += f"- Worlds still missing Constants.py: {len(missing_files['missing_constants'])}\n"
            report += f"- Worlds still missing Register.py: {len(missing_files['missing_register'])}\n"

        report += "\nSuccessful Migrations:\n"
        
        for result in successful:
            metadata = result['metadata']
            report += f"- {result['world']}: {metadata.game_name} by {metadata.author}\n"
        
        if failed:
            report += "\nFailed Migrations:\n"
            for result in failed:
                report += f"- {result['world']}: {result['error']}\n"
        
        if missing_metadata:
            report += "\nWorlds with Missing Metadata (require manual review):\n"
            for world in missing_metadata:
                report += f"- {world}\n"
        
        # Add remaining missing files to report
        if missing_files and missing_files['missing_pyproject']:
            report += f"\nWorlds Still Missing pyproject.toml:\n"
            for world in sorted(missing_files['missing_pyproject']):
                report += f"- {world}\n"
        
        if missing_files and missing_files['missing_constants']:
            report += f"\nWorlds Still Missing Constants.py:\n"
            for world in sorted(missing_files['missing_constants']):
                report += f"- {world}\n"
        
        if missing_files and missing_files['missing_register']:
            report += f"\nWorlds Still Missing Register.py:\n"
            for world in sorted(missing_files['missing_register']):
                report += f"- {world}\n"
        
        # Validation errors
        validation_errors = self.validate_generated_files()
        if validation_errors:
            report += "\nValidation Errors:\n"
            for error in validation_errors:
                report += f"- {error}\n"
        
        return report


def main():
    """Main entry point for the standardization tool."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Standardize world plugins")
    parser.add_argument("--worlds-dir", default="worlds", help="Path to worlds directory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated without writing files")
    parser.add_argument("--report-only", action="store_true", help="Generate report only")
    parser.add_argument("--search-missing", action="store_true", help="Search for worlds missing standardization files")
    parser.add_argument("--missing-pyproject-only", action="store_true", help="Process only worlds missing pyproject.toml files")
    
    args = parser.parse_args()
    write_files = not (args.dry_run or args.report_only or args.search_missing)
    processor = WorldBatchProcessor(args.worlds_dir, write_files=write_files)
    
    if args.search_missing:
        # Search for missing files only
        logger.info("Searching for worlds with missing standardization files...")
        missing_files = processor.search_missing_files()
        
        print(f"\nMissing Files Report")
        print(f"==================")
        print(f"Total worlds: {missing_files['total_worlds']}")
        print(f"Worlds missing pyproject.toml: {len(missing_files['missing_pyproject'])}")
        print(f"Worlds missing Constants.py: {len(missing_files['missing_constants'])}")
        print(f"Worlds missing Register.py: {len(missing_files['missing_register'])}")
        
        if missing_files['missing_pyproject']:
            print(f"\nWorlds missing pyproject.toml:")
            for world in sorted(missing_files['missing_pyproject']):
                print(f"  - {world}")
        
        if missing_files['missing_constants']:
            print(f"\nWorlds missing Constants.py:")
            for world in sorted(missing_files['missing_constants']):
                print(f"  - {world}")
        
        if missing_files['missing_register']:
            print(f"\nWorlds missing Register.py:")
            for world in sorted(missing_files['missing_register']):
                print(f"  - {world}")
        
        return
    
    if args.report_only:
        # Just analyze existing files
        logger.info("Analyzing existing worlds...")
        processor.process_all_worlds()
    elif args.missing_pyproject_only:
        # Process only worlds missing pyproject.toml
        logger.info("Processing worlds missing pyproject.toml files...")
        processor.process_worlds_missing_pyproject()
        
        if not args.dry_run:
            # Validate results
            errors = processor.validate_generated_files()
            if errors:
                logger.warning(f"Found {len(errors)} validation errors")
                for error in errors:
                    logger.warning(error)
    else:
        # Generate files for all worlds
        logger.info("Starting world standardization...")
        processor.process_all_worlds()
        
        if not args.dry_run:
            # Validate results
            errors = processor.validate_generated_files()
            if errors:
                logger.warning(f"Found {len(errors)} validation errors")
                for error in errors:
                    logger.warning(error)
    
    # Generate report (unless we're just searching)
    if not args.search_missing:
        report = processor.create_migration_report()
        print(report)
        
        # Save report to file
        report_file = Path("world_standardization_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"Report saved to {report_file}")


if __name__ == "__main__":
    main() 