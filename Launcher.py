"""Thin entry point for the standalone MultiworldGG Launcher process.

Built as MultiworldGGLauncher(.exe). Dispatch, in order:

1. --version / --help answer immediately, before any heavy import -- CI smokes
   this entry point headless on Linux, so nothing that pulls in Kivy (or
   MultiWorld, worlds.*) may load for --version.
2. --frontend=tui is rejected: the process split is GUI-only; the terminal
   client lives in the client entry point (MultiWorldGG --frontend=tui).
3. A positional matching a launcher component (display_name or script_name,
   e.g. "Text Client") runs that component headless, then waits for anything
   it spawned via multiprocessing before exiting.
4. Everything else delegates to MultiWorld.main(): a patch file / .apworld /
   archipelago:// URL positional routes exactly as it would double-clicked on
   the client exe, and a bare invocation opens the launcher UI.

On the delegation path argv is forwarded to MultiWorld.main() verbatim -- this
module consumed nothing from it, so there is no double parsing to reconcile.
"""
import sys

_HELP = """\
usage: MultiworldGGLauncher [-h] [--version] [PATCH_FILE|COMPONENT|URL] [ARGS ...]

MultiworldGG Launcher: opens the launcher window, runs a launcher component
headless, or routes a patch file / launch URL to the right client.

positional arguments:
  PATCH_FILE|COMPONENT|URL
                        a launcher component name (e.g. "Text Client"), a
                        patch file or .apworld, or an archipelago:// launch URL
  ARGS                  extra arguments passed to the matched component

options:
  -h, --help            show this help message and exit
  --version             print the MultiworldGG version and exit

Anything else (e.g. --game/--server-address) is forwarded to the client entry
point (MultiWorld.py). --frontend=tui is not supported by the Launcher; use
the client entry point for the terminal frontend.
"""


def _version_string() -> str:
    import BaseUtils
    return f"{BaseUtils.instance_name} {BaseUtils.__version__}"


def _requests_tui(argv: "list[str]") -> bool:
    """Detect --frontend=tui / --frontend tui without argparse: the value token
    of the pair form would otherwise be mistaken for our positional."""
    for index, token in enumerate(argv):
        if token == "--frontend=tui":
            return True
        if token == "--frontend" and index + 1 < len(argv) and argv[index + 1] == "tui":
            return True
    return False


def main(argv: "list[str] | None" = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if "--version" in argv:
        print(_version_string())
        return 0
    if "-h" in argv or "--help" in argv:
        print(_HELP, end="")
        return 0
    if _requests_tui(argv):
        import BaseUtils
        client = BaseUtils.FROZEN_TARGETS["MultiWorld"] + (".exe" if BaseUtils.is_windows else "")
        print("The standalone Launcher is GUI-only and cannot host the TUI.\n"
              f"Run the client entry point instead: {client} --frontend=tui "
              "(MultiWorld.py --frontend=tui from source).", file=sys.stderr)
        return 2

    if argv and not argv[0].startswith("-"):
        from worlds.LauncherComponents import find_component, processes, run_component
        component = find_component(argv[0])
        if component is not None:
            from Utils import init_logging
            init_logging("Launcher")
            run_component(component, *argv[1:])
            for process in processes:
                process.join()
            return 0

    # Patch/URL positionals become MultiWorld's launch_file; a bare invocation
    # computes to launcher role there.
    import MultiWorld
    MultiWorld.main(argv)
    return 0


if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    raise SystemExit(main())
