"""Pytest rootdir conftest.

Loaded by pytest before any test modules are collected. We prepend
`test/_stubs/` to `sys.path` so that test code importing `mwgg_igdb` resolves
to the in-repo stub instead of trying to import the real (network-installed)
package. See `test/_stubs/mwgg_igdb.py` for the stub itself.
"""
import sys
from pathlib import Path

_stub_dir = str(Path(__file__).parent / "test" / "_stubs")
if _stub_dir not in sys.path:
    sys.path.insert(0, _stub_dir)
