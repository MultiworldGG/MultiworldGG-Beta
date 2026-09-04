from __future__ import annotations

import asyncio
import collections
import datetime
import functools
import itertools
import logging
import multiprocessing
import pickle
import random
import socket
import threading
import time
import typing
import sys
from collections.abc import Iterable

import psutil
import websockets
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

import Utils

from MultiServer import (
    Context, server, auto_shutdown, ServerCommandProcessor, ClientMessageProcessor, load_server_cert,
    server_per_message_deflate_factory,
)
from Utils import restricted_loads, cache_argsless

from .locker import Locker
from .models import Command, GameDataPackage, Room


class CustomClientMessageProcessor(ClientMessageProcessor):
    ctx: WebHostContext

    def _cmd_video(self, platform: str, user: str):
        """Set a link for your name in the WebHostLib tracker pointing to a video stream.
        Currently, only YouTube and Twitch platforms are supported.
        """
        if platform.lower().startswith("t"):  # twitch
            self.ctx.video[self.client.team, self.client.slot] = "Twitch", user
            self.ctx.save()
            self.output(f"Registered Twitch Stream https://www.twitch.tv/{user}")
            return True
        elif platform.lower().startswith("y"):  # youtube
            self.ctx.video[self.client.team, self.client.slot] = "Youtube", user
            self.ctx.save()
            self.output(f"Registered Youtube Stream for {user}")
            return True
        return False


# inject
import MultiServer

MultiServer.client_message_processor = CustomClientMessageProcessor
del MultiServer


class DBCommandProcessor(ServerCommandProcessor):
    def output(self, text: str):
        self.ctx.logger.info(text)


class DualStackServer:
    """Wraps two websockets.Server instances (one AF_INET, one AF_INET6) under a single interface.

    Both servers listen on the same TCP port so that clients using either address family can
    reach the room.  The public API mirrors websockets.asyncio.server.Server closely enough
    that the rest of customserver.py can treat this object like a plain websockets server.
    """

    def __init__(self, server_v4: websockets.asyncio.server.Server,
                 server_v6: typing.Optional[websockets.asyncio.server.Server]) -> None:
        self._servers: typing.List[websockets.asyncio.server.Server] = [server_v4]
        if server_v6 is not None:
            self._servers.append(server_v6)

    @property
    def sockets(self) -> typing.Tuple[socket.socket, ...]:
        result: typing.List[socket.socket] = []
        for srv in self._servers:
            result.extend(srv.sockets)
        return tuple(result)

    def close(self) -> None:
        for srv in self._servers:
            srv.close()

    async def wait_closed(self) -> None:
        for srv in self._servers:
            await srv.wait_closed()


async def _serve_dual_stack(
    handler,
    desired_port: int,
    *,
    ssl,
    extensions,
    logger: logging.Logger,
) -> DualStackServer:
    """Bind AF_INET and AF_INET6 sockets on the same port and serve both.

    The v6 socket needs IPV6_V6ONLY=1 or it grabs the full dual-stack binding
    and the v4 socket can't share the port on Linux. A racing v6 bind retries
    on a fresh ephemeral port, then falls back to v4-only rather than crashing
    the room.
    """
    MAX_RETRIES = 3

    serve_kwargs = dict(ssl=ssl, extensions=extensions)

    for attempt in range(MAX_RETRIES):
        sock_v4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock_v4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock_v4.bind(("0.0.0.0", desired_port))
            port = sock_v4.getsockname()[1]
        except OSError:
            sock_v4.close()
            raise  # let the caller handle "port in use" via the OSError fallback

        sock_v6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        try:
            sock_v6.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
            sock_v6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock_v6.bind(("::", port))
        except OSError as exc:
            sock_v6.close()
            sock_v4.close()
            if attempt < MAX_RETRIES - 1:
                logger.warning(
                    "IPv6 bind to port %d failed (%s), retrying with a fresh port (attempt %d/%d).",
                    port, exc, attempt + 1, MAX_RETRIES,
                )
                desired_port = 0  # ask OS for a fresh ephemeral port next round
                continue
            # All retries exhausted: fall back to v4-only rather than crashing the room.
            logger.warning(
                "IPv6 dual-stack bind failed after %d attempts (%s). "
                "Falling back to IPv4-only for this room.",
                MAX_RETRIES, exc,
            )
            sock_v4_fallback = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_v4_fallback.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock_v4_fallback.bind(("0.0.0.0", desired_port))
            server_v4 = await websockets.serve(handler, sock=sock_v4_fallback, **serve_kwargs)
            return DualStackServer(server_v4, None)

        # Both sockets bound to the same port; hand them to websockets.
        server_v4 = await websockets.serve(handler, sock=sock_v4, **serve_kwargs)
        try:
            server_v6 = await websockets.serve(handler, sock=sock_v6, **serve_kwargs)
        except Exception as exc:
            server_v4.close()
            await server_v4.wait_closed()
            sock_v6.close()
            logger.warning(
                "websockets.serve for IPv6 socket failed (%s). "
                "Falling back to IPv4-only.",
                exc,
            )
            # Re-start v4-only on the same port
            sock_v4_retry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_v4_retry.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock_v4_retry.bind(("0.0.0.0", port))
            server_v4 = await websockets.serve(handler, sock=sock_v4_retry, **serve_kwargs)
            return DualStackServer(server_v4, None)

        return DualStackServer(server_v4, server_v6)

    # Should be unreachable, but satisfy the type checker.
    raise RuntimeError("_serve_dual_stack exhausted retry budget without returning")


class WebHostContext(Context):
    room_id: int
    _db_engine = None  # set by run_server_process

    def __init__(self, static_server_data: dict, logger: logging.Logger):
        # static server data is used during _load_game_data to load required data,
        # without needing to import worlds system, which takes quite a bit of memory
        self.static_server_data = static_server_data
        super(WebHostContext, self).__init__("", 0, "", "", 1,
                                             40, True, "enabled", "enabled",
                                             "enabled", 0, 2, logger=logger)
        del self.static_server_data
        self.main_loop = asyncio.get_running_loop()
        self.video = {}
        self.tags = ["AP", "WebHost"]

    def __del__(self):
        from Utils import format_SI_prefix
        self.logger.debug(f"Context destroyed, Mem: {format_SI_prefix(psutil.Process().memory_info().rss, 1024)}iB")

    def _load_game_data(self):
        for key, value in self.static_server_data.items():
            # NOTE: attributes are mutable and shared, so they will have to be copied before being modified
            setattr(self, key, value)
        self.non_hintable_names = collections.defaultdict(frozenset, self.non_hintable_names)

    async def listen_to_db_commands(self):
        cmdprocessor = DBCommandProcessor(self)

        while not self.exit_event.is_set():
            self._process_db_commands(cmdprocessor)
            try:
                await asyncio.wait_for(self.exit_event.wait(), 5)
            except asyncio.TimeoutError:
                pass

    def _process_db_commands(self, cmdprocessor):
        engine = WebHostContext._db_engine
        if engine is None:
            return
        with Session(engine) as session:
            commands = session.scalars(
                select(Command).where(Command.room_id == self.room_id)
            ).all()
            if commands:
                for command in commands:
                    self.main_loop.call_soon_threadsafe(cmdprocessor, command.commandtext)
                    session.delete(command)
                session.commit()

    def load(self, room_id: int):
        self.room_id = room_id
        engine = WebHostContext._db_engine
        with Session(engine) as session:
            room = session.get(Room, room_id)
            # last_port is -1 (crash sentinel) or 0/None (never hosted); -1 is
            # truthy and binding to it raises OverflowError, wedging the room.
            if room.last_port and room.last_port > 0:
                self.port = room.last_port
            else:
                self.port = get_random_port()

            multidata = self.decompress(room.seed.multidata)

        game_data_packages = {}

        static_gamespackage = self.gamespackage  # this is shared across all rooms
        static_item_name_groups = self.item_name_groups
        static_location_name_groups = self.location_name_groups
        self.gamespackage = {"Archipelago": static_gamespackage.get("Archipelago", {})}  # this may be modified by _load
        self.item_name_groups = {"Archipelago": static_item_name_groups.get("Archipelago", {})}
        self.location_name_groups = {"Archipelago": static_location_name_groups.get("Archipelago", {})}
        missing_checksum = False

        with Session(engine) as session:
            for game in list(multidata.get("datapackage", {})):
                game_data = multidata["datapackage"][game]
                if "checksum" in game_data:
                    if static_gamespackage.get(game, {}).get("checksum") == game_data["checksum"]:
                        # non-custom. remove from multidata and use static data
                        del multidata["datapackage"][game]
                    else:
                        row = session.get(GameDataPackage, game_data["checksum"])
                        if row:  # None if rolled on >= 0.3.9 but uploaded to <= 0.3.8
                            game_data_packages[game] = restricted_loads(row.data)
                            continue
                        else:
                            self.logger.warning(f"Did not find game_data_package for {game}: {game_data['checksum']}")
                else:
                    missing_checksum = True  # Game rolled on old AP and will load data package from multidata
                self.gamespackage[game] = static_gamespackage.get(game, {})
                self.item_name_groups[game] = static_item_name_groups.get(game, {})
                self.location_name_groups[game] = static_location_name_groups.get(game, {})

        if not game_data_packages and not missing_checksum:
            # all static -> use the static dicts directly
            self.gamespackage = static_gamespackage
            self.item_name_groups = static_item_name_groups
            self.location_name_groups = static_location_name_groups
        return self._load(multidata, game_data_packages, True)

    def init_save(self, enabled: bool = True):
        self.saving = enabled
        if self.saving:
            engine = WebHostContext._db_engine
            with Session(engine) as session:
                room = session.get(Room, self.room_id)
                savegame_data = room.multisave
                if savegame_data:
                    self.set_save(restricted_loads(savegame_data))
            self._seed_slot_avatars()
            self._start_async_saving(atexit_save=False)
        asyncio.create_task(self.listen_to_db_commands())

    def _seed_slot_avatars(self) -> None:
        """Seed profile_data with web-set slot avatars so connected clients
        render them. Best-effort: a failure here must never block room boot."""
        try:
            from WebHostLib.avatars import apply_slot_avatars_to_stored_data
            with Session(WebHostContext._db_engine) as session:
                apply_slot_avatars_to_stored_data(session, self.room_id, self.stored_data)
        except Exception:
            self.logger.exception("Failed to seed slot avatars from web")

    def _save(self, exit_save: bool = False) -> bool:
        engine = WebHostContext._db_engine
        with Session(engine) as session:
            room = session.get(Room, self.room_id)
            # Does not use Utils.restricted_dumps because we'd rather make a save than not make one
            room.multisave = pickle.dumps(self.get_save())
            # saving only occurs on activity, so we can "abuse" this information to mark this as last_activity
            if not exit_save:  # we don't want to count a shutdown as activity, which would restart the server again
                room.last_activity = Utils.utcnow()
            session.commit()
        return True

    def get_save(self) -> dict:
        d = super(WebHostContext, self).get_save()
        d["video"] = [(tuple(playerslot), videodata) for playerslot, videodata in self.video.items()]
        return d


def get_random_port():
    return random.randint(49152, 65535)


class GameRangePorts(typing.NamedTuple):
    valid_ports: list[int]
    ephemeral_allowed: bool


class RandomPortSocketCreator:
    """ Creates server sockets on random available ports from a configured range. """

    _next_port_index: int
    _used_ports_cache: tuple[frozenset[int], int] | None
    _parsed_ports: GameRangePorts

    def __init__(self, game_ports: Iterable[str | int]) -> None:
        self._next_port_index = 0
        self._used_ports_cache = None
        self._parsed_ports = self._parse_game_ports(game_ports)

    @property
    def ephemeral_allowed(self) -> bool:
        return self._parsed_ports.ephemeral_allowed

    @staticmethod
    def _parse_game_ports(game_ports: Iterable[str | int]) -> GameRangePorts:
        """ Parse the game ports configuration into a structured format. """
        valid_ports: list[int] = []
        ephemeral_allowed = False

        for item in game_ports:
            if isinstance(item, str) and "-" in item:
                start, end = map(int, item.split("-"))
                x = range(start, end + 1)
                valid_ports.extend(x)
            elif int(item) == 0:
                ephemeral_allowed = True
            else:
                valid_ports.append(int(item))

        random.shuffle(valid_ports)
        return GameRangePorts(valid_ports, ephemeral_allowed)

    @staticmethod
    def _try_conns_per_process(p: psutil.Process) -> Iterable[int]:
        """ Get ports from a single process's connections. """
        try:
            return (c.laddr.port for c in p.net_connections("tcp4") if c.laddr)
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            return ()

    @staticmethod
    def _get_active_net_connections() -> Iterable[int]:
        """ Get all active TCP4 connections on the system. """
        # Don't even try to check if system using AIX
        if psutil.AIX:
            return ()

        try:
            return (c.laddr.port for c in psutil.net_connections("tcp4") if c.laddr)
        # raises AccessDenied when done on macOS
        except psutil.AccessDenied:
            # flatten the list of iterables
            return itertools.chain.from_iterable(map(
                RandomPortSocketCreator._try_conns_per_process,
                psutil.process_iter(["net_connections"])
            ))

    def _get_used_ports(self) -> frozenset[int]:
        """ Get currently used ports with 90-second caching. """
        t_hash = round(time.monotonic() / 90)
        if self._used_ports_cache is None or self._used_ports_cache[1] != t_hash:
            self._used_ports_cache = (frozenset(self._get_active_net_connections()), t_hash)

        return self._used_ports_cache[0]

    def create(self, host: str) -> socket.socket:
        """ Create a server socket on an available port. """
        valid_ports, ephemeral_allowed = self._parsed_ports
        used_ports = self._get_used_ports()

        next_index = self._next_port_index
        for i, port in enumerate(itertools.chain(valid_ports[next_index:], valid_ports[:next_index])):
            if port in used_ports:
                continue

            try:
                res = socket.create_server((host, port))
                next_index = (next_index + i + 1) % len(valid_ports)
                self._next_port_index = next_index
                return res
            except OSError:
                pass

        if ephemeral_allowed:
            return socket.create_server((host, 0))

        raise OSError(98, "No available ports")


@cache_argsless
def get_static_server_data() -> dict:
    import worlds
    data = {
        "non_hintable_names": {
            world_name: world.hint_blacklist
            for world_name, world in worlds.AutoWorldRegister.world_types.items()
        },
        "gamespackage": {
            world_name: {
                key: value
                for key, value in game_package.items()
                if key not in ("item_name_groups", "location_name_groups")
            }
            for world_name, game_package in worlds.network_data_package["games"].items()
        },
        "item_name_groups": {
            world_name: world.item_name_groups
            for world_name, world in worlds.AutoWorldRegister.world_types.items()
        },
        "location_name_groups": {
            world_name: world.location_name_groups
            for world_name, world in worlds.AutoWorldRegister.world_types.items()
        },
    }

    return data


def set_up_logging(room_id, logs_folder: typing.Optional[str] = None) -> logging.Logger:
    import os
    # logger setup
    logger = logging.getLogger(f"RoomLogger {room_id}")

    # this *should* be empty, but just in case.
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    if logs_folder is None:
        from . import app
        logs_folder = app.config["LOGS_FOLDER"]
    os.makedirs(logs_folder, exist_ok=True)
    file_handler = logging.FileHandler(
        os.path.join(logs_folder, f"{room_id}.txt"),
        "a",
        encoding="utf-8-sig")
    file_handler.setFormatter(logging.Formatter("[%(asctime)s]: %(message)s"))
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    return logger


def tear_down_logging(room_id):
    """Close logging handling for a room."""
    logger_name = f"RoomLogger {room_id}"
    if logger_name in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()
        del logging.Logger.manager.loggerDict[logger_name]


def run_server_process(name: str, ponyconfig: dict, static_server_data: dict,
                       cert_file: typing.Optional[str], cert_key_file: typing.Optional[str],
                       host: str, game_ports: Iterable[str | int],
                       rooms_to_run: multiprocessing.Queue, rooms_shutting_down: multiprocessing.Queue,
                       logs_folder: typing.Optional[str] = None):
    from setproctitle import setproctitle

    setproctitle(name)
    Utils.init_logging(name)
    Utils.reload_application_options()
    import MultiServer
    MultiServer.version_tuple = Utils.version_tuple
    try:
        import resource
    except ModuleNotFoundError:
        pass  # unix only module
    else:
        # Each Server is another file handle, so request as many as we can from the system
        file_limit = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
        # set soft limit to hard limit
        resource.setrlimit(resource.RLIMIT_NOFILE, (file_limit, file_limit))
        del resource, file_limit

    # establish DB connection for multidata and multisave
    from WebHost import _pony_config_to_sqlalchemy_uri
    db_uri = _pony_config_to_sqlalchemy_uri(ponyconfig)
    engine = create_engine(db_uri)
    WebHostContext._db_engine = engine

    if "worlds" in sys.modules:
        raise Exception("Worlds system should not be loaded in the custom server.")

    import gc

    if not cert_file:
        def get_ssl_context():
            return None
    else:
        load_date = None
        ssl_context = load_server_cert(cert_file, cert_key_file)

        def get_ssl_context():
            nonlocal load_date, ssl_context
            today = datetime.date.today()
            if load_date != today:
                ssl_context = load_server_cert(cert_file, cert_key_file)
                load_date = today
            return ssl_context

    del ponyconfig
    gc.collect()  # free intermediate objects used during setup

    # Fresh spawned process: create and install our own loop (get_event_loop is
    # deprecated without a current loop on 3.12+).
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    socket_creator = RandomPortSocketCreator(game_ports)

    async def start_room(room_id):
        with Locker(f"RoomLocker {room_id}"):
            logger = logging.getLogger()  # init logger separately to assure error logs
            try:
                logger = set_up_logging(room_id, logs_folder)
                ctx = WebHostContext(static_server_data, logger)
                ctx.load(room_id)
                ctx.init_save()
                assert ctx.server is None
                handler = functools.partial(server, ctx=ctx)
                ssl_ctx = get_ssl_context()
                try:
                    ctx.server = await _serve_dual_stack(
                        handler,
                        ctx.port,
                        ssl=ssl_ctx,
                        extensions=[server_per_message_deflate_factory],
                        logger=ctx.logger,
                    )
                except OSError:  # likely port in use: retry on a port from the configured range
                    # Rebind dual-stack on the port RandomPortSocketCreator probed; the
                    # close-to-rebind race is tolerable (_serve_dual_stack retries).
                    probe = socket_creator.create(ctx.host)
                    retry_port = probe.getsockname()[1]
                    probe.close()
                    try:
                        ctx.server = await _serve_dual_stack(
                            handler,
                            retry_port,
                            ssl=ssl_ctx,
                            extensions=[server_per_message_deflate_factory],
                            logger=ctx.logger,
                        )
                    except OSError:
                        # Lost the rebind race. Only fall through to an ephemeral port if
                        # the GAME_PORTS config allows ports outside the configured range.
                        if not socket_creator.ephemeral_allowed:
                            raise
                        ctx.server = await _serve_dual_stack(
                            handler,
                            0,
                            ssl=ssl_ctx,
                            extensions=[server_per_message_deflate_factory],
                            logger=ctx.logger,
                        )
                # Both sockets share the same port; just read it from the first socket.
                port = ctx.server.sockets[0].getsockname()[1]
                if port:
                    ctx.logger.info(f'Hosting game at {host}:{port}')
                    with Session(engine) as session:
                        room = session.get(Room, ctx.room_id)
                        room.last_port = port
                        session.commit()
                    del room
                else:
                    ctx.logger.exception("Could not determine port. Likely hosting failure.")
                with Session(engine) as session:
                    ctx.auto_shutdown = session.get(Room, room_id).timeout
                if ctx.saving:
                    setattr(asyncio.current_task(), "save", lambda: ctx._save(True))
                assert ctx.shutdown_task is None
                ctx.shutdown_task = asyncio.create_task(auto_shutdown(ctx, []))
                await ctx.shutdown_task

            except (KeyboardInterrupt, SystemExit):
                if ctx.saving:
                    ctx._save(True)
                    setattr(asyncio.current_task(), "save", None)
            except Exception as e:
                with Session(engine) as session:
                    room = session.get(Room, room_id)
                    room.last_port = -1
                    session.commit()
                del room
                logger.exception(e)
                raise
            else:
                if ctx.saving:
                    ctx._save(True)
                    setattr(asyncio.current_task(), "save", None)
            finally:
                try:
                    ctx.save_dirty = False  # make sure the saving thread does not write to DB after final wakeup
                    ctx.exit_event.set()  # make sure the saving thread stops at some point
                    # NOTE: async saving should probably be an async task and could be merged with shutdown_task

                    if ctx.server:
                        ctx.server.close()
                        await ctx.server.wait_closed()

                    with Session(engine) as session:
                        # ensure the Room does not spin up again on its own, minute of safety buffer
                        room = session.get(Room, room_id)
                        room.last_activity = Utils.utcnow() - datetime.timedelta(minutes=1, seconds=room.timeout)
                        session.commit()
                    del room
                    tear_down_logging(room_id)
                    logging.info(f"Shutting down room {room_id} on {name}.")
                finally:
                    await asyncio.sleep(5)
                    rooms_shutting_down.put(room_id)

    class Starter(threading.Thread):
        _tasks: typing.List[asyncio.Future]

        def __init__(self):
            super().__init__()
            self._tasks = []

        def _done(self, task: asyncio.Future):
            self._tasks.remove(task)
            task.result()

        def run(self):
            while 1:
                next_room = rooms_to_run.get(block=True, timeout=None)
                gc.collect()
                task = asyncio.run_coroutine_threadsafe(start_room(next_room), loop)
                self._tasks.append(task)
                task.add_done_callback(self._done)
                logging.info(f"Starting room {next_room} on {name}.")
                del task  # delete reference to task object

    starter = Starter()
    starter.daemon = True
    starter.start()
    try:
        loop.run_forever()
    finally:
        # save all tasks that want to be saved during shutdown
        for task in asyncio.all_tasks(loop):
            save: typing.Optional[typing.Callable[[], typing.Any]] = getattr(task, "save", None)
            if save:
                save()
