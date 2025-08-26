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
from cx_Freeze._compat import IS_MACOS, IS_WINDOWS, IS_LINUX

if TYPE_CHECKING:
    from cx_Freeze import ModuleFinder


__all__ = ("Hook",)


class Hook(ModuleHook):
    """The Hook class for kivy."""

    def kivy(self, finder: "ModuleFinder", module: "Module") -> None:
        """The kivy package."""
        # Essential modules from PyInstaller hook
        finder.include_module("xml.etree.cElementTree")
        finder.include_module("kivy.core.gl")
        finder.include_module("kivy.weakmethod") 
        finder.include_module("kivy.core.window.window_info")
        
        # Core Kivy packages
        finder.include_package("kivy.core")
        finder.include_package("kivy.graphics")
        finder.include_package("kivy.uix")
        finder.include_package("kivy.input")
        finder.include_package("kivy.lang")
        finder.include_package("kivy.utils")
        finder.include_package("kivy.resources")
        finder.include_package("kivy.support")
        finder.include_package("kivy.effects")
        
        # Dynamically include kivy_deps modules
        try:
            import kivy_deps
            import pkgutil
            import importlib.util
            
            for importer, modname, ispkg in pkgutil.iter_modules(kivy_deps.__path__):
                if ispkg:  # Only include packages
                    full_name = f"kivy_deps.{modname}"
                    try:
                        finder.include_package(full_name)
                        print(f"Including kivy_deps package: {full_name}")
                    except Exception as e:
                        print(f"Failed to include {full_name}: {e}")
                        
        except ImportError as e:
            print(f"Warning: Could not import kivy_deps: {e}")
        
        # Include Factory-registered modules
        try:
            from kivy.factory import Factory
            for cls_info in Factory.classes.values():
                if cls_info.get('module'):
                    finder.include_module(cls_info['module'])
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

    def kivy_binaries(self, finder: "ModuleFinder", module: "Module") -> None:
        """Add platform-specific binary patterns."""

        if IS_WINDOWS:
            binary_patterns = [
                'weakproxy*.pyd',
                'properties*.pyd', 
                '_clock*.pyd',
                '_event*.pyd',
                '_metrics*.pyd',
                'graphics/*.pyd',
                'graphics/cgl_backend/*.pyd'
            ]
            try:
                from kivy_deps import sdl2, glew

                for folder in sdl2.dep_bins + glew.dep_bins:
                    if Path(folder).exists():
                        for source in Path(folder).glob("*.dll"):
                            library = source.relative_to(folder).as_posix()
                            finder.lib_files[source] = f"lib/{library}"

            except ImportError:
                pass
            
        elif IS_LINUX:
            binary_patterns = [
                # Use wildcards to catch different naming conventions
                'weakproxy*.so',
                'properties*.so', 
                '_clock*.so',
                '_event*.so',
                '_metrics*.so',
                'graphics/*.so',
                'graphics/cgl_backend/*.so'
            ]
        elif IS_MACOS:
            binary_patterns = [
                # Check for both .so and .dylib
                'weakproxy*.so',
                'properties*.so',
                '_clock*.so', 
                '_event*.so',
                '_metrics*.so',
                'graphics/*.so',
                'graphics/cgl_backend/*.so',
                # Also check for .dylib variants (less common for Python extensions)
                'graphics/*.dylib',
                'graphics/cgl_backend/*.dylib'
            ]
        else:
            binary_patterns = []
        
        source_lib = module.file.parent
        # Add binary patterns to bin_includes
        for pattern in binary_patterns:
            for source in Path(source_lib).glob(pattern):
                library = source.relative_to(source_lib).as_posix()
                if library not in finder.lib_files:
                    finder.lib_files[source] = f"lib/{library}"