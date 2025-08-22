import os
import sys
import subprocess
import multiprocessing
import warnings


if sys.platform in ("win32", "darwin") and sys.version_info < (3, 12, 0):
    # Official micro version updates. This should match the number in docs/running from source.md.
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. Official 3.12.+ is supported.")
elif sys.platform in ("win32", "darwin") and sys.version_info < (3, 12, 7):
    # There are known security issues, but no easy way to install fixed versions on Windows for testing.
    warnings.warn(f"Python Version {sys.version_info} has security issues. Don't use in production.")
elif sys.version_info < (3, 12, 0):
    # Other platforms may get security backports instead of micro updates, so the number is unreliable.
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. 3.12.+ is supported.")

# don't run update if environment is frozen/compiled or if not the parent process (skip in subprocess)
_skip_update = bool(
    getattr(sys, "frozen", False) or 
    multiprocessing.parent_process() or 
    os.environ.get("SKIP_REQUIREMENTS_UPDATE", "").lower() in ("1", "true", "yes")
)
update_ran = _skip_update


class RequirementsSet(set):
    def add(self, e):
        global update_ran
        update_ran &= _skip_update
        super().add(e)

    def update(self, *s):
        global update_ran
        update_ran &= _skip_update
        super().update(*s)


local_dir = os.path.dirname(__file__)
requirements_files = RequirementsSet((os.path.join(local_dir, 'requirements.txt'),))
wheels_files = RequirementsSet()

if not update_ran:
    for entry in os.scandir(os.path.join(local_dir, "worlds")):
        # skip .* (hidden / disabled) folders
        if not entry.name.startswith("."):
            if entry.is_dir():
                req_file = os.path.join(entry.path, "requirements.txt")
                if os.path.exists(req_file):
                    requirements_files.add(req_file)
                elif entry.name == "Wheels":
                    for wheel in os.listdir(os.path.join(local_dir, "worlds", "Wheels")):
                        if wheel.endswith(".whl"):
                            wheels_files.add(os.path.join(local_dir, "worlds", "Wheels", wheel))

def check_pip():
    # detect if pip is available
    try:
        import pip  # noqa: F401
    except ImportError:
        raise RuntimeError("pip not available. Please install pip.")


def confirm(msg: str):
    try:
        input(f"\n{msg}")
    except KeyboardInterrupt:
        print("\nAborting")
        sys.exit(1)

def update_worlds(worlds: list[str]):
    '''
    Update the world modules that we need from pypi wheels.
    Check global pypi first, if it is hasn't been pushed there, 
    install from the multiworld pypi repository.
    '''
    check_pip()
    for world in worlds:
        # TODO: Commented out until public beta because we know that there aren't any worlds on pypi yet
        # pypi_response = subprocess.call([sys.executable, "-m", "pip", "install", world, "--upgrade"])
        # if pypi_response == 1:
        subprocess.call([sys.executable, "-m", "pip", "install", "-i", "https://pypi.multiworld.gg/mwgg/apworlds", world, "--upgrade"])

def update_world_wheels():
    check_pip()
    for wheel in wheels_files:
        subprocess.call([sys.executable, "-m", "pip", "install", wheel, "--upgrade", "--target", os.path.join(local_dir, "worlds", "Lib")])

def update_command():
    check_pip()
    for file in requirements_files:
        subprocess.call([sys.executable, "-m", "pip", "install", "-r", file, "--upgrade"])


def install_packaging(yes=False):
    try:
        import packaging.requirements 
    except ImportError:
        check_pip()
        if not yes:
            confirm("packaging not found, press enter to install it")
        subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "packaging"])


def update(yes: bool = True, force: bool = False, worlds: list[str] = None) -> None:
    global update_ran
    if not update_ran:
        update_ran = True

        if force:
            if worlds:
                update_worlds(worlds)
            update_command()
            return

        install_packaging(yes=yes)
        import packaging.requirements
        import importlib.metadata

        update_world_wheels() #install wheels if they aren't

        if worlds:
            update_worlds(worlds)

        prev = ""  # if a line ends in \ we store here and merge later
        for req_file in requirements_files:
            path = os.path.join(os.path.dirname(sys.argv[0]), req_file)
            if not os.path.exists(path):
                path = os.path.join(os.path.dirname(__file__), req_file)
            with open(path) as requirementsfile:
                for line in requirementsfile:
                    if not line or line.lstrip(" \t")[0] == "#":
                        if not prev:
                            continue  # ignore comments
                        line = ""
                    elif line.rstrip("\r\n").endswith("\\"):
                        prev = prev + line.rstrip("\r\n")[:-1] + " "  # continue on next line
                        continue
                    line = prev + line
                    line = line.split("--hash=")[0]  # remove hashes from requirement for version checking
                    prev = ""
                    if line.startswith(("https://", "git+https://")):
                        # extract name and version for url
                        rest = line.split('/')[-1]
                        line = ""
                        if "#egg=" in rest:
                            # from egg info
                            rest, egg = rest.split("#egg=", 1)
                            egg = egg.split(";", 1)[0].rstrip()
                            if any(compare in egg for compare in ("==", ">=", ">", "<", "<=", "!=")):
                                warnings.warn(f"Specifying version as #egg={egg} will become unavailable in pip 25.0. "
                                              "Use name @ url#version instead.", DeprecationWarning)
                                line = egg
                        else:
                            egg = ""
                        if "@" in rest and not line:
                            raise ValueError("Can't deduce version from requirement")
                        elif not line:
                            # from filename
                            rest = rest.replace(".zip", "-").replace(".tar.gz", "-")
                            name, version, _ = rest.split("-", 2)
                            line = f'{egg or name}=={version}'
                    elif "@" in line and "#" in line:
                        # PEP 508 does not allow us to specify a version, so we use custom syntax
                        # name @ url#version ; marker
                        name, rest = line.split("@", 1)
                        version = rest.split("#", 1)[1].split(";", 1)[0].rstrip()
                        line = f"{name.rstrip()}=={version}"
                        if ";" in rest:  # keep marker
                            line += rest[rest.find(";"):]
                    
                    # Skip empty lines or lines that don't look like requirements
                    if not line.strip():
                        continue
                    
                    try:
                        requirement = packaging.requirements.Requirement(line)
                        try:
                            importlib.metadata.distribution(requirement.name)
                        except importlib.metadata.PackageNotFoundError:
                            if not yes:
                                import traceback
                                traceback.print_exc()
                                confirm(f"Requirement {requirement.name} is not satisfied, press enter to install it")
                            update_command()
                            return
                    except packaging.requirements.InvalidRequirement:
                        # Skip invalid requirement lines (like comments, empty lines, etc.)
                        continue
    if force:
        if worlds:
            update_worlds(worlds)
        update_world_wheels()
    return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Install archipelago requirements')
    parser.add_argument('-y', '--yes', dest='yes', action='store_true', help='answer "yes" to all questions')
    parser.add_argument('-f', '--force', dest='force', action='store_true', help='force update')
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
