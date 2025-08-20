from __future__ import annotations
import asyncio
import Utils
from CommonClient import CommonClient, logger, server_loop
from worlds.seaofthieves.Client.SotCustomClient import SOT_Context
from worlds.seaofthieves import ClientInput

apname = Utils.instance_name if Utils.instance_name else "Archipelago"


def launch(server_address: str = None, password: str = None, ready_callback=None, error_callback=None, apsot_file: str = None):
    """
    Launch the client
    """
    import logging
    logging.getLogger("SeaOfThievesClient")

    async def main():
        ctx = SOT_Context(server_address, password, ready_callback, error_callback)
        if ctx._can_takeover_existing_gui():
            await ctx._takeover_existing_gui() 
        else:
            logger.critical("Client did not launch properly, exiting.")
            if error_callback:
                error_callback()
            return

        ctx.ui.base_title = apname + " | Sea of Thieves"
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        await ctx.server_auth()

        try:
            if not apsot_file:
                apsot_file = Utils.open_filename('Select APSOT file', (('APSOT File', ('.apsot',)),))
            client_input: ClientInput = ClientInput()
            client_input.from_fire(apsot_file)
            ctx.userInformation.generationData = client_input
        except Exception as e:
            ctx.output("Error uploading sotci file, was your filepath correct? {}".format(e))
            if error_callback:
                error_callback()
            return

        ctx.active_tasks.append(asyncio.create_task(ctx.updaterLoopa(), name="game watcher"))
        
        await ctx.application_exit()

    import colorama

    # Check if we're already in an event loop (GUI mode) first
    try:
        loop = asyncio.get_running_loop()
        # We're in an existing event loop, create a task
        logger.info("Running in existing event loop (GUI mode)")
        
        task = asyncio.create_task(main(), name="SeaOfThievesMain")
        return task
    except RuntimeError:
        logger.critical("This is not a standalone client. Please run the MultiWorld GUI to start the Sea of Thieves client.")
        if error_callback:
            error_callback()


def main(server_address: str = None, password: str = None, ready_callback=None, error_callback=None, apsot_file: str = None):
    """Main entry point for integration with MultiWorld system"""
    launch(server_address, password, ready_callback, error_callback, apsot_file)


if __name__ == '__main__':
    launch()
