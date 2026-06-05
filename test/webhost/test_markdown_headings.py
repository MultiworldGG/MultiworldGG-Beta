import os
import unittest
from tempfile import NamedTemporaryFile

from WebHostLib.markdown import render_markdown


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


if __name__ == "__main__":
    unittest.main()
