from typing import Optional, Dict
import asyncio
import multiprocessing
import traceback
import os

# Move up two directories from the client script location
launcher_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(launcher_dir)

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
import Utils

apname = Utils.instance_name if Utils.instance_name else "Archipelago"

from .Sly1Interface import Sly1Interface, Sly1Episode
from .Callbacks import init, update
from .data.Constants import LEVELS, MOVES

class Sly1CommandProcessor(ClientCommandProcessor):
    def _cmd_vaults(self):
        """Print the names of levels with vaults you can open"""
        if isinstance(self.ctx, Sly1Context):
            if self.ctx.slot_data is None:
                logger.info("Connect to a slot first!")
            elif self.ctx.slot_data["options"]["ItemCluesanityBundleSize"] == 0:
                logger.info("Just do it like in vanilla, dummy!")
            elif not self.ctx.openable_vaults:
                logger.info("No vaults available to open")
            else:
                logger.info(f"Can open: {', '.join(self.ctx.openable_vaults)}")

    def _cmd_check_goal(self):
        """Check your progress towards your goal"""
        if isinstance(self.ctx, Sly1Context):
            if self.ctx.slot_data is None:
                logger.info("Connect to a slot first!")
            elif self.ctx.slot_data["options"].get("UnlockClockwerk", 1) == 1:
                logger.info(f"{self.ctx.bosses_beaten} bosses out of {self.ctx.slot_data["options"]["RequiredBosses"]}")
            else:
                logger.info(f"{self.ctx.goal_pages} pages out of {self.ctx.slot_data["options"]["RequiredPages"]}")

class Sly1Context(CommonContext):
    command_processor = Sly1CommandProcessor
    game_interface: Sly1Interface
    game = "Sly Cooper and the Thievius Raccoonus"
    items_handling = 0b111
    pcsx2_sync_task: Optional[asyncio.Task] = None
    is_connected_to_game: bool = False
    is_connected_to_server: bool = False
    slot_data: Optional[dict[str, Utils.Any]] = None
    last_error_message: Optional[str] = None
    openable_vaults: list[str] = []
    opened_vaults: list[str] = []

    #Game state
    current_episode: Optional[Sly1Episode] = None
    thief_moves: int = 0
    bosses_beaten: int = 0
    SAVE_FILE = "sly1_item_progress.json"

    #Items and checks
    inven_keys: list[int] = [0, 0, 0, 0]
    inven_moves: list[int] = [0 for _ in MOVES]
    level_keys: list[list[bool]] = [
        [False for _ in levels[0]] for levels in LEVELS.values()
    ]
    vaults: list[list[bool]] = [
        [False for _ in levels[0]] for levels in LEVELS.values()
    ]
    hourglasses: list[list[bool]] = [
        [False for _ in levels[0]] for levels in LEVELS.values()
    ]
    bottles: list[list[int]] = [
        [0 for _ in levels[0]] for levels in LEVELS.values()
    ]
    hubs: list[bool] = [False, False, False, False]
    goal_pages: int = 0
    all_moves = 0
    for name, move in MOVES.items():
        if "Blueprints" in name:
            continue
        if isinstance(move, list):
            for level in move:
                all_moves |= level
        else:
            all_moves |= move

    def __init__(self, server_address, password, ready_callback=None, error_callback=None):
        super().__init__(server_address, password)
        self.ready_callback = ready_callback
        self.error_callback = error_callback
        self.game_interface = Sly1Interface(logger)

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super(Sly1Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.slot_data = args["slot_data"]

def update_connection_status(ctx: Sly1Context, status: bool):
    if ctx.is_connected_to_game == status:
        return

    if status:
        logger.info("Connected to Sly 1")
    else:
        logger.info("Unable to connect to the PCSX2 instance, attempting to reconnect...")

    ctx.is_connected_to_game = status

async def pcsx2_sync_task(ctx: Sly1Context):
    logger.info("Starting Sly 1 Connector, attempting to connect to emulator...")
    ctx.game_interface.connect_to_game()
    while not ctx.exit_event.is_set():
        try:
            is_connected = ctx.game_interface.get_connection_state()
            update_connection_status(ctx, is_connected)
            if is_connected:
                await _handle_game_ready(ctx)
            else:
                await _handle_game_not_ready(ctx)
        except ConnectionError:
            ctx.game_interface.disconnect_from_game()
        except Exception as e:
            if isinstance(e, RuntimeError):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())
            await asyncio.sleep(3)
            continue

async def _handle_game_ready(ctx: Sly1Context) -> None:
    current_address = ctx.game_interface.get_current_address()
    current_episode = ctx.game_interface.get_current_episode()
    current_level = ctx.game_interface.get_current_level_name()

    ctx.game_interface.skip_cutscene()

    #if ctx.is_loading:
        #if not ctx.game_interface.is_loading():
            #ctx.is_loading = False
            #await asyncio.sleep(1)
        #await asyncio.sleep(0.1)
        #return

    #if ctx.game_interface.is_loading():
        #ctx.is_loading = True
        #return

    connected_to_server = (ctx.server is not None) and (ctx.slot is not None)

    new_connection = ctx.is_connected_to_server != connected_to_server
    if ctx.current_episode != current_episode or new_connection:
        ctx.current_episode = current_episode
        ctx.is_connected_to_server = connected_to_server
        await init(ctx, connected_to_server)
        await ctx.game_interface.write_name_pointers()

    await update(ctx, connected_to_server)

    if ctx.server:
        ctx.last_error_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return

        await asyncio.sleep(0.1)
    else:
        message = "Waiting for player to connect to server"
        if ctx.last_error_message is not message:
            logger.info("Waiting for player to connect to server")
            ctx.last_error_message = message
        await asyncio.sleep(1)


async def _handle_game_not_ready(ctx: Sly1Context):
    """If the game is not connected, this will attempt to retry connecting to the game."""
    ctx.game_interface.connect_to_game()
    await asyncio.sleep(3)

def launch(server_address: str = None, password: str = None, ready_callback=None, error_callback=None):
    """
    Launch the client
    """
    import logging
    logging.getLogger("Sly1Client")

    async def main():
        multiprocessing.freeze_support()
        
        ctx = Sly1Context(server_address, password, ready_callback, error_callback)
        if ctx._can_takeover_existing_gui():
            await ctx._takeover_existing_gui() 
        else:
            logger.critical("Client did not launch properly, exiting.")
            if error_callback:
                error_callback()
            return

        ctx.ui.base_title = apname + " | Sly Cooper"
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        await ctx.server_auth()

        ctx.pcsx2_sync_task = asyncio.create_task(pcsx2_sync_task(ctx), name="PCSX2 Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.pcsx2_sync_task:
            await asyncio.sleep(3)
            await ctx.pcsx2_sync_task

    import colorama

    # Check if we're already in an event loop (GUI mode) first
    try:
        loop = asyncio.get_running_loop()
        # We're in an existing event loop, create a task
        logger.info("Running in existing event loop (GUI mode)")
        
        task = asyncio.create_task(main(), name="Sly1Main")
        return task
    except RuntimeError:
        logger.critical("This is not a standalone client. Please run the MultiWorld GUI to start the Sly1 client.")
        if error_callback:
            error_callback()


def main(server_address: str = None, password: str = None, ready_callback=None, error_callback=None):
    """Main entry point for integration with MultiWorld system"""
    launch(server_address, password, ready_callback, error_callback)

if __name__ == "__main__":
    launch_client()