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
if (is_windows() or is_macos()) and sys.version_info < (3, 12, 0):
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. Official 3.12.+ is supported.")
elif (is_windows() or is_macos()) and sys.version_info < (3, 12, 7):
    logger.warning(f"Python Version {sys.version_info} has security issues. Don't use in production.")
elif sys.version_info < (3, 12, 0):
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. 3.12.+ is supported.")

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

def install_wheels(type="default") -> bool:
    """Install wheels from default_wheels directory"""
    wheels_dir = Path(f"{type}_wheels")
    if wheels_dir.exists():
        logger.info(f"Installing wheels from {type}_wheels...")

        for wheel_file in wheels_dir.glob("*.whl"):
            # Skip igdb variants (already handled above)
            if any(variant in wheel_file.name for variant in ["mwgg_igdb-", "mwgg_igdb_sixteen-", "mwgg_igdb_twelve-"]):
                continue
            
            # Skip platform-specific wheels that don't match current platform
            wheel_name = wheel_file.name.lower()
            if "win_amd64" in wheel_name or "win32" in wheel_name:
                if not is_windows():
                    logger.debug(f"Skipping {wheel_file.name} (Windows-only)")
                    continue
            if "macosx" in wheel_name:
                if not is_macos():
                    logger.debug(f"Skipping {wheel_file.name} (macOS-only)")
                    continue
            if "linux" in wheel_name:
                if not is_linux():
                    logger.debug(f"Skipping {wheel_file.name} (Linux-only)")
                    continue
            
            try:
                # First try with dependencies to ensure all required packages are installed
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    str(wheel_file), "--force-reinstall"
                ])
                logger.info(f"[OK] Installed {wheel_file.name}")
            except subprocess.CalledProcessError as e:
                logger.debug(f"Failed to install {wheel_file.name} with dependencies: {e}")
                # Fallback to no-deps if dependency installation fails
                try:
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", 
                        str(wheel_file), "--no-deps", "--force-reinstall"
                    ])
                    logger.info(f"[OK] Installed {wheel_file.name} (no-deps)")
                except subprocess.CalledProcessError as e2:
                    logger.warning(f"[FAILED] Failed to install {wheel_file.name}: {e2}")
        return True
    else:
        logger.info(f"{type}_wheels directory not found, skipping wheel installation")
        return False

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

    # Install default wheels
    if not args.skip_wheels:
        if not install_wheels("default"):
            sys.exit(1)

    # Install worlds wheels
    if not args.skip_wheels:
        if not install_wheels("worlds"):
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
