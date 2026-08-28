"""Tests for the breadcrumb Jinja macro."""

import pytest
from jinja2 import Environment, FileSystemLoader


@pytest.fixture
def env():
    # url_for must be a Jinja global so the imported macro can see it;
    # macros don't inherit the caller's render-context kwargs.
    env = Environment(
        loader=FileSystemLoader("WebHostLib/templates"),
    )
    env.globals["url_for"] = lambda endpoint, **kw: f"/{endpoint}"
    return env


def test_breadcrumb_renders_with_home_link(env):
    template = env.from_string(
        "{% from 'header/breadcrumb.html' import breadcrumb %}"
        "{{ breadcrumb([('Play', '/play'), ('Lobbies', '/play/lobbies')]) }}"
    )
    rendered = template.render()

    assert 'aria-label="Breadcrumb"' in rendered
    assert "/landing" in rendered  # home link
    assert "/play" in rendered
    assert "Lobbies" in rendered
    assert "mw-breadcrumb-current" in rendered  # last item is current


def test_breadcrumb_with_context(env):
    template = env.from_string(
        "{% from 'header/breadcrumb.html' import breadcrumb %}"
        "{{ breadcrumb([('Room', none)], context='2 slots') }}"
    )
    rendered = template.render()

    assert "mw-breadcrumb-context" in rendered
    assert "2 slots" in rendered


def test_breadcrumb_last_item_not_linked(env):
    template = env.from_string(
        "{% from 'header/breadcrumb.html' import breadcrumb %}"
        "{{ breadcrumb([('Play', '/play'), ('Current', '/somewhere')]) }}"
    )
    rendered = template.render()

    # Last item should NOT be an <a>, regardless of url being set
    assert ">Current<" in rendered
    # And should be in the "current" span
    assert 'mw-breadcrumb-current">Current' in rendered
