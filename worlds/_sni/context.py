from __future__ import annotations

import sys
import threading
import time
import multiprocessing
import os
import subprocess
import base64
import logging
import asyncio
import enum
import typing

from json import loads, dumps

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, gui_enabled, get_base_parser

import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"
from settings import Settings
from Utils import async_start
from MultiServer import mark_raw
if typing.TYPE_CHECKING:
    from .client import SNIClient

if __name__ == "__main__":
    Utils.init_logging("SNIClient", exception_logger="Client")

import colorama
from websockets.client import connect as websockets_connect, WebSocketClientProtocol
from websockets.exceptions import WebSocketException, ConnectionClosed

# Import SNI communication functions from __init__.py
from . import (
    SNESState, snes_logger, launch_sni, _snes_connect, get_snes_devices, 
    verify_snes_app, snes_connect, snes_disconnect, task_alive, 
    snes_autoreconnect, snes_recv_loop, snes_read, snes_write, 
    snes_buffered_write, snes_flush_writes
)


class DeathState(enum.IntEnum):
    killing_player = 1
    alive = 2
    dead = 3


class SNIClientCommandProcessor(ClientCommandProcessor):
    ctx: SNIContext

    def _cmd_slow_mode(self, toggle: str = "") -> None:
        """Toggle slow mode, which limits how fast you send / receive items."""
        if toggle:
            self.ctx.slow_mode = toggle.lower() in {"1", "true", "on"}
        else:
            self.ctx.slow_mode = not self.ctx.slow_mode

        self.output(f"Setting slow mode to {self.ctx.slow_mode}")

    @mark_raw
    def _cmd_snes(self, snes_options: str = "") -> bool:
        """Connect to a snes. Optionally include network address of a snes to connect to,
        otherwise show available devices; and a SNES device number if more than one SNES is detected.
        Examples: "/snes", "/snes 1", "/snes localhost:23074 1" """
        if self.ctx.snes_state in {SNESState.SNES_ATTACHED, SNESState.SNES_CONNECTED, SNESState.SNES_CONNECTING}:
            self.output("Already connected to SNES. Disconnecting first.")
            self._cmd_snes_close()
        return self.connect_to_snes(snes_options)

    def connect_to_snes(self, snes_options: str = "") -> bool:
        snes_address = self.ctx.snes_address
        snes_device_number = -1

        options = snes_options.split()
        num_options = len(options)

        if num_options > 1:
            snes_address = options[0]
            snes_device_number = int(options[1])
        elif num_options > 0:
            snes_device_number = int(options[0])

        self.ctx.snes_reconnect_address = None
        if self.ctx.snes_connect_task:
            self.ctx.snes_connect_task.cancel()
        self.ctx.snes_connect_task = asyncio.create_task(snes_connect(self.ctx, snes_address, snes_device_number),
                                                         name="SNES Connect")
        return True

    def _cmd_snes_close(self) -> bool:
        """Close connection to a currently connected snes"""
        self.ctx.snes_reconnect_address = None
        self.ctx.cancel_snes_autoreconnect()
        self.ctx.snes_state = SNESState.SNES_DISCONNECTED
        if self.ctx.snes_socket and not self.ctx.snes_socket.closed:
            async_start(self.ctx.snes_socket.close())
            return True
        else:
            return False

    # Left here for quick re-addition for debugging.
    # def _cmd_snes_write(self, address, data):
    #     """Write the specified byte (base10) to the SNES' memory address (base16)."""
    #     if self.ctx.snes_state != SNESState.SNES_ATTACHED:
    #         self.output("No attached SNES Device.")
    #         return False
    #     snes_buffered_write(self.ctx, int(address, 16), bytes([int(data)]))
    #     async_start(snes_flush_writes(self.ctx))
    #     self.output("Data Sent")
    #     return True

    # def _cmd_snes_read(self, address, size=1):
    #     """Read the SNES' memory address (base16)."""
    #     if self.ctx.snes_state != SNESState.SNES_ATTACHED:
    #         self.output("No attached SNES Device.")
    #         return False
    #     data = await snes_read(self.ctx, int(address, 16), size)
    #     self.output(f"Data Read: {data}")
    #     return True


class SNIContext(CommonContext):
    command_processor: typing.Type[SNIClientCommandProcessor] = SNIClientCommandProcessor
    game: typing.Optional[str] = None  # set in validate_rom
    items_handling: typing.Optional[int] = None  # set in game_watcher
    snes_connect_task: "typing.Optional[asyncio.Task[None]]" = None
    snes_autoreconnect_task: typing.Optional["asyncio.Task[None]"] = None

    snes_address: str
    snes_socket: typing.Optional[WebSocketClientProtocol]
    snes_state: SNESState
    snes_attached_device: typing.Optional[typing.Tuple[int, str]]
    snes_reconnect_address: typing.Optional[str]
    snes_recv_queue: "asyncio.Queue[bytes]"
    snes_request_lock: asyncio.Lock
    snes_write_buffer: typing.List[typing.Tuple[int, bytes]]
    snes_connector_lock: threading.Lock
    death_state: DeathState
    killing_player_task: "typing.Optional[asyncio.Task[None]]"
    allow_collect: bool
    slow_mode: bool

    client_handler: typing.Optional[SNIClient]
    awaiting_rom: bool
    rom: typing.Optional[bytes]
    prev_rom: typing.Optional[bytes]

    hud_message_queue: typing.List[str]  # TODO: str is a guess, is this right?
    death_link_allow_survive: bool

    def __init__(self, snes_address: str, server_address: str, password: str, ready_callback: typing.Callable[[], None] | None = None, error_callback: typing.Callable[[], None] | None = None) -> None:
        super(SNIContext, self).__init__(server_address, password)
        # callbacks
        self.ready_callback = ready_callback
        self.error_callback = error_callback
        # snes stuff
        self.snes_address = snes_address
        self.snes_socket = None
        self.snes_state = SNESState.SNES_DISCONNECTED
        self.snes_attached_device = None
        self.snes_reconnect_address = None
        self.snes_recv_queue = asyncio.Queue()
        self.snes_request_lock = asyncio.Lock()
        self.snes_write_buffer = []
        self.snes_connector_lock = threading.Lock()
        self.death_state = DeathState.alive  # for death link flop behaviour
        self.killing_player_task = None
        self.allow_collect = False
        self.slow_mode = False

        self.client_handler = None
        self.awaiting_rom = False
        self.rom = None
        self.prev_rom = None
        if self.ready_callback:
            from kivy.clock import Clock
            Clock.schedule_once(self.ready_callback, 0.1)

    async def connection_closed(self) -> None:
        await super(SNIContext, self).connection_closed()
        self.awaiting_rom = False

    def event_invalid_slot(self) -> typing.NoReturn:
        if self.snes_socket is not None and not self.snes_socket.closed:
            async_start(self.snes_socket.close())
        raise Exception("Invalid ROM detected, "
                        "please verify that you have loaded the correct rom and reconnect your snes (/snes)")

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super(SNIContext, self).server_auth(password_requested)
        if self.rom is None:
            self.awaiting_rom = True
            snes_logger.info(
                "No ROM detected, awaiting snes connection to authenticate to the multiworld server (/snes)")
            return
        self.awaiting_rom = False
        # TODO: This looks kind of hacky...
        # Context.auth is meant to be the "name" parameter in send_connect,
        # which has to be a str (bytes is not json serializable).
        # But here, Context.auth is being used for something else
        # (where it has to be bytes because it is compared with rom elsewhere).
        # If we need to save something to compare with rom elsewhere,
        # it should probably be in a different variable,
        # and let auth be used for what it's meant for.
        self.auth = self.rom
        auth = base64.b64encode(self.rom).decode()
        await self.send_connect(name=auth)

    def cancel_snes_autoreconnect(self) -> bool:
        if self.snes_autoreconnect_task:
            self.snes_autoreconnect_task.cancel()
            self.snes_autoreconnect_task = None
            return True
        return False

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        if not self.killing_player_task or self.killing_player_task.done():
            self.killing_player_task = asyncio.create_task(deathlink_kill_player(self))
        super(SNIContext, self).on_deathlink(data)

    async def handle_deathlink_state(self, currently_dead: bool, death_text: str = "") -> None:
        # in this state we only care about triggering a death send
        if self.death_state == DeathState.alive:
            if currently_dead:
                self.death_state = DeathState.dead
                await self.send_death(death_text)
        # in this state we care about confirming a kill, to move state to dead
        elif self.death_state == DeathState.killing_player:
            # this is being handled in deathlink_kill_player(ctx) already
            pass
        # in this state we wait until the player is alive again
        elif self.death_state == DeathState.dead:
            if not currently_dead:
                self.death_state = DeathState.alive

    async def shutdown(self) -> None:
        await super(SNIContext, self).shutdown()
        self.cancel_snes_autoreconnect()
        if self.snes_connect_task:
            try:
                await asyncio.wait_for(self.snes_connect_task, 1)
            except asyncio.TimeoutError:
                self.snes_connect_task.cancel()

    def on_package(self, cmd: str, args: typing.Dict[str, typing.Any]) -> None:
        if cmd in {"Connected", "RoomUpdate"}:
            if "checked_locations" in args and args["checked_locations"]:
                new_locations = set(args["checked_locations"])
                self.checked_locations |= new_locations
                self.locations_scouted |= new_locations
                # Items belonging to the player should not be marked as checked in game,
                # since the player will likely need that item.
                # Once the games handled by SNIClient gets made to be remote items,
                # this will no longer be needed.
                async_start(self.send_msgs([{"cmd": "LocationScouts", "locations": list(new_locations)}]))
                
        if self.client_handler is not None:
            self.client_handler.on_package(self, cmd, args)

    # def run_gui(self) -> None:
    #     from Gui import MultiMDApp

    #     class SNIManager(MultiMDApp):
    #         logging_pairs = [
    #             ("Client", "Archipelago"),
    #             ("SNES", "SNES"),
    #         ]
    #         base_title = apname + " SNI Client"

    #     self.ui = SNIManager(self)
    #     self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")  # type: ignore


async def deathlink_kill_player(ctx: SNIContext) -> None:
    ctx.death_state = DeathState.killing_player
    while ctx.death_state == DeathState.killing_player and \
            ctx.snes_state == SNESState.SNES_ATTACHED:

        if ctx.client_handler is None:
            continue

        await ctx.client_handler.deathlink_kill_player(ctx)

        ctx.last_death_link = time.time()

async def game_watcher(ctx: SNIContext) -> None:
    perf_counter = time.perf_counter()
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
        except asyncio.TimeoutError:
            pass
        ctx.watcher_event.clear()

        if not ctx.rom or not ctx.client_handler:
            ctx.finished_game = False
            ctx.death_link_allow_survive = False

            from .client import AutoSNIClientRegister
            ctx.client_handler = await AutoSNIClientRegister.get_handler(ctx)

            if not ctx.client_handler:
                continue

            if not ctx.rom:
                continue

            if not ctx.prev_rom or ctx.prev_rom != ctx.rom:
                ctx.locations_checked = set()
                ctx.locations_scouted = set()
                ctx.locations_info = {}
            ctx.prev_rom = ctx.rom

            if ctx.awaiting_rom:
                await ctx.server_auth(False)
            elif ctx.server is None:
                snes_logger.warning("ROM detected but no active multiworld server connection. " +
                                    "Connect using command: /connect server:port")

        if not ctx.client_handler:
            continue

        try:
            rom_validated = await ctx.client_handler.validate_rom(ctx)
        except Exception as e:
            snes_logger.error(f"An error occurred, see logs for details: {e}")
            text_file_logger = logging.getLogger()
            text_file_logger.exception(e)
            rom_validated = False

        if not rom_validated or (ctx.auth and ctx.auth != ctx.rom):
            snes_logger.warning("ROM change detected, please reconnect to the multiworld server")
            await ctx.disconnect(allow_autoreconnect=True)
            ctx.client_handler = None
            ctx.rom = None
            ctx.command_processor(ctx).connect_to_snes()
            continue

        delay = 7 if ctx.slow_mode else 0
        if time.perf_counter() - perf_counter < delay:
            continue

        perf_counter = time.perf_counter()

        try:
            await ctx.client_handler.game_watcher(ctx)
        except Exception as e:
            snes_logger.error(f"An error occurred, see logs for details: {e}")
            text_file_logger = logging.getLogger()
            text_file_logger.exception(e)
            await snes_disconnect(ctx)


async def run_game(romfile: str) -> None:
    auto_start = Settings.sni_options.snes_rom_start
    if auto_start is True:
        import webbrowser
        webbrowser.open(romfile)
    elif isinstance(auto_start, str) and os.path.isfile(auto_start):
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def launch(server_address: str = None, password: str = None, ready_callback=None, error_callback=None, snes_address: str = "localhost:23074", diff_file: str = None) -> None:
    logging.getLogger("SNIClient")

    async def main():
        multiprocessing.freeze_support()
        
        ctx = SNIContext(snes_address, server_address, password, ready_callback, error_callback)
        if ctx._can_takeover_existing_gui():
            await ctx._takeover_existing_gui() 
        else:
            snes_logger.critical("Client did not launch properly, exiting.")
            if error_callback:
                error_callback()
            return

        ctx.ui.base_title = apname + " | SNI Client"
        ctx.mwserver_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        await ctx.server_auth()

        if diff_file:
            import Patch
            logging.info("Patch file was supplied. Creating sfc rom..")
            try:
                meta, romfile = Patch.create_rom_file(diff_file)
            except Exception as e:
                Utils.messagebox('Error', str(e), True)
                raise
            
            # Only use metadata server if no server_address was provided
            if "server" in meta and not server_address:
                ctx.server_address = meta["server"]
                
            logging.info(f"Wrote rom file to {romfile}")
            
            # Store the ROM file path for game-specific adjustments
            ctx.rom_file = romfile
            
            if diff_file.endswith(".apsoe"):
                import webbrowser
                async_start(run_game(romfile))
                await _snes_connect(ctx, snes_address, False)
                webbrowser.open(f"http://www.evermizer.com/apclient/#server={meta['server']}")
                logging.info("Starting Evermizer Client in your Browser...")
                import time
                time.sleep(3)
                sys.exit()
            else:
                async_start(run_game(romfile))

        ctx.snes_connect_task = asyncio.create_task(snes_connect(ctx, ctx.snes_address), name="SNES Connect")
        watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")

        await ctx.exit_event.wait()

        ctx.server_address = None
        ctx.snes_reconnect_address = None
        if ctx.snes_socket is not None and not ctx.snes_socket.closed:
            await ctx.snes_socket.close()
        await watcher_task
        await ctx.shutdown()

    import colorama

    # Check if we're already in an event loop (GUI mode) first
    try:
        loop = asyncio.get_running_loop()
        # We're in an existing event loop, create a task
        snes_logger.info("Running in existing event loop (GUI mode)")
        
        # Create a simple namespace object to mimic argparse.Namespace
        class Args:
            def __init__(self, server_address, password, snes_address, diff_file):
                self.server_address = server_address
                self.password = password
                self.snes_address = snes_address
                self.diff_file = diff_file
        
        args = Args(server_address, password, snes_address, diff_file)
        task = asyncio.create_task(main(), name="SNIMain")
        return task
    except RuntimeError:
        snes_logger.critical("This is not a standalone client. Please run the MultiWorld GUI to start the SNI client.")
        if error_callback:
            error_callback()


def main(server_address: str = None, password: str = None, ready_callback=None, error_callback=None, snes_address: str = "localhost:23074", diff_file: str = None):
    launch(server_address, password, ready_callback, error_callback, snes_address, diff_file)
