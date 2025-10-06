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
import logging
logger = logging.getLogger("MultiWorld")

if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.DEBUG, format='%(message)s', stream=sys.stdout)

from pathlib import Path
from typing import List, Optional

import pip
from importlib import metadata

def is_frozen() -> bool:
    return getattr(sys, 'frozen', False)

def is_windows() -> bool:
    return sys.platform in ("win32", "cygwin", "msys")

def is_macos() -> bool:
    return sys.platform == "darwin"

def is_linux() -> bool:
    return sys.platform.startswith("linux")

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
wheels_files = RequirementsSet()

# Add wheel files if update hasn't run
if not update_ran:
    custom_wheels_dir = local_dir / "custom_wheels"
    if custom_wheels_dir.exists():
        for wheel_file in custom_wheels_dir.glob("*.whl"):
            wheels_files.add(str(wheel_file))
            
python_cmd = sys.executable
if is_frozen():
    # For frozen builds, install adjacent to the executable
    exe_dir = Path(sys.exec_prefix)
    pip_install_dir = exe_dir / "worlds_wheels"
    worlds_install_dir = exe_dir / "lib"
    # set up frozen pip command
    if is_windows():
        # Try to use system Python first, fall back to local if not available
        import shutil
        system_python = shutil.which("python")
        if system_python and "WindowsApps" not in system_python:
            python_cmd = system_python
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
                            if 8 <= version_num <= 13:  # Valid range
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
                python_cmd = system_python
            else:
                raise RuntimeError("No Python found")
        path = os.environ.get("PATH")
        if "python" not in path.lower() and str(worlds_install_dir) not in path:
            os.environ["PATH"] = str(worlds_install_dir) + ";" + path

    elif is_macos() or is_linux():
        os.symlink("python3", exe_dir / "python3")
        python_cmd = Path(exe_dir) / "python3"
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
    
    # Debug environment information
    logger.info("=== ENVIRONMENT DEBUG INFO ===")
    logger.info(f"is_frozen(): {is_frozen()}")
    logger.info(f"python_cmd: {python_cmd}")
    logger.info(f"sys.executable: {sys.executable}")
    logger.info(f"sys.exec_prefix: {sys.exec_prefix}")
    logger.info(f"sys.prefix: {sys.prefix}")
    logger.info(f"sys.path: {sys.path}")
    logger.info(f"PYTHONHOME: {os.environ.get('PYTHONHOME', 'Not set')}")
    logger.info(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
    logger.info(f"PYTHONSTARTUP: {os.environ.get('PYTHONSTARTUP', 'Not set')}")
    logger.info(f"PYTHONPLATLIBDIR: {os.environ.get('PYTHONPLATLIBDIR', 'Not set')}")
    logger.info(f"PYTHONCASEOK: {os.environ.get('PYTHONCASEOK', 'Not set')}")
    logger.info(f"PYTHONIOENCODING: {os.environ.get('PYTHONIOENCODING', 'Not set')}")
    logger.info(f"PYTHONHASHSEED: {os.environ.get('PYTHONHASHSEED', 'Not set')}")
    logger.info(f"PYTHONMALLOC: {os.environ.get('PYTHONMALLOC', 'Not set')}")
    logger.info(f"PYTHONCOERCECLOCALE: {os.environ.get('PYTHONCOERCECLOCALE', 'Not set')}")
    logger.info(f"PYTHONBREAKPOINT: {os.environ.get('PYTHONBREAKPOINT', 'Not set')}")
    logger.info(f"PYTHON_COLORS: {os.environ.get('PYTHON_COLORS', 'Not set')}")
    logger.info(f"PYTHON_HISTORY: {os.environ.get('PYTHON_HISTORY', 'Not set')}")
    logger.info(f"PYTHON_CPU_COUNT: {os.environ.get('PYTHON_CPU_COUNT', 'Not set')}")
    logger.info(f"PYTHONDEBUG: {os.environ.get('PYTHONDEBUG', 'Not set')}")
    logger.info(f"PYTHONDEVMODE: {os.environ.get('PYTHONDEVMODE', 'Not set')}")
    logger.info(f"PYTHONDONTWRITEBYTECODE: {os.environ.get('PYTHONDONTWRITEBYTECODE', 'Not set')}")
    logger.info(f"PYTHONFAULTHANDLER: {os.environ.get('PYTHONFAULTHANDLER', 'Not set')}")
    logger.info(f"PYTHON_FROZEN_MODULES: {os.environ.get('PYTHON_FROZEN_MODULES', 'Not set')}")
    logger.info(f"PYTHON_GIL: {os.environ.get('PYTHON_GIL', 'Not set')}")
    logger.info(f"PYTHONINSPECT: {os.environ.get('PYTHONINSPECT', 'Not set')}")
    logger.info(f"PYTHONINTMAXSTRDIGITS: {os.environ.get('PYTHONINTMAXSTRDIGITS', 'Not set')}")
    logger.info(f"PYTHONNODEBUGRANGES: {os.environ.get('PYTHONNODEBUGRANGES', 'Not set')}")
    logger.info(f"PYTHONNOUSERSITE: {os.environ.get('PYTHONNOUSERSITE', 'Not set')}")
    logger.info(f"PYTHONOPTIMIZE: {os.environ.get('PYTHONOPTIMIZE', 'Not set')}")
    logger.info(f"PYTHONPERFSUPPORT: {os.environ.get('PYTHONPERFSUPPORT', 'Not set')}")
    logger.info(f"PYTHONPROFILEIMPORTTIME: {os.environ.get('PYTHONPROFILEIMPORTTIME', 'Not set')}")
    logger.info(f"PYTHONPYCACHEPREFIX: {os.environ.get('PYTHONPYCACHEPREFIX', 'Not set')}")
    logger.info(f"PYTHONSAFEPATH: {os.environ.get('PYTHONSAFEPATH', 'Not set')}")
    logger.info(f"PYTHONTRACEMALLOC: {os.environ.get('PYTHONTRACEMALLOC', 'Not set')}")
    logger.info(f"PYTHONUNBUFFERED: {os.environ.get('PYTHONUNBUFFERED', 'Not set')}")
    logger.info(f"PYTHONUTF8: {os.environ.get('PYTHONUTF8', 'Not set')}")
    logger.info(f"PYTHONVERBOSE: {os.environ.get('PYTHONVERBOSE', 'Not set')}")
    logger.info(f"PYTHONWARNDEFAULTENCODING: {os.environ.get('PYTHONWARNDEFAULTENCODING', 'Not set')}")
    logger.info(f"PYTHONWARNINGS: {os.environ.get('PYTHONWARNINGS', 'Not set')}")
    logger.info(f"PATH: {os.environ.get('PATH', 'Not set')}")
    logger.info("=== END DEBUG INFO ===")
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
    if is_frozen():
        base_dir = worlds_install_dir
    
        for world in worlds:
            if "." in world:
                package_base, subdir = world.split(".", 1)
            
            package_dir = base_dir / package_base
            world_path = package_dir / subdir
            
            if not package_dir.exists():
                # try the next package
                continue
            
            if world_path.exists() and world_path.is_dir():
                logger.info(f"Removing directory: {world_path}")
                try:
                    shutil.rmtree(world_path)
                    logger.info(f"Successfully uninstalled: {package_base}.{subdir}")
                except Exception as e:
                    logger.error(f"Failed to remove {world_path}: {e}")
            else:
                logger.warning(f"Directory not found: {world_path}")
    else:
        for world in worlds:
            executable_args = [python_cmd, "-m", "pip", "uninstall", world, "--yes"]
            subprocess.run(executable_args)


def find_world_modules() -> List[str]:
    """Find all world modules in the multiworld repository."""
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
        world_modules = []
        for package in packages:
            if package.startswith("worlds-"):
                world_modules.append(package[7:])  # Remove "worlds-" prefix
        
        return world_modules
        
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        logger.warning(f"Failed to fetch world modules from {url}: {e}")
        return []
    except Exception as e:
        logger.warning(f"Unexpected error while fetching world modules: {e}")
        return []

def _move_compiled_files(directory: Path) -> None:
    """Moving .pyc files to parent directory for frozen builds
    Doing it this way to prevent users from editing .py files"""
    for pycache_dir in directory.rglob("__pycache__"):
        if pycache_dir.is_dir():
            parent_dir = pycache_dir.parent
            logger.debug(f"Moving .pyc files from {pycache_dir} to {parent_dir}")
            for pyc_file in pycache_dir.glob("*.pyc"):
                # Move .pyc file to parent directory
                if ".cpython" in pyc_file.name:
                    file_name = pyc_file.name.replace(f".cpython-{sys.version_info.major}{sys.version_info.minor}", "")
                else:
                    file_name = pyc_file.name
                target_path = parent_dir / file_name
                shutil.move(str(pyc_file), str(target_path))
                logger.debug(f"Moved {pyc_file.name} to {target_path}")
            # Remove empty __pycache__ directory
            try:
                pycache_dir.rmdir()
            except OSError:
                pass  # Directory not empty, leave it

def _add_to_library_zip(exe_dir: Path, source_path: Path) -> None:
    """Adding a modules to the library.zip file for frozen builds"""
    library_zip = exe_dir / "lib" / "library.zip"
    lib_dir = exe_dir / "lib"
    
    with zipfile.ZipFile(library_zip, "a") as zipf:
        if source_path.is_file():
            # Copy .pyd/.so directly to lib, others go to zip
            if source_path.suffix in ['.pyd', '.so']:
                target_path = lib_dir / source_path.name
                shutil.copy2(source_path, target_path)
                logger.debug(f"Copied {source_path.name} to lib directory")
            else:
                try:
                    zipf.write(source_path, source_path.name)
                except FileExistsError:
                    pass
        elif source_path.is_dir():
            # Add the entire directory tree to the zip, but copy .pyd/.so to lib
            for file_path in source_path.rglob("*"):
                if file_path.is_file() and not file_path.name.endswith(".py"):
                    if file_path.suffix in ['.pyd', '.so']:
                        # Copy compiled extensions directly to lib directory
                        target_path = lib_dir / file_path.name
                        shutil.copy2(file_path, target_path)
                        logger.debug(f"Copied {file_path.name} to lib directory")
                    else:
                        # Other files go to the zip with directory structure preserved
                        arcname = source_path.name / file_path.relative_to(source_path)
                        try:
                            zipf.write(file_path, str(arcname))
                        except FileExistsError:
                            pass       

def install_worlds(worlds: List[str]) -> None:
    """Install worlds from the multiworld repository."""
    check_pip()

    for world in worlds:
        logger.info(f"Installing world: {world}")
        
        if is_frozen():
            # In frozen environments, we need to install to a location that's in the Python path
            # and ensure we use the correct target directory
            executable_args = [python_cmd, "-m", "pip", "install", "--index-url", "https://pypi.org/simple",
                    "--extra-index-url", "https://pypi.multiworld.gg/mwgg/apworlds", 
                    world, "--compile", "--target", str(pip_install_dir), "--upgrade", "--no-cache-dir"]
            
            logger.info(f"Executing subprocess command: {executable_args}")
            logger.info(f"Working directory: {os.getcwd()}")
            
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
                # First, move all .pyc files from __pycache__ to parent directories
                _move_compiled_files(pip_install_dir)
                
                # Process each item in the install directory
                for item in pip_install_dir.iterdir():
                    if item.name != 'worlds' and item.name != 'mwgg_igdb':
                        # Add dependency packages to library.zip
                        logger.debug(f"Adding {item.name} to library")
                        _add_to_library_zip(exe_dir, item)
                    if "mwgg_igdb" in item.name:
                        # Copy everything from pip_install_dir to worlds_install_dir, excluding .py files
                        logger.debug(f"Installing mwgg_igdb...")
                        shutil.copytree(pip_install_dir / "mwgg_igdb", 
                                    worlds_install_dir / "mwgg_igdb", 
                                    dirs_exist_ok=True, 
                                    ignore=lambda src, files: [f for f in files if f.endswith('.py')])
                    else:
                        # Copy everything from pip_install_dir to worlds_install_dir, excluding .py files
                        logger.debug(f"Installing worlds...")
                        shutil.copytree(pip_install_dir / "worlds", 
                                    worlds_install_dir / "worlds", 
                                    dirs_exist_ok=True, 
                                    ignore=lambda src, files: [f for f in files if f.endswith('.py')])
                
                # Clean up temporary directory
                shutil.rmtree(pip_install_dir)
        else:
            executable_args = [python_cmd, "-m", "pip", "install", 
                    "--extra-index-url", "https://pypi.multiworld.gg/mwgg/apworlds", 
                    world, "--compile", "--upgrade", "--no-cache-dir"]
            result = subprocess.run(executable_args)
            if result.returncode != 0:
                logger.warning(f"Failed to install {world}")
            else:
                logger.info(f"Successfully installed {world}")

def update_world_wheels() -> None:
    """Install/update wheel files from custom_wheels directory."""
    check_pip()
    # Use threading version if frozen, otherwise use subprocess
    if is_frozen():
        for wheel in wheels_files:
            logger.info(f"Installing wheel: {wheel}")
            executable_args = [python_cmd, "-m", "pip", "install", wheel, "--upgrade", "--target", str(pip_install_dir)]
            
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
                # Move files from pip_install_dir to worlds_install_dir
                for obj in pip_install_dir.glob("*"):
                    obj.rename(worlds_install_dir / obj.name)
    else:
        for wheel in wheels_files:
            logger.info(f"Installing wheel: {wheel}")
            executable_args = [python_cmd, "-m", "pip", "install", wheel, "--upgrade"]
            result = subprocess.run(executable_args)
            if result.returncode != 0:
                logger.warning(f"Failed to install wheel {wheel}")
            else:
                logger.info(f"Successfully installed wheel {wheel}")


def update_requirements(needed_packages: List[str]) -> None:
    """Update packages from requirements.txt files and install worlds."""
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
    """
    if is_frozen():
        if (exe_dir / "custom_wheels").exists():
            logger.debug("Worlds wheels found, updating...")
            update_world_wheels()
        updates = check_for_updates(worlds_only=True)
        if updates:
            logger.info(f"Found updates for: {updates}")
            if not yes:
                confirm("Updates available. Press enter to continue with updates.")
            install_worlds(updates)
        else:
            logger.debug("No updates found.")
        return
    global update_ran
    
    if update_ran:
        return
    
    update_ran = True
    
    if force:
        logger.debug("Force update requested - skipping update checks")
        # Force mode updates all requirements and worlds
        update_requirements([])  # Empty list means update all
        return
    
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
        return
    
    # Update packages that need updates (including worlds)
    if available_updates:
        logger.debug("Updating packages that need updates...")
        update_requirements(available_updates)
    
    logger.debug("Update process completed.")


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
        requirements_files.update(args.additional_requirements)
    
    if args.worlds:
        update(args.yes, args.force, args.worlds)
    else:
        update(args.yes, args.force)
