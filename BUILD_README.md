# MultiWorldGG Build System

This directory contains the build system for creating standalone executables of MultiWorldGG using cx_Freeze.

## Files

- `setup.py` - Main cx_Freeze setup script
- `pyproject.toml` - Modern Python project configuration (alternative to setup.py)
- `build_exe.py` - Automated build script with dependency management
- `BUILD_README.md` - This file

## Prerequisites

- Python 3.13 or higher
- pip
- Virtual environment (recommended)

## Quick Start

### Option 1: Using the automated build script (Recommended)

```bash
# Navigate to the src directory
cd src

# Run the build script
python build_exe.py --verify
```

The build script will:
1. Install build_requirements.txt (includes cx_Freeze)
2. Install requirements.txt
3. Fetch the latest mwgg_gui / mwgg_tui / mwgg_splash wheel from each sibling repo's
   GitHub releases (via `install_wheels()`) and pip-install them into the build venv
4. Generate setup.ini (Windows only, for Inno Setup)
5. Run the cx_Freeze build via setup.py build_exe
6. Verify the build output (with --verify)

Worlds (infra `_bizhawk`, `_debug`, `_manual`, `_sni`, `_tracker`, `generic`) are bundled
directly from `src/worlds/` source — there is no separate worlds wheel build. Per-game
worlds and the mwgg_igdb game index are NOT installed at build time; they're git-pulled
at first run by ModuleUpdate.update() and ModuleUpdate.install_worlds().

### Option 2: Manual build using setup.py

```bash
# Navigate to the src directory
cd src

# Install build requirements & cx_Freeze
pip install -r build_requirements.txt

# Install requirements
pip install -r requirements.txt

# Fetch sibling-repo wheels (mwgg_gui, mwgg_tui, mwgg_splash) from their latest
# GitHub releases. This is what build_exe.install_wheels() does; you can also
# invoke it directly:
python -c "import build_exe; build_exe.install_wheels()"

# Run the build (mwgg_igdb is git-pulled at first run, not at build time)
python setup.py build_exe
```

### Option 3: Using pyproject.toml

```bash
# Navigate to the src directory
cd src

# Install build dependencies
pip install cx-Freeze==8.4.0 setuptools>=70.0.0

# Run build using pyproject.toml
python -m cx_Freeze.build_exe
```

## Build Script Options

The `build_exe.py` script supports several command-line options:

```bash
python build_exe.py [OPTIONS]

Options:
  --clean              Clean build directory before building
  --skip-requirements  Skip requirements installation
  --skip-wheels        Skip wheel installation
  --skip-modules       Skip module update
  --verify             Verify build output after building
```

### Examples

```bash
# Clean build with verification
python build_exe.py --clean --verify

# Skip requirements installation (if already installed)
python build_exe.py --skip-requirements

# Skip wheel installation (if already installed)
python build_exe.py --skip-wheels

# Minimal build (skip all optional steps)
python build_exe.py --skip-requirements --skip-wheels --skip-modules
```

## Generated Executables

The build process creates the following executables:

- **MultiWorld.exe** - GUI application (main client)
- **MultiWorldDebug.exe** - Console version for debugging (Windows only)
- **MultiServer.exe** - Command-line server
- **Generate.exe** - Command-line generator
- **Patch.exe** - Command-line patcher

## Build Output

The build output is located in:
```
build/exe.{platform}-{python_version}/
```

For example:
```
build/exe.win-amd64-3.13/
```

### Contents

The build directory contains:
- Executable files (.exe on Windows)
- `data/` - Application data files
- `lib/` - Python libraries and dependencies
- `LICENSE` - License file
- `README.md` - README file

## Troubleshooting

### Common Issues

1. **Missing dependencies**
   - Run `python build_exe.py --clean` to ensure a fresh build
   - Check that all requirements are installed: `pip list`

2. **Wheel installation failures**
   - Ensure network access to api.github.com and github.com
   - Confirm the sibling repos (`MultiworldGG/mwgg-gui`, `mwgg-tui`, `mwgg-splash`) have a
     published release with a wheel asset attached
   - Try invoking the fetch directly: `python -c "import build_exe; build_exe.install_wheels()"`

3. **Module update failures**
   - Check network connectivity
   - mwgg_igdb is git-pulled at first run; verify the venv at the platform-specific
     install path (`%LOCALAPPDATA%\MultiworldGG\mwgg_venv` on Windows) has internet access

4. **Build failures**
   - Check Python version (requires 3.13+)
   - Ensure cx_Freeze is installed: `pip install cx-Freeze==8.4.0`
   - Check for conflicting packages

### Debug Mode

For debugging build issues, you can run the build script with verbose output:

```bash
python build_exe.py --verify 2>&1 | tee build.log
```

### Manual Verification

To manually verify the build output:

```bash
# Check executables
ls build/exe.*/*.exe

# Check directories
ls build/exe.*/

# Test an executable
./build/exe.*/MultiWorld.exe --help
```

## Platform Support

- **Windows**: Full support with .exe files and icons
- **Linux**: Support for ELF binaries
- **macOS**: Support for .app bundles (requires additional setup)

## Customization

### Modifying Executables

Edit `setup.py` to modify executable configurations:

```python
executables = [
    Executable(
        script="MultiWorld.py",
        target_name="MultiWorld.exe",
        icon="data/khapicon.ico",
        base="Win32GUI",  # GUI mode
        # base=None,      # Console mode
    ),
    # ... other executables
]
```

### Adding Files

To include additional files, modify the `include_files` list in `setup.py`:

```python
"include_files": [
    ("../data", "data"),
    ("custom_file.txt", "custom_file.txt"),
    ("custom_dir", "custom_dir"),
]
```

### Package Configuration

Modify package includes/excludes in `setup.py`:

```python
"packages": [
    "worlds",
    "kivy",
    # Add more packages here
],
"excludes": [
    "Cython",
    "pytest",
    # Add packages to exclude here
]
```

## Dependencies

### Required Python Packages

See `requirements.txt` for the complete list. Key dependencies include:
- cx-Freeze==8.4.0
- kivy>=2.3.1
- kivymd>=2.0.1.dev0
- websockets>=13.0.1
- PyYAML>=6.0.2
- numpy>=1.26.1
- Pillow>=11.2.1

### System Dependencies

- **Windows**: Visual Studio Build Tools (for some packages)
- **Linux**: Development headers (python3-dev, etc.)
- **macOS**: Xcode Command Line Tools

## Contributing

When modifying the build system:

1. Test on multiple platforms if possible
2. Update this README with any changes
3. Ensure backward compatibility
4. Add appropriate error handling

## License

This build system is part of MultiWorldGG and is licensed under the same terms as the main project.
