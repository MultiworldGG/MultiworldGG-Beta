# Tests that yaml wrappers in Utils.py do what they should

import unittest
from typing import cast, Any, ClassVar, Dict

from Utils import dump, Dumper  # type: ignore[attr-defined]
from Utils import parse_yaml, parse_yamls, unsafe_parse_yaml


class AClass:
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__)


class TestYaml(unittest.TestCase):
    safe_data: ClassVar[Dict[str, Any]] = {
        "a": [1, 2, 3],
        "b": None,
        "c": True,
    }
    unsafe_data: ClassVar[Dict[str, Any]] = {
        "a": AClass()
    }

    @property
    def safe_str(self) -> str:
        return cast(str, dump(self.safe_data, Dumper=Dumper))

    @property
    def unsafe_str(self) -> str:
        return cast(str, dump(self.unsafe_data, Dumper=Dumper))

    def assertIsNonEmptyString(self, string: str) -> None:
        self.assertTrue(string)
        self.assertIsInstance(string, str)

    def test_dump(self) -> None:
        # Safe data dumps to real YAML text that round-trips back to the original value.
        safe_str = self.safe_str
        self.assertIsNonEmptyString(safe_str)
        self.assertEqual(safe_str, "a:\n- 1\n- 2\n- 3\nb: null\nc: true\n")
        self.assertEqual(self.safe_data, parse_yaml(safe_str))

        # Dumper is the *unsafe* full dumper, so arbitrary Python objects are serialized
        # via the python/object tag (a SafeDumper would raise instead) and round-trip back.
        unsafe_str = self.unsafe_str
        self.assertIsNonEmptyString(unsafe_str)
        self.assertIn("!!python/object:", unsafe_str)
        self.assertIn(AClass.__module__ + "." + AClass.__qualname__, unsafe_str)
        self.assertEqual(self.unsafe_data, unsafe_parse_yaml(unsafe_str))

    def test_safe_parse(self) -> None:
        self.assertEqual(self.safe_data, parse_yaml(self.safe_str))
        with self.assertRaises(Exception):
            parse_yaml(self.unsafe_str)
        with self.assertRaises(Exception):
            parse_yaml("1\n---\n2\n")

    def test_unsafe_parse(self) -> None:
        self.assertEqual(self.safe_data, unsafe_parse_yaml(self.safe_str))
        self.assertEqual(self.unsafe_data, unsafe_parse_yaml(self.unsafe_str))
        with self.assertRaises(Exception):
            unsafe_parse_yaml("1\n---\n2\n")

    def test_multi_parse(self) -> None:
        self.assertEqual(self.safe_data, next(parse_yamls(self.safe_str)))
        with self.assertRaises(Exception):
            next(parse_yamls(self.unsafe_str))
        self.assertEqual(2, len(list(parse_yamls("1\n---\n2\n"))))

    def test_unique_key(self) -> None:
        s = """
        a: 1
        a: 2
        """
        with self.assertRaises(Exception):
            parse_yaml(s)
        with self.assertRaises(Exception):
            next(parse_yamls(s))
