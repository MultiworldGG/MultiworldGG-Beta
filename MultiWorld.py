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

def _install_kivy_import_debugger() -> None:
    """Log where Kivy/ANGLE will be imported from and key env/paths.
    Does not alter behavior, only prints diagnostics to stdout.
    """
    try:
        print("=== KIVY IMPORT DEBUG ===")
        print(f"frozen={getattr(sys, 'frozen', False)} exe={sys.executable}")
        print(f"cwd={os.getcwd()}")
        print(f"argv0_dir={os.path.dirname(sys.argv[0])}")
        # Key env vars
        for key in ("KIVY_DATA_DIR", "KIVY_HOME", "KIVY_GL_BACKEND", "KIVY_WINDOW", "PATH"):
            val = os.environ.get(key)
            if key == "PATH" and val:
                # print just first few entries
                parts = val.split(os.pathsep)
                val = os.pathsep.join(parts[:5]) + ("..." if len(parts) > 5 else "")
            print(f"ENV {key}={val}")
        # sys.path (first few)
        for i, p in enumerate(sys.path[:10]):
            print(f"sys.path[{i}]={p}")
        # Try to locate specs without importing
        try:
            import importlib.machinery as _mach
            for name in ("kivy", "kivy_deps", "kivy_deps.sdl2", "kivy_deps.glew", "kivy_deps.angle", "kivy.utils"):
                try:
                    spec = _mach.PathFinder.find_spec(name)
                except Exception as e:
                    print(f"spec {name}: error {e}")
                else:
                    if spec is None:
                        print(f"spec {name}: None")
                    else:
                        locs = getattr(spec, 'submodule_search_locations', None)
                        print(f"spec {name}: origin={spec.origin} loader={type(spec.loader).__name__} locations={locs}")
        except Exception as e:
            print(f"spec scan error: {e}")
        # List likely DLL dirs
        try:
            base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else local_path()
            for rel in ("lib", os.path.join("lib", "kivy")):
                d = os.path.join(base_dir, rel)
                if os.path.isdir(d):
                    names = [n for n in os.listdir(d) if n.lower().endswith('.dll')][:10]
                    print(f"DLLs in {d}: {names}{'...' if len(names)==10 else ''}")
        except Exception as e:
            print(f"dir scan error: {e}")
        # Lightweight import tracer
        try:
            import importlib.abc as _abc
            import importlib.machinery as _mach2
            class _KivyTraceFinder(_abc.MetaPathFinder):
                def find_spec(self, fullname, path=None, target=None):
                    if fullname.startswith("kivy"):
                        try:
                            spec = _mach2.PathFinder.find_spec(fullname, path)
                        except Exception as e:
                            print(f"TRACE find_spec {fullname}: error {e}")
                            return None
                        if spec is not None:
                            print(f"TRACE import {fullname}: origin={spec.origin} loader={type(spec.loader).__name__}")
                        else:
                            print(f"TRACE import {fullname}: spec=None")
                        return spec
                    return None
            # Insert at front but after builtins
            sys.meta_path.insert(0, _KivyTraceFinder())
        except Exception as e:
            print(f"trace hook error: {e}")
        print("=== END KIVY IMPORT DEBUG ===")
    except Exception as e:
        print(f"kivy import debug setup failed: {e}")

def launch_splash_screen():
    """Launch the splash screen as a separate process"""
    try:
        if sys.platform == "win32":
            splash_process = subprocess.Popen(
                [sys.executable, "-m", "mwgg_splash"],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            splash_process = subprocess.Popen(
                [sys.executable, "-m", "mwgg_splash"]
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

def run_client(*args):
    """Start the MWGG client"""
    # Emit import diagnostics before any Kivy imports can happen
    _install_kivy_import_debugger()

    # Launch splash screen immediately at startup
    #splash_process = launch_splash_screen()
    
    async def main(args):
        from CommonClient import InitContext
        from Utils import init_logging
        init_logging("MultiWorld")

        ctx = InitContext()
        #ctx.splash_process = splash_process  # Pass the splash process to the context
        
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
    
# from ModuleUpdate import update
# update()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    run_client(*sys.argv[1:])