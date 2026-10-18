"""server_password is the pre-rename spelling of admin_password; multidata, saves and
command lines written before the rename must still reach Context.admin_password."""

import asyncio
import logging
import os
import pickle
import signal
import sys
import tempfile
import types
import unittest
import zlib
from unittest import mock

import MultiServer
from MultiServer import Context
from NetUtils import NetworkSlot, SlotType


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


class _Stop(Exception):
    pass


class TestCommandLinePasswordOutranksSave(unittest.TestCase):
    """The launcher's host dialog passes --admin-password; a save written with another
    password must not replace it, or remote admin answers "disabled"."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.data = os.path.join(tmp.name, "AP_TEST.archipelago")
        multidata = {
            "slot_info": {1: NetworkSlot("Player1", "Game A", SlotType.player)},
            "connect_names": {"Player1": (0, 1)},
            "locations": {1: {}},
            "slot_data": {1: {}},
            "er_hint_data": {},
            "precollected_items": {1: []},
            "precollected_hints": {1: set()},
            "version": (0, 6, 2),
            "minimum_versions": {"server": (0, 1, 6), "clients": {}},
            "seed_name": "TESTSEED",
            "datapackage": {"Game A": {"item_name_to_id": {}, "location_name_to_id": {}, "item_name_groups": {}}},
        }
        with open(self.data, "wb") as f:
            f.write(bytes([3]) + zlib.compress(pickle.dumps(multidata)))
        no_autosave = mock.patch.object(Context, "_start_async_saving")
        no_autosave.start()
        self.addCleanup(no_autosave.stop)

        ctx = Context("", 0, "saved", None, 1, 10, True)
        ctx.load(self.data)
        ctx.init_save()
        self.assertTrue(ctx._save())

    def _run_main(self, *flags: str) -> Context:
        created = []
        init_save = Context.init_save

        def recording_init_save(ctx: Context, *args, **kwargs) -> None:
            created.append(ctx)
            init_save(ctx, *args, **kwargs)

        with mock.patch.object(sys, "argv", ["MultiServer", self.data, *flags]):
            args = MultiServer.parse_args()
        sigint = signal.getsignal(signal.SIGINT)
        try:
            with mock.patch.object(Context, "init_save", recording_init_save), \
                    mock.patch.object(MultiServer.Utils, "init_logging"), \
                    mock.patch.object(MultiServer.websockets, "serve", side_effect=_Stop):
                with self.assertRaises(_Stop):
                    asyncio.run(MultiServer.main(args))
        finally:
            signal.signal(signal.SIGINT, sigint)
        return created[0]

    def test_command_line_password_beats_save(self) -> None:
        self.assertEqual(self._run_main("--admin-password", "typed").admin_password, "typed")

    def test_save_beats_host_yaml_default(self) -> None:
        self.assertEqual(self._run_main().admin_password, "saved")


if __name__ == "__main__":
    unittest.main()
