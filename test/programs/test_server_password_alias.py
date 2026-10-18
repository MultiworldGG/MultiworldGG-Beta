"""server_password is the pre-rename spelling of admin_password; multidata, saves and
command lines written before the rename must still reach Context.admin_password."""

import logging
import sys
import types
import unittest
from unittest import mock

import MultiServer
from MultiServer import Context


def _stub() -> types.SimpleNamespace:
    return types.SimpleNamespace(simple_options=Context.simple_options, logger=logging.getLogger("test"),
                                 admin_password=None, item_cheat=True)


class TestServerPasswordAlias(unittest.TestCase):
    def test_set_options_migrates_legacy_key(self) -> None:
        ctx = _stub()
        Context._set_options(ctx, {"server_password": "legacy"})
        self.assertEqual(ctx.admin_password, "legacy")

    def test_set_options_prefers_admin_password(self) -> None:
        ctx = _stub()
        Context._set_options(ctx, {"admin_password": "new", "server_password": "old"})
        self.assertEqual(ctx.admin_password, "new")

    def test_command_line_alias(self) -> None:
        with mock.patch.object(sys, "argv", ["MultiServer", "--server-password", "legacy"]):
            args = MultiServer.parse_args()
        self.assertEqual(args.admin_password, "legacy")
        self.assertFalse(hasattr(args, "server_password"))


if __name__ == "__main__":
    unittest.main()
