"""Launcher component registry and the launcher-facing component data model.

Top-level on purpose: launcher-side consumers (the GUI frontend, MultiWorld's
routing, the standalone Launcher) import this module directly. Importing it as
worlds.LauncherComponents would execute worlds/__init__ first, whose one-shot
world load belongs to client processes only -- the launcher must render its
component surfaces without importing any world. World modules keep importing
worlds.LauncherComponents, which re-exports this module's objects.
"""
import dataclasses
import hashlib
import json
import logging
import os
import pathlib
import pkgutil
import subprocess
import sys
import tempfile
import weakref
import webbrowser
from enum import Enum
from typing import Any, Optional, Callable, Iterable

from BaseUtils import get_client_exe, launch_exe, spawn_client
from Utils import local_path, open_filename, is_frozen, is_kivy_running, is_windows, \
    open_file, open_in_text_editor, user_path, read_apignore, FROZEN_TARGETS

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

_DEFAULT_ICON_PATH = local_path("data", "icon.png")
_LAUNCHER_ICON_CACHE_DIR = os.path.join(tempfile.gettempdir(), "mwgg_launcher_icons")

_BUILTIN_ATTRIBUTE = "_mwgg_builtin_component"

# True while this module runs its own top-level registrations; flipped to False
# at the end of the module. Components appended while True are the builtin
# ("native") set, known before any world is imported. Everything registered
# later (worlds at import time, runtime code) is non-builtin; which world or
# install source a component came from is the installer/index's business, not
# tracked here.
_INITIALIZING_COMPONENTS = True


class Type(str, Enum):
    TOOL = "TOOL"
    MISC = "MISC"
    CLIENT = "CLIENT"
    ADJUSTER = "ADJUSTER"
    HIDDEN = "HIDDEN"


class Component:
    """
    A Component represents a process launchable by MultiworldGG Launcher, either by a User action in the GUI,
    by resolving an archipelago/mwgg://user:pass@host:port link from the WebHost, by resolving a patch file's metadata,
    or by using a component name arg while running the Launcher in CLI i.e. `MultiworldGGLauncher.exe "Text Client"`

    Expected to be appended to LauncherComponents.component list to be used.
    """
    display_name: str
    """Used as the GUI button label and the component name in the CLI args"""
    description: str
    """Optional description displayed on the GUI underneath the display name"""
    type: Type
    """
    Enum "Type" classification of component intent, for filtering in the Launcher GUI
    If not set in the constructor, it will be inferred by display_name
    """
    script_name: Optional[str]
    """Recommended to use func instead; Name of file to run when the component is called"""
    frozen_name: Optional[str]
    """Recommended to use func instead; Name of the frozen executable file for this component"""
    icon: str  # just the name, no suffix
    """Lookup ID for the icon path in LauncherComponents.icon_paths"""
    cli: bool
    """Bool to control if the component gets launched in an appropriate Terminal for the OS"""
    func: Optional[Callable]
    """
    Function that gets called when the component gets launched
    Any arg besides the component name arg is passed into the func as well, so handling *args is suggested
    """
    file_identifier: Optional[Callable[[str], bool]]
    """
    Function that is run against patch file arg to identify which component is appropriate to launch
    If the function is an Instance of SuffixIdentifier the suffixes will also be valid for the Open Patch component
    """
    game_name: list[str]
    """Game name(s) to identify component when handling launch links from WebHost"""
    supports_uri: Optional[bool]
    """Bool to identify if a component supports being launched by launch links from WebHost"""

    def __init__(self, display_name: str, script_name: Optional[str] = None, frozen_name: Optional[str] = None,
                 cli: bool = False, icon: str = 'icon', component_type: Optional[Type] = None,
                 func: Optional[Callable] = None, file_identifier: Optional[Callable[[str], bool]] = None,
                 game_name: Optional[str | list[str]] = None, supports_uri: Optional[bool] = False,
                 description: str = "") -> None:
        self.display_name = display_name
        self.description = description
        self.script_name = script_name
        self.frozen_name = frozen_name or (apname + script_name) if script_name else None
        self.icon = icon
        self.cli = cli

        self.type = component_type or (
            Type.CLIENT if "Client" in display_name else
            Type.ADJUSTER if "Adjuster" in display_name else Type.MISC)
        self.func = func
        self.file_identifier = file_identifier
        if game_name is None:
            self.game_name = []
        elif isinstance(game_name, str):
            self.game_name = [game_name]
        else:
            self.game_name = game_name
        self.supports_uri = supports_uri

    def handles_file(self, path: str):
        return self.file_identifier(path) if self.file_identifier else False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.display_name})"

def _tag_builtin(component: Component) -> None:
    if getattr(component, _BUILTIN_ATTRIBUTE, None) is None:
        setattr(component, _BUILTIN_ATTRIBUTE, _INITIALIZING_COMPONENTS)


class ComponentList(list[Component]):
    def __init__(self, iterable: Iterable[Component] = ()) -> None:
        # list.__init__ would bypass append, skipping the builtin tagging.
        super().__init__()
        self.extend(iterable)

    def append(self, component: Component) -> None:
        _tag_builtin(component)
        super().append(component)

    def extend(self, components: Iterable[Component]) -> None:
        for component in components:
            self.append(component)

    def insert(self, index: int, component: Component) -> None:
        _tag_builtin(component)
        super().insert(index, component)


processes = weakref.WeakSet()

_rebuild_launcher_ui: Optional[Callable[[], None]] = None


def launch_subprocess(func: Callable, name: str | None = None, args: tuple[str, ...] = ()) -> None:
    import multiprocessing
    process = multiprocessing.Process(target=func, name=name, args=args)
    process.start()
    processes.add(process)


def launch(func: Callable, name: str | None = None, args: tuple[str, ...] = ()) -> None:
    from Utils import is_kivy_running
    if is_kivy_running():
        launch_subprocess(func, name, args)
    else:
        func(*args)


class SuffixIdentifier:
    suffixes: Iterable[str]

    def __init__(self, *args: str):
        self.suffixes = args

    def __call__(self, path: str) -> bool:
        if isinstance(path, str):
            for suffix in self.suffixes:
                if path.endswith(suffix):
                    return True
        return False


def identify(path: Optional[str]) -> Optional[Component]:
    """Return the first registered component whose file_identifier claims `path`.

    Works against whatever is currently registered: builtins only, until worlds
    have been imported."""
    if not path:
        return None
    for component in components:
        if component.handles_file(path):
            return component
    return None


def get_exe(component: Component) -> Optional[list[str]]:
    """Resolve the command line that runs a script/frozen-name component.

    Beta equivalent of upstream Launcher.get_exe: the monorepo has no Launcher
    module, so script components resolve against the frozen bundle root or the
    repo checkout directly."""
    if is_frozen():
        suffix = ".exe" if is_windows else ""
        return [local_path(f"{component.frozen_name}{suffix}")] if component.frozen_name else None
    return [sys.executable, local_path(f"{component.script_name}.py")] if component.script_name else None


def run_component(component: Component, *args: str) -> None:
    """Launch `component`, preferring its func over a script/frozen executable."""
    if component.func:
        component.func(*args)
        return

    if component.script_name:
        exe = get_exe(component)
        if not exe:
            logging.warning(f"Unable to resolve executable for launcher component {component.display_name}.")
            return
        launch_exe([*exe, *args], component.cli)
        return

    logging.warning(f"Component {component.display_name} does not appear to be executable.")


_launch_component = run_component  # deprecated alias


def run_world_tool(module: str, tool_name: str, *args: str) -> None:
    """Install, import, and run a world-declared tool in this process.

    World imports are safe here: only client processes must load worlds in a
    prescribed order (their datapackage depends on it) -- the launcher's
    datapackage is irrelevant, so an explicit, warned tool click may import
    the world directly, the same way MAIN's launcher runs components.
    Discovery (world_manifest_components) stays import-free; world code runs
    only on this user action. MWGG_ROLE is held out of the environment for the
    duration so a tool's child processes cannot inherit the launcher role.

    Raises on failure; GUI callers surface the error."""
    import importlib

    import ModuleUpdate
    ModuleUpdate.install_worlds([f"worlds.{module}"])
    importlib.import_module(f"worlds.{module}")
    component = find_component(tool_name)
    if component is None:
        raise ValueError(f"World '{module}' registers no tool named '{tool_name}'.")
    role = os.environ.pop("MWGG_ROLE", None)
    try:
        run_component(component, *args)
    finally:
        if role is not None:
            os.environ["MWGG_ROLE"] = role


def find_component(name: str) -> Optional[Component]:
    """Case-sensitive lookup by display_name or script_name."""
    for component in components:
        if component.display_name == name or component.script_name == name:
            return component
    return None


def builtin_components() -> list[Component]:
    """Builtin components in registration order: the set registered while this
    module was initializing, known without importing any world."""
    return [component for component in components if getattr(component, _BUILTIN_ATTRIBUTE, False)]


def launch_textclient(*args):
    spawn_client(client_type="text", extra_args=args)


def _install_apworld(path: str = "") -> Optional[pathlib.Path]:
    """Validate and copy an .apworld into custom_worlds/, registering its
    manifest so it's immediately selectable. Returns the installed path, or
    None if the user cancelled the file picker.

    Never imports the world's Python module (only the zip manifest is read,
    via Utils.discover_custom_world_module). A module of the same name already
    imported in this process doesn't matter: clients and component scans run
    in freshly spawned processes, which pick up the new file; the launcher
    only needs a list refresh (see install_apworld)."""
    if not path:
        path = open_filename('Select APWorld file to install', (('APWorld', ('.apworld',)),))
        if not path:
            # user closed menu
            return None

    if not path.endswith(".apworld"):
        raise Exception(f"Wrong file format, looking for .apworld. File identified: {path}")

    apworld_path = pathlib.Path(path)

    import zipfile
    try:
        zip_file = zipfile.ZipFile(apworld_path)
        directories = [f.name for f in zipfile.Path(zip_file).iterdir() if f.is_dir()]
        if len(directories) == 1 and directories[0] in apworld_path.stem:
            module_name = directories[0]
        else:
            raise Exception("APWorld appears to be invalid or damaged. (expected a single directory)")
        zip_file.open(module_name + "/__init__.py")
    except ValueError as e:
        raise Exception("Archive appears invalid or damaged.") from e
    except KeyError as e:
        raise Exception("Archive appears to not be an apworld. (missing __init__.py)") from e

    import ModuleUpdate
    custom_worlds_dir = ModuleUpdate.custom_worlds_dir
    try:
        custom_worlds_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise Exception("Custom Worlds directory appears to not be writable.") from e

    target = custom_worlds_dir / f"{module_name}.apworld"
    if apworld_path.resolve() == target.resolve():
        # Note that this doesn't check if the same world is already installed
        # under a different file; it only catches re-installing the file that's
        # already sitting in custom_worlds/.
        raise Exception(f"APWorld is already installed at {target}.")

    import shutil
    shutil.copyfile(apworld_path, target)

    import Utils
    Utils.discover_custom_world_module(target)

    return target


def install_apworld(path: str = "") -> None:
    import Utils
    try:
        target = _install_apworld(path)
        if target is None:
            logging.info("Aborting APWorld installation.")
            return
    except Exception as e:
        Utils.messagebox("Notice", str(e), error=True)
        logging.exception(e)
    else:
        logging.info(f"Installed APWorld successfully to {target}.")
        Utils.messagebox("Install complete.", f"Installed APWorld to {target}.")
        if _rebuild_launcher_ui and is_kivy_running():
            from kivy.clock import Clock

            def _refresh_after_install(dt):
                _rebuild_launcher_ui()  # type: ignore[misc]

            Clock.schedule_once(_refresh_after_install, 0)


def export_datapackage() -> None:
    import json

    from worlds import network_data_package

    path = user_path("datapackage_export.json")
    with open(path, "w") as f:
        json.dump(network_data_package, f, indent=4)

    open_file(path)


def open_host_yaml() -> None:
    import settings
    s = settings.get_settings()
    file = s.filename
    s.save()
    assert file, "host.yaml missing"
    open_in_text_editor(file)


def open_patch() -> None:
    import Utils
    try:
        filename = open_filename("Select patch", (("Patch", "*"),))
    except Exception as e:
        Utils.messagebox("Error", str(e), error=True)
        return
    if filename:
        spawn_client(launch_file=filename)


def browse_files() -> None:
    open_file(user_path())


components: ComponentList = ComponentList([
    # Launcher
    Component('Launcher', 'Launcher', FROZEN_TARGETS["Launcher"], component_type=Type.HIDDEN),
    # Core
    Component('Host', 'MultiServer', FROZEN_TARGETS["MultiServer"], cli=True,
              file_identifier=SuffixIdentifier('.archipelago', '.mwgg', '.zip'),
              description="Host a generated multiworld on your computer."),
    Component('Generate', 'Generate', FROZEN_TARGETS["Generate"], cli=True,
              description="Generate a multiworld with the YAMLs in the players folder."),
    Component("Install APWorld", func=install_apworld, component_type=Type.TOOL,
              file_identifier=SuffixIdentifier(".apworld"),
              description="Install an APWorld to play games not included with Archipelago by default."),
    Component('Text Client', func=launch_textclient,
              description="Connect to a multiworld using the text client."),
    Component("Export Datapackage", func=export_datapackage, component_type=Type.TOOL,
            description="Write item/location data for installed worlds to a file and open it."),
])

components.extend([
    Component("Open host.yaml", func=open_host_yaml,
              description="Open the host.yaml file to change settings for generation, games, and more."),
    Component("Open Patch", func=open_patch,
              description="Open a patch file, downloaded from the room page or provided by the host."),
    Component("MultiworldGG Website", func=lambda: webbrowser.open("https://multiworld.gg/"),
              description="Open multiworld.gg in your browser."),
    Component("Unofficial AP Discord", icon="discord", func=lambda: webbrowser.open("https://discord.multiworld.gg"),
              description="Join the Discord server to play public multiworlds, report issues, or just chat!"),
    Component("Browse Files", func=browse_files,
              description="Open the MultiworldGG installation folder in your file browser."),
])


# if registering an icon from within an apworld, the format "ap:module.name/path/to/file.png" can be used
icon_paths = {
    'icon': local_path('data', 'icon.png'),
    'mcicon': local_path('data', 'mcicon.png'),
    'discord': local_path('data', 'discord-mark-blue.png'),
}


def _normalize_cached_icon_path(icon_path: str) -> str:
    if icon_path.startswith("ap:"):
        return icon_path
    if os.path.isfile(icon_path):
        return icon_path

    icon_basename = os.path.basename(icon_path)
    if icon_basename:
        candidate_data_path = local_path("data", icon_basename)
        if os.path.isfile(candidate_data_path):
            return candidate_data_path

    return _DEFAULT_ICON_PATH


def resolve_icon_path(icon_path: str) -> str:
    if icon_path.startswith("ap:"):
        return _materialize_ap_icon(icon_path)
    return _normalize_cached_icon_path(icon_path)


def _materialize_ap_icon(icon_path: str) -> str:
    # WARNING: pkgutil.get_data IMPORTS the module. Never resolve an "ap:" icon
    # for custom-world content in the launcher process, which must never run
    # world code -- world-tool cards use the default icon instead.
    module_resource_path = icon_path.removeprefix("ap:")
    module_name, separator, resource_name = module_resource_path.partition("/")
    if not separator or not module_name or not resource_name:
        return _DEFAULT_ICON_PATH

    try:
        resource_data = pkgutil.get_data(module_name, resource_name)
    except Exception:
        resource_data = None
    if not resource_data:
        return _DEFAULT_ICON_PATH

    resource_extension = os.path.splitext(resource_name)[1] or ".png"
    icon_hash = hashlib.sha256(resource_data).hexdigest()
    icon_path_on_disk = os.path.join(_LAUNCHER_ICON_CACHE_DIR, f"{icon_hash}{resource_extension}")
    if os.path.isfile(icon_path_on_disk):
        return icon_path_on_disk

    try:
        os.makedirs(_LAUNCHER_ICON_CACHE_DIR, exist_ok=True)
        with open(icon_path_on_disk, "wb") as icon_file:
            icon_file.write(resource_data)
    except Exception:
        return _DEFAULT_ICON_PATH

    return icon_path_on_disk


@dataclasses.dataclass
class WorldTool:
    """A component declared in a world manifest's `components` list,
    resolved for the launcher without importing the world
    (see world_manifest_components)."""
    module: str
    world_name: str
    name: str
    type: str  # a _MANIFEST_COMPONENT_TYPES member, or "yaml" (see yaml_component)
    description: str = ""


_MANIFEST_COMPONENT_TYPES = ("client", "tool", "adjuster")

YAML_COMPONENT_NAME = "Create YAML"


def yaml_component(module: str, world_name: str = "") -> WorldTool:
    """The YAML-creator entry for a selected game's component strip.

    Synthesized per selection rather than scanned: it belongs to whichever
    game is selected, so worlds that declare nothing still get one. "yaml" is
    deliberately not a _MANIFEST_COMPONENT_TYPES member -- it is the frontend's
    own entry, never something a world may declare. Core owns the shape and
    label so every frontend renders the same entry; mapping the type to a YAML
    editor is the frontend's half."""
    return WorldTool(module=module, world_name=world_name or module,
                     name=YAML_COMPONENT_NAME, type="yaml")


def _coerce_manifest_component(entry: Any, source: str) -> Optional[dict[str, str]]:
    """Validate one manifest `components` entry -- a mirror of the world's
    Component registrations: {"name": <display_name>, "type": client|tool|adjuster},
    plus an optional description. Returns the normalized fields, or None (with
    a warning) for a malformed entry. Unknown keys are ignored."""
    if not isinstance(entry, dict):
        logging.warning(f"{source}: ignoring malformed components entry (expected a mapping): {entry!r}")
        return None
    name = entry.get("name")
    if not isinstance(name, str) or not name:
        logging.warning(f"{source}: ignoring components entry without a name: {entry!r}")
        return None
    component_type = entry.get("type")
    if component_type not in _MANIFEST_COMPONENT_TYPES:
        logging.warning(f"{source}: ignoring components entry {name!r} with unknown type {component_type!r}")
        return None
    description = entry.get("description", "")
    if not isinstance(description, str):
        description = ""
    return {"name": name, "type": component_type, "description": description}


def _manifest_world_tools(manifest: dict, module: str, source: str,
                          include: tuple[str, ...] = ("tool", "adjuster")) -> list[WorldTool]:
    """Build WorldTool entries from one manifest's `components` list, keeping
    only the `include` types."""
    declared = manifest.get("components")
    if not declared:
        return []
    if not isinstance(declared, list):
        logging.warning(f"{source}: manifest \"components\" should be a list, got {type(declared).__name__}")
        return []
    world_name = manifest.get("game") or manifest.get("game_name") or module
    entries: list[WorldTool] = []
    for entry in declared:
        fields = _coerce_manifest_component(entry, source)
        if fields is None or fields["type"] not in include:
            continue
        entries.append(WorldTool(module=module, world_name=world_name, **fields))
    return entries


def world_manifest_components(include: tuple[str, ...] = _MANIFEST_COMPONENT_TYPES) -> list[WorldTool]:
    """Import-free scan of the `components` declared in world manifests, all
    types by default (filter with `include`).

    All data comes from the in-memory GameIndex: build-time index entries plus
    custom_worlds manifests, which Utils.register_custom_worlds folds into the
    index (idempotent, zip-manifest-only; rescanning here picks up newly
    dropped or replaced apworlds, with the custom manifest authoritative for
    its components even on an indexed slug). Index entries count only when
    their dist is actually installed (per-slug importlib.metadata probe --
    never ModuleUpdate.find_world_modules, which shells out to uv); custom
    worlds are present by definition. Never imports world code: the launcher
    must render without running any world's code -- the import happens only in
    a spawned client process or on an explicit, warned tool click
    (run_world_tool)."""
    import importlib.metadata

    from Utils import register_custom_worlds
    from mwgg_igdb import GameIndex

    custom_modules = set(register_custom_worlds())

    entries: list[WorldTool] = []
    for module, game_data in GameIndex.get_all_games().items():
        if not isinstance(game_data, dict) or not game_data.get("components"):
            continue
        if module not in custom_modules:
            try:
                importlib.metadata.distribution(f"worlds.{module}")
            except importlib.metadata.PackageNotFoundError:
                continue
        entries.extend(_manifest_world_tools(game_data, module, f"GameIndex[{module}]", include))

    return entries


def world_tool_entries() -> list[WorldTool]:
    """Back-compat wrapper: tool/adjuster manifest entries only."""
    return world_manifest_components(include=("tool", "adjuster"))


def _validate_manifest_components(manifest: dict, file_name: str) -> None:
    """Warn -- never fail a build -- about `components` entries that don't
    mirror the world's actual registrations: malformed entries, names with no
    matching Component.display_name (find_component is case-sensitive; worlds
    are already imported when Build APWorlds runs), and declared types that
    disagree with the registered component's Type."""
    declared = manifest.get("components")
    if declared is None:
        return
    if not isinstance(declared, list):
        logging.warning(f"{file_name}: manifest \"components\" should be a list, got {type(declared).__name__}")
        return
    for entry in declared:
        fields = _coerce_manifest_component(entry, file_name)
        if fields is None:
            continue
        component = find_component(fields["name"])
        if component is None:
            logging.warning(
                f"{file_name}: components entry {fields['name']!r} does not match any registered "
                "component display_name; its launcher card would fail to run.")
        elif component.type.name.lower() != fields["type"]:
            logging.warning(
                f"{file_name}: components entry {fields['name']!r} declares type {fields['type']!r} "
                f"but the world registers it as {component.type.name.lower()!r}.")


if not is_frozen():
    def _build_apworlds(*launch_args: str):
        import json
        import os
        import zipfile

        from worlds import AutoWorldRegister
        from APContainer import APWorldContainer

        import argparse
        parser = argparse.ArgumentParser(prog="Build APWorlds", description="Build script for APWorlds")
        parser.add_argument("worlds", type=str, default=(), nargs="*", help="names of APWorlds to build")
        parser.add_argument("--skip_open_folder", action="store_true", help="don't open the output build folder")
        args = parser.parse_args(launch_args)

        if args.worlds:
            games = [(game, AutoWorldRegister.world_types.get(game, None)) for game in args.worlds]
        else:
            games = [(worldname, worldtype) for worldname, worldtype in AutoWorldRegister.world_types.items()
                     if not worldtype.zip_path]

        global_apignores = read_apignore(local_path("data", "GLOBAL.apignore"))
        if not global_apignores:
            raise RuntimeError("Could not read global apignore file for build component")

        apworlds_folder = os.path.join("build", "apworlds")
        os.makedirs(apworlds_folder, exist_ok=True)
        for worldname, worldtype in games:
            if not worldtype:
                logging.error(f"Requested APWorld \"{worldname}\" does not exist.")
                continue
            file_name = os.path.split(os.path.dirname(worldtype.__file__))[1]
            world_directory = os.path.join("worlds", file_name)
            if os.path.isfile(os.path.join(world_directory, "archipelago.json")):
                with open(os.path.join(world_directory, "archipelago.json"), mode="r", encoding="utf-8") as manifest_file:
                    manifest = json.load(manifest_file)

                assert "game" in manifest, (
                    f"World directory {world_directory} has an archipelago.json manifest file, but it "
                    "does not define a \"game\"."
                )
                assert manifest["game"] == worldtype.game, (
                    f"World directory {world_directory} has an archipelago.json manifest file, but value of the "
                    f"\"game\" field ({manifest['game']} does not equal the World class's game ({worldtype.game})."
                )
            else:
                manifest = {}

            _validate_manifest_components(manifest, file_name)

            zip_path = os.path.join(apworlds_folder, file_name + ".apworld")
            apworld = APWorldContainer(str(zip_path))
            apworld.game = worldtype.game
            manifest.update(apworld.get_manifest())
            apworld.manifest_path = os.path.join(file_name, "archipelago.json")

            local_ignores = read_apignore(pathlib.Path(world_directory, ".apignore"))
            apignores = global_apignores + local_ignores if local_ignores else global_apignores

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                for file in apignores.match_tree_files(world_directory, negate=True):
                    zf.write(pathlib.Path(world_directory, file), pathlib.Path(file_name, file))

                zf.writestr(apworld.manifest_path, json.dumps(manifest))
        if not args.skip_open_folder:
            open_file(apworlds_folder)

    components.append(Component("Build APWorlds", func=_build_apworlds, cli=True,
                                description="Build APWorlds from loose-file world folders."))


# Builtin registration is complete: anything appended to `components` from here on
# (world modules importing worlds.LauncherComponents at load time, custom-world
# installs, etc.) is not a builtin, so builtin_components() stays trustworthy.
_INITIALIZING_COMPONENTS = False
