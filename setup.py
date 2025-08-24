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
        "kivymd", 
        "kivy_deps",
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
        "mwgg_gui",
        "worlds",
        "PIL"
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
        "build_is_running_worlds",
        "gui"
    ],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": ["worlds", "kivymd", "mwgg_gui", "kivy", "kivy_deps"],
    "include_files": [
        ("data", "data"),
        ("LICENSE", "LICENSE"),
        ("README.md", "README.md"),
        ("_persistent_storage.yaml", "_persistent_storage.yaml"),
        ("data/SNI", "SNI") if os.path.exists("data/SNI") else None,
        ("EnemizerCLI", "EnemizerCLI") if os.path.exists("EnemizerCLI") else None,
        ("kivy/include", "lib/kivy/include"),
        ("kivy/data", "lib/kivy/data"),
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

def install_wheels():
    """Install wheels from default_wheels directory"""
    wheels_dir = Path("default_wheels")
    if wheels_dir.exists():
        print("Installing wheels from default_wheels...")
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
    install_wheels()
    
    # Update modules (skip world requirements)
    try:
        import ModuleUpdate
        ModuleUpdate.update(yes=True)
        print("Module update completed")
    except Exception as e:
        print(f"Module update failed: {e}")

def post_build_setup(build_exe_dir):
    """Run post-build setup tasks to include SDL2 and GLEW dependencies"""
    print("Running post-build setup...")
    
    if is_windows:
        try:
            from kivy_deps import sdl2, glew  # type: ignore
            print("Including SDL2 and GLEW dependencies...")
            for folder in sdl2.dep_bins + glew.dep_bins:
                if os.path.exists(folder):
                    dest_path = os.path.join(build_exe_dir, "share", folder.rsplit(os.path.sep, 2)[1])
                    if os.path.exists(dest_path):
                        shutil.rmtree(dest_path)
                    shutil.copytree(folder, dest_path)
                    print(f"Copied {folder} -> {dest_path}")
                else:
                    print(f"Warning: SDL2/GLEW folder not found: {folder}")
        except ImportError as e:
            print(f"Warning: kivy_deps not available: {e}")

        except Exception as e:
            print(f"Error copying SDL2/GLEW dependencies: {e}")

class CustomBuildExe(build_exe):
    """Custom build command that includes post-build setup"""
    
    def run(self):
        # Run the normal build
        super().run()
        # Get the build directory
        build_dir = self.build_exe
        if build_dir:
            if os.environ.get("MWGG_BUILD_IS_RUNNING"):
                print("Renaming worlds folder back to worlds")
                os.rename("build_is_running_worlds", "worlds")
                del os.environ["MWGG_BUILD_IS_RUNNING"]
            print(f"Build completed in: {build_dir}")
            # Run post-build setup
            post_build_setup(build_dir)

if __name__ == "__main__":
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
