import bisect
import hashlib
import json
import logging
import os
import pathlib
import pkgutil
import subprocess
import sys
import tempfile
import time
import weakref
from enum import Enum
from typing import Any, Optional, Callable, Iterable, Tuple

from Utils import local_path, open_filename, is_frozen, is_kivy_running, is_windows, open_file, user_path, \
    read_apignore

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

_DEFAULT_ICON_PATH = local_path("data", "icon.png")
_LAUNCHER_ICON_CACHE_DIR = os.path.join(tempfile.gettempdir(), "mwgg_launcher_icons")

_COMPONENT_ORIGIN_ATTRIBUTE = "_mwgg_component_origin"
_COMPONENT_ORIGIN_BUILTIN = "builtin"
_COMPONENT_ORIGIN_WORLD = "world"
_COMPONENT_ORIGIN_OTHER = "other"
_COMPONENT_ORIGIN_CACHE = "cache_stub"

_INITIALIZING_COMPONENTS = True


class APWorldInstallRestartRequired(Exception):
    def __init__(self, module_name: str) -> None:
        self.module_name = module_name
        super().__init__(
            f"Installed APWorld successfully, but '{module_name}' is already loaded, "
            "so a Launcher restart is required to use the new installation."
        )


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

def _is_worlds_loading() -> bool:
    worlds_module = sys.modules.get("worlds")
    return bool(getattr(worlds_module, "_worlds_loading", False))


def _classify_component_origin() -> str:
    if _is_worlds_loading():
        return _COMPONENT_ORIGIN_WORLD
    if _INITIALIZING_COMPONENTS:
        return _COMPONENT_ORIGIN_BUILTIN
    return _COMPONENT_ORIGIN_OTHER


def _component_origin(component: Component) -> str:
    origin = getattr(component, _COMPONENT_ORIGIN_ATTRIBUTE, None)
    return origin if isinstance(origin, str) else _COMPONENT_ORIGIN_OTHER


def _tag_component(component: Component) -> None:
    origin = getattr(component, _COMPONENT_ORIGIN_ATTRIBUTE, None)
    if not isinstance(origin, str):
        origin = _classify_component_origin()
    setattr(component, _COMPONENT_ORIGIN_ATTRIBUTE, origin)


class ComponentList(list[Component]):
    def append(self, component: Component) -> None:
        _tag_component(component)
        super().append(component)

    def extend(self, components: Iterable[Component]) -> None:
        for component in components:
            self.append(component)

    def insert(self, index: int, component: Component) -> None:
        _tag_component(component)
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

    Works against whatever is currently registered: with worlds unloaded that is
    the builtin components plus any launcher-cache stubs (their suffixes are
    serialized, so suffix lookups need no world import)."""
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


def launch_exe(exe: Iterable[str], in_terminal: bool = False) -> bool:
    """Run the command line `exe` in a new process. With `in_terminal`, try to
    run it in a terminal window; the return value reports whether one was used.
    Beta equivalent of upstream Launcher.launch (which the monorepo lacks)."""
    exe = list(exe)
    if in_terminal:
        if is_windows:
            # intentionally using a window title with a space so it gets quoted and treated as a title
            subprocess.Popen(["start", f"Running {apname}", *exe], shell=True)
            return True
        elif sys.platform.startswith("linux"):
            from shutil import which
            xdg = which("xdg-terminal-exec")
            if xdg:
                subprocess.Popen([xdg, "--", *exe])
                return True
            terminal = which("x-terminal-emulator") or which("konsole") or which("gnome-terminal") or which("xterm")
            if terminal:
                import shlex
                subprocess.Popen([terminal, "-e", shlex.join(exe)])
                return True
        elif sys.platform == "darwin":
            from shutil import which
            subprocess.Popen([which("open"), "-W", "-a", "Terminal.app", *exe])
            return True
    subprocess.Popen(exe)
    return False


def launch_textclient(*args):
    import CommonClient
    launch(CommonClient.run_as_textclient, name="TextClient", args=args)


# def _install_apworld(apworld_src: str = "") -> Optional[Tuple[pathlib.Path, pathlib.Path]]:
#     if not apworld_src:
#         apworld_src = open_filename('Select APWorld file to install', (('APWorld', ('.apworld',)),))
#         if not apworld_src:
#             # user closed menu
#             return

#     if not apworld_src.endswith(".apworld"):
#         raise Exception(f"Wrong file format, looking for .apworld. File identified: {apworld_src}")

#     apworld_path = pathlib.Path(apworld_src)

#     try:
#         import zipfile
#         zip = zipfile.ZipFile(apworld_path)
#         directories = [f.name for f in zipfile.Path(zip).iterdir() if f.is_dir()]
#         if len(directories) == 1 and directories[0] in apworld_path.stem:
#             module_name = directories[0]
#             apworld_name = module_name + ".apworld"
#         else:
#             raise Exception("APWorld appears to be invalid or damaged. (expected a single directory)")
#         zip.open(module_name + "/__init__.py")
#     except ValueError as e:
#         raise Exception("Archive appears invalid or damaged.") from e
#     except KeyError as e:
#         raise Exception("Archive appears to not be an apworld. (missing __init__.py)") from e

#     import worlds
#     if worlds.user_folder is None:
#         raise Exception("Custom Worlds directory appears to not be writable.")
#     for world_source in worlds.world_sources:
#         if apworld_path.samefile(world_source.resolved_path):
#             # Note that this doesn't check if the same world is already installed.
#             # It only checks if the user is trying to install the apworld file
#             # that comes from the installation location (worlds or custom_worlds)
#             raise Exception(f"APWorld is already installed at {world_source.resolved_path}.")

#     # TODO: run generic test suite over the apworld.
#     # TODO: have some kind of version system to tell from metadata if the apworld should be compatible.

# #     target = pathlib.Path(worlds.user_folder) / apworld_name
# #     import shutil
# #     shutil.copyfile(apworld_path, target)

#     # If a module with this name is already loaded, then we can't load it now.
#     # TODO: We need to be able to unload a world module,
#     # so the user can update a world without restarting the application.
#     found_already_loaded = False
#     for loaded_world in worlds.world_sources:
#         loaded_name = pathlib.Path(loaded_world.path).stem
#         if module_name == loaded_name:
#             found_already_loaded = True
#             break
#     if found_already_loaded and is_kivy_running():
#         raise Exception(f"Installed APWorld successfully, but '{module_name}' is already loaded, "
#                         "so a Launcher restart is required to use the new installation.")
#     world_source = worlds.WorldSource(str(target), is_zip=True, relative=False)
#     bisect.insort(worlds.world_sources, world_source)
#     world_source.load()

# #     return apworld_path, target


# def install_apworld(apworld_path: str = "") -> None:
#     try:
#         res = _install_apworld(apworld_path)
#         if res is None:
#             logging.info("Aborting APWorld installation.")
#             return
#         source, target = res
#     except Exception as e:
#         import Utils
#         Utils.messagebox("Notice", str(e), error=True)
#         logging.exception(e)
#     else:
#         import Utils
#         logging.info(f"Installed APWorld successfully, copied {source} to {target}.")
#         Utils.messagebox("Install complete.", f"Installed APWorld from {source}.")
        # if _rebuild_launcher_ui and is_kivy_running():
        #     from kivy.clock import Clock
        #     def _refresh_after_install(dt):
        #         _hydrate_launcher_components_from_cache()
        #         _rebuild_launcher_ui()  # type: ignore[misc]
        #     Clock.schedule_once(_refresh_after_install, 0)


def export_datapackage() -> None:
    import json

    from worlds import network_data_package

    path = user_path("datapackage_export.json")
    with open(path, "w") as f:
        json.dump(network_data_package, f, indent=4)

    open_file(path)

components: ComponentList = ComponentList([
    # Launcher
    Component('Launcher', 'Launcher', component_type=Type.HIDDEN),
    # Core
    Component('Host', 'MultiServer', f'{apname}Server', cli=True,
              file_identifier=SuffixIdentifier('.archipelago', '.mwgg', '.zip'),
              description="Host a generated multiworld on your computer."),
    Component('Generate', 'Generate', cli=True,
              description="Generate a multiworld with the YAMLs in the players folder."),
    # Component("Install APWorld", func=install_apworld, file_identifier=SuffixIdentifier(".apworld"),
            #   description="Install an APWorld to play games not included with Archipelago by default."),
    Component('Text Client', 'CommonClient', f'{apname}TextClient', func=launch_textclient,
              description="Connect to a multiworld using the text client."),
    Component("Export Datapackage", func=export_datapackage, component_type=Type.TOOL,
            description="Write item/location data for installed worlds to a file and open it."),
])

for component in components:
    setattr(component, _COMPONENT_ORIGIN_ATTRIBUTE, _COMPONENT_ORIGIN_BUILTIN)


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


def has_world_components() -> bool:
    return any(
        _component_origin(component) in {_COMPONENT_ORIGIN_WORLD, _COMPONENT_ORIGIN_CACHE}
        for component in components
    )


if not is_frozen():
    def _build_apworlds(*launch_args: str):
        import json
        import os
        import zipfile

        from worlds import AutoWorldRegister
        from APContainer import APWorldContainer
        from FileUtils import FileUtilsSingleton

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
        FileUtilsSingleton().open_directory(apworlds_folder)

    components.append(Component("Build APWorlds", func=_build_apworlds, cli=True,
                                description="Build APWorlds from loose-file world folders."))
