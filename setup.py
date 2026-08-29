#!/usr/bin/env python3
"""
cx_Freeze setup script for MultiworldGG
"""

import os
import sys
import platform
import logging

from cx_Freeze import setup, Executable, build_exe
from cx_Freeze.command.bdist_mac import bdist_mac

# cx_Freeze's bundled numpy hook (cx_Freeze/hooks/_numpy_.py) is for numpy < 2.0, 
# so the workaround is not needed; stub the hook to prevent frozen exe errors.
import cx_Freeze.hooks._numpy_ as _cxf_numpy_hook
def _no_overrides_patch(self, finder, module):
    return None
_cxf_numpy_hook.Hook.numpy__core_overrides = _no_overrides_patch
_cxf_numpy_hook.Hook.numpy_core_overrides = _no_overrides_patch

from Utils import version_tuple, instance_name, is_windows, is_macos, FROZEN_TARGETS


def _find_libmtdev() -> str | None:
    """Locate libmtdev.so.1 on the build machine for explicit bundling.

    cx_Freeze's `bin_includes` only overrides exclusion of libs it already
    sees as link-time deps; libmtdev is runtime-loaded via ctypes from
    `kivy/lib/mtdev.py`, so cx_Freeze never finds it. We bundle it
    ourselves via `include_files` instead.
    """
    if platform.system() != "Linux":
        return None
    for path in (
        "/usr/lib/x86_64-linux-gnu/libmtdev.so.1",
        "/usr/lib64/libmtdev.so.1",
        "/usr/lib/libmtdev.so.1",
    ):
        if os.path.exists(path):
            return path
    return None


_libmtdev_path = _find_libmtdev()

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
        "LauncherComponents",
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
        # pygments must NOT be excluded: mwgg_gui.yaml_creator hard-imports it
        # (YamlLexer) and the frozen build dies without it.
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
    # cffi/pycparser must stay outside the zip for pythonnet (BFBB lib freezing)
    "zip_exclude_packages": ["kivymd", "mwgg_gui", "kivy", "worlds", "PIL", "mwgg_tui", "mwgg_splash", "numpy",
                             "cffi", "pycparser"],
    "include_files": [
        ("data", "data"),
        ("LICENSE", "LICENSE"),
        ("README.md", "README.md"),
        ("application.yaml", "application.yaml"),
        ("data/SNI", "SNI") if os.path.exists("data/SNI") else None,
        ("data/EnemizerCLI", "EnemizerCLI") if os.path.exists("data/EnemizerCLI") else None,
        ("kivy/data", "lib/kivy/data"),
        ("kivy/include", "lib/kivy/include"),
        # Mac/Linux only: ship the uv binary next to the frozen exe so the runtime can exec it
        # Windows installs uv via Inno Setup (winget, with PowerShell installer fallback) at install time.
        ("uv_runtime/uv", "uv") if (not is_windows and not is_macos and os.path.exists("uv_runtime/uv")) else None,
        ("uv_runtime/uv-arm64", "uv-arm64") if (is_macos and os.path.exists("uv_runtime/uv-arm64")) else None,
        ("uv_runtime/uv-x86_64", "uv-x86_64") if (is_macos and os.path.exists("uv_runtime/uv-x86_64")) else None,
        # NOTE: libmtdev.so.1 is copied at post-build time (see post_build_setup);
        # `include_files` put it under lib/ where Kivy's ctypes CDLL didn't find it.
    ],
    "include_msvcr": True,
    "replace_paths": ["*."],
    "optimize": 1,
    "bin_includes": ["libffi.so", "libcrypt.so"] if platform.system() == "Linux" else []
}

# Remove None entries from include_files and packages
build_exe_options["include_files"] = [item for item in build_exe_options["include_files"] if item is not None]
build_exe_options["packages"] = [item for item in build_exe_options["packages"] if item is not None]

# Launcher exe names derive from BaseUtils.FROZEN_TARGETS so they can't drift.
# test_launcher_stack.py greps this file's target_name literals against
# FROZEN_TARGETS.values(); the Debug variant has no entry, hence computed here.
_exe_suffix = ".exe" if is_windows else ""
_launcher_exe_name = FROZEN_TARGETS["Launcher"] + _exe_suffix
_launcher_debug_exe_name = FROZEN_TARGETS["Launcher"] + "Debug" + _exe_suffix

# Executable configurations
executables = [
    Executable(
        script="MultiWorld.py",
        target_name="MultiworldGG.exe" if is_windows else "MultiworldGG",
        icon="data/icon.ico" if is_windows else "data/icon.png",
        base="gui" if is_windows else None,
        shortcut_name="MultiworldGG",
        shortcut_dir="DesktopFolder"
    ),
    Executable(
        script="MultiServer.py", 
        target_name="MultiworldGGServer.exe" if is_windows else "MultiworldGGServer",
        icon="data/icon.ico" if is_windows else "data/icon.png",
        base=None,
        shortcut_name="MultiworldGGServer",
        shortcut_dir="DesktopFolder"
    ),
    Executable(
        script="Generate.py",
        target_name="MultiworldGGGenerate.exe" if is_windows else "MultiworldGGGenerate", 
        icon="data/icon.ico" if is_windows else "data/icon.png",
        base=None,
        shortcut_name="MultiworldGGGenerate",
        shortcut_dir="DesktopFolder"
    ),
    Executable(
        script="Patch.py",
        target_name="MultiworldGGPatch.exe" if is_windows else "MultiworldGGPatch",
        icon="data/icon.ico" if is_windows else "data/icon.png",
        base=None,
        shortcut_name="MultiworldGGPatch",
        shortcut_dir="DesktopFolder"
    ),
    # Standalone Launcher: stays open, spawning everything else as separate
    # processes; bare double-click behaves like the pre-split client (gui base,
    # no console window). cx_Freeze >= 8.5 dropped the legacy "Win32GUI" name.
    Executable(
        script="Launcher.py",
        target_name=_launcher_exe_name,
        icon="data/icon.ico" if is_windows else "data/icon.png",
        base="gui" if is_windows else None,
        shortcut_name="MultiworldGG Launcher",
        shortcut_dir="DesktopFolder"
    )
]

# Windows-specific: Add debug versions
if is_windows:
    executables.append(
        Executable(
            script="MultiWorld.py",
            target_name="MultiworldGGClientDebug.exe",
            icon="data/icon.ico",
            base=None,  # Console version for debugging
            shortcut_name="MultiworldGGClient Debug",
            shortcut_dir="DesktopFolder"
        )
    )
    executables.append(
        Executable(
            script="Launcher.py",
            target_name=_launcher_debug_exe_name,
            icon="data/icon.ico",
            base=None,  # Console version for debugging / CI smoke testing
            shortcut_name="MultiworldGG Launcher Debug",
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

    # world_launcher_cache.json.gz is a stray from the removed pre-split launcher
    # cache; the ("data", "data") copy would ship it from a dev checkout, so delete it.
    stray_cache = os.path.join(build_exe_dir, "data", "world_launcher_cache.json.gz")
    if os.path.isfile(stray_cache):
        os.remove(stray_cache)
        logger.info(f"Removed stray {stray_cache} from frozen build output.")

    # Ship empty Players/ and custom_worlds/ dirs. No README breadcrumb: a stray
    # .txt gets picked up by the player-file / custom-world scanners.
    for subdir in ("Players", "custom_worlds"):
        os.makedirs(os.path.join(build_exe_dir, subdir), exist_ok=True)

    # Linux: copy libmtdev.so.1 to the bundle root. include_files/bin_includes are
    # unreliable for it (runtime ctypes load, not a link-time dep); $ORIGIN placement
    # plus MultiWorld.py's absolute-path pre-load is the combination that works.
    if platform.system() == "Linux":
        import shutil
        libmtdev = _find_libmtdev()
        if libmtdev:
            dest = os.path.join(build_exe_dir, "libmtdev.so.1")
            shutil.copy(libmtdev, dest)  # follows symlink, dest is a regular file
            logger.info(f"Bundled {libmtdev} -> {dest}")
        else:
            logger.warning("libmtdev.so.1 not found on build host; AppImage will "
                           "log a benign 'MTDev is not supported' warning at startup.")


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
