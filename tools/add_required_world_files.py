#!/usr/bin/env python3
"""
Script to add pyproject.toml and _whl_bld_iface.py drop-ins to existing world
directories.

The world's __init__.py is parsed (via ast) for `Component(..., func=NAME, ...)`
calls. The first CLIENT-typed Component's `func=` name is used as the launch
callable; the templater wires it up through `_whl_bld_iface.CLIENT_FUNCTION`,
which the entry point in pyproject.toml references.

This is a one-time generation per world per release; the resulting drop-ins are
committed/pushed to the per-world repo's wheel branch and reused on subsequent
rebuilds, so the templater never needs to import the world.
"""

import argparse
import ast
import sys
from pathlib import Path
from typing import Optional

from world_manifest import get_apworld_manifest


PYPROJECT_TEMPLATE = """[project]
name = "worlds.{module_name}"
version = "{version}"
description = "MultiWorld: {game_name}"
classifiers = ["Private :: Do Not Upload"]
requires-python = ">=3.13"
{authors_section}
{client_section}

[tool.setuptools.packages.find]
where = ["src"]
include = ["worlds.{module_name}"]
namespaces = true
"""


WHL_BLD_IFACE_TEMPLATE_WITH_CLIENT = '''\
# Auto-generated. Do not edit.
"""Interface from pyproject.toml entry points to the worlds.{module_name} module."""

from . import {func_name}

CLIENT_FUNCTION = {func_name}
'''


WHL_BLD_IFACE_TEMPLATE_NO_CLIENT = '''\
# Auto-generated. Do not edit.
"""Interface from pyproject.toml entry points to the worlds.{module_name} module."""

CLIENT_FUNCTION = None
'''


def _is_client_component_call(call: ast.Call) -> bool:
    """Return True if `call` is a Component(...) registration of type CLIENT.

    Matches both `Component(...)` and `<anything>.Component(...)` callees.
    Components with no `component_type` keyword default to CLIENT.
    """
    callee = call.func
    if isinstance(callee, ast.Name):
        if callee.id != "Component":
            return False
    elif isinstance(callee, ast.Attribute):
        if callee.attr != "Component":
            return False
    else:
        return False

    for kw in call.keywords:
        if kw.arg != "component_type":
            continue
        # component_type=Type.CLIENT or component_type=ComponentType.CLIENT
        if isinstance(kw.value, ast.Attribute):
            return kw.value.attr == "CLIENT"
        # component_type=CLIENT (bare name)
        if isinstance(kw.value, ast.Name):
            return kw.value.id == "CLIENT"
        # Any other shape: not a static CLIENT
        return False

    # No component_type kwarg present: defaults to CLIENT.
    return True


def find_client_func(init_path: Path) -> Optional[str]:
    """Walk __init__.py and return the name passed as `func=` to the first
    CLIENT-typed Component(...) call, or None if no such call has a plain-name
    func value.
    """
    tree = ast.parse(init_path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not _is_client_component_call(node):
            continue

        for kw in node.keywords:
            if kw.arg != "func":
                continue
            if isinstance(kw.value, ast.Name):
                return kw.value.id
            # func=lambda ... or func=foo.bar — not resolvable as a top-level
            # symbol; treat this Component as having no extractable func and
            # keep searching for a later CLIENT Component that does.
            break

    return None


def create_world_files(module_name: str, overwrite: bool = False):
    """Create pyproject.toml and _whl_bld_iface.py for an existing world dir."""

    module_name = module_name.lower()

    src_dir = Path(__file__).parent.parent
    target_dir = src_dir / "worlds" / module_name

    if not target_dir.exists():
        print(f"Error: World directory '{target_dir}' does not exist.")
        return False

    manifest = get_apworld_manifest(module_name)
    game_name = manifest.get("game", "Unknown")
    authors = manifest.get("authors", ["Unknown"])
    version = manifest.get("world_version", "0.0.1")

    func_name = find_client_func(target_dir / "__init__.py")
    if func_name is not None:
        client_section = (
            f'\n[project.entry-points."mwgg.client"]\n'
            f'"worlds.{module_name}.Client" = '
            f'"worlds.{module_name}._whl_bld_iface:CLIENT_FUNCTION"'
        )
        iface_content = WHL_BLD_IFACE_TEMPLATE_WITH_CLIENT.format(
            module_name=module_name, func_name=func_name
        )
    else:
        client_section = ""
        iface_content = WHL_BLD_IFACE_TEMPLATE_NO_CLIENT.format(module_name=module_name)

    pyproject_path = target_dir / "pyproject.toml"
    iface_path = target_dir / "_whl_bld_iface.py"

    pyproject_content = PYPROJECT_TEMPLATE.format(
        module_name=module_name,
        version=version,
        game_name=game_name,
        authors_section="\n".join(
            [f'[[project.authors]]\nname = "{author}"' for author in authors]
        ),
        client_section=client_section,
    )

    for path, content in ((pyproject_path, pyproject_content), (iface_path, iface_content)):
        if path.exists() and not overwrite:
            print(f"Skipping {path} - already exists (use --overwrite to replace)")
            continue
        try:
            path.write_text(content, encoding="utf-8")
            print(f"Created {path}")
        except Exception as e:
            print(f"Error writing {path}: {e}")
            return False

    print(f"\nSuccessfully created files for world '{module_name}'")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Add template files to an existing world directory"
    )
    parser.add_argument(
        "module_name",
        help="Name of the world directory (e.g., 'tloz', 'oot')"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files if they exist"
    )
    args = parser.parse_args()

    success = create_world_files(args.module_name, args.overwrite)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
