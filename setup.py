#!/usr/bin/env python3
"""
cx_Freeze setup script for MultiWorldGG
"""

import os
import sys
import platform
import logging

from cx_Freeze import setup, Executable, build_exe
from cx_Freeze.command.bdist_mac import bdist_mac

from Utils import version_tuple, instance_name, is_windows

logger = logging.getLogger("MultiWorld")

if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.WARNING, format='%(name)s: %(message)s', stream=sys.stdout)
if not logging.getLogger("MultiWorld").hasHandlers():
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setFormatter(logging.Formatter('%(message)s'))
    logger.setLevel(logging.INFO)

# Does not respect root logger level.
logging.getLogger("cx_Freeze").setLevel(logging.getLogger().level)
logging.getLogger("kivy").setLevel(logging.getLogger().level)

# Import project utilities
sys.path.insert(0, os.path.dirname(__file__))

# Build configuration
build_exe_options = {
    "packages": [
        # GUI/Graphics frameworks (complex packages with data files)
        "kivy",
        "kivy_deps" if is_windows else None,
        "kivymd",
        "asynckivy",

        # Core utilities (might be dynamically loaded or conditional)
        "websockets",
        "cymem",
        "PIL",

        # Platform-specific memory access (conditional imports)
        "pymem" if is_windows else None,
        "dolphin_memory_engine" if is_windows else None,

        # System utilities (might be conditionally imported)
        "pyshortcuts",

        # World-specific packages
        "orjson",
        "aiohttp",          # sc2 world
        "requests",         # multiple worlds
        "google.protobuf",  # sc2 world
        "pymongo",          # ff4fe world
        "loguru",           # sc2 world

        # Custom packages
        "mwgg_gui",
        "mwgg_tui",
        "mwgg_splash",
        "worlds"
    ],
    "includes": [
        "ModuleUpdate",
        "BaseUtils",
        "CommonClient",
        "ClientBuilder",
        "BaseClasses",
        "Options",
        "frontend_protocol",
        "kvui",
    ],
    "excludes": [
        "Cython",
        "PySide2",
        "pygments",
        "pandas",
        "matplotlib",
        "scipy",
        "pytest",
        "unittest",
        "test",
        "tests",
        "__pycache__",
        ".pytest_cache",
        "kivy_deps.sdl2",
        "kivy_deps.glew",
        "kivy_deps.angle"
    ],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": ["kivymd", "mwgg_gui", "kivy", "worlds", "PIL", "mwgg_tui", "mwgg_splash"],
    "include_files": [
        ("data", "data"),
        ("LICENSE", "LICENSE"),
        ("README.md", "README.md"),
        ("application.yaml", "application.yaml"),
        ("data/SNI", "SNI") if os.path.exists("data/SNI") else None,
        ("data/EnemizerCLI", "EnemizerCLI") if os.path.exists("data/EnemizerCLI") else None,
        ("kivy/data", "lib/kivy/data"),
        ("kivy/include", "lib/kivy/include"),
        # Mac/Linux only: ship astral's install.sh so first launch can install uv if it's not on PATH.
        # Windows installs uv via Inno Setup (winget, with PowerShell installer fallback) at install time.
        ("uv_runtime/install-uv.sh", "install-uv.sh") if not is_windows and os.path.exists("uv_runtime/install-uv.sh") else None,
    ],
    "include_msvcr": True,
    "replace_paths": ["*."],
    "optimize": 1,
    "bin_includes": ["libffi.so", "libcrypt.so"] if platform.system() == "Linux" else []
}

# Remove None entries from include_files and packages
build_exe_options["include_files"] = [item for item in build_exe_options["include_files"] if item is not None]
build_exe_options["packages"] = [item for item in build_exe_options["packages"] if item is not None]

# Executable configurations
executables = [
    Executable(
        script="MultiWorld.py",
        target_name="MultiWorldGG.exe" if is_windows else "MultiWorldGG",
        icon="data/icon.ico" if is_windows else "data/icon.png",
        base="Win32GUI" if is_windows else None,
        shortcut_name="MultiWorldGG",
        shortcut_dir="DesktopFolder"
    ),
    Executable(
        script="MultiServer.py", 
        target_name="MultiWorldGGServer.exe" if is_windows else "MultiWorldGGServer",
        icon="data/icon.ico" if is_windows else "data/icon.png",
        base=None,
        shortcut_name="MultiWorldGGServer",
        shortcut_dir="DesktopFolder"
    ),
    Executable(
        script="Generate.py",
        target_name="MultiWorldGGGenerate.exe" if is_windows else "MultiWorldGGGenerate", 
        icon="data/icon.ico" if is_windows else "data/icon.png",
        base=None,
        shortcut_name="MultiWorldGGGenerate",
        shortcut_dir="DesktopFolder"
    ),
    Executable(
        script="Patch.py",
        target_name="MultiWorldGGPatch.exe" if is_windows else "MultiWorldGGPatch",
        icon="data/icon.ico" if is_windows else "data/icon.png", 
        base=None,
        shortcut_name="MultiWorldGGPatch",
        shortcut_dir="DesktopFolder"
    )
]

# Windows-specific: Add debug version of MultiWorld
if is_windows:
    executables.append(
        Executable(
            script="MultiWorld.py",
            target_name="MultiWorldGGClientDebug.exe",
            icon="data/icon.ico",
            base=None,  # Console version for debugging
            shortcut_name="MultiWorldGGClient Debug",
            shortcut_dir="DesktopFolder"
        )
    )

def pre_build_setup():
    """Run pre-build setup tasks"""
    logger.debug("Running pre-build setup...")
    # Build requirements are in the wrapper build script
    # Import our custom kivy hook to ensure it's loaded
    try:
        import cx_custom_hooks._kivy_ as kivy # type: ignore
    except ImportError as e:
        logger.warning(f"Warning: Could not load custom kivy hook: {e}")

def post_build_setup(build_exe_dir):
    """Run post-build setup tasks to include SDL2 and GLEW dependencies"""
    logger.debug("Running post-build setup...")
    os.mkdir(os.path.join(build_exe_dir, "Players"))


def _register_custom_hooks():
    """Monkey-patch cx_Freeze.hooks to include our custom kivy hook.

    bdist_mac runs build_exe internally without going through CustomBuildExe,
    so this needs to be callable from both build paths.

    Info is here:
    https://github.com/marcelotduarte/cx_Freeze/blob/8.4.0/cx_Freeze/module.py#L412
    """
    try:
        import cx_custom_hooks._kivy_ as kivy
        import cx_Freeze.hooks

        if hasattr(kivy.Hook, 'kivy'):
            def load_kivy(finder, module):
                hook = kivy.Hook(module)
                hook.kivy(finder, module)
                hook.kivy_binaries(finder, module)

            def load_kivy_binaries(finder, module):
                hook = kivy.Hook(module)
                hook.kivy_binaries(finder, module)

            cx_Freeze.hooks.load_kivy = load_kivy
            cx_Freeze.hooks.load_kivy_binaries = load_kivy_binaries

            logger.debug("Custom kivy hook registered with cx_Freeze")
        else:
            logger.debug("Warning: Custom kivy hook does not have required methods")
    except ImportError as e:
        logger.debug(f"Warning: Could not register custom kivy hook: {e}")
    except Exception as e:
        logger.debug(f"Error registering custom kivy hook: {e}")


class CustomBuildExe(build_exe):
    """Custom build command that includes post-build setup and custom hooks"""

    def run(self):
        # Register our custom hooks before building
        _register_custom_hooks()

        # Run the normal build
        super().run()
        # Get the build directory
        build_dir = self.build_exe
        if build_dir:
            logger.info(f"Build completed in: {build_dir}")
            # Run post-build setup
            post_build_setup(build_dir)


class CustomBdistMac(bdist_mac):
    """bdist_mac that registers the custom kivy hook before building."""

    def run(self):
        _register_custom_hooks()
        super().run()


if __name__ == "__main__":
    # Run pre-build setup
    pre_build_setup()

    options = {"build_exe": build_exe_options}

    bdist_mac_options = {
        "bundle_name": instance_name,
        "iconfile": "data/icon.icns" if os.path.exists("data/icon.icns") else None,
    }
    options["bdist_mac"] = {k: v for k, v in bdist_mac_options.items() if v is not None}

    cmdclass = {"build_exe": CustomBuildExe}
    if sys.platform == "darwin":
        cmdclass["bdist_mac"] = CustomBdistMac

    # Setup configuration
    setup(
        name=instance_name,
        version=version_tuple.as_pep440_string(),
        description=f"{instance_name} - MultiWorld.GG - More, and Faster",
        author="DelilahIsDidi, TreZc0",
        options=options,
        executables=executables,
        cmdclass=cmdclass,
    )
