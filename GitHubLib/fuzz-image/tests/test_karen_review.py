"""Tests for Karen, the apworld-PR security reviewer (``karen_review.py``).

The module is loaded via the ``karen`` session fixture in conftest.py (it is a
standalone script, not an importable package module).

No real network, subprocess, or Docker is exercised: ``urllib.request.urlopen``,
``shutil.which`` and ``subprocess.run`` are monkeypatched on the loaded module
wherever a check would otherwise reach out. Only stdlib + jsonschema are used.
"""
import hashlib
import io
import json
import zipfile
from pathlib import Path


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _zip_bytes(members: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    return buf.getvalue()


class _FakeResponse:
    """Minimal stand-in for the urlopen context-manager / response object."""

    def __init__(self, data: bytes):
        self._buf = io.BytesIO(data)

    def read(self, size: int = -1) -> bytes:
        return self._buf.read(size)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _patch_urlopen(karen, monkeypatch, data: bytes) -> None:
    monkeypatch.setattr(
        karen.urllib.request, "urlopen", lambda req, timeout=None: _FakeResponse(data)
    )


# --------------------------------------------------------------------------- #
# 1. network-at-import AST scan
# --------------------------------------------------------------------------- #
def test_top_level_network_call_fails_but_nested_is_ignored(karen, tmp_path):
    (tmp_path / "m.py").write_text(
        "import requests\n"
        "requests.get('http://example.com')\n"
        "\n"
        "def fetch():\n"
        "    return requests.post('http://nested')\n",
        encoding="utf-8",
    )
    calls, imports = karen._scan_module_for_network(tmp_path / "m.py")

    # The top-level call is flagged; the post() buried in a def is NOT.
    assert any("requests.get" in c for c in calls)
    assert not any("requests.post" in c for c in calls)
    # The top-level import is surfaced separately (warn-level signal).
    assert any("import requests" in i for i in imports)

    result = karen.check_no_network_at_import(tmp_path)
    assert result.status == "fail"  # a real top-level call => fail, not warn
    assert any("requests.get" in d for d in result.details)


def test_top_level_import_without_call_warns(karen, tmp_path):
    (tmp_path / "m.py").write_text("import requests\n", encoding="utf-8")

    result = karen.check_no_network_at_import(tmp_path)

    assert result.status == "warn"
    assert any("import requests" in d for d in result.details)


# --------------------------------------------------------------------------- #
# 2. & 3. wheel download / expand: zip-slip, SHA gate
# --------------------------------------------------------------------------- #
def test_wheel_zip_slip_member_is_rejected(karen, tmp_path, monkeypatch):
    _patch_urlopen(karen, monkeypatch, _zip_bytes({"../evil.py": b"x = 1"}))

    ok, msg = karen._download_and_expand_wheel(
        "https://example.com/pkg/foo-1.0-py3-none-any.whl", tmp_path / "world"
    )

    assert ok is False
    assert "unsafe path" in msg
    # The traversal target must NOT have been written outside dest.
    assert not (tmp_path / "evil.py").exists()


def test_wheel_sha256_mismatch_rejected_before_expansion(karen, tmp_path, monkeypatch):
    payload = _zip_bytes({"foo/__init__.py": b"VALUE = 7\n"})
    _patch_urlopen(karen, monkeypatch, payload)

    url = "https://example.com/pkg/foo-1.0-py3-none-any.whl#sha256=deadbeef"
    ok, msg = karen._download_and_expand_wheel(url, tmp_path / "world")

    assert ok is False
    assert "SHA256 mismatch" in msg
    # Expansion aborted: the contained module was never extracted.
    assert not (tmp_path / "world" / "foo" / "__init__.py").exists()


def test_wheel_matching_sha256_expands(karen, tmp_path, monkeypatch):
    payload = _zip_bytes({"foo/__init__.py": b"VALUE = 7\n"})
    _patch_urlopen(karen, monkeypatch, payload)
    good = hashlib.sha256(payload).hexdigest()

    url = f"https://example.com/pkg/foo-1.0-py3-none-any.whl#sha256={good}"
    dest = tmp_path / "world"
    ok, msg = karen._download_and_expand_wheel(url, dest)

    assert ok is True
    extracted = dest / "foo" / "__init__.py"
    assert extracted.read_text(encoding="utf-8") == "VALUE = 7\n"


# --------------------------------------------------------------------------- #
# 4. schema validation
# --------------------------------------------------------------------------- #
_MINIMAL_SCHEMA = {
    "type": "object",
    "required": ["game"],
    "properties": {"game": {"type": "string"}},
}


def _write_schema(tmp_path: Path) -> Path:
    sp = tmp_path / "schema.json"
    sp.write_text(json.dumps(_MINIMAL_SCHEMA), encoding="utf-8")
    return sp


def test_schema_present_required_field_passes(karen, tmp_path):
    schema = _write_schema(tmp_path)
    manifest = tmp_path / "foo.json"
    manifest.write_text(json.dumps({"game": "Some Game"}), encoding="utf-8")

    result = karen.check_schema(manifest, schema)

    assert result.status == "pass"
    assert result.details == []


def test_schema_missing_required_field_fails_with_detail(karen, tmp_path):
    schema = _write_schema(tmp_path)
    manifest = tmp_path / "foo.json"
    manifest.write_text(json.dumps({}), encoding="utf-8")

    result = karen.check_schema(manifest, schema)

    assert result.status == "fail"
    assert len(result.details) == 1
    assert "'game' is a required property" in result.details[0]


# --------------------------------------------------------------------------- #
# 5. manifest consistency
# --------------------------------------------------------------------------- #
def test_manifest_consistency_flags_duplicate_keys(karen, tmp_path):
    manifest = tmp_path / "foo.json"
    manifest.write_text('{"game": "A", "game": "B"}', encoding="utf-8")

    result = karen.check_manifest_consistency(manifest)

    assert result.status == "fail"
    assert any("duplicate keys" in d and "game" in d for d in result.details)


def test_manifest_consistency_flags_url_apworld_mismatch(karen, tmp_path):
    manifest = tmp_path / "foo.json"
    manifest.write_text(
        json.dumps({"module_location": "https://github.com/o/r/tree/main/worlds/bar"}),
        encoding="utf-8",
    )

    result = karen.check_manifest_consistency(manifest)

    assert result.status == "fail"
    # filename stem is 'foo' but the URL points at 'bar'.
    assert any("'bar'" in d and "'foo'" in d for d in result.details)


def test_manifest_consistency_flags_bad_stem(karen, tmp_path):
    manifest = tmp_path / "Foo-Bar.json"  # uppercase + hyphen are illegal
    manifest.write_text(json.dumps({"game": "x"}), encoding="utf-8")

    result = karen.check_manifest_consistency(manifest)

    assert result.status == "fail"
    assert any("lowercase alphanumeric" in d for d in result.details)


def test_manifest_consistency_passes_when_consistent(karen, tmp_path):
    manifest = tmp_path / "foo.json"
    manifest.write_text(
        json.dumps({"module_location": "https://github.com/o/r/tree/main/worlds/foo"}),
        encoding="utf-8",
    )

    assert karen.check_manifest_consistency(manifest).status == "pass"


# --------------------------------------------------------------------------- #
# 6. no ROM files
# --------------------------------------------------------------------------- #
def test_no_rom_files_flags_rom_extension(karen, tmp_path):
    (tmp_path / "game.z64").write_bytes(b"ROM")
    (tmp_path / "world.py").write_text("x = 1\n", encoding="utf-8")
    # Files inside .git / __pycache__ must be ignored even with a ROM suffix.
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "packed.z64").write_bytes(b"x")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "cached.nes").write_bytes(b"x")

    result = karen.check_no_rom_files(tmp_path)

    assert result.status == "fail"
    assert result.details == ["game.z64"]  # only the real ROM, dirs skipped


def test_no_rom_files_passes_for_pure_python(karen, tmp_path):
    (tmp_path / "world.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "data.json").write_text("{}", encoding="utf-8")

    assert karen.check_no_rom_files(tmp_path).status == "pass"


# --------------------------------------------------------------------------- #
# 7. URL parsing helpers
# --------------------------------------------------------------------------- #
def test_parse_module_location_github_tree(karen):
    parsed = karen._parse_module_location(
        "https://github.com/MyOrg/MyRepo/tree/v1.2/worlds/foo"
    )
    assert parsed == {
        "clone_url": "https://github.com/MyOrg/MyRepo.git",
        "ref": "v1.2",
        "subpath": "worlds/foo",
    }


def test_parse_module_location_git_https_defaults_ref_to_head(karen):
    no_ref = karen._parse_module_location("git+https://github.com/o/r.git")
    with_ref = karen._parse_module_location("git+https://github.com/o/r.git@abc123")

    assert no_ref["ref"] == "HEAD"
    assert no_ref["clone_url"] == "https://github.com/o/r.git"
    assert with_ref["ref"] == "abc123"


def test_parse_module_location_unsupported_returns_none(karen):
    assert karen._parse_module_location("https://example.com/foo.tar.gz") is None


def test_is_wheel_url_and_sha_extraction(karen):
    assert karen._is_wheel_url("https://x/y/foo-1.0-py3-none-any.whl") is True
    assert karen._is_wheel_url("https://x/y/foo.tar.gz") is False
    # sha256 fragment is lowercased; absent fragment yields None.
    assert karen._wheel_sha256("https://x/y/foo.whl#sha256=ABCDEF") == "abcdef"
    assert karen._wheel_sha256("https://x/y/foo.whl") is None


# --------------------------------------------------------------------------- #
# 8. rendering + overall precedence
# --------------------------------------------------------------------------- #
def test_overall_precedence_fail_beats_warn_beats_pass(karen):
    world_fail = karen.WorldReview(
        "foo",
        "worlds/foo.json",
        checks=[
            karen.CheckResult("a", "pass"),
            karen.CheckResult("b", "warn"),
            karen.CheckResult("c", "fail"),
        ],
    )
    world_warn = karen.WorldReview(
        "bar",
        "worlds/bar.json",
        checks=[karen.CheckResult("a", "pass"), karen.CheckResult("b", "warn")],
    )
    world_pass = karen.WorldReview(
        "baz", "worlds/baz.json", checks=[karen.CheckResult("a", "pass")]
    )

    assert world_fail.overall == "fail"
    assert world_warn.overall == "warn"
    assert world_pass.overall == "pass"
    # Run rolls up to the worst member.
    assert karen.ReviewRun(worlds=[world_pass, world_warn]).overall == "warn"
    assert karen.ReviewRun(worlds=[world_pass, world_warn, world_fail]).overall == "fail"


def test_render_comment_contains_marker_fail_glyph_and_footer(karen):
    world = karen.WorldReview(
        "foo",
        "worlds/foo.json",
        checks=[
            karen.CheckResult("schema", "fail", "bad", details=["root: nope"]),
        ],
    )
    comment = karen.render_comment(karen.ReviewRun(worlds=[world]))

    assert karen.PR_COMMENT_MARKER in comment
    assert karen._STATUS_GLYPH["fail"] in comment
    # Failing-run footer.
    assert "There are some problems" in comment
    # fail-level details are expanded.
    assert "root: nope" in comment


def test_render_summary_shape(karen):
    world = karen.WorldReview(
        "foo",
        "worlds/foo.json",
        checks=[karen.CheckResult("schema", "pass", "ok", details=["d1"])],
    )
    summary = karen.render_summary(karen.ReviewRun(worlds=[world]))

    assert set(summary) == {"overall", "worlds"}
    assert summary["overall"] == "pass"
    (w,) = summary["worlds"]
    assert set(w) == {"apworld", "manifest_path", "overall", "checks"}
    (check,) = w["checks"]
    assert set(check) == {"name", "status", "message", "details"}
    assert check["name"] == "schema"
    assert check["status"] == "pass"
    assert check["details"] == ["d1"]


# --------------------------------------------------------------------------- #
# 9. CLI exit codes (no clone/network path is reached)
# --------------------------------------------------------------------------- #
def test_cli_no_changed_returns_zero_and_writes_trivial_comment(karen, tmp_path):
    comment = tmp_path / "comment.md"

    rc = karen._cli(["--output-comment", str(comment)])

    assert rc == 0
    text = comment.read_text(encoding="utf-8")
    assert karen.PR_COMMENT_MARKER in text
    assert "No new or updated index entries" in text


def test_cli_world_dir_with_two_changed_errors(karen, tmp_path):
    import pytest

    with pytest.raises(SystemExit) as exc:
        karen._cli(
            [
                "--world-dir",
                str(tmp_path),
                "--changed",
                "a.json",
                "--changed",
                "b.json",
            ]
        )
    # argparse parser.error() exits with code 2.
    assert exc.value.code == 2


def test_cli_single_missing_changed_yields_schema_fail_and_returns_one(karen, tmp_path):
    summary = tmp_path / "summary.json"
    missing = tmp_path / "does_not_exist.json"

    rc = karen._cli(
        [
            "--changed",
            str(missing),
            # restrict to fast checks so no clone/network path is taken
            "--check",
            "schema",
            "--check",
            "manifest_consistency",
            "--output-summary",
            str(summary),
        ]
    )

    assert rc == 1
    data = json.loads(summary.read_text(encoding="utf-8"))
    assert data["overall"] == "fail"
    (world,) = data["worlds"]
    (check,) = world["checks"]
    assert check["name"] == "schema"
    assert check["status"] == "fail"
    assert "file not found" in check["message"]


# --------------------------------------------------------------------------- #
# 10. bandit / pip-audit cheap branches
# --------------------------------------------------------------------------- #
def test_bandit_tool_missing_fails(karen, tmp_path, monkeypatch):
    monkeypatch.setattr(karen.shutil, "which", lambda name: None)

    result = karen.check_bandit(tmp_path)

    assert result.status == "fail"
    assert "bandit" in result.message.lower()


def test_pip_audit_tool_missing_fails(karen, tmp_path, monkeypatch):
    monkeypatch.setattr(karen.shutil, "which", lambda name: None)

    result = karen.check_pip_audit(tmp_path)

    assert result.status == "fail"
    assert "pip-audit" in result.message.lower()


def test_bandit_non_json_output_fails(karen, tmp_path, monkeypatch):
    monkeypatch.setattr(karen.shutil, "which", lambda name: "/usr/bin/" + name)

    class _Proc:
        stdout = "not json at all"
        stderr = ""
        returncode = 1

    monkeypatch.setattr(karen.subprocess, "run", lambda *a, **k: _Proc())

    result = karen.check_bandit(tmp_path)

    assert result.status == "fail"
    assert "JSON" in result.message


def test_bandit_skips_when_not_a_directory(karen, tmp_path):
    result = karen.check_bandit(tmp_path / "missing_dir")

    assert result.status == "skip"
