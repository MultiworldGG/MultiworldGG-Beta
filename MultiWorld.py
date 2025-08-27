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
else:
    os.environ["KIVY_DATA_DIR"] = os.path.join(local_path(),"kivy", "data")
os.environ["KIVY_HOME"] = os.path.join(local_path(),"data")
os.makedirs(os.environ["KIVY_HOME"], exist_ok=True)

from mwgg_splash import main

logger = logging.getLogger("MultiWorld")

def launch_splash_screen():
    """Launch the splash screen as a separate process"""
    try:
        if sys.platform == "win32":
            splash_process = subprocess.Popen(
                [sys.executable, "-m", "mwgg_splash", "20"],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            splash_process = subprocess.Popen(
                [sys.executable, "-m", "mwgg_splash", "20"]
            )
        
        # Check if the process started successfully
        if splash_process.poll() is not None:
            # Process exited immediately, something went wrong
            logging.error("Splash screen process exited immediately")
            return None
        
        logging.info(f"Splash screen launched with PID: {splash_process.pid}")
        return splash_process
    except Exception as e:
        logging.error(f"Failed to launch splash screen: {e}")
        return None

def terminate_splash_screen(splash_process=None):
    """Send termination signal to the splash screen"""
    try:
        # Create a termination file in KIVY_DATA_DIR
        kivy_data_dir = os.getenv("KIVY_DATA_DIR")
        if not kivy_data_dir:
            kivy_data_dir = os.getenv("KIVY_HOME")
        if not kivy_data_dir:
            # Fallback to script directory if environment variables not set
            kivy_data_dir = os.path.dirname(os.path.abspath(__file__))
        
        flag_path = os.path.join(kivy_data_dir, "terminate_splash.flag")
        
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

def run_client(*args, splash_process=None):
    """Start the MWGG client"""
    
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
    logging.getLogger().setLevel(logging.INFO)
    splash_process = launch_splash_screen()
    run_client(*sys.argv[1:], splash_process)