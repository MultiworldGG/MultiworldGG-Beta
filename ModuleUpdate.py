import sys
import os
import subprocess
import multiprocessing
import warnings
import json
import shutil
import zipfile
import re
import shutil
import logging

logger = logging.getLogger("Update")

if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.DEBUG, format='%(message)s', stream=sys.stdout)

from pathlib import Path
from typing import List, Optional

from importlib import invalidate_caches
from BaseUtils import tuplize_version, Version
from APContainer import APWorldContainer

# mwgg_igdb package source — orphan branch on the Index repo, force-pushed daily by
# the Index repo's daily-release workflow. Same package name and import path
# regardless of variant; variant choice only affects which games are filtered in/out.
# See MultiworldGG-Index/scripts/build_variants.py for variant definitions.
MWGG_IGDB_VARIANT = "sixteen"  # canonical default
MWGG_INDEX_REPO = "MultiworldGG/MultiworldGG-Index"
MWGG_IGDB_BRANCH = f"game_index_{MWGG_IGDB_VARIANT}"
MWGG_IGDB_GIT_URL = f"git+https://github.com/{MWGG_INDEX_REPO}@{MWGG_IGDB_BRANCH}"

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

# Don't import pip directly, we can set/forget this instead.
subprocess.run([python_cmd, "-m", "ensurepip"])

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


def install_mwgg_igdb(upgrade: bool = False) -> bool:
    """Install or refresh the mwgg_igdb package from the Index repo orphan branch.

    Called before any code path that imports `mwgg_igdb` — the package is the
    runtime source-of-truth for which worlds exist and where to fetch them.
    Returns True if the install succeeded.
    """
    args = [str(python_cmd), "-m", "pip", "install", MWGG_IGDB_GIT_URL, "--no-cache-dir"]
    if upgrade:
        args.append("--upgrade")
    logger.info(f"Installing mwgg_igdb ({MWGG_IGDB_VARIANT}) from {MWGG_IGDB_BRANCH}")
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        logger.warning(f"Failed to install mwgg_igdb: {result.stderr}")
        return False
    return True


def _get_game_index():
    """Lazy-import GameIndex; install mwgg_igdb if missing. Returns None on failure."""
    try:
        from mwgg_igdb import GameIndex
        return GameIndex
    except ImportError:
        if install_mwgg_igdb():
            invalidate_caches()
            try:
                from mwgg_igdb import GameIndex
                return GameIndex
            except ImportError as e:
                logger.warning(f"mwgg_igdb still unimportable after install: {e}")
        return None


def _module_location_tag(url: str) -> Optional[str]:
    """Extract the version tag from a `git+...@module-install/<ver>` URL."""
    if not url or "@" not in url:
        return None
    ref = url.rsplit("@", 1)[-1]
    if "/" in ref:
        return ref.rsplit("/", 1)[-1]
    return ref


_VARIANTS = ("nr", "ao", "twelve", "sixteen")


def _parse_variant_token(token: str) -> Optional[str]:
    """Return the variant name if `token` is `mwgg_igdb` or `mwgg_igdb_<variant>`, else None.

    Bare `mwgg_igdb` (no suffix) maps to the canonical default `sixteen`. Inno Setup
    passes one of these tokens in the `--worlds` list to select the parental-rating gate.
    """
    if token == "mwgg_igdb":
        return "sixteen"
    prefix = "mwgg_igdb_"
    if token.startswith(prefix):
        variant = token[len(prefix):]
        if variant in _VARIANTS:
            return variant
    return None


def _set_variant(variant: str) -> None:
    """Switch the runtime mwgg_igdb variant; takes effect on next install_mwgg_igdb call."""
    global MWGG_IGDB_VARIANT, MWGG_IGDB_BRANCH, MWGG_IGDB_GIT_URL
    MWGG_IGDB_VARIANT = variant
    MWGG_IGDB_BRANCH = f"game_index_{variant}"
    MWGG_IGDB_GIT_URL = f"git+https://github.com/{MWGG_INDEX_REPO}@{MWGG_IGDB_BRANCH}"


def check_for_updates(worlds_only: bool = False) -> List[str]:
    """
    Return packages with newer versions available.

    For worlds: re-pull mwgg_igdb (always latest), then return slugs whose
    installed dist version doesn't match the tag in `module_location`.
    For non-world packages: query PyPI against requirements.txt entries.
    """
    if is_frozen() and not worlds_only:
        return []
    try:
        import packaging.requirements
    except ImportError:
        logger.warning("packaging module not available, installing...")
        subprocess.run([str(python_cmd), "-m", "pip", "install", "--upgrade", "packaging"])
        import packaging.requirements

    if worlds_only:
        install_mwgg_igdb(upgrade=True)
        index = _get_game_index()
        if index is None:
            return []
        import importlib.metadata
        outdated: List[str] = []
        for slug, entry in index.get_all_games().items():
            loc = entry.get("module_location")
            if not loc:
                continue
            tag = _module_location_tag(loc)
            if not tag:
                continue
            try:
                dist = importlib.metadata.distribution(f"worlds.{slug}")
            except importlib.metadata.PackageNotFoundError:
                continue
            if dist.version != tag:
                outdated.append(f"worlds.{slug}")
        logger.info(f"Worlds with available updates: {outdated}")
        return outdated

    try:
        executable_args = [str(python_cmd), "-m", "pip", "list", "-o", "--format", "json",
            "-i", "https://pypi.org/simple"]
        logger.info(f"Executing subprocess command: {executable_args}")
        response = subprocess.run(executable_args, capture_output=True, text=True, timeout=45)
        if response.returncode != 0:
            logger.warning(f"Could not check for updates: {response.stderr}")
            return []

        outdated_packages = json.loads(response.stdout)
        logger.info(f"Newer versions of the following packages are available: {outdated_packages}")

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

        packages_to_update = []
        for pkg in outdated_packages:
            pkg_name = pkg["name"]
            latest_version = pkg["latest_version"]

            if pkg_name in all_requirements:
                requirement = all_requirements[pkg_name]
                try:
                    if not requirement.specifier:
                        packages_to_update.append(pkg_name)
                    else:
                        from packaging.version import parse as parse_version
                        latest_ver = parse_version(latest_version)
                        if latest_ver in requirement.specifier:
                            packages_to_update.append(pkg_name)
                        else:
                            logger.debug(f"Skipping {pkg_name}: latest version {latest_version} doesn't satisfy requirement {requirement}")
                except Exception as e:
                    logger.debug(f"Skipping {pkg_name}: couldn't check version constraint: {e}")
            else:
                packages_to_update.append(pkg_name)

        return packages_to_update

    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        logger.warning(f"Could not check for updates: {e}")
        return []


def uninstall_worlds(worlds: List[str]) -> None:
    """Uninstall a list of `worlds.<slug>` packages from the venv."""
    for world in worlds:
        executable_args = [str(python_cmd), "-m", "pip", "uninstall", world, "--yes"]
        subprocess.run(executable_args)


def find_world_modules() -> set[str]:
    """Return all known world slugs: union of mwgg_igdb entries and currently installed `worlds.<slug>` dists."""
    world_modules_set: set[str] = set()

    index = _get_game_index()
    if index is not None:
        world_modules_set.update(index.get_all_games().keys())

    try:
        executable_args = [str(python_cmd), "-m", "pip", "list", "--format", "json"]
        logger.debug(f"Executing subprocess command to find installed worlds: {executable_args}")
        response = subprocess.run(executable_args, capture_output=True, text=True, timeout=45)
        if response.returncode == 0:
            for package in json.loads(response.stdout):
                package_name = package.get("name", "")
                if package_name.startswith("worlds"):
                    world_name = package_name[7:]
                    if not world_name.startswith("_"):
                        world_modules_set.add(world_name)
        else:
            logger.warning(f"Could not list installed packages: {response.stderr}")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        logger.warning(f"Could not check installed world modules: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error while checking installed world modules: {e}")

    return world_modules_set


def install_worlds(worlds: List[str], update: bool = False, no_recurse: bool = False) -> list[str]:
    """
    Install worlds by resolving each slug's `module_location` from mwgg_igdb and pip-installing the URL.

    `module_location` is a `git+https://.../<repo>@module-install/<world_version>` URL set by the
    Index repo. The gen-pymod-release force-pushes immutable tags per release.

    Falls back to a custom_worlds/<slug>.apworld lookup if the slug isn't in the index or its
    `module_location` install fails.

    Args:
        worlds: List of slugs (with or without `worlds.` prefix) to install.
        update: If True, uninstall old versions first.
        no_recurse: If True, skip the post-install dependency-check pass.

    Returns:
        List of slugs that fell back to a custom apworld.
    """
    apworlds: list[str] = []

    # Partition variant tokens (`mwgg_igdb` / `mwgg_igdb_<variant>`) out of the slug list.
    # Inno Setup passes exactly one variant token in `--worlds`; honor it by switching
    # the runtime variant and (re)installing mwgg_igdb before resolving slugs.
    world_slugs: list[str] = []
    selected_variant: Optional[str] = None
    for entry in worlds:
        variant = _parse_variant_token(entry)
        if variant is not None:
            selected_variant = variant
        else:
            world_slugs.append(entry)

    if selected_variant is not None:
        _set_variant(selected_variant)
        install_mwgg_igdb(upgrade=True)

    if update:
        logger.info(f"Uninstalling old versions of: {world_slugs}")
        uninstall_worlds(world_slugs)

    index = _get_game_index()
    games = index.get_all_games() if index is not None else {}

    for world in world_slugs:
        slug = world.removeprefix("worlds.")
        target = f"worlds.{slug}"

        if update:
            logger.info(f"Updating world: {target}")
        else:
            logger.info(f"Installing world: {target}")

        entry = games.get(slug, {})
        module_location = entry.get("module_location")

        if not module_location:
            logger.warning(f"No module_location for {slug} in mwgg_igdb; checking custom_worlds")
            apworld_file = custom_worlds_dir / f"{slug}.apworld"
            if apworld_file.exists():
                logger.info(f"Found apworld file: {apworld_file}")
                apworlds.append(target)
            else:
                logger.warning(f"Custom apworld file not found at {apworld_file}, {slug} cannot be installed")
            continue

        executable_args = [str(python_cmd), "-m", "pip", "install", "--no-deps",
                module_location, "--upgrade", "--no-cache-dir"]
        logger.info(f"Executing subprocess command: {executable_args}")
        result = subprocess.run(executable_args, capture_output=True, text=True)
        logger.info(result.stdout)

        if result.returncode != 0:
            logger.warning(f"World {target} failed to install from {module_location}")
            if result.stderr:
                logger.error(result.stderr)
            apworld_file = custom_worlds_dir / f"{slug}.apworld"
            if apworld_file.exists():
                logger.info(f"Found apworld file: {apworld_file}")
                apworlds.append(target)
            else:
                logger.warning(f"Custom apworld file not found at {apworld_file}")
        else:
            logger.info(f"Successfully installed {target}")

    invalidate_caches()

    if is_frozen() and not no_recurse:
        # Check for any additional updates that might be needed
        logger.info("Checking for additional dependencies...")
        additional_deps_args = [python_cmd, "-m", "pip", "check"]
        additional_deps_result = subprocess.run(additional_deps_args, capture_output=True, text=True)
        stdout = additional_deps_result.stdout
        
        no_deps = ("No broken requirements found." in stdout)
        if no_deps:
            logger.info(f"Updates complete.")
            return apworlds
        
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
            update_requirements(packages_to_install)
    
    return apworlds

def update_world_from_package() -> None:
    """Install/update wheel files from custom_worlds directory."""
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
            logger.info(f"APWorld found, checking versions: {world}")
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
                except Exception as e:
                    logger.warning(f"Failed to read version from APworld {world}: {e}")
                
                # Check if world is already installed using pip show
                package_name = f"worlds.{module_name}"
                installed_version: Optional[Version] = None
                
                try:
                    executable_args = [python_cmd, "-m", "pip", "show", package_name]
                    result = subprocess.run(executable_args, capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0:
                        # Package is installed, parse version from output
                        for line in result.stdout.splitlines():
                            if line.startswith("Version:"):
                                version_str = line.split(":", 1)[1].strip()
                                installed_version = tuplize_version(version_str)
                                logger.info(f"Installed world {module_name} has version {version_str}")
                                break
                        else:
                            logger.info(f"Installed world {module_name} found but no version in pip show output")
                    else:
                        # Package not installed
                        logger.info(f"World {module_name} is not installed")
                except (subprocess.TimeoutExpired, Exception) as e:
                    logger.warning(f"Failed to check installed version for {module_name} using pip show: {e}")
                
                # Compare versions: install if new_version > installed_version
                # According to spec: "An APWorld without a world_version is always treated as older than one with a version"
                if new_version is None and installed_version is not None:
                    logger.info(f"There is a custom apworld file with no world version specified, please remove it from your custom_worlds directory.")
                elif installed_version is None or new_version > installed_version:
                    if installed_version is not None:
                        uninstall_worlds([package_name])
                        logger.info(f"New version {new_version.as_simple_string()} > installed {installed_version.as_simple_string()}, uninstalling old version so new version will be picked up.")
                else:
                    logger.info(f"There is a custom apworld file with an older version than what is installed. Please remove it from your custom_worlds directory.")

            except Exception as e:
                logger.warning(f"Failed to check versions for APworld {world}: {e}")
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
    # Ensure packaging is available
    try:
        import packaging.requirements
    except ImportError:
        logger.warning("packaging module not available, installing...")
        subprocess.run([python_cmd, "-m", "pip", "install", "--upgrade", "packaging"])
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
    try:
        import packaging.requirements  # noqa: F401
    except ImportError:
        if not yes:
            confirm("packaging not found, press enter to install it")
        executable_args = [python_cmd, "-m", "pip", "install", "--upgrade", "packaging"]
        subprocess.run(executable_args)


def check_requirements_satisfied(yes: bool = False) -> bool:
    """
    Check if all requirements are satisfied.
    Returns True if all requirements are met, False otherwise.
    """
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
    # Install/refresh mwgg_igdb upfront so any subsequent code path can rely on
    # `from mwgg_igdb import GameIndex` working. NOTE: in the prior architecture the
    # installer (Inno Setup on Windows, equivalent on macOS/Linux) seeded mwgg_igdb
    # by invoking ModuleUpdate via the CLI as part of first-run setup, then runtime
    # update() calls trusted that to already be present. Doing it here unconditionally
    # may be redundant when the installer already ran it — accepted cost for a single
    # consistent code path. If installer-side seeding gets re-introduced, this call
    # can be guarded by a "first run since install" check (e.g. mwgg_igdb dist
    # presence + age) rather than running every update().
    install_mwgg_igdb(upgrade=True)

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
