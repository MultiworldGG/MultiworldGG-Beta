from __future__ import annotations

import json
import zipfile
import os
import threading
import ast
import shutil
import logging
from io import BytesIO
from pathlib import Path
from typing import Dict, Any, Optional, Union, BinaryIO, Literal, List, Tuple, TYPE_CHECKING

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
    path: Optional[str]

    def __init__(self, path: Optional[str] = None):
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

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
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

    def get_manifest(self) -> Dict[str, Any]:
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

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        from Utils import tuplize_version, version_tuple
        try:
            manifest = super().read_contents(opened_zipfile)
        except KeyError as e:
            # Feature gate: archipelago.json is optional for versions < 0.7.250
            if version_tuple < (0, 7, 250):
                # Return empty manifest, metadata will remain None
                return {}
            raise
        if "game" in manifest:
            self.game = manifest["game"]
        for version_key in ("world_version", "minimum_ap_version", "maximum_ap_version"):
            if version_key in manifest:
                setattr(self, version_key, tuplize_version(manifest[version_key]))
        return manifest

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super().get_manifest()
        manifest["game"] = self.game
        manifest["compatible_version"] = 7
        for version_key in ("world_version", "minimum_ap_version", "maximum_ap_version"):
            version = getattr(self, version_key)
            if version:
                manifest[version_key] = version.as_simple_string()
        return manifest


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

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        manifest = super().read_contents(opened_zipfile)
        self.player = manifest["player"]
        self.server = manifest["server"]
        self.player_name = manifest["player_name"]
        return manifest

    def get_manifest(self) -> Dict[str, Any]:
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
    procedure: Union[Literal["custom"], List[Tuple[str, List[Any]]]] = "custom"

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super(APPatch, self).get_manifest()
        manifest["procedure"] = self.procedure
        manifest["compatible_version"] = 6
        return manifest


# Templates for generating pip-installable world packages
PYPROJECT_TEMPLATE = """[project]
name = "worlds.{module_name}"
version = "{version}"
description = "MultiWorld: {game_name}"
classifiers = ["Private :: Do Not Upload"]
requires-python = ">=3.12"
{authors_section}
{client_section}

[tool.setuptools.packages.find]
where = ["src"]
include = ["worlds.{module_name}"]
namespaces = true
"""

REGISTER_TEMPLATE = """from . import {world_class}, {web_class}
{client_import}

WORLD_NAME = "{module_name}"

GAME_NAME = "{game_name}"
AUTHOR = "{authors}"
VERSION = "{version}"

WORLD_CLASS = {world_class}
WEB_WORLD_CLASS = {web_class}
CLIENT_FUNCTION = {client_function}
"""


def parse_world_classes(init_py_content: str) -> tuple[Optional[str], Optional[str]]:
    """
    Parse __init__.py to find World and WebWorld class names.
    
    Returns:
        Tuple of (world_class_name, web_class_name) or (None, None) if not found
    """
    try:
        tree = ast.parse(init_py_content)
        world_class = None
        web_class = None
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check base classes
                for base in node.bases:
                    # Handle direct name references (e.g., World, WebWorld)
                    if isinstance(base, ast.Name):
                        if base.id == "World":
                            world_class = node.name
                        elif base.id == "WebWorld":
                            web_class = node.name
                    # Handle attribute references (e.g., worlds.AutoWorld.World)
                    elif isinstance(base, ast.Attribute):
                        if base.attr == "World":
                            world_class = node.name
                        elif base.attr == "WebWorld":
                            web_class = node.name
        
        return world_class, web_class
    except Exception as e:
        logger.warning(f"Failed to parse __init__.py for class names: {e}")
        return None, None


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


def prepare_apworld_for_pip(apworld_path: str, temp_dir: Path, manifest: dict[str, object]) -> Optional[Path]:
    """
    Restructure apworld to pip-installable format and return path to installable archive.
    
    Args:
        apworld_path: Path to the .apworld file
        temp_dir: Temporary directory for processing
        
    Returns:
        Path to the installable .zip file, or None on failure
    """
    try:
        module_name = apworld_path.stem
        
        # Read apworld metadata
        game_name = manifest.get("game", "Unknown")
        authors = manifest.get("authors", ["Unknown"])
        world_version = manifest.get("world_version")
        
        # Extract apworld to temp directory
        extract_dir = temp_dir / f"apworld_{module_name}" / "src" / "worlds"
        extract_dir.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(apworld_path, 'r') as apworld_zip:
            apworld_zip.extractall(extract_dir)
        
        # Find World and WebWorld classes in __init__.py
        init_py_path = extract_dir / module_name / "__init__.py"
        if not init_py_path.exists():
            logger.warning(f"__init__.py not found in {module_name}")
            return None
        
        init_py_content = init_py_path.read_text(encoding='utf-8')
        world_class, web_class = parse_world_classes(init_py_content)
        
        if not world_class or not web_class:
            logger.warning(f"Could not find World/WebWorld classes in {module_name}/__init__.py")
            return None
        
        # Find client function from Component with Type.CLIENT
        client_function_name = parse_client_function(init_py_content)
        
        # Create pip-installable structure
        # Package name format: worlds_{module_name}-{version}
        package_name = f"worlds_{module_name}"
        package_dir = temp_dir / f"apworld_{module_name}"
        
        # Generate pyproject.toml
        authors_section = "\n".join([f'[[project.authors]]\nname = "{author}"' for author in authors])
        
        # Generate client entry point section if client function found
        client_section = ""
        if client_function_name:
            client_section = f'\n[project.entry-points."mwgg.client"]\n"worlds.{module_name}.Client" = "worlds.{module_name}.Register:CLIENT_FUNCTION"'
        
        pyproject_content = PYPROJECT_TEMPLATE.format(
            module_name=module_name,
            version=world_version,
            game_name=game_name,
            authors_section=authors_section,
            client_section=client_section
        )
        (package_dir / "pyproject.toml").write_text(pyproject_content, encoding='utf-8')
        
        # Generate Register.py
        # Use client function from Component if found, otherwise None
        client_import = ""
        client_function = "None"
        if client_function_name:
            # Function is defined in __init__.py, so we can reference it directly
            # Import it from the parent module (__init__.py)
            client_import = f"from . import {client_function_name}"
            client_function = client_function_name
        
        register_content = REGISTER_TEMPLATE.format(
            module_name=module_name,
            game_name=game_name,
            authors=authors,
            version=world_version,
            world_class=world_class,
            web_class=web_class,
            client_import=client_import,
            client_function=client_function
        )
        (extract_dir / "Register.py").write_text(register_content, encoding='utf-8')
        
        # Create installable zip
        installable_zip = temp_dir / f"{package_name}-{world_version}.zip"
        with zipfile.ZipFile(installable_zip, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(package_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(package_dir)
                    zip_file.write(file_path, arcname)
        
        return installable_zip
    except Exception as e:
        logger.warning(f"Failed to prepare apworld for pip: {e}")
        return None

