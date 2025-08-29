#!/usr/bin/env python3
"""
cx_Freeze setup script for MultiWorldGG
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

# Because worlds is a namespace, it wants to include the entire folder, and there's no
# way to exclude it but also include the wheels worlds packages.
# Rename the folder, and we'll put it back afterwards.

if os.path.exists("worlds"):
    print("Renaming worlds folder to build_is_running_worlds to avoid cx_Freeze including it")
    os.rename("worlds", "build_is_running_worlds")
    os.environ["MWGG_BUILD_IS_RUNNING"] = "1"

from cx_Freeze import setup, Executable, build_exe

# Import project utilities
sys.path.insert(0, os.path.dirname(__file__))
from Utils import version_tuple, instance_name, archipelago_guid, is_windows, local_path

# Build configuration
build_exe_options = {
    "packages": [
        "kivy",
        "kivy_deps",
        "kivymd", 
        "websockets", 
        "cymem",
        "bsdiff4",
        "platformdirs",
        "certifi",
        "orjson",
        "typing_extensions",
        "dolphin_memory_engine",
        "pyshortcuts",
        "tqdm",
        "numpy",
        "colorama",
        "yaml",
        "jellyfish",
        "jinja2",
        "schema",
        "asynckivy",
        "PIL",
        "mwgg_gui",
        "worlds",
    ],
    "includes": [
        "ModuleUpdate",
        "BaseUtils",
        "CommonClient",
        "Gui",
        "ClientBuilder",
        "BaseClasses",
        "Options"
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
        "worlds",
        "kivy_deps.sdl2",
        "kivy_deps.glew",
        "kivy_deps.angle"
    ],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": ["kivymd", "mwgg_gui", "kivy"],
    "include_files": [
        ("data", "data"),
        ("LICENSE", "LICENSE"),
        ("README.md", "README.md"),
        ("_persistent_storage.yaml", "_persistent_storage.yaml"),
        ("data/SNI", "SNI") if os.path.exists("data/SNI") else None,
        ("EnemizerCLI", "EnemizerCLI") if os.path.exists("EnemizerCLI") else None,
        ("kivy/data", "lib/kivy/data"),
        ("kivy/include", "lib/kivy/include"),
        ("worlds_wheels", "worlds_wheels")
    ],
    "include_msvcr": False,
    "replace_paths": ["*."],
    "optimize": 1,
    "bin_includes": ["libffi.so", "libcrypt.so"] if platform.system() == "Linux" else []
}

# Remove None entries from include_files
build_exe_options["include_files"] = [item for item in build_exe_options["include_files"] if item is not None]

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

def install_wheels(type="default"):
    """Install wheels from default_wheels directory"""
    wheels_dir = Path(f"{type}_wheels")
    if wheels_dir.exists():
        print(f"Installing wheels from {type}_wheels...")
        for wheel_file in wheels_dir.glob("*.whl"):
            try:
                # First try with dependencies to ensure all required packages are installed
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    str(wheel_file), "--force-reinstall"
                ])
                print(f"Installed {wheel_file.name} with dependencies")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {wheel_file.name} with dependencies: {e}")
                # Fallback to no-deps if dependency installation fails
                try:
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", 
                        str(wheel_file), "--no-deps", "--force-reinstall"
                    ])
                    print(f"Installed {wheel_file.name} without dependencies")
                except subprocess.CalledProcessError as e2:
                    print(f"Failed to install {wheel_file.name}: {e2}")

def install_requirements():
    """Install requirements from main requirements.txt only"""
    req_file = Path("requirements.txt")
    if req_file.exists():
        print("Installing requirements from main requirements.txt...")
        try:
            # Use absolute path to ensure we're using the correct requirements.txt
            abs_req_file = req_file.absolute()
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(abs_req_file)
            ])
            print("Requirements installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install requirements: {e}")

def pre_build_setup():
    """Run pre-build setup tasks"""
    print("Running pre-build setup...")
    
    # Install requirements
    install_requirements()
    
    # Install wheels
    install_wheels("default")
        
    # Import our custom kivy hook to ensure it's loaded
    try:
        import cx_custom_hooks._kivy_ as kivy
    except ImportError as e:
        print(f"Warning: Could not load custom kivy hook: {e}")

def post_build_setup(build_exe_dir):
    """Run post-build setup tasks to include SDL2 and GLEW dependencies"""
    print("Running post-build setup...")
    os.environ["PIP_PREFIX"] = str(Path(build_exe_dir) / "world_plugins")
    install_wheels("worlds")
    print("Worlds installed successfully")

class CustomBuildExe(build_exe):
    """Custom build command that includes post-build setup and custom hooks"""
    
    def run(self):
        # Register our custom hooks before building
        self._register_custom_hooks()
        
        # Run the normal build
        super().run()
        # Get the build directory
        build_dir = self.build_exe
        if build_dir:
            if os.environ.get("MWGG_BUILD_IS_RUNNING") or os.path.exists("build_is_running_worlds"):
                print("Renaming worlds folder back to worlds")
                os.rename("build_is_running_worlds", "worlds")
                if "MWGG_BUILD_IS_RUNNING" in os.environ:
                    del os.environ["MWGG_BUILD_IS_RUNNING"]
            print(f"Build completed in: {build_dir}")
            # Run post-build setup
            post_build_setup(build_dir)
    
    def _register_custom_hooks(self):
        """Register our custom hooks with cx_Freeze
        
        This is not quite set up correctly but my brain is
        done fighting Claude.
        
        Info is here:
        https://github.com/marcelotduarte/cx_Freeze/blob/8.4.0/cx_Freeze/module.py#L412
        """
        try:
            # Import our custom hook
            import cx_custom_hooks._kivy_ as kivy

            # Monkey-patch cx_Freeze.hooks to include our hook
            import cx_Freeze.hooks
            
            # Add our hook functions to cx_Freeze.hooks
            if hasattr(kivy.Hook, 'kivy'):
                # Create function-based hooks from our class-based hook
                def load_kivy(finder, module):
                    hook = kivy.Hook(module)
                    hook.kivy(finder, module)
                    hook.kivy_binaries(finder, module)
                
                def load_kivy_binaries(finder, module):
                    hook = kivy.Hook(module)
                    hook.kivy_binaries(finder, module)
                
                # Add the functions to cx_Freeze.hooks
                cx_Freeze.hooks.load_kivy = load_kivy
                cx_Freeze.hooks.load_kivy_binaries = load_kivy_binaries

                print("Custom kivy hook registered with cx_Freeze")
            else:
                print("Warning: Custom kivy hook does not have required methods")

        except ImportError as e:
            print(f"Warning: Could not register custom kivy hook: {e}")
        except Exception as e:
            print(f"Error registering custom kivy hook: {e}")

if __name__ == "__main__":
    # Ensure DISTUTILS_DEBUG is not set to avoid debug output
    os.environ.pop('DISTUTILS_DEBUG', None)
    
    # Run pre-build setup
    pre_build_setup()
    
    # Setup configuration
    setup(
        name=instance_name,
        version=f"{version_tuple.major}.{version_tuple.minor}.{version_tuple.build}",
        description=f"{instance_name} - MultiWorld.GG - More, and Faster",
        author="DelilahIsDidi, TreZc0",
        options={"build_exe": build_exe_options},
        executables=executables,
        cmdclass={"build_exe": CustomBuildExe}
    )

