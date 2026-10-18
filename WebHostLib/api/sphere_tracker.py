"""Sphere tracker JSON endpoints.

``/api/sphere_tracker/<tracker>`` is the all-at-once view consumed by third-party tools.
``/api/sphere_tracker/<tracker>/rows`` backs the sphere tracker page: one flat row per checked
location, filtered, sorted and paged server-side from a per-room table cached in the worker.
``/api/sphere_tracker/<tracker>/rows.csv`` streams every row of the room and ignores the query.

Query parameters of ``rows``:
    q                       case-insensitive substring over finder, receiver, item, location, game
    exact                   truthy: ``q`` must equal one of those fields instead of appearing in it
    team, finder, receiver  repeatable slot numbers (comma lists accepted)
    game                    repeatable game names
    classification          repeatable: progression, useful, trap, filler
    sphere_min, sphere_max  inclusive sphere range
    sort, dir               a SORT_KEYS name and ``asc`` or ``desc``
    offset, limit, draw     paging (``limit`` capped at MAX_LIMIT); ``draw`` is echoed for DataTables

``rows.csv`` guards: at most CSV_MAX_CONCURRENT exports per worker process (503 with Retry-After
beyond that), and an export ends with a ``# truncated`` line once CSV_MAX_ROWS rows are written or
CSV_TIME_BUDGET_SECONDS have gone into serialising.
"""
from __future__ import annotations

import csv
import datetime
import io
import re
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Iterator, NamedTuple
from uuid import UUID

from flask import Response, abort, jsonify, request
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import ServiceUnavailable

from NetUtils import get_item_classification_label
from .. import cache
from ..models import Room
from ..tracker import TrackerData, TRACKER_CACHE_TIMEOUT_IN_SECONDS
from . import api_endpoints

DEFAULT_LIMIT = 100
MAX_LIMIT = 1000
MAX_TABLES = 8
MAX_VIEWS_PER_TABLE = 4
TABLE_IDLE_SECONDS = 300
CLASSIFICATIONS = ("progression", "useful", "trap", "filler")
CSV_COLUMNS = ("team", "sphere", "finder_slot", "finder", "receiver_slot", "receiver", "item_id", "item",
               "classification", "location_id", "location", "game", "checked_at")
CSV_CHUNK_ROWS = 5000
CSV_MAX_ROWS = 1_000_000
CSV_TIME_BUDGET_SECONDS = 20.0
CSV_MAX_CONCURRENT = 1


class SphereRow(NamedTuple):
    team: int
    sphere: int
    finder_slot: int
    finder: str
    receiver_slot: int
    receiver: str
    item_id: int
    item: str
    flags: int
    location_id: int
    location: str
    game: str
    checked_at: int | None

    def as_dict(self) -> dict[str, Any]:
        data = self._asdict()
        data["classification"] = get_item_classification_label(self.flags)
        return data


def _classification_rank(flags: int) -> int:
    if flags & 0b001:
        return 0
    if flags & 0b010:
        return 1
    if flags & 0b100:
        return 3
    return 2


def _matches_classification(flags: int, wanted: frozenset[str]) -> bool:
    return bool(("progression" in wanted and flags & 0b001)
                or ("useful" in wanted and flags & 0b010)
                or ("trap" in wanted and flags & 0b100)
                or ("filler" in wanted and not flags))


SORT_KEYS: dict[str, Callable[[SphereRow], Any]] = {
    "sphere": lambda row: row.sphere,
    "finder": lambda row: row.finder,
    "receiver": lambda row: row.receiver,
    "item": lambda row: row.item,
    "classification": lambda row: _classification_rank(row.flags),
    "location": lambda row: row.location,
    "game": lambda row: row.game,
    "checked_at": lambda row: row.checked_at,
}


@dataclass(frozen=True)
class RowQuery:
    q: str = ""
    exact: bool = False
    teams: frozenset[int] = frozenset()
    finders: frozenset[int] = frozenset()
    receivers: frozenset[int] = frozenset()
    games: frozenset[str] = frozenset()
    classifications: frozenset[str] = frozenset()
    sphere_min: int | None = None
    sphere_max: int | None = None
    sort: str = "sphere"
    desc: bool = False

    @classmethod
    def from_args(cls, args: MultiDict) -> "RowQuery":
        classifications = frozenset(value.lower() for value in _split(args.getlist("classification")))
        if not classifications <= set(CLASSIFICATIONS):
            abort(400, f"classification must be one of {', '.join(CLASSIFICATIONS)}")
        sort = args.get("sort", "sphere")
        if sort not in SORT_KEYS:
            abort(400, f"sort must be one of {', '.join(SORT_KEYS)}")
        direction = args.get("dir", "asc")
        if direction not in ("asc", "desc"):
            abort(400, "dir must be asc or desc")
        return cls(
            q=args.get("q", "").strip(),
            exact=_bool_arg(args, "exact"),
            teams=_int_set(args.getlist("team")),
            finders=_int_set(args.getlist("finder")),
            receivers=_int_set(args.getlist("receiver")),
            games=frozenset(game for game in args.getlist("game") if game),
            classifications=classifications,
            sphere_min=_int_arg(args, "sphere_min"),
            sphere_max=_int_arg(args, "sphere_max"),
            sort=sort,
            desc=direction == "desc",
        )


def _split(values: Iterable[str]) -> Iterator[str]:
    for value in values:
        for part in value.split(","):
            part = part.strip()
            if part:
                yield part


def _int_set(values: Iterable[str]) -> frozenset[int]:
    try:
        return frozenset(int(part) for part in _split(values))
    except ValueError:
        abort(400, "slot filters must be integers")


def _int_arg(args: MultiDict, name: str, default: int | None = None) -> int | None:
    value = args.get(name, "").strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        abort(400, f"{name} must be an integer")


def _bool_arg(args: MultiDict, name: str) -> bool:
    return args.get(name, "").strip().lower() not in ("", "0", "false", "no", "off")


@dataclass
class SphereTable:
    """Flat, default-ordered rows for one room plus the small per-table caches the endpoints use."""
    rows: list[SphereRow]
    seed_name: str
    last_activity: datetime.datetime
    built_at: float
    last_used: float
    lowercase: dict[str, str] = field(default_factory=dict)
    views: dict[RowQuery, list[SphereRow]] = field(default_factory=dict)


def build_table(tracker_data: TrackerData, last_activity: datetime.datetime, now: float) -> SphereTable:
    rows: list[SphereRow] = []
    names: dict[int, str] = {}
    games: dict[int, str] = {}
    for team, _ in tracker_data.get_all_slots().items():
        for slot in tracker_data.get_all_slots()[team]:
            names[slot] = tracker_data.get_player_name(slot)
            games[slot] = tracker_data.get_player_game(slot)

    for team, players in tracker_data.get_all_players().items():
        for sphere, sphere_locations in enumerate(tracker_data.get_spheres(), start=1):
            for finder, location_ids in sphere_locations.items():
                checked = tracker_data.get_player_checked_locations(team, finder)
                if not checked:
                    continue
                locations = tracker_data.get_player_locations(finder)
                times = tracker_data.get_player_location_check_times(team, finder)
                finder_name, finder_game = names[finder], games[finder]
                location_names = tracker_data.location_id_to_name[finder_game]
                for location_id in checked.intersection(location_ids):
                    placed = locations.get(location_id)
                    if placed is None:
                        continue
                    item_id, receiver, flags = placed
                    rows.append(SphereRow(
                        team, sphere, finder, finder_name, receiver, names[receiver],
                        item_id, tracker_data.item_id_to_name[games[receiver]][item_id], flags,
                        location_id, location_names[location_id], finder_game, times.get(location_id),
                    ))
    rows.sort(key=lambda row: (row.team, row.sphere, row.finder, row.location))
    return SphereTable(rows, tracker_data.get_seed_name(), last_activity, now, now)


_tables: dict[UUID, SphereTable] = {}
_build_locks: dict[UUID, threading.Lock] = {}
_tables_lock = threading.Lock()


def _fresh(table: SphereTable, room: Room, now: float) -> bool:
    return table.last_activity == room.last_activity and now - table.built_at < TRACKER_CACHE_TIMEOUT_IN_SECONDS


def _cached_table(room: Room, now: float) -> SphereTable | None:
    table = _tables.get(room.tracker)
    if table and _fresh(table, room, now):
        table.last_used = now
        return table
    return None


def _evict(now: float) -> None:
    for tracker, table in list(_tables.items()):
        if now - table.last_used > TABLE_IDLE_SECONDS:
            del _tables[tracker]
    while len(_tables) > MAX_TABLES:
        del _tables[min(_tables, key=lambda tracker: _tables[tracker].last_used)]
    for tracker in list(_build_locks):
        if tracker not in _tables:
            del _build_locks[tracker]


def get_table(room: Room) -> SphereTable:
    """Returns the room's row table, rebuilding it once the multisave changed or the cache timeout passed."""
    now = time.monotonic()
    with _tables_lock:
        table = _cached_table(room, now)
        if table:
            return table
        build_lock = _build_locks.setdefault(room.tracker, threading.Lock())
    with build_lock:
        with _tables_lock:
            table = _cached_table(room, now)
            if table:
                return table
        table = build_table(TrackerData(room), room.last_activity, time.monotonic())
        with _tables_lock:
            _tables[room.tracker] = table
            _evict(table.built_at)
    return table


def _filter_rows(table: SphereTable, query: RowQuery) -> list[SphereRow]:
    rows: Iterable[SphereRow] = table.rows
    if query.teams:
        rows = (row for row in rows if row.team in query.teams)
    if query.finders:
        rows = (row for row in rows if row.finder_slot in query.finders)
    if query.receivers:
        rows = (row for row in rows if row.receiver_slot in query.receivers)
    if query.games:
        rows = (row for row in rows if row.game in query.games)
    if query.sphere_min is not None:
        rows = (row for row in rows if row.sphere >= query.sphere_min)
    if query.sphere_max is not None:
        rows = (row for row in rows if row.sphere <= query.sphere_max)
    if query.classifications and not query.classifications >= set(CLASSIFICATIONS):
        wanted = query.classifications
        rows = (row for row in rows if _matches_classification(row.flags, wanted))
    if query.q:
        needle = query.q.lower()
        lowercase = table.lowercase

        def low(text: str) -> str:
            try:
                return lowercase[text]
            except KeyError:
                lowercase[text] = lowered = text.lower()
                return lowered

        if query.exact:
            rows = (row for row in rows if needle in (low(row.finder), low(row.receiver), low(row.item),
                                                       low(row.location), low(row.game)))
        else:
            rows = (row for row in rows if needle in low(row.finder) or needle in low(row.receiver)
                    or needle in low(row.item) or needle in low(row.location) or needle in low(row.game))
    return rows if isinstance(rows, list) else list(rows)


def _sort_rows(rows: list[SphereRow], query: RowQuery) -> list[SphereRow]:
    if query.sort == "sphere" and not query.desc:
        return rows
    key = SORT_KEYS[query.sort]
    if query.sort != "checked_at":
        return sorted(rows, key=key, reverse=query.desc)
    # rows without a timestamp stay last in both directions
    timed = sorted((row for row in rows if row.checked_at is not None), key=key, reverse=query.desc)
    timed.extend(row for row in rows if row.checked_at is None)
    return timed


def select_rows(table: SphereTable, query: RowQuery) -> list[SphereRow]:
    """Filtered and sorted rows for ``query``, memoized on the table for repeat page fetches."""
    with _tables_lock:
        rows = table.views.get(query)
    if rows is not None:
        return rows
    rows = _sort_rows(_filter_rows(table, query), query)
    with _tables_lock:
        while len(table.views) >= MAX_VIEWS_PER_TABLE:
            table.views.pop(next(iter(table.views)), None)
        table.views[query] = rows
    return rows


@api_endpoints.route("/sphere_tracker/<suuid:tracker>/rows")
def sphere_tracker_rows(tracker: UUID) -> Response:
    room = Room.get(tracker=tracker)
    if not room:
        abort(404)
    query = RowQuery.from_args(request.args)
    offset = max(_int_arg(request.args, "offset", 0), 0)
    limit = min(max(_int_arg(request.args, "limit", DEFAULT_LIMIT), 1), MAX_LIMIT)

    table = get_table(room)
    rows = select_rows(table, query)
    payload: dict[str, Any] = {
        "recordsTotal": len(table.rows),
        "recordsFiltered": len(rows),
        "offset": offset,
        "limit": limit,
        "data": [row.as_dict() for row in rows[offset:offset + limit]],
    }
    draw = _int_arg(request.args, "draw")
    if draw is not None:
        payload["draw"] = draw
    return jsonify(payload)


_csv_exports = threading.BoundedSemaphore(CSV_MAX_CONCURRENT)


def _csv_timestamp(checked_at: int | None) -> str:
    if checked_at is None:
        return ""
    return datetime.datetime.fromtimestamp(checked_at, datetime.timezone.utc).isoformat()


def _csv_chunks(rows: list[SphereRow]) -> Iterator[str]:
    """Header, then CSV_CHUNK_ROWS rows per chunk; cut at CSV_MAX_ROWS or once serialising alone
    (time blocked on the client does not count) has used CSV_TIME_BUDGET_SECONDS, ending with a note."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(CSV_COLUMNS)
    yield buffer.getvalue()
    limit = min(len(rows), CSV_MAX_ROWS)
    written = 0
    spent = 0.0
    while written < limit:
        started = time.monotonic()
        buffer.seek(0)
        buffer.truncate()
        chunk = rows[written:min(written + CSV_CHUNK_ROWS, limit)]
        for row in chunk:
            writer.writerow((
                row.team, row.sphere, row.finder_slot, row.finder, row.receiver_slot, row.receiver,
                row.item_id, row.item, get_item_classification_label(row.flags),
                row.location_id, row.location, row.game, _csv_timestamp(row.checked_at),
            ))
        written += len(chunk)
        spent += time.monotonic() - started
        yield buffer.getvalue()
        if spent >= CSV_TIME_BUDGET_SECONDS:
            break
    if written < len(rows):
        buffer.seek(0)
        buffer.truncate()
        writer.writerow((f"# truncated: {written} of {len(rows)} rows",))
        yield buffer.getvalue()


@api_endpoints.route("/sphere_tracker/<suuid:tracker>/rows.csv")
def sphere_tracker_rows_csv(tracker: UUID) -> Response:
    room = Room.get(tracker=tracker)
    if not room:
        abort(404)
    if not _csv_exports.acquire(blocking=False):
        raise ServiceUnavailable("Another sphere tracker export is running, retry in a moment.", retry_after=10)
    try:
        table = get_table(room)
    except BaseException:
        _csv_exports.release()
        raise
    response = Response(_csv_chunks(table.rows), mimetype="text/csv")
    response.call_on_close(_csv_exports.release)
    filename = re.sub(r"[^A-Za-z0-9_-]+", "_", table.seed_name) or "room"
    response.headers["Content-Disposition"] = f'attachment; filename="sphere_tracker_{filename}.csv"'
    return response


def _collect_used_data(td: TrackerData) -> tuple[
    dict[int, dict[int, dict[int, dict[int, list[tuple[int, int, int]]]]]],
    dict[str, set[int]],
    dict[str, dict[int, int]],
]:
    """
    Walk through spheres and compute:
      - used_pairs_by_team:
          {team: {sphere_idx: {finder_slot: {receiver_slot: [(item_id, loc_id, item_flag), ...]}}}}
      - used_loc_ids_by_game: {game: {loc_id, ...}}
      - used_item_flags_by_game: {game: {item_id: flags_or}}
    """
    used_pairs_by_team: dict[int, dict[int, dict[int, dict[int, list[tuple[int, int, int]]]]]] = {}
    used_loc_ids_by_game: dict[str, set[int]] = {}
    used_item_flags_by_game: dict[str, dict[int, int]] = {}

    spheres = td.get_spheres() or []
    all_players = td.get_all_players() or {}

    for team, _players in (all_players or {}).items():
        team_map = used_pairs_by_team.setdefault(team, {})
        for sphere_idx, sphere in enumerate(spheres, start=1):
            sphere_map = team_map.setdefault(sphere_idx, {})
            for finder_slot, sphere_loc_ids in (sphere or {}).items():
                checked = td.get_player_checked_locations(team, finder_slot) or set()
                if not checked:
                    continue

                loc_map = td.get_player_locations(finder_slot) or {}
                if not loc_map:
                    continue

                finder_game = td.get_player_game(finder_slot)

                for loc_id in set(sphere_loc_ids).intersection(checked):
                    if loc_id not in loc_map:
                        continue
                    item_id, receiver_slot, item_flags = loc_map[loc_id]
                    receiver_game = td.get_player_game(receiver_slot)

                    finder_map = sphere_map.setdefault(finder_slot, {})
                    rec_list = finder_map.setdefault(receiver_slot, [])
                    rec_list.append((item_id, loc_id, int(item_flags or 0)))

                    used_loc_ids_by_game.setdefault(finder_game, set()).add(loc_id)

                    game_flags = used_item_flags_by_game.setdefault(receiver_game, {})
                    game_flags[item_id] = game_flags.get(item_id, 0) | int(item_flags or 0)

    # stable, deterministic sort: by (loc_id, item_id); ignore the flag in ordering
    for team_map in used_pairs_by_team.values():
        for sphere_map in team_map.values():
            for finder_map in sphere_map.values():
                for receiver_slot, pairs in finder_map.items():
                    pairs.sort(key=lambda t: (t[1], t[0]))  # (loc_id, item_id)

    return used_pairs_by_team, used_loc_ids_by_game, used_item_flags_by_game


def _collect_player_games(td: TrackerData) -> dict[int, dict[int, str]]:
    """
    Build a map {team: {slot: game_name}} using TrackerData.get_player_game.
    """
    all_players = td.get_all_players() or {}
    out: dict[int, dict[int, str]] = {}
    for team, slots in (all_players or {}).items():
        team_map = out.setdefault(team, {})
        for slot in (slots or []):
            team_map[slot] = td.get_player_game(slot)
    return out


# Main endpoint (IDs + game meta). Cache varies only on `tracker`.
# Names for items/locations should be resolved client-side via the datapackage.

@api_endpoints.route("/sphere_tracker/<suuid:tracker>")
def api_sphere_tracker(tracker):
    """IDs view enriched with per-pair item flag. Client resolves names via /api/datapackage
       and player games via /api/room_status/<RoomUUID>."""
    return _api_sphere_tracker_cached(tracker)

@cache.memoize(timeout=TRACKER_CACHE_TIMEOUT_IN_SECONDS)
def _api_sphere_tracker_cached(tracker):
    room = Room.get(tracker=tracker)
    if not room:
        abort(404)

    td = TrackerData(room)
    used_pairs_by_team, _used_loc_ids_by_game, _used_item_flags_by_game = _collect_used_data(td)

    out: list[dict[str, Any]] = []
    for team_id in sorted(used_pairs_by_team.keys()):
        spheres_out: list[dict[str, Any]] = []
        for sphere_idx in sorted(used_pairs_by_team[team_id].keys()):
            finders_out: list[dict[str, Any]] = []
            for finder_slot in sorted(used_pairs_by_team[team_id][sphere_idx].keys()):
                receivers_out: list[dict[str, Any]] = []
                for receiver_slot in sorted(used_pairs_by_team[team_id][sphere_idx][finder_slot].keys()):
                    pairs = [
                        [item_id, loc_id, item_flag]
                        for (item_id, loc_id, item_flag) in
                        used_pairs_by_team[team_id][sphere_idx][finder_slot][receiver_slot]
                    ]
                    receivers_out.append({
                        "receiver_slot": receiver_slot,
                        "pairs": pairs
                    })
                if receivers_out:
                    finders_out.append({
                        "finder_slot": finder_slot,
                        "receivers": receivers_out
                    })
            if finders_out:
                spheres_out.append({"sphere": sphere_idx, "finders": finders_out})
        if spheres_out:
            out.append({"team": team_id, "spheres": spheres_out})

    return jsonify(out)
