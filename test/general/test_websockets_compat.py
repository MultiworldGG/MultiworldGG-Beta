"""World clients written against websockets 13.x (shipped MWGG) check server
liveness via the legacy `ctx.server.socket.closed` / `.open` attributes (e.g.
kh3's _is_ap_connected). The websockets 14+ asyncio Connection removed both, so
CommonClient restores them as State-backed properties; these tests pin that
compat surface and its legacy semantics (both False while opening/closing).
"""
import unittest
from types import SimpleNamespace

from websockets.asyncio.client import ClientConnection
from websockets.asyncio.connection import Connection
from websockets.protocol import State

import CommonClient  # noqa: F401  importing it installs the compat properties


class TestWebsocketsLegacyCompat(unittest.TestCase):
    def test_compat_properties_installed(self) -> None:
        for name in ("closed", "open"):
            with self.subTest(name=name):
                self.assertIsInstance(getattr(Connection, name, None), property)

    def test_client_connection_inherits_compat(self) -> None:
        # The object world clients actually touch is ctx.server.socket, a
        # ClientConnection returned by websockets.connect in server_loop.
        for name in ("closed", "open"):
            with self.subTest(name=name):
                self.assertTrue(hasattr(ClientConnection, name))

    def test_closed_matches_legacy_semantics(self) -> None:
        # legacy: closed is True only once fully CLOSED
        for state, expected in ((State.CONNECTING, False), (State.OPEN, False),
                                (State.CLOSING, False), (State.CLOSED, True)):
            with self.subTest(state=state):
                stub = SimpleNamespace(state=state)
                self.assertIs(Connection.closed.fget(stub), expected)

    def test_open_matches_legacy_semantics(self) -> None:
        # legacy: open is True only while fully OPEN
        for state, expected in ((State.CONNECTING, False), (State.OPEN, True),
                                (State.CLOSING, False), (State.CLOSED, False)):
            with self.subTest(state=state):
                stub = SimpleNamespace(state=state)
                self.assertIs(Connection.open.fget(stub), expected)

    def test_world_client_liveness_check_pattern(self) -> None:
        # The exact expression kh3 uses: bool(server and socket and not socket.closed)
        server = SimpleNamespace(socket=SimpleNamespace(state=State.OPEN))
        server.socket.closed = Connection.closed.fget(server.socket)
        self.assertTrue(bool(server and server.socket and not server.socket.closed))

    def test_deprecation_warning_once_per_call_site(self) -> None:
        # Accessing a legacy attribute surfaces a warning in the client log,
        # but only once per call site -- these checks sit in per-package loops.
        stub = SimpleNamespace(state=State.OPEN)
        with self.assertLogs("Client", level="WARNING") as logs:
            for _ in range(3):
                Connection.closed.fget(stub)  # one call site, three accesses
        records = [r for r in logs.output if "socket.closed" in r]
        self.assertEqual(len(records), 1)
        self.assertIn("Deprecated websockets API", records[0])
        self.assertIn(__file__, records[0])  # points at the offending call site


if __name__ == "__main__":
    unittest.main()
