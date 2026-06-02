import base64
import json
import pickle
import typing
import uuid
import zipfile
import zlib

from io import BytesIO
from flask import request, flash, redirect, url_for, session, render_template, abort
from markupsafe import Markup
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
import schema

import MultiServer
from NetUtils import GamesPackage, SlotType
from Utils import VersionException, __version__
from . import app
from .models import Seed, Room, Slot, GameDataPackage, Lobby, db, commit, flush, rollback

banned_extensions = (".sfc", ".z64", ".n64", ".nes", ".smc", ".sms", ".gb", ".gbc", ".gba")
allowed_options_extensions = (".yaml", ".json", ".yml", ".txt", ".zip")
allowed_generation_extensions = (".archipelago", ".mwgg", ".zip")

games_package_schema = schema.Schema({
    "item_name_groups": {str: [str]},
    "item_name_to_id": {str: int},
    "location_name_groups": {str: [str]},
    "location_name_to_id": {str: int},
    schema.Optional("checksum"): str,
    schema.Optional("version"): int,
})


def allowed_options(filename: str) -> bool:
    return filename.endswith(allowed_options_extensions)


def allowed_generation(filename: str) -> bool:
    return filename.endswith(allowed_generation_extensions)


def banned_file(filename: str) -> bool:
    return filename.endswith(banned_extensions)


def process_multidata(compressed_multidata, files={}):
    from worlds.AutoWorld import data_package_checksum
    game_data: GamesPackage

    decompressed_multidata = MultiServer.Context.decompress(compressed_multidata)

    slots: typing.Set[Slot] = set()
    if "datapackage" in decompressed_multidata:
        # strip datapackage from multidata, leaving only the checksums
        for game, game_data in decompressed_multidata["datapackage"].items():
            if game_data.get("checksum"):
                original_checksum = game_data.pop("checksum")
                game_data = games_package_schema.validate(game_data)
                game_data = {key: value for key, value in sorted(game_data.items())}
                game_data["checksum"] = data_package_checksum(game_data)
                if original_checksum != game_data["checksum"]:
                    raise Exception(f"Original checksum {original_checksum} != "
                                    f"calculated checksum {game_data['checksum']} "
                                    f"for game {game}.")

                decompressed_multidata["datapackage"][game] = {
                    "version": game_data.get("version", 0),
                    "checksum": game_data["checksum"],
                }
                if not GameDataPackage.get(checksum=game_data["checksum"]):
                    game_data_package = GameDataPackage(checksum=game_data["checksum"],
                                                        data=pickle.dumps(game_data))
                    try:
                        flush()  # flush game data package (may raise on duplicate checksum)
                        commit()
                    except IntegrityError:
                        rollback()
                        db.session.expunge(game_data_package)

    if "slot_info" in decompressed_multidata:
        for slot, slot_info in decompressed_multidata["slot_info"].items():
            # Ignore Player Groups (e.g. item links)
            if slot_info.type == SlotType.group:
                continue
            slots.add(Slot(data=files.get(slot, None),
                           player_name=slot_info.name,
                           player_id=slot,
                           game=slot_info.game))
        flush()  # flush slots so they get IDs

    compressed_multidata = compressed_multidata[0:1] + zlib.compress(pickle.dumps(decompressed_multidata), 9)
    return slots, compressed_multidata


def upload_zip_to_db(zfile: zipfile.ZipFile, owner=None, meta={"race": False}, sid=None):
    from worlds.Files import AutoPatchRegister
    if not owner:
        owner = session["_id"]
    infolist = zfile.infolist()
    if all(allowed_options(file.filename) or file.is_dir() for file in infolist):
        flash(Markup("Error: Your .zip file only contains options files. "
                     'Did you mean to <a href="/generate">generate a game</a>?'))
        return

    spoiler = ""
    files = {}
    multidata = None

    # Load files.
    for file in infolist:
        handler = AutoPatchRegister.get_handler(file.filename)
        if banned_file(file.filename):
            return "Uploaded data contained a rom file, which is likely to contain copyrighted material. " \
                   "Your file was deleted."

        # AP Container
        elif handler:
            data = zfile.open(file, "r").read()
            with zipfile.ZipFile(BytesIO(data)) as container:
                player = json.loads(container.open("archipelago.json").read())["player"]
            files[player] = data

        # Spoiler
        elif file.filename.endswith(".txt"):
            spoiler = zfile.open(file, "r").read().decode("utf-8-sig")

        # Multi-data
        elif file.filename.endswith(".archipelago") or file.filename.endswith(".mwgg"):
            try:
                multidata = zfile.open(file).read()
            except:
                flash("Could not load multidata. File may be corrupted or incompatible.")
                multidata = None

        # Factorio
        elif file.filename.endswith(".zip"):
            try:
                _, _, slot_id, *_ = file.filename.split('_')[0].split('-', 3)
            except ValueError:
                flash("Error: Unexpected file found in .zip: " + file.filename)
                return
            data = zfile.open(file, "r").read()
            files[int(slot_id[1:])] = data

        # All other files using the standard MultiWorld.get_out_file_name_base method
        else:
            try:
                _, _, slot_id, *_ = file.filename.split('.')[0].split('_', 3)
            except ValueError:
                flash("Error: Unexpected file found in .zip: " + file.filename)
                return
            data = zfile.open(file, "r").read()
            files[int(slot_id[1:])] = data

    # Load multi data.
    if multidata:
        slots, multidata = process_multidata(multidata, files)

        seed = Seed(multidata=multidata, spoiler=spoiler, owner=owner, meta=json.dumps(meta),
                    id=sid if sid else uuid.uuid4())
        flush()  # create seed so it gets an ID
        for slot in slots:
            slot.seed_id = seed.id
        return seed
    else:
        flash("No multidata was found in the zip file, which is required.")


@app.route("/play/host", methods=["GET", "POST"])
def uploads():
    if request.method == "POST":
        # check if the POST request has a file part.
        if "file" not in request.files:
            flash("No file part in POST request.")
        else:
            uploaded_file = request.files["file"]
            # If the user does not select file, the browser will still submit an empty string without a file name.
            if uploaded_file.filename == "":
                flash("No selected file.")
            elif uploaded_file and allowed_generation(uploaded_file.filename):
                if zipfile.is_zipfile(uploaded_file):
                    with zipfile.ZipFile(uploaded_file, "r") as zfile:
                        try:
                            res = upload_zip_to_db(zfile)
                        except VersionException:
                            flash(f"Could not load multidata. Wrong Version detected.")
                        except Exception as e:
                            flash(f"Could not load multidata. File may be corrupted or incompatible. ({e})")
                        else:
                            if isinstance(res, str):
                                return res
                            elif res:
                                commit()
                                return redirect(url_for("view_seed", seed=res.id))
                else:
                    uploaded_file.seek(0)  # offset from is_zipfile check
                    # noinspection PyBroadException
                    try:
                        multidata = uploaded_file.read()
                        slots, multidata = process_multidata(multidata)
                    except Exception as e:
                        flash(f"Could not load multidata. File may be corrupted or incompatible. ({e})")
                    else:
                        seed = Seed(multidata=multidata, owner=session["_id"])
                        flush()  # place into DB and generate IDs
                        for slot in slots:
                            slot.seed_id = seed.id
                        commit()
                        return redirect(url_for("view_seed", seed=seed.id))
            else:
                flash("Not recognized file format. Awaiting a .archipelago/.mwgg file or .zip containing one.")
    return render_template("hostGame.html", version=__version__)


@app.route('/me', methods=['GET'])
def me():
    """Dashboard overview for the current browser session."""
    from .dashboard import get_dashboard_data
    data = get_dashboard_data(session["_id"])
    if data.is_empty:
        return render_template("me_first_run.html")
    return render_template("me.html", data=data, session_key=session["_id"])


@app.route('/me/rooms', methods=['GET'])
def my_rooms():
    """Full list of all rooms owned (or co-owned) by this browser."""
    from .dashboard import classify_room
    from .ownership import list_authorized_rooms
    rooms = list_authorized_rooms(session["_id"])
    return render_template(
        "me_rooms.html",
        rooms=rooms,
        classify_room=classify_room,
        session_key=session["_id"],
    )


@app.route('/me/lobbies', methods=['GET'])
def my_lobbies():
    """Full list of all (non-closed) lobbies owned (or co-owned) by this browser."""
    from .ownership import list_authorized_lobbies
    lobbies = list_authorized_lobbies(session["_id"])
    return render_template("me_lobbies.html", lobbies=lobbies, session_key=session["_id"])


@app.route('/me/seeds', methods=['GET'])
def my_seeds():
    """Full list of all seeds owned by this browser."""
    seeds = db.session.scalars(
        select(Seed).where(Seed.owner == session["_id"])
        .order_by(Seed.creation_time.desc())
    ).all()
    return render_template("me_seeds.html", seeds=seeds)


