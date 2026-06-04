import builtins
import unittest

from BaseUtils import Version, tuplize_version


class TestTuplizeVersionPrerelease(unittest.TestCase):
    def test_tuplize_version_strips_prerelease_suffix_to_release_tuple(self) -> None:
        self.assertEqual(tuplize_version("0.8.0b7"), Version(0, 8, 0))
        self.assertNotEqual(tuplize_version("0.8.0b7"), Version(0, 0, 0))

    def test_tuplize_version_fallback_strips_prerelease_when_packaging_missing(self) -> None:
        real_import = builtins.__import__

        def blocking_import(name, *args, **kwargs):
            if name == "packaging" or name.startswith("packaging."):
                raise ImportError("packaging blocked for fallback test")
            return real_import(name, *args, **kwargs)

        builtins.__import__ = blocking_import
        try:
            self.assertEqual(tuplize_version("0.8.0b7"), Version(0, 8, 0))
            self.assertEqual(tuplize_version("1.2b3"), Version(1, 2, 0))
            self.assertEqual(tuplize_version("5rc1"), Version(5, 0, 0))
        finally:
            builtins.__import__ = real_import
