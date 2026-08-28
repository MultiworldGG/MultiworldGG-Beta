"""Tests for the SECRET_KEY production-default guardrail in WebHost.get_app()."""
from __future__ import annotations

import socket

import pytest


def test_get_app_refuses_hostname_secret_in_production(monkeypatch):
    """The webhost must refuse to boot if SECRET_KEY is still the hostname-derived
    default and TESTING is False: that key signs session cookies and is
    trivially forgeable by anyone who can guess the host name."""
    from WebHostLib import app as raw_app
    import WebHost

    # Force the hostname-derived default and clear any test-mode override.
    raw_app.config["SECRET_KEY"] = bytes(socket.gethostname(), encoding="utf-8")
    raw_app.config["TESTING"] = False

    # Don't let an actual config.yaml on disk override it during the test.
    monkeypatch.setattr(WebHost.os.path, "exists", lambda p: False)

    with pytest.raises(RuntimeError, match="SECRET_KEY is still the hostname-derived default"):
        WebHost.get_app()


def test_get_app_allows_hostname_secret_when_testing(monkeypatch):
    """The same default is fine under TESTING=True (the project's pytest fixture sets it)."""
    from WebHostLib import app as raw_app
    import WebHost

    raw_app.config["SECRET_KEY"] = bytes(socket.gethostname(), encoding="utf-8")
    raw_app.config["TESTING"] = True
    raw_app.config["PONY"] = {"provider": "sqlite", "filename": ":memory:", "create_db": True}

    monkeypatch.setattr(WebHost.os.path, "exists", lambda p: False)

    # Should not raise: TESTING=True bypasses the guardrail. We don't care
    # about the return value; if it returns, the guardrail didn't trip.
    try:
        WebHost.get_app()
    except (AssertionError, ValueError) as e:
        # get_app() raises on duplicate blueprint registration when called more than once
        # in the same process (AssertionError on older Flask, ValueError on Flask 3.x);
        # that's fine for this test (we only care that RuntimeError isn't raised by the guardrail).
        message = e.args[0] if e.args else str(e)
        if "register_blueprint" not in message and "already registered" not in message:
            raise
