from __future__ import annotations
import os
import sys
import asyncio
import shutil

import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"
if __name__ == "__main__":
    Utils.init_logging("ChecksFinderClient", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop


class ChecksFinderClientCommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True


class ChecksFinderContext(CommonContext):
    command_processor: int = ChecksFinderClientCommandProcessor
    game = "ChecksFinder"
    items_handling = 0b111  # full remote

    def __init__(self, server_address, password, ready_callback=None, error_callback=None):
        super(ChecksFinderContext, self).__init__(server_address, password)
        self.ready_callback = ready_callback
        self.error_callback = error_callback
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        if "localappdata" in os.environ:
            self.game_communication_path = os.path.expandvars(r"%localappdata%/ChecksFinder")
        else:
            # not windows. game is an exe so let's see if wine might be around to run it
            if "WINEPREFIX" in os.environ:
                wineprefix = os.environ["WINEPREFIX"]
            elif shutil.which("wine") or shutil.which("wine-stable"):
                wineprefix = os.path.expanduser("~/.wine") # default root of wine system data, deep in which is app data
            else:
                msg = "ChecksFinderClient couldn't detect system type. Unable to infer required game_communication_path"
                logger.error("Error: " + msg)
                Utils.messagebox("Error", msg, error=True)
                sys.exit(1)
            self.game_communication_path = os.path.join(
                wineprefix,
                "drive_c",
                os.path.expandvars("users/$USER/Local Settings/Application Data/ChecksFinder"))

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ChecksFinderContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(ChecksFinderContext, self).connection_closed()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root + "/" + file)

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(ChecksFinderContext, self).shutdown()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root+"/"+file)

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
            for ss in self.checked_locations:
                filename = f"send{ss}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    f.close()
        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received):
                for item in args['items']:
                    filename = f"AP_{str(NetworkItem(*item).location)}PLR{str(NetworkItem(*item).player)}.item"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        f.write(str(NetworkItem(*item).item))
                        f.close()

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        f.close()

    # def run_gui(self):
    #     """Import kivy UI system and start running it as self.ui_task."""
    #     from Gui import MultiMDApp

    #     class ChecksFinderManager(MultiMDApp):
    #         logging_pairs = [
    #             ("Client", "Archipelago")
    #         ]
    #         base_title = apname + " ChecksFinder Client"

    #     self.ui = ChecksFinderManager(self)
    #     self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def game_watcher(ctx: ChecksFinderContext):
    from worlds.checksfinder.Locations import lookup_id_to_name
    while not ctx.exit_event.is_set():
        if ctx.syncing == True:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        sending = []
        victory = False
        for root, dirs, files in os.walk(ctx.game_communication_path):
            for file in files:
                if file.find("send") > -1:
                    st = file.split("send", -1)[1]
                    sending = sending+[(int(st))]
                if file.find("victory") > -1:
                    victory = True
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


def launch(server_address: str = None, password: str = None, ready_callback=None, error_callback=None):
    """
    Launch the client
    """
    import logging
    logging.getLogger("ChecksFinderClient")

    async def main():
        ctx = ChecksFinderContext(server_address, password, ready_callback, error_callback)
        if ctx._can_takeover_existing_gui():
            await ctx._takeover_existing_gui() 
        else:
            logger.critical("Client did not launch properly, exiting.")
            if error_callback:
                error_callback()
            return

        ctx.ui.base_title = apname + " | ChecksFinder"
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        await ctx.server_auth()

        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="ChecksFinderProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher
        await ctx.shutdown()

    import colorama

    # Check if we're already in an event loop (GUI mode) first
    try:
        loop = asyncio.get_running_loop()
        # We're in an existing event loop, create a task
        logger.info("Running in existing event loop (GUI mode)")
        
        task = asyncio.create_task(main(), name="ChecksFinderMain")
        return task
    except RuntimeError:
        logger.critical("This is not a standalone client. Please run the MultiWorld GUI to start the ChecksFinder client.")
        if error_callback:
            error_callback()


def main(server_address: str = None, password: str = None, ready_callback=None, error_callback=None):
    """Main entry point for integration with MultiWorld system"""
    launch(server_address, password, ready_callback, error_callback)