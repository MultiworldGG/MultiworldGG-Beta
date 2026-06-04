import unittest
import typing
from uuid import uuid4

from flask import Flask
from flask.testing import FlaskClient


class TestBase(unittest.TestCase):
    app: typing.ClassVar[Flask]
    client: FlaskClient

    @classmethod
    def setUpClass(cls) -> None:
        from WebHostLib import app as raw_app
        from WebHost import get_app

        raw_app.config["PONY"] = {
            "provider": "sqlite",
            "filename": ":memory:",
            "create_db": True,
        }
        raw_app.config.update({
            "TESTING": True,
            "DEBUG": True,
        })
        try:
            cls.app = get_app()
        except (AssertionError, ValueError) as e:
            # Only one global app object exists, so a second get_app() in the same
            # (xdist) worker re-registers blueprints. Flask <3 raised AssertionError,
            # Flask 3.x raises ValueError. Either way the already-configured app is fine.
            message = e.args[0] if e.args else ""
            if "register_blueprint" not in message and "already registered" not in message:
                raise
            cls.app = raw_app

    def setUp(self) -> None:
        self.client = self.app.test_client()
