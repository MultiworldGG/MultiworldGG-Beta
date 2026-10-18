import os
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

import FileUtils


def _done(returncode: int = 0, stdout: str = "", stderr: str = "") -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess([], returncode, stdout, stderr)


class TestMacFileDialogs(unittest.TestCase):
    """The osascript dialogs run in osascript itself, take user strings as argv and never time out."""

    def setUp(self):
        self.utils = FileUtils.MacFileUtils()
        self.folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.folder, ignore_errors=True)

    def _run(self, result: subprocess.CompletedProcess):
        patcher = mock.patch.object(FileUtils.subprocess, "run", return_value=result)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def _script_and_argv(self, run: mock.Mock) -> tuple[str, list[str]]:
        run.assert_called_once()
        command = run.call_args.args[0]
        self.assertEqual(command[:2], ["osascript", "-e"])
        self.assertNotIn("timeout", run.call_args.kwargs)
        script = command[2]
        self.assertNotIn("System Events", script)
        self.assertTrue(script.startswith("on run argv\nactivate\n"))
        return script, command[3:]

    def test_open_file_passes_title_as_argv(self):
        title = 'Select the YAML for "me"'
        run = self._run(_done(stdout="/Users/me/me.yaml\n"))
        self.assertEqual(self.utils.open_file_input_dialog(title, [("YAML", [".yaml"])]), "/Users/me/me.yaml")
        script, argv = self._script_and_argv(run)
        self.assertIn("choose file with prompt (item 1 of argv)", script)
        self.assertNotIn("default location", script)
        self.assertNotIn(title, script)
        self.assertEqual(argv, [title])

    def test_open_file_starts_in_an_existing_suggested_folder(self):
        run = self._run(_done(stdout="/Users/me/me.yaml\n"))
        self.utils.open_file_input_dialog("Pick", [("YAML", [".yaml"])], suggest=os.path.join(self.folder, ""))
        script, argv = self._script_and_argv(run)
        self.assertIn("default location (POSIX file (item 2 of argv))", script)
        self.assertEqual(argv, ["Pick", os.path.join(self.folder, "")])

    def test_open_file_ignores_a_missing_suggested_folder(self):
        run = self._run(_done(stdout="/Users/me/me.yaml\n"))
        self.utils.open_file_input_dialog("Pick", [("YAML", [".yaml"])], suggest=os.path.join(self.folder, "a", "b"))
        script, argv = self._script_and_argv(run)
        self.assertNotIn("default location", script)
        self.assertEqual(argv, ["Pick"])

    def test_open_multiple_files_keeps_commas_in_names(self):
        run = self._run(_done(stdout="/Users/me/a, b.yaml\n/Users/me/c.yaml\n"))
        picked = self.utils.open_file_input_dialog("Pick", [("YAML", [".yaml"])], multiple=True)
        self.assertEqual(picked, ["/Users/me/a, b.yaml", "/Users/me/c.yaml"])
        script, _ = self._script_and_argv(run)
        self.assertIn("with multiple selections allowed", script)

    def test_cancel_returns_none_without_fallback(self):
        self._run(_done(1, stderr="0:42: execution error: User canceled. (-128)\n"))
        with mock.patch.object(FileUtils.MacFileUtils, "_fallback_file") as fallback:
            self.assertIsNone(self.utils.open_file_input_dialog("Pick", [("YAML", [".yaml"])]))
        fallback.assert_not_called()

    def test_osascript_failure_falls_back(self):
        self._run(_done(1, stderr="execution error: Not authorized to send Apple events. (-1743)\n"))
        with mock.patch.object(FileUtils.MacFileUtils, "_fallback_file", return_value="/x.yaml") as fallback:
            self.assertEqual(self.utils.open_file_input_dialog("Pick", [("YAML", [".yaml"])]), "/x.yaml")
        fallback.assert_called_once_with("Pick", [("YAML", [".yaml"])], "", False)

    def test_open_directory(self):
        run = self._run(_done(stdout="/Users/me/Players/\n"))
        self.assertEqual(self.utils.open_directory("Folder", suggest=self.folder), "/Users/me/Players/")
        script, argv = self._script_and_argv(run)
        self.assertIn("choose folder with prompt (item 1 of argv) "
                      "default location (POSIX file (item 2 of argv))", script)
        self.assertEqual(argv, ["Folder", self.folder])

    def test_save_splits_suggest_into_name_and_folder(self):
        run = self._run(_done(stdout="/Users/me/out.zip\n"))
        suggest = os.path.join(self.folder, "out.zip")
        self.assertEqual(self.utils.save_file_input_dialog("Save", [("Zip", [".zip"])], suggest), "/Users/me/out.zip")
        script, argv = self._script_and_argv(run)
        self.assertIn("choose file name with prompt (item 1 of argv) default name (item 2 of argv) "
                      "default location (POSIX file (item 3 of argv))", script)
        self.assertEqual(argv, ["Save", "out.zip", self.folder])


if __name__ == "__main__":
    unittest.main()
