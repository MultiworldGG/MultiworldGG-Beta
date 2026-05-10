import sys
import os
import subprocess
import multiprocessing
import warnings
import json
import shutil
import time
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
MWGG_IGDB_UPGRADE_INTERVAL_SECONDS = 86400  # once-daily throttle for upgrade pulls

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
if (is_windows() or is_macos()) and sys.version_info < (3, 13, 0):
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. Official 3.13.+ is supported.")
elif sys.version_info < (3, 13, 0):
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. 3.13.+ is supported.")

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

# Default for dev mode (not frozen): use the running interpreter and let uv install into its venv.
python_cmd = sys.executable
uv_cmd: str = ""


def find_uv() -> str:
    """Locate the uv binary. uv is user-installed, not bundled — see inno_setup.iss for the
    Windows install path (winget/PowerShell installer) and uv_runtime/install-uv.sh for Mac/Linux
    first-launch install. We probe `shutil.which` first, then platform-specific known locations,
    then (Mac/Linux frozen only) run the bundled installer as a last resort.
    """
    found = shutil.which("uv")
    if found:
        return found

    if is_windows():
        # The Inno installer just ran `winget install astral-sh.uv` (or astral's PowerShell installer)
        # but the user's PATH won't reflect the new entry until their explorer session refreshes.
        # Probe the known shim locations directly so the post-install --update-modules call works.
        # WinGet/Links shims are reparse points; Windows can refuse to traverse them with
        # WinError 448 ("untrusted mount point") — Python 3.13 Path.exists() does not suppress
        # that, so swallow OSError per-candidate and keep probing.
        local_appdata = os.environ.get("LOCALAPPDATA", "")
        candidates = [
            Path(local_appdata) / "Microsoft" / "WinGet" / "Links" / "uv.exe",
            Path.home() / ".local" / "bin" / "uv.exe",
        ]
        for candidate in candidates:
            try:
                if candidate.exists():
                    return str(candidate)
            except OSError as e:
                logger.warning(f"Could not probe uv candidate {candidate}: {e}")
                continue
    elif is_frozen():
        # First launch on Mac/Linux: bundled installer hasn't run yet. Run it once,
        # then check the default install location (~/.local/bin/uv).
        installer = Path(sys.executable).parent / "install-uv.sh"
        if installer.exists():
            logger.info(f"uv not found on PATH; running bundled installer {installer}")
            try:
                subprocess.run(["sh", str(installer)], check=True)
            except subprocess.CalledProcessError as e:
                logger.warning(f"Bundled uv installer failed: {e}")
            else:
                local_uv = Path.home() / ".local" / "bin" / "uv"
                if local_uv.exists():
                    return str(local_uv)
                # Re-probe PATH in case the installer modified it via shell rc files
                # that aren't visible to this already-running process.
                found = shutil.which("uv")
                if found:
                    return found

    raise RuntimeError(
        "uv not found on PATH and no fallback succeeded. Install uv manually: "
        "`winget install astral-sh.uv` (Windows) or "
        "`curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux). "
        "See https://docs.astral.sh/uv/getting-started/installation/."
    )


def venv_is_healthy(venv_path: Path) -> bool:
    """True if the venv at venv_path is still usable (creator interpreter dir exists, python runs)."""
    cfg = venv_path / "pyvenv.cfg"
    if not cfg.exists():
        return False
    home_dir: Optional[Path] = None
    for line in cfg.read_text().splitlines():
        if line.startswith("home"):
            _, _, val = line.partition("=")
            home_dir = Path(val.strip())
            break
    # If pyvenv.cfg's `home = ` points at a directory that no longer exists (e.g. user
    # uninstalled the Python that originally created the venv), the venv is dead.
    if home_dir is None or not home_dir.exists():
        return False
    venv_python = venv_path / ("Scripts" if is_windows() else "bin") / ("python.exe" if is_windows() else "python")
    if not venv_python.exists():
        return False
    try:
        return subprocess.run([str(venv_python), "--version"], capture_output=True, timeout=10).returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


uv_cmd = find_uv()

if is_frozen():
    # For frozen builds, install in a home directory to prevent readonly issues
    exe_dir = Path(sys.exec_prefix)
    default_libs_dir = Path(exe_dir, "lib")
    worlds_install_dir = install_path()
    if str(worlds_install_dir) not in sys.path:
        sys.path.append(str(worlds_install_dir))
    if str(default_libs_dir) not in sys.path:
        sys.path.append(str(default_libs_dir))

    venv_path = install_path()
    if venv_path.exists() and not venv_is_healthy(venv_path):
        logger.info(f"Existing venv at {venv_path} is broken or stale; recreating.")
        shutil.rmtree(venv_path, ignore_errors=True)
    if not venv_path.exists():
        venv_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Creating venv at {venv_path} via uv.")
        # uv reuses an existing system Python 3.13 if one is present; otherwise it
        # downloads python-build-standalone into %APPDATA%\uv\data\python\ (no UAC).
        subprocess.run([uv_cmd, "venv", str(venv_path), "--python", "3.13"], check=True)
    python_cmd = venv_path / ("Scripts" if is_windows() else "bin") / ("python.exe" if is_windows() else "python")


def _uv_pip(*args: str) -> list[str]:
    """Build a `uv pip ...` command targeting the active venv (python_cmd)."""
    return [uv_cmd, "pip", *args, "--python", str(python_cmd)]

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


def _igdb_stamp_path() -> Path:
    return install_path().parent / ".mwgg_igdb_last_upgrade"


def _igdb_upgraded_recently() -> bool:
    try:
        path = _igdb_stamp_path()
        if not path.exists():
            return False
        last = float(path.read_text().strip())
    except (OSError, ValueError, RuntimeError):
        return False
    elapsed = time.time() - last
    return 0 <= elapsed < MWGG_IGDB_UPGRADE_INTERVAL_SECONDS


def _record_igdb_upgrade() -> None:
    try:
        path = _igdb_stamp_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(time.time()))
    except (OSError, RuntimeError) as e:
        logger.debug(f"Could not write mwgg_igdb upgrade stamp: {e}")


def install_mwgg_igdb(upgrade: bool = False, force: bool = False) -> bool:
    """Install or refresh the mwgg_igdb package from the Index repo orphan branch.

    Called before any code path that imports `mwgg_igdb` — the package is the
    runtime source-of-truth for which worlds exist and where to fetch them.

    Args:
        upgrade: Run pip with --upgrade.
        force: With upgrade=True, bypass the once-daily throttle. Use for variant
               switches and standalone CLI invocation where a fresh pull is required.

    Concurrency: two processes that race on a stale stamp can both run pip into the
    same venv. uv pip writes to a temp location before rename, so the worst outcome
    is two pulls instead of one — not corruption.

    Returns True if the install succeeded (or was throttled).
    """
    if upgrade and not force and _igdb_upgraded_recently():
        logger.debug(
            f"mwgg_igdb upgrade attempted within {MWGG_IGDB_UPGRADE_INTERVAL_SECONDS}s; skipping"
        )
        return True
    args = _uv_pip("install", MWGG_IGDB_GIT_URL, "--no-cache")
    if upgrade:
        args.append("--upgrade")
    logger.info(f"Installing mwgg_igdb ({MWGG_IGDB_VARIANT}) from {MWGG_IGDB_BRANCH}")
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        logger.warning(f"Failed to install mwgg_igdb: {result.stderr}")
        return False
    if upgrade:
        _record_igdb_upgrade()
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
    """Extract the version from a release-asset wheel URL.

    Expects URLs like
    ``https://github.com/<owner>/<repo>/releases/download/<release_tag>/<dist>-<ver>-py3-none-any.whl``,
    optionally with a ``#sha256=<hex>`` fragment. Returns None for anything
    that isn't a recognizable wheel URL (legacy ``git+...@<ref>`` URLs from
    the v2 publish flow degrade to None — the caller then skips the
    comparison rather than crashing).
    """
    if not url:
        return None
    name = url.rsplit("/", 1)[-1]
    name = name.split("#", 1)[0].split("?", 1)[0]
    if not name.endswith(".whl"):
        return None
    parts = name[:-len(".whl")].split("-")
    # PEP 427: dist, version, [build,] python, abi, platform — version is index 1.
    if len(parts) < 5:
        return None
    return parts[1]


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

    # Dev-only path: ask uv for outdated dists. uv's resolver enforces requirements.txt
    # specifiers at install time, so we don't need to pre-filter here.
    try:
        executable_args = _uv_pip("list", "--outdated", "--format", "json")
        logger.info(f"Executing subprocess command: {executable_args}")
        response = subprocess.run(executable_args, capture_output=True, text=True, timeout=45)
        if response.returncode != 0:
            logger.warning(f"Could not check for updates: {response.stderr}")
            return []

        outdated_packages = json.loads(response.stdout)
        logger.info(f"Newer versions of the following packages are available: {outdated_packages}")
        return [pkg["name"] for pkg in outdated_packages]

    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        logger.warning(f"Could not check for updates: {e}")
        return []


def uninstall_worlds(worlds: List[str]) -> None:
    """Uninstall a list of `worlds.<slug>` packages from the venv."""
    for world in worlds:
        # uv pip uninstall is non-interactive by default; no --yes equivalent needed.
        subprocess.run(_uv_pip("uninstall", world))


def find_world_modules() -> set[str]:
    """Return all known world slugs: union of mwgg_igdb entries and currently installed `worlds.<slug>` dists."""
    world_modules_set: set[str] = set()

    index = _get_game_index()
    if index is not None:
        world_modules_set.update(index.get_all_games().keys())

    try:
        executable_args = _uv_pip("list", "--format", "json")
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

    `module_location` is a `https://.../<dist>-<world_version>-py3-none-any.whl#sha256=<hex>`
    release-asset URL set by the Index repo. `gen-pymod-release` uploads the wheel to the
    GitHub release on each per-world publish; the SHA256 fragment is pinned at PR-open time and
    verified by pip on install (PEP 503).

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
        install_mwgg_igdb(upgrade=True, force=True)

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

        executable_args = _uv_pip("install", "--no-deps", module_location, "--upgrade", "--no-cache")
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
        additional_deps_args = _uv_pip("check")
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
            # uv prefers wheels by default, no --prefer-binary equivalent needed.
            executable_args = _uv_pip("install", world, "--upgrade", "--no-cache")
            
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
                    executable_args = _uv_pip("show", package_name)
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
            executable_args = _uv_pip("install", wheel, "--upgrade")
            result = subprocess.run(executable_args)
            if result.returncode != 0:
                logger.warning(f"Failed to install wheel {wheel}")
            else:
                logger.info(f"Successfully installed wheel {wheel}")


def update_requirements(needed_packages: List[str]) -> None:
    """
    Update packages from requirements.txt files and install worlds.

    uv's resolver respects each requirement's version specifier on its own; we don't
    pre-parse with `packaging`. When `needed_packages` is empty, upgrade everything in
    each requirements file. Otherwise, upgrade only the named entries.
    """
    update_all = len(needed_packages) == 0

    for req_file in requirements_files:
        if not req_file.exists():
            logger.warning(f"Requirements file not found: {req_file}")
            continue

        logger.debug(f"Processing requirements from: {req_file}")
        if update_all:
            executable_args = _uv_pip("install", "--upgrade", "-r", str(req_file))
            result = subprocess.run(executable_args)
            if result.returncode != 0:
                logger.warning(f"Failed to install/update from {req_file.name}")
        else:
            requirements = parse_requirements_file(req_file)
            for req_line in requirements:
                # Extract the bare package name (everything up to the first version op or marker).
                pkg_name = re.split(r'[<>=!~;@\s]', req_line, 1)[0].strip()
                if pkg_name in needed_packages:
                    result = subprocess.run(_uv_pip("install", "--upgrade", req_line))
                    if result.returncode != 0:
                        logger.warning(f"Failed to install/update {req_line}")

    # Handle worlds (these are not in requirements.txt files)
    worlds_to_install = [pkg for pkg in needed_packages if pkg.startswith("worlds") or pkg.startswith("mwgg")]
    if worlds_to_install:
        logger.info(f"Installing/updating worlds: {worlds_to_install}")
        install_worlds(worlds_to_install)


def check_requirements_satisfied(yes: bool = False) -> bool:
    """
    Ensure all requirements files are satisfied. Returns True on success.

    With uv this is fast and idempotent — install runs unconditionally; if everything
    is already present, uv reports "Audited N packages" and exits in milliseconds.
    """
    for req_file in requirements_files:
        if not req_file.exists():
            logger.warning(f"Requirements file not found: {req_file}")
            continue
        logger.info(f"Ensuring requirements from {req_file.name} are satisfied")
        result = subprocess.run(
            _uv_pip("install", "-r", str(req_file)),
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            logger.warning(f"Failed to install requirements from {req_file.name}: {result.stderr}")
            return False
    return True


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
    # `from mwgg_igdb import GameIndex` working. Throttled to once per
    # MWGG_IGDB_UPGRADE_INTERVAL_SECONDS via a stamp file so every entry-point
    # start-up doesn't fire a network round-trip. Standalone CLI invocations of
    # ModuleUpdate.py write a fresh stamp before calling update(), so the throttle
    # naturally suppresses this call on the same-process re-entry — see __main__.
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

    # Standalone always pulls fresh; the stamp written here suppresses the
    # throttled install_mwgg_igdb(upgrade=True) calls inside the subsequent update().
    install_mwgg_igdb(upgrade=True, force=True)

    if args.additional_requirements:
        requirements_files.update([Path(req) for req in args.additional_requirements])

    if args.worlds:
        update(args.yes, args.force, args.worlds)
    else:
        update(args.yes, args.force)
