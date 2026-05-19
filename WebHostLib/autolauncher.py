from __future__ import annotations

import json
import logging
import multiprocessing
import os
import shutil
import typing
from datetime import timedelta, datetime
from threading import Event, Thread
from typing import Any
from uuid import UUID

from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import Session

from Utils import restricted_loads, utcnow
from .locker import Locker, AlreadyRunningException

_stop_event = Event()


def stop() -> None:
    """Stops previously launched threads"""
    global _stop_event
    stop_event = _stop_event
    _stop_event = Event()  # new event for new threads
    stop_event.set()


# Track in-flight generations with their start time for stuck detection
_in_flight_generations: dict[UUID, datetime] = {}
_in_flight_lock = __import__('threading').Lock()

# Engine shared within this process (set by init_generator or _get_engine)
_engine = None


def _get_engine():
    global _engine
    return _engine


def _mark_generation_complete(gen_id: UUID) -> None:
    """Remove a generation from in-flight tracking when it completes."""
    with _in_flight_lock:
        _in_flight_generations.pop(gen_id, None)


def _mark_generation_started(gen_id: UUID) -> None:
    """Track when a generation starts for stuck detection."""
    with _in_flight_lock:
        _in_flight_generations[gen_id] = utcnow()


def _get_stuck_generations(threshold: timedelta) -> list[UUID]:
    """Return IDs of generations that have exceeded the stuck threshold."""
    now = utcnow()
    with _in_flight_lock:
        return [gid for gid, start_time in _in_flight_generations.items()
                if now - start_time > threshold]


def handle_generation_success(seed_id):
    if seed_id:
        _mark_generation_complete(seed_id)
    logging.info(f"Generation finished for seed {seed_id}")


def handle_generation_failure(result: BaseException):
    try:  # hacky way to get the full RemoteTraceback
        raise result
    except Exception as e:
        logging.exception(e)


def _get_lobby_apworld_root() -> str | None:
    from . import app as web_app
    root = web_app.config.get("LOBBY_APWORLD_PATH")
    if not root:
        return None
    return os.path.abspath(str(root))


def _cleanup_stale_preview_files(max_age: timedelta = timedelta(hours=1)) -> int:
    root = _get_lobby_apworld_root()
    if not root or not os.path.isdir(root):
        return 0

    cutoff = utcnow() - max_age
    removed_files = 0
    for lobby_entry in os.scandir(root):
        if not lobby_entry.is_dir():
            continue
        preview_dir = os.path.join(lobby_entry.path, "preview")
        if not os.path.isdir(preview_dir):
            continue
        for preview_file in os.scandir(preview_dir):
            if not preview_file.is_file():
                continue
            try:
                modified = datetime.utcfromtimestamp(preview_file.stat().st_mtime)
            except OSError:
                continue
            if modified < cutoff:
                try:
                    os.unlink(preview_file.path)
                    removed_files += 1
                except OSError:
                    pass
        try:
            if not any(os.scandir(preview_dir)):
                os.rmdir(preview_dir)
        except OSError:
            pass

    if removed_files:
        logging.info(f"Removed {removed_files} stale lobby APWorld preview file(s).")
    return removed_files


def _mp_gen_game(
    gen_options: dict,
    meta: dict[str, Any] | None = None,
    owner=None,
    sid=None,
    timeout: int|None = None,
) -> Any:
    from setproctitle import setproctitle
    from . import app as flask_app
    from .generate import gen_game

    setproctitle(f"Generator ({sid})")
    try:
        # gen_game uses db.engine (Flask-SQLAlchemy proxy) which needs an app context.
        # Pool workers don't run inside a Flask request, so push one here.
        with flask_app.app_context():
            return gen_game(gen_options, meta=meta, owner=owner, sid=sid, timeout=timeout)
    finally:
        setproctitle(f"Generator (idle)")


def launch_generator(pool: multiprocessing.pool.Pool, generation: Generation, timeout: int|None) -> None:
    try:
        meta = json.loads(generation.meta)
        options = restricted_loads(generation.options)
        logging.info(f"Generating {generation.id} for {len(options)} players")
        pool.apply_async(
            _mp_gen_game,
            (options,),
            {
                "meta": meta,
                "sid": generation.id,
                "owner": generation.owner,
                "timeout": timeout,
            },
            handle_generation_success,
            handle_generation_failure,
        )
    except Exception as e:
        generation.state = STATE_ERROR
        logging.exception(e)
    else:
        generation.state = STATE_STARTED
        _mark_generation_started(generation.id)


def init_generator(config: dict[str, Any]) -> None:
    global _engine
    from setproctitle import setproctitle

    setproctitle("Generator (idle)")

    try:
        import resource
    except ModuleNotFoundError:
        pass  # unix only module
    else:
        # set soft limit for memory to from config (default 4GiB)
        soft_limit = config["GENERATOR_MEMORY_LIMIT"]
        old_limit, hard_limit = resource.getrlimit(resource.RLIMIT_AS)
        if soft_limit != old_limit:
            resource.setrlimit(resource.RLIMIT_AS, (soft_limit, hard_limit))
            logging.debug(f"Changed AS mem limit {old_limit} -> {soft_limit}")
        del resource, soft_limit, hard_limit

    pony_config = config["PONY"]
    from WebHost import _pony_config_to_sqlalchemy_uri
    db_uri = _pony_config_to_sqlalchemy_uri(pony_config)
    _engine = create_engine(db_uri)


def cleanup():
    """delete unowned user-content and expired lobbies"""
    engine = _get_engine()
    with Session(engine) as session:
        # >>> bool(uuid.UUID(int=0))
        # True
        null_owner = UUID(int=0)
        rooms_to_delete = session.scalars(
            select(Room).where(Room.owner == null_owner)
        ).all()
        rooms_count = len(rooms_to_delete)
        for room in rooms_to_delete:
            session.delete(room)

        seeds_to_delete = session.scalars(
            select(Seed).where(Seed.owner == null_owner)
        ).all()
        seeds_count = 0
        for seed in seeds_to_delete:
            # Only delete if no rooms reference this seed
            if not session.scalars(select(Room).where(Room.seed_id == seed.id).limit(1)).first():
                session.delete(seed)
                seeds_count += 1

        slots_to_delete = session.scalars(
            select(Slot).where(Slot.seed_id == None)
        ).all()
        slots_count = len(slots_to_delete)
        for slot in slots_to_delete:
            session.delete(slot)
        # Command gets cascade-deleted when Room is deleted
        session.commit()

    if rooms_count or seeds_count or slots_count:
        logging.info(f"{rooms_count} Rooms, {seeds_count} Seeds and {slots_count} Slots have been deleted.")

    # Clean up expired lobbies (closed for > 1 hour) and done lobbies (> 3 days old)
    engine = _get_engine()
    with Session(engine) as session:
        now = utcnow()
        closed_cutoff = now - timedelta(hours=1)
        done_cutoff = now - timedelta(days=3)
        stale_lobbies = session.scalars(
            select(Lobby).where(
                ((Lobby.state == LOBBY_CLOSED) & (Lobby.last_activity < closed_cutoff)) |
                ((Lobby.state == LOBBY_DONE) & (Lobby.last_activity < done_cutoff))
            )
        ).all()
        lobby_apworld_root = _get_lobby_apworld_root()
        for lobby in stale_lobbies:
            request_paths = [r.storage_path for r in lobby.apworld_requests]
            apworld_paths = [a.storage_path for a in lobby.apworlds]

            for r in list(lobby.apworld_requests):
                session.delete(r)
            for a in list(lobby.apworlds):
                session.delete(a)

            lobby_apworld_dir = (
                os.path.join(lobby_apworld_root, str(lobby.id))
                if lobby_apworld_root else None
            )
            if lobby_apworld_dir:
                shutil.rmtree(lobby_apworld_dir, ignore_errors=True)
            else:
                for path in request_paths + apworld_paths:
                    try:
                        os.unlink(path)
                    except OSError:
                        pass
            # Clear player references on messages first (messages are cascade-deleted by lobby)
            for m in lobby.messages:
                m.player_id = None
            session.delete(lobby)
        if stale_lobbies:
            session.commit()
            logging.info(f"{len(stale_lobbies)} stale lobbies cleaned up.")

    _cleanup_stale_preview_files()


def expire_lobbies():
    """Expire lobbies that have been inactive beyond their timeout."""
    engine = _get_engine()
    with Session(engine) as session:
        now = utcnow()
        stale_lobbies = session.scalars(
            select(Lobby).where(Lobby.state.in_([LOBBY_OPEN, LOBBY_LOCKED, LOBBY_GENERATING]))
        ).all()
        expired_count = 0
        for lobby in stale_lobbies:
            if now - lobby.last_activity > timedelta(minutes=lobby.timeout_minutes):
                lobby.state = LOBBY_CLOSED
                expired_count += 1
        if expired_count:
            session.commit()
            logging.info(f"{expired_count} lobbies expired due to inactivity.")
    _cleanup_stale_preview_files()


def autohost(config: dict):
    def keep_running():
        global _engine
        stop_event = _stop_event
        try:
            with Locker("autohost"):
                # Set up engine for this thread
                pony_config = config["PONY"]
                from WebHost import _pony_config_to_sqlalchemy_uri
                db_uri = _pony_config_to_sqlalchemy_uri(pony_config)
                _engine = create_engine(db_uri)

                cleanup()
                hosters = []
                for x in range(config["HOSTERS"]):
                    hoster = MultiworldInstance(config, x)
                    hosters.append(hoster)
                    hoster.start()

                last_lobby_check = utcnow()

                while not stop_event.wait(0.1):
                    with Session(_engine) as session:
                        max_timeout = config["MAX_ROOM_TIMEOUT"]
                        rooms = session.scalars(
                            select(Room)
                            .where(Room.last_activity >= utcnow() - timedelta(seconds=max_timeout))
                            .order_by(desc(Room.last_port))
                        ).all()
                        for room in rooms:
                            # we have to filter twice, as per-room timeout can't be expressed in one query
                            if room.last_activity >= utcnow() - timedelta(seconds=room.timeout + 5):
                                hosters[room.id.int % len(hosters)].start_room(room.id)

                    # Check for expired lobbies every 5 minutes
                    now = utcnow()
                    if now - last_lobby_check > timedelta(minutes=5):
                        last_lobby_check = now
                        try:
                            expire_lobbies()
                        except Exception as e:
                            logging.exception(e)

        except AlreadyRunningException:
            logging.info("Autohost reports as already running, not starting another.")

    Thread(target=keep_running, name="AP_Autohost").start()


def autogen(config: dict):
    def keep_running():
        global _engine
        stop_event = _stop_event
        try:
            with Locker("autogen"):
                # Set up engine for this thread
                pony_config = config["PONY"]
                from WebHost import _pony_config_to_sqlalchemy_uri
                db_uri = _pony_config_to_sqlalchemy_uri(pony_config)
                _engine = create_engine(db_uri)

                with multiprocessing.Pool(config["GENERATORS"], initializer=init_generator,
                                          initargs=(config,), maxtasksperchild=10) as generator_pool:
                    job_time = config["JOB_TIME"]
                    # Grace period: JOB_TIME * 3
                    # When worker is killed and neither the success nor error callback fires.
                    stuck_threshold = timedelta(seconds=(job_time * 3))
                    last_stuck_check = utcnow()

                    with Session(_engine) as session:
                        to_start = session.scalars(
                            select(Generation).where(Generation.state == STATE_STARTED)
                        ).all()

                        if to_start:
                            logging.info("Resuming generation")
                            for generation in to_start:
                                sid = session.get(Seed, generation.id)
                                if sid:
                                    session.delete(generation)
                                else:
                                    launch_generator(generator_pool, generation, timeout=job_time)

                            # Delete error-state generations
                            error_gens = session.scalars(
                                select(Generation).where(Generation.state == STATE_ERROR)
                            ).all()
                            for g in error_gens:
                                session.delete(g)
                            session.commit()

                    while not stop_event.wait(0.1):
                        try:
                            now = utcnow()

                            # Check for stuck generations every 2 mins
                            if now - last_stuck_check > timedelta(seconds=120):
                                last_stuck_check = now
                                stuck_ids = _get_stuck_generations(stuck_threshold)
                                if stuck_ids:
                                    with Session(_engine) as session:
                                        for gid in stuck_ids:
                                            gen = session.get(Generation, gid)
                                            if gen is not None and gen.state == STATE_STARTED:
                                                # Worker died without completing - mark as error
                                                logging.warning(f"Generation {gid} appears stuck (worker may have died), marking as error")
                                                gen.state = STATE_ERROR
                                                meta = json.loads(gen.meta)
                                                meta["error"] = "Generation worker died unexpectedly. Please try again."
                                                gen.meta = json.dumps(meta)
                                            _mark_generation_complete(gid)
                                        session.commit()

                            with Session(_engine) as session:
                                # for_update locks the database row(s) during transaction
                                to_start = session.scalars(
                                    select(Generation)
                                    .where(Generation.state == STATE_QUEUED)
                                    .with_for_update()
                                ).all()
                                for generation in to_start:
                                    launch_generator(generator_pool, generation, timeout=job_time)
                                if to_start:
                                    session.commit()
                        except Exception as e:
                            logging.exception(e)
                            stop_event.wait(5)
        except AlreadyRunningException:
            logging.info("Autogen reports as already running, not starting another.")

    Thread(target=keep_running, name="AP_Autogen").start()


class MultiworldInstance():
    def __init__(self, config: dict, id: int):
        self.room_ids = set()
        self.process: typing.Optional[multiprocessing.Process] = None
        self.ponyconfig = config["PONY"]
        self.cert = config["SELFLAUNCHCERT"]
        self.key = config["SELFLAUNCHKEY"]
        self.host = config["HOST_ADDRESS"]
        self.rooms_to_start = multiprocessing.Queue()
        self.rooms_shutting_down = multiprocessing.Queue()
        self.name = f"MultiHoster{id}"
        self.process_start_time = None
        self.restart_interval = timedelta(hours=12)

    def start(self):
        if self.process and self.process.is_alive():
            return False

        process = multiprocessing.Process(group=None, target=run_server_process,
                                          args=(self.name, self.ponyconfig, get_static_server_data(),
                                                self.cert, self.key, self.host,
                                                self.rooms_to_start, self.rooms_shutting_down),
                                          name=self.name)
        process.start()
        self.process = process
        self.process_start_time = utcnow()

    def should_restart(self) -> bool:
        """Check if process should be restarted to reload fresh APWorld data"""
        if not self.process_start_time:
            return False

        time_for_restart = utcnow() - self.process_start_time > self.restart_interval
        is_idle = len(self.room_ids) == 0
        return time_for_restart and is_idle

    def start_room(self, room_id):
        while not self.rooms_shutting_down.empty():
            self.room_ids.remove(self.rooms_shutting_down.get(block=True, timeout=None))

        if self.should_restart():
            logging.info(f"{self.name} restarting to load fresh APWorld data (process was idle, no rooms were interrupted")
            self.stop(wait=True)  # Wait for old process to fully terminate before starting new one
            self.start()

        if room_id in self.room_ids:
            pass  # should already be hosted currently.
        else:
            self.room_ids.add(room_id)
            self.rooms_to_start.put(room_id)

    def stop(self, wait: bool = False):
        if self.process:
            self.process.terminate()
            if wait:
                self.process.join(timeout=5)
                if self.process.is_alive():
                    self.process.kill()
                    self.process.join(timeout=2)
            self.process = None
            self.process_start_time = None
            self.rooms_to_start = multiprocessing.Queue()
            self.rooms_shutting_down = multiprocessing.Queue()

    def done(self):
        return self.process and not self.process.is_alive()

    def collect(self):
        self.process.join()  # wait for process to finish
        self.process = None


from .models import Room, Generation, STATE_QUEUED, STATE_STARTED, STATE_ERROR, Seed, Slot, Lobby, LobbyApworld, LOBBY_OPEN, LOBBY_GENERATING, LOBBY_CLOSED, LOBBY_DONE, LOBBY_LOCKED
from .customserver import run_server_process, get_static_server_data
