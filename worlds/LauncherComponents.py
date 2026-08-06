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
from enum import Enum, auto
from typing import Any, Optional, Callable, Iterable, Tuple

from Utils import local_path, open_filename, is_frozen, is_kivy_running, is_windows, is_linux, is_macos, \
    open_file, user_path, read_apignore, env_cleared_lib_path, FROZEN_TARGETS

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


class Type(Enum):
    TOOL = auto()
    MISC = auto()
    CLIENT = auto()
    ADJUSTER = auto()
    FUNC = auto()  # do not use anymore
    HIDDEN = auto()


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
        if component_type == Type.FUNC:
            from Utils import deprecate
            deprecate(f"Launcher Component {self.display_name} is using Type.FUNC Type, which is pending removal.")
            component_type = Type.MISC

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


def launch_subprocess(func: Callable, name: str | None = None, args: Tuple[str, ...] = ()) -> None:
    import multiprocessing
    process = multiprocessing.Process(target=func, name=name, args=args)
    process.start()
    processes.add(process)


def launch(func: Callable, name: str | None = None, args: Tuple[str, ...] = ()) -> None:
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


def get_client_exe() -> list[str]:
    """Resolve the command line that launches the beta's single client entry point.

    Centralizes exe-name resolution (frozen name vs source script) so callers
    never hardcode "MultiWorldGG(.exe)" themselves."""
    if is_frozen():
        suffix = ".exe" if is_windows else ""
        return [local_path(f"{FROZEN_TARGETS['MultiWorld']}{suffix}")]
    return [sys.executable, local_path("MultiWorld.py")]


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


def spawn_client(game: Optional[str] = None, *, server_address: Optional[str] = None,
                 slot_name: Optional[str] = None, password: Optional[str] = None,
                 client_type: str = "game", launch_file: Optional[str] = None,
                 extra_args: Iterable[str] = ()) -> "subprocess.Popen[Any]":
    """Spawn a client process, detached from this one.

    Every launch from the Launcher process is a separate OS process, and
    children deliberately survive launcher exit: closing the launcher window
    must not kill an in-progress game session. MWGG_NO_SPLASH=1 is set in the
    child env rather than appended as a CLI flag -- MultiWorld.py's arg parser
    doesn't know a --no-splash flag yet, only the env var is read (Phase 2)."""
    argv = list(get_client_exe())
    if launch_file:
        argv.append(launch_file)
    if game is not None:
        argv += ["--game", game]
    if server_address is not None:
        argv += ["--server-address", server_address]
    if slot_name is not None:
        argv += ["--slot-name", slot_name]
    if password is not None:
        argv += ["--password", password]
    argv += ["--client-type", client_type]
    argv += list(extra_args)

    env = os.environ.copy()
    env["MWGG_ROLE"] = "client"
    env["MWGG_CLIENT_TYPE"] = client_type
    env["MWGG_NO_SPLASH"] = "1"

    popen_kwargs: dict[str, Any] = {"env": env}
    if is_windows:
        popen_kwargs["creationflags"] = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        popen_kwargs["start_new_session"] = True

    return subprocess.Popen(argv, **popen_kwargs)


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


def find_component(name: str) -> Optional[Component]:
    """Case-sensitive lookup by display_name or script_name."""
    for component in components:
        if component.display_name == name or component.script_name == name:
            return component
    return None


def builtin_components() -> list[Component]:
    """Builtin components in registration order, excluding anything appended
    after world loading starts (see _classify_component_origin)."""
    return [component for component in components if _component_origin(component) == _COMPONENT_ORIGIN_BUILTIN]


def launch_textclient(*args):
    spawn_client(client_type="text", extra_args=args)


def _install_apworld(path: str = "") -> Optional[pathlib.Path]:
    """Validate and copy an .apworld into custom_worlds/, registering its
    manifest so it's immediately selectable. Returns the installed path, or
    None if the user cancelled the file picker.

    Never imports the world's Python module (only the zip manifest is read,
    via Utils.discover_custom_world_module) -- if a module of the same name is
    already imported in this process, installation still succeeds but a
    restart is required to actually use the new code, since Python caches
    imported modules and this beta has no world-unload mechanism."""
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

    # If a module with this name is already imported, we can't hot-swap it in:
    # Python caches imported modules and this beta has no unload mechanism.
    already_loaded = f"worlds.{module_name}" in sys.modules

    import shutil
    shutil.copyfile(apworld_path, target)

    import Utils
    Utils.discover_custom_world_module(target)

    if already_loaded and is_kivy_running():
        raise Exception(f"Installed APWorld successfully, but '{module_name}' is already loaded, "
                        "so a Launcher restart is required to use the new installation.")

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
    from shutil import which
    if is_linux:
        exe = which('sensible-editor') or which('gedit') or \
              which('xdg-open') or which('gnome-open') or which('kde-open')
    elif is_macos:
        exe = which("open")
    else:
        webbrowser.open(file)
        return

    env = env_cleared_lib_path()
    subprocess.Popen([exe, file], env=env)


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

for component in components:
    setattr(component, _COMPONENT_ORIGIN_ATTRIBUTE, _COMPONENT_ORIGIN_BUILTIN)

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


# Builtin registration is complete: anything appended to `components` from here on
# (world modules importing worlds.LauncherComponents at load time, custom-world
# installs, etc.) is not a builtin, so builtin_components() stays trustworthy.
_INITIALIZING_COMPONENTS = False
