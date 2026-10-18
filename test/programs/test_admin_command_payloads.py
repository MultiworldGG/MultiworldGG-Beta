"""Tests for the structured payloads MultiServer attaches to remote-admin replies.

The row and option builders take a context but only read plain attributes, so a
SimpleNamespace stub drives them without a live Context (which would load worlds).
"""

import collections
import contextlib
import datetime
import io
import re
import types
import unittest

from MultiServer import (
    Context,
    ServerCommandProcessor,
    build_options_payload,
    build_player_rows,
    format_players_table,
)
from NetUtils import ClientStatus, NetworkSlot, SlotType

GAME = "TestGame"
ACTIVITY = datetime.datetime(2026, 9, 3, 12, 0, tzinfo=datetime.timezone.utc)


def _client(*tags: str) -> types.SimpleNamespace:
    return types.SimpleNamespace(tags=list(tags))


def stub_context(**overrides) -> types.SimpleNamespace:
    ctx = types.SimpleNamespace(
        simple_options=Context.simple_options,
        option_choices=Context.option_choices,
        secret_options=Context.secret_options,
        slot_info={
            1: NetworkSlot("PlayerOne", GAME, SlotType.player),
            2: NetworkSlot("PlayerTwo", GAME, SlotType.player),
            3: NetworkSlot("Watcher", "", SlotType.spectator),
            4: NetworkSlot("Both", GAME, SlotType.group, (1, 2)),
        },
        player_names={(0, 1): "PlayerOne", (0, 2): "PlayerTwo", (0, 3): "Watcher", (0, 4): "Both"},
        name_aliases={(0, 2): "Two"},
        clients={0: {1: [_client("AP", "DeathLink"), _client("AP")], 2: []}},
        locations={1: {10: (100, 1, 0), 11: (101, 2, 0)}, 2: {20: (102, 1, 0)}},
        location_checks=collections.defaultdict(set, {(0, 1): {10}}),
        client_game_state=collections.defaultdict(int, {(0, 1): ClientStatus.CLIENT_PLAYING}),
        client_activity_timers={(0, 1): ACTIVITY},
        hint_cost=10, location_check_points=1, admin_password="hunter2", password=None,
        release_mode="auto", remaining_mode="goal", collect_mode="auto", release_threshold=0,
        countdown_mode="auto", hint_mode="default", item_cheat=True, compatibility=2,
        broadcast_all=lambda msgs: None,
    )
    for key, value in overrides.items():
        setattr(ctx, key, value)
    return ctx


def _cells(line: str) -> list[str]:
    return re.split(r" {2,}", line.strip())


class TestBuildPlayerRows(unittest.TestCase):
    def test_rows_skip_non_player_slots_and_carry_state(self) -> None:
        rows = build_player_rows(stub_context())
        self.assertEqual(rows, [
            {"team": 0, "slot": 1, "name": "PlayerOne", "alias": "", "game": GAME, "connected": True,
             "status": 20, "checks": 1, "total": 2, "last_activity": ACTIVITY.timestamp(),
             "tags": ["AP", "DeathLink"]},
            {"team": 0, "slot": 2, "name": "PlayerTwo", "alias": "Two", "game": GAME, "connected": False,
             "status": 0, "checks": 0, "total": 1, "last_activity": None, "tags": []},
        ])

    def test_rows_sorted_by_team_then_slot(self) -> None:
        ctx = stub_context()
        ctx.player_names = dict(reversed(list(ctx.player_names.items())))
        self.assertEqual([row["slot"] for row in build_player_rows(ctx)], [1, 2])

    def test_rows_do_not_insert_defaultdict_keys(self) -> None:
        ctx = stub_context()
        build_player_rows(ctx)
        self.assertNotIn((0, 2), ctx.client_game_state)
        self.assertNotIn((0, 2), ctx.location_checks)


class TestFormatPlayersTable(unittest.TestCase):
    def test_table_columns(self) -> None:
        now = (ACTIVITY + datetime.timedelta(minutes=5, seconds=30)).timestamp()
        rows = build_player_rows(stub_context())
        lines = format_players_table(rows, now=now).splitlines()
        self.assertEqual([_cells(line) for line in lines], [
            ["name", "game", "status", "checks", "%", "last activity", "connected"],
            ["PlayerOne", GAME, "playing", "1/2", "50.0", "0:05:30 ago", "yes"],
            ["Two (PlayerTwo)", GAME, "unknown", "0/1", "0.0", "never", "no"],
        ])

    def test_empty_rows_still_render_header(self) -> None:
        self.assertEqual(_cells(format_players_table([])),
                         ["name", "game", "status", "checks", "%", "last activity", "connected"])


class TestBuildOptionsPayload(unittest.TestCase):
    def test_entries_follow_simple_options_order_and_types(self) -> None:
        entries = build_options_payload(stub_context())
        self.assertEqual([entry["name"] for entry in entries], list(Context.simple_options))
        self.assertEqual({entry["name"]: entry["type"] for entry in entries},
                         {name: value_type.__name__ for name, value_type in Context.simple_options.items()})

    def test_passwords_masked_and_flagged_secret(self) -> None:
        by_name = {entry["name"]: entry for entry in build_options_payload(stub_context())}
        self.assertEqual(by_name["admin_password"],
                         {"name": "admin_password", "type": "str", "value": "********", "secret": True})
        self.assertEqual(by_name["password"], {"name": "password", "type": "str", "value": "", "secret": True})
        self.assertEqual(by_name["hint_cost"], {"name": "hint_cost", "type": "int", "value": 10})
        self.assertEqual(by_name["item_cheat"], {"name": "item_cheat", "type": "bool", "value": True})

    def test_choices_only_on_constrained_str_options(self) -> None:
        by_name = {entry["name"]: entry for entry in build_options_payload(stub_context())}
        self.assertEqual(by_name["release_mode"]["choices"], ["goal", "enabled", "disabled", "auto", "auto_enabled"])
        self.assertEqual(by_name["collect_mode"]["choices"], ["goal", "enabled", "disabled", "auto", "auto_enabled"])
        self.assertEqual(by_name["remaining_mode"]["choices"], ["goal", "enabled", "disabled"])
        self.assertEqual(by_name["countdown_mode"]["choices"], ["enabled", "disabled", "auto"])
        self.assertEqual(by_name["hint_mode"]["choices"], ["default", "own", "all"])
        for name in ("hint_cost", "location_check_points", "admin_password", "password", "release_threshold",
                     "item_cheat", "compatibility"):
            self.assertNotIn("choices", by_name[name], name)


class _CapturingProcessor(ServerCommandProcessor):
    def __init__(self, ctx) -> None:
        super().__init__(ctx)
        self.replies: list[tuple[str, dict]] = []

    def output(self, text: str, **extra) -> None:
        self.replies.append((text, extra))


class TestServerCommandProcessorPayloads(unittest.TestCase):
    def test_players_attaches_rows(self) -> None:
        proc = _CapturingProcessor(stub_context())
        self.assertTrue(proc._cmd_players())
        (text, extra), = proc.replies
        self.assertEqual(extra, {"players": build_player_rows(proc.ctx)})
        self.assertTrue(text.startswith("name"))

    def test_options_keeps_the_classic_lines_and_attaches_entries_to_the_header(self) -> None:
        proc = _CapturingProcessor(stub_context())
        self.assertTrue(proc._cmd_options())
        (header, extra), *lines = proc.replies
        self.assertEqual(header, "Current options:")
        self.assertEqual(extra, {"options": build_options_payload(proc.ctx)})
        self.assertEqual([text for text, _ in lines],
                         [f"Option {name} is set to {getattr(proc.ctx, name)}"
                          for name in Context.simple_options])
        self.assertTrue(all(line_extra == {} for _, line_extra in lines))

    def test_status_attaches_team_and_tag_per_reply(self) -> None:
        proc = _CapturingProcessor(stub_context())
        with unittest.mock.patch("MultiServer.get_status_string",
                                 lambda ctx, team, tag: f"Player Status on team {team}:"):
            self.assertTrue(proc._cmd_status("DeathLink"))
        self.assertEqual(proc.replies, [
            (f"Player Status on team {team}:", {"status": {"team": team, "tag": "DeathLink"}})
            for team in proc.ctx.clients])

    def test_option_success_attaches_refreshed_entries(self) -> None:
        proc = _CapturingProcessor(stub_context())
        self.assertTrue(proc._cmd_option("hint_mode", "own"))
        (text, extra), = proc.replies
        self.assertEqual(text, "Set option hint_mode to own")
        entry = next(entry for entry in extra["options"] if entry["name"] == "hint_mode")
        self.assertEqual(entry["value"], "own")
        self.assertEqual(proc.ctx.hint_mode, "own")

    def test_option_rejection_has_no_payload(self) -> None:
        proc = _CapturingProcessor(stub_context())
        self.assertFalse(proc._cmd_option("remaining_mode", "auto"))
        (text, extra), = proc.replies
        self.assertEqual(extra, {})
        self.assertEqual(text, "Unrecognized remaining_mode value 'auto', known: goal, enabled, disabled")
        self.assertEqual(proc.ctx.remaining_mode, "goal")

    def test_output_routes_extra_keys_into_admin_result(self) -> None:
        ctx = stub_context()
        notices = []
        ctx.notify_client = lambda client, text, extra: notices.append((client, text, extra))
        proc = ServerCommandProcessor(ctx)
        proc.client = object()
        with contextlib.redirect_stdout(io.StringIO()):
            proc.output("hi", players=[])
        self.assertEqual(notices, [(proc.client, "hi", {"type": "AdminCommandResult", "players": []})])

    def test_output_without_remote_admin_only_prints(self) -> None:
        ctx = stub_context()
        ctx.notify_client = lambda *args: self.fail("no remote admin is logged in")
        proc = ServerCommandProcessor(ctx)
        with contextlib.redirect_stdout(io.StringIO()) as console:
            proc.output("hi", players=[])
        self.assertEqual(console.getvalue(), "hi\n")
