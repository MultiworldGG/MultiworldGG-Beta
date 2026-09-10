import unittest
from MultiServer import Context, ServerCommandProcessor, raw_argument, split_command


class TestCommandSplitting(unittest.TestCase):
    def test_split_command(self) -> None:
        self.assertEqual(split_command('/send "My Name" Bow'), ["/send", "My Name", "Bow"])
        self.assertEqual(split_command("/send \u201cMy Name\u201d Bow"), ["/send", "My Name", "Bow"])
        self.assertEqual(split_command("/send \"My Name\" Link's Bow"), ["/send", "My Name", "Link's", "Bow"])
        self.assertEqual(split_command("/send 'My Name' Bow"), ["/send", "'My", "Name'", "Bow"])
        self.assertEqual(split_command(r"/send C:\path Bow"), ["/send", r"C:\path", "Bow"])
        self.assertEqual(split_command('/send "My Name Bow'), ["/send", '"My', "Name", "Bow"])
        self.assertEqual(split_command("/players   "), ["/players"])

    def test_raw_argument(self) -> None:
        self.assertIsNone(raw_argument("/release"))
        self.assertIsNone(raw_argument("/release   "))
        self.assertEqual(raw_argument("/release My Name"), "My Name")
        self.assertEqual(raw_argument("/release My Name  "), "My Name")
        self.assertEqual(raw_argument('/release "My Name"'), "My Name")
        self.assertEqual(raw_argument("/release \u201cMy Name\u201d"), "My Name")
        self.assertEqual(raw_argument('!admin /release "My Name"'), '/release "My Name"')
        self.assertEqual(raw_argument("/release Link's"), "Link's")
        self.assertEqual(raw_argument('/release "'), '"')


class TestResolvePlayerName(unittest.TestCase):
    def test_resolve(self) -> None:
        p = ServerCommandProcessor(Context("", 0, "", "", 0, 0, False))
        p.ctx.player_names = {
            (1, 1): "AAA",
            (1, 2): "aBc",
            (1, 3): "abC",
        }
        assert not p.resolve_player("abc"), "ambiguous name entry shouldn't resolve to player"
        assert not p.resolve_player("Abc"), "ambiguous name entry shouldn't resolve to player"
        assert p.resolve_player("aBc") == (1, 2, "aBc"), "matching case resolve"
        assert p.resolve_player("abC") == (1, 3, "abC"), "matching case resolve"
        assert not p.resolve_player("aB"), "partial name shouldn't resolve to player"
        assert not p.resolve_player("abCD"), "incorrect name shouldn't resolve to player"

        p.ctx.player_names = {
            (1, 1): "aaa",
            (1, 2): "abc",
            (1, 3): "abC",
        }
        assert p.resolve_player("abc") == (1, 2, "abc"), "matching case resolve"
        assert not p.resolve_player("Abc"), "ambiguous name entry shouldn't resolve to player"
        assert not p.resolve_player("aBc"), "ambiguous name entry shouldn't resolve to player"
        assert p.resolve_player("abC") == (1, 3, "abC"), "matching case resolve"

        p.ctx.player_names = {
            (1, 1): "AbcdE",
            (1, 2): "abc",
            (1, 3): "abCD",
        }
        assert p.resolve_player("abc") == (1, 2, "abc"), "matching case resolve"
        assert p.resolve_player("abC") == (1, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("Abc") == (1, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("ABC") == (1, 2, "abc"), "case insensitive resolves when 1 match"
        assert p.resolve_player("abcd") == (1, 3, "abCD"), "case insensitive resolves when 1 match"
        assert not p.resolve_player("aB"), "partial name shouldn't resolve to player"
