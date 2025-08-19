"""
A module for interacting with SNI (SNES Network Interface).

This module provides low-level functions for connecting to and communicating with SNI,
similar to how _bizhawk provides BizHawk communication functions.
"""

import asyncio
import enum
import logging
import os
import subprocess
import sys
import time
import typing
from json import dumps, loads

import Utils
from settings import Settings
from websockets.client import connect as websockets_connect, WebSocketClientProtocol
from websockets.exceptions import ConnectionClosed, WebSocketException

if typing.TYPE_CHECKING:
    from .context import SNIContext

snes_logger = logging.getLogger("SNES")

_global_snes_reconnect_delay = 5


class SNESState(enum.IntEnum):
    SNES_DISCONNECTED = 0
    SNES_CONNECTING = 1
    SNES_CONNECTED = 2
    SNES_ATTACHED = 3


class SNESRequest(typing.TypedDict):
    Opcode: str
    Space: str
    Operands: typing.List[str]
    # TODO: When Python 3.11 is the lowest version supported, `Operands` can use `typing.NotRequired` (pep-0655)
    # Then the `Operands` key doesn't need to be given for opcodes that don't use it.


def launch_sni() -> None:
    sni_path = Settings.sni_options.sni_path

    if not os.path.isdir(sni_path):
        sni_path = Utils.local_path(sni_path)
    if os.path.isdir(sni_path):
        dir_entry: "os.DirEntry[str]"
        for dir_entry in os.scandir(sni_path):
            if dir_entry.is_file():
                lower_file = dir_entry.name.lower()
                if (lower_file.startswith("sni.") and not lower_file.endswith(".proto")) or (lower_file == "sni"):
                    sni_path = dir_entry.path
                    break

    if os.path.isfile(sni_path):
        snes_logger.info(f"Attempting to start {sni_path}")
        import sys
        if not sys.stdout:  # if it spawns a visible console, may as well populate it
            subprocess.Popen(os.path.abspath(sni_path), cwd=os.path.dirname(sni_path))
        else:
            proc = subprocess.Popen(os.path.abspath(sni_path), cwd=os.path.dirname(sni_path),
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                proc.wait(.1)  # wait a bit to see if startup fails (missing dependencies)
                snes_logger.info('Failed to start SNI. Try running it externally for error output.')
            except subprocess.TimeoutExpired:
                pass  # seems to be running

    else:
        snes_logger.info(
            f"Attempt to start SNI was aborted as path {sni_path} was not found, "
            f"please start it yourself if it is not running")


async def _snes_connect(ctx: "SNIContext", address: str, retry: bool = True) -> WebSocketClientProtocol:
    address = f"ws://{address}" if "://" not in address else address
    snes_logger.info("Connecting to SNI at %s ..." % address)
    seen_problems: typing.Set[str] = set()
    while True:
        try:
            snes_socket = await websockets_connect(address, ping_timeout=None, ping_interval=None)
        except Exception as e:
            problem = "%s" % e
            # only tell the user about new problems, otherwise silently lay in wait for a working connection
            if problem not in seen_problems:
                seen_problems.add(problem)
                snes_logger.error(f"Error connecting to SNI ({problem})")

                if len(seen_problems) == 1:
                    # this is the first problem. Let's try launching SNI if it isn't already running
                    launch_sni()

            await asyncio.sleep(1)
        else:
            return snes_socket
        if not retry:
            break


async def get_snes_devices(ctx: "SNIContext") -> typing.List[str]:
    socket = await _snes_connect(ctx, ctx.snes_address)  # establish new connection to poll
    DeviceList_Request: SNESRequest = {
        "Opcode": "DeviceList",
        "Space": "SNES",
        "Operands": []
    }
    await socket.send(dumps(DeviceList_Request))

    reply: typing.Dict[str, typing.Any] = loads(await socket.recv())
    devices: typing.List[str] = reply['Results'] if 'Results' in reply and len(reply['Results']) > 0 else []

    if not devices:
        snes_logger.info('No SNES device found. Please connect a SNES device to SNI.')
        while not devices and not ctx.exit_event.is_set():
            await asyncio.sleep(0.1)
            await socket.send(dumps(DeviceList_Request))
            reply = loads(await socket.recv())
            devices = reply['Results'] if 'Results' in reply and len(reply['Results']) > 0 else []
    if devices:
        await verify_snes_app(socket)
    await socket.close()
    return sorted(devices)


async def verify_snes_app(socket: WebSocketClientProtocol) -> None:
    AppVersion_Request = {
        "Opcode": "AppVersion",
    }
    await socket.send(dumps(AppVersion_Request))

    app: str = loads(await socket.recv())["Results"][0]
    if "SNI" not in app:
        snes_logger.warning(f"Warning: Did not find SNI as the endpoint, instead {app} was found.")


async def snes_connect(ctx: "SNIContext", address: str, deviceIndex: int = -1) -> None:
    global _global_snes_reconnect_delay
    if ctx.snes_socket is not None and ctx.snes_state == SNESState.SNES_CONNECTED:
        if ctx.rom:
            snes_logger.error('Already connected to SNES, with rom loaded.')
        else:
            snes_logger.error('Already connected to SNI, likely awaiting a device.')
        return

    ctx.cancel_snes_autoreconnect()

    device = None
    recv_task = None
    ctx.snes_state = SNESState.SNES_CONNECTING
    socket = await _snes_connect(ctx, address)
    ctx.snes_socket = socket
    ctx.snes_state = SNESState.SNES_CONNECTED

    try:
        devices = await get_snes_devices(ctx)
        device_count = len(devices)

        if device_count == 1:
            device = devices[0]
        elif ctx.snes_reconnect_address:
            assert ctx.snes_attached_device
            if ctx.snes_attached_device[1] in devices:
                device = ctx.snes_attached_device[1]
            else:
                device = devices[ctx.snes_attached_device[0]]
        elif device_count > 1:
            if deviceIndex == -1:
                snes_logger.info(f"Found {device_count} SNES devices. "
                                 f"Connect to one with /snes <address> <device number>. For example /snes {address} 1")

                for idx, availableDevice in enumerate(devices):
                    snes_logger.info(str(idx + 1) + ": " + availableDevice)

            elif (deviceIndex < 0) or (deviceIndex - 1) > device_count:
                snes_logger.warning("SNES device number out of range")

            else:
                device = devices[deviceIndex - 1]

        if device is None:
            await snes_disconnect(ctx)
            return

        snes_logger.info("Attaching to " + device)

        Attach_Request: SNESRequest = {
            "Opcode": "Attach",
            "Space": "SNES",
            "Operands": [device]
        }
        await ctx.snes_socket.send(dumps(Attach_Request))
        ctx.snes_state = SNESState.SNES_ATTACHED
        ctx.snes_attached_device = (devices.index(device), device)
        ctx.snes_reconnect_address = address
        recv_task = asyncio.create_task(snes_recv_loop(ctx))

    except Exception as e:
        ctx.snes_state = SNESState.SNES_DISCONNECTED
        if task_alive(recv_task):
            if not ctx.snes_socket.closed:
                await ctx.snes_socket.close()
        else:
            if ctx.snes_socket is not None:
                if not ctx.snes_socket.closed:
                    await ctx.snes_socket.close()
                ctx.snes_socket = None
        snes_logger.error(f"Error connecting to snes ({e}), retrying in {_global_snes_reconnect_delay} seconds")
        ctx.snes_autoreconnect_task = asyncio.create_task(snes_autoreconnect(ctx), name="snes auto-reconnect")
        _global_snes_reconnect_delay *= 2
    else:
        _global_snes_reconnect_delay = 5  # Reset to default delay
        snes_logger.info(f"Attached to {device}")


async def snes_disconnect(ctx: "SNIContext") -> None:
    if ctx.snes_socket:
        if not ctx.snes_socket.closed:
            await ctx.snes_socket.close()
        ctx.snes_socket = None


def task_alive(task: typing.Optional[asyncio.Task]) -> bool:
    if task:
        return not task.done()
    return False


async def snes_autoreconnect(ctx: "SNIContext") -> None:
    await asyncio.sleep(_global_snes_reconnect_delay)
    if not ctx.snes_socket and not task_alive(ctx.snes_connect_task):
        address = ctx.snes_reconnect_address if ctx.snes_reconnect_address else ctx.snes_address
        ctx.snes_connect_task = asyncio.create_task(snes_connect(ctx, address), name="SNES Connect")


async def snes_recv_loop(ctx: "SNIContext") -> None:
    try:
        if ctx.snes_socket is None:
            raise Exception("invalid context state - snes_socket not connected")
        async for msg in ctx.snes_socket:
            ctx.snes_recv_queue.put_nowait(typing.cast(bytes, msg))
        snes_logger.warning("Snes disconnected")
    except Exception as e:
        if not isinstance(e, WebSocketException):
            snes_logger.exception(e)
        snes_logger.error("Lost connection to the snes, type /snes to reconnect")
    finally:
        socket, ctx.snes_socket = ctx.snes_socket, None
        if socket is not None and not socket.closed:
            await socket.close()

        ctx.snes_state = SNESState.SNES_DISCONNECTED
        ctx.snes_recv_queue = asyncio.Queue()
        ctx.hud_message_queue = []

        ctx.rom = None

        if ctx.snes_reconnect_address:
            snes_logger.info(f"... automatically reconnecting to snes in {_global_snes_reconnect_delay} seconds")
            assert ctx.snes_autoreconnect_task is None
            ctx.snes_autoreconnect_task = asyncio.create_task(snes_autoreconnect(ctx), name="snes auto-reconnect")


async def snes_read(ctx: "SNIContext", address: int, size: int) -> typing.Optional[bytes]:
    try:
        await ctx.snes_request_lock.acquire()

        if (
            ctx.snes_state != SNESState.SNES_ATTACHED or
            ctx.snes_socket is None or
            not ctx.snes_socket.open or
            ctx.snes_socket.closed
        ):
            return None

        GetAddress_Request: SNESRequest = {
            "Opcode": "GetAddress",
            "Space": "SNES",
            "Operands": [hex(address)[2:], hex(size)[2:]]
        }
        try:
            await ctx.snes_socket.send(dumps(GetAddress_Request))
        except ConnectionClosed:
            return None

        data: bytes = bytes()
        while len(data) < size:
            try:
                data += await asyncio.wait_for(ctx.snes_recv_queue.get(), 5)
            except asyncio.TimeoutError:
                break

        if len(data) != size:
            snes_logger.error('Error reading %s, requested %d bytes, received %d' % (hex(address), size, len(data)))
            if len(data):
                snes_logger.error(str(data))
                snes_logger.warning('Communication Failure with SNI')
            if ctx.snes_socket is not None and not ctx.snes_socket.closed:
                await ctx.snes_socket.close()
            return None

        return data
    finally:
        ctx.snes_request_lock.release()


async def snes_write(ctx: "SNIContext", write_list: typing.List[typing.Tuple[int, bytes]]) -> bool:
    try:
        await ctx.snes_request_lock.acquire()

        if ctx.snes_state != SNESState.SNES_ATTACHED or ctx.snes_socket is None or \
                not ctx.snes_socket.open or ctx.snes_socket.closed:
            return False

        PutAddress_Request: SNESRequest = {"Opcode": "PutAddress", "Operands": [], 'Space': 'SNES'}
        try:
            for address, data in write_list:
                PutAddress_Request['Operands'] = [hex(address)[2:], hex(len(data))[2:]]
                if ctx.snes_socket is not None:
                    await ctx.snes_socket.send(dumps(PutAddress_Request))
                    await ctx.snes_socket.send(data)
                else:
                    snes_logger.warning(f"Could not send data to SNES: {data}")
        except ConnectionClosed:
            return False

        return True
    finally:
        ctx.snes_request_lock.release()


def snes_buffered_write(ctx: "SNIContext", address: int, data: bytes) -> None:
    if ctx.snes_write_buffer and (ctx.snes_write_buffer[-1][0] + len(ctx.snes_write_buffer[-1][1])) == address:
        # append to existing write command, bundling them
        ctx.snes_write_buffer[-1] = (ctx.snes_write_buffer[-1][0], ctx.snes_write_buffer[-1][1] + data)
    else:
        ctx.snes_write_buffer.append((address, data))


async def snes_flush_writes(ctx: "SNIContext") -> None:
    if not ctx.snes_write_buffer:
        return

    # swap buffers
    ctx.snes_write_buffer, writes = [], ctx.snes_write_buffer
    await snes_write(ctx, writes)
