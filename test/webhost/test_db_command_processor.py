"""The room page's command processor must accept the remote-admin payload keywords
ServerCommandProcessor.output takes, or /players, /options, /status and /option
crash with a TypeError in the room log.
"""

import logging
import unittest
from unittest import mock

from WebHostLib.customserver import DBCommandProcessor
from test.programs.test_admin_command_payloads import stub_context


class TestDBCommandProcessorPayloads(unittest.TestCase):
    def setUp(self) -> None:
        self.logger = logging.getLogger("test-db-command-processor")
        self.proc = DBCommandProcessor(stub_context(logger=self.logger))

    def run_line(self, line: str) -> list[str]:
        with self.assertLogs(self.logger, level="INFO") as captured:
            self.assertTrue(self.proc(line), line)
        self.assertFalse(any("Traceback" in entry for entry in captured.output), captured.output)
        return captured.output

    def test_players_options_and_option_log_their_text(self) -> None:
        self.assertTrue(self.run_line("/players")[0].startswith("INFO:test-db-command-processor:name"))
        self.assertIn("INFO:test-db-command-processor:Current options:", self.run_line("/options"))
        self.assertEqual(self.run_line("/option hint_mode own"),
                         ["INFO:test-db-command-processor:Set option hint_mode to own"])
        self.assertEqual(self.proc.ctx.hint_mode, "own")

    def test_status_logs_one_line_per_team(self) -> None:
        with mock.patch("MultiServer.get_status_string", lambda ctx, team, tag: f"Player Status on team {team}:"):
            self.assertEqual(self.run_line("/status DeathLink"),
                             [f"INFO:test-db-command-processor:Player Status on team {team}:"
                              for team in self.proc.ctx.clients])
