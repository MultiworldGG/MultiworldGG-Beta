import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import Updater
import Utils


class _Response:
    def __init__(self, json_data=None, text="", headers=None):
        self._json_data = json_data
        self.text = text
        self.headers = headers or {}

    def json(self):
        return self._json_data

    def raise_for_status(self):
        return None


def _release(tag, assets, *, prerelease=False, draft=False, body="Release notes"):
    return {
        "tag_name": tag,
        "prerelease": prerelease,
        "draft": draft,
        "body": body,
        "assets": [
            {"name": name, "browser_download_url": f"https://example.invalid/{name}", "size": 1234}
            for name in assets
        ],
    }


# GitHub mangles spaces in asset names to dots; inno_setup.iss emits dotted names directly.
WIN_INSTALLER = "Setup.MultiworldGG-Test.0.9.0b2.exe"
APP_ASSETS = [
    "MultiworldGG-0.9.0b2-linux-x86_64.tar.gz",
    "MultiworldGG-Test-0.9.0b2-x86_64.AppImage",
    "multiworldgg_test-0.9.0b2.dmg",
    WIN_INSTALLER,
]
WHEEL_ASSETS = ["worlds_oot-9.1.0-py3-none-any.whl", "worlds_alttp-5.1.0-py3-none-any.whl"]


class TestUpdaterAssetSelection(unittest.TestCase):
    assets = [
        {"name": "multiworldgg_test-0.9.0b2.dmg", "browser_download_url": "https://example.invalid/mac"},
        {"name": "MultiworldGG-Test-0.9.0b2-x86_64.AppImage", "browser_download_url": "https://example.invalid/linux"},
        {"name": WIN_INSTALLER, "browser_download_url": "https://example.invalid/win"},
    ]

    def test_selects_windows_installer(self):
        asset = Updater.select_installer_asset(self.assets, "windows")
        self.assertEqual(asset["name"], WIN_INSTALLER)

    def test_selects_linux_appimage(self):
        asset = Updater.select_installer_asset(self.assets, "linux")
        self.assertEqual(asset["name"], "MultiworldGG-Test-0.9.0b2-x86_64.AppImage")

    def test_selects_macos_dmg(self):
        asset = Updater.select_installer_asset(self.assets, "macos")
        self.assertEqual(asset["name"], "multiworldgg_test-0.9.0b2.dmg")

    def test_prefers_setup_named_installer_over_other_exe(self):
        assets = [
            {"name": "MultiworldGGPortable.exe", "browser_download_url": "https://example.invalid/portable"},
            {"name": WIN_INSTALLER, "browser_download_url": "https://example.invalid/win"},
        ]
        self.assertEqual(Updater.select_installer_asset(assets, "windows")["name"], WIN_INSTALLER)

    def test_channel_matches_distinguishes_test_and_stable(self):
        with patch.object(Utils, "instance_name", "MultiworldGG-Test"):
            self.assertTrue(Updater._channel_matches("Setup.MultiworldGG-Test.0.9.0b2.exe"))
            self.assertTrue(Updater._channel_matches("multiworldgg_test-0.9.0b2.dmg"))
            self.assertTrue(Updater._channel_matches("MultiworldGG-Test-0.9.0b2-x86_64.AppImage"))
            self.assertFalse(Updater._channel_matches("Setup.MultiworldGG.0.9.1.exe"))
        with patch.object(Utils, "instance_name", "MultiworldGG"):
            self.assertTrue(Updater._channel_matches("Setup.MultiworldGG.0.9.1.exe"))
            self.assertFalse(Updater._channel_matches("Setup.MultiworldGG-Test.0.9.0b2.exe"))
            self.assertFalse(Updater._channel_matches("MultiworldGG-Test-0.9.0b2-x86_64.AppImage"))


class TestUpdaterReleaseSelection(unittest.TestCase):
    def _find(self, releases, platform_key="windows", instance_name="MultiworldGG-Test"):
        with patch.object(Utils, "instance_name", instance_name), \
                patch("requests.get", return_value=_Response(json_data=releases)):
            return Updater.find_update_release(platform_key)

    def test_skips_worlds_wheels_release_without_installer(self):
        releases = [
            _release("worlds-wheels-2026-08-24", WHEEL_ASSETS),
            _release("0.9.0b2", APP_ASSETS),
        ]
        release, installer = self._find(releases)
        self.assertEqual(release["tag_name"], "0.9.0b2")
        self.assertEqual(installer["name"], WIN_INSTALLER)

    def test_skips_prerelease_release(self):
        releases = [
            _release("0.9.1", ["Setup.MultiworldGG-Test.0.9.1.exe"], prerelease=True),
            _release("0.9.0b2", APP_ASSETS),
        ]
        release, _ = self._find(releases)
        self.assertEqual(release["tag_name"], "0.9.0b2")

    def test_no_release_when_only_prereleases_have_installers(self):
        releases = [
            _release("worlds-wheels-2026-08-24", WHEEL_ASSETS),
            _release("0.9.0b2", APP_ASSETS, prerelease=True),
        ]
        with self.assertRaises(RuntimeError):
            self._find(releases)

    def test_skips_draft_release(self):
        releases = [
            _release("0.9.1", ["Setup.MultiworldGG-Test.0.9.1.exe"], draft=True),
            _release("0.9.0b2", APP_ASSETS),
        ]
        release, _ = self._find(releases)
        self.assertEqual(release["tag_name"], "0.9.0b2")

    def test_newest_version_wins_regardless_of_list_order(self):
        releases = [
            _release("0.9.0b1", ["Setup.MultiworldGG-Test.0.9.0b1.exe"]),
            _release("0.9.0b2", APP_ASSETS),
            _release("0.8.4b12", ["Setup.MultiworldGG-Test.0.8.4b12.exe"]),
        ]
        release, _ = self._find(releases)
        self.assertEqual(release["tag_name"], "0.9.0b2")

    def test_release_without_platform_installer_is_skipped(self):
        releases = [
            _release("0.9.0b3", ["multiworldgg_test-0.9.0b3.dmg"]),
            _release("0.9.0b2", APP_ASSETS),
        ]
        release, _ = self._find(releases)
        self.assertEqual(release["tag_name"], "0.9.0b2")

    def test_prefers_own_channel_over_newer_foreign_channel(self):
        releases = [
            _release("0.9.1", ["Setup.MultiworldGG.0.9.1.exe"]),
            _release("0.9.0b2", APP_ASSETS),
        ]
        release, installer = self._find(releases)
        self.assertEqual(release["tag_name"], "0.9.0b2")
        self.assertEqual(installer["name"], WIN_INSTALLER)

    def test_falls_back_to_any_installer_when_channel_never_matches(self):
        releases = [_release("0.9.0b2", APP_ASSETS)]
        release, installer = self._find(releases, instance_name="Rebranded App")
        self.assertEqual(release["tag_name"], "0.9.0b2")
        self.assertEqual(installer["name"], WIN_INSTALLER)

    def test_raises_when_no_release_has_installer(self):
        releases = [_release("worlds-wheels-2026-08-24", WHEEL_ASSETS)]
        with self.assertRaisesRegex(RuntimeError, "No feasible installer"):
            self._find(releases)


class TestUpdaterReleaseInfo(unittest.TestCase):
    def test_get_latest_release_info_includes_asset_metadata_and_checksum(self):
        releases = [
            _release("worlds-wheels-2026-08-24", WHEEL_ASSETS),
            _release("0.9.0b2", APP_ASSETS + ["MultiworldGG-Test-0.9.0b2-x86_64.AppImage.sha256"]),
        ]
        checksum = "a" * 64

        # Updater imports requests at function level, so patch the real module.
        with patch.object(Updater, "_platform_key", return_value="linux"), \
                patch.object(Utils, "instance_name", "MultiworldGG-Test"), \
                patch("requests.get", side_effect=[
                    _Response(json_data=releases),
                    _Response(text=f"{checksum}  MultiworldGG-Test-0.9.0b2-x86_64.AppImage\n"),
                ]):
            release = Updater.get_latest_release_info()

        self.assertEqual(release.version.as_simple_string(), "0.9.0")
        self.assertEqual(release.version.tag, "0.9.0b2")
        self.assertEqual(release.asset.name, "MultiworldGG-Test-0.9.0b2-x86_64.AppImage")
        self.assertEqual(release.asset.size, 1234)
        self.assertEqual(release.asset.checksum, checksum)
        self.assertEqual(release.changelog, "Release notes")

    def test_release_info_unpacks_as_gui_triple(self):
        release = Updater.ReleaseInfo(
            version=Updater.ReleaseVersion("0.9.0b2"),
            asset=Updater.UpdateAsset(WIN_INSTALLER, "https://example.invalid/win"),
            changelog="Release notes",
        )
        version, download_url, changelog = release
        self.assertEqual(version, (0, 9, 0))
        self.assertEqual(download_url, "https://example.invalid/win")
        self.assertEqual(changelog, "Release notes")

    def test_checksum_verification_rejects_bad_hash(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"not the expected payload")
            path = Path(f.name)
        self.addCleanup(path.unlink, missing_ok=True)

        with self.assertRaisesRegex(RuntimeError, "checksum"):
            Updater._verify_checksum(path, "0" * 64)

    def test_checksum_manifest_matches_dotted_installer_name(self):
        checksum = "b" * 64
        manifest = f"{checksum}  {WIN_INSTALLER}\n"

        self.assertEqual(Updater._parse_checksum_manifest(manifest, WIN_INSTALLER), checksum)

    def test_install_rejects_non_newer_release_info(self):
        release = Updater.ReleaseInfo(
            version=Utils.version_tuple,
            asset=Updater.UpdateAsset("MultiworldGG.AppImage", "https://example.invalid/appimage"),
            changelog="",
        )

        with self.assertRaisesRegex(RuntimeError, "not newer"):
            Updater.download_and_install_update(release)

    def test_appimage_helper_template_renders_script(self):
        script = Updater._render_helper_template(
            "appimage_update.sh.template",
            parent_pid=123,
            backup_path="'/tmp/current.AppImage.old'",
            current_path="'/tmp/current.AppImage'",
            download_path="'/tmp/new.AppImage.download'",
        )

        self.assertIn("while kill -0 123", script)
        self.assertIn("mv '/tmp/new.AppImage.download' '/tmp/current.AppImage'", script)

    def test_macos_helper_template_renders_script(self):
        script = Updater._render_helper_template(
            "macos_update.sh.template",
            parent_pid=456,
            app_path="'/Applications/MultiworldGG.app'",
            source_app="'/Volumes/MultiworldGG/MultiworldGG.app'",
            stage_app="'/Applications/MultiworldGG.app.update'",
            volume="'/Volumes/MultiworldGG'",
            dmg_path="'/tmp/MultiworldGG.dmg'",
            admin_script="'do shell script'",
        )

        self.assertIn("while kill -0 456", script)
        self.assertIn("osascript -e 'do shell script'", script)


class TestReleaseVersionComparison(unittest.TestCase):
    """tuplize_version drops PEP 440 pre-release suffixes; ReleaseVersion must
    still order same-release-tuple versions against the running build."""

    def _running(self, version_string):
        return patch.multiple(
            Utils,
            __version__=version_string,
            version_tuple=Utils.tuplize_version(version_string),
        )

    def test_later_beta_is_newer_than_running_beta(self):
        with self._running("0.9.0b2"):
            self.assertGreater(Updater.ReleaseVersion("0.9.0b5"), Utils.version_tuple)
            self.assertFalse(Updater.ReleaseVersion("0.9.0b5") <= Utils.version_tuple)

    def test_same_beta_is_not_newer(self):
        with self._running("0.9.0b2"):
            self.assertLessEqual(Updater.ReleaseVersion("0.9.0b2"), Utils.version_tuple)

    def test_earlier_beta_is_not_newer(self):
        with self._running("0.9.0b2"):
            self.assertLessEqual(Updater.ReleaseVersion("0.9.0b1"), Utils.version_tuple)

    def test_final_release_is_newer_than_running_beta(self):
        with self._running("0.9.0b2"):
            self.assertGreater(Updater.ReleaseVersion("0.9.0"), Utils.version_tuple)

    def test_beta_is_not_newer_than_running_final(self):
        with self._running("0.9.0"):
            self.assertLessEqual(Updater.ReleaseVersion("0.9.0b5"), Utils.version_tuple)

    def test_plain_tuple_ordering_still_applies(self):
        with self._running("0.9.0b2"):
            self.assertGreater(Updater.ReleaseVersion("0.9.1"), Utils.version_tuple)
            self.assertLessEqual(Updater.ReleaseVersion("0.8.4b12"), Utils.version_tuple)

    def test_install_accepts_newer_beta_of_same_release_tuple(self):
        release = Updater.ReleaseInfo(
            version=Updater.ReleaseVersion("0.9.0b5"),
            asset=Updater.UpdateAsset(WIN_INSTALLER, "https://example.invalid/win"),
            changelog="",
        )
        with self._running("0.9.0b2"), \
                patch.object(Utils, "is_windows", True), \
                patch.object(Updater, "_download_and_install_win") as install:
            Updater.download_and_install_update(release)
        install.assert_called_once()

    def test_install_rejects_older_beta_of_same_release_tuple(self):
        release = Updater.ReleaseInfo(
            version=Updater.ReleaseVersion("0.9.0b1"),
            asset=Updater.UpdateAsset(WIN_INSTALLER, "https://example.invalid/win"),
            changelog="",
        )
        with self._running("0.9.0b2"):
            with self.assertRaisesRegex(RuntimeError, "not newer"):
                Updater.download_and_install_update(release)


if __name__ == "__main__":
    unittest.main()
