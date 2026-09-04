"""Tests for MultiServer command dispatch.

Covers MultiServer.process_client_cmd (the network packet dispatcher),
CommonCommandProcessor / ClientMessageProcessor permission gating, and a
couple of ServerCommandProcessor argument-parsing paths.

These run process_client_cmd directly with a hand-built Context and a fake
Client whose async send/broadcast methods are captured (no real sockets),
so assertions are made on real captured packets and real Context state
changes rather than on "did not raise".
"""

import asyncio
import collections
import unittest
import weakref

import MultiServer
from MultiServer import Context, Client, ServerCommandProcessor
from NetUtils import LocationStore, NetworkSlot, SlotType, ClientStatus
from Utils import Version

GAME = "TestGame"


class FakeSocket:
    """Minimal stand-in so on_client_joined's protocol.extensions access works."""
    class _Protocol:
        extensions = ()

    state = None  # never State.OPEN, so the unstubbed broadcast paths no-op

    def __init__(self) -> None:
        self.protocol = FakeSocket._Protocol()


# A Context's constructor mutates the shared, process-global
# `worlds.network_data_package` (it deletes the *_name_groups keys in place),
# so it can only be built once per process. We build a single base Context and
# reset the per-test mutable state in setUp instead of rebuilding it.
_base_ctx: Context | None = None


def _repair_data_package_groups() -> None:
    """Re-add the group keys Context.__init__ deletes from the shared package.

    Context._load_game_data does an in-place ``del`` of item_name_groups /
    location_name_groups on the process-global ``worlds.network_data_package``.
    A second Context construction (e.g. by another test file in the same
    process) would then KeyError. We restore the keys before and after our own
    construction so neither this file nor its neighbors is order-dependent.
    The values are unused after load (groups come from the world classes).
    """
    import worlds
    for game_package in worlds.network_data_package["games"].values():
        game_package.setdefault("item_name_groups", {})
        game_package.setdefault("location_name_groups", {})


def setUpModule() -> None:
    # Repair any damage a previously-run test file's Context left behind.
    _repair_data_package_groups()


def tearDownModule() -> None:
    # Leave the shared package healthy for any test file that runs after us.
    _repair_data_package_groups()


def _make_base_context() -> Context:
    _repair_data_package_groups()
    ctx = Context("", 0, "", "", location_check_points=1, hint_cost=0, item_cheat=True,
                  release_mode="disabled", collect_mode="disabled", compatibility=2)
    _repair_data_package_groups()

    # Register a synthetic game's name<->id tables via the real init path.
    ctx.gamespackage[GAME] = {
        "item_name_to_id": {"Sword": 100, "Shield": 101, "Bow": 102},
        "location_name_to_id": {"Chest A": 10, "Chest B": 11, "Chest C": 20},
    }
    ctx._init_game_data()

    ctx.games = {1: GAME, 2: GAME}
    ctx.slot_info = {
        1: NetworkSlot("PlayerOne", GAME, SlotType.player),
        2: NetworkSlot("PlayerTwo", GAME, SlotType.player),
    }
    ctx.player_names = {(0, 1): "PlayerOne", (0, 2): "PlayerTwo"}
    ctx.player_name_lookup = {"PlayerOne": (0, 1), "PlayerTwo": (0, 2)}
    ctx.connect_names = {"PlayerOne": (0, 1), "PlayerTwo": (0, 2)}
    ctx.minimum_client_versions = {1: Version(0, 1, 6), 2: Version(0, 1, 6)}
    ctx.locations = LocationStore({
        1: {10: (100, 1, 0), 11: (101, 2, 0)},
        2: {20: (102, 1, 0)},
    })

    # Capture everything the dispatcher tries to push to clients/broadcasts,
    # instead of touching real websockets.
    def fake_send_msgs_factory(c):
        async def fake_send_msgs(endpoint, msgs):
            c.captured.append(("send", list(msgs)))
            return True
        return fake_send_msgs

    ctx.send_msgs = fake_send_msgs_factory(ctx)
    ctx.broadcast = lambda endpoints, msgs: ctx.captured.append(("broadcast", list(msgs)))
    ctx.broadcast_all = lambda msgs: ctx.captured.append(("broadcast_all", list(msgs)))
    ctx.broadcast_team = lambda team, msgs: ctx.captured.append(("broadcast_team", list(msgs)))
    ctx.broadcast_text_all = lambda text, additional_arguments={}: \
        ctx.captured.append(("broadcast_text_all", text))
    return ctx


def build_context() -> Context:
    """Return the shared base Context with a freshly reset per-test state.

    Slot 1 has two locations:
      10 -> item 100 for player 1 (own item)
      11 -> item 101 for player 2 (sent to the other player)
    Slot 2 has one location:
      20 -> item 102 for player 1
    """
    global _base_ctx
    if _base_ctx is None:
        _base_ctx = _make_base_context()
    ctx = _base_ctx

    # Reset everything a test or the dispatcher may mutate.
    ctx.captured = []  # list of (kind, payload) tuples
    ctx.clients = {0: collections.defaultdict(list)}
    ctx.endpoints = []
    ctx.location_checks = collections.defaultdict(set)
    ctx.received_items = {}
    ctx.start_inventory = {}
    ctx.stored_data = {}
    ctx.stored_data_notification_clients = collections.defaultdict(weakref.WeakSet)
    ctx.client_game_state = collections.defaultdict(int)
    ctx.client_ids = {}
    ctx.client_activity_timers = {}
    ctx.client_connection_timers = {}
    ctx.hints = collections.defaultdict(set)
    ctx.hints_used = collections.defaultdict(int)
    ctx.allow_releases = {}
    ctx.allow_collecting_from = {}
    ctx.def_allow_collecting_from = {}
    ctx.groups = {}
    ctx.group_collected = {}
    ctx.goal_overrides = set()
    ctx.name_aliases = {}
    ctx.password = None
    ctx.release_mode = "disabled"
    ctx.collect_mode = "disabled"
    ctx.compatibility = 2
    return ctx


def make_client(ctx: Context, *, slot: int = 1, team: int = 0, auth: bool = True) -> Client:
    client = Client(FakeSocket(), ctx)
    client.auth = auth
    client.team = team
    client.slot = slot
    client.version = Version(0, 8, 4)
    client.tags = []
    if auth:
        ctx.clients[team][slot].append(client)
    return client


def sent_packets(ctx: Context):
    """All packet dicts the dispatcher sent directly to the acting client."""
    out = []
    for kind, payload in ctx.captured:
        if kind == "send":
            out.extend(payload)
    return out


def run_cmd(ctx: Context, client: Client, args: dict) -> None:
    asyncio.run(MultiServer.process_client_cmd(ctx, client, args))


def run_sync(func):
    """Run a synchronous callable inside a live event loop.

    Server-side command handlers (e.g. _cmd_release) fire off websocket sends
    via Utils.async_start -> asyncio.create_task, which requires a running
    loop. We provide one and then let scheduled fire-and-forget tasks finish.
    """
    async def runner():
        result = func()
        await asyncio.sleep(0)  # let any created tasks run once
        return result
    return asyncio.run(runner())


def connect_args(**overrides) -> dict:
    args = {
        "cmd": "Connect",
        "password": None,
        "name": "PlayerOne",
        "game": GAME,
        "version": (0, 8, 4),
        "tags": [],
        "items_handling": 0b001,
        "uuid": "uuid-1",
        "slot_data": False,
    }
    args.update(overrides)
    return args


class TestConnect(unittest.TestCase):
    def test_bad_password_refused(self) -> None:
        ctx = build_context()
        ctx.password = "secret"
        client = make_client(ctx, auth=False)
        run_cmd(ctx, client, connect_args(password="wrong"))

        packets = sent_packets(ctx)
        self.assertEqual(len(packets), 1)
        self.assertEqual(packets[0]["cmd"], "ConnectionRefused")
        self.assertIn("InvalidPassword", packets[0]["errors"])
        # refusal must not authenticate the client
        self.assertFalse(client.auth)

    def test_unknown_slot_refused(self) -> None:
        ctx = build_context()
        client = make_client(ctx, auth=False)
        run_cmd(ctx, client, connect_args(name="NoSuchPlayer"))

        packets = sent_packets(ctx)
        self.assertEqual(packets[0]["cmd"], "ConnectionRefused")
        self.assertIn("InvalidSlot", packets[0]["errors"])

    def test_bad_version_and_game_refused(self) -> None:
        ctx = build_context()
        client = make_client(ctx, auth=False)
        run_cmd(ctx, client, connect_args(version=(0, 1, 0), game="WrongGame"))

        packets = sent_packets(ctx)
        self.assertEqual(packets[0]["cmd"], "ConnectionRefused")
        errors = set(packets[0]["errors"])
        self.assertIn("IncompatibleVersion", errors)
        self.assertIn("InvalidGame", errors)

    def test_successful_connect(self) -> None:
        ctx = build_context()
        client = make_client(ctx, auth=False)
        run_cmd(ctx, client, connect_args())

        packets = sent_packets(ctx)
        cmds = [p["cmd"] for p in packets]
        self.assertIn("Connected", cmds)
        self.assertNotIn("ConnectionRefused", cmds)
        connected = next(p for p in packets if p["cmd"] == "Connected")
        self.assertEqual(connected["team"], 0)
        self.assertEqual(connected["slot"], 1)
        # both of slot 1's locations are still missing on a fresh connect
        self.assertEqual(sorted(connected["missing_locations"]), [10, 11])
        # dispatcher authenticated the client and registered it
        self.assertTrue(client.auth)
        self.assertIn(client, ctx.clients[0][1])


class TestLocationChecks(unittest.TestCase):
    def test_marks_locations_and_routes_items(self) -> None:
        ctx = build_context()
        sender = make_client(ctx, slot=1)
        # a separate authenticated client for the receiving player (slot 2)
        make_client(ctx, slot=2)

        run_cmd(ctx, sender, {"cmd": "LocationChecks", "locations": [10, 11]})

        # Real state: both locations now recorded as checked for (team 0, slot 1).
        self.assertEqual(ctx.location_checks[0, 1], {10, 11})

        # Location 10 holds slot 1's OWN item. send_items_to only enqueues an
        # own-world item into the remote-items queue, not the local one.
        self.assertEqual(MultiServer.get_received_items(ctx, 0, 1, False), [])
        own_remote = MultiServer.get_received_items(ctx, 0, 1, True)
        self.assertEqual([(i.item, i.location, i.player) for i in own_remote],
                         [(100, 10, 1)])

        # Location 11 holds slot 2's item -> routed to slot 2 in both queues.
        other_items = MultiServer.get_received_items(ctx, 0, 2, False)
        self.assertEqual([(i.item, i.location, i.player) for i in other_items],
                         [(101, 11, 1)])

    def test_tracker_cannot_check(self) -> None:
        ctx = build_context()
        client = make_client(ctx, slot=1)
        client.no_locations = True
        run_cmd(ctx, client, {"cmd": "LocationChecks", "locations": [10]})

        packets = sent_packets(ctx)
        self.assertEqual(packets[0]["cmd"], "InvalidPacket")
        # nothing should have been marked
        self.assertEqual(ctx.location_checks[0, 1], set())

    def test_register_location_checks_ignores_unknown_location_ids(self) -> None:
        ctx = build_context()
        make_client(ctx, slot=1)
        # slot 1 only knows locations 10 and 11; 999 is unknown to this multidata
        MultiServer.register_location_checks(ctx, 0, 1, [10, 999])

        # the unknown id is silently dropped; only the known check is recorded
        self.assertEqual(ctx.location_checks[0, 1], {10})

        # and the unknown id is not echoed back as a checked location
        room_updates = [payload[0] for kind, payload in ctx.captured
                        if kind == "broadcast" and payload and payload[0].get("cmd") == "RoomUpdate"]
        self.assertTrue(room_updates)
        self.assertEqual(set(room_updates[-1]["checked_locations"]), {10})


class TestSay(unittest.TestCase):
    def test_routes_text_to_message_processor(self) -> None:
        ctx = build_context()
        client = make_client(ctx, slot=1)
        calls = []
        client.messageprocessor = lambda text: calls.append(text)

        run_cmd(ctx, client, {"cmd": "Say", "text": "hello world"})
        self.assertEqual(calls, ["hello world"])

    def test_non_printable_rejected(self) -> None:
        ctx = build_context()
        client = make_client(ctx, slot=1)
        calls = []
        client.messageprocessor = lambda text: calls.append(text)

        run_cmd(ctx, client, {"cmd": "Say", "text": "bad\x00text"})
        self.assertEqual(calls, [])  # never reached the processor
        self.assertEqual(sent_packets(ctx)[0]["cmd"], "InvalidPacket")


class TestSetAndNotify(unittest.TestCase):
    def test_set_applies_operations_and_replies(self) -> None:
        ctx = build_context()
        client = make_client(ctx, slot=1)
        run_cmd(ctx, client, {
            "cmd": "Set", "key": "counter", "default": 0, "want_reply": True,
            "operations": [{"operation": "add", "value": 5},
                           {"operation": "mul", "value": 3}],
        })
        # (0 + 5) * 3 == 15 stored
        self.assertEqual(ctx.stored_data["counter"], 15)

        # want_reply -> a SetReply broadcast addressed to the acting client
        replies = [payload for kind, payload in ctx.captured if kind == "broadcast"]
        self.assertTrue(replies)
        reply = replies[-1][0]
        self.assertEqual(reply["cmd"], "SetReply")
        self.assertEqual(reply["key"], "counter")
        self.assertEqual(reply["value"], 15)
        self.assertEqual(reply["original_value"], 0)

    def test_set_rejects_read_key(self) -> None:
        ctx = build_context()
        client = make_client(ctx, slot=1)
        run_cmd(ctx, client, {
            "cmd": "Set", "key": "_read_hints_0_1",
            "operations": [{"operation": "replace", "value": 1}],
        })
        self.assertEqual(sent_packets(ctx)[0]["cmd"], "InvalidPacket")
        self.assertNotIn("_read_hints_0_1", ctx.stored_data)

    def test_set_notify_registers_then_set_broadcasts(self) -> None:
        ctx = build_context()
        watcher = make_client(ctx, slot=1)
        setter = make_client(ctx, slot=2)

        # watcher subscribes to "shared"
        run_cmd(ctx, watcher, {"cmd": "SetNotify", "keys": ["shared"]})
        self.assertIn(watcher, ctx.stored_data_notification_clients["shared"])

        # setter writes "shared" -> watcher must be a broadcast target
        ctx.captured.clear()
        run_cmd(ctx, setter, {
            "cmd": "Set", "key": "shared", "default": 0,
            "operations": [{"operation": "replace", "value": 42}],
        })
        self.assertEqual(ctx.stored_data["shared"], 42)
        broadcasts = [(kind, payload) for kind, payload in ctx.captured if kind == "broadcast"]
        self.assertTrue(broadcasts, "Set on a watched key should broadcast a SetReply")
        self.assertEqual(broadcasts[-1][1][0]["value"], 42)


class TestReleaseCollectPermissionGating(unittest.TestCase):
    def _release(self, ctx, client):
        return run_sync(client.messageprocessor._cmd_release)

    def _collect(self, ctx, client):
        return run_sync(client.messageprocessor._cmd_collect)

    def test_release_forbidden_when_disabled(self) -> None:
        ctx = build_context()
        ctx.release_mode = "disabled"
        client = make_client(ctx, slot=1)
        # populate item state so a successful release would be observable
        self.assertFalse(self._release(ctx, client))
        # nothing released -> slot 1's own locations not auto-checked
        self.assertEqual(ctx.location_checks[0, 1], set())

    def test_release_allowed_when_enabled(self) -> None:
        ctx = build_context()
        ctx.release_mode = "enabled"
        client = make_client(ctx, slot=1)
        self.assertTrue(self._release(ctx, client))
        # release_player registers ALL of slot 1's locations as checked
        self.assertEqual(ctx.location_checks[0, 1], {10, 11})

    def test_release_allowed_by_per_player_override(self) -> None:
        ctx = build_context()
        ctx.release_mode = "disabled"
        client = make_client(ctx, slot=1)
        ctx.allow_releases[(0, 1)] = True  # explicit per-player allow beats disabled
        self.assertTrue(self._release(ctx, client))
        self.assertEqual(ctx.location_checks[0, 1], {10, 11})

    def test_collect_forbidden_when_disabled(self) -> None:
        ctx = build_context()
        ctx.collect_mode = "disabled"
        client = make_client(ctx, slot=1)
        self.assertFalse(self._collect(ctx, client))

    def test_collect_allowed_when_enabled(self) -> None:
        ctx = build_context()
        ctx.collect_mode = "enabled"
        client = make_client(ctx, slot=1)
        self.assertTrue(self._collect(ctx, client))
        # collect pulls slot 1's items from every world that holds them:
        # location 10 (own world) and location 20 (slot 2's world).
        self.assertEqual(ctx.location_checks[0, 1], {10})
        self.assertEqual(ctx.location_checks[0, 2], {20})


class TestServerCommandProcessor(unittest.TestCase):
    def test_option_unknown_returns_false(self) -> None:
        ctx = build_context()
        proc = ServerCommandProcessor(ctx)
        out = []
        proc.output = lambda text: out.append(text)
        self.assertFalse(proc._cmd_option("not_a_real_option", "x"))
        self.assertTrue(any("Unrecognized option" in line for line in out))

    def test_option_invalid_mode_value_rejected(self) -> None:
        ctx = build_context()
        proc = ServerCommandProcessor(ctx)
        out = []
        proc.output = lambda text: out.append(text)
        # release_mode only accepts goal/enabled/disabled/auto/auto_enabled
        self.assertFalse(proc._cmd_option("release_mode", "banana"))
        self.assertEqual(ctx.release_mode, "disabled")  # unchanged

    def test_option_sets_valid_value(self) -> None:
        ctx = build_context()
        proc = ServerCommandProcessor(ctx)
        proc.output = lambda text, **extra: None
        self.assertTrue(proc._cmd_option("release_mode", "enabled"))
        self.assertEqual(ctx.release_mode, "enabled")

    def test_send_item_to_player(self) -> None:
        ctx = build_context()
        proc = ServerCommandProcessor(ctx)
        proc.output = lambda text: None
        # /send PlayerTwo Bow  -> item 102 lands in slot 2's received items
        self.assertTrue(run_sync(lambda: proc._cmd_send("PlayerTwo", "Bow")))
        items = MultiServer.get_received_items(ctx, 0, 2, False)
        self.assertEqual([(i.item, i.player) for i in items], [(102, 0)])

    def test_send_unknown_player_returns_false(self) -> None:
        ctx = build_context()
        proc = ServerCommandProcessor(ctx)
        out = []
        proc.output = lambda text: out.append(text)
        self.assertFalse(proc._cmd_send("Nobody", "Bow"))
        # no items routed to anyone
        self.assertEqual(MultiServer.get_received_items(ctx, 0, 1, False), [])
        self.assertEqual(MultiServer.get_received_items(ctx, 0, 2, False), [])


SLOT_PINS = {
    1: {"version": (1, 2, 3), "custom": False},
    2: {"version": (0, 5, 0), "custom": True},
}

# Everything Context._load reassigns; snapshotted around the _load tests so the
# shared base Context keeps the fixture slots/locations the other classes rely on.
_LOAD_CLOBBERED = (
    "read_data", "generator_version", "minimum_client_versions", "slot_info", "games",
    "groups", "clients", "def_allow_collecting_from", "seed_name", "connect_names",
    "locations", "slot_data", "er_hint_data", "spheres", "world_versions", "mwgg_index_tag",
    "player_names", "player_name_lookup",
)


class TestWorldVersionPinFlow(unittest.TestCase):
    """world_versions/mwgg_index_tag: multidata blob -> Context._load -> game-keyed RoomInfo."""

    @staticmethod
    def _minimal_multidata(with_pins: bool) -> dict:
        data = {
            "slot_info": {
                1: NetworkSlot("Player1", "Game A", SlotType.player),
                2: NetworkSlot("Player2", "Game B", SlotType.player),
            },
            "connect_names": {"Player1": (0, 1), "Player2": (0, 2)},
            "locations": {1: {}, 2: {}},
            "slot_data": {1: {}, 2: {}},
            "er_hint_data": {},
            "precollected_items": {1: [], 2: []},
            "precollected_hints": {1: set(), 2: set()},
            "version": (0, 6, 2),
            "minimum_versions": {"server": (0, 1, 6), "clients": {}},
            "seed_name": "TESTSEED",
            "spheres": [],
            "datapackage": {},
        }
        if with_pins:
            data["world_versions"] = {slot: dict(pin) for slot, pin in SLOT_PINS.items()}
            data["mwgg_index_tag"] = "sixteen-2026.06.10"
        return data

    def _load(self, ctx: Context, multidata: dict) -> None:
        missing = object()
        saved = {attr: getattr(ctx, attr, missing) for attr in _LOAD_CLOBBERED}
        saved["player_names"] = dict(ctx.player_names)
        saved["player_name_lookup"] = dict(ctx.player_name_lookup)
        try:
            ctx._load(multidata, {}, False)
            self.loaded_world_versions = ctx.world_versions
            self.loaded_mwgg_index_tag = ctx.mwgg_index_tag
        finally:
            for attr, value in saved.items():
                if value is missing:
                    delattr(ctx, attr)
                else:
                    setattr(ctx, attr, value)

    def test_pin_survives_multidata_blob(self) -> None:
        """world_versions must round-trip through the same path Main writes / MultiServer reads."""
        import zlib
        from Utils import restricted_dumps, restricted_loads
        blob = zlib.compress(restricted_dumps({"world_versions": SLOT_PINS}), 9)
        restored = restricted_loads(zlib.decompress(blob))
        self.assertEqual(restored["world_versions"], SLOT_PINS)

    def test_load_populates_world_versions(self) -> None:
        ctx = build_context()
        self._load(ctx, self._minimal_multidata(with_pins=True))
        self.assertEqual(self.loaded_world_versions, SLOT_PINS)
        self.assertEqual(self.loaded_mwgg_index_tag, "sixteen-2026.06.10")

    def test_load_tolerates_pre_feature_seed(self) -> None:
        ctx = build_context()
        self._load(ctx, self._minimal_multidata(with_pins=False))
        self.assertEqual(self.loaded_world_versions, {})
        self.assertIsNone(self.loaded_mwgg_index_tag)

    def test_roominfo_collapses_slots_to_game_keys(self) -> None:
        ctx = build_context()
        ctx.slot_info = {
            1: NetworkSlot("Player1", "Game A", SlotType.player),
            2: NetworkSlot("Player2", "Game B", SlotType.player),
        }
        ctx.world_versions = dict(SLOT_PINS)
        ctx.mwgg_index_tag = "sixteen-2026.06.10"
        try:
            client = make_client(ctx)
            asyncio.run(MultiServer.on_client_connected(ctx, client))
        finally:
            ctx.slot_info = _base_ctx_slot_info()
            ctx.world_versions = {}
            ctx.mwgg_index_tag = None

        room_info = sent_packets(ctx)[-1]
        self.assertEqual(room_info["cmd"], "RoomInfo")
        # game-keyed (the client cannot key by slot at RoomInfo time)
        self.assertEqual(
            room_info["world_versions"],
            {"Game A": {"version": (1, 2, 3), "custom": False},
             "Game B": {"version": (0, 5, 0), "custom": True}},
        )
        self.assertEqual(room_info["mwgg_index_tag"], "sixteen-2026.06.10")

    def test_roominfo_empty_pins_on_pre_feature_seed(self) -> None:
        ctx = build_context()
        ctx.world_versions = {}
        ctx.mwgg_index_tag = None
        client = make_client(ctx)
        asyncio.run(MultiServer.on_client_connected(ctx, client))
        room_info = sent_packets(ctx)[-1]
        self.assertEqual(room_info["world_versions"], {})
        self.assertIsNone(room_info["mwgg_index_tag"])


def _base_ctx_slot_info() -> dict:
    return {
        1: NetworkSlot("PlayerOne", GAME, SlotType.player),
        2: NetworkSlot("PlayerTwo", GAME, SlotType.player),
    }


if __name__ == "__main__":
    unittest.main()
