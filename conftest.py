"""Pytest rootdir conftest.

Loaded by pytest before any test modules are collected. We prepend
`test/_stubs/` to `sys.path` so that test code importing `mwgg_igdb` resolves
to the in-repo stub instead of trying to import the real (network-installed)
package. See `test/_stubs/mwgg_igdb.py` for the stub itself.
"""
import os
import sys
from pathlib import Path

_stub_dir = str(Path(__file__).parent / "test" / "_stubs")
if _stub_dir not in sys.path:
    sys.path.insert(0, _stub_dir)


def pytest_configure(config):
    # AP_TEST_WORLDS implies `-m world` unless an explicit -m was given; the scoping itself lives in
    # test/__init__
    if os.environ.get("AP_TEST_WORLDS") and not config.option.markexpr:
        config.option.markexpr = "world"


def pytest_ignore_collect(collection_path, config):
    # skip worlds/<world>/... for any world not named, so other worlds are never imported
    env = os.environ.get("AP_TEST_WORLDS")
    if not env:
        return None
    selected = {name.strip() for name in env.split(",") if name.strip()}
    parts = collection_path.parts
    if "worlds" in parts:
        i = parts.index("worlds")
        if i + 1 < len(parts) and parts[i + 1] not in selected:
            return True
    return None


def pytest_collection_modifyitems(items):
    # mark for `-m world`: classes with `world_relevant = True`, plus anything under worlds/ (nodeid is
    # always "/"-separated and relative to rootdir)
    for item in items:
        if getattr(getattr(item, "cls", None), "world_relevant", False) or \
                item.nodeid.split("/", 1)[0] == "worlds":
            item.add_marker("world")
