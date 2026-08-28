"""Pure / filesystem-only ModuleUpdate.py helpers -- no real network or pip/uv runs.

ModuleUpdate keeps module-level globals (update_ran, the resolved variant trio,
the uv-resolution cache); every test that flips one restores it so collection
order can't leak state. test/__init__.py forces update_ran=True.
"""
import datetime
import os
import subprocess
import types

import pytest

import ModuleUpdate


# --------------------------------------------------------------------------- #
# _parse_url_requirement
# --------------------------------------------------------------------------- #
def test_parse_url_requirement_tarball_to_pinned_spec():
    out = ModuleUpdate._parse_url_requirement(
        "https://github.com/owner/repo/archive/foo-1.2.3.tar.gz"
    )
    assert out == "foo==1.2.3"


def test_parse_url_requirement_zip_to_pinned_spec():
    out = ModuleUpdate._parse_url_requirement("https://example.com/dl/bar-0.9.zip")
    assert out == "bar==0.9"


def test_parse_url_requirement_at_in_filename_raises():
    # An '@' in the trailing filename means the version can't be deduced.
    with pytest.raises(ValueError):
        ModuleUpdate._parse_url_requirement("https://example.com/foo@1.0.zip")


def test_parse_url_requirement_unsplittable_returns_empty():
    # Only one '-' segment after suffix substitution -> ValueError -> "".
    assert ModuleUpdate._parse_url_requirement("https://example.com/noseparator.zip") == ""


# --------------------------------------------------------------------------- #
# _parse_custom_pep508_requirement
# --------------------------------------------------------------------------- #
def test_parse_custom_pep508_basic():
    out = ModuleUpdate._parse_custom_pep508_requirement(
        "mypackage @ git+https://example.com/x.git#1.2.3"
    )
    assert out == "mypackage==1.2.3"


def test_parse_custom_pep508_preserves_environment_marker():
    out = ModuleUpdate._parse_custom_pep508_requirement(
        "mypackage @ git+https://example.com/x.git#1.2.3 ; python_version >= '3.8'"
    )
    assert out == "mypackage==1.2.3; python_version >= '3.8'"


# --------------------------------------------------------------------------- #
# _module_location_tag
# --------------------------------------------------------------------------- #
def test_module_location_tag_extracts_wheel_version():
    url = (
        "https://github.com/o/r/releases/download/v1.4.2/"
        "mypkg-1.4.2-py3-none-any.whl#sha256=deadbeef"
    )
    assert ModuleUpdate._module_location_tag(url) == "1.4.2"


def test_module_location_tag_non_wheel_and_short_return_none():
    # Legacy git+...@ref URL (not a wheel) and a too-short wheel name both -> None.
    assert ModuleUpdate._module_location_tag("git+https://github.com/o/r@abc123") is None
    assert ModuleUpdate._module_location_tag("https://x/y/short-1.0.whl") is None
    assert ModuleUpdate._module_location_tag("") is None


# --------------------------------------------------------------------------- #
# _parse_variant_token
# --------------------------------------------------------------------------- #
def test_parse_variant_token_known_and_unknown():
    assert ModuleUpdate._parse_variant_token("mwgg_igdb") == "sixteen"
    assert ModuleUpdate._parse_variant_token("mwgg_igdb_twelve") == "twelve"
    assert ModuleUpdate._parse_variant_token("mwgg_igdb_nr") == "nr"
    assert ModuleUpdate._parse_variant_token("mwgg_igdb_bogus") is None
    assert ModuleUpdate._parse_variant_token("worlds.alttp") is None


# --------------------------------------------------------------------------- #
# _igdb_install_date / _igdb_upgraded_recently  (mtime-driven)
# --------------------------------------------------------------------------- #
def _fake_spec_for(path):
    return types.SimpleNamespace(origin=str(path))


def test_igdb_install_date_reads_file_mtime(tmp_path, monkeypatch):
    pkg = tmp_path / "mwgg_igdb.py"
    pkg.write_text("__variant__ = 'sixteen'\n")
    known = datetime.datetime(2021, 6, 15, 12, 0, 0).timestamp()
    os.utime(pkg, (known, known))
    monkeypatch.setattr(ModuleUpdate.importlib.util, "find_spec", lambda name: _fake_spec_for(pkg))

    assert ModuleUpdate._igdb_install_date() == datetime.date(2021, 6, 15)


def test_igdb_install_date_none_when_not_installed(monkeypatch):
    monkeypatch.setattr(ModuleUpdate.importlib.util, "find_spec", lambda name: None)
    assert ModuleUpdate._igdb_install_date() is None


def test_igdb_upgraded_recently_true_only_for_today(tmp_path, monkeypatch):
    pkg = tmp_path / "mwgg_igdb.py"
    pkg.write_text("x\n")
    monkeypatch.setattr(ModuleUpdate.importlib.util, "find_spec", lambda name: _fake_spec_for(pkg))

    now = datetime.datetime.now().timestamp()
    os.utime(pkg, (now, now))
    assert ModuleUpdate._igdb_upgraded_recently() is True

    old = datetime.datetime(2000, 1, 1).timestamp()
    os.utime(pkg, (old, old))
    assert ModuleUpdate._igdb_upgraded_recently() is False


# --------------------------------------------------------------------------- #
# _detect_installed_variant / _resolve_variant
# --------------------------------------------------------------------------- #
@pytest.fixture
def restore_variant_globals():
    """Snapshot/restore the resolved-variant trio + explicit-override sentinel."""
    saved = (
        ModuleUpdate._EXPLICIT_VARIANT,
        ModuleUpdate.MWGG_IGDB_VARIANT,
        ModuleUpdate.MWGG_IGDB_BRANCH,
        ModuleUpdate.MWGG_IGDB_GIT_URL,
    )
    yield
    (
        ModuleUpdate._EXPLICIT_VARIANT,
        ModuleUpdate.MWGG_IGDB_VARIANT,
        ModuleUpdate.MWGG_IGDB_BRANCH,
        ModuleUpdate.MWGG_IGDB_GIT_URL,
    ) = saved


def test_detect_installed_variant_reads_module_attr(monkeypatch):
    monkeypatch.setattr(ModuleUpdate.importlib.util, "find_spec", lambda name: object())
    fake_mod = types.ModuleType("mwgg_igdb")
    fake_mod.__variant__ = "twelve"
    monkeypatch.setitem(__import__("sys").modules, "mwgg_igdb", fake_mod)
    assert ModuleUpdate._detect_installed_variant() == "twelve"


def test_detect_installed_variant_rejects_unknown_value(monkeypatch):
    monkeypatch.setattr(ModuleUpdate.importlib.util, "find_spec", lambda name: object())
    fake_mod = types.ModuleType("mwgg_igdb")
    fake_mod.__variant__ = "not_a_real_variant"
    monkeypatch.setitem(__import__("sys").modules, "mwgg_igdb", fake_mod)
    assert ModuleUpdate._detect_installed_variant() is None


def test_detect_installed_variant_none_when_no_spec(monkeypatch):
    monkeypatch.setattr(ModuleUpdate.importlib.util, "find_spec", lambda name: None)
    assert ModuleUpdate._detect_installed_variant() is None


def test_resolve_variant_explicit_override_wins(monkeypatch, restore_variant_globals):
    # Even when detection would yield 'twelve', an explicit set_variant wins
    # and the derived globals are kept consistent.
    monkeypatch.setattr(ModuleUpdate, "_detect_installed_variant", lambda: "twelve")
    monkeypatch.setattr(ModuleUpdate, "_EXPLICIT_VARIANT", "ao")

    assert ModuleUpdate._resolve_variant() == "ao"
    assert ModuleUpdate.MWGG_IGDB_VARIANT == "ao"
    assert ModuleUpdate.MWGG_IGDB_BRANCH == "game_index_ao"
    assert ModuleUpdate.MWGG_IGDB_GIT_URL == (
        "git+https://github.com/MultiworldGG/MultiworldGG-Index@game_index_ao"
    )


def test_resolve_variant_falls_back_to_default_when_undetectable(monkeypatch, restore_variant_globals):
    monkeypatch.setattr(ModuleUpdate, "_EXPLICIT_VARIANT", None)
    monkeypatch.setattr(ModuleUpdate, "_detect_installed_variant", lambda: None)

    assert ModuleUpdate._resolve_variant() == ModuleUpdate.DEFAULT_MWGG_IGDB_VARIANT
    assert ModuleUpdate.MWGG_IGDB_BRANCH == f"game_index_{ModuleUpdate.DEFAULT_MWGG_IGDB_VARIANT}"


# --------------------------------------------------------------------------- #
# custom_worlds scan -> worlds_files["wheels"] / ["apworlds"]
# --------------------------------------------------------------------------- #
def test_custom_worlds_scan_populates_worlds_files(tmp_path, monkeypatch):
    """_scan_custom_worlds() collects every .whl and .apworld in custom_worlds_dir
    into the two RequirementsSets, guarded by `not update_ran`."""
    wheel = tmp_path / "worlds.example-1.0-py3-none-any.whl"
    apworld = tmp_path / "example.apworld"
    decoy = tmp_path / "README.txt"
    for f in (wheel, apworld, decoy):
        f.write_text("x")

    saved_update_ran = ModuleUpdate.update_ran
    saved_wheels = set(ModuleUpdate.worlds_files["wheels"])
    saved_apworlds = set(ModuleUpdate.worlds_files["apworlds"])
    monkeypatch.setattr(ModuleUpdate, "custom_worlds_dir", tmp_path)
    try:
        ModuleUpdate.worlds_files["wheels"].clear()
        ModuleUpdate.worlds_files["apworlds"].clear()
        ModuleUpdate.update_ran = False

        ModuleUpdate._scan_custom_worlds()

        assert ModuleUpdate.worlds_files["wheels"] == {str(wheel)}
        assert ModuleUpdate.worlds_files["apworlds"] == {str(apworld)}
        # The stray non-world file is collected into neither set.
        assert str(decoy) not in ModuleUpdate.worlds_files["wheels"]
        assert str(decoy) not in ModuleUpdate.worlds_files["apworlds"]

        # The update_ran guard short-circuits the scan (no re-collection after update).
        ModuleUpdate.worlds_files["wheels"].clear()
        ModuleUpdate.update_ran = True
        ModuleUpdate._scan_custom_worlds()
        assert ModuleUpdate.worlds_files["wheels"] == set()
    finally:
        ModuleUpdate.worlds_files["wheels"].clear()
        ModuleUpdate.worlds_files["wheels"].update(saved_wheels)
        ModuleUpdate.worlds_files["apworlds"].clear()
        ModuleUpdate.worlds_files["apworlds"].update(saved_apworlds)
        ModuleUpdate.update_ran = saved_update_ran


# --------------------------------------------------------------------------- #
# _uv_candidate_paths / _uv_run  (no real uv, no network)
# --------------------------------------------------------------------------- #
def test_uv_candidate_paths_includes_bare_uv_and_is_nonempty():
    cands = ModuleUpdate._uv_candidate_paths()
    assert isinstance(cands, list) and cands
    # PATH lookup ("uv") is always one of the candidates regardless of platform.
    assert any(str(c) == "uv" for c in cands)


@pytest.fixture
def reset_uv_resolution_cache():
    """_uv_run caches the resolved binary path / unavailability across calls."""
    saved = (ModuleUpdate._uv_resolved_path, ModuleUpdate._uv_unavailable)
    ModuleUpdate._uv_resolved_path = None
    ModuleUpdate._uv_unavailable = False
    yield
    ModuleUpdate._uv_resolved_path, ModuleUpdate._uv_unavailable = saved


def test_uv_run_constructs_candidate_plus_args_command(monkeypatch, reset_uv_resolution_cache):
    """_uv_run runs `<candidate> <args>` and caches the first usable candidate."""
    recorded = {}

    def fake_run(cmd, check=False, **kwargs):
        recorded["cmd"] = list(cmd)
        recorded["kwargs"] = kwargs
        return subprocess.CompletedProcess(cmd, 0, "ok-stdout", "")

    monkeypatch.setattr(ModuleUpdate, "_uv_candidate_paths", lambda: [ModuleUpdate.Path("uv")])
    monkeypatch.setattr(subprocess, "run", fake_run)

    result = ModuleUpdate._uv_run(["pip", "list"], timeout=12)

    assert result.returncode == 0
    assert result.stdout == "ok-stdout"
    # Command is candidate binary followed verbatim by the supplied args.
    assert recorded["cmd"] == [ModuleUpdate.Path("uv"), "pip", "list"]
    # Non-interactive: stdin is detached and the requested timeout is forwarded.
    assert recorded["kwargs"]["stdin"] is subprocess.DEVNULL
    assert recorded["kwargs"]["timeout"] == 12
    assert recorded["kwargs"]["capture_output"] is True
    # First usable candidate is cached for subsequent calls.
    assert ModuleUpdate._uv_resolved_path == ModuleUpdate.Path("uv")


def test_uv_run_falls_through_oserror_then_returns_127(monkeypatch, reset_uv_resolution_cache):
    """Every candidate raising OSError marks uv unavailable and returns a 127
    CompletedProcess instead of raising."""
    tried = []

    def fake_run(cmd, check=False, **kwargs):
        tried.append(cmd[0])
        raise OSError("no such uv")

    monkeypatch.setattr(
        ModuleUpdate,
        "_uv_candidate_paths",
        lambda: [ModuleUpdate.Path("uv-a"), ModuleUpdate.Path("uv-b")],
    )
    monkeypatch.setattr(subprocess, "run", fake_run)

    result = ModuleUpdate._uv_run(["pip", "list"])

    assert result.returncode == 127
    assert tried == [ModuleUpdate.Path("uv-a"), ModuleUpdate.Path("uv-b")]
    assert ModuleUpdate._uv_unavailable is True


def test_uv_run_short_circuits_when_unavailable(monkeypatch, reset_uv_resolution_cache):
    """Once uv is known-unavailable, _uv_run returns 127 without touching subprocess."""
    ModuleUpdate._uv_unavailable = True

    def explode(*a, **k):  # pragma: no cover - must not be called
        raise AssertionError("subprocess.run must not run when uv is unavailable")

    monkeypatch.setattr(subprocess, "run", explode)
    result = ModuleUpdate._uv_run(["pip", "list"])
    assert result.returncode == 127


def test_uv_pip_appends_python_target():
    cmd = ModuleUpdate._uv_pip("install", "somepkg", "--no-cache")
    assert cmd[0] == "pip"
    assert cmd[1:4] == ["install", "somepkg", "--no-cache"]
    # The interpreter is pinned via --python <python_cmd> as the trailing pair.
    assert cmd[-2] == "--python"
    assert cmd[-1] == str(ModuleUpdate.python_cmd)
