#!/usr/bin/env python3
"""
cx_Freeze setup script for MultiWorldGG
"""

import os
import sys
import platform
import subprocess
import shutil
import logging

from pathlib import Path

from cx_Freeze import setup, Executable, build_exe

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
# Because worlds is a namespace, it wants to include the entire folder, and there's no
# way to exclude it but also include the wheels worlds packages.
# Rename the folder, and we'll put it back afterwards.
if os.path.exists("worlds"):
    logger.debug("Renaming worlds folder to build_is_running_worlds to avoid cx_Freeze including it")
    os.rename("worlds", "build_is_running_worlds")
    os.environ["MWGG_BUILD_IS_RUNNING"] = "1"


# Import project utilities
sys.path.insert(0, os.path.dirname(__file__))
from Utils import version_tuple, instance_name, archipelago_guid, is_windows, local_path

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
        "cffi",
        "numpy",
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
        "mwgg_igdb",
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
        "kivy_deps.sdl2",
        "kivy_deps.glew",
        "kivy_deps.angle"
    ],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": ["kivymd", "mwgg_gui", "kivy", "worlds", "mwgg_igdb"],
    "include_files": [
        ("data", "data"),
        ("LICENSE", "LICENSE"),
        ("README.md", "README.md"),
        ("application.yaml", "application.yaml"),
        ("data/SNI", "SNI") if os.path.exists("data/SNI") else None,
        ("EnemizerCLI", "EnemizerCLI") if os.path.exists("EnemizerCLI") else None,
        ("kivy/data", "lib/kivy/data"),
        ("kivy/include", "lib/kivy/include"),
    ],
    "include_msvcr": False,
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
        import cx_custom_hooks._kivy_ as kivy
    except ImportError as e:
        logger.warning(f"Warning: Could not load custom kivy hook: {e}")

def post_build_setup(build_exe_dir):
    """Run post-build setup tasks to include SDL2 and GLEW dependencies"""
    logger.debug("Running post-build setup...")
    os.mkdir(os.path.join(build_exe_dir, "Players"))

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
                logger.debug("Renaming worlds folder back to worlds")
                os.rename("build_is_running_worlds", "worlds")
                if "MWGG_BUILD_IS_RUNNING" in os.environ:
                    del os.environ["MWGG_BUILD_IS_RUNNING"]
            logger.info(f"Build completed in: {build_dir}")
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

                logger.debug("Custom kivy hook registered with cx_Freeze")
            else:
                logger.debug("Warning: Custom kivy hook does not have required methods")

        except ImportError as e:
            logger.debug(f"Warning: Could not register custom kivy hook: {e}")
        except Exception as e:
            logger.debug(f"Error registering custom kivy hook: {e}")


# class CustomAppImage(bdist_appimage):
#     description = "build an app image from build output"
#     user_options = [
#         ("build-folder=", None, "Folder to convert to AppImage."),
#         ("dist-file=", None, "AppImage output file."),
#         ("app-dir=", None, "Folder to use for packaging."),
#         ("app-icon=", None, "The icon to use for the AppImage."),
#         ("app-exec=", None, "The application to run inside the image."),
#         ("yes", "y", 'Answer "yes" to all questions.'),
#     ]
#     build_folder: Path | None
#     dist_file: Path | None
#     app_dir: Path | None
#     app_name: str
#     app_exec: Path | None
#     app_icon: Path | None  # source file
#     app_id: str  # lower case name, used for icon and .desktop
#     yes: bool

#     def write_desktop(self) -> None:
#         assert self.app_dir, "Invalid app_dir"
#         desktop_filename = self.app_dir / f"{self.app_id}.desktop"
#         with open(desktop_filename, 'w', encoding="utf-8") as f:
#             f.write("\n".join((
#                 "[Desktop Entry]",
#                 f'Name={self.app_name}',
#                 f'Exec={self.app_exec}',
#                 "Type=Application",
#                 "Categories=Game",
#                 f'Icon={self.app_id}',
#                 ''
#             )))
#         desktop_filename.chmod(0o755)

#     def write_launcher(self, default_exe: Path) -> None:
#         assert self.app_dir, "Invalid app_dir"
#         launcher_filename = self.app_dir / "AppRun"
#         with open(launcher_filename, 'w', encoding="utf-8") as f:
#             f.write(f"""#!/bin/sh
# exe="{default_exe}"
# match="${{1#--executable=}}"
# if [ "${{#match}}" -lt "${{#1}}" ]; then
#     exe="$match"
#     shift
# elif [ "$1" = "-executable" ] || [ "$1" = "--executable" ]; then
#     exe="$2"
#     shift; shift
# fi
# tmp="${{exe#*/}}"
# if [ ! "${{#tmp}}" -lt "${{#exe}}" ]; then
#     exe="{default_exe.parent}/$exe"
# fi
# export LD_LIBRARY_PATH="${{LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}}$APPDIR/{default_exe.parent}/lib"
# $APPDIR/$exe "$@"
# """)
#         launcher_filename.chmod(0o755)

#     def install_icon(self, src: Path, name: str | None = None, symlink: Path | None = None) -> None:
#         assert self.app_dir, "Invalid app_dir"
#         try:
#             from PIL import Image
#         except ModuleNotFoundError:
#             if not self.yes:
#                 input("Requirement PIL is not satisfied, press enter to install it")
#             subprocess.call([sys.executable, '-m', 'pip', 'install', 'Pillow', '--upgrade'])
#             from PIL import Image
#         im = Image.open(src)
#         res, _ = im.size

#         if not name:
#             name = src.stem
#         ext = src.suffix
#         dest_dir = Path(self.app_dir / f'usr/share/icons/hicolor/{res}x{res}/apps')
#         dest_dir.mkdir(parents=True, exist_ok=True)
#         dest_file = dest_dir / f'{name}{ext}'
#         shutil.copy(src, dest_file)
#         if symlink:
#             symlink.symlink_to(dest_file.relative_to(symlink.parent))

#     def initialize_options(self) -> None:
#         assert self.distribution.metadata.name
#         self.build_folder = None
#         self.app_dir = None
#         self.app_name = self.distribution.metadata.name
#         self.app_icon = self.distribution.executables[0].icon
#         self.app_exec = Path('opt/{app_name}/{exe}'.format(
#             app_name=self.distribution.metadata.name, exe=self.distribution.executables[0].target_name
#         ))
#         self.dist_file = Path("dist", "{app_name}_{app_version}_{platform}.AppImage".format(
#             app_name=self.distribution.metadata.name, app_version=self.distribution.metadata.version,
#             platform=sysconfig.get_platform()
#         ))
#         self.yes = False

#     def finalize_options(self) -> None:
#         assert self.build_folder
#         if not self.app_dir:
#             self.app_dir = self.build_folder.parent / "AppDir"
#         self.app_id = self.app_name.lower()

#     def run(self) -> None:
#         assert self.build_folder and self.dist_file, "Command not properly set up"
#         assert (
#             self.app_icon and self.app_id and self.app_dir and self.app_exec and self.app_name
#         ), "AppImageCommand not properly set up"
#         self.dist_file.parent.mkdir(parents=True, exist_ok=True)
#         if self.app_dir.is_dir():
#             shutil.rmtree(self.app_dir)
#         self.app_dir.mkdir(parents=True)
#         opt_dir = self.app_dir / "opt" / self.app_name
#         shutil.copytree(self.build_folder, opt_dir)
#         root_icon = self.app_dir / f'{self.app_id}{self.app_icon.suffix}'
#         self.install_icon(self.app_icon, self.app_id, symlink=root_icon)
#         shutil.copy(root_icon, self.app_dir / '.DirIcon')
#         self.write_desktop()
#         self.write_launcher(self.app_exec)
#         print(f'{self.app_dir} -> {self.dist_file}')
#         subprocess.call(f'ARCH={build_arch} ./appimagetool -n "{self.app_dir}" "{self.dist_file}"', shell=True)

# class OSXAppCommand(bdist_mac):
#     description = "macOS .app bundle with extra_data symlinked into Contents/MacOS"
#     user_options = bdist_mac.user_options + [
#             ("yes", "y", "Answer 'yes' to all questions"),
#     ]
#     def initialize_options(self):
#         super().initialize_options()
#         self.yes = False
#         self.extra_data = None

#     def finalize_options(self):
#         super().finalize_options()
#         build_exe = self.get_finalized_command("build_exe")
#         self.extra_data = getattr(build_exe, "extra_data", [])

#     def run(self):
#         super().run()
#         bundle = self.bundle_dir
#         macos_dir = os.path.join(bundle, "Contents", "MacOS")
#         os.makedirs(macos_dir, exist_ok=True)

#         for item in self.extra_data:
#             name = os.path.basename(item)
#             link_path = os.path.join(macos_dir, name)
#             target = os.path.join("..", "Resources", name)

#             if os.path.lexists(link_path):
#                 os.remove(link_path)

#             os.symlink(target, link_path)



if __name__ == "__main__": 
    # Run pre-build setup
    pre_build_setup()
    
    # Setup configuration
    setup(
        name=instance_name,
        version=version_tuple.as_pep440_string(),
        description=f"{instance_name} - MultiWorld.GG - More, and Faster",
        author="DelilahIsDidi, TreZc0",
        options={"build_exe": build_exe_options},
        executables=executables,
        cmdclass={"build_exe": CustomBuildExe}
    )

