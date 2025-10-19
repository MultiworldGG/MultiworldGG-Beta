from multiprocessing import freeze_support, Process, Queue, set_start_method
import asyncio
import sys
import logging
import os
import re
import subprocess
import time
from importlib import metadata
from argparse import ArgumentParser

os.environ["KIVY_NO_CONSOLELOG"] = "0"
os.environ["KIVY_NO_FILELOG"] = "0"
os.environ["KIVY_LOG_ENABLE"] = "1"

# from CommonClient import console_loop
# from MultiServer import console
# apname = "Archipelago" if not Utils.archipelago_name else Utils.archipelago_name

from BaseUtils import local_path, is_frozen, init_logging
from mwgg_splash import main as splash_main

if is_frozen():
    os.environ["KIVY_NO_ARGS"] = "1"

# Ensure ctypes is imported early (fixes WinDLL issues in frozen builds)
import ctypes

if is_frozen():
    os.environ["KIVY_DATA_DIR"] = os.path.join(local_path(),"lib", "kivy", "data")
    lib_path = os.path.join(sys.exec_prefix, "lib")
    if lib_path not in sys.path:
        sys.path.append(lib_path)
else:
    os.environ["KIVY_DATA_DIR"] = os.path.join(local_path(),"kivy", "data")
os.environ["KIVY_HOME"] = os.path.join(local_path(),"data")
os.makedirs(os.environ["KIVY_HOME"], exist_ok=True)

# mwgg_splash is imported dynamically when needed to avoid bundling it into frozen executable

def terminate_splash_screen(queue: "Queue" ):
    """Terminate the splash screen process by name"""
    try:
        # Try queue-based termination first if queue is provided
        queue.put_nowait({"type": "terminate"})
        
        # Search for processes by name using multiprocessing
        import multiprocessing
        active_processes = multiprocessing.active_children()
        
        for proc in active_processes:
            if proc.name == "SplashScreen" and proc.is_alive():
                # Try process termination
                proc.terminate()
                proc.join(timeout=2)
                # Final fallback - force kill
                if proc.is_alive():
                    proc.kill()
                    proc.join()
                return
        
    except Exception as e:
        logging.error(f"Failed to terminate splash screen: {e}")

def run_client(*args, queue=None):
    """Start the MWGG client"""
    
    async def main(args: list[str]):
        from CommonClient import InitContext

        logger = logging.getLogger("MultiWorld")
        ctx = InitContext()
        
        # Check if a specific module was requested
        try:
            if args and args.game and args.server_address:
                logger.info(f"Attempting to launch game: {args.game}")
                from Utils import get_available_worlds, discover_and_launch_module

                if args.game not in get_available_worlds():
                    raise Exception(f"Game {args.game} not found in available worlds")

                # Try to launch the module via entrypoints
                try:
                    discover_and_launch_module(module_name=args.game, 
                                            server_address=args.server_address, 
                                            slot_name=args.slot_name, 
                                            password=args.password)
                    return  # Module takeover successful, exit initial client
                except Exception as e:
                    logger.error(f"Module launch failed: {e}")
                    # Fall back to initial client
                    logger.info("Falling back to launcher")
        except Exception as e:
            pass
        
        # Default initial client behavior
        logger.info("Launching default GUI")
        try:
            ctx.run_gui(splash_queue=queue)
            await ctx.exit_event.wait()
        except Exception as e:
            logger.error(f"Error during GUI execution: {e}", exc_info=True)
            # Don't exit immediately - let the user see the error
            print(f"\nCRITICAL ERROR: {e}")
            print("Press Enter to exit...")
            input()
        finally:
            # Ensure cleanup happens even if there are errors
            try:
                await ctx.shutdown()
            except Exception as e:
                logger.error(f"Error during shutdown: {e}", exc_info=True)
            finally:
                sys.exit()

    import colorama
    colorama.just_fix_windows_console()

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\nPress Enter to exit...")
        input()
    finally:
        colorama.deinit()

if __name__ == "__main__":
    # Multiprocessing protection for frozen executables
    # This prevents fork bombs when creating subprocesses in cx_Freeze builds
    freeze_support()

    init_logging("MultiWorld", logging.DEBUG)
    logger = logging.getLogger("MultiWorld")

    # Start the splash screen process
    set_start_method("spawn")
    splash_queue = Queue()
    Process(target=splash_main, name="SplashScreen", args=(splash_queue,)).start()
    
    # Wait for splash process to signal ready (after checking/applying updates)
    logger.info("Checking for updates...")
    try:
        message = splash_queue.get(timeout=60)  # Wait up to 60 seconds
        if isinstance(message, dict):
            msg_type = message.get("type")
            if msg_type == "update_complete":
                logger.info("Updates applied successfully")
            elif msg_type == "ready":
                pass
    except Exception as e:
        logger.warning(f"Timeout or error waiting for splash screen: {e}")
    
    # Parse the command line arguments
    if sys.argv[1:]:
        parser = ArgumentParser()
        parser.add_argument("--game", type=str, default=None, optional=True, help="The game module to launch\nGame Name will not work, use the apworld abbreviation")
        parser.add_argument("--server-address", type=str, default=None, optional=True, help="The server address to connect to")
        parser.add_argument("--slot-name", type=str, default=None, optional=True, help="The slot name to connect to")
        parser.add_argument("--password", type=str, default=None, optional=True, help="The password to connect to")
        args = parser.parse_args(sys.argv[1:])
    else:
        args = None
    # Run the main client in the current process
    run_client(args, queue=splash_queue)