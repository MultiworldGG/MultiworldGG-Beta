import pickle
import zlib
from uuid import UUID, uuid4

from flask import url_for

from NetUtils import NetworkSlot, SlotType
from . import TestBase

GAME = "Sphere Test Game"
DATAPACKAGE = {
    "checksum": "sphere-tracker-test-datapackage",
    "item_name_to_id": {"Sword": 100, "Shield": 101, "Bow": 102, "Bomb": 103, "Rupee": 104},
    "location_name_to_id": {"Chest A": 10, "Chest B": 11, "Chest C": 12, "Cave <Deep>": 20, "Cave Exit": 21},
}


def make_multidata() -> bytes:
    multidata = {
        "seed_name": "Sphere Seed",
        "slot_info": {
            1: NetworkSlot("Alice", GAME, SlotType.player),
            2: NetworkSlot("Bob", GAME, SlotType.player),
        },
        "locations": {
            1: {10: (100, 1, 0b001), 11: (101, 2, 0b010), 12: (104, 2, 0)},
            2: {20: (102, 1, 0b100), 21: (103, 1, 0b001)},
        },
        "precollected_items": {1: [], 2: []},
        "spheres": [{1: {10, 11}, 2: {20}}, {1: {12}, 2: {21}}],
        "datapackage": {GAME: DATAPACKAGE},
    }
    return bytes([3]) + zlib.compress(pickle.dumps(multidata))


def make_multisave(checks: dict, times: dict) -> bytes:
    return pickle.dumps({"location_checks": checks, "location_check_times": times})


class TestSphereTracker(TestBase):
    """Rows: sphere 1 holds Chest A (Sword, progression), Chest B (Shield, useful) and Cave <Deep> (Bow, trap);
    sphere 2 holds Cave Exit (Bomb, progression). Chest C is unchecked. Cave <Deep> has no timestamp."""
    room_id: UUID
    tracker_uuid: UUID

    def setUp(self) -> None:
        from WebHostLib.models import db, commit, GameDataPackage, Room, Seed

        super().setUp()
        self.tracker_uuid = uuid4()
        owner = uuid4()
        with self.app.app_context():
            if not GameDataPackage.get(checksum=DATAPACKAGE["checksum"]):
                GameDataPackage(checksum=DATAPACKAGE["checksum"], data=pickle.dumps(DATAPACKAGE))
            seed = Seed(multidata=make_multidata(), owner=owner)
            db.session.flush()
            room = Room(seed_id=seed.id, owner=owner, tracker=self.tracker_uuid, multisave=make_multisave(
                {(0, 1): {10, 11}, (0, 2): {20, 21}},
                {(0, 1): {10: 1000, 11: 2000}, (0, 2): {21: 1500}},
            ))
            db.session.flush()
            self.room_id = room.id
            commit()

    def tearDown(self) -> None:
        from WebHostLib.models import db, commit, Room, Seed

        with self.app.app_context():
            room = Room.get(id=self.room_id)
            if room:
                seed = Seed.get(id=room.seed_id)
                db.session.delete(room)
                if seed:
                    db.session.delete(seed)
                commit()

    def url(self, endpoint: str, tracker: UUID | None = None, **query) -> str:
        with self.app.test_request_context():
            return url_for(endpoint, tracker=tracker or self.tracker_uuid, **query)

    def rows(self, **query) -> dict:
        response = self.client.get(self.url("api.sphere_tracker_rows", **query))
        self.assertEqual(response.status_code, 200, response.data)
        return response.get_json()

    def test_page_renders_shell_without_rows(self) -> None:
        response = self.client.get(self.url("get_multiworld_sphere_tracker"))
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('id="sphere-filters"', html)
        self.assertIn('<option value="1">Alice</option>', html)
        self.assertIn(f'<option value="{GAME}">{GAME}</option>', html)
        self.assertIn(self.url("api.sphere_tracker_rows"), html)
        self.assertIn("<tbody></tbody>", html)
        self.assertNotIn("Chest A", html)

    def test_rows_default_order_and_fields(self) -> None:
        data = self.rows()
        self.assertEqual(data["recordsTotal"], 4)
        self.assertEqual(data["recordsFiltered"], 4)
        self.assertEqual((data["offset"], data["limit"]), (0, 100))
        self.assertNotIn("draw", data)
        self.assertEqual([row["location"] for row in data["data"]],
                         ["Chest A", "Chest B", "Cave <Deep>", "Cave Exit"])
        self.assertEqual(data["data"][0], {
            "team": 0, "sphere": 1, "finder_slot": 1, "finder": "Alice", "receiver_slot": 1, "receiver": "Alice",
            "item_id": 100, "item": "Sword", "flags": 1, "classification": "progression",
            "location_id": 10, "location": "Chest A", "game": GAME, "checked_at": 1000,
        })
        self.assertEqual([row["classification"] for row in data["data"]],
                         ["progression", "useful", "trap", "progression"])
        self.assertIsNone(data["data"][2]["checked_at"])

    def test_rows_paging_echoes_draw(self) -> None:
        data = self.rows(offset=1, limit=2, draw=7)
        self.assertEqual(data["draw"], 7)
        self.assertEqual((data["offset"], data["limit"]), (1, 2))
        self.assertEqual(data["recordsFiltered"], 4)
        self.assertEqual([row["location"] for row in data["data"]], ["Chest B", "Cave <Deep>"])
        self.assertEqual(self.rows(offset=10)["data"], [])
        self.assertEqual(self.rows(limit=5000)["limit"], 1000)

    def test_rows_filters(self) -> None:
        locations = lambda **query: [row["location"] for row in self.rows(**query)["data"]]
        self.assertEqual(locations(finder=2), ["Cave <Deep>", "Cave Exit"])
        self.assertEqual(locations(receiver=1), ["Chest A", "Cave <Deep>", "Cave Exit"])
        self.assertEqual(locations(classification="progression"), ["Chest A", "Cave Exit"])
        self.assertEqual(locations(classification="trap,useful"), ["Chest B", "Cave <Deep>"])
        self.assertEqual(locations(classification=["filler", "trap"]), ["Cave <Deep>"])
        self.assertEqual(locations(sphere_min=2), ["Cave Exit"])
        self.assertEqual(locations(sphere_max=1, finder=1), ["Chest A", "Chest B"])
        self.assertEqual(locations(q="CAVE"), ["Cave <Deep>", "Cave Exit"])
        self.assertEqual(locations(q="bob"), ["Chest B", "Cave <Deep>", "Cave Exit"])
        self.assertEqual(locations(game=GAME), ["Chest A", "Chest B", "Cave <Deep>", "Cave Exit"])
        self.assertEqual(locations(game="Other Game"), [])
        self.assertEqual(locations(team=1), [])
        data = self.rows(finder=1)
        self.assertEqual((data["recordsTotal"], data["recordsFiltered"]), (4, 2))

    def test_rows_sorting(self) -> None:
        times = lambda **query: [row["checked_at"] for row in self.rows(**query)["data"]]
        self.assertEqual(times(sort="checked_at"), [1000, 1500, 2000, None])
        self.assertEqual(times(sort="checked_at", dir="desc"), [2000, 1500, 1000, None])
        items = [row["item"] for row in self.rows(sort="item")["data"]]
        self.assertEqual(items, ["Bomb", "Bow", "Shield", "Sword"])
        spheres = [row["sphere"] for row in self.rows(sort="sphere", dir="desc")["data"]]
        self.assertEqual(spheres, [2, 1, 1, 1])
        classes = [row["classification"] for row in self.rows(sort="classification")["data"]]
        self.assertEqual(classes, ["progression", "progression", "useful", "trap"])

    def test_rows_rejects_bad_parameters(self) -> None:
        for query in ({"sort": "bogus"}, {"dir": "sideways"}, {"finder": "alice"}, {"classification": "junk"},
                      {"sphere_min": "x"}):
            response = self.client.get(self.url("api.sphere_tracker_rows", **query))
            self.assertEqual(response.status_code, 400, query)

    def test_rows_follow_multisave_updates(self) -> None:
        from Utils import utcnow
        from WebHostLib.models import commit, Room

        self.assertEqual(self.rows()["recordsTotal"], 4)
        with self.app.app_context():
            room = Room.get(id=self.room_id)
            room.multisave = make_multisave({(0, 1): {10, 11, 12}, (0, 2): {20, 21}}, {})
            room.last_activity = utcnow()
            commit()
        data = self.rows()
        self.assertEqual(data["recordsTotal"], 5)
        self.assertEqual([row["checked_at"] for row in data["data"]], [None] * 5)
        self.assertIn("Chest C", [row["location"] for row in data["data"]])

    def test_csv_export(self) -> None:
        response = self.client.get(self.url("api.sphere_tracker_rows_csv", sort="checked_at", dir="desc"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/csv")
        self.assertEqual(response.headers["Content-Disposition"],
                         'attachment; filename="sphere_tracker_Sphere_Seed.csv"')
        lines = response.get_data(as_text=True).splitlines()
        self.assertEqual(lines[0], "team,sphere,finder_slot,finder,receiver_slot,receiver,item_id,item,"
                                   "classification,location_id,location,game,checked_at")
        self.assertEqual(lines[1:], [
            f"0,1,1,Alice,2,Bob,101,Shield,useful,11,Chest B,{GAME},1970-01-01T00:33:20+00:00",
            f"0,2,2,Bob,1,Alice,103,Bomb,progression,21,Cave Exit,{GAME},1970-01-01T00:25:00+00:00",
            f"0,1,1,Alice,1,Alice,100,Sword,progression,10,Chest A,{GAME},1970-01-01T00:16:40+00:00",
            f"0,1,2,Bob,1,Alice,102,Bow,trap,20,Cave <Deep>,{GAME},",
        ])
        filtered = self.client.get(self.url("api.sphere_tracker_rows_csv", finder=1)).get_data(as_text=True)
        self.assertEqual(len(filtered.splitlines()), 3)

    def test_legacy_endpoint_shape(self) -> None:
        response = self.client.get(self.url("api.api_sphere_tracker"))
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual([team["team"] for team in data], [0])
        self.assertEqual([sphere["sphere"] for sphere in data[0]["spheres"]], [1, 2])
        first = data[0]["spheres"][0]["finders"]
        self.assertEqual([finder["finder_slot"] for finder in first], [1, 2])
        self.assertEqual(first[0]["receivers"], [
            {"receiver_slot": 1, "pairs": [[100, 10, 1]]},
            {"receiver_slot": 2, "pairs": [[101, 11, 2]]},
        ])

    def test_unknown_tracker_404(self) -> None:
        for endpoint in ("api.sphere_tracker_rows", "api.sphere_tracker_rows_csv", "get_multiworld_sphere_tracker"):
            response = self.client.get(self.url(endpoint, tracker=uuid4()))
            self.assertEqual(response.status_code, 404, endpoint)
