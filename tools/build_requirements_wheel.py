#!/usr/bin/env python3
"""
BuildReqWheels - Git dependency wheel builder for MultiworldGG

This module handles building and caching wheels for git-based dependencies
to avoid repeated git pulls and compilation during builds.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional, Dict

class GitWheelBuilder:
    """Handles building and managing wheels from git dependencies"""
    
    def __init__(self, requirements_file: str = "requirements.txt", 
                 wheels_dir: str = "default_wheels",
                 git_packages: Optional[List[str]] = None):
        """
        Initialize the wheel builder
        
        Args:
            requirements_file: Path to requirements.txt file
            wheels_dir: Directory to store built wheels
            git_packages: List of git package names to build wheels for.
                         If None, uses default list.
        """
        if requirements_file == "requirements.txt":
            src_dir = Path(os.path.abspath(__file__)).parent
            if src_dir.name == "tools":
                src_dir = str(src_dir.parent)
            requirements_file = f"{src_dir}/requirements.txt"

        self.requirements_file = Path(requirements_file)
        self.wheels_dir = Path(wheels_dir)
        
        # Git dependencies we want to build wheels for
        if git_packages is None:
            self.git_packages = ["kivymd", "gclib", "PyFastYaz0Yay0", "PyFastBTI"]
        else:
            self.git_packages = git_packages
        
    def build_git_wheels(self, force_rebuild: bool = False) -> None:
        """Build wheels from git dependencies and save to wheels directory
        
        Args:
            force_rebuild: If True, rebuild wheels even if they already exist
        """
        action = "Rebuilding" if force_rebuild else "Checking and building"
        print(f"{action} wheels from git dependencies...")
        
        if not self.requirements_file.exists():
            print(f"No {self.requirements_file} found")
            return
        
        self.wheels_dir.mkdir(exist_ok=True)
        
        # Check existing wheels
        existing_wheels = self._get_existing_wheels()
        
        # Parse requirements.txt to find git URLs
        git_requirements = self._parse_git_requirements()
        
        for pkg_name, git_req in git_requirements:
            pkg_name_lower = pkg_name.lower()
            
            # Check if we already have a wheel for this package (unless force rebuild)
            if not force_rebuild and pkg_name_lower in existing_wheels:
                print(f"Found existing wheel for {pkg_name}: {existing_wheels[pkg_name_lower].name}")
                continue
            
            try:
                if force_rebuild and pkg_name_lower in existing_wheels:
                    # Remove existing wheel before rebuilding
                    old_wheel = existing_wheels[pkg_name_lower]
                    print(f"Removing existing wheel: {old_wheel.name}")
                    old_wheel.unlink()
                
                print(f"Building wheel for {pkg_name} from {git_req}")
                
                # Build wheel using pip wheel
                subprocess.check_call([
                    sys.executable, "-m", "pip", "wheel",
                    "--wheel-dir", str(self.wheels_dir),
                    "--no-deps",  # Don't build dependencies, just the main package
                    "--no-cache-dir",  # Don't use cache to ensure fresh build
                    git_req
                ])
                print(f"Successfully built wheel for {pkg_name}")
                
            except subprocess.CalledProcessError as e:
                print(f"Failed to build wheel for {git_req}: {e}")
                # Continue with other packages even if one fails

    def install_from_wheels_first(self) -> List[str]:
        """Install git packages from wheels if available, return list of packages still needed
        
        Returns:
            List of package names that still need to be installed from git
        """
        print("Checking for git packages in wheels directory...")
        
        installed_from_wheels = []
        
        if not self.wheels_dir.exists():
            return self.git_packages
        
        # Check existing wheels
        existing_wheels = self._get_existing_wheels()
        
        # Try to install from wheels
        for pkg in self.git_packages:
            pkg_lower = pkg.lower()
            if pkg_lower in existing_wheels:
                wheel_file = existing_wheels[pkg_lower]
                try:
                    print(f"Installing {pkg} from wheel: {wheel_file.name}")
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install",
                        str(wheel_file), "--force-reinstall"
                    ])
                    installed_from_wheels.append(pkg)
                    print(f"Successfully installed {pkg} from wheel")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install {pkg} from wheel: {e}")
        
        # Return packages that still need to be installed from git
        remaining_packages = [pkg for pkg in self.git_packages if pkg not in installed_from_wheels]
        return remaining_packages

    def create_filtered_requirements(self) -> Optional[Path]:
        """Create a temporary requirements file without git packages that were installed from wheels
        
        Returns:
            Path to temporary filtered requirements file, or None if no requirements file exists
        """
        if not self.requirements_file.exists():
            return None
        
        # Get packages that still need git installation
        remaining_git_packages = self.install_from_wheels_first()
        
        # Read original requirements
        with open(self.requirements_file, 'r') as f:
            lines = f.readlines()
        
        # Filter out git requirements for packages we installed from wheels
        filtered_lines = []
        for line in lines:
            line_stripped = line.strip()
            if line_stripped and not line_stripped.startswith('#'):
                if 'git+https://' in line_stripped:
                    # Check if this git requirement is for a package we still need
                    should_keep = False
                    for pkg in remaining_git_packages:
                        if pkg.lower() in line_stripped.lower():
                            should_keep = True
                            break
                    if should_keep:
                        filtered_lines.append(line)
                else:
                    # Keep non-git requirements
                    filtered_lines.append(line)
            else:
                # Keep comments and empty lines
                filtered_lines.append(line)
        
        # Write filtered requirements to temp file
        temp_req_file = Path("requirements_filtered.txt")
        with open(temp_req_file, 'w') as f:
            f.writelines(filtered_lines)
        
        return temp_req_file

    def install_requirements(self, force_rebuild: bool = False) -> None:
        """Install requirements with wheel optimization
        
        Args:
            force_rebuild: If True, force rebuild of git dependency wheels
        """
        # First, build wheels for git dependencies (only if they don't exist or force rebuild)
        self.build_git_wheels(force_rebuild=force_rebuild)
        
        # Create filtered requirements file (installs from wheels first)
        temp_req_file = self.create_filtered_requirements()
        
        if temp_req_file and temp_req_file.exists():
            print("Installing requirements from filtered requirements file...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "-r", str(temp_req_file.absolute())
                ])
                print("Requirements installed successfully")
                # Clean up temp file
                temp_req_file.unlink()
            except subprocess.CalledProcessError as e:
                print(f"Failed to install requirements: {e}")
                # Clean up temp file even on failure
                if temp_req_file.exists():
                    temp_req_file.unlink()
        else:
            print("No requirements file to process")

    def _get_existing_wheels(self) -> Dict[str, Path]:
        """Get dictionary of existing wheels by package name
        
        Returns:
            Dictionary mapping lowercase package names to wheel file paths
        """
        existing_wheels = {}
        if self.wheels_dir.exists():
            for wheel_file in self.wheels_dir.glob("*.whl"):
                # Extract package name from wheel filename (format: package-version-python-abi-platform.whl)
                wheel_name = wheel_file.name
                pkg_name = wheel_name.split('-')[0].lower()
                existing_wheels[pkg_name] = wheel_file
        return existing_wheels

    def _parse_git_requirements(self) -> List[Tuple[str, str]]:
        """Parse requirements.txt to find git URLs for our packages
        
        Returns:
            List of tuples (package_name, git_requirement_line)
        """
        with open(self.requirements_file, 'r') as f:
            lines = f.readlines()
        
        git_requirements = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Look for git+ URLs or @ git+ patterns
                if 'git+https://' in line:
                    for pkg in self.git_packages:
                        if pkg.lower() in line.lower():
                            git_requirements.append((pkg, line))
                            break
        
        return git_requirements

    def list_wheels(self) -> List[Path]:
        """List all wheel files in the wheels directory
        
        Returns:
            List of wheel file paths
        """
        if not self.wheels_dir.exists():
            return []
        return list(self.wheels_dir.glob("*.whl"))

    def clean_wheels(self, package_names: Optional[List[str]] = None) -> None:
        """Remove wheel files
        
        Args:
            package_names: If provided, only remove wheels for these packages.
                          If None, remove all git package wheels.
        """
        if package_names is None:
            package_names = self.git_packages
        
        existing_wheels = self._get_existing_wheels()
        removed_count = 0
        
        for pkg_name in package_names:
            pkg_lower = pkg_name.lower()
            if pkg_lower in existing_wheels:
                wheel_file = existing_wheels[pkg_lower]
                print(f"Removing wheel: {wheel_file.name}")
                wheel_file.unlink()
                removed_count += 1
        
        print(f"Removed {removed_count} wheel file(s)")

    def add_git_package(self, package_name: str) -> None:
        """Add a package to the git packages list
        
        Args:
            package_name: Name of the package to add
        """
        if package_name not in self.git_packages:
            self.git_packages.append(package_name)
            print(f"Added {package_name} to git packages list")
        else:
            print(f"{package_name} is already in git packages list")

    def remove_git_package(self, package_name: str) -> None:
        """Remove a package from the git packages list
        
        Args:
            package_name: Name of the package to remove
        """
        if package_name in self.git_packages:
            self.git_packages.remove(package_name)
            print(f"Removed {package_name} from git packages list")
        else:
            print(f"{package_name} is not in git packages list")

    def get_git_packages(self) -> List[str]:
        """Get the current list of git packages
        
        Returns:
            List of git package names
        """
        return self.git_packages.copy()


def main():
    """Command line interface for wheel building"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Build and manage git dependency wheels')
    parser.add_argument('--rebuild', action='store_true', 
                       help='Force rebuild of all git dependency wheels')
    parser.add_argument('--build-only', action='store_true',
                       help='Only build wheels, do not install requirements')
    parser.add_argument('--list', action='store_true',
                       help='List existing wheels')
    parser.add_argument('--clean', action='store_true',
                       help='Remove all git package wheels')
    parser.add_argument('--show-packages', action='store_true',
                       help='Show current git packages being managed')
    parser.add_argument('--wheels-dir', default='default_wheels',
                       help='Directory for wheel files (default: default_wheels)')
    parser.add_argument('--requirements', default='requirements.txt',
                       help='Requirements file to process (default: requirements.txt)')
    parser.add_argument('--packages', nargs='*',
                       help='List of git package names to manage (default: kivymd gclib PyFastYaz0Yay0 PyFastBTI)')
    
    args = parser.parse_args()
    
    builder = GitWheelBuilder(
        requirements_file=args.requirements,
        wheels_dir=args.wheels_dir,
        git_packages=args.packages
    )
    
    if args.show_packages:
        packages = builder.get_git_packages()
        print("Current git packages being managed:")
        for pkg in packages:
            print(f"  - {pkg}")
        return
    
    if args.list:
        wheels = builder.list_wheels()
        if wheels:
            print("Existing wheels:")
            for wheel in wheels:
                print(f"  - {wheel.name}")
        else:
            print("No wheels found")
        return
    
    if args.clean:
        builder.clean_wheels()
        return
    
    if args.build_only:
        builder.build_git_wheels(force_rebuild=args.rebuild)
        return
    
    # Default: install requirements with wheel optimization
    builder.install_requirements(force_rebuild=args.rebuild)


if __name__ == "__main__":
    main()
