import os
import sys
import subprocess
import multiprocessing
import warnings
import json
import urllib.request
from pathlib import Path
from typing import List, Optional

# Version compatibility checks
if sys.platform in ("win32", "darwin") and sys.version_info < (3, 12, 0):
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. Official 3.12.+ is supported.")
elif sys.platform in ("win32", "darwin") and sys.version_info < (3, 12, 7):
    warnings.warn(f"Python Version {sys.version_info} has security issues. Don't use in production.")
elif sys.version_info < (3, 12, 0):
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. 3.12.+ is supported.")

# Skip update if environment is frozen/compiled or if not the parent process
_skip_update = bool(
    getattr(sys, "frozen", False) or 
    multiprocessing.parent_process()
)

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
local_dir = Path(__file__).parent
requirements_files = RequirementsSet({local_dir / "requirements.txt"})
wheels_files = RequirementsSet()

# Add wheel files if update hasn't run
if not update_ran:
    custom_wheels_dir = local_dir / "custom_wheels"
    if custom_wheels_dir.exists():
        for wheel_file in custom_wheels_dir.glob("*.whl"):
            wheels_files.add(str(wheel_file))


def check_pip() -> None:
    """Verify pip is available."""
    try:
        import pip  # noqa: F401
    except ImportError:
        raise RuntimeError("pip not available. Please install pip.")


def confirm(msg: str) -> None:
    """Get user confirmation for an action."""
    try:
        input(f"\n{msg}")
    except KeyboardInterrupt:
        print("\nAborting")
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


def check_for_updates() -> List[str]:
    """
    Check which packages need updates by querying PyPI.
    Returns a list of package names that need updating.
    """
    # Ensure packaging is available
    try:
        import packaging.requirements
    except ImportError:
        print("Warning: packaging module not available, installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "packaging"])
        import packaging.requirements
    
    try:
        response = subprocess.run(
            [sys.executable, "-m", "pip", "list", "-o", "--format", "json", 
             "-i", "https://pypi.org/simple", "--extra-index-url", 
             "https://pypi.multiworld.gg/mwgg/apworlds/+simple"],
            capture_output=True, text=True, timeout=45
        )
        
        if response.returncode != 0:
            print(f"Warning: Could not check for updates: {response.stderr}")
            return []
        
        outdated_packages = json.loads(response.stdout)
        
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
                            print(f"Skipping {pkg_name}: latest version {latest_version} doesn't satisfy requirement {requirement}")
                except Exception as e:
                    # If we can't parse the version, skip it
                    print(f"Skipping {pkg_name}: couldn't check version constraint: {e}")
            else:
                # Package not in requirements.txt, so we can update it
                packages_to_update.append(pkg_name)
        
        return packages_to_update
    
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Warning: Could not check for updates: {e}")
        return []


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
        print(f"Warning: Failed to fetch world modules from {url}: {e}")
        return []
    except Exception as e:
        print(f"Warning: Unexpected error while fetching world modules: {e}")
        return []

def install_world(world: str) -> None:
    """Install a single world from the multiworld repository."""
    check_pip()
    
    print(f"Installing world: {world}")
    result = subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "-i", "https://pypi.multiworld.gg/mwgg/apworlds", 
        world, "--upgrade"
    ])
    
    if result.returncode != 0:
        print(f"Warning: Failed to install {world}")


def update_world_wheels() -> None:
    """Install/update wheel files from custom_wheels directory."""
    check_pip()
    
    for wheel in wheels_files:
        print(f"Installing wheel: {wheel}")
        result = subprocess.run([sys.executable, "-m", "pip", "install", wheel, "--upgrade"])
        if result.returncode != 0:
            print(f"Warning: Failed to install wheel {wheel}")


def update_requirements(needed_packages: List[str]) -> None:
    """Update packages from requirements.txt files and install worlds."""
    check_pip()
    
    # Ensure packaging is available
    try:
        import packaging.requirements
    except ImportError:
        print("Warning: packaging module not available, installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "packaging"])
        import packaging.requirements
    
    # If needed_packages is empty, update all requirements (for force mode or missing requirements)
    update_all = len(needed_packages) == 0
    
    # Handle regular requirements from files
    for req_file in requirements_files:
        if not req_file.exists():
            print(f"Warning: Requirements file not found: {req_file}")
            continue
            
        print(f"Processing requirements from: {req_file}")
        requirements = parse_requirements_file(req_file)
        
        packages_to_update = []
        for req_line in requirements:
            try:
                requirement = packaging.requirements.Requirement(req_line)
                # Update if: force mode, package needs update, or package is missing
                if update_all or requirement.name in needed_packages:
                    packages_to_update.append(req_line)
            except packaging.requirements.InvalidRequirement:
                print(f"Warning: Invalid requirement line: {req_line}")
                continue
        
        if packages_to_update:
            print(f"Installing/updating packages: {[req.split('==')[0] if '==' in req else req.split('>=')[0] if '>=' in req else req for req in packages_to_update]}")
            for package in packages_to_update:
                result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", package])
                if result.returncode != 0:
                    print(f"Warning: Failed to install/update {package}")
        else:
            print("No packages from this requirements file need updating.")
    
    # Handle worlds (these are not in requirements.txt files)
    worlds_to_install = [pkg for pkg in needed_packages if pkg.startswith("worlds") or pkg == "mwgg_gui"]
    if worlds_to_install:
        print(f"Installing/updating worlds: {worlds_to_install}")
        for world in worlds_to_install:
            install_world(world)


def install_packaging(yes: bool = False) -> None:
    """Install packaging module if not available."""
    try:
        import packaging.requirements  # noqa: F401
    except ImportError:
        check_pip()
        if not yes:
            confirm("packaging not found, press enter to install it")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "packaging"])


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
            print(f"Warning: Requirements file not found: {req_file}")
            continue
        
        requirements = parse_requirements_file(req_file)
        
        for req_line in requirements:
            try:
                requirement = packaging.requirements.Requirement(req_line)
                try:
                    importlib.metadata.distribution(requirement.name)
                except importlib.metadata.PackageNotFoundError:
                    print(f"Missing requirement: {requirement.name}")
                    all_satisfied = False
                    if not yes:
                        confirm(f"Requirement {requirement.name} is not satisfied, press enter to install it")
            except packaging.requirements.InvalidRequirement:
                print(f"Warning: Invalid requirement line: {req_line}")
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
    global update_ran
    
    if update_ran:
        return
    
    update_ran = True
    
    if force:
        print("Force update requested - skipping update checks")
        # Force mode updates all requirements and worlds
        update_requirements([])  # Empty list means update all
        return
    
    # Check for available updates
    print("Checking for available updates...")
    available_updates = check_for_updates()
    
    # Add worlds to requirements if specified
    if worlds:
        for world in worlds:
            # Add world as a requirement to be processed
            if world not in available_updates:
                available_updates.append(world)
    
    if available_updates:
        print(f"Found updates for: {available_updates}")
        if not yes:
            confirm("Updates available. Press enter to continue with updates.")
    else:
        print("No updates found.")
    
    # Check if requirements are satisfied
    print("Checking if all requirements are satisfied...")
    if not check_requirements_satisfied(yes=yes):
        print("Installing missing requirements...")
        update_requirements([])  # Empty list means update all missing requirements
        return
    
    # Update packages that need updates (including worlds)
    if available_updates:
        print("Updating packages that need updates...")
        update_requirements(available_updates)
    
    # Update world wheels
    if wheels_files:
        print("Updating world wheels...")
        update_world_wheels()
    
    print("Update process completed.")


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
