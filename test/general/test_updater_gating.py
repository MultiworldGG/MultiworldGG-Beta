import os
import unittest
from unittest import mock

import Updater


def _platform(is_windows: bool = False, is_linux: bool = False, is_macos: bool = False):
    return mock.patch.multiple(
        Updater, is_windows=is_windows, is_linux=is_linux, is_macos=is_macos
    )


class TestCanCheckForUpdates(unittest.TestCase):
    def test_source_checkout_never_checks(self) -> None:
        with mock.patch("Updater.is_frozen", return_value=False):
            for platform_kwargs in (
                {"is_windows": True},
                {"is_linux": True},
                {"is_macos": True},
            ):
                with _platform(**platform_kwargs):
                    self.assertFalse(Updater.can_check_for_updates())

    def test_frozen_windows_always_checks(self) -> None:
        with mock.patch("Updater.is_frozen", return_value=True), \
                _platform(is_windows=True):
            self.assertTrue(Updater.can_check_for_updates())

    def test_frozen_linux_requires_appimage_env(self) -> None:
        with mock.patch("Updater.is_frozen", return_value=True), \
                _platform(is_linux=True):
            with mock.patch.dict(os.environ, {}, clear=True):
                self.assertFalse(Updater.can_check_for_updates())
            with mock.patch.dict(os.environ, {"APPIMAGE": "/opt/MultiworldGG.AppImage"}):
                self.assertTrue(Updater.can_check_for_updates())

    def test_frozen_macos_requires_app_bundle_path(self) -> None:
        with mock.patch("Updater.is_frozen", return_value=True), \
                _platform(is_macos=True):
            bundle_exe = "/Applications/MultiworldGG.app/Contents/MacOS/MultiworldGG"
            with mock.patch("os.path.realpath", return_value=bundle_exe):
                self.assertTrue(Updater.can_check_for_updates())
            with mock.patch("os.path.realpath", return_value="/usr/local/bin/MultiworldGG"):
                self.assertFalse(Updater.can_check_for_updates())

    def test_unknown_platform_never_checks(self) -> None:
        with mock.patch("Updater.is_frozen", return_value=True), _platform():
            self.assertFalse(Updater.can_check_for_updates())


class TestReleasePageUrl(unittest.TestCase):
    def test_release_page_url_points_at_latest_release(self) -> None:
        url = Updater.get_release_page_url()
        self.assertEqual(
            url,
            f"https://github.com/{Updater.GITHUB_OWNER}/{Updater.GITHUB_REPO}/releases/latest",
        )
