from __future__ import annotations

import json
import zipfile
import os
import threading
import ast
import shutil
import importlib
import logging
import hashlib
from io import BytesIO
from pathlib import Path
from typing import Any, Optional, Union, BinaryIO, Literal, TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from Utils import Version

logger = logging.getLogger("MultiWorld")

semaphore = threading.Semaphore(os.cpu_count() or 4)

del threading

container_version: int = 7


def is_ap_player_container(game: str, data: bytes, player: int):
    if not zipfile.is_zipfile(BytesIO(data)):
        return False
    with zipfile.ZipFile(BytesIO(data), mode='r') as zf:
        if "archipelago.json" in zf.namelist():
            manifest = json.loads(zf.read("archipelago.json"))
            if "game" in manifest and "player" in manifest:
                if game == manifest["game"] and player == manifest["player"]:
                    return True
    return False


class InvalidDataError(Exception):
    """
    Since games can override `read_contents` in APContainer,
    this is to report problems in that process.
    """


class APContainer:
    """A zipfile containing at least archipelago.json, which contains a manifest json payload."""
    version: int = container_version
    compression_level: int = 9
    compression_method: int = zipfile.ZIP_DEFLATED
    manifest_path: str = "archipelago.json"
    path: Optional[Path]

    def __init__(self, path: Optional[Path] = None):
        self.path = path

    def write(self, file: Optional[Union[str, BinaryIO]] = None) -> None:
        zip_file = file if file else self.path
        if not zip_file:
            raise FileNotFoundError(f"Cannot write {self.__class__.__name__} due to no path provided.")
        with semaphore:  # TODO: remove semaphore once generate_output has a thread limit
            with zipfile.ZipFile(
                    zip_file, "w", self.compression_method, True, self.compression_level) as zf:
                if file:
                    self.path = zf.filename
                self.write_contents(zf)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        manifest = self.get_manifest()
        try:
            manifest_str = json.dumps(manifest)
        except Exception as e:
            raise Exception(f"Manifest {manifest} did not convert to json.") from e
        else:
            opened_zipfile.writestr(self.manifest_path, manifest_str)

    def read(self, file: Optional[Union[str, BinaryIO]] = None) -> None:
        """Read data into patch object. file can be file-like, such as an outer zip file's stream."""
        zip_file = file if file else self.path
        if not zip_file:
            raise FileNotFoundError(f"Cannot read {self.__class__.__name__} due to no path provided.")
        with zipfile.ZipFile(zip_file, "r") as zf:
            if file:
                self.path = zf.filename
            try:
                self.read_contents(zf)
            except Exception as e:
                message = ""
                if len(e.args):
                    arg0 = e.args[0]
                    if isinstance(arg0, str):
                        message = f"{arg0} - "
                raise InvalidDataError(f"{message}This might be the incorrect world version for this file") from e

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> dict[str, Any]:
        try:
            assert self.manifest_path.endswith("archipelago.json"), "Filename should be archipelago.json"
            manifest_info = opened_zipfile.getinfo(self.manifest_path)
        except KeyError as e:
            for info in opened_zipfile.infolist():
                if info.filename.endswith("archipelago.json"):
                    manifest_info = info
                    self.manifest_path = info.filename
                    break
            else:
                raise e
        with opened_zipfile.open(manifest_info, "r") as f:
            manifest = json.load(f)
        if manifest["compatible_version"] > self.version:
            raise Exception(f"File (version: {manifest['compatible_version']}) too new "
                            f"for this handler (version: {self.version})")
        return manifest

    def get_manifest(self) -> dict[str, Any]:
        return {
            # minimum version of patch system expected for patching to be successful
            "compatible_version": 5,
            "version": container_version,
        }


class APWorldContainer(APContainer):
    """A zipfile containing a world implementation."""
    game: str | None = None
    world_version: "Version | None" = None
    minimum_ap_version: "Version | None" = None
    maximum_ap_version: "Version | None" = None
    apworld_spec: importlib.machinery.ModuleSpec | None = None
    

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> dict[str, Any]:
        from Utils import tuplize_version, version_tuple
        try:
            manifest = super().read_contents(opened_zipfile)
        except KeyError as e:
            # Feature gate: archipelago.json is optional for versions < 0.7.300
            if version_tuple < (0, 7, 300):
                # Return empty manifest, metadata will remain None
                return {}
            raise
        if "game" in manifest:
            self.game = manifest["game"]
        for version_key in ("world_version", "minimum_ap_version", "maximum_ap_version"):
            if version_key in manifest:
                setattr(self, version_key, tuplize_version(manifest[version_key]))
        return manifest

    def get_manifest(self) -> dict[str, Any]:
        manifest = super().get_manifest()
        manifest["game"] = self.game
        manifest["compatible_version"] = 7
        for version_key in ("world_version", "minimum_ap_version", "maximum_ap_version"):
            version = getattr(self, version_key)
            if version:
                manifest[version_key] = version.as_simple_string()
        return manifest

    def sys_modules_import_apworld(self):
        """Locate, register, and execute the apworld zipfile's `worlds.<stem>` module."""
        import sys
        import importlib.util
        from zipimport import zipimporter
        name = f"worlds.{self.path.stem}"
        importer = zipimporter(str(self.path.absolute()))
        spec = importer.find_spec(name)
        if spec is None:
            raise ImportError(f"apworld {self.path} does not contain module {name}")
        self.apworld_spec = spec
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module

class APPlayerContainer(APContainer):
    """A zipfile containing at least archipelago.json meant for a player"""
    game: Optional[str] = None
    patch_file_ending: str = ""

    player: Optional[int]
    player_name: str
    server: str

    def __init__(self, path: Optional[str] = None, player: Optional[int] = None,
                 player_name: str = "", server: str = ""):
        super().__init__(path)
        self.player = player
        self.player_name = player_name
        self.server = server

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> dict[str, Any]:
        manifest = super().read_contents(opened_zipfile)
        self.player = manifest["player"]
        self.server = manifest["server"]
        self.player_name = manifest["player_name"]
        return manifest

    def get_manifest(self) -> dict[str, Any]:
        manifest = super().get_manifest()
        manifest.update({
            "server": self.server,  # allow immediate connection to server in multiworld. Empty string otherwise
            "player": self.player,
            "player_name": self.player_name,
            "game": self.game,
            "patch_file_ending": self.patch_file_ending,
        })
        return manifest


class APPatch(APPlayerContainer):
    """
    An `APPlayerContainer` that represents a patch file.
    It includes the `procedure` key in the manifest to indicate that it is a patch.

    Your implementation should inherit from this if your output file
    represents a patch file, but will not be applied with AP's `Patch.py`
    """
    procedure: Union[Literal["custom"], list[tuple[str, list[Any]]]] = "custom"

    def get_manifest(self) -> dict[str, Any]:
        manifest = super(APPatch, self).get_manifest()
        manifest["procedure"] = self.procedure
        manifest["compatible_version"] = 6
        return manifest

def parse_client_function(init_py_content: str) -> Optional[str]:
    """
    Parse __init__.py to find client function from Component with Type.CLIENT.
    
    Looks for: components.append(Component(..., func=function_name, component_type=Type.CLIENT, ...))
    
    Returns:
        Function name if found, None otherwise
    """
    try:
        tree = ast.parse(init_py_content)
        
        for node in ast.walk(tree):
            # Look for method calls: components.append(...)
            if isinstance(node, ast.Call):
                if (isinstance(node.func, ast.Attribute) and 
                    node.func.attr == "append" and
                    isinstance(node.func.value, ast.Name) and
                    node.func.value.id == "components"):
                    
                    # Check if argument is Component(...)
                    if node.args and isinstance(node.args[0], ast.Call):
                        component_call = node.args[0]
                        if (isinstance(component_call.func, ast.Name) and 
                            component_call.func.id == "Component"):
                            
                            # Check keyword arguments
                            has_client_type = False
                            func_name = None
                            
                            for keyword in component_call.keywords:
                                if keyword.arg == "component_type":
                                    # Check if it's Type.CLIENT
                                    if (isinstance(keyword.value, ast.Attribute) and
                                        isinstance(keyword.value.value, ast.Name) and
                                        keyword.value.value.id == "Type" and
                                        keyword.value.attr == "CLIENT"):
                                        has_client_type = True
                                elif keyword.arg == "func":
                                    # Extract function name
                                    if isinstance(keyword.value, ast.Name):
                                        func_name = keyword.value.id
                            
                            if has_client_type and func_name:
                                return func_name
        
        return None
    except Exception as e:
        logger.warning(f"Failed to parse __init__.py for client function: {e}")
        return None
