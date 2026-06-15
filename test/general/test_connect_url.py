"""Tests for the mwgg:// launch-URL parser and avatar gate (deep-link PR4).

These back MultiWorld.py's protocol-launch handling: a website "Connect via
Game Client" link decomposes into connection prefs + the chosen avatar, which
get persisted before the GUI opens.
"""
from CommonClient import parse_connect_url, safe_avatar_source


def test_parse_full_room_link():
    url = ("mwgg://FlatDelilah:None@mw.prismativerse.com:62252"
           "?game=A%20Link%20to%20the%20Past&room=abc"
           "&avatar=https%3A%2F%2Fmw.prismativerse.com%2Favatar%2Fabc.png")
    parsed = parse_connect_url(url)
    assert parsed["hostname"] == "mw.prismativerse.com"
    assert parsed["port"] == 62252
    assert parsed["name"] == "FlatDelilah"
    assert parsed["password"] is None  # :None@ encodes "no password"
    assert parsed["game"] == "A Link to the Past"
    assert parsed["avatar"] == "https://mw.prismativerse.com/avatar/abc.png"


def test_parse_archipelago_scheme_and_real_password():
    parsed = parse_connect_url("archipelago://name:secret@host:38281")
    assert parsed["hostname"] == "host"
    assert parsed["port"] == 38281
    assert parsed["name"] == "name"
    assert parsed["password"] == "secret"


def test_parse_rejects_non_connection_urls():
    assert parse_connect_url("https://example.com") is None
    assert parse_connect_url("/path/to/patch.aplttp") is None
    assert parse_connect_url("") is None
    assert parse_connect_url(None) is None


def test_safe_avatar_source_allows_trusted_https():
    for url in ("https://mw.prismativerse.com/avatar/abc.png",
                "https://multiworld.gg/avatar/abc.png"):
        assert safe_avatar_source(url) == url


def test_safe_avatar_source_rejects_untrusted_or_insecure():
    assert safe_avatar_source("https://evil.example/x.png") == ""
    assert safe_avatar_source("http://multiworld.gg/avatar/x.png") == ""  # not https
    assert safe_avatar_source("") == ""
    assert safe_avatar_source("not a url") == ""
