from __future__ import annotations

import collections
import copy
import logging
import asyncio
import urllib.parse
import sys
import typing
import time
import functools

import websockets

import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"

from MultiServer import CommandProcessor, mark_raw
from Utils import gui_enabled, Version, stream_input, async_start
from worlds import network_data_package, AutoWorldRegister
from NetUtils import (Endpoint, ClientStatus, encode, decode, NetworkItem, NetworkPlayer, NetworkSlot, 
                      Permission, SlotType, LocationStore, Hint, HintStatus, MWGGUIHintStatus,JSONtoTextParser,
                      RawJSONtoTextParser, add_json_text, add_json_location, add_json_item, JSONTypes, TEXT_COLORS)
from ClientState import ClientState
from ClientBuilder import GameClient
from multiprocessing import Queue

# GUI-only dialog components are imported lazily at their call sites so
# importing CommonClient does not drag the full Kivy stack into the TUI process.

from Utils import Version, stream_input, async_start, init_logging
import os
import ssl

if typing.TYPE_CHECKING:
    import argparse
    from frontend_protocol import FrontendProtocol
    from typing import Optional

logger = logging.getLogger("Client")


_pending_launch_callbacks: "typing.Optional[typing.Dict[str, typing.Callable[[], None]]]" = None


def _set_pending_launch_callbacks(ready_callback: "typing.Optional[typing.Callable[[], None]]",
                                  error_callback: "typing.Optional[typing.Callable[[], None]]") -> None:
    """Stash the launcher-provided callbacks so the next CommonContext that is built picks them up.

    Called by Utils._perform_module_launch immediately before invoking the world's
    launch function. World clients don't need to forward these kwargs themselves.
    """
    global _pending_launch_callbacks
    _pending_launch_callbacks = {
        "ready_callback": ready_callback,
        "error_callback": error_callback,
    }


def _consume_pending_launch_callbacks() -> "typing.Tuple[typing.Optional[typing.Callable[[], None]], typing.Optional[typing.Callable[[], None]]]":
    """Pop the pending callbacks. After consume, the dict is cleared so a second
    context construction in the same flow won't re-bind the same closures."""
    global _pending_launch_callbacks
    pending = _pending_launch_callbacks
    _pending_launch_callbacks = None
    if pending is None:
        return None, None
    return pending.get("ready_callback"), pending.get("error_callback")


def _make_one_shot(callback: "typing.Optional[typing.Callable[[], None]]") -> "typing.Callable[[], None]":
    """Wrap a callback so it fires at most once. Subsequent calls are no-ops.

    A no-op stub is returned when the underlying callback is None, so callers
    can invoke it unconditionally without None-checks.
    """
    state = {"fired": False, "fn": callback}

    def _invoke() -> None:
        if state["fired"]:
            return
        state["fired"] = True
        fn = state["fn"]
        state["fn"] = None
        if fn is None:
            return
        try:
            fn()
        except Exception as exc:
            logger.error(f"Error in client launch callback: {exc}")

    return _invoke


@Utils.cache_argsless
def get_ssl_context():
    import certifi
    return ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certifi.where())

def set_local_network_data_package() -> typing.Tuple[typing.Dict[str, typing.Any], typing.Dict[str, typing.Any]]:
    from worlds import DataPackage, AutoWorldRegister
    local_network_data_package: DataPackage = {
        "games": {world_name: world.get_data_package_data() for world_name, world in AutoWorldRegister.world_types.items()},
    }
    local_network_data_package_single_game: typing.Dict[str, DataPackage] = {
        game_name: {"games": {game_name: pkg_data}}
        for game_name, pkg_data in local_network_data_package["games"].items()
    }
    return local_network_data_package, local_network_data_package_single_game

class ClientCommandProcessor(CommandProcessor):
    """
    The Command Processor will parse every method of the class that starts with "_cmd_" as a command to be called
    when parsing user input, i.e. _cmd_exit will be called when the user sends the command "/exit".

    The decorator @mark_raw can be imported from MultiServer and tells the parser to only split on the first
    space after the command i.e. "/exit one two three" will be passed in as method("one two three") with mark_raw
    and method("one", "two", "three") without.

    In addition all docstrings for command methods will be displayed to the user on launch and when using "/help"
    """
    def __init__(self, ctx: CommonContext):
        self.ctx = ctx

    def output(self, text: str):
        """Helper function to abstract logging to the CommonClient UI"""
        logger.info(text)

    def _cmd_exit(self) -> bool:
        """Close connections and client"""
        if self.ctx.ui:
            self.ctx.ui.stop()
        self.ctx.exit_event.set()
        return True

    def _cmd_connect(self, address: str = "") -> bool:
        """Connect to a Multiworld Server.  Example format: PlayerName:password@multiworld.gg:38281"""
        if address:
            self.ctx.server_address = None
        elif not self.ctx.server_address:
            self.output("Please specify an address.  Example format: PlayerName:password@multiworld.gg:38281")
            return False
        async_start(self.ctx.connect(address if address else None), name="connecting")
        return True

    def _cmd_disconnect(self) -> bool:
        """Disconnect from a MultiWorld Server"""
        async_start(self.ctx.disconnect(), name="disconnecting")
        return True

    def _cmd_received(self) -> bool:
        """List all of your received items"""
        item: NetworkItem
        self.output(f'{len(self.ctx.items_received)} received items, sorted by time:')
        for index, item in enumerate(self.ctx.items_received, 1):
            parts = []
            add_json_item(parts, item.item, self.ctx.slot, item.flags)
            add_json_text(parts, " from ")
            add_json_location(parts, item.location, item.player)
            add_json_text(parts, " by ")
            add_json_text(parts, item.player, type=JSONTypes.player_id)
            self.ctx.on_print_json({"data": parts, "cmd": "PrintJSON"})
        return True

    def _cmd_missing(self, filter_text = "") -> bool:
        """List all missing location checks, from your local game state.
        Can be given text, which will be used as a filter."""
        if not self.ctx.game:
            self.output("No game set, cannot determine missing checks.")
            return False
        count = 0
        checked_count = 0

        lookup = self.ctx.location_names[self.ctx.game]
        for location_id, location in lookup.items():
            if filter_text and filter_text not in location:
                continue
            if location_id < 0:
                continue
            if location_id not in self.ctx.locations_checked:
                if location_id in self.ctx.missing_locations:
                    self.output('Missing: ' + location)
                    count += 1
                elif location_id in self.ctx.checked_locations:
                    self.output('Checked: ' + location)
                    count += 1
                    checked_count += 1

        if count:
            self.output(
                f"Found {count} missing location checks{f'. {checked_count} location checks previously visited.' if checked_count else ''}")
        else:
            self.output("No missing location checks found.")
        return True

    def output_datapackage_part(self, name: typing.Literal["Item Names", "Location Names"]) -> bool:
        """
        Helper to digest a specific section of this game's datapackage.

        :param name: Printed to the user as context for the part.

        :return: Whether the process was successful.
        """
        if not self.ctx.game:
            self.output(f"No game set, cannot determine {name}.")
            return False

        lookup = self.ctx.item_names if name == "Item Names" else self.ctx.location_names
        lookup = lookup[self.ctx.game]
        self.output(f"{name} for {self.ctx.game}")
        for name in lookup.values():
            self.output(name)
        return True

    def _cmd_items(self) -> bool:
        """List all item names for the currently running game."""
        return self.output_datapackage_part("Item Names")

    def _cmd_locations(self) -> bool:
        """List all location names for the currently running game."""
        return self.output_datapackage_part("Location Names")

    def output_group_part(self, group_key: typing.Literal["item_name_groups", "location_name_groups"],
                          filter_key: str,
                          name: str) -> bool:
        """
        Logs an item or location group from the player's game's datapackage.

        :param group_key: Either Item or Location group to be processed.
        :param filter_key: Which group key to filter to. If an empty string is passed will log all item/location groups.
        :param name: Printed to the user as context for the part.

        :return: Whether the process was successful.
        """
        if not self.ctx.game:
            self.output(f"No game set, cannot determine existing {name} Groups.")
            return False
        lookup = Utils.persistent_load().get("groups_by_checksum", {}).get(self.ctx.checksums[self.ctx.game], {})\
            .get(self.ctx.game, {}).get(group_key, {})
        if lookup is None:
            self.output("datapackage not yet loaded, try again")
            return False

        if filter_key:
            if filter_key not in lookup:
                self.output(f"Unknown {name} Group {filter_key}")
                return False

            self.output(f"{name}s for {name} Group \"{filter_key}\"")
            for entry in lookup[filter_key]:
                self.output(entry)
        else:
            self.output(f"{name} Groups for {self.ctx.game}")
            for group in lookup:
                self.output(group)
        return True

    @mark_raw
    def _cmd_item_groups(self, key: str = "") -> bool:
        """
        List all item group names for the currently running game.

        :param key: Which item group to filter to. Will log all groups if empty.
        """
        return self.output_group_part("item_name_groups", key, "Item")

    @mark_raw
    def _cmd_location_groups(self, key: str = "") -> bool:
        """
        List all location group names for the currently running game.

        :param key: Which item group to filter to. Will log all groups if empty.
        """
        return self.output_group_part("location_name_groups", key, "Location")

    def _cmd_ready(self) -> bool:
        """Send ready status to server."""
        self.ctx.ready = not self.ctx.ready
        if self.ctx.ready:
            state = ClientStatus.CLIENT_READY
            self.output("Readied up.")
        else:
            state = ClientStatus.CLIENT_CONNECTED
            self.output("Unreadied.")
        async_start(self.ctx.send_msgs([{"cmd": "StatusUpdate", "status": state}]), name="send StatusUpdate")
        return True

    def default(self, raw: str):
        """The default message parser to be used when parsing any messages that do not match a command"""
        raw = self.ctx.on_user_say(raw)
        if raw:
            async_start(self.ctx.send_msgs([{"cmd": "Say", "text": raw}]), name="send Say")


class InitContext:
    """Base context for initial GUI state with minimal properties"""
    # properties
    _username: str | None = None
    _password: str | None = None
    server_address: str | None
    """Autoconnect address provided by the ctx constructor
    expected format: url://username:password@hostname:port"""

    command_processor: typing.Type[CommandProcessor] = ClientCommandProcessor
    all_players_chat: bool = True
    """If False only your own server chatter (items, locations, hints) will be shown in the console."""
    # internals
    _messagebox: typing.Optional["MessageBox"] = None
    """Current message box through Gui"""
    _messagebox_connection_loss: typing.Optional["MessageBox"] = None
    """Message box reporting a loss of connection"""
    _consolebox: typing.Optional["ConsoleBox"] = None
    """Launcher window "console" box"""
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.exit_event = asyncio.Event()
        self.takeover_complete = asyncio.Event()
        self.server_address = None
        self.all_players_chat = True
        self._state = ClientState.INITIAL
        self._is_transitioning = False
        self._splash_queue: Optional[Queue] = None

    def _set_server_address(self, server_address: str) -> str:
        prefix = "ws://" if "://" not in server_address else urllib.parse.urlparse(server_address).scheme
        server_address = f"{prefix}{server_address}"
        username = urllib.parse.urlparse(server_address).username or ""
        password = urllib.parse.urlparse(server_address).password or ""
        server_hostname = urllib.parse.urlparse(server_address).hostname or self.hostname
        server_port = urllib.parse.urlparse(server_address).port or self.port
        if username:
            self.username = username
            if password:
                self.password = password
                return f"{prefix}{self.username}:{self.password}@{server_hostname}:{server_port}"
            return f"{prefix}{self.username}:@{server_hostname}:{server_port}"
        return f"{prefix}{server_hostname}:{server_port}"

    def _set_saved_properties(self):
        '''Set the server address from the saved properties
        username:password@hostname:port format
        No password is saved, using an empty string'''
        last_username = Utils.persistent_load().get('client', {}).get('last_username', "")
        last_server_hostname = Utils.persistent_load().get('client', {}).get('last_server_hostname', "multiworld.gg")
        last_server_port = str(Utils.persistent_load().get('client', {}).get('last_server_port', 38281))
        netloc = lambda: f"{last_username}@{last_server_hostname}:{last_server_port}" if last_username else f"{last_server_hostname}:{last_server_port}"
        self.server_address = f"ws://{netloc()}" if netloc() else None

    def make_gui(self) -> "type[FrontendProtocol]":
        """Return the frontend `App` class selected by `MWGG_FRONTEND` (gui/tui).

        Mirrored on `CommonContext` so launcher-stage InitContext and game-stage
        CommonContext share a dispatch path.
        """
        from frontend_protocol import resolve_frontend_class
        return resolve_frontend_class()

    def run_gui(self, splash_queue: Optional[Queue] = None):
        """Run the GUI as self.ui_task."""
        if splash_queue:
            self._splash_queue = splash_queue
        self._set_saved_properties()
        self.ui = self.make_gui()(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def shutdown(self):
        if self.ui_task:
            await self.ui_task

    @property
    def username(self) -> str:
        if self._username:
            return self._username
        elif hasattr(self, 'server_address'):
            self._username = urllib.parse.urlparse(self.server_address).username or None
            if self._username:
                return self._username
        self._username = Utils.persistent_load().get('client', {}).get('last_username', '')
        return self._username
    
    @username.setter
    def username(self, value: str|bytes):
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        self._username = value
        Utils.persistent_store('client', 'last_username', value)

    @property
    def password(self) -> str:
        if self._password:
            return self._password
        elif hasattr(self, 'server_address'):
            self._password = urllib.parse.urlparse(self.server_address).password or ""
            return self._password
        else:
            self._password = ""
            return self._password
    
    @password.setter
    def password(self, value: str):
        self._password = value

    @property
    def hostname(self) -> str:
        if hasattr(self, 'server_address'):
            hostname = urllib.parse.urlparse(self.server_address).hostname or None
            if hostname:
                return hostname
        hostname = Utils.persistent_load().get('client', {}).get('last_server_hostname', 'multiworld.gg')
        return hostname

    @property
    def port(self) -> str:
        if hasattr(self, 'server_address'):
            port = urllib.parse.urlparse(self.server_address).port or None
            if port:
                return str(port)
        port = str(Utils.persistent_load().get('client', {}).get('last_server_port', 38281))
        return port

class CommonContext(InitContext):
    # The following attributes are used to Connect and should be adjusted as needed in subclasses
    tags: typing.Set[str] = {"AP"}
    game: typing.Optional[str] = None
    items_handling: typing.Optional[int] = None
    want_slot_data: bool = True  # should slot_data be retrieved via Connect

    class NameLookupDict:
        """A specialized dict, with helper methods, for id -> name item/location data package lookups by game."""
        def __init__(self, ctx: CommonContext, lookup_type: typing.Literal["item", "location"]):
            self.ctx: CommonContext = ctx
            self.lookup_type: typing.Literal["item", "location"] = lookup_type
            self._unknown_item: typing.Callable[[int], str] = lambda key: f"Unknown {lookup_type} (ID: {key})"
            self._archipelago_lookup: typing.Dict[int, str] = {}
            self._game_store: typing.Dict[str, typing.ChainMap[int, str]] = collections.defaultdict(
                lambda: collections.ChainMap(self._archipelago_lookup, Utils.KeyedDefaultDict(self._unknown_item)))

        # noinspection PyTypeChecker
        def __getitem__(self, key: str) -> typing.Mapping[int, str]:
            assert isinstance(key, str), f"ctx.{self.lookup_type}_names used with an id, use the lookup_in_ helpers instead"
            return self._game_store[key]

        def __len__(self) -> int:
            return len(self._game_store)

        def __iter__(self) -> typing.Iterator[str]:
            return iter(self._game_store)

        def __repr__(self) -> str:
            return repr(self._game_store)

        def lookup_in_game(self, code: int, game_name: typing.Optional[str] = None) -> str:
            """Returns the name for an item/location id in the context of a specific game or own game if `game` is
            omitted.
            """
            if game_name is None:
                game_name = self.ctx.game
                assert game_name is not None, f"Attempted to lookup {self.lookup_type} with no game name available."

            return self._game_store[game_name][code]

        def lookup_in_slot(self, code: int, slot: typing.Optional[int] = None) -> str:
            """Returns the name for an item/location id in the context of a specific slot or own slot if `slot` is
            omitted.

            Use of `lookup_in_slot` should not be used when not connected to a server. If looking in own game, set
            `ctx.game` and use `lookup_in_game` method instead.
            """
            if slot is None:
                slot = self.ctx.slot
                assert slot is not None, f"Attempted to lookup {self.lookup_type} with no slot info available."

            return self.lookup_in_game(code, self.ctx.slot_info[slot].game)

        def update_game(self, game: str, name_to_id_lookup_table: typing.Dict[str, int]) -> None:
            """Overrides existing lookup tables for a particular game."""
            id_to_name_lookup_table = Utils.KeyedDefaultDict(self._unknown_item)
            id_to_name_lookup_table.update({code: name for name, code in name_to_id_lookup_table.items()})
            self._game_store[game] = collections.ChainMap(self._archipelago_lookup, id_to_name_lookup_table)
            if game == "Archipelago":
                # Keep track of the Archipelago data package separately so if it gets updated in a custom datapackage,
                # it updates in all chain maps automatically.
                self._archipelago_lookup.clear()
                self._archipelago_lookup.update(id_to_name_lookup_table)

    # defaults
    starting_reconnect_delay: int = 5
    current_reconnect_delay: int = starting_reconnect_delay
    command_processor: typing.Type[CommandProcessor] = ClientCommandProcessor
    ui: typing.Optional["FrontendProtocol"] = None
    ui_task: typing.Optional["asyncio.Task[None]"] = None
    input_task: typing.Optional["asyncio.Task[None]"] = None
    keep_alive_task: typing.Optional["asyncio.Task[None]"] = None
    server_task: typing.Optional["asyncio.Task[None]"] = None
    autoreconnect_task: typing.Optional["asyncio.Task[None]"] = None
    disconnected_intentionally: bool = False
    server: typing.Optional[Endpoint] = None
    server_version: Version = Version(0, 0, 0)
    generator_version: Version = Version(0, 0, 0)
    current_energy_link_value: typing.Optional[int] = None  # to display in UI, gets set by server
    max_size: int = 16*1024*1024  # 16 MB of max incoming packet size

    last_death_link: float = time.time()  # last send/received death link on AP layer

    # remaining type info
    slot_info: dict[int, NetworkSlot]
    """Slot Info from the server for the current connection"""
    # server_address: str | None
    # """Autoconnect address provided by the ctx constructor"""
    # password: str | None
    # """Password used for Connecting, expected by server_auth"""
    hint_cost: int | None
    """Current Hint Cost per Hint from the server"""
    hint_points: int | None
    """Current available Hint Points from the server"""
    player_names: dict[int, str]
    """Current lookup of slot number to player display name from server (includes aliases)"""

    finished_game: bool
    """
    Bool to signal that status should be updated to Goal after reconnecting
    to be used to ensure that a StatusUpdate packet does not get lost when disconnected
    """
    ready: bool
    """Bool to keep track of state for the /ready command"""
    team: int | None
    """Team number of currently connected slot"""
    slot: int | None
    """Slot number of currently connected slot"""
    auth: str | None
    """Name used in Connect packet"""
    seed_name: str | None
    """Seed name that will be validated on opening a socket if present"""
    timer: float
    """Start time based on first location checked"""
    admin: bool
    """Bool to keep track of admin login state"""

    # locations
    locations_checked: set[int]
    """
    Local container of location ids checked to signal that LocationChecks should be resent after reconnecting
    to be used to ensure that a LocationChecks packet does not get lost when disconnected
    """
    locations_scouted: set[int]
    """
    Local container of location ids scouted to signal that LocationScouts should be resent after reconnecting
    to be used to ensure that a LocationScouts packet does not get lost when disconnected
    """
    items_received: list[NetworkItem]
    """List of NetworkItems recieved from the server"""
    missing_locations: set[int]
    """Container of Locations that are unchecked per server state"""
    checked_locations: set[int]
    """Container of Locations that are checked per server state"""
    server_locations: set[int]
    """Container of Locations that exist per server state; a combination between missing and checked locations"""
    locations_info: dict[int, NetworkItem]
    """Dict of location id: NetworkItem info from LocationScouts request"""

    # data storage
    stored_data: dict[str, typing.Any]
    """
    Data Storage values by key that were retrieved from the server
    any keys subscribed to with SetNotify will be kept up to date
    """
    stored_data_notification_keys: set[str]
    """Current container of watched Data Storage keys, managed by ctx.set_notify"""

    # internals
    _last_activity_time: float | None
    """Time of last activity, used to track elapsed time"""
    _shared_activity_time: float | None
    """Time of all players' last activity, used to track elapsed time"""
    _messagebox: typing.Optional["MessageBox"] = None
    """Current message box through Gui"""
    _messagebox_connection_loss: typing.Optional["MessageBox"] = None
    """Message box reporting a loss of connection"""
    _consolebox: typing.Optional["ConsoleBox"] = None
    """Current console error box through Gui"""

    def __init__(self, server_address: typing.Optional[str] = None, password: typing.Optional[str] = None) -> None:
        super().__init__()  # Initialize InitContext
        self._current_client: Optional[GameClient] = None
        self._state = ClientState.INITIAL
        self._is_transitioning = False
        self._initial_ctx: dict["FrontendProtocol", asyncio.Task] = {}
        self._main_task: Optional[asyncio.Task] = None
        self._shared_activity_time = None
        self._last_activity_time = None
        # server state
        if server_address:
            self.server_address = self._set_server_address(server_address)
        self.hint_cost = None
        self.slot_info = {}
        self.permissions = {
            "release": "disabled",
            "collect": "disabled",
            "remaining": "disabled",
        }

        # own state
        self.finished_game = False
        self.ready = False
        self.team = None
        self.slot = None
        self.auth = None
        self.seed_name = None
        self.timer = 0.0
        self.admin = False
        self.locations_checked = set()  # local state
        self.locations_scouted = set()
        self.items_received = []
        self.missing_locations = set()  # server state
        self.checked_locations = set()  # server state
        self.server_locations = set()  # all locations the server knows of, missing_location | checked_locations
        self.locations_info = {}

        self.stored_data = {}
        self.stored_data_notification_keys = set()

        self.input_queue = asyncio.Queue()
        self.input_requests = 0

        # game state
        self.player_names = {0: "Archipelago"}
        self.exit_event = asyncio.Event()
        self.watcher_event = asyncio.Event()

        self.item_names = self.NameLookupDict(self, "item")
        self.location_names = self.NameLookupDict(self, "location")
        self.checksums = {}

        self.jsontotextparser = JSONtoTextParser(self)
        self.rawjsontotextparser = RawJSONtoTextParser(self)

        # Launcher-provided callbacks, stashed by Utils._perform_module_launch.
        # One-shot wrappers so the same callback can't fire twice across the
        # takeover-completion path, the kvui async_run failure path, and the
        # outer Utils._perform_module_launch exception handler.
        ready_cb, error_cb = _consume_pending_launch_callbacks()
        self._ready_callback = _make_one_shot(ready_cb)
        self._error_callback = _make_one_shot(error_cb)

        # execution
        self.keep_alive_task = asyncio.create_task(keep_alive(self), name="Bouncy")

    def _can_takeover_existing_ui(self) -> bool:
        """Check if an existing frontend UI (Kivy GUI or Textual TUI) can be taken over.

        Both frontends register their running instance on `cls._active_instance` in
        __init__ and clear it in on_stop/on_unmount. We inspect whichever class
        `MWGG_FRONTEND` selected.
        """
        try:
            from frontend_protocol import resolve_frontend_class
            cls = resolve_frontend_class()
            app = getattr(cls, "_active_instance", None)
            return (app is not None and
                    hasattr(app, 'ctx') and
                    isinstance(app.ctx, InitContext) and
                    app.ctx._state == ClientState.INITIAL and
                    not app.ctx._is_transitioning)
        except Exception:
            return False

    async def _takeover_existing_ui(self) -> None:
        """Take over existing frontend UI instance (Kivy GUI or Textual TUI)"""
        # Import locally to avoid circular import
        from ClientBuilder import GameClient
        from frontend_protocol import resolve_frontend_class

        app = getattr(resolve_frontend_class(), "_active_instance", None)
        existing_ctx = app.ctx

        # Mark transition state
        existing_ctx._is_transitioning = True
        self._is_transitioning = True

        try:
            # Preserve exit_event from existing context
            self.exit_event = existing_ctx.exit_event

            # Preserve UI references from existing context
            if hasattr(existing_ctx, 'ui'):
                self.ui = existing_ctx.ui
            if hasattr(existing_ctx, 'ui_task'):
                self.ui_task = existing_ctx.ui_task

            # Create game client builder with existing context
            game_client = GameClient(self, {
                "ui_task": self.ui_task,
                "ui": self.ui
            })

            # Update app reference to new context
            app.ctx = self

            # Update state
            self._state = ClientState.GAME
            self._current_client = game_client

            # Build new client features
            await game_client.build()

            # The world's UI is now in front of the user. Signal the launcher.
            self._ready_callback()

        except Exception:
            self._error_callback()
            raise
        finally:
            existing_ctx._is_transitioning = False
            self._is_transitioning = False
            self.takeover_complete.set()

    def run_gui(self):
        """Modified to support takeover of existing frontend UI (Kivy or TUI)."""
        if self._can_takeover_existing_ui():
            return asyncio.create_task(self._takeover_existing_ui())
        else:
            return self._create_new_gui()

    def _create_new_gui(self):
        """Create new GUI instance (existing behavior)"""
        self.ui = self.make_gui()(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    @functools.cached_property
    def raw_text_parser(self) -> RawJSONtoTextParser:
        return RawJSONtoTextParser(self)

    @property
    def total_locations(self) -> typing.Optional[int]:
        """Will return None until connected."""
        if self.checked_locations or self.missing_locations:
            return len(self.checked_locations | self.missing_locations)

    async def connection_closed(self):
        if self.server and self.server.socket is not None:
            await self.server.socket.close()
        self.reset_server_state()

    def reset_server_state(self):
        self.auth = None
        self.slot = None
        self.team = None
        self.timer = 0.0
        self.admin = False
        self.items_received = []
        self.locations_info = {}
        self.server_version = Version(0, 0, 0)
        self.generator_version = Version(0, 0, 0)
        self.server = None
        self.server_task = None
        self.hint_cost = None
        self.permissions = {
            "release": "disabled",
            "collect": "disabled",
            "remaining": "disabled",
        }

    async def disconnect(self, allow_autoreconnect: bool = False):
        if not allow_autoreconnect:
            self.disconnected_intentionally = True
            if self.cancel_autoreconnect():
                logger.info("Cancelled auto-reconnect.")
        if self.server and not self.server.socket.closed:
            await self.server.socket.close()
        if self.server_task is not None:
            await self.server_task
        if self.ui:
            self.ui.update_hints()

    async def send_msgs(self, msgs: typing.List[typing.Any]) -> None:
        """ `msgs` JSON serializable """
        if not self.server or not self.server.socket.open or self.server.socket.closed:
            return
        if msgs[0]["cmd"] == "LocationChecks":
            self.update_timer()
        await self.server.socket.send(encode(msgs))

    def consume_players_package(self, package: typing.List[tuple]):
        self.player_names = {slot: name for team, slot, name, orig_name in package if self.team == team}
        self.player_names[0] = "Archipelago"
        if self.ui:
            self.ui.ui_player_data = {slot: {} for team, slot, alias, name in package if self.team == team}

    def event_invalid_game(self):
        self.gui_error('Invalid Game', 'Please verify that you connected with the right game to the correct world.')
        logger.error('Invalid Game; please verify that you connected with the right game to the correct world.')

    async def client_get_password(self, password_requested: bool = False) -> str:
        if password_requested and not self.password:
            logger.info('Enter the password required to join this game:')
            self.password = await self.console_input()
            return self.password

    async def client_get_username(self) -> None:
        if not self.auth:
            self.auth = self.username
            if not self.auth:
                logger.info('Enter player name:')
                self.auth = await self.console_input()

    server_auth = client_get_password
    get_username = client_get_username
    # These names are crap, so I renamed them.

    async def send_connect(self, **kwargs: typing.Any) -> None:
        """
        Send a `Connect` packet to log in to the server,
        additional keyword args can override any value in the connection packet
        """
        payload = {
            'cmd': 'Connect',
            'password': self.password, 'name': self.auth, 'version': Utils.version_tuple,
            'tags': self.tags, 'items_handling': self.items_handling,
            'uuid': Utils.get_unique_identifier(), 'game': self.game, "slot_data": self.want_slot_data,
        }
        if kwargs:
            payload.update(kwargs)
        await self.send_msgs([payload])
        await self.send_msgs([{"cmd": "Get", "keys": ["_read_race_mode"]}])

    async def check_locations(self, locations: typing.Collection[int]) -> set[int]:
        """Send new location checks to the server. Returns the set of actually new locations that were sent."""
        locations = set(locations) & self.missing_locations
        await self.send_msgs([{"cmd": 'LocationChecks', "locations": tuple(locations)}])
        return locations

    async def console_input(self, prompt: Optional[str] = "") -> str:
        if self.ui and self.ui.is_on_console_screen():
            self.ui.focus_textinput()
        elif self.ui:
            if self._consolebox:
                self._consolebox = None
            from mwgg_gui.components.dialog import ConsoleBox
            self._consolebox = ConsoleBox(title="Response from " + self.hostname + ":" + self.port, prompt=prompt)
        self.input_requests += 1
        return await self.input_queue.get()

    async def connect(self, address: typing.Optional[str] = None) -> None:
        """ disconnect any previous connection, and open new connection to the server """
        await self.disconnect()
        self.server_task = asyncio.create_task(server_loop(self, address), name="server loop")

    def cancel_autoreconnect(self) -> bool:
        if self.autoreconnect_task:
            self.autoreconnect_task.cancel()
            self.autoreconnect_task = None
            return True
        return False

    def slot_concerns_self(self, slot) -> bool:
        """Helper function to abstract player groups, should be used instead of checking slot == self.slot directly."""
        if slot == self.slot:
            return True
        if slot in self.slot_info:
            return self.slot in self.slot_info[slot].group_members
        return False

    def is_echoed_chat(self, print_json_packet: dict) -> bool:
        """Helper function for filtering out messages sent by self."""
        return print_json_packet.get("type", "") == "Chat" \
            and print_json_packet.get("team", None) == self.team \
            and print_json_packet.get("slot", None) == self.slot

    def is_uninteresting_item_send(self, print_json_packet: dict) -> bool:
        """Helper function for filtering out ItemSend prints that do not concern the local player."""
        return print_json_packet.get("type", "") == "ItemSend" \
            and not self.slot_concerns_self(print_json_packet["receiving"]) \
            and not self.slot_concerns_self(print_json_packet["item"].player)
    
    def is_connection_change(self, print_json_packet: dict) -> bool:
        """Helper function for filtering out connection changes."""
        return print_json_packet.get("type", "") in ["Join","Part"]

    def on_print(self, args: dict):
        logger.info(args["text"])

    def on_print_json(self, args: dict):
        if self.ui:
            '''
            Filter out ItemSend messages that are not relevant to the local player if all_players_chat is False.
            '''
            if args.get("type") == 'Hint' and not self.slot_concerns_self(args.get("receiving")) and args.get("found"):
                pass
            elif args.get("type") == 'ItemSend' and not self.all_players_chat:
                if self.slot_concerns_self(args.get("receiving")):
                    self.ui.print_json(copy.deepcopy(args["data"]))
                elif args.get("item") and self.slot_concerns_self(args["item"].player):
                    self.ui.print_json(copy.deepcopy(args["data"]))
            else:
                # send copy to UI
                self.ui.print_json(copy.deepcopy(args["data"]))
                
        if args.get("type") == "Countdown":
            self.ui.countdown_timer = args.get("countdown", 0)
            self.update_timer(offset_time = self.ui.countdown_timer)  

        logging.getLogger("FileLog").info(self.rawjsontotextparser(copy.deepcopy(args["data"])),
                                          extra={"NoStream": True})
        logging.getLogger("StreamLog").info(self.jsontotextparser(copy.deepcopy(args["data"])),
                                            extra={"NoFile": True})
        if "tags" in args and args["slot"] in self.ui.ui_player_data:
            if not self.ui.ui_player_data[args["slot"]]:
                return
            # Toggle boolean UI flags based on presence in server-provided tags
            tags_iterable = args["tags"] or []
            tags_set = set(tags_iterable)
            player_data = self.ui.ui_player_data[args["slot"]]
            player_data.bk_mode = ("in_bk" in tags_set)
            player_data.deafened = ("deafened" in tags_set)
            # Extract pronouns from any tag that starts with "pronouns", e.g., "pronouns:she/her"
            pronouns_value = ""
            for tag_value in tags_iterable:
                if isinstance(tag_value, str) and tag_value.startswith("pronouns"):
                    _, _, suffix = tag_value.partition(":")
                    pronouns_value = suffix
                    break
            player_data.pronouns = pronouns_value


    def on_package(self, cmd: str, args: dict):
        """For custom package handling in subclasses."""
        pass

    def on_user_say(self, text: str) -> typing.Optional[str]:
        """Gets called before sending a Say to the server from the user.
        Returned text is sent, or sending is aborted if None is returned."""
        return text

    def on_ui_command(self, text: str) -> None:
        """Gets called by kivy when the user executes a command starting with `/` or `!`.
        The command processor is still called; this is just intended for command echoing."""
        self.ui.print_json([{"text": text, "type": "color", "color": "orange"}])

    def update_permissions(self, permissions: typing.Dict[str, int]):
        """Internal method to parse and save server permissions from RoomInfo"""
        for permission_name, permission_flag in permissions.items():
            try:
                flag = Permission(permission_flag)
                logger.info(f"{permission_name.capitalize()} permission: {flag.name}")
                self.permissions[permission_name] = flag.name
            except Exception as e:  # safeguard against permissions that may be implemented in the future
                logger.exception(e)

    async def shutdown(self):
        self.server_address = ""
        self.username = None
        self.password = None
        self.cancel_autoreconnect()
        if self.server and not self.server.socket.closed:
            await self.server.socket.close()
        if self.server_task:
            await self.server_task

        while self.input_requests > 0:
            self.input_queue.put_nowait(None)
            self.input_requests -= 1
        
        # Set exit event first so keep_alive can exit naturally
        self.exit_event.set()
        
        # Cancel keep_alive task if it's still running
        if self.keep_alive_task and not self.keep_alive_task.done():
            self.keep_alive_task.cancel()
            try:
                await self.keep_alive_task
            except asyncio.CancelledError:
                pass  # Expected when task is cancelled
        
        if self.ui_task:
            await self.ui_task
        if self.input_task:
            self.input_task.cancel()
    
    # Hints
    def update_hint(self, location: int, finding_player: int, status: typing.Optional[HintStatus]) -> None:
        msg = {"cmd": "UpdateHint", "location": location, "player": finding_player}
        if status is not None:
            msg["status"] = status
        async_start(self.send_msgs([msg]), name="update_hint")

    def update_mwgg_hint(self, location: int, finding_player: int, mwgg_status: MWGGUIHintStatus) -> None:
        msg = {"cmd": "Set", 
               "key": f"hints_{self.team}_{self.slot}_mwgg", 
               "want_reply": False, 
               "default": {}, 
               "operations": [{"operation": "replace", "value": {f"{finding_player}_{location}": mwgg_status.value}}]}
        async_start(self.send_msgs([msg]), name="update_mwgg_hint")

    @property
    def shared_activity_time(self) -> float | None:
        return self._shared_activity_time

    @shared_activity_time.setter
    def shared_activity_time(self, activity_time: float):
        self._shared_activity_time = activity_time

    @property
    def activity_time(self) -> float | None:
        return self._last_activity_time

    @activity_time.setter
    def activity_time(self, activity_time: float):
        self._last_activity_time = activity_time
        msg = {"cmd": "Set", 
            "key": f"activity_{self.team}_{self.slot}", 
            "want_reply": False,
            "default": [],
            "operations": [{"operation": "replace", "value": activity_time}]}
        async_start(self.send_msgs([msg]), name="set_last_activity")

    def update_timer(self, offset_time: float = 0):
        '''
        Update the timer based on the activity time.
        If the activity time is more than 300 seconds since the last activity, add the "break" time to the timer list.
        If the activity time is less than 300 seconds since the last activity, track this as the "last" activity time.
        If the activity time is not set, this is the first activity, so set the timer to the activity time.
        '''
        if self.timer == 0.0:
            self.activity_time = time.time() + offset_time
            if self.server and self.server.socket:
                if offset_time != 0 or len(self.checked_locations) > 0:
                    server_timer = self.stored_data.get("timer") or [self.activity_time]#start time
                    self.timer = server_timer[0]
                    msg = {"cmd": "Set", 
                        "key": f"timer", 
                        "want_reply": True,
                        "default": [self.timer],
                        "operations": [{"operation": "replace", "value": server_timer}]}
                    async_start(self.send_msgs([msg]), name="update_timer")
                    return
        else:
            if self.server and self.server.socket:
                if self.shared_activity_time is None:
                    self.shared_activity_time = 0
                    for i in self.player_names.keys():
                        if i != self.slot:
                            activity = self.stored_data.get(f"activity_{self.team}_{i}", 0)
                            if activity:
                                self.shared_activity_time = activity if activity > self.shared_activity_time else self.shared_activity_time
                    if self.shared_activity_time == 0:
                        return
                activity_time = time.time()
                elapsed_break = activity_time - self.shared_activity_time
                if elapsed_break > 300:
                    stored_activity_idx = self.stored_data.get("timer") or [self.timer]
                    stored_activity_idx.append(elapsed_break)
                    msg = {"cmd": "Set", 
                        "key": f"timer", 
                        "want_reply": False,
                        "default": [self.timer],
                        "operations": [{"operation": "replace", "value": stored_activity_idx}]}
                    async_start(self.send_msgs([msg]), name="update_timer")
                self.activity_time = activity_time

    # DataPackage
    async def prepare_data_package(self, relevant_games: typing.Set[str],
                                   remote_data_package_checksums: typing.Dict[str, str]):
        """Validate that all data is present for the current multiworld.
        Download, assimilate and cache missing data from the server."""
        # by documentation any game can use Archipelago locations/items -> always relevant
        relevant_games.add("Archipelago")

        from worlds import network_data_package, network_data_package_single_game
        network_data_package, network_data_package_single_game = set_local_network_data_package()

        for game in relevant_games:
            if game in network_data_package["games"]:
                self.checksums[game] = network_data_package["games"][game]["checksum"]

        self.update_data_package(network_data_package)

        needed_updates: typing.Set[str] = set()
        for game in relevant_games:
            if game not in remote_data_package_checksums:
                continue

            remote_checksum: typing.Optional[str] = remote_data_package_checksums.get(game)

            if not remote_checksum:  # custom data package and no checksum for this game
                needed_updates.add(game)
                continue

            cached_checksum: typing.Optional[str] = self.checksums.get(game)
            # no action required if cached version is new enough
            if remote_checksum != cached_checksum:
                local_checksum: typing.Optional[str] = network_data_package["games"].get(game, {}).get("checksum")
                if remote_checksum == local_checksum:
                    self.update_game(network_data_package["games"][game], game)
                else:
                    cached_game = Utils.load_data_package_for_checksum(game, remote_checksum)
                    cache_checksum: typing.Optional[str] = cached_game.get("checksum")
                    # download remote version if cache is not new enough
                    if remote_checksum != cache_checksum:
                        needed_updates.add(game)
                    else:
                        self.update_game(cached_game, game)
        if needed_updates:
            await self.send_msgs([{"cmd": "GetDataPackage", "games": [game_name]} for game_name in needed_updates])

    def update_game(self, game_package: dict, game: str):
        self.item_names.update_game(game, game_package["item_name_to_id"])
        self.location_names.update_game(game, game_package["location_name_to_id"])
        self.checksums[game] = game_package.get("checksum")

    def update_data_package(self, data_package: dict):
        for game, game_data in data_package["games"].items():
            self.update_game(game_data, game)

    def consume_network_data_package(self, data_package: dict):
        self.update_data_package(data_package)
        logger.info(f"Got new ID/Name DataPackage for {', '.join(data_package['games'])}")
        for game, game_data in data_package["games"].items():
            Utils.store_data_package_for_checksum(game, game_data)

    def consume_network_item_groups(self):
        data = {"item_name_groups": self.stored_data[f"_read_item_name_groups_{self.game}"]}
        current_cache = Utils.persistent_load().get("groups_by_checksum", {}).get(self.checksums[self.game], {})
        if self.game in current_cache:
            current_cache[self.game].update(data)
        else:
            current_cache[self.game] = data
        Utils.persistent_store("groups_by_checksum", self.checksums[self.game], current_cache)

    def consume_network_location_groups(self):
        data = {"location_name_groups": self.stored_data[f"_read_location_name_groups_{self.game}"]}
        current_cache = Utils.persistent_load().get("groups_by_checksum", {}).get(self.checksums[self.game], {})
        if self.game in current_cache:
            current_cache[self.game].update(data)
        else:
            current_cache[self.game] = data
        Utils.persistent_store("groups_by_checksum", self.checksums[self.game], current_cache)

    # data storage

    def set_notify(self, *keys: str) -> None:
        """Subscribe to be notified of changes to selected data storage keys.

        The values can be accessed via the "stored_data" attribute of this context, which is a dictionary mapping the
        names of the data storage keys to the latest values received from the server.
        """
        if new_keys := (set(keys) - self.stored_data_notification_keys):
            self.stored_data_notification_keys.update(new_keys)
            async_start(self.send_msgs([{"cmd": "Get",
                                         "keys": list(new_keys)},
                                        {"cmd": "SetNotify",
                                         "keys": list(new_keys)}]))

    # DeathLink hooks

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        """Gets dispatched when a new DeathLink is triggered by another linked player."""
        self.last_death_link = max(data["time"], self.last_death_link)
        text = data.get("cause", "")
        if text:
            logger.info(f"DeathLink: {text}")
        else:
            logger.info(f"DeathLink: Received from {data['source']}")

    async def send_death(self, death_text: str = ""):
        """Helper function to send a deathlink using death_text as the unique death cause string."""
        if self.server and self.server.socket:
            logger.info("DeathLink: Sending death to your friends...")
            self.last_death_link = time.time()
            await self.send_msgs([{
                "cmd": "Bounce", "tags": ["DeathLink"],
                "data": {
                    "time": self.last_death_link,
                    "source": self.player_names[self.slot],
                    "cause": death_text
                }
            }])

    async def update_death_link(self, death_link: bool):
        """Helper function to set Death Link connection tag on/off and update the connection if already connected.
        TODO: FIX SET VS LIST TAGS"""
        old_tags = self.tags.copy()
        if death_link:
            if isinstance(self.tags, set):
                self.tags.add("DeathLink")
            else:
                if "DeathLink" not in self.tags:
                    self.tags.append("DeathLink")
        else:
            if isinstance(self.tags, set):
                self.tags -= {"DeathLink"}
            else:
                if "DeathLink" in self.tags:
                    self.tags.remove("DeathLink")
        if old_tags != self.tags and self.server and not self.server.socket.closed:
            await self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}])

    async def update_tags(self, tags: typing.Set[str]):
        """Helper function to update the tags of the client."""
        old_tags = self.tags.copy()
        self.tags = tags
        if old_tags != self.tags and self.server and not self.server.socket.closed:
            await self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}])

    def gui_error(self, title: str, text: typing.Union[Exception, str]) -> typing.Optional["MessageBox"]:
        """Displays an error messagebox in the loaded Kivy UI. Override if using a different UI framework"""
        if not self.ui:
            return None
        title = title or "Error"
        if self._messagebox:
            self._messagebox.dismiss()
        # make "Multiple exceptions" look nice
        text = str(text).replace('[Errno', '\n[Errno').strip()
        # split long messages into title and text
        parts = title.split('. ', 1)
        if len(parts) == 1:
            parts = title.split(', ', 1)
        if len(parts) > 1:
            text = f"{parts[1]}\n\n{text}" if text else parts[1]
            title = parts[0]
        # display error
        from mwgg_gui.components.dialog import MessageBox
        self._messagebox = MessageBox(title=title, message=text, is_error=True)
        self._messagebox.open()
        return self._messagebox

    def handle_connection_loss(self, msg: str) -> None:
        """Helper for logging and displaying a loss of connection. Must be called from an except block."""
        exc_info = sys.exc_info()
        logger.exception(msg, exc_info=exc_info, extra={'compact_gui': True})
        
        # Hide loading screen if it exists
        if self.ui:
            self.ui.hide_loading()
     
        error_msg = ""
        # Provide helpful guidance for retrying connection
        if self.server_address:
            error_msg = f"To retry the connection, use: /connect {self.server_address}"
        else:
            error_msg = "To retry the connection, use: /connect <server_address:port>"
        
        # Show error message box using MDDialog
        if self.ui:
            error_text = str(exc_info[1]) if exc_info[1] else msg
            self._messagebox_connection_loss = self.gui_error("Connection Error", error_text + "\n" + msg)
        else:
            # Fallback to old method if no UI
            self.error(msg, exc_info[1])

    def make_gui(self) -> "type[FrontendProtocol]":
        """
        Return the frontend `App` class needed for `run_gui` so it can be overridden before being built.

        Dispatches on the `MWGG_FRONTEND` environment variable (set by `MultiWorld.py` from
        `--frontend={gui,tui}`). Defaults to the Kivy GUI.

        Common changes are changing `base_title` to update the window title of the client and
        updating `logging_pairs` to automatically make new tabs that can be filled with their respective logger.

        ex. `logging_pairs.append(("Foo", "Bar"))`
        will add a "Bar" tab which follows the logger returned from `logging.getLogger("Foo")`
        """
        from frontend_protocol import resolve_frontend_class
        return resolve_frontend_class()

    def run_cli(self):
        if sys.stdin:
            if sys.stdin.fileno() != 0:
                from multiprocessing import parent_process
                if parent_process():
                    return  # ignore MultiProcessing pipe

            # steam overlay breaks when starting console_loop
            if 'gameoverlayrenderer' in os.environ.get('LD_PRELOAD', ''):
                logger.info("Skipping terminal input, due to conflicting Steam Overlay detected. Please use GUI only.")
            else:
                self.input_task = asyncio.create_task(console_loop(self), name="Input")


async def keep_alive(ctx: CommonContext, seconds_between_checks=100):
    """some ISPs/network configurations drop TCP connections if no payload is sent (ignore TCP-keep-alive)
     so we send a payload to prevent drop and if we were dropped anyway this will cause an auto-reconnect."""
    seconds_elapsed = 0
    while not ctx.exit_event.is_set():
        await asyncio.sleep(1)  # short sleep to not block program shutdown
        if ctx.server and ctx.slot:
            seconds_elapsed += 1
            if seconds_elapsed > seconds_between_checks:
                ctx.update_timer()
                await ctx.send_msgs([{"cmd": "Bounce", "slots": [ctx.slot]}])
                seconds_elapsed = 0


async def server_loop(ctx: CommonContext, address: typing.Optional[str] = None) -> None:
    await ctx.takeover_complete.wait()
    if ctx.server and ctx.server.socket:
        logger.error('Already connected')
        return

    if address is None:  # set through CLI or APBP
        address = ctx.server_address

    # Wait for the user to provide a multiworld server address
    if not address:
        logger.info(f"Please connect to an {apname} server.")
        return

    ctx.cancel_autoreconnect()
    if ctx._messagebox_connection_loss:
        ctx._messagebox_connection_loss.dismiss()
        ctx._messagebox_connection_loss = None

    address = f"ws://{address}" if "://" not in address \
        else address.replace("archipelago://", "ws://").replace("mwgg://", "ws://")
    
    def reconnect_hint() -> str:
        return ", type /connect to reconnect" if ctx.server_address else ""

    username = f" with username {urllib.parse.urlparse(address).username}" if urllib.parse.urlparse(address).username else ""
    password = f" with password ********" if urllib.parse.urlparse(address).password else ""
    hostname = urllib.parse.urlparse(address).hostname
    port = str(urllib.parse.urlparse(address).port)
    logger.info(f'Connecting to {apname} server at {hostname}:{port}{username}{password}.')
    try:
        socket = await websockets.connect(address, ping_timeout=None, ping_interval=None,
                                          ssl=get_ssl_context() if address.startswith("wss://") else None,
                                          max_size=ctx.max_size)
        ctx.server = Endpoint(socket)
        logger.info('Connected')
        ctx.server_address = address
        ctx.current_reconnect_delay = ctx.starting_reconnect_delay
        ctx.disconnected_intentionally = False
        try:
            async for data in ctx.server.socket:
                for msg in decode(data):
                    await process_server_cmd(ctx, msg)
        except asyncio.CancelledError:
            # Expected when the task is cancelled during shutdown
            logger.info("Server loop cancelled during shutdown")
            raise
        except Exception as e:
            # Log unexpected errors but don't let them crash the loop
            logger.warning(f"Error in server loop: {e}", exc_info=True)
        finally:
            logger.warning(f"Disconnected from multiworld server{reconnect_hint()}")
    except websockets.InvalidMessage:
        # probably encrypted
        if address.startswith("ws://"):
            # try wss
            await server_loop(ctx, "ws" + address[1:])
        else:
            ctx.handle_connection_loss(f"Lost connection to the multiworld server due to InvalidMessage"
                                       f"{reconnect_hint()}")
    except ConnectionRefusedError:
        ctx.handle_connection_loss("Connection refused by the server. "
                                   f"May not be running {apname} on that address or port.")
    except websockets.InvalidURI:
        ctx.handle_connection_loss("Failed to connect to the multiworld server (invalid URI)")
    except asyncio.TimeoutError:
        ctx.handle_connection_loss("Failed to connect to the multiworld server. Connection timed out.")
    except OSError:
        ctx.handle_connection_loss("Failed to connect to the multiworld server")
    except Exception:
        ctx.handle_connection_loss(f"Lost connection to the multiworld server{reconnect_hint()}")
    finally:
        await ctx.connection_closed()
        if ctx.server_address and ctx.username and not ctx.disconnected_intentionally:
            logger.info(f"... automatically reconnecting in {ctx.current_reconnect_delay} seconds")
            assert ctx.autoreconnect_task is None
            ctx.autoreconnect_task = asyncio.create_task(server_autoreconnect(ctx), name="server auto reconnect")
        ctx.current_reconnect_delay *= 2


async def server_autoreconnect(ctx: CommonContext):
    if ctx.exit_event.is_set():
        return
    await asyncio.sleep(ctx.current_reconnect_delay)
    if ctx.server_address and ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")


async def process_server_cmd(ctx: CommonContext, args: dict):
    try:
        cmd = args["cmd"]
    except:
        logger.exception(f"Could not get command from {args}")
        raise
    if cmd == 'RoomInfo':
        if ctx.seed_name and ctx.seed_name != args["seed_name"]:
            msg = "The server is running a different multiworld than your client is. (invalid seed_name)"
            logger.info(msg, extra={'compact_gui': True})
            ctx.gui_error('Error', msg)
        else:
            logger.info('--------------------------------')
            logger.info('Room Information:')
            logger.info('--------------------------------')
            version = args["version"]
            ctx.server_version = Version(*version)

            if "generator_version" in args:
                ctx.generator_version = Version(*args["generator_version"])
                logger.info(f'Server protocol version: {ctx.server_version.as_simple_string()}, '
                            f'generator version: {ctx.generator_version.as_simple_string()}, '
                            f'tags: {", ".join(args["tags"])}')
            else:
                logger.info(f'Server protocol version: {ctx.server_version.as_simple_string()}, '
                            f'tags: {", ".join(args["tags"])}')
            if args['password']:
                logger.info('Password required')
            ctx.update_permissions(args.get("permissions", {}))
            logger.info(
                f"A !hint costs {args['hint_cost']}% of your total location count as points"
                f" and you get {args['location_check_points']}"
                f" for each location checked. Use !hint for more information.")
            ctx.hint_cost = int(args['hint_cost'])
            ctx.check_points = int(args['location_check_points'])

            if "players" in args:  # TODO remove when servers sending this are outdated
                players = args.get("players", [])
                if len(players) < 1:
                    logger.info('No player connected')
                else:
                    players.sort()
                    current_team = -1
                    logger.info('Connected Players:')
                    for network_player in players:
                        if network_player.team != current_team:
                            logger.info(f'  Team #{network_player.team + 1}')
                            current_team = network_player.team
                        logger.info('    %s (Player %d)' % (network_player.alias, network_player.slot))

            # update data package
            data_package_checksums = args.get("datapackage_checksums", {})
            await ctx.prepare_data_package(set(args["games"]), data_package_checksums)

            await ctx.server_auth(args['password'])

    elif cmd == 'DataPackage':
        ctx.consume_network_data_package(args['data'])

    elif cmd == 'ConnectionRefused':
        errors = args["errors"]
        if 'InvalidGame' in errors:
            ctx.disconnected_intentionally = True
            ctx.event_invalid_game()
        elif 'IncompatibleVersion' in errors:
            ctx.disconnected_intentionally = True
            raise Exception('Server reported your client version as incompatible. '
                            'This probably means you have to update.')
        elif 'InvalidItemsHandling' in errors:
            raise Exception('The item handling flags requested by the client are not supported')
        # last to check, recoverable problem
        elif 'InvalidSlot' in errors:
            logger.error('Player name is incorrect, please verify that you have entered your player name exactly as it appears in your YAML file.')
            ctx.auth = None
            ctx.username = None
            await ctx.client_get_username()
        elif 'InvalidPassword' in errors:
            logger.error('Invalid password')
            ctx.password = None
            await ctx.client_get_password(True)
        elif errors:
            raise Exception("Unknown connection errors: " + str(errors))
        else:
            raise Exception('Connection refused by the multiworld host, no reason provided')

    elif cmd == 'Connected':
        ctx.username = ctx.auth
        ctx.team = args["team"]
        ctx.slot = args["slot"]
        # int keys get lost in JSON transfer
        ctx.slot_info = {0: NetworkSlot("Archipelago", "Archipelago", SlotType.player)}
        ctx.slot_info.update({int(pid): data for pid, data in args["slot_info"].items()})
        ctx.hint_points = args.get("hint_points", 0)
        ctx.players = args["players"]
        ctx.consume_players_package(args["players"])
        ctx.stored_data_notification_keys.add(f"_read_hints_{ctx.team}_{ctx.slot}")
        ctx.stored_data_notification_keys.add(f"hints_{ctx.team}_{ctx.slot}_mwgg")
        ctx.stored_data_notification_keys.add(f"timer")
        # Add profile_data keys for all players in the multiworld
        for slot_id in ctx.slot_info.keys():
            if slot_id != 0:  # Skip Archipelago slot
                ctx.stored_data_notification_keys.add(f"profile_data_{ctx.team}_{slot_id}")
                ctx.stored_data_notification_keys.add(f"activity_{ctx.team}_{slot_id}")
        msgs = []
        if ctx.locations_checked:
            msgs.append({"cmd": "LocationChecks",
                         "locations": list(ctx.locations_checked)})
        if ctx.locations_scouted:
            msgs.append({"cmd": "LocationScouts",
                         "locations": list(ctx.locations_scouted)})
        if ctx.stored_data_notification_keys:
            msgs.append({"cmd": "Get",
                         "keys": list(ctx.stored_data_notification_keys)})
            msgs.append({"cmd": "SetNotify",
                         "keys": list(ctx.stored_data_notification_keys)})
        if msgs:
            await ctx.send_msgs(msgs)
        if ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        # Get the server side view of missing as of time of connecting.
        # This list is used to only send to the server what is reported as ACTUALLY Missing.
        # This also serves to allow an easy visual of what locations were already checked previously
        # when /missing is used for the client side view of what is missing.
        ctx.missing_locations = set(args["missing_locations"])
        ctx.checked_locations = set(args["checked_locations"])
        ctx.server_locations = ctx.missing_locations | ctx. checked_locations

        server_url = urllib.parse.urlparse(ctx.server_address)
        Utils.persistent_store("client", "last_server_hostname", server_url.hostname)
        Utils.persistent_store("client", "last_server_port", server_url.port)

        if ctx.ui:
            ctx.ui.on_connect()

    elif cmd == 'ReceivedItems':
        start_index = args["index"]
        
        if ctx.items_received is None:
            ctx.items_received = []

        if start_index == 0:
            ctx.items_received = []
        elif start_index != len(ctx.items_received):
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks",
                                 "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
        if start_index == len(ctx.items_received):
            for item in args['items']:
                ctx.items_received.append(NetworkItem(*item))
        ctx.watcher_event.set()

    elif cmd == 'LocationInfo':
        for item in [NetworkItem(*item) for item in args['locations']]:
            ctx.locations_info[item.location] = item
        ctx.watcher_event.set()

    elif cmd == "RoomUpdate":
        if "players" in args:
            ctx.consume_players_package(args["players"])
            ctx.players = args["players"]
        if "hint_points" in args:
            ctx.hint_points = args['hint_points']
        if "checked_locations" in args:
            checked = set(args["checked_locations"])
            ctx.checked_locations |= checked
            ctx.missing_locations -= checked
        if "permissions" in args:
            ctx.update_permissions(args["permissions"])

    elif cmd == 'Print':
        ctx.on_print(args)

    elif cmd == 'PrintJSON':
        data = args.get("data", [])
        if "CommandResult" in args.get("type", "") and any("successful" in a.get("text", "") for a in data if "text" in a):
            text_parts = [a["text"] for a in data if "text" in a]
            if "Login" in text_parts:
                ctx.admin = True
            elif "Logout" in text_parts:
                ctx.admin = False
        ctx.on_print_json(args)

    elif cmd == 'InvalidPacket':
        logger.warning(f"Invalid Packet of {args['type']}: {args['text']}")

    elif cmd == "Bounced":
        tags = args.get("tags", [])
        # we can skip checking "DeathLink" in ctx.tags, as otherwise we wouldn't have been send this
        if "DeathLink" in tags and ctx.last_death_link != args["data"]["time"]:
            ctx.on_deathlink(args["data"])

    elif cmd == "Retrieved":
        ctx.stored_data.update(args["keys"])
        if ctx.ui and f"_read_hints_{ctx.team}_{ctx.slot}" in args["keys"]:
            ctx.ui.update_hints()
        if ctx.ui and f"hints_{ctx.team}_{ctx.slot}_mwgg" in args["keys"]:
            ctx.ui.update_mwgg_hints()
        if ctx.ui and f"timer" in args["keys"]:
            ctx.ui.update_timer(args["keys"].get("timer"))
        # Update profile data for all players when retrieved (on connect)
        if ctx.ui:
            for key in args["keys"]:
                if key.startswith(f"profile_data_{ctx.team}_"):
                    slot_id = int(key.split("_")[-1])
                    if slot_id in ctx.ui.ui_player_data:
                        profile_data = args["keys"][key]
                        if profile_data:
                            for item, data in profile_data.items():
                                if hasattr(ctx.ui.ui_player_data[slot_id], item):
                                    setattr(ctx.ui.ui_player_data[slot_id], item, data)
        if f"activity_{ctx.team}_" in args["keys"]:
            activity_value = args["keys"].get(f"activity_{ctx.team}_{ctx.slot}")
            if activity_value is not None and (ctx.shared_activity_time is None or activity_value > ctx.shared_activity_time):
                ctx.shared_activity_time = activity_value

    elif cmd == "SetReply":
        ctx.stored_data[args["key"]] = args["value"]
        if ctx.ui and f"_read_hints_{ctx.team}_{ctx.slot}" == args["key"]:
            ctx.ui.update_hints()
        elif ctx.ui and f"hints_{ctx.team}_{ctx.slot}_mwgg" == args["key"]:
            ctx.ui.update_mwgg_hints()
        elif ctx.ui and f"timer" == args["key"]:
            ctx.ui.update_timer(args["value"])
        elif args["key"].startswith(f"profile_data_{ctx.team}_"):
            # Update profile data when another client changes their profile
            if ctx.ui:
                slot_id = int(args["key"].split("_")[-1])
                if slot_id in ctx.ui.ui_player_data and slot_id != ctx.slot:
                    profile_data = args["value"]
                    if profile_data:
                        for item, data in profile_data.items():
                            if hasattr(ctx.ui.ui_player_data[slot_id], item):
                                setattr(ctx.ui.ui_player_data[slot_id], item, data)
        elif args["key"].startswith(f"activity_{ctx.team}_"):
            if args["value"] is not None and (ctx.shared_activity_time is None or args["value"] > ctx.shared_activity_time):
                ctx.shared_activity_time = args["value"]
        elif args["key"].startswith("EnergyLink"):
            ctx.current_energy_link_value = args["value"]
            if ctx.ui:
                ctx.ui.set_new_energy_link_value()

    elif cmd == "SetUserTags":
        ctx.player_info[args["slot"]]["tags"] = args["tags"]
    else:
        logger.debug(f"unknown command {cmd}")

    ctx.on_package(cmd, args)


async def console_loop(ctx: CommonContext):
    from rich import Console
    console = Console(force_terminal=True, force_interactive=True)
    commandprocessor = ctx.command_processor(ctx)
    queue = asyncio.Queue()
    stream_input(console.input(prompt=f"{ctx.server_address}: "), queue)
    while not ctx.exit_event.is_set():
        try:
            input_text = await queue.get()
            queue.task_done()

            if ctx.input_requests > 0:
                ctx.input_requests -= 1
                ctx.input_queue.put_nowait(input_text)
                continue

            if input_text:
                commandprocessor(input_text)
        except Exception as e:
            logger.exception(e)


def get_base_parser(description: typing.Optional[str] = None):
    """Base argument parser to be reused for components subclassing off of CommonClient"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--connect', default=None, help='Address of the multiworld host.')
    parser.add_argument('--password', default=None, help='Password of the multiworld host.')
    if sys.stdout:  # If terminal output exists, offer gui-less mode
        parser.add_argument('--nogui', default=False, action='store_true', help="Turns off Client GUI.")
    return parser


def handle_url_arg(args: "argparse.Namespace",
                   parser: "typing.Optional[argparse.ArgumentParser]" = None) -> "argparse.Namespace":
    """
    Parse the url arg "archipelago://name:pass@host:port" or "mwgg://name:pass@host:port" from launcher into correct launch args for CommonClient
    If alternate data is required the urlparse response is saved back to args.url if valid
    """
    if not args.url:
        return args
        
    url = urllib.parse.urlparse(args.url)
    if url.scheme != "archipelago" and url.scheme != "mwgg":
        if not parser:
            parser = get_base_parser()
        parser.error(f"bad url, found {args.url}, expected url in form of archipelago://multiworld.gg:38281 or mwgg://multiworld.gg:38281")
        return args

    args.url = url
    args.connect = url.netloc
    if url.username:
        args.name = urllib.parse.unquote(url.username)
    if url.password:
        args.password = urllib.parse.unquote(url.password)

    return args


def launch_textclient(server_address: str = None):
    """Launch text client in GUI integration mode like KH2.

    ready_callback and error_callback are wired centrally in CommonContext via
    Utils._perform_module_launch; no need for this function to accept or forward them.
    """

    class TextContext(CommonContext):
        # Text Mode to use !hint and such with games that have no text entry
        tags = CommonContext.tags | {"TextOnly"}
        game = ""  # empty matches any game since 0.3.2
        items_handling = 0b111  # receive all items for /received
        want_slot_data = False  # Can't use game specific slot_data

        def __init__(self, server_address: str = None):
            super(TextContext, self).__init__(server_address=server_address)

            if self.username is not None:
                self.auth = self.username
            else:
                self.auth = None

        async def server_auth(self, password_requested: bool = False):
            if password_requested and not self.password:
                await super(TextContext, self).server_auth(password_requested)

            if not self.auth:
                await self.get_username()
            await self.send_connect(game="")

        def on_package(self, cmd: str, args: dict):
            if cmd == "Connected":
                self.game = self.slot_info[self.slot].game

        async def disconnect(self, allow_autoreconnect: bool = False):
            self.game = ""
            await super().disconnect(allow_autoreconnect)

    async def main(args):
        ctx = TextContext(server_address)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        # Try to takeover existing frontend UI (Kivy or TUI)
        if ctx._can_takeover_existing_ui():
            await ctx._takeover_existing_ui()
        else:
            logger.critical("Text client did not launch properly, exiting.")
            ctx._error_callback()
            ctx.takeover_complete.set()  # unblock the pending server_loop so it can take its no-address early return
            return

        ctx.ui.base_title = apname + " | Text Client"
        await ctx.server_auth()

        # Wait for exit instead of running a watcher
        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    # Check if we're already in an event loop (GUI mode)
    try:
        loop = asyncio.get_running_loop()
        logger.info("Running text client in existing event loop (GUI mode)")

        # Create a simple namespace object to mimic argparse.Namespace
        class Args:
            def __init__(self, server_address):
                self.server_address = server_address

        args = Args(server_address)
        task = asyncio.create_task(main(args), name="TextClientMain")
        return task
    except RuntimeError:
        logger.critical("This is not a standalone text client. Please run the MultiWorld GUI.")
        # No CommonContext was constructed in this branch, so no _error_callback
        # is reachable here; Utils._perform_module_launch will fire its pending
        # callback fallback if this raises out.

def main_textclient(server_address: str):
    """Main entry point for integration with MultiWorld system"""
    return launch_textclient(server_address)