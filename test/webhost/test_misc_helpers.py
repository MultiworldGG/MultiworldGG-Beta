"""Unit tests for pure/IO helpers in ``WebHostLib.misc``.

These pin two non-obvious behaviors that were previously documented only by
inline comments:

* how ``format_authors_string`` joins three-or-more authors, and
* how ``_read_log`` consumes (or seeks past) an optional UTF-8 BOM and then
  applies ``offset`` relative to the current stream position.
"""
import io

from WebHostLib.misc import format_authors_string, _read_log


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
