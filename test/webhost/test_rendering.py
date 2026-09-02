"""Webhost rendering-helper tests; add new rendering tests here.

Covers the breadcrumb Jinja macro, the /play setup-checklist partial,
``render_markdown`` heading ids and self-links, and pure/IO helpers in ``WebHostLib.misc`` that pin two
non-obvious behaviors previously documented only by inline comments: how
``format_authors_string`` joins three-or-more authors, and how ``_read_log``
consumes (or seeks past) an optional UTF-8 BOM and then applies ``offset``
relative to the current stream position.
"""
import io
import os
import re
import unittest
from tempfile import NamedTemporaryFile

import pytest
from jinja2 import Environment, FileSystemLoader

from WebHostLib.markdown import render_markdown
from WebHostLib.misc import format_authors_string, _read_log


# ---------------------------------------------------------------------------
# Breadcrumb Jinja macro
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# /play setup checklist partial
# ---------------------------------------------------------------------------

def test_play_checklist_is_ephemeral(env):
    rendered = env.get_template("partials/play_checklist.html").render()

    boxes = re.findall(r'<input[^>]*type="checkbox"[^>]*>', rendered)
    assert len(boxes) == 7
    # Without autocomplete=off Firefox restores checkbox state across reloads.
    assert all('autocomplete="off"' in box for box in boxes)
    assert 'data-tooltip="Pick a game, player options, and turn the YAML in"' in rendered
    assert 'data-tooltip="GO!"' in rendered


# ---------------------------------------------------------------------------
# render_markdown heading ids and self-links
# ---------------------------------------------------------------------------

def _render(document: str) -> str:
    f = NamedTemporaryFile(delete=False)
    try:
        f.write(document.encode("utf-8"))
        f.close()
        return render_markdown(f.name)
    finally:
        os.unlink(f.name)


class RenderMarkdownHeadingTest(unittest.TestCase):
    def test_render_markdown_headings_self_link_and_dedupe_ids(self) -> None:
        html = _render("# Setup\n\n## Setup\n\n## Setup\n")
        # Every heading (level < 4) gets an id and its text wrapped in an anchor
        # that links to that same id.
        self.assertIn('<h1 id="setup"><a href="#setup">Setup</a></h1>', html)
        # Duplicate heading texts get de-duplicated id suffixes starting at -1.
        self.assertIn('<h2 id="setup-1"><a href="#setup-1">Setup</a></h2>', html)
        self.assertIn('<h2 id="setup-2"><a href="#setup-2">Setup</a></h2>', html)

    def test_render_markdown_heading_id_slugifies_text(self) -> None:
        html = _render("### Other Heading!\n")
        # Non-id characters are stripped, text is lowercased, spaces become hyphens.
        self.assertIn('<h3 id="other-heading"><a href="#other-heading">Other Heading!</a></h3>', html)

    def test_render_markdown_level_four_heading_is_not_linked(self) -> None:
        html = _render("#### Deep Heading\n")
        # Only headings with level < 4 are given an id / self-link.
        self.assertIn("<h4>Deep Heading</h4>", html)
        self.assertNotIn("href=", html)
        self.assertNotIn("id=", html)


# ---------------------------------------------------------------------------
# WebHostLib.misc pure/IO helpers
# ---------------------------------------------------------------------------

def test_format_authors_string_empty_returns_empty_string():
    assert format_authors_string([]) == ""


def test_format_authors_string_single_returns_the_name():
    assert format_authors_string(["Alice"]) == "Alice"


def test_format_authors_string_two_joined_by_ampersand():
    assert format_authors_string(["Alice", "Bob"]) == "Alice & Bob"


def test_format_authors_string_three_or_more_uses_commas_and_ampersand():
    # Final two separated by " & ", the rest by ", ", with no Oxford comma.
    assert format_authors_string(["Alice", "Bob", "Carol"]) == "Alice, Bob & Carol"
    assert (
        format_authors_string(["Alice", "Bob", "Carol", "Dave"])
        == "Alice, Bob, Carol & Dave"
    )


def test_read_log_skips_utf8_bom_but_keeps_content_when_absent():
    with_bom = io.BytesIO(b"\xEF\xBB\xBFhello world")
    assert b"".join(_read_log(with_bom)) == b"hello world"

    without_bom = io.BytesIO(b"hello world")
    assert b"".join(_read_log(without_bom)) == b"hello world"


def test_read_log_offset_is_relative_to_position_after_bom():
    # With a BOM the 3 BOM bytes are consumed first, so offset=6 then skips
    # the next 6 content bytes ("hello ") and yields "world".
    with_bom = io.BytesIO(b"\xEF\xBB\xBFhello world")
    assert b"".join(_read_log(with_bom, 6)) == b"world"

    # Without a BOM the stream is rewound to byte 0, so the same offset of 6
    # lands at the same content position.
    without_bom = io.BytesIO(b"hello world")
    assert b"".join(_read_log(without_bom, 6)) == b"world"


def test_read_log_handles_file_shorter_than_bom():
    # A 2-byte file can't hold the 3-byte BOM; it must not be mistaken for one
    # and no content may be lost.
    short = io.BytesIO(b"hi")
    assert b"".join(_read_log(short)) == b"hi"
