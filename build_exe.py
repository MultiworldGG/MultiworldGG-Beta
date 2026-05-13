#!/usr/bin/env python3
"""
Build script for MultiWorldGG executables using cx_Freeze
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse
import logging
import urllib.request
import urllib.error
import json
import tempfile

logger = logging.getLogger("MultiWorld")
if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.WARNING, format='%(name)s: %(message)s', stream=sys.stdout)
if not logging.getLogger("MultiWorld").hasHandlers():
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setFormatter(logging.Formatter('%(message)s'))
    logger.setLevel(logging.INFO)

def is_windows() -> bool:
    return sys.platform in ("win32", "cygwin", "msys")
def is_macos() -> bool:
    return sys.platform == "darwin"
def is_linux() -> bool:
    return sys.platform.startswith("linux")

# Version compatibility checks
if (is_windows() or is_macos()) and sys.version_info < (3, 13, 0):
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. Official 3.13.+ is supported.")
elif sys.version_info < (3, 13, 0):
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. 3.13.+ is supported.")

# Define function to install requirements, then install build requirements
def install_requirements(build: bool = False) -> bool:
    """Install requirements from requirements.txt file(s)"""

    #Install build_requirements.txt
    if build:
        req_file = Path("build_requirements.txt")
    else:
        req_file = Path("requirements.txt")
    if req_file.exists():
        logger.debug(f"Installing requirements from {req_file.name}...")
        try:
            # Use absolute path to ensure we're using the correct requirements.txt
            abs_req_file = req_file.absolute()
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(abs_req_file)
            ])
            logger.debug("Requirements installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to install requirements: {e}")
            return False
    else:
        logger.info(f"{req_file.name} not found, skipping requirements installation")
        return True

# Sibling repos under the MultiworldGG GitHub org that publish wheel releases.
# build_exe pip-installs the latest wheel asset from each into the build venv so
# cx_Freeze can bundle them. Per-game worlds are NOT here — those are pulled at
# first run by ModuleUpdate.install_worlds() from mwgg_igdb module_location URLs.
# TODO: add the platform-helpers repo (pyfastbti, pyfastyaz0yay0) here once it
# exists. The current frozen build doesn't need those — every world that did has
# been pulled out of the monorepo.
SIBLING_WHEEL_REPOS: list[tuple[str, str]] = [
    ("MultiworldGG", "mwgg-gui"),
    ("MultiworldGG", "mwgg-tui"),
    ("MultiworldGG", "mwgg-splash"),
]


# Token for fetching from private sibling repos during beta. Set
# MWGG_BUILD_GITHUB_TOKEN (locally or via the workflow's `env:` block) to a PAT or
# GitHub App installation token with `contents: read` on the SIBLING_WHEEL_REPOS.
# When the repos go public this can be unset and anonymous requests will work.
_BUILD_GH_TOKEN_ENV = "MWGG_BUILD_GITHUB_TOKEN"


def _gh_headers() -> dict:
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get(_BUILD_GH_TOKEN_ENV, "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _pick_wheel_asset(assets: list[dict]) -> dict | None:
    """Return the best wheel asset for the current platform, or None.

    Prefer pure-Python (`py3-none-any`) wheels; fall back to a platform-tagged
    wheel matching the current OS. Skip wheels tagged for other platforms.
    """
    wheels = [a for a in assets if a.get("name", "").endswith(".whl")]
    if not wheels:
        return None

    def matches_platform(name: str) -> bool:
        if "py3-none-any" in name:
            return True
        if is_windows() and ("win_amd64" in name or "win32" in name):
            return True
        if is_linux() and "linux" in name:
            return True
        if is_macos() and "macosx" in name:
            return True
        return False

    def is_foreign(name: str) -> bool:
        # A platform-tagged wheel for someone else's platform.
        foreign_tags = []
        if not is_windows():
            foreign_tags += ["win_amd64", "win32"]
        if not is_linux():
            foreign_tags += ["linux"]
        if not is_macos():
            foreign_tags += ["macosx"]
        return any(tag in name for tag in foreign_tags)

    # Pure-Python first.
    for a in wheels:
        if "py3-none-any" in a["name"]:
            return a
    # Then native-platform.
    for a in wheels:
        if matches_platform(a["name"]) and not is_foreign(a["name"]):
            return a
    return None


def _latest_release_wheel_asset(owner: str, repo: str) -> dict | None:
    """Fetch the latest release for a sibling repo and return the chosen wheel asset dict."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    req = urllib.request.Request(api_url, headers=_gh_headers())
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # 404 on a private repo means the token isn't set or doesn't grant read access.
        if e.code == 404 and not os.environ.get(_BUILD_GH_TOKEN_ENV, "").strip():
            logger.warning(
                f"GET {api_url} returned 404; if {owner}/{repo} is private, set "
                f"{_BUILD_GH_TOKEN_ENV} to a PAT with `contents: read` on it"
            )
        else:
            logger.warning(f"GET {api_url} failed: {e}")
        return None
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        logger.warning(f"Could not fetch latest release for {owner}/{repo}: {e}")
        return None

    asset = _pick_wheel_asset(data.get("assets", []))
    if asset is None:
        logger.warning(f"No suitable wheel asset on latest release of {owner}/{repo}")
        return None
    return asset


def _download_release_asset(owner: str, repo: str, asset: dict) -> str | None:
    """Download a release asset by id; return the path to a file with the asset's
    original filename (inside a fresh temp dir). Works for private repos.

    The filename must match PEP 427 — pip parses dist/version/tags from it — so we
    can't use mkstemp's randomized name. We create a temp dir and write the asset
    into it with `asset["name"]`. Caller is responsible for cleaning up the dir.

    Uses the `/releases/assets/{id}` endpoint with `Accept: application/octet-stream`,
    which serves the binary directly (or 302-redirects to a signed URL that needs no
    further auth). urllib follows the redirect; we strip Authorization on hop to a
    foreign host so the signed URL isn't double-authed and rejected.
    """
    asset_id = asset.get("id")
    name = asset.get("name") or ""
    if asset_id is None or not name:
        logger.warning(f"Asset from {owner}/{repo} has no id/name; cannot download")
        return None

    asset_url = f"https://api.github.com/repos/{owner}/{repo}/releases/assets/{asset_id}"
    headers = _gh_headers()
    headers["Accept"] = "application/octet-stream"

    # Custom handler: when GitHub returns 302 to AWS S3, drop our Authorization header
    # before following — the redirect target has signed credentials baked into the URL,
    # and S3 will reject a stray Bearer token.
    class _StripAuthRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            new_req = super().redirect_request(req, fp, code, msg, headers, newurl)
            if new_req is not None:
                new_req.headers.pop("Authorization", None)
                new_req.unredirected_hdrs.pop("Authorization", None)
            return new_req

    opener = urllib.request.build_opener(_StripAuthRedirect())
    req = urllib.request.Request(asset_url, headers=headers)

    tmp_dir = tempfile.mkdtemp(prefix="mwgg_wheel_")
    path = os.path.join(tmp_dir, name)
    try:
        with opener.open(req, timeout=120) as resp, open(path, "wb") as out:
            shutil.copyfileobj(resp, out)
    except (urllib.error.URLError, TimeoutError) as e:
        logger.warning(f"Failed to download asset {name} from {owner}/{repo}: {e}")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return None
    return path


def install_wheels() -> bool:
    """Install sibling-repo wheels from their latest GitHub releases.

    For each repo in SIBLING_WHEEL_REPOS, GET the latest release, pick a wheel
    asset compatible with the current platform, download it (authenticated when
    MWGG_BUILD_GITHUB_TOKEN is set, anonymous otherwise), and pip-install it
    into the build venv. cx_Freeze then bundles the installed package into the
    frozen build via setup.py's `packages` list.
    """
    if not os.environ.get(_BUILD_GH_TOKEN_ENV, "").strip():
        logger.info(
            f"{_BUILD_GH_TOKEN_ENV} not set; fetching anonymously. "
            "If a sibling repo is private the fetch will 404."
        )

    for owner, repo in SIBLING_WHEEL_REPOS:
        asset = _latest_release_wheel_asset(owner, repo)
        if asset is None:
            return False
        wheel_path = _download_release_asset(owner, repo, asset)
        if wheel_path is None:
            return False
        logger.info(f"Installing {owner}/{repo} wheel {asset.get('name')}")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", wheel_path,
                "--force-reinstall", "--no-cache-dir",
            ])
        except subprocess.CalledProcessError as e:
            logger.warning(f"pip install failed for {owner}/{repo}: {e}")
            return False
        finally:
            shutil.rmtree(os.path.dirname(wheel_path), ignore_errors=True)
    return True

def update_modules() -> bool:
    """Update modules using ModuleUpdate"""
    try:
        import ModuleUpdate
        logger.debug("Updating modules...")
        ModuleUpdate.update(yes=True)
        logger.debug("Module update completed")
        return True
    except Exception as e:
        logger.debug(f"Module update failed: {e}")
        return False

def generate_setup_ini() -> bool:
    """Generate setup.ini file with build configuration"""
    try:
        # Import to get version info
        sys.path.insert(0, os.path.dirname(__file__))
        from Utils import version_tuple
        import platform
        
        # Determine build directory name
        build_dir = f"build\\exe.win-amd64-{sys.version_info.major}.{sys.version_info.minor}"

        # Get full version string
        version_str = version_tuple.as_pep440_string()
        
        # Write setup.ini
        with open("setup.ini", "w") as f:
            f.write("[Data]\n")
            f.write(f"source_path={build_dir}\n")
            f.write(f"app_version={version_str}\n")
        
        logger.info(f"Generated setup.ini with source_path={build_dir}, app_version={version_str}")
        return True
    except Exception as e:
        logger.warning(f"Failed to generate setup.ini: {e}")
        return False

def run_cx_freeze_build() -> bool:
    """Run the cx_Freeze build process"""
    logger.debug("Starting cx_Freeze build...")
    try:
        # Import and run setup
        from setup import setup
        import cx_Freeze
        
        # Run the build
        subprocess.check_call([
            sys.executable, "setup.py", "build_exe"
        ])
        logger.debug("cx_Freeze build completed successfully")
        return True
    except Exception as e:
        logger.debug(f"cx_Freeze build failed: {e}")
        return False

def clean_build_directory() -> bool:
    """Clean the build directory"""
    build_dir = Path("build")
    if build_dir.exists():
        logger.debug("Cleaning build directory...")
        try:
            shutil.rmtree(build_dir)
            logger.debug("Build directory cleaned")
            return True
        except Exception as e:
            logger.debug(f"Failed to clean build directory: {e}")
            return False
    return True

def verify_build_output() -> bool:
    """Verify that the build output contains expected executables"""
    build_dir = Path("build")
    if not build_dir.exists():
        logger.debug("Build directory not found")
        return False
    
    # Find the actual build directory (platform-specific)
    exe_dirs = list(build_dir.glob("exe.*"))
    if not exe_dirs:
        logger.debug("No executable build directory found")
        return False
    
    exe_dir = exe_dirs[0]
    logger.debug(f"Checking build output in: {exe_dir}")
    
    expected_exes = [
        "MultiWorldGG.exe" if sys.platform == "win32" else "MultiWorldGG",
        "MultiWorldGGServer.exe" if sys.platform == "win32" else "MultiWorldGGServer",
        "MultiWorldGGGenerate.exe" if sys.platform == "win32" else "MultiWorldGGGenerate",
        "MultiWorldGGPatch.exe" if sys.platform == "win32" else "MultiWorldGGPatch"
    ]
    
    if sys.platform == "win32":
        expected_exes.append("MultiWorldGGClientDebug.exe")
    
    missing_exes = []
    for exe in expected_exes:
        exe_path = exe_dir / exe
        if exe_path.exists():
            logger.info(f"[OK] Found {exe}")
        else:
            logger.info(f"[FAILED] Missing {exe}")
            missing_exes.append(exe)
    
    if missing_exes:
        logger.info(f"Build verification failed: {len(missing_exes)} executables missing")
        return False
    
    # Check for required directories
    required_dirs = ["data", "lib"]
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = exe_dir / dir_name
        if dir_path.exists():
            logger.info(f"[OK] Found {dir_name}/")
        else:
            logger.info(f"[FAILED] Missing {dir_name}/")
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        logger.info(f"Build verification failed: {len(missing_dirs)} directories missing")
        return False
    
    logger.info("Build verification passed!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Build MultiWorldGG executables")
    parser.add_argument("--clean", action="store_true", help="Clean build directory before building")
    parser.add_argument("--skip-requirements", action="store_true", help="Skip requirements installation")
    parser.add_argument("--skip-wheels", action="store_true", help="Skip wheel installation")
    parser.add_argument("--skip-modules", action="store_true", help="Skip module update")
    parser.add_argument("--verify", action="store_true", help="Verify build output after building")
    parser.add_argument("--logger-level", action="store", help="Set logger level", default="INFO")
    args = parser.parse_args()
    logger.setLevel(args.logger_level)

    logger.info("MultiWorldGG Build Script")
    logger.info("=" * 50)
    # Change to src directory
    os.chdir(Path(__file__).parent)
    
    # Clean if requested
    if args.clean:
        if not clean_build_directory():
            sys.exit(1)
    
    # Install requirements
    if not install_requirements(build=True):
        sys.exit(1)

    if not args.skip_requirements:
        if not install_requirements(build=False):
            sys.exit(1)

    # Install sibling-repo wheels (mwgg_gui, mwgg_tui, mwgg_splash) from their
    # latest GitHub releases. cx_Freeze bundles them once they're in the build
    # venv. Worlds bundle directly from src/worlds/ source — no wheel fetch
    # there. Per-game worlds are installed at first run by
    # ModuleUpdate.install_worlds() from mwgg_igdb's module_location URLs.
    if not args.skip_wheels:
        if not install_wheels():
            sys.exit(1)

    # Update modules
    # if not args.skip_modules:
    #     if not update_modules():
    #         sys.exit(1)

    # Generate setup.ini for Inno Setup (Windows installer)
    if is_windows():
        if not generate_setup_ini():
            logger.warning("Failed to generate setup.ini, continuing anyway...")

    # Run build
    if not run_cx_freeze_build():
        sys.exit(1)
    
    # Verify build
    if args.verify:
        if not verify_build_output():
            sys.exit(1)
    
    logger.info("=" * 50)
    logger.info("Build completed successfully!")
    
    # Show build location
    build_dir = Path("build")
    if build_dir.exists():
        exe_dirs = list(build_dir.glob("exe.*"))
        if exe_dirs:
            logger.info(f"Executables are located in: {exe_dirs[0].absolute()}")

if __name__ == "__main__":
    main()
