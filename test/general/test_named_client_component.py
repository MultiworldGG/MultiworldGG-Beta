"""Tests for the named-client-component launch path (--component).

spawn_client(component=...) appends `--component <display_name>` to the child
argv; the child forwards it through _resolve_client_route's route_kwargs and
Utils._perform_module_launch resolves it via
Utils._resolve_named_client_component -- a module-scoped scan that must never
let another world's registrations be reachable by name, and must fall back to
default client resolution (never die) on an unknown or non-client name.
"""
import logging

import pytest

import LauncherComponents as lc
import Utils


def _fake_launch(*args):
    pass


def _other_launch(*args):
    pass


@pytest.fixture
def registered(request):
    """Append Components to the live registry and always remove them."""
    added: list[lc.Component] = []

    def _register(component: lc.Component) -> lc.Component:
        lc.components.append(component)
        added.append(component)
        return component

    yield _register
    for component in added:
        lc.components.remove(component)


def test_resolve_named_client_component_scoped_match(registered, monkeypatch):
    monkeypatch.setattr(_fake_launch, "__module__", "worlds.kh2.submod", raising=False)
    monkeypatch.setattr(_other_launch, "__module__", "worlds.other", raising=False)
    registered(lc.Component("Alt Client", func=_other_launch, component_type=lc.Type.CLIENT))
    target = registered(lc.Component("Alt Client", func=_fake_launch, component_type=lc.Type.CLIENT))

    resolved = Utils._resolve_named_client_component("worlds.kh2", "Alt Client")

    assert resolved is target.func


def test_resolve_named_client_component_rejects_other_modules(registered, monkeypatch, caplog):
    monkeypatch.setattr(_other_launch, "__module__", "worlds.other", raising=False)
    registered(lc.Component("Alt Client", func=_other_launch, component_type=lc.Type.CLIENT))

    with caplog.at_level(logging.WARNING):
        resolved = Utils._resolve_named_client_component("worlds.kh2", "Alt Client")

    assert resolved is None
    assert any("falling back" in record.message for record in caplog.records)


def test_resolve_named_client_component_rejects_non_client_types(registered, monkeypatch, caplog):
    monkeypatch.setattr(_fake_launch, "__module__", "worlds.kh2", raising=False)
    registered(lc.Component("KH2 Fixup", func=_fake_launch, component_type=lc.Type.TOOL))

    with caplog.at_level(logging.WARNING):
        resolved = Utils._resolve_named_client_component("worlds.kh2", "KH2 Fixup")

    assert resolved is None


def test_resolve_client_route_forwards_component(monkeypatch):
    import MultiWorld

    monkeypatch.setattr(Utils, "get_available_worlds", lambda: {"kh2"})
    args = MultiWorld.make_arg_parser().parse_args(
        ["--game", "kh2", "--component", "Alt Client"])

    route_module, route_kwargs = MultiWorld._resolve_client_route(args)

    assert route_module == "kh2"
    assert route_kwargs["component"] == "Alt Client"


def test_resolve_client_route_component_defaults_to_none(monkeypatch):
    import MultiWorld

    monkeypatch.setattr(Utils, "get_available_worlds", lambda: {"kh2"})
    args = MultiWorld.make_arg_parser().parse_args(["--game", "kh2"])

    _route_module, route_kwargs = MultiWorld._resolve_client_route(args)

    assert route_kwargs["component"] is None
