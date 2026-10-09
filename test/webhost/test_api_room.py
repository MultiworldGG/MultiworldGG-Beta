"""/api/room_status and /api/get_seeds player listings over the Seed.slots relationship."""
from types import SimpleNamespace
from uuid import uuid4

import pytest

from WebHostLib import to_url

EXPECTED_PLAYERS = [["Alice", "Clique"], ["Bob", "Clique"], ["Charlie", "Clique"]]


@pytest.fixture
def room_with_slots(app):
    from WebHostLib.models import db, commit, Room, Seed, Slot

    with app.app_context():
        owner = uuid4()
        seed = Seed(multidata=b"", owner=owner)
        db.session.flush()
        # inserted out of player order so id order differs from player_id order
        for player_id, name in ((3, "Charlie"), (1, "Alice"), (2, "Bob")):
            Slot(player_id=player_id, player_name=name, game="Clique", seed_id=seed.id, data=b"patch")
        room = Room(seed_id=seed.id, owner=owner, tracker=uuid4())
        db.session.flush()
        snapshot = SimpleNamespace(id=room.id, seed_id=seed.id, owner=owner)
        commit()

    yield snapshot

    with app.app_context():
        db.session.delete(db.session.get(Seed, snapshot.seed_id))
        commit()


def test_room_status_lists_players_in_player_id_order(client, room_with_slots):
    response = client.get(f"/api/room_status/{to_url(room_with_slots.id)}")

    assert response.status_code == 200, response.data
    data = response.get_json()
    assert data["players"] == EXPECTED_PLAYERS
    assert [download["slot"] for download in data["downloads"]] == [1, 2, 3]


def test_get_seeds_lists_players_in_player_id_order(client, room_with_slots):
    with client.session_transaction() as session:
        session["_id"] = room_with_slots.owner

    response = client.get("/api/get_seeds")

    assert response.status_code == 200, response.data
    seeds = response.get_json()
    assert [seed["players"] for seed in seeds] == [EXPECTED_PLAYERS]
