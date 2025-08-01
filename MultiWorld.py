import asyncio
import sys
import logging
import os
import re
import subprocess
import time
from Utils import discover_and_launch_module

worlds_modules_dir = os.path.abspath(os.path.join("worlds"))
if worlds_modules_dir not in sys.path:
    sys.path.insert(0, worlds_modules_dir)

import gui.Gui

logger = logging.getLogger("MultiWorld")

def launch_splash_screen():
    """Launch the splash screen as a separate process"""
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        splash_path = os.path.join(script_dir, "gui", "splashscreen.py")
        
        # Launch the splash screen process
        if sys.platform == "win32":
            splash_process = subprocess.Popen(
                [sys.executable, splash_path],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            splash_process = subprocess.Popen(
                [sys.executable, splash_path]
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
        ctx = InitContext()
        ctx.splash_process = splash_process  # Pass the splash process to the context
        
        # Check if a specific module was requested
        if len(args) > 1 and args[1].startswith("--game="):
            game_name = args[1].split("=")[1]
            logger.info(f"Attempting to launch game: {game_name}")
            
            # Try to launch the module via entrypoints
            try:
                discover_and_launch_module(game_name, args)
                return  # Module takeover successful, exit initial client
            except Exception as e:
                logger.error(f"Module launch failed: {e}")
                # Fall back to initial client
                logger.info("Falling back to initial client")
        
        # Default initial client behavior
        logger.info("Launching default GUI")
        ctx.run_gui()

        await ctx.exit_event.wait()
        await ctx.shutdown()
        sys.exit()

    import colorama
    colorama.just_fix_windows_console()

    asyncio.run(main(args))
    colorama.deinit()

if __name__ == "__main__":
   run_client(*sys.argv[1:])