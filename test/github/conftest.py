"""Importer for the standalone ``karen_review.py`` script.

``karen_review.py`` lives in the sibling ``GitHubLib/fuzz-image/`` service, not
under this test package. It is a script, not a package module, and it uses
``@dataclass`` decorators that require the module to be registered in
``sys.modules`` *before* its body executes (otherwise ``dataclass`` raises
``AttributeError`` resolving the module). We load it by file path and register
it, then expose it as a session fixture.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

# This file is test/github/conftest.py; the reviewer lives in the sibling service.
_KAREN_PATH = Path(__file__).resolve().parents[2] / "GitHubLib" / "fuzz-image" / "karen_review.py"


def _load_karen():
    spec = importlib.util.spec_from_file_location("karen_review", _KAREN_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["karen_review"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def karen():
    return _load_karen()
