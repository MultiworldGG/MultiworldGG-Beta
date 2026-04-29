
import logging
import sys
import asyncio
import typing
from CommonClient import CommonContext, get_base_parser, server_loop
import Utils
import re
import urllib.parse
from .OpenRCT2Socket import OpenRCT2Socket

apname = Utils.instance_name if Utils.instance_name else "Archipelago"

if __name__ == "__main__":
    print("\n\n\n\n\n\n==================================\n")
    Utils.init_logging("TextClient", exception_logger="Client")
# without terminal, we have to use gui mode
gui_enabled = not sys.stdout or "--nogui" not in sys.argv

logger = logging.getLogger("Client")

class OpenRCT2Context(CommonContext):
    tags = {"DeathLink"}
    game = "OpenRCT2"
    items_handling = 0b111  # receive all items for /received
    want_slot_data = True 

    def __init__(self, server_address: typing.Optional[str], slot_name: typing.Optional[str], password: typing.Optional[str], ready_callback=None, error_callback=None) -> None:
        super().__init__(server_address, password)
        self.ready_callback = ready_callback
        self.error_callback = error_callback
        self.username = urllib.parse.urlparse(server_address).username
        self.gamesock = OpenRCT2Socket(self)
        self.game_connection_established = False
        #kivy.set_title("OpenRCT2 Client")
        if self.ready_callback:
            from kivy.clock import Clock
            Clock.schedule_once(self.ready_callback, 0.1)

    async def server_auth(self, password_requested: bool = False):
        if not self.game_connection_established:
            logger.info('Awaiting connection to OpenRCT2')
            await self.gamesock.connected_to_game.wait()
            
        
        if password_requested and not self.password:
            await super(OpenRCT2Context, self).server_auth(password_requested)


        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "PrintJSON":
            for index, item in enumerate(args['data']):
                match = re.search(r'\[color=[^\]]+\](.*?)\[/color\]', args['data'][index]['text'])
                if match:
                    args['data'][index]['text'] = match.group(1) 
        print(args)
        self.gamesock.sendobj(args)

    # def run_gui(self): #Sets the title of the client
    #     """Import kivy UI system and start running it as self.ui_task."""
    #     from Gui import MultiMDApp

    #     class TextManager(MultiMDApp):
    #         logging_pairs = [
    #             ("Client", "Archipelago")
    #         ]
    #         base_title = "OpenRCT2 Client"

    #     self.ui = TextManager(self)
    #     self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def launch(server_address: str = None, password: str = None, ready_callback=None, error_callback=None):
    """
    Launch the client
    """
    import logging
    logging.getLogger("OpenRCT2Client")

    async def main():
        ctx = OpenRCT2Context(server_address, password, ready_callback, error_callback)
        if ctx._can_takeover_existing_gui():
            await ctx._takeover_existing_gui() 
        else:
            logger.critical("Client did not launch properly, exiting.")
            if error_callback:
                error_callback()
            return

        ctx.ui.base_title = apname + " | OpenRCT2"
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        await ctx.server_auth()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    # Check if we're already in an event loop (GUI mode) first
    try:
        loop = asyncio.get_running_loop()
        # We're in an existing event loop, create a task
        logger.info("Running in existing event loop (GUI mode)")
        
        task = asyncio.create_task(main(), name="OpenRCT2Main")
        return task
    except RuntimeError:
        logger.critical("This is not a standalone client. Please run the MultiWorld GUI to start the OpenRCT2 client.")
        if error_callback:
            error_callback()


def main(server_address: str = None, password: str = None, ready_callback=None, error_callback=None):
    """Main entry point for integration with MultiWorld system"""
    launch(server_address, password, ready_callback, error_callback)
