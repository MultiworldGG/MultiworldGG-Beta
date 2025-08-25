"""
cx_Freeze hook for Kivy

This hook ensures that all necessary Kivy modules, binaries, and data files
are included when building with cx_Freeze.
"""
from __future__ import annotations

import os
import sys
import glob
import importlib
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook
from cx_Freeze._compat import IS_MACOS, IS_MINGW, IS_WINDOWS

if TYPE_CHECKING:
    from cx_Freeze import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for kivy."""

    def kivy(self, finder: "ModuleFinder", module: "Module") -> None:
        """The kivy package."""
        # Include core Kivy packages
        finder.include_package("kivy.core")
        finder.include_package("kivy.graphics")
        finder.include_package("kivy.uix")
        finder.include_package("kivy.input")
        finder.include_package("kivy.lang")
        finder.include_package("kivy.metrics")
        finder.include_package("kivy.resources")
        finder.include_package("kivy.support")
        finder.include_package("kivy.utils")
        finder.include_package("kivy.extras")
        finder.include_package("kivy.effects")
        finder.include_package("kivy.eventmanager")
        finder.include_package("kivy.garden")
        finder.include_package("kivy.lib")
        finder.include_package("kivy.modules")
        finder.include_package("kivy.network")
        finder.include_package("kivy.storage")

        # Include Kivy deps
        finder.include_package("kivy_deps.sdl2")
        finder.include_package("kivy_deps.glew")
        finder.include_package("kivy_deps.angle")

        if IS_MINGW or IS_WINDOWS:
            extension = "*.pyd"
        elif IS_MACOS:
            extension = "*.dylib"
        else:
            extension = "*.so*"

        source_lib = module.file.parent
        for folder in source_lib.glob(f"*/lib/{extension}"):
            library = folder.relative_to(source_lib).as_posix()
            finder.lib_files[folder] = f"lib/{library}"

        if IS_MACOS:
            for folder in source_lib.glob(f"*/lib/*.so"):
                library = folder.relative_to(source_lib).as_posix()
                finder.lib_files[folder] = f"lib/{library}"

        if IS_MINGW or IS_WINDOWS:
            extension = "*.dll"

        try:
            sdl2_package = importlib.import_module('kivy_deps.sdl2')
            glew_package = importlib.import_module('kivy_deps.glew')
            angle_package = importlib.import_module('kivy_deps.angle')

            for folder in sdl2_package.dep_bins + glew_package.dep_bins + angle_package.dep_bins:
                if Path(folder).exists():
                    for source in Path(folder).glob(extension):
                        library = source.relative_to(folder).as_posix()
                        finder.lib_files[source] = f"lib/{library}"

        except ImportError:
            pass

    def kivy_tests(self, _finder: "ModuleFinder", module: "Module") -> None:
        """Ignore test modules."""
        module.ignore_names.add("kivy.tests")

    def kivy_tools(self, _finder: "ModuleFinder", module: "Module") -> None:
        """Ignore development tools."""
        module.ignore_names.add("kivy.tools")

    def kivy_tools_packaging(self, _finder: "ModuleFinder", module: "Module") -> None:
        """Ignore packaging tools."""
        module.ignore_names.add("kivy.tools.packaging")

    def kivy_tools_packaging_pyinstaller_hooks(self, _finder: "ModuleFinder", module: "Module") -> None:
        """Ignore PyInstaller hooks."""
        module.ignore_names.add("kivy.tools.packaging.pyinstaller_hooks")

    def kivy_data(self, finder: "ModuleFinder", module: "Module") -> None:
        """Include Kivy data files."""
        try:
            kivy_package = importlib.import_module('kivy')
            kivy_path = Path(kivy_package.__file__).parent
            
            # Commenting out data directory - we're overriding quite a bit of those files.
            # data_path = kivy_path / 'data'
            # if data_path.exists():
            #     finder.include_files.append((str(data_path), 'lib/kivy/data'))
            
            # Include include directory
            include_path = kivy_path / 'include'
            if include_path.exists():
                finder.include_files.append((str(include_path), 'lib/kivy/include'))
                
        except ImportError:
            # Kivy not installed, skip data files
            pass

    def kivy_binaries(self, finder: "ModuleFinder", module: "Module") -> None:
        """Add platform-specific binary patterns."""
        pass
        # if sys.platform == 'win32':
        #     binary_patterns = [
        #         '*.pyd',
        #         'kivy/graphics/*.pyd',
        #         'kivy/graphics/cgl_backend/*.pyd',
        #         'kivy/core/*.pyd',
        #         'kivy/core/audio/*.pyd',
        #         'kivy/core/clipboard/*.pyd',
        #         'kivy/core/image/*.pyd',
        #         'kivy/core/text/*.pyd',
        #         'kivy/core/window/*.pyd',
        #         'kivy/input/*.pyd',
        #         'kivy/input/providers/*.pyd',
        #         'kivy/lang/*.pyd',
        #         'kivy/metrics/*.pyd',
        #         'kivy/resources/*.pyd',
        #         'kivy/support/*.pyd',
        #         'kivy/utils/*.pyd',
        #         'kivy/uix/*.pyd',
        #         'kivy/deps/sdl2/*.pyd',
        #         'kivy/deps/glew/*.pyd',
        #         'kivy/deps/angle/*.pyd',
        #     ]
        #     try:
        #         sdl2_package = importlib.import_module('kivy_deps.sdl2')
        #         glew_package = importlib.import_module('kivy_deps.glew')
        #         angle_package = importlib.import_module('kivy_deps.angle')
                
        #         if sdl2_package.dep_bins:
        #             finder.include_files.append((str(sdl2_package.dep_bins), 'lib'))
        #         if glew_package.dep_bins:
        #             finder.include_files.append((str(glew_package.dep_bins), 'lib'))
        #         if angle_package.dep_bins:
        #             finder.include_files.append((str(angle_package.dep_bins), 'lib'))
        #     except ImportError:
        #         pass
            

        # elif sys.platform == 'linux':
        #     binary_patterns = [
        #         '*.so',
        #         'kivy/graphics/*.so',
        #         'kivy/graphics/cgl_backend/*.so',
        #         'kivy/core/*.so',
        #         'kivy/core/audio/*.so',
        #         'kivy/core/clipboard/*.so',
        #         'kivy/core/image/*.so',
        #         'kivy/core/text/*.so',
        #         'kivy/core/window/*.so',
        #         'kivy/input/*.so',
        #         'kivy/input/providers/*.so',
        #         'kivy/lang/*.so',
        #         'kivy/metrics/*.so',
        #         'kivy/resources/*.so',
        #         'kivy/support/*.so',
        #         'kivy/utils/*.so',
        #         'kivy/uix/*.so',
        #     ]
        # elif sys.platform == 'darwin':
        #     binary_patterns = [
        #         '*.so',
        #         '*.dylib',
        #         'kivy/graphics/*.so',
        #         'kivy/graphics/*.dylib',
        #         'kivy/graphics/cgl_backend/*.so',
        #         'kivy/graphics/cgl_backend/*.dylib',
        #         'kivy/core/*.so',
        #         'kivy/core/*.dylib',
        #         'kivy/core/audio/*.so',
        #         'kivy/core/audio/*.dylib',
        #         'kivy/core/clipboard/*.so',
        #         'kivy/core/clipboard/*.dylib',
        #         'kivy/core/image/*.so',
        #         'kivy/core/image/*.dylib',
        #         'kivy/core/text/*.so',
        #         'kivy/core/text/*.dylib',
        #         'kivy/core/window/*.so',
        #         'kivy/core/window/*.dylib',
        #         'kivy/input/*.so',
        #         'kivy/input/*.dylib',
        #         'kivy/input/providers/*.so',
        #         'kivy/input/providers/*.dylib',
        #         'kivy/lang/*.so',
        #         'kivy/lang/*.dylib',
        #         'kivy/metrics/*.so',
        #         'kivy/metrics/*.dylib',
        #         'kivy/resources/*.so',
        #         'kivy/resources/*.dylib',
        #         'kivy/support/*.so',
        #         'kivy/support/*.dylib',
        #         'kivy/utils/*.so',
        #         'kivy/utils/*.dylib',
        #         'kivy/uix/*.so',
        #         'kivy/uix/*.dylib',
        #     ]
        # else:
        #     binary_patterns = []
        
        # # Add binary patterns to bin_includes
        # for pattern in binary_patterns:
        #     if pattern not in finder.bin_includes:
        #         finder.bin_includes.append(pattern)
