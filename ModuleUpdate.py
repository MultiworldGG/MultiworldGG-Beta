import sys
import os
import subprocess
import multiprocessing
from multiprocessing import Process
import warnings
import json
import urllib.request
import shutil
import zipfile
import re
import shutil
import tempfile
import logging

logger = logging.getLogger("Update")

if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.DEBUG, format='%(message)s', stream=sys.stdout)

from pathlib import Path
from typing import List, Optional

from importlib import metadata, invalidate_caches

from BaseUtils import tuplize_version, Version
from APContainer import APWorldContainer, prepare_apworld_for_pip

def is_frozen() -> bool:
    return getattr(sys, 'frozen', False)

def is_windows() -> bool:
    return sys.platform in ("win32", "cygwin", "msys")

def is_macos() -> bool:
    return sys.platform == "darwin"

def is_linux() -> bool:
    return sys.platform.startswith("linux")

def install_path() -> Path:
    # Returns the path to the install directory for the python modules
    # Frozen builds only
    if is_windows():
        return Path.home() / "AppData" / "Local" / "MultiworldGG" / "mwgg_venv"
    elif is_macos():
        return Path.home() / "Library" / "Application Support" / "MultiworldGG" / "mwgg_venv"
    elif is_linux():
        return Path.home() / ".local" / "share" / "MultiworldGG" / "mwgg_venv"
    else:
        raise RuntimeError("Unsupported platform")

import pip

# Version compatibility checks
if (is_windows() or is_macos()) and sys.version_info < (3, 12, 0):
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. Official 3.12.+ is supported.")
elif (is_windows() or is_macos()) and sys.version_info < (3, 12, 7):
    warnings.warn(f"Python Version {sys.version_info} has security issues. Don't use in production.")
elif sys.version_info < (3, 12, 0):
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. 3.12.+ is supported.")

# Skip update if running in splash screen process
# Allow updates in main process and main client process
_skip_update = bool(
    multiprocessing.parent_process() and multiprocessing.current_process().name != "MultiWorldGG"
)

local_dir = Path(__file__).parent

update_ran = _skip_update
need_update: List[str] = []

class RequirementsSet(set):
    """Custom set that tracks whether updates have been run."""
    
    def add(self, e):
        global update_ran
        update_ran &= _skip_update
        super().add(e)

    def update(self, *s):
        global update_ran
        update_ran &= _skip_update
        super().update(*s)


# Initialize file sets

requirements_files = RequirementsSet({local_dir / "requirements.txt"})
worlds_files = {"wheels": RequirementsSet(), "apworlds": RequirementsSet()}

# Add wheel files if update hasn't run
if not update_ran:
    custom_worlds_dir = local_dir / "custom_worlds"
    if custom_worlds_dir.exists():
        for world_file in custom_worlds_dir.glob("*.whl"):
            worlds_files["wheels"].add(str(world_file))
        for world_file in custom_worlds_dir.glob("*.apworld"):
            worlds_files["apworlds"].add(str(world_file))

# Only for unfrozen builds, overriding for frozen            
python_cmd = sys.executable

if is_frozen():
    # For frozen builds, install in a home directory to prevent readonly issues
    exe_dir = Path(sys.exec_prefix)
    default_libs_dir = Path(exe_dir, "lib")
    worlds_install_dir = install_path()
    if str(worlds_install_dir) not in sys.path:
        sys.path.append(worlds_install_dir)
    if str(default_libs_dir) not in sys.path:
        sys.path.append(default_libs_dir)
        
    # set up frozen pip command
    if is_windows():
        # Try to use system Python first, fall back to local if not available
        if (install_path() / "Scripts" / "python.exe").exists():
            python_cmd = install_path() / "Scripts" / "python.exe"
        else:
            system_python = shutil.which("python")
            if system_python and "WindowsApps" not in system_python:
                pass
            else:
                system_py = shutil.which("py")
                py_output = subprocess.run([system_py, "-0p"], capture_output=True, text=True)
                system_python = py_output.stdout.strip()

                # Priority order: 3.12 → 3.13 → 3.11 → 3.10 → 3.9 → 3.8
                # Exclude venv paths and test versions (like python3.13t.exe)
                python_versions = []
                for line in py_output.stdout.splitlines():
                    if "venv" in line:
                        continue
                    if "python.exe" in line:
                        # Extract version and path - handle both formats:
                        # Format 1: "-V:3.12          C:\Program Files\Python312\python.exe"
                        # Format 2: "-V:3.13 *        C:\Users\Lindsay\AppData\Local\Programs\Python\Python313\python.exe"
                        parts = line.split()
                        if len(parts) >= 2:
                            version_part = parts[0]
                            # Handle the * marker in format 2
                            path = parts[-1] if parts[-1].endswith('.exe') else parts[1]
                            # Extract version number (e.g., "3.12" from "-V:3.12")
                            version_match = re.search(r'3\.(\d+)', version_part)
                            if version_match:
                                version_num = int(version_match.group(1))
                                if 10 <= version_num <= 14:  # Valid range
                                    python_versions.append((version_num, path))
                
                # Sort by priority: 3.12 first, then descending order
                def version_priority(item):
                    version_num = item[0]
                    if version_num == 12:
                        return 0  # Highest priority
                    else:
                        return 20 - version_num  # 3.13=7, 3.11=9, 3.10=10, 3.9=11, 3.8=12
                
                python_versions.sort(key=version_priority)
                if python_versions:
                    system_python = python_versions[0][1]
                if system_python and "WindowsApps" not in system_python:
                    pass
                else:
                    raise RuntimeError("No Python found")

            # Install windows venv
            venv_path = install_path()
            venv_path.mkdir(parents=True, exist_ok=True)
            subprocess.run([system_python, "-m", "venv", str(venv_path)], check=True)
            python_cmd = venv_path / "Scripts" / "python.exe"

    elif is_macos() or is_linux():
        # Create a venv in cache_path that uses the AppImage's python as base
        venv_path = install_path()
        if (venv_path / "bin" / "python").exists():
            python_cmd = venv_path / "bin" / "python"
        else:
            logger.info(f"Creating venv in {str(venv_path)}")
            system_python = shutil.which("python")
            if not system_python:
                system_python = shutil.which("python3")
            else:
                raise RuntimeError("No Python found")
            subprocess.run([system_python, "-m", "venv", str(venv_path)], check=True)
            python_cmd = venv_path / "bin" / "python"
    else:
        raise RuntimeError("Unsupported platform")

def check_pip() -> None:
    """Verify pip is available."""
    try:
        import pip  # noqa: F401
    except ImportError:
        #TODO: Fallback here - run it. https://bootstrap.pypa.io/get-pip.py
        raise RuntimeError("pip not available. Please install pip.")


def confirm(msg: str) -> None:
    """Get user confirmation for an action."""
    try:
        input(f"\n{msg}")
    except KeyboardInterrupt:
        logger.info("\nAborting")
        sys.exit(1)


def parse_requirements_file(file_path: Path) -> List[str]:
    """
    Parse a requirements.txt file and return a list of requirement strings.
    Handles line continuations, comments, and various requirement formats.
    """
    requirements = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    prev_line = ""
    
    for line in lines:
        line = line.rstrip('\r\n')
        
        # Handle line continuations
        if line.endswith('\\'):
            prev_line += line[:-1] + " "
            continue
        
        line = prev_line + line
        prev_line = ""
        
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith('#'):
            continue
        
        # Remove hash specifications for version checking
        line = line.split("--hash=")[0].strip()
        
        # Handle URL-based requirements
        if line.startswith(("https://", "git+https://")):
            line = _parse_url_requirement(line)
        
        # Handle custom PEP 508 syntax
        elif "@" in line and "#" in line:
            line = _parse_custom_pep508_requirement(line)
        
        if line.strip():
            requirements.append(line.strip())
    
    return requirements


def _parse_url_requirement(line: str) -> str:
    """Parse URL-based requirements and extract package name and version."""
    rest = line.split('/')[-1]
    
    # Extract from filename
    if "@" in rest:
        raise ValueError("Can't deduce version from requirement")
    
    rest = rest.replace(".zip", "-").replace(".tar.gz", "-")
    try:
        name, version, _ = rest.split("-", 2)
        return f'{name}=={version}'
    except ValueError:
        return ""


def _parse_custom_pep508_requirement(line: str) -> str:
    """Parse custom PEP 508 syntax: name @ url#version ; marker."""
    name, rest = line.split("@", 1)
    version = rest.split("#", 1)[1].split(";", 1)[0].rstrip()
    result = f"{name.rstrip()}=={version}"
    
    if ";" in rest:  # keep marker
        result += rest[rest.find(";"):]
    
    return result


def check_for_updates(worlds_only: bool = False) -> List[str]:
    """
    Check which packages need updates by querying PyPI.
    Returns a list of package names that need updating.
    """
    if is_frozen() and not worlds_only:
        return []
    # Ensure packaging is available
    try:
        import packaging.requirements
    except ImportError:
        logger.warning("packaging module not available, installing...")
        executable_args = [python_cmd, "-m", "pip", "install", "--upgrade", "packaging"]
        subprocess.run(executable_args)
        import packaging.requirements
    
    try:
        if worlds_only:
            executable_args = [python_cmd, "-m", "pip", "list", "-o", "--format", "json", 
                "-i", "https://pypi.multiworld.gg/mwgg/apworlds/+simple"]
        else:
            executable_args = [python_cmd, "-m", "pip", "list", "-o", "--format", "json", 
                "-i", "https://pypi.org/simple", "--extra-index-url", "https://pypi.multiworld.gg/mwgg/apworlds/+simple"]
        
        logger.info(f"Executing subprocess command: {executable_args}")
        logger.info(f"Working directory: {os.getcwd()}")
        response = subprocess.run(executable_args, capture_output=True, text=True, timeout=45)
        if response.returncode != 0:
            logger.warning(f"Could not check for updates: {response.stderr}")
            return []
        
        outdated_packages = json.loads(response.stdout)
        logger.info(f"Newer versions of the following packages are available: {outdated_packages}")
        
        if worlds_only:
            return [world["name"] for world in outdated_packages]

        # Get all requirements to check version constraints
        all_requirements = {}
        for req_file in requirements_files:
            if req_file.exists():
                requirements = parse_requirements_file(req_file)
                for req_line in requirements:
                    try:
                        requirement = packaging.requirements.Requirement(req_line)
                        all_requirements[requirement.name] = requirement
                    except packaging.requirements.InvalidRequirement:
                        continue
        
        # Filter outdated packages based on requirements.txt constraints
        packages_to_update = []
        for pkg in outdated_packages:
            pkg_name = pkg["name"]
            latest_version = pkg["latest_version"]
            
            # If package is in requirements.txt, check if update is allowed
            if pkg_name in all_requirements:
                requirement = all_requirements[pkg_name]
                
                # Check if the latest version satisfies the requirement constraint
                try:
                    # If the requirement has no version specifier, we can update
                    if not requirement.specifier:
                        packages_to_update.append(pkg_name)
                    else:
                        # Check if the latest version satisfies the current requirement
                        from packaging.version import parse as parse_version
                        latest_ver = parse_version(latest_version)
                        
                        # Test if the latest version satisfies the requirement
                        if latest_ver in requirement.specifier:
                            packages_to_update.append(pkg_name)
                        else:
                            logger.debug(f"Skipping {pkg_name}: latest version {latest_version} doesn't satisfy requirement {requirement}")
                except Exception as e:
                    # If we can't parse the version, skip it
                    logger.debug(f"Skipping {pkg_name}: couldn't check version constraint: {e}")
            else:
                # Package not in requirements.txt, so we can update it
                packages_to_update.append(pkg_name)
        
        return packages_to_update
    
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        logger.warning(f"Could not check for updates: {e}")
        return []

def uninstall_worlds(worlds: List[str]) -> None:
    """Uninstall a list of mwgg packages from the multiworld repository."""
    for world in worlds:
        executable_args = [python_cmd, "-m", "pip", "uninstall", world, "--yes"]
        subprocess.run(executable_args)


def find_world_modules() -> List[str]:
    """Find all world modules in the multiworld repository and currently installed packages."""
    world_modules = []
    
    # First, fetch from the repository
    try:
        # Fetch the simple index page from the multiworld PyPI repository
        url = "https://pypi.multiworld.gg/mwgg/apworlds/+simple"
        
        # Set up request with timeout
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'MultiWorldGG/1.0')
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html_content = response.read().decode('utf-8')
        
        # Parse the HTML to extract package names
        # The simple index format is: <a href="package_name/">package_name</a>
        import re
        package_pattern = r'<a href="([^/"]+)/">\1</a>'
        packages = re.findall(package_pattern, html_content)
        
        # Filter for world packages and strip the "worlds-" prefix
        for package in packages:
            if package.startswith("worlds-"):
                world_modules.append(package[7:])  # Remove "worlds-" prefix
        
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        logger.warning(f"Failed to fetch world modules from {url}: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error while fetching world modules: {e}")
    
    # Convert to set for efficient lookup
    world_modules_set = set(world_modules)
    
    from mwgg_igdb import GAMES_DATA, GameIndex
    game_modules = set(GAMES_DATA.keys())
    from BaseUtils import get_archipelago_json
    for world_module in world_modules:
        # remove pypi packages that are not in the game index - these are filtered out by rating
        if world_module not in game_modules:
            world_modules_set.remove(world_module)

    # Also check for currently installed world modules
    try:
        executable_args = [python_cmd, "-m", "pip", "list", "--format", "json"]
        logger.debug(f"Executing subprocess command to find installed worlds: {executable_args}")
        response = subprocess.run(executable_args, capture_output=True, text=True, timeout=45)
        
        if response.returncode == 0:
            installed_packages = json.loads(response.stdout)
            
            # Filter for world packages and add any that aren't already in the list
            for package in installed_packages:
                package_name = package.get("name", "")
                if package_name.startswith("worlds."):
                    world_name = package_name[7:]  # Remove "worlds." prefix
                    if world_name not in world_modules_set:
                        game_name, authors, minimum_ap_version, version = get_archipelago_json(world_name)
                        GameIndex.add_game(world_name, {"game_name": game_name, "cover_url": "", "age_rating": "NR"})
                        world_modules.append(world_name)
                        world_modules_set.add(world_name)
        else:
            logger.warning(f"Could not list installed packages: {response.stderr}")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        logger.warning(f"Could not check installed world modules: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error while checking installed world modules: {e}")
    

    return world_modules

def _parse_package_name_version(filename: str) -> tuple[str, str]:
    """
    TODO: Change to pip show command
    """
    # Remove common suffixes
    name = filename.replace('.dist-info', '').replace('.egg-info', '')
    
    # Split on last hyphen followed by a digit (version separator)
    match = re.match(r'^(.+?)-(\d+.*)$', name)
    if match:
        return match.group(1), match.group(2)
    return name, ''

def install_worlds(worlds: List[str], update: bool = False, no_recurse: bool = False) -> bool:
    """
    Install worlds from the multiworld repository.
    
    This will install worlds from the multiworld repository. It will also check for additional
    updates after installation completes.

    If additional updates are found, the restart flag will be set to True.
    
    Args:
        worlds: List of world packages to install
        update: If True, uninstall old versions first
        no_recurse: If True, do not check for additional updates after installation completes.
    
    Returns:
        True if additional updates were found, False otherwise.
    """
    check_pip()

    if update:
        logger.info(f"Uninstalling old versions of: {worlds}")
        uninstall_worlds(worlds)

    for idx, world in enumerate(worlds):
        
        if update:
            logger.info(f"Updating world: {world}")
        else:
            logger.info(f"Installing world: {world}")
        
        if is_frozen():
            # In frozen environments, we need to install to a location that's in the Python path
            # and ensure we use the correct target directory
            
            executable_args = [python_cmd, "-m", "pip", "install", "--no-deps", "--index-url", "https://pypi.org/simple",
                    "--extra-index-url", "https://pypi.multiworld.gg/mwgg/apworlds", 
                    world, "--prefer-binary", "--upgrade", "--no-cache-dir"]
            
            logger.info(f"Executing subprocess command: {executable_args}")
            
            # Use threading instead of multiprocessing to avoid argument contamination
            import threading
            import queue
            
            result_queue = queue.Queue()
            
            def _pip_install_thread():
                try:
                    result = subprocess.run(executable_args, capture_output=True, text=True)
                    result_queue.put((result.returncode, result.stdout, result.stderr))
                except Exception as e:
                    result_queue.put((1, "", str(e)))
            
            install_thread = threading.Thread(target=_pip_install_thread, daemon=True)
            install_thread.start()
            install_thread.join()
            
            # Get the return values from the worker thread
            try:
                returncode, stdout, stderr = result_queue.get_nowait()
                logger.info(stdout)
            except:
                returncode = 1  # Assume failure if we can't get the result
                stdout = ""
                stderr = "Failed to get process result"
            
            if returncode != 0:
                logger.warning(f"Failed to install {world} into {worlds_install_dir}")
                if stderr:
                    logger.error(f"{stderr}")
            else:
                # Before moving files, process all installed packages
                logger.debug(f"Processing downloaded packages...")

        else:
            executable_args = [python_cmd, "-m", "pip", "install", 
                    "--extra-index-url", "https://pypi.multiworld.gg/mwgg/apworlds", 
                    world, "--prefer-binary", "--upgrade", "--no-cache-dir"]
            result = subprocess.run(executable_args)
            if result.returncode != 0:
                logger.warning(f"Failed to install {world}")
            else:
                logger.info(f"Successfully installed {world}")
    
    invalidate_caches()
    if no_recurse:
        # We've already run through the deps once, so restart instead and run again.
        return True
    if is_frozen():
        # Check for any additional updates that might be needed
        logger.info("Checking for additional dependencies...")
        additional_deps_args = [python_cmd, "-m", "pip", "check"]
        additional_deps_result = subprocess.run(additional_deps_args, capture_output=True, text=True)
        stdout = additional_deps_result.stdout
        
        no_deps = ("No broken requirements found." in stdout)
        if no_deps:
            logger.info(f"Updates complete.")
            return False
        
        # Parse dependencies from pip check output
        # Handles: "pyramid 1.5.2 requires WebOb, which is not installed."
        # Handles: "pyramid 1.5.2 has requirement WebOb>=1.3.1, but you have WebOb 0.8."

        else:
            packages_to_install = []
            for line in stdout.splitlines():
                match = re.search(r'(?:requires|has requirement)\s+([a-zA-Z0-9_-]+)([><=!.0-9]+)?', line)
                if match:
                    package = match.group(1)
                    version_req = match.group(2) if match.group(2) else ""
                    install_spec = f"{package}{version_req}"
                    packages_to_install.append(install_spec)
            return install_worlds(packages_to_install, update=True, no_recurse=True)
    
    return False

def install_apworld_via_pip(apworld_path: Path, manifest: dict[str, object]) -> bool:
    """
    Install apworld via pip using Direct URL syntax.
    
    Args:
        apworld_path: Path to the .apworld file
        
    Returns:
        True if installation succeeded, False otherwise
    """
    module_name = apworld_path.stem
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Prepare apworld for pip
        installable_zip = prepare_apworld_for_pip(apworld_path, temp_path, manifest)
        if not installable_zip:
            return False
        
        # Install via pip using Direct URL syntax
        # Format: worlds.{module_name} @ file://{absolute_path}
        absolute_path = installable_zip.resolve()
        if is_windows():
            # Windows file:// URLs need forward slashes
            file_url = f"file:///{absolute_path.as_posix()}"
        else:
            file_url = f"file://{absolute_path}"
        
        pip_spec = f"worlds.{module_name} @ {file_url}"
        
        executable_args = [python_cmd, "-m", "pip", "install", pip_spec, 
                          "--no-deps", "--upgrade", "--no-cache-dir"]
        
        if is_frozen():
            # Use threading for frozen builds
            import threading
            import queue
            
            result_queue = queue.Queue()
            
            def _pip_install_thread():
                try:
                    result = subprocess.run(executable_args, capture_output=True, text=True)
                    result_queue.put((result.returncode, result.stdout, result.stderr))
                except Exception as e:
                    result_queue.put((1, "", str(e)))
            
            install_thread = threading.Thread(target=_pip_install_thread, daemon=True)
            install_thread.start()
            install_thread.join()
            
            try:
                returncode, stdout, stderr = result_queue.get_nowait()
                logger.info(stdout)
                if stderr:
                    logger.debug(stderr)
            except:
                returncode = 1
                stderr = "Failed to get process result"
        else:
            result = subprocess.run(executable_args, capture_output=True, text=True)
            returncode = result.returncode
            stdout = result.stdout
            stderr = result.stderr
        
        if returncode != 0:
            logger.warning(f"Failed to install {module_name} via pip: {stderr}")
            return False
        
        logger.info(f"Successfully installed {module_name} via pip")
        return True


def update_world_from_package() -> None:
    """Install/update wheel files from custom_worlds directory."""
    check_pip()
    # Use threading version if frozen, otherwise use subprocess
    if is_frozen():
        for world in worlds_files["wheels"]:
            logger.info(f"Installing wheel: {world}")
            executable_args = [python_cmd, "-m", "pip", "install", world, "--upgrade", 
                    "--prefer-binary", "--no-cache-dir"]
            
            # Use threading instead of multiprocessing to avoid argument contamination
            import threading
            import queue
            
            result_queue = queue.Queue()
            
            def _pip_install_thread():
                try:
                    result = subprocess.run(executable_args, capture_output=True, text=True)
                    result_queue.put((result.returncode, result.stdout, result.stderr))
                except Exception as e:
                    result_queue.put((1, "", str(e)))
            
            install_thread = threading.Thread(target=_pip_install_thread, daemon=True)
            install_thread.start()
            install_thread.join()
            
            # Get the return values from the worker thread
            try:
                returncode, stdout, stderr = result_queue.get_nowait()
                logger.info(stdout)
            except:
                returncode = 1  # Assume failure if we can't get the result
                stdout = ""
                stderr = "Failed to get process result"
            
            if returncode != 0:
                logger.warning(f"Failed to install wheel {wheel}")
                if stderr:
                    logger.error(f"{stderr}")
            else:
                logger.info(f"Successfully installed wheel {wheel}")

        for world in worlds_files["apworlds"]:
            logger.info(f"Installing APworld: {world}")
            try:
                # Extract module name from apworld filename (e.g., "world_name.apworld" -> "world_name")
                world_path = Path(world)
                module_name = world_path.stem  # Gets filename without extension
                
                # Read version from the apworld zip file using APWorldContainer
                new_version: Optional[Version] = None
                manifest: dict[str, object] = {}
                try:
                    apworld_container = APWorldContainer(world)
                    # Set manifest path to expected location
                    with zipfile.ZipFile(world, 'r') as apworld_zip:
                        manifest = apworld_container.read_contents(apworld_zip)
                    if "world_version" in manifest:
                        new_version = tuplize_version(manifest["world_version"])
                        logger.info(f"APworld {world} has version {new_version}")
                    else:
                        logger.info(f"APworld {world} has no world_version specified")
                    logger.info(f"APworld {world} has version {new_version}")
                except Exception as e:
                    logger.warning(f"Failed to read version from APworld {world}: {e}")
                
                # Check if world is already installed in worlds_install_dir
                # All worlds are installed to lib/site-packages/worlds (lowercase on Linux/macOS, uppercase on Windows)
                lib_dir = "Lib" if is_windows() else "lib"
                installed_world_path = worlds_install_dir / lib_dir / "site-packages" / "worlds" / module_name
                installed_version: Optional[Version] = None
                should_install = True
                
                if installed_world_path.exists():
                    installed_json_path = installed_world_path / "archipelago.json"
                    if installed_json_path.exists():
                        try:
                            with open(installed_json_path, 'r', encoding='utf-8') as f:
                                installed_manifest = json.load(f)
                                if "world_version" in installed_manifest:
                                    installed_version = tuplize_version(installed_manifest["world_version"])
                                    logger.info(f"Installed world {module_name} has version {installed_manifest['world_version']}")
                                else:
                                    logger.info(f"Installed world {module_name} has no world_version specified")
                        except Exception as e:
                            logger.warning(f"Failed to read version from installed world {module_name}: {e}")
                    
                    # Compare versions: install if new_version > installed_version
                    # According to spec: "An APWorld without a world_version is always treated as older than one with a version"
                    if new_version is not None and installed_version is not None:
                        if new_version > installed_version:
                            logger.info(f"New version {new_version.as_simple_string()} is higher than installed {installed_version.as_simple_string()}, will install")
                            should_install = True
                        else:
                            logger.info(f"Installed version {installed_version.as_simple_string()} is >= new version {new_version.as_simple_string()}, skipping")
                            should_install = False
                    elif new_version is not None and installed_version is None:
                        # New has version, installed doesn't - install
                        logger.info(f"New APworld has version {new_version.as_simple_string()}, installed has none, will install")
                        should_install = True
                    elif new_version is None and installed_version is not None:
                        # Installed has version, new doesn't - don't install
                        logger.info(f"Installed has version {installed_version.as_simple_string()}, new APworld has none, skipping")
                        should_install = False
                    else:
                        # Both have no version - install to update
                        logger.info(f"Neither version specified, will install to update")
                        should_install = True
                
                if not should_install:
                    logger.info(f"Skipping installation of APworld {world} (version check)")
                    continue
                
                # Install via pip (restructures apworld and installs properly)
                if install_apworld_via_pip(world_path, manifest):
                    logger.info(f"Successfully installed APworld {world} via pip")
                else:
                    # Fallback to direct extraction if pip fails
                    logger.warning(f"Pip installation failed, falling back to direct extraction for {world}")
                    lib_dir = "Lib" if is_windows() else "lib"
                    worlds_target_dir = worlds_install_dir / lib_dir / "site-packages" / "worlds"
                    worlds_target_dir.mkdir(parents=True, exist_ok=True)
                    with zipfile.ZipFile(world, 'r') as unzipped_world:
                        unzipped_world.extractall(worlds_target_dir)
                    logger.info(f"Installed APworld {world} via direct extraction")
            except Exception as e:
                logger.warning(f"Failed to install APworld {world}: {e}")
    else:
        for wheel in worlds_files["wheels"]:
            logger.info(f"Installing wheel: {wheel}")
            executable_args = [python_cmd, "-m", "pip", "install", wheel, "--upgrade"]
            result = subprocess.run(executable_args)
            if result.returncode != 0:
                logger.warning(f"Failed to install wheel {wheel}")
            else:
                logger.info(f"Successfully installed wheel {wheel}")


def update_requirements(needed_packages: List[str]) -> None:
    """
    Update packages from requirements.txt files and install worlds.
    
    Args:
        needed_packages: List of packages that need updating
    """
    if is_frozen():
        return
    check_pip()
    # Ensure packaging is available
    try:
        import packaging.requirements
    except ImportError:
        logger.warning("packaging module not available, installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "packaging"])
        import packaging.requirements
    
    # If needed_packages is empty, update all requirements (for force mode or missing requirements)
    update_all = len(needed_packages) == 0
    
    # Handle regular requirements from files
    for req_file in requirements_files:
        if not req_file.exists():
            logger.warning(f"Requirements file not found: {req_file}")
            continue
            
        logger.debug(f"Processing requirements from: {req_file}")
        requirements = parse_requirements_file(req_file)
        
        packages_to_update = []
        for req_line in requirements:
            try:
                requirement = packaging.requirements.Requirement(req_line)
                # Update if: force mode, package needs update, or package is missing
                if update_all or requirement.name in needed_packages:
                    packages_to_update.append(req_line)
            except packaging.requirements.InvalidRequirement:
                logger.warning(f"Invalid requirement line: {req_line}")
                continue
        
        if packages_to_update:
            logger.info(f"Installing/updating packages: {[req.split('==')[0] if '==' in req else req.split('>=')[0] if '>=' in req else req for req in packages_to_update]}")
            for package in packages_to_update:
                executable_args = [python_cmd, "-m", "pip", "install", "--upgrade", package]
                result = subprocess.run(executable_args)
                if result.returncode != 0:
                    logger.warning(f"Failed to install/update {package}")
        else:
            logger.info("No packages from this requirements file need updating.")
    
    # Handle worlds (these are not in requirements.txt files)
    worlds_to_install = [pkg for pkg in needed_packages if pkg.startswith("worlds") or pkg.startswith("mwgg")]
    if worlds_to_install:
        logger.info(f"Installing/updating worlds: {worlds_to_install}")
        install_worlds(worlds_to_install)


def install_packaging(yes: bool = False) -> None:
    """Install packaging module if not available."""
    if is_frozen():
        return
    try:
        import packaging.requirements  # noqa: F401
    except ImportError:
        check_pip()
        if not yes:
            confirm("packaging not found, press enter to install it")
        executable_args = [python_cmd, "-m", "pip", "install", "--upgrade", "packaging"]
        subprocess.run(executable_args)


def check_requirements_satisfied(yes: bool = False) -> bool:
    """
    Check if all requirements are satisfied.
    Returns True if all requirements are met, False otherwise.
    """
    if is_frozen():
        return True
    install_packaging(yes=yes)
    
    try:
        import packaging.requirements
        import importlib.metadata
    except ImportError:
        return False
    
    all_satisfied = True
    
    for req_file in requirements_files:
        if not req_file.exists():
            logger.warning(f"Requirements file not found: {req_file}")
            continue
        
        requirements = parse_requirements_file(req_file)
        
        for req_line in requirements:
            try:
                requirement = packaging.requirements.Requirement(req_line)
                try:
                    importlib.metadata.distribution(requirement.name)
                except importlib.metadata.PackageNotFoundError:
                    logger.warning(f"Missing requirement: {requirement.name}")
                    all_satisfied = False
                    if not yes:
                        confirm(f"Requirement {requirement.name} is not satisfied, press enter to install it")
            except packaging.requirements.InvalidRequirement:
                logger.warning(f"Invalid requirement line: {req_line}")
                continue
    
    return all_satisfied


def update(yes: bool = True, force: bool = False, worlds: Optional[List[str]] = None) -> None:
    """
    Main update function.
    
    Args:
        yes: Answer yes to all prompts
        force: Force update without checking
        worlds: List of specific worlds to update
    
    Returns:
        None
    """
    if is_frozen():
        if (exe_dir / "custom_wheels").exists():
            logger.debug("Custom Worlds found, checking...")
            update_world_from_package()
        updates = check_for_updates(worlds_only=True)
        if updates:
            restart_needed = install_worlds(updates)
            if restart_needed:
                # Library updates were staged, need to restart
                from Utils import exit_restart_for_update
                exit_restart_for_update()
        else:
            logger.debug("No updates found.")
    global update_ran
    
    if update_ran:
        return
    
    update_ran = True
    
    if force:
        logger.debug("Force update requested - skipping update checks")
        # Force mode updates all requirements and worlds
        update_requirements([])  # Empty list means update all
    
    # Check for available updates
    logger.debug("Checking for available updates...")
    available_updates = check_for_updates()
    
    if available_updates:
        logger.debug(f"Found updates for: {available_updates}")
        if not yes:
            confirm("Updates available. Press enter to continue with updates.")
    else:
        logger.debug("No updates found.")
    
    # Check if requirements are satisfied
    logger.debug("Checking if all requirements are satisfied...")
    if not check_requirements_satisfied(yes=yes):
        logger.debug("Installing missing requirements...")
        update_requirements([])  # Empty list means update all missing requirements
    
    # Update packages that need updates (including worlds)
    if available_updates:
        logger.debug("Updating packages that need updates...")
        update_requirements(available_updates)
    
    logger.debug("Update process completed.")


class RestartException(Exception):
    """Exception raised when a restart is needed."""
    pass

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Install archipelago requirements')
    parser.add_argument('-y', '--yes', dest='yes', action='store_true', 
                       help='answer "yes" to all questions')
    parser.add_argument('-f', '--force', dest='force', action='store_true', 
                       help='force update')
    parser.add_argument('-a', '--append', nargs="*", dest='additional_requirements',
                       help='List paths to additional requirement files.')
    parser.add_argument('-w', '--worlds', nargs="*", dest='worlds',
                       help='List of worlds to update.')
    
    args = parser.parse_args()
    
    if args.additional_requirements:
        requirements_files.update([Path(req) for req in args.additional_requirements])
    
    if args.worlds:
        update(args.yes, args.force, args.worlds)
    else:
        update(args.yes, args.force)
