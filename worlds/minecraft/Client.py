import argparse
import json
import os
import sys
import re
import subprocess
import shutil
import atexit
from shutil import copyfile
from time import strftime
import logging

import requests

import Utils
from Utils import is_windows
from settings import get_settings

# 1 or more digits followed by m or g, then optional b
max_heap_re = re.compile(r"^\d+[mMgG][bB]?$")


def prompt_yes_no(prompt):
    yes_inputs = {'yes', 'ye', 'y'}
    no_inputs = {'no', 'n'}
    while True:
        choice = input(prompt + " [y/n] ").lower()
        if choice in yes_inputs: 
            return True
        elif choice in no_inputs:
            return False
        else:
            print('Please respond with "y" or "n".')


def find_ap_randomizer_jar(forge_dir):
    """Create mods folder if needed; find AP randomizer jar; return None if not found."""
    # Ensure the forge directory exists
    try:
        os.makedirs(forge_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating forge directory: {e}")
        return None
    
    mods_dir = os.path.join(forge_dir, 'mods')
    try:
        if os.path.isdir(mods_dir):
            for entry in os.scandir(mods_dir):
                if entry.name.startswith("aprandomizer") and entry.name.endswith(".jar"):
                    logging.info(f"Found AP randomizer mod: {entry.name}")
                    return entry.name
            return None
        else:
            os.makedirs(mods_dir, exist_ok=True)
            logging.info(f"Created mods folder in {forge_dir}")
            return None
    except Exception as e:
        print(f"Error handling mods directory: {e}")
        return None

def replace_apmc_files(forge_dir, apmc_file):
    """Create APData folder if needed; clean .apmc files from APData; copy given .apmc into directory."""
    if apmc_file is None:
        return
    
    # Ensure the forge directory exists
    try:
        os.makedirs(forge_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating forge directory: {e}")
        return
    
    apdata_dir = os.path.join(forge_dir, 'APData')
    copy_apmc = True
    
    try:
        if not os.path.isdir(apdata_dir):
            os.makedirs(apdata_dir, exist_ok=True)
            logging.info(f"Created APData folder in {forge_dir}")
        
        for entry in os.scandir(apdata_dir):
            if entry.name.endswith(".apmc") and entry.is_file():
                if not os.path.samefile(apmc_file, entry.path):
                    os.remove(entry.path)
                    logging.info(f"Removed {entry.name} in {apdata_dir}")
                else: # apmc already in apdata
                    copy_apmc = False
        
        if copy_apmc:
            copyfile(apmc_file, os.path.join(apdata_dir, os.path.basename(apmc_file)))
            logging.info(f"Copied {os.path.basename(apmc_file)} to {apdata_dir}")
            
    except Exception as e:
        print(f"Error handling APMC files: {e}")
        return

def read_apmc_file(apmc_file):
    from base64 import b64decode

    with open(apmc_file, 'r') as f:
        return json.loads(b64decode(f.read()))

def update_mod_simple(forge_dir, url: str):
    """Check mod version, download new mod from GitHub releases page if needed. """
    ap_randomizer = find_ap_randomizer_jar(forge_dir)
    os.path.basename(url)
    if ap_randomizer is not None:
        logging.info(f"Your current mod is {ap_randomizer}.")
    else:
        logging.info(f"You do not have the AP randomizer mod installed.")

    if ap_randomizer != os.path.basename(url):
        logging.info(f"A new release of the Minecraft AP randomizer mod was found: "
                     f"{os.path.basename(url)}")
        if show_yes_no_simple("Mod Update Available", f"A new release of the Minecraft AP randomizer mod was found:\n{os.path.basename(url)}\n\nWould you like to update?"):
            old_ap_mod = os.path.join(forge_dir, 'mods', ap_randomizer) if ap_randomizer is not None else None
            new_ap_mod = os.path.join(forge_dir, 'mods', os.path.basename(url))
            logging.info("Downloading AP randomizer mod. This may take a moment...")
            apmod_resp = requests.get(url)
            if apmod_resp.status_code == 200:
                with open(new_ap_mod, 'wb') as f:
                    f.write(apmod_resp.content)
                    logging.info(f"Wrote new mod file to {new_ap_mod}")
                if old_ap_mod is not None:
                    os.remove(old_ap_mod)
                    logging.info(f"Removed old mod file from {old_ap_mod}")
            else:
                logging.error(f"Error retrieving the randomizer mod (status code {apmod_resp.status_code}).")
                logging.error(f"Please report this issue on the MultiworldGG Discord server.")
                sys.exit(1)

def check_eula_simple(forge_dir):
    """Check if the EULA is agreed to, and prompt the user to read and agree if necessary."""
    # Ensure the forge directory exists
    try:
        os.makedirs(forge_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating forge directory: {e}")
        return
    
    eula_path = os.path.join(forge_dir, "eula.txt")
    if not os.path.isfile(eula_path):
        # Create eula.txt
        try:
            with open(eula_path, 'w') as f:
                f.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n")
                f.write(f"#{strftime('%a %b %d %X %Z %Y')}\n")
                f.write("eula=false\n")
            print(f"Created EULA file: {eula_path}")
        except Exception as e:
            print(f"Error creating EULA file: {e}")
            return
    
    try:
        with open(eula_path, 'r+') as f:
            text = f.read()
            if 'false' in text:
                # Prompt user to agree to the EULA
                if show_yes_no_simple("EULA Agreement", "Do you agree to the Minecraft EULA?\n\nBy clicking 'Yes', you agree to the terms at:\nhttps://account.mojang.com/documents/minecraft_eula"):
                    # Update eula.txt to set eula=true
                    f.seek(0)
                    f.write(text.replace('eula=false', 'eula=true'))
                    f.truncate()
                    logging.info("EULA agreed to.")
                else:
                    logging.error("EULA not agreed to. Cannot continue.")
                    sys.exit(1)
    except Exception as e:
        print(f"Error reading/updating EULA file: {e}")
        return

def find_jdk_dir(java_version):
    """Find the JDK directory for the specified Java version."""
    if is_windows:
        # Check common installation paths
        common_paths = [
            f"C:\\Program Files\\Java\\jdk-{java_version}",
            f"C:\\Program Files\\Eclipse Adoptium\\jdk-{java_version}",
            f"C:\\Program Files\\Microsoft\\jdk-{java_version}",
            f"C:\\Program Files\\OpenJDK\\jdk-{java_version}",
            f"C:\\Program Files\\Zulu\\zulu-{java_version}",
            f"C:\\Program Files\\Java\\jdk-{java_version}.0",
            f"C:\\Program Files\\Eclipse Adoptium\\jdk-{java_version}.0",
            f"C:\\Program Files\\Microsoft\\jdk-{java_version}.0",
            f"C:\\Program Files\\OpenJDK\\jdk-{java_version}.0",
            f"C:\\Program Files\\Zulu\\zulu-{java_version}.0",
        ]
        
        for path in common_paths:
            if os.path.isdir(path):
                return path
                
        # Also check current directory for extracted JDKs
        for entry in os.listdir():
            if os.path.isdir(entry) and entry.startswith(f"jdk{java_version}"):
                return os.path.abspath(entry)
                
        # Check if java is in PATH
        try:
            result = subprocess.run(["java", "-version"], capture_output=True, text=True)
            if result.returncode == 0:
                # Java is available, but we don't know the path
                return None
        except FileNotFoundError:
            pass
            
    return None

def find_jdk(java_version):
    """Get the java exe location"""
    if is_windows:
        # First try to find JDK in specific directory
        jdk = find_jdk_dir(java_version)
        if jdk is not None:
            jdk_exe = os.path.join(jdk, "bin", "java.exe")
            if os.path.isfile(jdk_exe):
                return jdk_exe
        
        # Fallback: try to find java in PATH
        try:
            result = subprocess.run(["java", "-version"], capture_output=True, text=True)
            if result.returncode == 0:
                # Java is available in PATH, try to find the executable
                java_exe = shutil.which("java")
                if java_exe:
                    return java_exe
        except FileNotFoundError:
            pass
            
        # If we get here, no Java found
        return None
    else:
        jdk_exe = shutil.which("java")
        if not jdk_exe:
            jdk_exe = shutil.which("java") # try to fall back to system java
            if not jdk_exe:
                raise Exception("Could not find Java. Is Java installed on the system?")
        return jdk_exe

def download_java(java_version):
    """Download and install Java for the specified version."""
    if not is_windows:
        print("Java download is only supported on Windows.")
        return
        
    print(f"Downloading Java {java_version}...")
    
    # Remove old JDK if it exists
    jdk = find_jdk_dir(java_version)
    if jdk is not None:
        print(f"Removing old JDK...")
        from shutil import rmtree
        rmtree(jdk)

    print(f"Downloading Java...")
    jdk_url = f"https://corretto.aws/downloads/latest/amazon-corretto-{java_version}-x64-windows-jdk.zip"
    resp = requests.get(jdk_url)
    if resp.status_code == 200: # OK
        print(f"Extracting Java (this may take a few minutes)...")
        
        # Show progress dialog
        show_progress_dialog("Java Installation", "Downloading and extracting Java...\nThis may take several minutes.\nPlease wait.")
        
        import zipfile
        from io import BytesIO
        
        # Show progress during extraction
        with zipfile.ZipFile(BytesIO(resp.content)) as zf:
            total_files = len(zf.namelist())
            print(f"Found {total_files} files to extract...")
            
            for i, file_info in enumerate(zf.infolist(), 1):
                if i % 100 == 0 or i == total_files: # Show progress every 100 files
                    print(f"Extracting... {i}/{total_files} files")
                zf.extract(file_info)
        
        print("Java extraction completed!")
    else:
        print(f"Error downloading Java (status code {resp.status_code}).")
        print(f"If this was not expected, please report this issue on the MultiworldGG Discord server.")
        if not show_yes_no_simple("Download Error", f"Error downloading Java (status code {resp.status_code}).\n\nContinue anyways?"):
            sys.exit(0)

def install_forge(forge_dir, forge_version, java_version):
    """Download and install Minecraft Forge for the specified version."""
    print(f"Installing Minecraft Forge {forge_version}...")
    
    # Create the forge directory if it doesn't exist
    try:
        os.makedirs(forge_dir, exist_ok=True)
        print(f"Created forge directory: {forge_dir}")
    except Exception as e:
        print(f"Error creating forge directory: {e}")
        return
    
    # Find Java executable
    java_exe = find_jdk(java_version)
    if java_exe is not None:
        print(f"Found Java at: {java_exe}")
        print(f"Downloading Forge {forge_version}...")
        print("Please wait while downloading the Forge installer...")
        forge_url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{forge_version}/forge-{forge_version}-installer.jar"
        resp = requests.get(forge_url)
        if resp.status_code == 200: # OK
            forge_install_jar = os.path.join(forge_dir, "forge_install.jar")
            with open(forge_install_jar, 'wb') as f:
                f.write(resp.content)
            print(f"Installing Forge (this may take several minutes)...")
            print("Please wait while Forge downloads and installs all required files...")
            
            # Show progress dialog
            show_progress_dialog("Forge Installation", "Installing Minecraft Forge...\nThis may take several minutes.\nPlease wait.")
            
            # Run the installer with progress indication
            install_process = subprocess.Popen(
                [java_exe, "-jar", forge_install_jar, "--installServer", forge_dir],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # Show progress while installer runs
            while True:
                output = install_process.stdout.readline()
                if output == '' and install_process.poll() is not None:
                    break
                if output:
                    # Filter out verbose output but show important progress
                    if any(keyword in output.lower() for keyword in ['downloading', 'installing', 'extracting', 'copying', 'creating']):
                        print(f"Forge installer: {output.strip()}")
            
            # Wait for completion and check result
            return_code = install_process.wait()
            if return_code == 0:
                print("Forge installation completed successfully!")
            else:
                print(f"Forge installation completed with return code: {return_code}")
            
            # Clean up installer
            os.remove(forge_install_jar)
        else:
            print(f"Error downloading Forge (status code {resp.status_code}).")
            print(f"If this was not expected, please report this issue on the MultiworldGG Discord server.")
            if not show_yes_no_simple("Download Error", f"Error downloading Forge (status code {resp.status_code}).\n\nContinue anyways?"):
                sys.exit(0)
    else:
        print(f"Java {java_version} not found, cannot install Forge.")
        print("Available Java installations:")
        # List what we found
        if is_windows:
            for entry in os.listdir():
                if os.path.isdir(entry) and entry.startswith("jdk"):
                    print(f"  - {entry}")
        
        if not show_yes_no_simple("Java Not Found", f"Java {java_version} not found, cannot install Forge.\n\nContinue anyways?"):
            sys.exit(0)

def run_forge_server(forge_dir, java_version, max_heap):
    """Run the Forge server with the specified parameters."""
    # Find the server jar
    server_jar = None
    for entry in os.scandir(forge_dir):
        if entry.name.endswith(".jar"):
            # Look for Forge server jar (could be named server.jar, forge-*-server.jar, or forge-*-shim.jar)
            if ("server" in entry.name.lower() or 
                "shim" in entry.name.lower() or 
                entry.name.startswith("forge-")):
                server_jar = entry.name  # Just the filename, not full path
                print(f"Using Forge server jar: {entry.name}")
                break
    
    if not server_jar:
        raise FileNotFoundError("Could not find Forge server jar in the forge directory.")
    
    # Build the command
    cmd = [
        "java",
        f"-Xmx{max_heap}",
        "-jar",
        server_jar,
        "nogui"
    ]
    
    # Set working directory
    env = os.environ.copy()
    env["JAVA_HOME"] = find_jdk_dir(java_version) or ""
    
    print(f"Starting Forge server with command: {' '.join(cmd)}")
    
    if is_windows:
        # On Windows, use 'start' command to open a new console window cleanly
        # This is much more reliable than subprocess.CREATE_NEW_CONSOLE
        start_cmd = f'start "Minecraft Forge Server" cmd /k "cd /d "{forge_dir}" && {" ".join(cmd)}"'
        
        # Use subprocess.run to execute the start command
        subprocess.run(start_cmd, shell=True, cwd=forge_dir, env=env)
        
        # Return a dummy process since we can't easily track the started process
        return None
    else:
        # On non-Windows, just run normally
        return subprocess.Popen(cmd, cwd=forge_dir, env=env)

def get_minecraft_versions(data_version, release_channel):
    """Get Minecraft version information from the versions file."""
    # Try to fetch the latest version info
    try:
        resp = requests.get("https://raw.githubusercontent.com/Seatori/Minecraft_AP_Randomizer/refs/heads/transfer-ownership/versions/minecraft_versions.json")
        if resp.status_code == 200:
            data = resp.json()
            local = False
        else:
            local = True
    except Exception:
        local = True

    if local:
        with open(Utils.user_path("minecraft_versions.json"), 'r') as f:
            data = json.load(f)
    else:
        with open(Utils.user_path("minecraft_versions.json"), 'w') as f:
            json.dump(data, f)

    try:
        if data_version:
            return next(filter(lambda entry: entry["version"] == data_version, data[release_channel]))
        else:
            return resp.json()[release_channel][0]
    except (StopIteration, KeyError):
        logging.error(f"No compatible mod version found for client version {data_version} on \"{release_channel}\" channel.")
        if release_channel != "release":
            logging.error("Consider switching \"release_channel\" to \"release\" in your Host.yaml file")
        else:
            logging.error("No suitable mod found on the \"release_channel\" channel. Please Contact us on discord to report this error.")
        sys.exit(0)

def is_correct_forge(forge_dir, forge_version) -> bool:
    if os.path.isdir(os.path.join(forge_dir, "libraries", "net", "minecraftforge", "forge", forge_version)):
        return True
    return False





def show_java_prompt_simple(java_version):
    """Show Java installation prompt using tkinter"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        result = messagebox.askyesno(
            "Java Installation Required",
            f"Java {java_version} was not found on your system.\n\n"
            "To continue, you need to install Java.\n\n"
            "Please:\n"
            "1. Click 'Yes' when you're ready to continue with the install\n"
            "2. Or click 'No' to cancel setup"
        )
        
        root.destroy()
        return result
        
    except ImportError:
        # Fallback to terminal if tkinter fails
        print(f"Java {java_version} not found. Please install Java from https://adoptium.net/")
        return True

def show_forge_prompt_simple(forge_dir, forge_version, java_version):
    """Show Forge installation prompt using tkinter"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        result = messagebox.askyesno(
            "Forge Installation Required",
            f"Minecraft Forge {forge_version} was not found on your system.\n\n"
            "To continue, you need to install Forge.\n\n"
            "Please:\n"
            "1. Click 'Yes' when you're ready to continue with the install.\n"
            "2. Or click 'No' to cancel setup"
        )
        
        root.destroy()
        return result
        
    except ImportError:
        # Fallback to terminal if tkinter fails
        print(f"Forge {forge_version} not found. Please install Forge from https://files.minecraftforge.net/")
        return True

def show_yes_no_simple(title, message):
    """Show a simple yes/no dialog using tkinter"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        result = messagebox.askyesno(title, message)
        
        root.destroy()
        return result
        
    except ImportError:
        # Fallback to terminal if tkinter fails
        print(f"{title}: {message}")
        return True

def show_progress_dialog(title, message):
    """Show a progress dialog with a message"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Show info dialog (non-blocking)
        messagebox.showinfo(title, message)
        
        root.destroy()
        
    except ImportError:
        # Fallback to terminal if tkinter fails
        print(f"{title}: {message}")

def open_file_dialog(title, file_types):
    """Open a file dialog using tkinter or fallback to command line"""
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        # Create a simple dialog
        root = tk.Tk()
        root.withdraw() # Hide the main window
        
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=file_types
        )
        root.destroy()
        return file_path if file_path else None
        
    except ImportError:
        # Fallback to command line if tkinter is not available
        print("=" * 60)
        print("FILE SELECTION REQUIRED")
        print("=" * 60)
        print(f"Please enter the path to your APMC file:")
        print("(or press Enter to skip)")
        print("=" * 60)
        
        try:
            user_input = input("APMC file path: ").strip()
            if user_input:
                return os.path.abspath(user_input)
            else:
                return None
        except EOFError:
            print("No input available. Skipping file selection.")
            return None

def run_simple_setup(args):
    """Run the setup process using simple dialogs"""
    print(f"Starting Minecraft setup with args: {args}")
    
    # Parse arguments
    if not args:
        # This is a continuation, skip argument parsing
        print("Continuing setup after installation")
        apmc_file = None
    else:
        apmc_file = os.path.abspath(args.apmc_file) if args.apmc_file else None
        print(f"APMC file: {apmc_file}")
    
    # If we're running in a new terminal (no launcher args), prompt for APMC file
    if not args and not apmc_file:
        print("Running in setup terminal - please select your APMC file.")
        apmc_file = open_file_dialog('Select APMC File', [('.apmc', 'APMC Files')])
    
    # Change to executable's working directory
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    
    options = get_settings().minecraft_options
    channel = args.channel or options.release_channel if args else options.release_channel
    apmc_data = None
    data_version = args.data_version or None if args else None
    
    if apmc_file is None and not (args and args.install):
        # Use simple file dialog instead of Kivy
        apmc_file = open_file_dialog('Select APMC File', [('.apmc', 'APMC Files')])
    
    if apmc_file is not None and data_version is None:
        apmc_data = read_apmc_file(apmc_file)
        data_version = apmc_data.get('client_version', '')
    
    versions = get_minecraft_versions(data_version, channel)
    
    forge_dir = options.forge_directory
    max_heap = options.max_heap_size
    forge_version = args.forge or versions["forge"] if args else versions["forge"]
    java_version = args.java or versions["java"] if args else versions["java"]
    mod_url = versions["url"]
    
    if args and args.install:
        if is_windows:
            print("Installing Java")
            download_java(java_version)
        if not is_correct_forge(forge_dir, forge_version):
            print("Installing Minecraft Forge")
            install_forge(forge_dir, forge_version, java_version)
        else:
            print("Correct Forge version already found, skipping install.")
        return
    
    if apmc_data is None and apmc_file:
        raise FileNotFoundError(f"APMC file does not exist or is inaccessible at the given location ({apmc_file})")
    
    # Now check Java and Forge requirements
    print("Checking Java installation...")
    java_dir = find_jdk_dir(java_version)
    if not java_dir:
        print("Java directory not found, showing prompt")
        if show_java_prompt_simple(java_version):
            print("Installing Java...")
            download_java(java_version)
            print("Java installation completed. Continuing setup...")
        else:
            print("Setup cancelled by user.")
            return
    
    print("Checking Forge installation...")
    if not is_correct_forge(forge_dir, forge_version):
        print("Forge not found, showing prompt")
        if show_forge_prompt_simple(forge_dir, forge_version, java_version):
            print("Installing Minecraft Forge...")
            install_forge(forge_dir, forge_version, java_version)
            print("Forge installation completed. Continuing setup...")
        else:
            print("Setup cancelled by user.")
            return
    
    # Check EULA
    check_eula_simple(forge_dir)
    
    # Update mod if needed
    update_mod_simple(forge_dir, mod_url)
    
    # Copy APMC file
    replace_apmc_files(forge_dir, apmc_file)
    
    # Launch the Forge server
    print("Launching Minecraft Forge Server...")
    try:
        # Check if we have a server jar
        server_jar = None
        for entry in os.scandir(forge_dir):
            if entry.name.endswith(".jar"):
                # Look for Forge server jar (could be named server.jar, forge-*-server.jar, or forge-*-shim.jar)
                if ("server" in entry.name.lower() or 
                    "shim" in entry.name.lower() or 
                    entry.name.startswith("forge-")):
                    server_jar = entry.path
                    print(f"Found Forge server jar: {entry.name}")
                    break
        
        if not server_jar:
            print("No Forge server jar found. The setup is complete, but you need to:")
            print("1. Download and install Forge manually from: https://files.minecraftforge.net/")
            print(f"2. Install it to: {forge_dir}")
            print("3. Run the server manually using: java -Xmx{max_heap} -jar <server_jar> nogui")
            return
        
        server_process = run_forge_server(forge_dir, java_version, max_heap)
        print("Minecraft Forge Server launched successfully!")
        
        if is_windows:
            print("The server is now running in a new console window.")
            print("You can connect to it in Minecraft at localhost")
            
            # Show a simple info dialog
            try:
                import tkinter as tk
                from tkinter import messagebox
                
                root = tk.Tk()
                root.withdraw()
                
                messagebox.showinfo(
                    "Minecraft Server Started",
                    "Minecraft Forge Server is now running!\n\n"
                    "Please open Minecraft via Forge 1.20.4 and connect to localhost.\n\n"
                    "The server console can be found in a separate terminal window.\n\n"
                    "You may close this prompt."
                )
                
                root.destroy()
            except ImportError:
                print("Server console window opened. Connect to localhost in Minecraft.")
        else:
            print("Server is running. Connect to localhost in Minecraft.")
        
    except Exception as e:
        print(f"Error launching Minecraft server: {e}")
        import traceback
        traceback.print_exc()

def main(*launcher_args: str):
    # Minecraft client is always called in Kivy mode
    print(f"Launcher args: {launcher_args}")
    print("Running in Kivy mode")
    
    # Run setup directly with tkinter prompts
    run_simple_setup(None)

# Handle direct script execution
if __name__ == "__main__":
    # If called directly, run the setup process
    if len(sys.argv) > 1:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("apmc_file", default=None, nargs='?', help="Path to a MultiworldGG Minecraft data file (.apmc)")
        parser.add_argument('--install', '-i', dest='install', default=False, action='store_true',
                            help="Download and install Java and the Forge server. Does not launch the client afterwards.")
        parser.add_argument('--release_channel', '-r', dest="channel", type=str, action='store',
                            help="Specify release channel to use.")
        parser.add_argument('--java', '-j', metavar='17', dest='java', type=str, default=False, action='store',
                            help="specify java version.")
        parser.add_argument('--forge', '-f', metavar='1.18.2-40.1.0', dest='forge', type=str, default=False, action='store',
                            help="specify forge version. (Minecraft Version-Forge Version)")
        parser.add_argument('--version', '-v', metavar='9', dest='data_version', type=int, action='store',
                            help="specify Mod data version to download.")
        
        args = parser.parse_args()
        run_simple_setup(args)
    else:
        # No arguments, run setup with file dialog
        run_simple_setup(None)
