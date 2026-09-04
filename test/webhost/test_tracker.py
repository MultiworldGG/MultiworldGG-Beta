import os
import pickle
from pathlib import Path
from typing import ClassVar
from uuid import UUID, uuid4

from flask import url_for

from . import TestBase


class TestTracker(TestBase):
    room_id: UUID
    tracker_uuid: UUID
    log_filename: str
    data: ClassVar[bytes]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        with (Path(__file__).parent / "data" / "One_MultiworldGG.mwgg").open("rb") as f:
            cls.data = f.read()

    def setUp(self) -> None:
        from MultiServer import Context as MultiServerContext
        from WebHostLib.models import db, commit, GameDataPackage, Room, Seed

        super().setUp()

        multidata = MultiServerContext.decompress(self.data)

        with self.client.session_transaction() as session:
            session["_id"] = uuid4()
            self.tracker_uuid = uuid4()
            with self.app.app_context():
                # store game datapackage(s)
                for game, game_data in multidata["datapackage"].items():
                    if not GameDataPackage.get(checksum=game_data["checksum"]):
                        GameDataPackage(checksum=game_data["checksum"],
                                        data=pickle.dumps(game_data))
                # create an empty seed and a room from it
                seed = Seed(multidata=self.data, owner=session["_id"])
                db.session.flush()
                room = Room(seed_id=seed.id, owner=session["_id"], tracker=self.tracker_uuid)
                db.session.flush()
                self.room_id = room.id
                commit()
                self.log_filename = os.path.join(self.app.config["LOGS_FOLDER"], f"{self.room_id}.txt")

    def tearDown(self) -> None:
        from sqlalchemy import select
        from WebHostLib.models import db, commit, Command, Room, Seed

        with self.app.app_context():
            room: Room = Room.get(id=self.room_id)
            if room:
                for command in db.session.scalars(
                    select(Command).where(Command.room_id == self.room_id)
                ).all():
                    db.session.delete(command)
                seed_id = room.seed_id
                db.session.delete(room)
                if seed_id:
                    seed = Seed.get(id=seed_id)
                    if seed:
                        db.session.delete(seed)
                commit()

        try:
            os.unlink(self.log_filename)
        except FileNotFoundError:
            pass

    def test_valid_if_modified_since(self) -> None:
        """
        Verify that we get a 200 response for valid If-Modified-Since
        """
        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(
                url_for(
                    "get_player_tracker",
                    tracker=self.tracker_uuid,
                    tracked_team=0,
                    tracked_player=1,
                ),
                headers={"If-Modified-Since": "Wed, 21 Oct 2015 07:28:00 GMT"},
            )
            self.assertEqual(response.status_code, 200)

    def test_invalid_if_modified_since(self) -> None:
        """
        Verify that we get a 400 response for invalid If-Modified-Since
        """
        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(
                url_for(
                    "get_player_tracker",
                    tracker=self.tracker_uuid,
                    tracked_team=1,
                    tracked_player=0,
                ),
                headers={"If-Modified-Since": "Wed, 21 Oct 2015 07:28:00"},  # missing timezone
            )
            self.assertEqual(response.status_code, 400)

    def test_tracker_data_api(self) -> None:
        """The /tracker endpoint returns the per-player tracking payload computed from the seed.

        The seed's single slot is a spectator (SlotType.spectator), so all player-driven
        lists (built from ``get_all_players()``) are empty, while ``hints`` is built from
        ``get_all_slots()`` and therefore contains the lone slot, and ``total_checks_done``
        reports one team with zero checks.
        """
        with self.app.test_request_context():
            with self.client.open(url_for("api.tracker_data", tracker=self.tracker_uuid)) as response:
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content_type, "application/json")
                data = response.get_json()

        self.assertEqual(set(data), {
            "aliases", "player_avatars", "player_items_received", "player_checks_done",
            "total_checks_done", "hints", "activity_timers", "connection_timers", "player_status",
        })
        # No player-type slots, so every per-player list is empty.
        for key in ("aliases", "player_avatars", "player_items_received", "player_checks_done",
                    "activity_timers", "connection_timers", "player_status"):
            self.assertEqual(data[key], [], key)
        # total_checks_done is keyed by team via get_team_locations_checked_count(); one team, no checks.
        self.assertEqual(data["total_checks_done"], [{"team": 0, "checks_done": 0}])
        # hints iterates get_all_slots() (includes the spectator slot 1 on team 0) with no hints stored.
        self.assertEqual(data["hints"], [{"team": 0, "player": 1, "hints": []}])

    def test_static_tracker_data_api(self) -> None:
        """The /static_tracker endpoint echoes the seed's datapackage and per-player static data."""
        with self.app.test_request_context():
            with self.client.open(url_for("api.static_tracker_data", tracker=self.tracker_uuid)) as response:
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content_type, "application/json")
                data = response.get_json()

        self.assertEqual(set(data), {"groups", "datapackage", "player_locations_total", "player_game"})
        # The lone slot is a spectator, so the player-driven lists and groups are empty.
        self.assertEqual(data["groups"], [])
        self.assertEqual(data["player_game"], [])
        self.assertEqual(data["player_locations_total"], [])
        # datapackage is passed through from the seed's multidata verbatim.
        self.assertEqual(set(data["datapackage"]), {"Archipelago"})
        archipelago = data["datapackage"]["Archipelago"]
        self.assertEqual(archipelago["checksum"], "ac9141e9ad0318df2fa27da5f20c50a842afeecb")
        self.assertEqual(archipelago["item_name_to_id"], {"Nothing": -1})
        self.assertEqual(archipelago["location_name_to_id"], {"Cheat Console": -1, "Server": -2})

    def test_tracker_slot_data_api(self) -> None:
        """The /slot_data_tracker endpoint returns per-player slot data (empty: only a spectator slot)."""
        with self.app.test_request_context():
            with self.client.open(url_for("api.tracker_slot_data", tracker=self.tracker_uuid)) as response:
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content_type, "application/json")
                self.assertEqual(response.get_json(), [])

    def test_tracker_api_unknown_tracker_404(self) -> None:
        """Each tracker endpoint aborts with 404 when no room matches the tracker UUID."""
        unknown = uuid4()
        with self.app.test_request_context():
            for endpoint in ("api.tracker_data", "api.static_tracker_data", "api.tracker_slot_data"):
                with self.client.open(url_for(endpoint, tracker=unknown)) as response:
                    self.assertEqual(response.status_code, 404, endpoint)
