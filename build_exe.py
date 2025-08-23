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

# Set environment variable to skip world requirements installation immediately
os.environ["SKIP_REQUIREMENTS_UPDATE"] = "1"

def install_cx_freeze():
    """Install cx_Freeze if not already installed"""
    try:
        import cx_Freeze
        print("cx_Freeze is already installed")
        return True
    except ImportError:
        print("Installing cx_Freeze...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "cx-Freeze>=6.15.0"
            ])
            print("cx_Freeze installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install cx_Freeze: {e}")
            return False

def install_requirements():
    """Install requirements from main requirements.txt only"""
    # Ensure we're looking at the main requirements.txt in the current directory
    req_file = Path("requirements.txt")
    if req_file.exists():
        print(f"Installing requirements from: {req_file.absolute()}")
        try:
            # Use absolute path to ensure we're using the correct requirements.txt
            abs_req_file = req_file.absolute()
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(abs_req_file)
            ])
            print("Requirements installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install requirements: {e}")
            return False
    else:
        print("requirements.txt not found, skipping requirements installation")
        return True

def install_wheels():
    """Install wheels from default_wheels directory"""
    wheels_dir = Path("default_wheels")
    if wheels_dir.exists():
        print("Installing wheels from default_wheels...")
        success_count = 0
        total_count = 0
        
        for wheel_file in wheels_dir.glob("*.whl"):
            total_count += 1
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", 
                    str(wheel_file), "--no-deps", "--force-reinstall"
                ])
                print(f"✓ Installed {wheel_file.name}")
                success_count += 1
            except subprocess.CalledProcessError as e:
                print(f"✗ Failed to install {wheel_file.name}: {e}")
        
        print(f"Wheel installation complete: {success_count}/{total_count} successful")
        return success_count > 0
    else:
        print("default_wheels directory not found, skipping wheel installation")
        return True

def update_modules():
    """Update modules using ModuleUpdate"""
    try:
        import os
        # Set environment variable to skip world requirements installation
        os.environ["SKIP_REQUIREMENTS_UPDATE"] = "1"
        import ModuleUpdate
        print("Updating modules...")
        ModuleUpdate.update(yes=True)
        print("Module update completed")
        return True
    except Exception as e:
        print(f"Module update failed: {e}")
        return False

def run_cx_freeze_build():
    """Run the cx_Freeze build process"""
    print("Starting cx_Freeze build...")
    try:
        # Import and run setup
        from setup import setup
        import cx_Freeze
        
        # Run the build
        subprocess.check_call([
            sys.executable, "setup.py", "build_exe"
        ])
        print("cx_Freeze build completed successfully")
        return True
    except Exception as e:
        print(f"cx_Freeze build failed: {e}")
        return False

def clean_build_directory():
    """Clean the build directory"""
    build_dir = Path("build")
    if build_dir.exists():
        print("Cleaning build directory...")
        try:
            shutil.rmtree(build_dir)
            print("Build directory cleaned")
            return True
        except Exception as e:
            print(f"Failed to clean build directory: {e}")
            return False
    return True

def verify_build_output():
    """Verify that the build output contains expected executables"""
    build_dir = Path("build")
    if not build_dir.exists():
        print("Build directory not found")
        return False
    
    # Find the actual build directory (platform-specific)
    exe_dirs = list(build_dir.glob("exe.*"))
    if not exe_dirs:
        print("No executable build directory found")
        return False
    
    exe_dir = exe_dirs[0]
    print(f"Checking build output in: {exe_dir}")
    
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
            print(f"✓ Found {exe}")
        else:
            print(f"✗ Missing {exe}")
            missing_exes.append(exe)
    
    if missing_exes:
        print(f"Build verification failed: {len(missing_exes)} executables missing")
        return False
    
    # Check for required directories
    required_dirs = ["data", "lib"]
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = exe_dir / dir_name
        if dir_path.exists():
            print(f"✓ Found {dir_name}/")
        else:
            print(f"✗ Missing {dir_name}/")
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"Build verification failed: {len(missing_dirs)} directories missing")
        return False
    
    print("Build verification passed!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Build MultiWorldGG executables")
    parser.add_argument("--clean", action="store_true", help="Clean build directory before building")
    parser.add_argument("--skip-requirements", action="store_true", help="Skip requirements installation")
    parser.add_argument("--skip-wheels", action="store_true", help="Skip wheel installation")
    parser.add_argument("--skip-modules", action="store_true", help="Skip module update")
    parser.add_argument("--verify", action="store_true", help="Verify build output after building")
    
    args = parser.parse_args()
    
    print("MultiWorldGG Build Script")
    print("=" * 50)
    
    # Change to src directory
    os.chdir(Path(__file__).parent)
    
    # Clean if requested
    if args.clean:
        if not clean_build_directory():
            sys.exit(1)
    
    # Install cx_Freeze
    if not install_cx_freeze():
        sys.exit(1)
    
    # Install requirements
    if not args.skip_requirements:
        if not install_requirements():
            sys.exit(1)
    
    # Install wheels
    if not args.skip_wheels:
        if not install_wheels():
            sys.exit(1)
    
    # Update modules
    if not args.skip_modules:
        if not update_modules():
            sys.exit(1)
    
    # Run build
    if not run_cx_freeze_build():
        sys.exit(1)
    
    # Verify build
    if args.verify:
        if not verify_build_output():
            sys.exit(1)
    
    print("=" * 50)
    print("Build completed successfully!")
    
    # Show build location
    build_dir = Path("build")
    if build_dir.exists():
        exe_dirs = list(build_dir.glob("exe.*"))
        if exe_dirs:
            print(f"Executables are located in: {exe_dirs[0].absolute()}")

if __name__ == "__main__":
    main()
