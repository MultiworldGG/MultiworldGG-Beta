"""Worlds venv and world install management.

Owns the per-user uv-managed worlds venv, the mwgg_igdb index package, and
per-world wheel/apworld installs. Importing this module has side effects, in
this order: read-only venv probe -> skip-flag computation -> custom_worlds
scan -> venv create/repair + sys.path insert -> installer wheel_cache
(variant marker, mwgg_igdb bootstrap, cached-wheel install).

Mutable module globals (update_ran, requirements_files, worlds_files,
custom_worlds_dir, python_cmd, the MWGG_IGDB_* trio) are public API: callers
and tests read and write them through the module namespace.
"""

import sys
import os
import subprocess
import multiprocessing
import json
import re
import shutil
import time
import datetime
import zipfile
import tarfile
import logging
import tempfile
import contextlib
import errno
import importlib.metadata
import importlib.util
import urllib.request

logger = logging.getLogger("Update")

# Fallback for entry points that call update() before their own init_logging.
if not logging.getLogger().hasHandlers() and sys.stdout:
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stdout)

from pathlib import Path
from collections.abc import Iterable
from typing import Any, List, Optional, TypeVar, cast, override

from importlib import invalidate_caches
from BaseUtils import local_path, mwgg_venv_site_packages, use_worlds_venv, is_frozen


# ── Platform & paths ─────────────────────────────────────────────────────────

def is_windows() -> bool:
    return sys.platform in ("win32", "cygwin", "msys")


def is_macos() -> bool:
    return sys.platform == "darwin"


def is_linux() -> bool:
    return sys.platform.startswith("linux")


def install_path() -> Path:
    """Per-user worlds venv location (frozen builds)."""
    if is_windows():
        return Path.home() / "AppData" / "Local" / "MultiworldGG" / "mwgg_venv"
    elif is_macos():
        return Path.home() / "Library" / "Application Support" / "MultiworldGG" / "mwgg_venv"
    elif is_linux():
        return Path.home() / ".local" / "share" / "MultiworldGG" / "mwgg_venv"
    else:
        raise RuntimeError("Unsupported platform")


if (is_windows() or is_macos()) and sys.version_info < (3, 13, 0):
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. Official 3.13.+ is supported.")
elif sys.version_info < (3, 13, 0):
    raise RuntimeError(f"Incompatible Python Version found: {sys.version_info}. 3.13.+ is supported.")


# ── Install gating ───────────────────────────────────────────────────────────

def _worlds_venv_is_readonly() -> bool:
    """True when the worlds venv lives on a read-only mount (e.g. a Docker `:ro`
    bind mount). Such consumers must never attempt installs; the mwgg_upgrader
    service is the sole writer of the venv."""
    if not use_worlds_venv():
        return False
    venv_dir = install_path()
    try:
        venv_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=venv_dir):
            pass
    except OSError as e:
        logger.warning(f"Worlds venv at {venv_dir} not writable ({e!r}); "
                       "treating as read-only (installs disabled).")
        return True
    return False


# Detected once at import: a read-only worlds venv disables every install path
# below (like SKIP_ALL_INSTALLS), so consumers can't crash writing the upgrader-owned venv.
_VENV_READONLY = _worlds_venv_is_readonly()
if _VENV_READONLY:
    logger.info("Worlds venv is read-only; installs disabled (mwgg_upgrader owns writes).")


def _skip_all_installs() -> bool:
    """Installs are off via explicit env opt-out or a read-only worlds venv."""
    return bool(os.environ.get("SKIP_ALL_INSTALLS")) or _VENV_READONLY


# True in spawned children (any multiprocessing child not named "MultiworldGG",
# splash included) and under the env opt-outs. Gates the custom_worlds scan and
# the dev pipeline in _update_locked; update_worlds() ignores it on purpose so
# the splash child can run the world update.
_skip_update = bool(
    (multiprocessing.parent_process() and multiprocessing.current_process().name != "MultiworldGG")
    or os.environ.get("SKIP_REQUIREMENTS_UPDATE", "")
    or _skip_all_installs()
)

update_ran = _skip_update

_T = TypeVar("_T")


# ── Mutable public state ─────────────────────────────────────────────────────

class RequirementsSet(set[_T]):
    """Set that re-arms the updater (update_ran) whenever a file is added."""

    @override
    def add(self, e: _T) -> None:
        global update_ran
        update_ran &= _skip_update
        super().add(e)

    @override
    def update(self, *s: Iterable[_T]) -> None:
        global update_ran
        update_ran &= _skip_update
        super().update(*s)


# Core requirements.txt doubles as a constraint file for every requirements
# install below, so additional files can't upgrade core deps past its pins.
core_constraints: Path = Path(local_path("requirements.txt"))
requirements_files: RequirementsSet[Path] = RequirementsSet({core_constraints})
worlds_files: dict[str, RequirementsSet[str]] = {"wheels": RequirementsSet(), "apworlds": RequirementsSet()}


# custom_worlds lives next to the executable / source checkout: single source of
# truth for the launch scan. Do NOT special-case frozen builds to write_path(),
# or custom worlds silently stop being selectable.
def _resolve_custom_worlds_dir() -> Path:
    return Path(local_path("custom_worlds"))


custom_worlds_dir = _resolve_custom_worlds_dir()

try:
    custom_worlds_dir.mkdir(parents=True, exist_ok=True)
except OSError:
    pass  # best-effort; read-only filesystems tolerated


def _scan_custom_worlds() -> None:
    """Register .whl/.apworld files in custom_worlds_dir into worlds_files.

    Skipped once a full update has run. Tests monkeypatch the module globals
    and call this directly.
    """
    if update_ran or not custom_worlds_dir.exists():
        return
    for world_file in custom_worlds_dir.glob("*.whl"):
        worlds_files["wheels"].add(str(world_file))
    for world_file in custom_worlds_dir.glob("*.apworld"):
        worlds_files["apworlds"].add(str(world_file))


_scan_custom_worlds()


# ── uv runner ────────────────────────────────────────────────────────────────

# Default for dev mode (not frozen): use the running interpreter and let uv install into its venv.
python_cmd = sys.executable

_uv_resolved_path: Optional[Path] = None
_uv_unavailable: bool = False


def _uv_candidate_paths() -> list[Path]:
    """uv lookup order; fixed list, no filesystem hunting."""
    candidates: list[Path] = []
    # Frozen builds on Linux/macOS ship uv next to the executable
    if is_frozen():
        exe_dir = Path(sys.executable).parent
        if is_macos():
            import platform
            arch = platform.machine()  # "arm64" on Apple Silicon, "x86_64" on Intel
            candidates.append(exe_dir / f"uv-{arch}")
        elif not is_windows():
            candidates.append(exe_dir / "uv")
    candidates.append(Path("uv"))  # PATH lookup
    if is_windows():
        candidates += [
            Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links" / "uv.exe",  # winget shim
            Path.home() / ".local" / "bin" / "uv.exe",                          # astral PS installer
        ]
        try:
            # The Links shim is an AppExecLink some tokens can't stat/exec (WinError 448);
            # the actual winget-installed PE is a plain file that works in any token.
            packages_dir = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages"
            candidates += sorted(packages_dir.glob("astral-sh.uv_*/**/uv.exe"))
        except OSError:
            pass
    else:
        candidates += [
            Path.home() / ".local" / "bin" / "uv",     # astral installer / pipx
            Path("/opt/homebrew/bin/uv"),              # Homebrew (Apple Silicon)
            Path("/usr/local/bin/uv"),                 # Homebrew (Intel) / generic
        ]
    return candidates


def _uv_pip(*args: str) -> list[str]:
    return ["pip", *args, "--python", str(python_cmd)]


def _uv_run(args: list[str], timeout: float = 120, check: bool = False) -> subprocess.CompletedProcess[str]:
    """Run `uv <args>` against the first reachable uv binary."""
    global _uv_resolved_path, _uv_unavailable

    # Windows-only: new process group + no console window so uv can't flash a
    # window or steal the parent's Ctrl-C; 0 is the no-op default elsewhere.
    creationflags = (
        subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
        if is_windows() else 0
    )

    if _uv_unavailable:
        return subprocess.CompletedProcess(args, 127, "", "uv not found at any known path")

    candidates = [_uv_resolved_path] if _uv_resolved_path else _uv_candidate_paths()

    for cand in candidates:
        cmd = [cand] + args
        try:
            result = subprocess.run(
                cmd,
                check=check,
                capture_output=True,
                # uv emits UTF-8 (box-drawing error art); the locale default
                # (cp1252 on Windows) mis-decodes it into undecodable bytes
                # for anything re-reading our log stream.
                encoding="utf-8",
                errors="replace",
                stdin=subprocess.DEVNULL,
                timeout=timeout,
                creationflags=creationflags,
            )
        except OSError as e:
            # Candidate unusable; try next.
            logger.debug(f"uv not usable at {cand} ({e!r}); trying next candidate")
            continue
        if _uv_resolved_path is None:
            _uv_resolved_path = cand
            logger.debug(f"Using uv at {cand}")
        return result

    _uv_unavailable = True
    if is_windows():
        install_hint = (
            "install uv via `winget install astral-sh.uv`, "
            "`irm https://astral.sh/uv/install.ps1 | iex`, or `choco install uv`"
        )
    else:
        install_hint = "install uv via `curl -LsSf https://astral.sh/uv/install.sh | sh`"
    logger.warning(
        "uv not found at any known install path. Worlds cannot be pre-installed; "
        f"they will be installed on demand when needed. To pre-install, {install_hint}."
    )
    return subprocess.CompletedProcess(args, 127, "", "uv not found at any known path")


# ── Worlds-venv bootstrap ────────────────────────────────────────────────────

def venv_is_healthy(venv_path: Path) -> bool:
    """True if the venv's interpreter actually runs.

    No pre-probes: stat()-ing the venv's `home =` (a uv-managed python) raises
    OSError on untraversable mounts (WinError 448); just run the interpreter and
    treat any failure as unhealthy so the caller recreates.
    """
    venv_python = venv_path / ("Scripts" if is_windows() else "bin") / ("python.exe" if is_windows() else "python")
    try:
        return subprocess.run([str(venv_python), "--version"], capture_output=True, timeout=10).returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


_venv_just_created = False

if use_worlds_venv():
    # Route worlds + mwgg_igdb into a dedicated venv under user data
    if is_frozen():
        exe_dir = Path(sys.exec_prefix)
        default_libs_dir = Path(exe_dir, "lib")
        if str(default_libs_dir) not in sys.path:
            sys.path.append(str(default_libs_dir))

    venv_path = install_path()
    venv_ready = True
    if not venv_is_healthy(venv_path):
        # Any failure must degrade to "install on demand later", never crash
        # the import: this runs at module load for every consumer.
        try:
            venv_path.mkdir(parents=True, exist_ok=True)
            if any(venv_path.iterdir()):
                logger.info(f"Repairing stale venv at {venv_path} via uv (site-packages preserved).")
            else:
                logger.info(f"Creating venv at {venv_path} via uv.")
            # uv reuses an existing system Python 3.13 if one is present; otherwise it
            # downloads python-build-standalone.
            venv_result = _uv_run(
                ["venv", str(venv_path), "--allow-existing", "--python", "3.13"],
                timeout=600,
            )
            venv_ready = venv_result.returncode == 0
            _venv_just_created = venv_ready
        except Exception as e:
            logger.debug(f"Worlds venv setup failed: {e!r}")
            venv_ready = False
        if not venv_ready:
            logger.warning(
                "Could not create the worlds venv. Worlds will be installed on demand "
                "the next time uv is available."
            )

    if venv_ready:
        python_cmd = venv_path / ("Scripts" if is_windows() else "bin") / ("python.exe" if is_windows() else "python")

        # Make worlds-venv packages (mwgg_igdb etc.) importable from this process.
        site_packages = mwgg_venv_site_packages()
        if site_packages not in sys.path:
            sys.path.insert(0, site_packages)


# ── mwgg_igdb index & variants ───────────────────────────────────────────────

# mwgg_igdb package source: orphan branch on the Index repo, fetched as GitHub's source
# tarball -- a `git+` URL makes uv shell out to a git executable that end users lack.
# See MultiworldGG-Index/scripts/build_variants.py for variant definitions.
DEFAULT_MWGG_IGDB_VARIANT = "sixteen"  # ultimate fallback when nothing is installed
_VARIANTS = ("nr", "ao", "twelve", "sixteen")
_EXPLICIT_VARIANT: Optional[str] = None  # set via set_variant(); wins over detection
MWGG_INDEX_REPO = "MultiworldGG/MultiworldGG-Index"


def _index_archive_url(ref: str) -> str:
    """Source tarball URL for `ref` (`heads/<branch>` or `tags/<tag>`) on the Index repo."""
    return f"https://github.com/{MWGG_INDEX_REPO}/archive/refs/{ref}.tar.gz"


# The three globals below mirror the currently *resolved* variant. _resolve_variant()
# keeps them consistent; callers should treat them as read-only.
MWGG_IGDB_VARIANT = DEFAULT_MWGG_IGDB_VARIANT
MWGG_IGDB_BRANCH = f"game_index_{MWGG_IGDB_VARIANT}"
MWGG_IGDB_URL = _index_archive_url(f"heads/{MWGG_IGDB_BRANCH}")


def _detect_installed_variant() -> Optional[str]:
    """Return the variant currently installed locally, or None if undetectable.

    Reads the `__variant__` constant the Index build bakes into the generated
    `mwgg_igdb` module. Absent (pre-`__variant__` build) or unimportable → None,
    and callers fall back to DEFAULT_MWGG_IGDB_VARIANT.
    """
    if importlib.util.find_spec("mwgg_igdb") is None:
        return None
    try:
        import mwgg_igdb
    except ImportError:
        return None
    variant = getattr(mwgg_igdb, "__variant__", None)
    if isinstance(variant, str) and variant in _VARIANTS:
        return variant
    return None


def _resolve_variant() -> str:
    """Pick the variant to act on, refresh the derived globals, and return it.

    Precedence: explicit `set_variant()` > detected install > default fallback.
    """
    global MWGG_IGDB_VARIANT, MWGG_IGDB_BRANCH, MWGG_IGDB_URL
    if _EXPLICIT_VARIANT is not None:
        variant = _EXPLICIT_VARIANT
    else:
        variant = _detect_installed_variant() or DEFAULT_MWGG_IGDB_VARIANT
    # Public globals, intentionally reassigned (callers and tests read them).
    MWGG_IGDB_VARIANT = variant  # pyright: ignore[reportConstantRedefinition]
    MWGG_IGDB_BRANCH = f"game_index_{variant}"  # pyright: ignore[reportConstantRedefinition]
    MWGG_IGDB_URL = _index_archive_url(f"heads/{MWGG_IGDB_BRANCH}")  # pyright: ignore[reportConstantRedefinition]
    return variant


def set_variant(variant: str) -> None:
    """Switch the runtime mwgg_igdb variant; takes effect on next install_mwgg_igdb call."""
    global _EXPLICIT_VARIANT
    _EXPLICIT_VARIANT = variant  # pyright: ignore[reportConstantRedefinition]  # override sentinel
    _resolve_variant()


def _parse_variant_token(token: str) -> Optional[str]:
    """Return the variant name if `token` is `mwgg_igdb` or `mwgg_igdb_<variant>`, else None.

    Bare `mwgg_igdb` maps to the canonical default `sixteen`. Inno Setup passes
    one of these tokens in the `--worlds` list to select the parental-rating gate.
    """
    if token == "mwgg_igdb":
        return "sixteen"
    prefix = "mwgg_igdb_"
    if token.startswith(prefix):
        variant = token[len(prefix):]
        if variant in _VARIANTS:
            return variant
    return None


def _igdb_install_date() -> Optional[datetime.date]:
    """Local date `mwgg_igdb` was last written to disk, or None if not installed.

    The module file's mtime is the package's own install datestamp (set fresh
    every time uv (re)installs it), so no separate stamp file is needed.
    """
    spec = importlib.util.find_spec("mwgg_igdb")
    if spec is None or not spec.origin or not os.path.exists(spec.origin):
        return None
    return datetime.date.fromtimestamp(os.path.getmtime(spec.origin))


def _igdb_upgraded_recently() -> bool:
    """True when an upgrade pull would be a no-op: mwgg_igdb was installed today."""
    # force=True callers (variant switches, CLI) bypass this throttle entirely.
    install_date = _igdb_install_date()
    return install_date is not None and install_date == datetime.date.today()


def installed_mwgg_index_tag() -> Optional[str]:
    """Return the Index release tag the installed mwgg_igdb corresponds to, or None.

    Stamped into a generated seed so a client can reconstruct the exact world set
    from that index snapshot (the Index branches are force-pushed, but every release
    is preserved as a `<variant>-<date>` tag). Prefers a `__tag__` baked by the Index
    build; otherwise derives `<variant>-<zero-padded CalVer>` from the package version
    (e.g. variant 'sixteen' + version '2026.6.10' -> 'sixteen-2026.06.10').
    """
    try:
        import mwgg_igdb
    except ImportError:
        return None
    baked = getattr(mwgg_igdb, "__tag__", None)
    if isinstance(baked, str) and baked:
        return baked
    variant = _detect_installed_variant() or DEFAULT_MWGG_IGDB_VARIANT
    try:
        version = importlib.metadata.version("mwgg_igdb")
    except importlib.metadata.PackageNotFoundError:
        return None
    parts = version.split(".")
    if len(parts) >= 3 and all(p.isdigit() for p in parts[:3]):
        year, month, day, *rest = parts
        date = ".".join([year, f"{int(month):02d}", f"{int(day):02d}", *rest])
        return f"{variant}-{date}"
    return f"{variant}-{version}"


def install_mwgg_igdb(upgrade: bool = False, force: bool = False) -> bool:
    """Install or refresh the mwgg_igdb package from the Index repo orphan branch.

    Called before any code path that imports `mwgg_igdb`: the package is the
    runtime source-of-truth for which worlds exist and where to fetch them.

    Args:
        upgrade: Run pip with --upgrade.
        force: With upgrade=True, bypass the once-daily throttle.

    Returns True if the install succeeded (or was throttled).
    """
    # Racing installs from two processes are benign: uv writes temp-then-rename.
    if _skip_all_installs():
        return True
    _resolve_variant()
    if upgrade and not force and _igdb_upgraded_recently():
        logger.debug("mwgg_igdb already installed today; skipping upgrade pull")
        return True
    args = _uv_pip("install", MWGG_IGDB_URL, "--no-cache")
    if upgrade:
        # --reinstall rewrites the package even when the branch HEAD is unchanged,
        # advancing its mtime so the once-daily throttle stays satisfied until tomorrow.
        args.append("--reinstall")
    logger.info(f"Installing mwgg_igdb ({MWGG_IGDB_VARIANT}) from {MWGG_IGDB_BRANCH}")
    try:
        result = _uv_run(args, timeout=300)
    except subprocess.TimeoutExpired:
        logger.warning("uv install of mwgg_igdb timed out.")
        return False
    if result.returncode != 0:
        logger.warning(f"Failed to install mwgg_igdb: {result.stderr}")
        return False
    return True


def _bootstrap_fresh_venv_mwgg_igdb() -> None:
    """The venv creator installs mwgg_igdb synchronously: a sys.path entry probed
    before it exists is None-cached in sys.path_importer_cache and never rechecked."""
    if _venv_just_created:
        install_mwgg_igdb()
        invalidate_caches()


def _get_game_index():
    """Lazy-import GameIndex; install mwgg_igdb if missing. Returns None on failure."""
    try:
        from mwgg_igdb import GameIndex
        return GameIndex
    except ImportError:
        if install_mwgg_igdb():
            invalidate_caches()
            try:
                from mwgg_igdb import GameIndex
                return GameIndex
            except ImportError as e:
                logger.warning(f"mwgg_igdb still unimportable after install: {e}")
        return None


# ── Installer wheel_cache (Inno) ─────────────────────────────────────────────

# Inno's native [Files] download step stages selected worlds' wheels here, next to
# the exe, before first launch (replaces the broken de-elevated runasoriginaluser exec).
def _wheel_cache_dir() -> Path:
    return Path(sys.executable).parent / "wheel_cache"


def _wheel_cache_variant_token(cache_dir: Optional[Path] = None) -> Optional[str]:
    """Read wheel_cache's variant marker; pass a dir explicitly to read a claimed copy."""
    marker = (cache_dir or _wheel_cache_dir()) / "mwgg_igdb_variant.txt"
    try:
        token = marker.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return token if token in _VARIANTS else None


def _apply_wheel_cache_variant() -> None:
    """Apply the installer's chosen variant; must run before
    _bootstrap_fresh_venv_mwgg_igdb() or the first mwgg_igdb install misses it."""
    if not is_frozen() or _skip_all_installs():
        return
    token = _wheel_cache_variant_token()
    if token is not None:
        set_variant(token)


def _install_wheel_cache_wheels(wheel_paths: list[str]) -> None:
    """Install every cached wheel in one `uv pip install`, deps resolved normally."""
    args = _uv_pip("install", *wheel_paths)
    try:
        result = _uv_run(args, timeout=300)
    except subprocess.TimeoutExpired:
        result = None
    if result is None or result.returncode != 0:
        stderr = (result.stderr if result else "timed out").strip()
        for wheel in wheel_paths:
            logger.warning(f"Failed to install cached wheel {wheel}: {stderr}")
        return
    for wheel in wheel_paths:
        logger.info(f"Installed cached wheel {wheel}")
    invalidate_caches()


def _consume_wheel_cache() -> None:
    """Claim wheel_cache/ via atomic rename (loser gets OSError, skips) and install
    it into the worlds venv; best effort, failures degrade to on-demand install."""
    if not is_frozen() or _skip_all_installs():
        return
    cache_dir = _wheel_cache_dir()
    consuming_dir = cache_dir.with_name(cache_dir.name + ".consuming")

    # A stale claim from a crashed prior run must not wedge every future launch.
    if consuming_dir.exists():
        shutil.rmtree(consuming_dir, ignore_errors=True)

    try:
        os.rename(cache_dir, consuming_dir)
    except OSError:
        return  # absent, or another process just claimed it

    try:
        token = _wheel_cache_variant_token(consuming_dir)
        if token is not None:
            set_variant(token)
        wheels = sorted(str(p) for p in consuming_dir.glob("*.whl"))
        if wheels:
            _install_wheel_cache_wheels(wheels)
    except Exception as e:
        # Never crash module import; worlds are installed on demand instead.
        logger.warning(f"wheel_cache processing failed: {e!r}")
    finally:
        shutil.rmtree(consuming_dir, ignore_errors=True)


# Marker peeked before the first mwgg_igdb install; claim/install runs after.
_apply_wheel_cache_variant()
_bootstrap_fresh_venv_mwgg_igdb()
_consume_wheel_cache()


# ── World install primitives ─────────────────────────────────────────────────

def _world_slug(world: str) -> str:
    return world.removeprefix("worlds.")


def _module_location_tag(url: str) -> Optional[str]:
    """Extract the version from a release-asset wheel URL.

    Expects ``https://.../<dist>-<ver>-py3-none-any.whl``, optionally with a
    ``#sha256=<hex>`` fragment. Returns None for anything that isn't a
    recognizable wheel URL; the caller then skips the comparison.
    """
    if not url:
        return None
    name = url.rsplit("/", 1)[-1]
    name = name.split("#", 1)[0].split("?", 1)[0]
    if not name.endswith(".whl"):
        return None
    parts = name[:-len(".whl")].split("-")
    # PEP 427: dist, version, [build,] python, abi, platform; version is index 1.
    if len(parts) < 5:
        return None
    return parts[1]


def _venv_worlds_dir() -> Path:
    """Return the venv worlds dir from which worlds/__init__.py extends __path__.
    Apworlds get extracted here so they're importable via the normal file loader
    (multiprocessing.spawn in child processes needs disk-based modules; zipimport-
    only modules can't be re-imported in the spawned child).
    """
    if use_worlds_venv():
        return Path(mwgg_venv_site_packages("worlds"))
    # Dev: matches the hardcoded path in src/worlds/__init__.py
    from sysconfig import get_path
    return Path(get_path("purelib")) / "worlds"


# Consumed by the upgrader tools (tools/mwgg_upgrade.py, tools/mcp_mwgg_upgrader.py),
# so it is unused within this module, hence the targeted ignore.
def _venv_has_worlds() -> bool:  # pyright: ignore[reportUnusedFunction]
    try:
        worlds_dir = _venv_worlds_dir()
        return worlds_dir.exists() and any(worlds_dir.iterdir())
    except OSError:
        return False


def _install_apworld_to_venv(apworld_file: Path, slug: str) -> bool:
    """Extract the `<slug>/` directory from apworld_file into the venv worlds dir.
    Returns True on success. Overwrites existing files in place rather than
    rmtree'ing (rmtree fails on Windows if the module is currently loaded).
    """
    venv_worlds = _venv_worlds_dir()
    try:
        venv_worlds.mkdir(parents=True, exist_ok=True)
        prefix = f"{slug}/"
        with zipfile.ZipFile(apworld_file, "r") as zf:
            members = [m for m in zf.namelist() if m == prefix or m.startswith(prefix)]
            if not members:
                logger.warning(f"Apworld {apworld_file} contains no '{slug}/' directory")
                return False
            for member in members:
                zf.extract(member, str(venv_worlds))
        # Refresh the dir's mtime so the stale-extraction pruner sees this
        # extraction as "last used" even if zipfile restored archive timestamps.
        target_dir = venv_worlds / slug
        try:
            os.utime(target_dir, None)
        except OSError:
            pass
        logger.info(f"Extracted apworld {apworld_file} to {target_dir}")
        # Extend an already-imported worlds package's __path__ so the new module is
        # discoverable without a restart (worlds/__init__.py handles the startup case).
        worlds_pkg = sys.modules.get("worlds")
        if worlds_pkg is not None and hasattr(worlds_pkg, "__path__"):
            venv_str = str(venv_worlds)
            if venv_str not in worlds_pkg.__path__:
                worlds_pkg.__path__.append(venv_str)
        return True
    except Exception as e:
        logger.error(f"Failed to extract apworld {apworld_file} to {venv_worlds}: {e}")
        return False


def _prune_stale_apworld_extractions(max_age_days: int = 30) -> None:
    """Remove extracted-apworld dirs in the venv worlds dir whose mtime is older
    than max_age_days. Skips any dir backed by a real importlib.metadata
    Distribution (pip-installed wheels), so this only ever touches our own
    extraction output.
    """
    venv_worlds = _venv_worlds_dir()
    if not venv_worlds.exists():
        return
    cutoff = time.time() - max_age_days * 86400
    for entry in venv_worlds.iterdir():
        if not entry.is_dir() or entry.name.startswith("_"):
            continue
        try:
            importlib.metadata.distribution(f"worlds.{entry.name}")
            continue  # pip-installed; leave alone
        except importlib.metadata.PackageNotFoundError:
            pass
        try:
            if entry.stat().st_mtime >= cutoff:
                continue
        except OSError:
            continue
        try:
            shutil.rmtree(entry)
            logger.info(f"Pruned stale extracted apworld {entry} (mtime > {max_age_days}d)")
        except OSError as e:
            logger.warning(f"Could not prune stale apworld {entry}: {e}")


def uninstall_worlds(worlds: List[str]) -> None:
    """Uninstall a list of `worlds.<slug>` packages from the venv."""
    for world in worlds:
        try:
            _uv_run(_uv_pip("uninstall", world), timeout=60)
        except subprocess.TimeoutExpired:
            logger.warning(f"uv uninstall of {world} timed out.")


def find_world_modules() -> set[str]:
    """Return all known world slugs: union of mwgg_igdb entries and currently installed `worlds.<slug>` dists."""
    world_modules_set: set[str] = set()

    index = _get_game_index()
    if index is not None:
        world_modules_set.update(index.get_all_games().keys())

    try:
        executable_args = _uv_pip("list", "--format", "json")
        logger.debug(f"Executing subprocess command to find installed worlds: {executable_args}")
        response = _uv_run(executable_args, timeout=45)
        if response.returncode == 0:
            for package in json.loads(response.stdout):
                package_name = package.get("name", "")
                if package_name.startswith("worlds") and len(package_name) > 7:
                    # uv hyphenates dist names (worlds.dark_souls_3 -> worlds-dark-souls-3); restore the slug.
                    world_name = package_name[7:].replace("-", "_")
                    if not world_name.startswith("_"):
                        world_modules_set.add(world_name)
        else:
            logger.warning(f"Could not list installed packages: {response.stderr}")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        logger.warning(f"Could not check installed world modules: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error while checking installed world modules: {e}")

    return world_modules_set


def _format_manual_install_hint(module_location: str) -> str:
    """Render a copy-pasteable `uv pip install` command for the host shell."""
    return (
        "To install manually on the host (where build tools are available), run:\n"
        f"    bash:      source {mwgg_venv_site_packages()}/bin/activate\n"
        f"    win PS:    & {mwgg_venv_site_packages()}/Scripts/Activate.ps1\n"
        f"    docker:    source ~/<your-local-venv>/bin/activate\n"
        f"    then run:\n"
        f"               uv pip install '{module_location}' --upgrade --no-cache\n"
        f"    docker admins will need to copy the site packages to /var/lib/mwgg/mwgg_venv"
    )


# ── Dependency healing ───────────────────────────────────────────────────────

def _canonical_name(name: str) -> str:
    """PEP 503 name normalization."""
    return re.sub(r"[-_.]+", "-", name).lower()


def _installed_dist_names() -> set[str]:
    """Canonical names of every dist visible to this process (one venv pass)."""
    names: set[str] = set()
    for dist in importlib.metadata.distributions():
        try:
            name = dist.metadata["Name"]
        except Exception:
            continue
        if name:  # email.Message returns None for a missing key despite the str stub
            names.add(_canonical_name(name))
    return names


def _missing_requirements(requires: Optional[list[str]],
                          installed_names: Optional[set[str]] = None) -> list[str]:
    """Names a dist's declared requirements need that are absent from the venv.

    Presence-only: version specifiers are ignored (uv reconciles versions on
    reinstall). Extras-gated and false-marker requirements don't apply;
    unparseable requirement strings are skipped (unhealable, never loop on them).
    """
    if not requires:
        return []
    try:
        from packaging.requirements import InvalidRequirement, Requirement
    except ImportError:
        # Stale env without `packaging` yet; healing resumes once requirements install.
        return []
    if installed_names is None:
        installed_names = _installed_dist_names()
    missing: list[str] = []
    for raw in requires:
        try:
            req = Requirement(raw)
        except InvalidRequirement:
            continue
        if req.marker is not None and not req.marker.evaluate({"extra": ""}):
            continue
        if _canonical_name(req.name) not in installed_names:
            missing.append(req.name)
    return missing


def _world_dist(slug: str) -> Optional[importlib.metadata.Distribution]:
    try:
        return importlib.metadata.distribution(f"worlds.{slug}")
    except importlib.metadata.PackageNotFoundError:
        return None


def _state_dir() -> Path:
    """Shared writable dir for cross-process state (install lock, heal markers)."""
    state_dir = install_path().parent if use_worlds_venv() else Path(tempfile.gettempdir())
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


def _heal_state_path() -> Path:
    return _state_dir() / ".mwgg-heal-attempts.json"


def _load_heal_attempts() -> dict[str, str]:
    """slug -> module_location of that world's last failed install.

    Suppresses re-healing a wheel that already failed; a new release URL in the
    index mismatches the stored value and re-arms exactly one retry. The store
    is an optimization, never authority: any read failure degrades to {}.
    """
    try:
        data = json.loads(_heal_state_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    attempts: dict[Any, Any] = data
    return {key: value for key, value in attempts.items()
            if isinstance(key, str) and isinstance(value, str)}


def _save_heal_attempts(attempts: dict[str, str]) -> None:
    try:
        _heal_state_path().write_text(json.dumps(attempts), encoding="utf-8")
    except OSError:
        pass  # worst case: one extra heal attempt next cold start


def _record_heal_attempt(slug: str, module_location: str) -> None:
    attempts = _load_heal_attempts()
    if attempts.get(slug) != module_location:
        attempts[slug] = module_location
        _save_heal_attempts(attempts)


def _clear_heal_attempt(slug: str) -> None:
    attempts = _load_heal_attempts()
    if slug in attempts:
        del attempts[slug]
        _save_heal_attempts(attempts)


# ── Install decisions ────────────────────────────────────────────────────────

def _world_requires_install(slug: str, games: dict[str, dict[str, object]],
                            installed_names: Optional[set[str]] = None,
                            heal_attempts: Optional[dict[str, str]] = None) -> bool:
    """True when the world's wheel should be (re)installed: dist missing,
    version behind the index tag, or installed with missing dependencies.

    The dependency branch is the healing path: the caller reinstalls WITH deps
    from the current module_location. A wheel that already failed (recorded
    heal attempt for this exact URL) is left alone until the index serves a
    new URL, bounding retries to one per (slug, wheel URL).
    """
    dist = _world_dist(slug)
    if dist is None:
        return True

    module_location = games.get(slug, {}).get("module_location")
    if not isinstance(module_location, str):
        return False

    tag = _module_location_tag(module_location)
    if tag and dist.version != tag:
        return True

    missing = _missing_requirements(dist.requires, installed_names)
    if not missing:
        return False
    if heal_attempts is None:
        heal_attempts = _load_heal_attempts()
    if heal_attempts.get(slug) == module_location:
        return False
    logger.info(f"World {slug} is missing dependencies {missing}; reinstalling with them")
    return True


def _worlds_requiring_install(worlds: list[str], games: dict[str, dict[str, object]],
                              installed_names: Optional[set[str]] = None,
                              heal_attempts: Optional[dict[str, str]] = None) -> list[str]:
    return [world for world in worlds
            if _world_requires_install(_world_slug(world), games, installed_names, heal_attempts)]


def check_for_updates(worlds_only: bool = False) -> List[str]:
    """Return packages with newer versions (or, for worlds, missing deps) available.

    For worlds: re-pull mwgg_igdb (throttled), then return installed worlds
    that _world_requires_install flags — version behind the index tag or
    dependencies missing. Never-installed and apworld-extracted worlds (no
    dist) are not returned; they install on demand at launch.
    For non-world packages (dev only): query PyPI against requirements.txt entries.
    """
    if worlds_only:
        install_mwgg_igdb(upgrade=True)
        index = _get_game_index()
        if index is None:
            return []
        games: dict[str, dict[str, Any]] = index.get_all_games()
        installed_names = _installed_dist_names()
        heal_attempts = _load_heal_attempts()
        outdated = [
            f"worlds.{slug}" for slug in games
            if _world_dist(slug) is not None
            and _world_requires_install(slug, games, installed_names, heal_attempts)
        ]
        logger.info(f"Worlds with available updates: {outdated}")
        return outdated

    # Dev-only path: ask uv for outdated dists. uv's resolver enforces requirements.txt
    # specifiers at install time, so we don't need to pre-filter here.
    try:
        executable_args = _uv_pip("list", "--outdated", "--format", "json")
        logger.info(f"Executing subprocess command: {executable_args}")
        response = _uv_run(executable_args, timeout=45)
        if response.returncode != 0:
            logger.warning(f"Could not check for updates: {response.stderr}")
            return []

        outdated_packages = json.loads(response.stdout)
        logger.info(f"Newer versions of the following packages are available: {outdated_packages}")
        return [pkg["name"] for pkg in outdated_packages]

    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        logger.warning(f"Could not check for updates: {e}")
        return []


# ── install_worlds & the cold-start world update ─────────────────────────────

class WorldInstallResult(List[str]):
    """The apworld-fallback list install_worlds returns, plus `.failed`:
    targets that neither installed nor fell back, so the venv is missing them.
    """
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.failed: list[str] = []


def install_worlds(worlds: List[str], update: bool = False, with_deps: bool = False) -> WorldInstallResult:
    """
    Install worlds by resolving each apworld's `module_location` from mwgg_igdb and pip-installing the URL.

    `module_location` is a `https://.../<dist>-<world_version>-py3-none-any.whl#sha256=<hex>`
    release-asset URL set by the Index repo.

    Falls back to a custom_worlds/<slug>.apworld lookup if the apworld isn't in the index or its
    `module_location` install fails.

    Args:
        worlds: List of apworlds to install.
        update: If True, uninstall old versions first.
        with_deps: If True, install the wheel *with* its transitive dependencies.
            Otherwise, dependencies are still installed for new worlds and for
            worlds flagged by the dependency-healing check, and skipped for
            worlds already healthy at the current tag.

    Returns:
        The apworlds that fell back to a custom apworld, carrying `.failed` -- the
        targets that could not be installed at all. Callers that gate a deploy on a
        complete venv must check `.failed`; a non-empty list means worlds are missing.
    """
    if _skip_all_installs():
        return WorldInstallResult()
    apworlds = WorldInstallResult()

    def fall_back_to_apworld(slug: str, target: str) -> None:
        """Last resort after an install failure: extract custom_worlds/<slug>.apworld
        into the venv. Records the target as failed when that is not possible."""
        apworld_file = custom_worlds_dir / f"{slug}.apworld"
        if apworld_file.exists():
            logger.info(f"Found apworld file: {apworld_file}")
            if _install_apworld_to_venv(apworld_file, slug):
                apworlds.append(target)
                return
            logger.warning(f"Could not extract apworld fallback {apworld_file}")
        else:
            logger.warning(f"Custom apworld file not found at {apworld_file}")
        logger.warning(f"{target} could not be installed and has no apworld fallback")
        apworlds.failed.append(target)

    world_slugs: list[str] = []
    selected_variant: Optional[str] = None
    for entry in worlds:
        variant = _parse_variant_token(entry)
        if variant is not None:
            selected_variant = variant
        else:
            world_slugs.append(entry)
    if selected_variant is not None:
        set_variant(selected_variant)
        install_mwgg_igdb(upgrade=True, force=True)

    index = _get_game_index()
    games: dict[str, dict[str, Any]] = index.get_all_games() if index is not None else {}

    # with_deps installs never consult the healthy-world snapshot, so skip the scan.
    installed_names: Optional[set[str]] = None
    heal_attempts: dict[str, str] = {}
    installed_world_slugs: set[str] = set()
    if not with_deps:
        installed_names = _installed_dist_names()
        heal_attempts = _load_heal_attempts()
        # Snapshot BEFORE uninstall_worlds: a world properly installed at the current
        # mwgg_igdb tag with its deps present stays in the set so update=True
        # reinstalls can skip deps.
        installed_world_slugs = {
            _world_slug(world) for world in world_slugs
            if not _world_requires_install(_world_slug(world), games, installed_names, heal_attempts)
        }

    if update:
        logger.info(f"Uninstalling old versions of: {world_slugs}")
        uninstall_worlds(world_slugs)

    if not update and not with_deps and world_slugs:
        worlds_to_install = _worlds_requiring_install(world_slugs, games, installed_names, heal_attempts)
        skipped_worlds = sorted(set(world_slugs) - set(worlds_to_install))
        if skipped_worlds:
            logger.debug(f"Skipping already-installed worlds: {skipped_worlds}")
        if not worlds_to_install:
            _prune_stale_apworld_extractions()
            invalidate_caches()
            return apworlds
        world_slugs = worlds_to_install

    for world in world_slugs:
        slug = world.removeprefix("worlds.")
        target = f"worlds.{slug}"

        if update:
            logger.info(f"Updating world: {target}")
        else:
            logger.info(f"Installing world: {target}")

        entry = games.get(slug, {})
        module_location = entry.get("module_location")

        if not module_location:
            logger.warning(f"No module_location for {slug} in mwgg_igdb; checking custom_worlds")
            fall_back_to_apworld(slug, target)
            continue

        install_args = ["install"]
        if not with_deps and slug in installed_world_slugs:
            install_args.append("--no-deps")
        install_args += [module_location, "--upgrade", "--no-cache"]
        executable_args = _uv_pip(*install_args)
        logger.info(f"Executing subprocess command: {executable_args}")
        try:
            result = _uv_run(executable_args, timeout=300)
        except subprocess.TimeoutExpired:
            logger.warning(f"uv install of {target} timed out; treating as failure.")
            logger.warning(_format_manual_install_hint(module_location))
            _record_heal_attempt(slug, module_location)
            fall_back_to_apworld(slug, target)
            continue
        logger.info(result.stdout)

        if result.returncode != 0:
            stderr_text = (result.stderr or "").strip() or "uv returned non-zero with no stderr"
            logger.warning(f"World {target} failed to install from {module_location}:\n{stderr_text}")
            logger.warning(_format_manual_install_hint(module_location))
            _record_heal_attempt(slug, module_location)
            fall_back_to_apworld(slug, target)
        else:
            logger.info(f"Successfully installed {target}")
            _clear_heal_attempt(slug)

    _prune_stale_apworld_extractions()
    invalidate_caches()
    return apworlds


def update_worlds() -> Optional[WorldInstallResult]:
    """Pull the latest mwgg_igdb, then reinstall every installed world whose
    version no longer matches its index tag or whose dependencies are missing.

    Platform- and freeze-neutral; the launcher runs this on every cold start,
    with the Windows splash fronting the same call. Returns None when nothing
    was outdated, else install_worlds' result for the outdated set.
    """
    if _skip_all_installs():
        return None
    updates = check_for_updates(worlds_only=True)
    if not updates:
        return None
    return install_worlds(updates)


# ── Room-pinned installs from a tagged index snapshot ────────────────────────
# A room records the mwgg_igdb release tag it was generated against
# (NetUtils.MultiData["mwgg_index_tag"], stamped by installed_mwgg_index_tag()). To install a world
# at the version current at that tag WITHOUT disturbing the installed/active mwgg_igdb,
# we read that one world's module_location straight out of the tagged index snapshot and
# pip-install just that wheel. The snapshot is the tag's source tarball: the variant
# branches are force-pushed (history rewritten) so `git+...@<tag>` is unreliable, but
# GitHub serves `archive/refs/tags/<tag>.tar.gz` for any tag.

# Cache of tag -> games-data dict, so a room with several worlds downloads the snapshot once.
_TAGGED_INDEX_GAMES_CACHE: dict[str, dict[str, Any]] = {}


def _load_tagged_index_games(tag: str) -> Optional[dict[str, Any]]:
    """Return the games dict from the mwgg_igdb snapshot at `tag`, or None.

    Downloads the tag's source tarball and loads its mwgg_igdb module in ISOLATION -- it
    is never installed and the active mwgg_igdb is never touched. Cached per tag. Returns
    None on any download/parse failure so callers degrade gracefully.
    """
    if tag in _TAGGED_INDEX_GAMES_CACHE:
        return _TAGGED_INDEX_GAMES_CACHE[tag]
    url = _index_archive_url(f"tags/{tag}")
    try:
        with tempfile.TemporaryDirectory() as tmp:
            archive = os.path.join(tmp, "index.tar.gz")
            urllib.request.urlretrieve(url, archive)
            with tarfile.open(archive, "r:gz") as tf:
                tf.extractall(tmp, filter="data")
            module_path = None
            for root, _dirs, files in os.walk(tmp):
                if "mwgg_igdb.py" in files:
                    module_path = os.path.join(root, "mwgg_igdb.py")
                    break
            if module_path is None:
                logger.warning(f"Tagged index {tag} has no mwgg_igdb.py")
                return None
            spec = importlib.util.spec_from_file_location(f"_mwgg_igdb_pinned_{tag}", module_path)
            if spec is None or spec.loader is None:
                return None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            games: Any = None
            game_index: Any = getattr(module, "GameIndex", None)
            if game_index is not None and hasattr(game_index, "get_all_games"):
                games = game_index.get_all_games()
            if not isinstance(games, dict):
                games = getattr(module, "GAMES_DATA", None)
            if not isinstance(games, dict):
                return None
            # isinstance narrows Any to dict[Unknown, Unknown]; re-widen for strict pyright.
            typed_games = cast("dict[str, Any]", games)
            _TAGGED_INDEX_GAMES_CACHE[tag] = typed_games
            return typed_games
    except Exception as e:
        logger.warning(f"Could not load tagged index {tag}: {e!r}")
        return None


def module_location_from_tag(slug: str, tag: str) -> Optional[str]:
    """The module_location (wheel URL) for `slug` as recorded in the index at `tag`."""
    games = _load_tagged_index_games(tag)
    if not games:
        return None
    entry: Any = games.get(slug)
    if not isinstance(entry, dict):
        return None
    location: Any = cast("dict[str, Any]", entry).get("module_location")
    return location if isinstance(location, str) and location else None


def install_worlds_from_tag(slugs: list[str], tag: str, with_deps: bool = False) -> list[str]:
    """Install the given managed worlds at the versions recorded in the index `tag`.

    Reads each world's module_location from the tagged snapshot (the active mwgg_igdb is
    left untouched) and reinstalls only those whose installed version differs from the
    tagged one, with `--reinstall --no-cache` (NOT `--upgrade`, so a downgrade takes).
    Returns the slugs that could not be resolved or installed.
    """
    if _skip_all_installs():
        return []
    failed: list[str] = []
    for raw_slug in slugs:
        slug = _world_slug(raw_slug)
        url = module_location_from_tag(slug, tag)
        if not url:
            logger.warning(f"No module_location for worlds.{slug} in tagged index {tag}")
            failed.append(slug)
            continue
        want = _module_location_tag(url)  # version embedded in the wheel filename
        try:
            installed = importlib.metadata.distribution(f"worlds.{slug}").version
        except importlib.metadata.PackageNotFoundError:
            installed = None
        if want and installed == want:
            continue  # already at the tagged version
        install_args = ["install", url, "--reinstall", "--no-cache"]
        # A swap (already installed at a different version) must restore the pinned
        # version's deps; only a from-scratch install honors a deps opt-out.
        if not with_deps and installed is None:
            install_args.append("--no-deps")
        try:
            result = _uv_run(_uv_pip(*install_args), timeout=300)
        except subprocess.TimeoutExpired:
            logger.warning(f"Tagged install of worlds.{slug} timed out.")
            failed.append(slug)
            continue
        if result.returncode != 0:
            stderr_text = (result.stderr or "").strip() or "uv returned non-zero with no stderr"
            logger.warning(f"Tagged install of worlds.{slug} failed:\n{stderr_text}")
            failed.append(slug)
            continue
        logger.info(f"Installed worlds.{slug} from index tag {tag} ({want})")
    _prune_stale_apworld_extractions()
    invalidate_caches()
    return failed


# ── Dev requirements pipeline ────────────────────────────────────────────────

def confirm(msg: str) -> None:
    """Get user confirmation for an action."""
    try:
        input(f"\n{msg}")
    except KeyboardInterrupt:
        logger.info("\nAborting")
        sys.exit(1)


def update_requirements(needed_packages: List[str]) -> None:
    """Install/upgrade from all registered requirements files, then worlds.

    Empty `needed_packages` upgrades everything; otherwise uv upgrades only the
    named dists (--upgrade-package names absent from a file's resolution are
    ignored by uv). Core requirements.txt constrains every install.
    """
    for req_file in requirements_files:
        if not req_file.exists():
            logger.warning(f"Requirements file not found: {req_file}")
            continue
        logger.debug(f"Processing requirements from: {req_file}")
        executable_args = _uv_pip("install", "-r", str(req_file),
                                  "--constraint", str(core_constraints))
        if needed_packages:
            for pkg in needed_packages:
                executable_args.extend(["--upgrade-package", pkg])
        else:
            executable_args.append("--upgrade")
        result = _uv_run(executable_args, timeout=30)
        if result.returncode != 0:
            logger.warning(f"Failed to install/update from {req_file.name}")

    # Worlds are not in requirements.txt files; route them to install_worlds.
    worlds_to_install = [pkg for pkg in needed_packages if pkg.startswith("worlds") or pkg.startswith("mwgg")]
    if worlds_to_install:
        logger.info(f"Installing/updating worlds: {worlds_to_install}")
        install_worlds(worlds_to_install)


def check_requirements_satisfied() -> bool:
    """Ensure all requirements files are satisfied. Returns True on success."""
    for req_file in requirements_files:
        if not req_file.exists():
            logger.warning(f"Requirements file not found: {req_file}")
            continue
        logger.info(f"Ensuring requirements from {req_file.name} are satisfied")
        # Idempotent: uv audits and exits fast when everything is present.
        result = _uv_run(
            _uv_pip("install", "-r", str(req_file), "--constraint", str(core_constraints)),
            timeout=30,
        )
        if result.returncode != 0:
            logger.warning(f"Failed to install requirements from {req_file.name}: {result.stderr}")
            return False
    return True


# ── Top-level update pipeline ────────────────────────────────────────────────

@contextlib.contextmanager
def _install_lock():
    """Serialize the top-level update pipeline across processes."""
    lock_path = _state_dir() / ".mwgg-install.lock"
    with open(lock_path, "a+b") as lock_file:
        lock_file.seek(0, os.SEEK_END)
        if lock_file.tell() == 0:
            lock_file.write(b"\0")
            lock_file.flush()

        if is_windows():
            import msvcrt
            lock_file.seek(0)
            while True:
                try:
                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError as e:
                    if (
                        e.errno not in (errno.EACCES, errno.EDEADLK)
                        and getattr(e, "winerror", None) not in (32, 33)
                    ):
                        raise
                    time.sleep(0.25)
            try:
                yield
            finally:
                lock_file.seek(0)
                msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            # The gate type-checks with pythonPlatform=Windows, where typeshed hides
            # flock/LOCK_*; platform false positives, not real attribute errors.
            import fcntl
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
            try:
                yield
            finally:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]


def update(yes: bool = True, force: bool = False, worlds: Optional[List[str]] = None) -> None:
    """Run the update pipeline (worlds, then dev requirements) under the install lock."""
    if _skip_all_installs():
        return
    with _install_lock():
        _update_locked(yes=yes, force=force, worlds=worlds)


def _update_locked(yes: bool, force: bool, worlds: Optional[List[str]]) -> None:
    if _skip_all_installs():
        return
    if worlds:
        install_mwgg_igdb(upgrade=True)
        install_worlds(worlds, update=force)
        return
    if _skip_update and not force:
        # Children spawned under a live launcher must not re-run the updater;
        # the launcher owns the world update via update_worlds() on cold start.
        return
    restart_needed = update_worlds()
    if restart_needed:
        # Apworld fallbacks were staged into the venv; a restart loads them.
        from Utils import exit_restart_for_update
        exit_restart_for_update()

    global update_ran
    if update_ran:
        return
    update_ran = True

    if is_frozen():
        # Base requirements are baked into the frozen bundle at build time.
        return

    if force:
        logger.debug("Force update requested - upgrading everything")
        update_requirements([])
        return

    logger.debug("Checking for available updates...")
    available_updates = check_for_updates()
    if available_updates:
        logger.debug(f"Found updates for: {available_updates}")
        if not yes:
            confirm("Updates available. Press enter to continue with updates.")
    else:
        logger.debug("No updates found.")

    if not check_requirements_satisfied():
        logger.debug("Installing missing requirements...")
        update_requirements([])

    if available_updates:
        update_requirements(available_updates)

    logger.debug("Update process completed.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Install MultiworldGG requirements')
    parser.add_argument('-y', '--yes', dest='yes', action='store_true',
                        help='answer "yes" to all questions')
    parser.add_argument('-f', '--force', dest='force', action='store_true',
                        help='force update')
    parser.add_argument('-a', '--append', nargs="*", dest='additional_requirements',
                        help='List paths to additional requirement files.')
    parser.add_argument('-w', '--worlds', nargs="*", dest='worlds',
                        help='List of worlds to update.')

    args = parser.parse_args()

    # Standalone always pulls fresh; today's install mtime then throttles the
    # upgrade=True calls inside the subsequent update().
    install_mwgg_igdb(upgrade=True, force=True)

    if args.additional_requirements:
        requirements_files.update([Path(req) for req in args.additional_requirements])

    if args.worlds:
        update(args.yes, args.force, args.worlds)
    else:
        update(args.yes, args.force)
