import binascii
import io
import json
import sys
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

from .. import Q1World
from ..id import local_id
from ..items import all_items
from ..levels import all_eps_incl_special, all_levels_incl_special

BASE_DIR = Path(__file__).parent.parent


DEPENDENCIES = [BASE_DIR / "resources" / "ap_config.json"]

ID_MAP = BASE_DIR / "resources" / "id_map.json"


def update_ids():
    sprite_id_idx = 1
    secret_id_idx = 11000
    exit_id_idx = 10000

    all_ids = {"locations": {}, "items": {}}
    all_uuids = {"locations": {}}
    for level in all_levels_incl_special:
        for location in level.locations.values():
            loc_id = -1
            if (
                "item_" in location.classname
                or "weapon_" in location.classname
                or location.classname == "all_kills"
            ):
                loc_id = sprite_id_idx
                sprite_id_idx += 1
            elif location.classname == "trigger_secret":
                loc_id = secret_id_idx
                secret_id_idx += 1
            elif location.classname == "trigger_changelevel":
                loc_id = exit_id_idx
                exit_id_idx += 1
            if loc_id > 0:
                all_ids["locations"][location.name] = loc_id
                all_uuids["locations"][location.name] = location.uuid
    for item in all_items.values():
        all_ids["items"][item.name] = local_id(item.ap_id)

    checksum = sha256()
    checksum.update(json.dumps(all_ids, indent=None).encode("utf-8"))
    all_ids["checksum"] = checksum.hexdigest()

    with io.open(ID_MAP, "w") as out_file:
        out_file.write(json.dumps(all_ids, indent=2))

    return all_ids, all_uuids


def generate_ap_config(all_ids: dict, all_uuids: dict):
    ap_config = {
        "game": Q1World.game,
        "name": Q1World.game_full_name,
        "game_id": Q1World.game_id,
        "checksum": all_ids["checksum"],
        "episodes": {},
        "locations": {},
        "items": {},
    }

    ep_count = 0

    # level metadata
    for episode in all_eps_incl_special:
        ep_count += 1
        episode_data = {
            "name": episode.name,
            "levels": {},
        }
        for level in episode.levels:
            episode_data["levels"][level.prefix] = {
                "name": level.name,
                "mapfile": level.mapfile,
                "unlock": local_id(all_items[level.unlock].ap_id),
                "boss": level.has_boss,
            }
            level_locations = {"items": {}, "secrets": {}, "exits": {}}
            for location in sorted(level.locations.values(), key=lambda x: x.game_id):
                short_name = location.name[len(level.prefix) + 1 :]
                if (
                    "item_" in location.classname
                    or "weapon_" in location.classname
                    or location.classname == "all_kills"
                ):
                    category = "items"
                elif "trigger_secret" == location.classname:
                    category = "secrets"
                elif "trigger_changelevel" == location.classname:
                    category = "exits"
                level_locations[category][str(location.game_id)] = {
                    "id": local_id(all_ids["locations"][location.name]),
                    "uuid": ""
                    + str(all_uuids["locations"][location.name])
                    + "",  # string format for jansson lib in C
                    "name": short_name,
                }
            ap_config["locations"][level.prefix] = level_locations

        ap_config["episodes"][f"e{ep_count}"] = episode_data

    # items
    for item in sorted(all_items.values(), key=lambda x: x.ap_id):
        item_data = {
            "name": item.name,
            "type": item.type,
        }
        if item.persistent:
            item_data["persistent"] = True
        if item.unique:
            item_data["unique"] = True
        if item.silent:
            item_data["silent"] = True
        item_data.update(**item.props)

        ap_config["items"][str(local_id(item.ap_id))] = item_data

    with io.open(BASE_DIR / "resources" / "ap_config.json", "w") as out_file:
        out_file.write(json.dumps(ap_config, indent=2))


def bundle_data(target: Path):
    # update ids for consistency
    all_ids, all_uuids = update_ids()
    generate_ap_config(all_ids, all_uuids)


# python -m worlds.quake.utils.bundle_data
# run as -m worlds.quake.utils.bundle_data from Archipelago root dir for imports to work
# Can provide an output directory as command line parameter for convenience
if __name__ == "__main__":
    out_dir = BASE_DIR / "resources"
    if len(sys.argv) > 1:
        out_dir = Path(sys.argv[1])
    bundle_data(out_dir)
