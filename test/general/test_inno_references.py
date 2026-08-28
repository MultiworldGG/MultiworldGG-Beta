"""Lint inno_setup.iss for {app}\\<name>.exe references setup.py doesn't build.

The allowed set is derived, not hand-maintained: every literal target_name in
setup.py, every BaseUtils.FROZEN_TARGETS value, plus the LauncherDebug name
setup.py derives at build time (it has no FROZEN_TARGETS entry of its own).
"""
import re

import BaseUtils
import Utils

_INNO_PATH = Utils.local_path("inno_setup.iss")
_SETUP_PY_PATH = Utils.local_path("setup.py")

# Historically stale exe names, kept as an explicit regression guard on top of the
# derived allow-list (a name could start being built for unrelated reasons).
_KNOWN_STALE_NAMES = {
    "MultiworldGGBizHawkClient",
    "MultiworldGGSNIClient",
    "ArchipelagoBizHawkClient",
}


def _setup_py_target_names() -> set[str]:
    with open(_SETUP_PY_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    names: set[str] = set()
    for line in text.splitlines():
        if "target_name" not in line:
            continue
        for match in re.findall(r'"([^"]+)"', line):
            names.add(match[:-4] if match.endswith(".exe") else match)
    return names


def _known_built_exe_names() -> set[str]:
    """Every exe base name (no .exe) that setup.py is known to build."""
    names = _setup_py_target_names() | set(BaseUtils.FROZEN_TARGETS.values())
    # LauncherDebug is derived in setup.py (_launcher_debug_exe_name), never a
    # quoted literal, so _setup_py_target_names() can't see it.
    names.add(BaseUtils.FROZEN_TARGETS["Launcher"] + "Debug")
    names.discard("")
    return names


def _inno_exe_references() -> list[str]:
    with open(_INNO_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    return re.findall(r"\{app\}\\(\w+\.exe)", text)


def test_inno_exe_references_resolve_to_a_built_executable():
    allowed = {f"{name}.exe" for name in _known_built_exe_names()}
    references = _inno_exe_references()
    assert references, "expected to find at least one {app}\\<name>.exe reference in inno_setup.iss"

    stale = sorted(set(references) - allowed)
    assert not stale, (
        f"inno_setup.iss references exe(s) setup.py doesn't build: {stale}. "
        f"Known-built names: {sorted(allowed)}"
    )


def test_inno_has_no_known_stale_exe_references():
    references = {ref[:-4] for ref in _inno_exe_references()}
    stale_hits = references & _KNOWN_STALE_NAMES
    assert not stale_hits, f"inno_setup.iss still references retired exe(s): {sorted(stale_hits)}"


def test_inno_app_exe_name_is_the_launcher():
    with open(_INNO_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    match = re.search(r'#define MyAppExeName "([^"]+)"', text)
    assert match, "expected a #define MyAppExeName line in inno_setup.iss"
    assert match.group(1) == f"{BaseUtils.FROZEN_TARGETS['Launcher']}.exe"
