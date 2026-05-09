# World Plugin Standardization Design Specification

## Overview

This document outlines the design for standardizing all world plugins in the MultiworldGG project by propagating `pyproject.toml` and `Register.py` files throughout all directories in the `worlds/` folder. This standardization will improve maintainability, enable proper package management, and provide consistent metadata across all game worlds.

## Current State Analysis

### Existing Patterns
- **Generic World**: Has both `pyproject.toml` and `Register.py` with standardized structure
- **KH2 World**: Has `pyproject.toml` but no `Register.py` (metadata embedded in `__init__.py`)
- **Most Worlds**: Have metadata scattered throughout `__init__.py` files
- **No Worlds**: Currently use standardized entry point registration

### Current Issues
1. **Inconsistent Metadata**: Game information, authors, versions scattered across files
2. **No Package Management**: Worlds not properly packaged for distribution
3. **Manual Registration**: Worlds must be manually imported and registered
4. **Maintenance Overhead**: Changes require updates in multiple locations

## Design Goals

1. **Standardization**: All worlds contain a Register.py and pyproject.toml consistent with their world.
2. **Automation**: Worlds auto-register via entry points
3. **Maintainability**: Single source of truth for metadata
4. **Packaging**: Proper Python package structure for each world
5. **Backward Compatibility**: Existing functionality preserved

## Proposed Structure

### File Organization
```
worlds/
├── {world_name}/
│   ├── pyproject.toml          # Package metadata and entry points
│   ├── Register.py             # World registration and metadata
│   ├── __init__.py             # World implementation (simplified)
│   ├── Client.py               # Client implementation
│   └── ...                     # Other world-specific files
```

### pyproject.toml Template
```toml
[project]
name = "{world_name}"
version = "{version}"
description = "{game_description}"
authors = [
    {name = "{author_name}"}
]
requires-python = ">=3.13"

[project.entry-points."mwgg.plugins"]
"{world_name}.WorldClass" = "{world_name}.Register:WORLD_CLASS"
"{world_name}.WebWorldClass" = "{world_name}.Register:WEB_WORLD_CLASS"
```

### Register.py Template
```python
from . import {WorldClass}
from . import {WebWorldClass}

"""
{Game Name} World Registration

This file contains the metadata and class references for the {world_name} world.
"""

# Required metadata
WORLD_NAME = "{world_name}"
GAME_NAME = "{Game Name}"
IGDB_ID = {igdb_id}
AUTHOR = "{author_name}"
VERSION = "{version}"

# Plugin entry points
WORLD_CLASS = {WorldClass}
WEB_WORLD_CLASS = {WebWorldClass}
CLIENT_FUNCTION = None
```

## Implementation Strategy

### Phase 1: Analysis and Template Creation
1. **Audit Existing Worlds**: Extract metadata from all `__init__.py` files. If the metadata doesn't exist in the `__init__.py` file, add this world to a list to give to me at the end. The client function is not in `__init__.py` and we will put clients on hold until later.
2. **Create Templates**: Generate standardized templates for `pyproject.toml` and `Register.py`
3. **Define Migration Rules**: Establish rules for extracting and transforming existing metadata

### Phase 2: Automated Generation
1. **Metadata Extraction Script**: Create script to parse existing world metadata
2. **File Generation Script**: Generate `pyproject.toml` and `Register.py` for each world
3. **Validation Script**: Verify generated files meet standards

### Phase 3: World Migration
1. **Batch Processing**: Process all worlds in parallel
2. **Manual Review**: Review generated files for accuracy
3. **Testing**: Verify worlds still function correctly
4. **Cleanup**: Map data pulled from `__init__.py` files back into the `__init__.py` as a reference to `Register.py`

### Phase 4: Integration and Testing
1. **Entry Point Registration**: Update main application to use entry points
2. **Fallback Mechanism**: Maintain backward compatibility during transition
3. **Documentation**: Update documentation and examples

## Technical Specifications

### Metadata Extraction Rules

#### From `__init__.py`:
- **Game Name**: Extract from `game` class attribute or class docstring
- **Author**: Extract from `author` class attribute
- **Version**: Extract from version-related attributes or use "1.0.0" as default
- **IGDB ID**: Extract from `igdb_id` class attribute or use 0 as default
- **World Class**: Extract main World class name
- **Web World Class**: Extract WebWorld class name if present
- **Client Function**: Set to None (on hold until later)

#### Special Cases:
- **Multiple Authors**: Convert to list format in pyproject.toml
- **Missing Metadata**: Use sensible defaults and mark for manual review
- **Complex Dependencies**: Preserve in requirements.txt or pyproject.toml

### File Generation Rules

#### pyproject.toml:
- **Package Name**: Use lowercase, underscore-separated world name
- **Entry Points**: Follow consistent naming pattern (exclude client functions)
- **Dependencies**: Include any world-specific requirements
- **Python Version**: Require >=3.13 for consistency

#### Register.py:
- **Imports**: Import actual classes from `__init__.py`
- **Metadata**: Use extracted values with fallbacks
- **Documentation**: Include game description from class docstring
- **Entry Points**: Reference actual class names, set CLIENT_FUNCTION to None

### Validation Rules

#### Required Fields:
- `WORLD_NAME`: Must match directory name
- `GAME_NAME`: Must be non-empty string
- `AUTHOR`: Must be non-empty string
- `VERSION`: Must be valid semver format
- `WORLD_CLASS`: Must reference existing class

#### Optional Fields:
- `IGDB_ID`: Integer or 0
- `WEB_WORLD_CLASS`: Class or None
- `CLIENT_FUNCTION`: Set to None (on hold)

## Example: Metroid Prime World

### Extracted Metadata
```
Plugin Name: metroidprime
Game Name: Metroid Prime
Author: Electro15
Version: 1.0.0
IGDB ID: 1105
World Class: MetroidPrimeWorld
Web World Class: MetroidPrimeWeb
Client Function: None
Description: Metroid Prime is a first-person action-adventure game originally for the Gamecube. Play as the bounty hunter Samus Aran as she traverses the planet Tallon IV and uncovers the plans of the Space Pirates.
Requirements: []
```

### Generated pyproject.toml
```toml
[project]
name = "metroidprime"
version = "1.0.0"
description = "Metroid Prime is a first-person action-adventure game originally for the Gamecube. Play as the bounty hunter Samus Aran as she traverses the planet Tallon IV and uncovers the plans of the Space Pirates."
authors = [
    {name = "Electro15"}
]
requires-python = ">=3.13"

[project.entry-points."mwgg.plugins"]
"metroidprime.WorldClass" = "metroidprime.Register:WORLD_CLASS"
"metroidprime.WebWorldClass" = "metroidprime.Register:WEB_WORLD_CLASS"
```

### Generated Register.py
```python
from . import MetroidPrimeWorld
from . import MetroidPrimeWeb

"""
Metroid Prime World Registration

This file contains the metadata and class references for the metroidprime world.
"""

# Required metadata
WORLD_NAME = "metroidprime"
GAME_NAME = "Metroid Prime"
IGDB_ID = 1105
AUTHOR = "Electro15"
VERSION = "1.0.0"

# Plugin entry points
WORLD_CLASS = MetroidPrimeWorld
WEB_WORLD_CLASS = MetroidPrimeWeb
CLIENT_FUNCTION = None
```

### Updated __init__.py imports
```python
# Add at top of __init__.py
from .Constants import GAME_NAME, AUTHOR, IGDB_ID, VERSION

# Remove or comment out existing metadata assignments
# game = "Metroid Prime"  # Now imported from Register
# author = "Electro15"    # Now imported from Register
# igdb_id = 1105         # Now imported from Register
# version = "1.0.0"      # Now imported from Register
```

## Implementation Scripts

### 1. Metadata Extractor
```python
class WorldMetadataExtractor:
    def extract_from_init_py(self, world_path: str) -> Dict[str, Any]:
        """Extract metadata from world's __init__.py file"""
        
    def extract_game_name(self, content: str) -> str:
        """Extract game name from class attributes or docstring"""
        
    def extract_author(self, content: str) -> str:
        """Extract author from class attributes"""
        
    def extract_version(self, content: str) -> str:
        """Extract version from various possible locations"""
```

### 2. File Generator
```python
class WorldFileGenerator:
    def generate_pyproject_toml(self, metadata: Dict[str, Any]) -> str:
        """Generate pyproject.toml content from metadata"""
        
    def generate_register_py(self, metadata: Dict[str, Any]) -> str:
        """Generate Register.py content from metadata"""
        
    def generate_for_world(self, world_path: str) -> None:
        """Generate both files for a single world"""
```

### 3. Batch Processor
```python
class WorldBatchProcessor:
    def process_all_worlds(self) -> None:
        """Process all worlds in parallel"""
        
    def validate_generated_files(self) -> List[str]:
        """Validate all generated files and return errors"""
        
    def create_migration_report(self) -> str:
        """Generate report of migration results including missing metadata list"""
```

## Migration Process

### Pre-Migration Checklist
- [X] Backup current world files
- [ ] Create test environment
- [ ] Document current metadata locations
- [ ] Establish rollback procedures

### Migration Steps
1. **Extract Metadata**: Run metadata extraction on all worlds
2. **Generate Files**: Create `pyproject.toml` and `Register.py` for each world
3. **Manual Review**: Review generated files for accuracy
4. **Update Imports**: Modify `__init__.py` files to use Register.py
5. **Test Worlds**: Verify each world still functions correctly
6. **Update Documentation**: Update any references to old metadata locations

### Post-Migration Validation
- [ ] All worlds load correctly
- [ ] Entry points register properly
- [ ] Metadata is consistent and accurate
- [ ] No functionality is lost
- [ ] Documentation is updated

## Benefits

### Immediate Benefits
1. **Consistent Structure**: All worlds follow same pattern
2. **Easier Maintenance**: Single source of truth for metadata
3. **Better Packaging**: Proper Python package structure
4. **Automated Registration**: Worlds auto-discover and register

### Long-term Benefits
1. **Plugin Ecosystem**: Enable third-party world plugins
2. **Distribution**: Worlds can be distributed as separate packages
3. **Versioning**: Proper semantic versioning for each world
4. **Dependencies**: Clear dependency management per world

## Risks and Mitigation

### Risks
1. **Breaking Changes**: Migration might break existing functionality
3. **Inconsistencies**: Generated files might not match expectations
4. **Performance**: Entry point discovery might impact startup time

### Mitigation Strategies
1. **Comprehensive Testing**: Test each world before and after migration
3. **Manual Review**: Human review of all generated files

## Success Criteria

### Technical Criteria
- [ ] All worlds have valid `pyproject.toml` and `Register.py` files
- [ ] All worlds auto-register via entry points
- [ ] No functionality is lost during migration
- [ ] Performance impact is minimal (<100ms startup time increase)

### Process Criteria
- [ ] All worlds tested and validated
- [ ] Documentation updated and accurate

## Future Enhancements

### Plugin Distribution
- Support for third-party world plugins

### Advanced Metadata
- Support for world categories and tags
- Support for world-specific configuration schemas

### Development Tools
- Code generation templates for new worlds

## Conclusion

This standardization will significantly improve the maintainability and extensibility of the MultiworldGG project. By establishing consistent patterns and proper package management, we enable future growth while maintaining backward compatibility. The phased approach ensures minimal disruption while achieving the desired standardization goals. 