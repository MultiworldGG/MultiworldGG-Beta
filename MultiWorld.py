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
    # Set KIVY_DEPS_ROOT for ANGLE dependency
    os.environ["KIVY_DEPS_ROOT"] = os.path.join(local_path(),"lib")
else:
    os.environ["KIVY_DATA_DIR"] = os.path.join(local_path(),"kivy", "data")

os.environ["KIVY_HOME"] = os.path.join(local_path(),"data")
os.makedirs(os.environ["KIVY_HOME"], exist_ok=True)

# Debug logging for Kivy paths
logging.debug(f"KIVY_DATA_DIR: {os.environ.get('KIVY_DATA_DIR')}")
logging.debug(f"KIVY_DEPS_ROOT: {os.environ.get('KIVY_DEPS_ROOT')}")
logging.debug(f"KIVY_HOME: {os.environ.get('KIVY_HOME')}")

from mwgg_splash import main

logger = logging.getLogger("MultiWorld")

def launch_splash_screen():
    """Launch the splash screen as a separate process"""
    try:
        # When not frozen, use Python module execution
        if sys.platform == "win32":
            splash_process = subprocess.Popen(
                [sys.executable, "-m", "mwgg_splash"],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            splash_process = subprocess.Popen(
                [sys.executable, "-m", "mwgg_splash"]
            )
        
        logging.info(f"Splash screen launched with PID: {splash_process.pid}")
        return splash_process
    except Exception as e:
        logging.error(f"Failed to launch splash screen: {e}")
        return None

def terminate_splash_screen(splash_process=None):
    """Send termination signal to the splash screen"""
    try:
        # Create a termination file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        flag_path = os.path.join(script_dir, "gui", "terminate_splash.flag")
        
        with open(flag_path, "w") as f:
            f.write("terminate")
        
        logging.info("Termination signal sent to splash screen")
        
        # Clean up the flag file
        if os.path.exists(flag_path):
            os.remove(flag_path)
            
        # If the process is still running, terminate it
        if splash_process and splash_process.poll() is None:
            splash_process.terminate()
            splash_process.wait(timeout=2)

    except Exception as e:
        logging.error(f"Failed to terminate splash screen: {e}")

def run_client(*args):
    """Start the MWGG client"""
    # Launch splash screen immediately at startup
    splash_process = launch_splash_screen()
    
    async def main(args):
        from CommonClient import InitContext
        from Utils import init_logging
        init_logging("MultiWorld")

        ctx = InitContext()
        ctx.splash_process = splash_process  # Pass the splash process to the context
        
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

    asyncio.run(main(args))
    colorama.deinit()
    
# from ModuleUpdate import update
# update()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    run_client(*sys.argv[1:])