from multiprocessing import freeze_support, Process
import asyncio
import sys
import logging
import os
import re
import subprocess
import time
from importlib import metadata


os.environ["KIVY_NO_CONSOLELOG"] = "0"
os.environ["KIVY_NO_FILELOG"] = "0"
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_LOG_ENABLE"] = "1"

# from CommonClient import console_loop
# from MultiServer import console
# apname = "Archipelago" if not Utils.archipelago_name else Utils.archipelago_name

from BaseUtils import local_path, is_frozen

if is_frozen():
    os.environ["KIVY_DATA_DIR"] = os.path.join(local_path(),"lib", "kivy", "data")
    sys.path.append(os.path.join(os.path.dirname(__file__), "world_plugins", "lib", "python", \
        sys.winver, "site-packages", "worlds"))
else:
    os.environ["KIVY_DATA_DIR"] = os.path.join(local_path(),"kivy", "data")
os.environ["KIVY_HOME"] = os.path.join(local_path(),"data")
os.makedirs(os.environ["KIVY_HOME"], exist_ok=True)

# mwgg_splash is imported dynamically when needed to avoid bundling it into frozen executable

logger = logging.getLogger("MultiWorld")


def terminate_splash_screen():
    """Terminate the splash screen process by name"""
    try:
        # Search for processes by name using multiprocessing
        import multiprocessing
        active_processes = multiprocessing.active_children()
        
        for proc in active_processes:
            if proc.name == "SplashScreen" and proc.is_alive():
                logging.debug(f"Found splash screen process by name (PID: {proc.pid})")
                proc.terminate()
                proc.join(timeout=2)
                if proc.is_alive():
                    logging.warning("Splash process didn't terminate gracefully, forcing kill")
                    proc.kill()
                    proc.join()
                logging.debug("Splash screen process terminated successfully")
                return
        
        logging.debug("No splash screen process found to terminate")
        
    except Exception as e:
        logging.error(f"Failed to terminate splash screen: {e}")

def run_client(*args):
    """Start the MWGG client"""
    
    async def main(args):
        from CommonClient import InitContext
        from Utils import init_logging
        init_logging("MultiWorld")

        ctx = InitContext()
        
        # Check if a specific module was requested
        if len(args) > 1 and args[1].startswith("--game="):
            game_name = args[1].split("=")[1]
            logger.info(f"Attempting to launch game: {game_name}")
            
            # Try to launch the module via entrypoints
            try:
                from Utils import discover_and_launch_module
                discover_and_launch_module(game_name, args)
                return  # Module takeover successful, exit initial client
            except Exception as e:
                logger.error(f"Module launch failed: {e}")
                # Fall back to initial client
                logger.info("Falling back to initial client")
        
        # Default initial client behavior
        logger.info("Launching default GUI")
        try:
            ctx.run_gui()
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
    logging.getLogger().setLevel(logging.INFO)
    from mwgg_splash import main as splash_main
    
    # Start splash screen in separate process
    splash_process = Process(target=splash_main, name="SplashScreen")
    splash_process.start()
    
    # Run the main client in the current process
    run_client(*sys.argv[1:])