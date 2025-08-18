from enum import IntEnum

class EntranceGroups(IntEnum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    # Areas
    HOUSE = 1 << 3
    CAVE = 2 << 3
    ISLAND = 3 << 3
    OVERWORLD = 4 << 3
    DUNGEON_ENTRANCE = 5 << 3
    BOSS = 6 << 3
    DUNGEON_ROOM = 7 << 3
    WARP_PORTAL = 8 << 3
    STAIRS = 9 << 3
    HOLES = 10 << 3
    # Bitmasks
    DIRECTION_MASK = HOUSE - 1
    AREA_MASK = ~0 << 3


OPPOSITE_ENTRANCE_GROUPS = {
    EntranceGroups.RIGHT: EntranceGroups.LEFT,
    EntranceGroups.LEFT: EntranceGroups.RIGHT,
    EntranceGroups.UP: EntranceGroups.DOWN,
    EntranceGroups.DOWN: EntranceGroups.UP,
    0: 0
}

ENTRANCE_DATA = {
    # "Name": {
    #   "return_name": str. what to call the vanilla connecting entrance that generates automatically
    #   "entrance": tuple[int, int, int], stage room entrance. If you come from entrance
    #   "exit": tuple[int, int, int], stage room entrance. What the vanilla game sends you on entering
    #   "entrance_region": str. logic region that the entrance is in
    #   "exit_region": str. logic region it leads to in
    #   "coords": tuple[int, int, int]. x, y, z. Where to place link on a continuous transition. y value is also used
    #       to differentiate transitions at different heights
    #   "extra_data": dict[str: int]. additional coordinate data for continuous boundaries, like "x_max" etc.
    #   "type": EntranceGroup. Entrance group entrance type (house, cave, sea etc)
    #   "direction": EntranceGroup. Entrance group direction
    #   "two_way": bool=True. generates a reciprocal entrance, also used for ER generation
    # }

    "Mercay SW Oshus": {
        "return_name": "Oshus House",
        "entrance": (0xB, 0, 2),
        "exit": (0xB, 0xA, 1),
        "entrance_region": "mercay sw",
        "exit_region": "mercay oshus",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "two_way": True
    },
    "Mercay SW Apricot": {
        "return_name": "Apricot House",
        "entrance": (0xB, 0x0, 3),
        "exit": (0xB, 0xB, 1),
        "entrance_region": "mercay sw",
        "exit_region": "mercay apricot",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
        "two_way": True
    },
    "Mercay SW Sword Cave": {
        "return_name": "Inside Sword Cave",
        "entrance": (0xB, 0x0, 4),
        "exit": (0xB, 0x13, 1),
        "entrance_region": "mercay sw",
        "exit_region": "mercay sword cave",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.UP,
    },
    "Mercay SW North": {
        "return_name": "Mercay NW South",
        "entrance": (0xB, 0x0, 0xFC),
        "exit": (0xB, 0x1, 0xFB),
        "coords": (-164000, -164, 16000),  # The coord that doesn't matter doesn't matter. Y level diferentiates exit
        "entrance_region": "mercay sw",
        "exit_region": "mercay nw",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
    },
    "Mercay SW East": {
        "return_name": "Mercay SE West",
        "entrance": (0xB, 0x0, 0xFD),
        "exit": (0xB, 0x3, 0xFE),
        "coords": (4780, -164, 53300),
        "entrance_region": "mercay sw bridge",
        "exit_region": "mercay se",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
    },
    "Mercay SE Milk Bar": {
        "return_name": "Inside Milk Bar",
        "entrance": (0xB, 0x3, 0x3),
        "exit": (0xB, 0xC, 0x0),
        "entrance_region": "mercay se",
        "exit_region": "mercay milk bar",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
    },
    "Mercay SE Shipyard": {
        "return_name": "Inside Shipyard",
        "entrance": (0xB, 0x3, 0x4),
        "exit": (0xB, 0xD, 0x0),
        "entrance_region": "mercay se",
        "exit_region": "mercay shipyard",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
    },
    "Mercay SE Tuzi": {
        "return_name": "Tuzi House",
        "entrance": (0xB, 0x3, 0x5),
        "exit": (0xB, 0xE, 0x0),
        "entrance_region": "mercay se",
        "exit_region": "mercay tuzi",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
    },
    "Mercay SE Treasure Teller": {
        "return_name": "Treasure Teller House",
        "entrance": (0xB, 0x3, 0x6),
        "exit": (0xB, 0xF, 0x0),
        "entrance_region": "mercay se",
        "exit_region": "mercay treasure teller",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
    },
    "Mercay SE Shop": {
        "return_name": "Inside Mercay Shop",
        "entrance": (0xB, 0x3, 0x7),
        "exit": (0xB, 0x11, 0x1),
        "entrance_region": "mercay se",
        "exit_region": "mercay shop",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
    },

    # =========== Ember Island ================
    "Ember Port House": {
        "return_name": "Inside Ember Port House",
        "entrance": (0xD, 0x0, 0x2),
        "exit": (0xD, 0xB, 0x0),
        "entrance_region": "ember port",
        "exit_region": "ember port house",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
    },
    "Ember Astrid House": {
        "return_name": "Inside Astrid House",
        "entrance": (0xD, 0x0, 0x1),
        "exit": (0xD, 0xA, 0x0),
        "entrance_region": "ember port",
        "exit_region": "ember astrid",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
    },
    "Astrid House Stairs": {
        "return_name": "Astrid Basement",
        "entrance": (0xD, 0xA, 0x1),
        "exit": (0xD, 0x14, 0x0),
        "entrance_region": "ember astrid",
        "exit_region": "ember astrid basement",
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.DOWN,
    },
    "Ember Kayo House": {
        "return_name": "Inside Kayo House",
        "entrance": (0xD, 0x0, 0x3),
        "exit": (0xD, 0xC, 0x0),
        "entrance_region": "ember port",
        "exit_region": "ember kayo",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.UP,
    },
    "Ember West Coast South": {
        "return_name": "Ember East Coast South",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, -164, 80000),
        "extra_data": {"z_min": 0},
        "entrance_region": "ember port",
        "exit_region": "ember coast east",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
    },
    "Ember West Coast North": {
        "return_name": "Ember East Coast North",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, -164, -85000),
        "extra_data": {"z_max": 0},
        "entrance_region": "ember coast north",
        "exit_region": "ember coast east",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
    },
    "Ember West Climb North": {
        "return_name": "Ember East Climb North",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, 4751, -65000),
        "extra_data": {"z_max": 0},
        "entrance_region": "ember port",
        "exit_region": "ember climb east",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
    },
    "Ember West Climb South": {
        "return_name": "Ember East Climb South",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, 4751, 50000),
        "extra_data": {"z_min": 0},
        "entrance_region": "ember climb west",
        "exit_region": "ember coast east",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
    },
    "Ember West Heights North": {
        "return_name": "Ember East Heights North",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, 9666, -50000),
        "extra_data": {"z_max": 0},
        "entrance_region": "ember climb west",
        "exit_region": "ember outside tof",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
    },
    "Ember West Heights South": {
        "return_name": "Ember East Heights South",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, 9666, 25000),
        "extra_data": {"z_min": 0},
        "entrance_region": "ember summit west",
        "exit_region": "ember outside tof",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
    },
    "Ember West Summit North": {
        "return_name": "Ember East Summit North",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, 14582, -35000),
        "extra_data": {"z_max": 0},
        "entrance_region": "ember summit west",
        "exit_region": "ember summit north",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
    },
    "Ember West Summit South": {
        "return_name": "Ember East Summit South",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, 14582, 8000),
        "extra_data": {"z_min": 0},
        "entrance_region": "ember summit west",
        "exit_region": "ember summit east",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
    },

    # "Mercay SE -> Mercay NE": {
    #     "entrance": (0xB, 0x3, 0x7),
    #     "exit": (0xB, 0x11, 0x1),
    #     "two_way": True
    # },
    # "Mercay NE -> Freedle Tunnel": {
    #     "entrance": (0xB, 0x2, 0x2),
    #     "exit": (0xB, 0x12, 0x3),
    #     "two_way": True
    # },
    # "Freedle Island -> Freedle Tunnel": {
    #     "entrance": (0xB, 0x2, 0x3),
    #     "exit": (0xB, 0x12, 0x2),
    #     "two_way": True
    # },
    # "Mercay NE -> Mercay NE": {
    #     "entrance": (0xB, 0x3, 0x7),
    #     "exit": (0xB, 0x11, 0x1),
    #     "two_way": True
    # },


}

OPPOSITES = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left"
}

ENTRANCES = {}
counter = {}
i = 0
for name, data in ENTRANCE_DATA.items():
    ENTRANCES[name] = data
    ENTRANCES[name]["id"] = i
    # print(f"{i} {ENTRANCES[name]['entrance_region']} -> {ENTRANCES[name]['exit_region']}")
    i += 1
    point = data["entrance_region"] + "<=>" + data ["exit_region"]
    counter.setdefault(point, 0)
    counter[point] += 1

    if data.get("two_way", True):
        reverse_name = data.get("return_name", f"Unnamed Entrance {i}")
        reverse_data = {
            "entrance_region": data.get("reverse_exit_region", data["exit_region"]),
            "exit_region": data.get("reverse_entrance_region", data["entrance_region"]),
            "id": i,
            "entrance": data["exit"],
            "exit": data["entrance"],
            "two_way": True,
            "type": data["type"],
            "direction": OPPOSITE_ENTRANCE_GROUPS[data["direction"]],
            "coords": data.get("coords", None),
        }
        if "extra_data" in data:
            reverse_data["extra_data"] = data["extra_data"]
        ENTRANCES[reverse_name] = reverse_data
        # print(f"{i} {ENTRANCES[reverse_name]['entrance_region']} -> {ENTRANCES[reverse_name]['exit_region']}")
        i += 1
        point = reverse_data["entrance_region"] + "<=>" + reverse_data["exit_region"]
        counter.setdefault(point, 0)
        counter[point] += 1


print({key: value for key, value in counter.items() if value != 1})



if __name__ == "__main__":
    for name, data in ENTRANCES.items():
        print(f"{name}:", "{")
        for k, v in data.items():
            print(f"\t{k}: {v}")
        print("},")
