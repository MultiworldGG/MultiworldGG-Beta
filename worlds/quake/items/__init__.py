from typing import Dict

from ..base_classes import ItemDef
from ..id import net_id
from ..levels import all_levels_incl_special

automap_base_id = 7000
unlock_base_id = 8000
key_base_id = 9000

# Filled step by step below for readability
item_groups = {}

dynamic_level_items = {}

for level in all_levels_incl_special:
    # automap
    automap = ItemDef(
        f"{level.prefix} Automap",
        net_id(automap_base_id),
        "automap",
        {
            "mapfile": level.mapfile,
        },
        persistent=True,
        unique=True,
    )
    automap_base_id += 1
    dynamic_level_items[automap.name] = automap

    # unlock
    unlock = ItemDef(
        f"{level.prefix} Unlock",
        net_id(unlock_base_id),
        "map",
        {
            "mapfile": level.mapfile,
        },
        persistent=True,
        unique=True,
        progression=True,
    )
    unlock_base_id += 1
    dynamic_level_items[unlock.name] = unlock

    # keys
    for color in level.keys:
        if color == "Silver":
            flags = 131072
        elif color == "Gold":
            flags = 262144
        else:
            continue
        key = ItemDef(
            f"{level.prefix} {color} Key",
            net_id(key_base_id),
            "key",
            {
                "flags": flags,
                "mapfile": level.mapfile,
            },
            persistent=True,
            unique=True,
            progression=True,
        )
        key_base_id += 1
        dynamic_level_items[key.name] = key

goal_items = {
    "Exit": ItemDef(
        "Exit", net_id(100), "goal", {}, silent=True, persistent=True, progression=True
    ),
    "Secret": ItemDef(
        "Secret",
        net_id(101),
        "goal",
        {},
        silent=True,
        persistent=True,
        progression=True,
    ),
    "Boss": ItemDef(
        "Boss",
        net_id(102),
        "goal",
        {},
        silent=True,
        persistent=True,
        progression=True,
    ),
}

junk_items = {
    "Nothing": ItemDef("Nothing", net_id(0), "filler", {}, silent=True),
    "Heal (+1)": ItemDef(
        "Heal (+1)",
        net_id(403),
        "health",
        {"heal": 1, "overheal": True},
    ),
    "Armor (+1)": ItemDef(
        "Armor (+1)",
        net_id(404),
        "armor",
        {"armor": 1},
    ),
    "Shotgun Ammo (+1)": ItemDef(
        "Shotgun Ammo (+1)",
        net_id(405),
        "ammo",
        {"ammo": 1, "ammonum": 0},
    ),
    "Nail Ammo (+1)": ItemDef(
        "Nail Ammo (+1)",
        net_id(406),
        "ammo",
        {"ammo": 1, "ammonum": 1},
    ),
    "Rocket Ammo (+1)": ItemDef(
        "Rocket Ammo (+1)",
        net_id(407),
        "ammo",
        {"ammo": 1, "ammonum": 2},
    ),
    "Cell Ammo (+1)": ItemDef(
        "Cell Ammo (+1)",
        net_id(408),
        "ammo",
        {"ammo": 1, "ammonum": 3},
    ),
}

weapons = {
    "Super Shotgun": ItemDef(
        "Super Shotgun",
        net_id(201),
        "weapon",
        {"ammonum": 0, "ammo": 25, "flags": 2},
        unique=True,
        persistent=True,
    ),
    "Nailgun": ItemDef(
        "Nailgun",
        net_id(202),
        "weapon",
        {"ammonum": 1, "ammo": 20, "flags": 4},
        unique=True,
        persistent=True,
    ),
    "Super Nailgun": ItemDef(
        "Super Nailgun",
        net_id(203),
        "weapon",
        {"ammonum": 1, "ammo": 20, "flags": 8},
        unique=True,
        persistent=True,
    ),
    "Grenade Launcher": ItemDef(
        "Grenade Launcher",
        net_id(204),
        "weapon",
        {"ammonum": 2, "ammo": 5, "flags": 16},
        unique=True,
        persistent=True,
        progression=True,
    ),
    "Rocket Launcher": ItemDef(
        "Rocket Launcher",
        net_id(205),
        "weapon",
        {"ammonum": 2, "ammo": 5, "flags": 32},
        unique=True,
        persistent=True,
        progression=True,
    ),
    "Thunderbolt": ItemDef(
        "Thunderbolt",
        net_id(206),
        "weapon",
        {"ammonum": 3, "ammo": 20, "flags": 64},
        unique=True,
        persistent=True,
    ),
    # hipnotic
    "Proximity Gun": ItemDef(
        "Proximity Gun",
        net_id(207),
        "weapon",
        {"ammonum": 2, "ammo": 5, "flags": 65536},
        unique=True,
        persistent=True,
        progression=True,
    ),
    "Mjolnir": ItemDef(
        "Mjolnir",
        net_id(208),
        "weapon",
        {"ammonum": 3, "ammo": 20, "flags": 128},
        unique=True,
        persistent=True,
    ),
    "Laser Cannon": ItemDef(
        "Laser Cannon",
        net_id(209),
        "weapon",
        {"ammonum": 3, "ammo": 20, "flags": 8388608},
        unique=True,
        persistent=True,
    ),
    # rogue
    "Lava Nailgun Upgrade": ItemDef(
        "Lava Nailgun Upgrade",
        net_id(210),
        "weapon",
        {"ammonum": 4, "ammo": 20, "flags": 4096, "it2_flags": 8},
        unique=True,
        persistent=True,
    ),
    "Lava Super Nailgun Upgrade": ItemDef(
        "Lava Super Nailgun Upgrade",
        net_id(211),
        "weapon",
        {"ammonum": 4, "ammo": 20, "flags": 8192, "it2_flags": 8},
        unique=True,
        persistent=True,
    ),
    "Multi-Grenade Upgrade": ItemDef(
        "Multi-Grenade Upgrade",
        net_id(212),
        "weapon",
        {"ammonum": 5, "ammo": 5, "flags": 1638, "it2_flags": 32},
        unique=True,
        persistent=True,
    ),
    "Multi-Rocket Upgrade": ItemDef(
        "Multi-Rocket Upgrade",
        net_id(213),
        "weapon",
        {"ammonum": 5, "ammo": 5, "flags": 32768, "it2_flags": 32},
        unique=True,
        persistent=True,
    ),
    "Plasma Gun Upgrade": ItemDef(
        "Plasma Gun Upgrade",
        net_id(214),
        "weapon",
        {"ammonum": 6, "ammo": 20, "flags": 65536, "it2_flags": 16},
        unique=True,
        persistent=True,
    ),
}

progressive_weapons = {
    "Progressive Shotgun": ItemDef(
        "Progressive Shotgun",
        net_id(241),
        "progressive",
        {"items": [221]},
        silent=True,
        persistent=True,
    ),
    "Progressive Super Shotgun": ItemDef(
        "Progressive Super Shotgun",
        net_id(242),
        "progressive",
        {"items": [201, 221]},
        silent=True,
        persistent=True,
    ),
    "Progressive Nailgun": ItemDef(
        "Progressive Nailgun",
        net_id(243),
        "progressive",
        {"items": [202, 222]},
        silent=True,
        persistent=True,
    ),
    "Progressive Super Nailgun": ItemDef(
        "Progressive Super Nailgun",
        net_id(244),
        "progressive",
        {"items": [203, 222]},
        silent=True,
        persistent=True,
    ),
    "Progressive Grenade Launcher": ItemDef(
        "Progressive Grenade Launcher",
        net_id(245),
        "progressive",
        {"items": [204, 223]},
        silent=True,
        persistent=True,
        progression=True,
    ),
    "Progressive Rocket Launcher": ItemDef(
        "Progressive Rocket Launcher",
        net_id(246),
        "progressive",
        {"items": [205, 223]},
        silent=True,
        persistent=True,
        progression=True,
    ),
    "Progressive Thunderbolt": ItemDef(
        "Progressive Thunderbolt",
        net_id(247),
        "progressive",
        {"items": [206, 224]},
        silent=True,
        persistent=True,
    ),
    # hipnotic
    "Progressive Proximity Gun": ItemDef(
        "Progressive Proximity Gun",
        net_id(248),
        "progressive",
        {"items": [207, 223]},
        silent=True,
        persistent=True,
        progression=True,
    ),
    "Progressive Mjolnir": ItemDef(
        "Progressive Mjolnir",
        net_id(249),
        "progressive",
        {"items": [208, 224]},
        silent=True,
        persistent=True,
    ),
    "Progressive Laser Cannon": ItemDef(
        "Progressive Laser Cannon",
        net_id(250),
        "progressive",
        {"items": [209, 224]},
        silent=True,
        persistent=True,
    ),
    # rogue
    "Progressive Lava Nailgun Upgrade": ItemDef(
        "Progressive Lava Nailgun Upgrade",
        net_id(251),
        "progressive",
        {"items": [210, 225]},
        silent=True,
        persistent=True,
    ),
    "Progressive Lava Super Nailgun Upgrade": ItemDef(
        "Progressive Lava Super Nailgun Upgrade",
        net_id(252),
        "progressive",
        {"items": [211, 225]},
        silent=True,
        persistent=True,
    ),
    "Progressive Multi-Grenade Upgrade": ItemDef(
        "Progressive Multi-Grenade Upgrade",
        net_id(253),
        "progressive",
        {"items": [212, 226]},
        silent=True,
        persistent=True,
    ),
    "Progressive Multi-Rocket Upgrade": ItemDef(
        "Progressive Multi-Rocket Upgrade",
        net_id(254),
        "progressive",
        {"items": [213, 226]},
        silent=True,
        persistent=True,
    ),
    "Progressive Plasma Gun Upgrade": ItemDef(
        "Progressive Plasma Gun Upgrade",
        net_id(256),
        "progressive",
        {"items": [214, 227]},
        silent=True,
        persistent=True,
    ),
}

weapon_capacity = {
    "Shells Capacity": ItemDef(
        "Shells Capacity",
        net_id(221),
        "ammo",
        {"ammonum": 0, "capacity": 10, "ammo": 25},
        persistent=True,
    ),
    "Spikes Capacity": ItemDef(
        "Spikes Capacity",
        net_id(222),
        "ammo",
        {"ammonum": 1, "capacity": 20, "ammo": 20},
        persistent=True,
    ),
    "Rockets Capacity": ItemDef(
        "Rockets Capacity",
        net_id(223),
        "ammo",
        {"ammonum": 2, "capacity": 5, "ammo": 5},
        persistent=True,
    ),
    "Cells Capacity": ItemDef(
        "Cells Capacity",
        net_id(224),
        "ammo",
        {"ammonum": 3, "capacity": 20, "ammo": 20},
        persistent=True,
    ),
    "Lava Nails Capacity": ItemDef(
        "Lava Nails Capacity",
        net_id(225),
        "ammo",
        {"ammonum": 4, "capacity": 20, "ammo": 20},
        persistent=True,
    ),
    "Multi Rockets Capacity": ItemDef(
        "Multi Rockets Capacity",
        net_id(226),
        "ammo",
        {"ammonum": 5, "capacity": 5, "ammo": 5},
        persistent=True,
    ),
    "Plasma Capacity": ItemDef(
        "Plasma Capacity",
        net_id(227),
        "ammo",
        {"ammonum": 5, "capacity": 10, "ammo": 20},
        persistent=True,
    ),
}

ammo = {
    "Shells Ammo": ItemDef(
        "Shells Ammo",
        net_id(261),
        "ammo",
        {"ammonum": 0, "ammo": 25},
    ),
    "Spikes Ammo": ItemDef(
        "Spikes Ammo",
        net_id(262),
        "ammo",
        {"ammonum": 1, "ammo": 30},
    ),
    "Rockets Ammo": ItemDef(
        "Rockets Ammo",
        net_id(263),
        "ammo",
        {"ammonum": 2, "ammo": 5},
    ),
    "Cells Ammo": ItemDef(
        "Cells Ammo",
        net_id(264),
        "ammo",
        {"ammonum": 3, "ammo": 20},
    ),
    "Lava Nails Ammo": ItemDef(
        "Lava Nails Ammo",
        net_id(265),
        "ammo",
        {"ammonum": 4, "ammo": 30},
    ),
    "Multi Rockets Ammo": ItemDef(
        "Multi Rockets Ammo",
        net_id(266),
        "ammo",
        {"ammonum": 5, "ammo": 5},
    ),
    "Plasma Ammo": ItemDef(
        "Plasma Ammo",
        net_id(267),
        "ammo",
        {"ammonum": 6, "ammo": 15},
    ),
}

item_groups["Shotgun"] = {"Progressive Shotgun"}
item_groups["Super Shotgun"] = {"Super Shotgun", "Progressive Super Shotgun"}
item_groups["Nailgun"] = {"Nailgun", "Progressive Nailgun"}
item_groups["Super Nailgun"] = {"Super Nailgun", "Progressive Super Nailgun"}
item_groups["Grenade Launcher"] = {"Grenade Launcher", "Progressive Grenade Launcher"}
item_groups["Rocket Launcher"] = {"Rocket Launcher", "Progressive Rocket Launcher"}
item_groups["Thunderbolt"] = {"Thunderbolt", "Progressive Thunderbolt"}
item_groups["Proximity Gun"] = {"Proximity Gun", "Progressive Proximity Gun"}
item_groups["Mjolnir"] = {"Mjolnir", "Progressive Mjolnir"}
item_groups["Laser Cannon"] = {"Laser Cannon", "Progressive Laser Cannon"}
item_groups["Lava Nailgun Upgrade"] = {
    "Lava Nailgun Upgrade",
    "Progressive Lava Nailgun Upgrade",
}
item_groups["Lava Super Nailgun Upgrade"] = {
    "Lava Super Nailgun Upgrade",
    "Progressive Lava Super Nailgun Upgrade",
}
item_groups["Multi-Grenade Upgrade"] = {
    "Multi-Grenade Upgrade",
    "Progressive Multi-Grenade Upgrade",
}
item_groups["Multi-Rocket Upgrade"] = {
    "Multi-Rocket Upgrade",
    "Progressive Multi-Rocket Upgrade",
}
item_groups["Plasma Gun Upgrade"] = {
    "Plasma Gun Upgrade",
    "Progressive Plasma Gun Upgrade",
}

abilities = {
    "Jump": ItemDef(
        "Jump",
        net_id(350),
        "ability",
        {"enables": "jump"},
        persistent=True,
        unique=True,
        progression=True,
    ),
    "Dive": ItemDef(
        "Dive",
        net_id(351),
        "ability",
        {"enables": "dive"},
        persistent=True,
        unique=True,
        progression=True,
    ),
    "Door": ItemDef(
        "Door",
        net_id(354),
        "ability",
        {"enables": "door"},
        persistent=True,
        unique=True,
        progression=True,
    ),
    "Button": ItemDef(
        "Button",
        net_id(355),
        "ability",
        {"enables": "button"},
        persistent=True,
        unique=True,
        progression=True,
    ),
    "Shoot Switch": ItemDef(
        "Shoot Switch",
        net_id(356),
        "ability",
        {"enables": "shootswitch"},
        persistent=True,
        unique=True,
        progression=True,
    ),
    "Grenade Jump": ItemDef(
        "Grenade Jump",
        net_id(357),
        "ability",
        {"enables": "grenadejump"},
        persistent=True,
        unique=True,
        progression=True,
    ),
    "Rocket Jump": ItemDef(
        "Rocket Jump",
        net_id(358),
        "ability",
        {"enables": "rocketjump"},
        persistent=True,
        unique=True,
        progression=True,
    ),
    "Grenade Damage Remover": ItemDef(
        "Grenade Damage Remover",
        net_id(359),
        "ability",
        {"enables": "grenadedmgremover"},
        persistent=True,
        unique=True,
        progression=True,
    ),
    "Rocket Damage Remover": ItemDef(
        "Rocket Damage Remover",
        net_id(360),
        "ability",
        {"enables": "rocketdmgremover"},
        persistent=True,
        unique=True,
        progression=True,
    ),
    "Run": ItemDef(
        "Run",
        net_id(361),
        "ability",
        {"enables": "run"},
        persistent=True,
        unique=True,
        progression=True,
    ),
}

healing_items = {
    "Small Medkit": ItemDef(
        "Small Medkit",
        net_id(400),
        "inventory",
        {"invnum": 5, "capacity": 15},
        persistent=True,
        silent=True,
    ),
    "Large Medkit": ItemDef(
        "Large Medkit",
        net_id(440),
        "inventory",
        {"invnum": 5, "capacity": 25},
        persistent=True,
        silent=True,
    ),
    "Megahealth": ItemDef(
        "Megahealth",
        net_id(441),
        "inventory",
        {"invnum": 5, "capacity": 100},
        persistent=True,
        silent=True,
    ),
    "Green Armor": ItemDef(
        "Green Armor",
        net_id(442),
        "inventory",
        {"invnum": 6, "capacity": 15},
        persistent=True,
        silent=True,
    ),
    "Yellow Armor": ItemDef(
        "Yellow Armor",
        net_id(443),
        "inventory",
        {"invnum": 6, "capacity": 25},
        persistent=True,
        silent=True,
    ),
    "Red Armor": ItemDef(
        "Red Armor",
        net_id(444),
        "inventory",
        {"invnum": 6, "capacity": 100},
        persistent=True,
        silent=True,
    ),
}

inventory_items = {
    "Quad Damage": ItemDef(
        "Quad Damage",
        net_id(301),
        "inventory",
        {"invnum": 0, "capacity": 1},
        persistent=True,
        unique=True,
    ),
    "Invulnerability": ItemDef(
        "Invulnerability",
        net_id(302),
        "inventory",
        {"invnum": 1, "capacity": 1},
        persistent=True,
        unique=True,
    ),
    "Biosuit": ItemDef(
        "Biosuit",
        net_id(303),
        "inventory",
        {"invnum": 2, "capacity": 1},
        persistent=True,
        unique=True,
    ),
    "Invisibility": ItemDef(
        "Invisibility",
        net_id(304),
        "inventory",
        {"invnum": 3, "capacity": 1},
        persistent=True,
        unique=True,
    ),
    "Backpack": ItemDef(
        "Backpack",
        net_id(305),
        "inventory",
        {"invnum": 4, "capacity": 1},
        persistent=True,
        unique=True,
    ),
    # hipnotic
    # not adding wetsuit since its just a worse biosuit
    "Empathy Shields": ItemDef(
        "Empathy Shields",
        net_id(306),
        "inventory",
        {"invnum": 5, "capacity": 1},
        persistent=True,
        unique=True,
    ),
    # rogue
    "Power Shield": ItemDef(
        "Power Shield",
        net_id(307),
        "inventory",
        {"invnum": 6, "capacity": 1},
        persistent=True,
        unique=True,
    ),
    "Anti-Grav Belt": ItemDef(
        "Anti-Grav Belt",
        net_id(307),
        "inventory",
        {"invnum": 7, "capacity": 1},
        persistent=True,
        unique=True,
    ),
}

inventory_items_capacity = {
    "Quad Damage Capacity": ItemDef(
        "Quad Damage Capacity",
        net_id(321),
        "invcapacity",
        {"invnum": 0, "capacity": 1},
        persistent=True,
    ),
    "Invulnerability Capacity": ItemDef(
        "Invulnerability Capacity",
        net_id(322),
        "invcapacity",
        {"invnum": 1, "capacity": 1},
        persistent=True,
    ),
    "Biosuit Capacity": ItemDef(
        "Biosuit Capacity",
        net_id(323),
        "invcapacity",
        {"invnum": 2, "capacity": 1},
        persistent=True,
    ),
    "Invisibility Capacity": ItemDef(
        "Invisibility Capacity",
        net_id(324),
        "invcapacity",
        {"invnum": 3, "capacity": 1},
        persistent=True,
    ),
    "Backpack Capacity": ItemDef(
        "Backpack Capacity",
        net_id(325),
        "invcapacity",
        {"invnum": 4, "capacity": 1},
        persistent=True,
    ),
    "Empathy Shields Capacity": ItemDef(
        "Empathy Shields Capacity",
        net_id(326),
        "invcapacity",
        {"invnum": 5, "capacity": 1},
        persistent=True,
    ),
    "Power Shield Capacity": ItemDef(
        "Power Shield Capacity",
        net_id(327),
        "invcapacity",
        {"invnum": 6, "capacity": 1},
        persistent=True,
    ),
    "Anti-Grav Belt Capacity": ItemDef(
        "Anti-Grav Belt Capacity",
        net_id(328),
        "invcapacity",
        {"invnum": 7, "capacity": 1},
        persistent=True,
    ),
}

inventory_items_progressive = {
    "Progressive Quad Damage": ItemDef(
        "Progressive Quad Damage",
        net_id(341),
        "progressive",
        {"items": [301, 321]},
        persistent=True,
        silent=True,
    ),
    "Progressive Invulnerability": ItemDef(
        "Progressive Invulnerability",
        net_id(342),
        "progressive",
        {"items": [302, 322]},
        persistent=True,
        silent=True,
    ),
    "Progressive Biosuit": ItemDef(
        "Progressive Biosuit",
        net_id(343),
        "progressive",
        {"items": [303, 323]},
        persistent=True,
        silent=True,
    ),
    "Progressive Invisibility": ItemDef(
        "Progressive Invisibility",
        net_id(344),
        "progressive",
        {"items": [304, 324]},
        persistent=True,
        silent=True,
    ),
    "Progressive Backpack": ItemDef(
        "Progressive Backpack",
        net_id(345),
        "progressive",
        {"items": [305, 325]},
        persistent=True,
        silent=True,
    ),
    "Progressive Empathy Shields": ItemDef(
        "Progressive Empathy Shields",
        net_id(346),
        "progressive",
        {"items": [306, 326]},
        persistent=True,
        silent=True,
    ),
    "Progressive Power Shield": ItemDef(
        "Progressive Power Shield",
        net_id(347),
        "progressive",
        {"items": [307, 327]},
        persistent=True,
        silent=True,
    ),
    "Progressive Anti-Grav Belt": ItemDef(
        "Progressive Anti-Grav Belt",
        net_id(348),
        "progressive",
        {"items": [308, 328]},
        persistent=True,
        silent=True,
    ),
}

item_groups["Biosuit"] = {"Biosuit", "Progressive Biosuit"}
item_groups["Biosuit Capacity"] = {"Biosuit", "Biosuit Capacity", "Progressive Biosuit"}
item_groups["Quad Damage"] = {"Quad Damage", "Progressive Quad Damage"}
item_groups["Quad Damage Capacity"] = {
    "Quad Damage",
    "Quad Damage Capacity",
    "Progressive Quad Damage",
}
item_groups["Invulnerability"] = {"Invulnerability", "Progressive Invulnerability"}
item_groups["Invulnerability Capacity"] = {
    "Invulnerability",
    "Invulnerability Capacity",
    "Progressive Invulnerability",
}
item_groups["Invisibility"] = {"Invisibility", "Progressive Invisibility"}
item_groups["Invisibility Capacity"] = {
    "Invisibility",
    "Invisibility Capacity",
    "Progressive Invisibility",
}
item_groups["Backpack"] = {"Backpack", "Progressive Backpack"}
item_groups["Backpack Capacity"] = {
    "Backpack",
    "Backpack Capacity",
    "Progressive Backpack",
}
item_groups["Empathy Shields"] = {"Empathy Shields", "Progressive Empathy Shields"}
item_groups["Empathy Shields Capacity"] = {
    "Empathy Shields",
    "Empathy Shields Capacity",
    "Progressive Empathy Shields",
}
item_groups["Power Shield"] = {"Power Shield", "Progressive Power Shield"}
item_groups["Power Shield Capacity"] = {
    "Power Shield",
    "Power Shield Capacity",
    "Progressive Power Shield",
}
item_groups["Anti-Grav Belt"] = {"Anti-Grav Belt", "Progressive Anti-Grav Belt"}
item_groups["Anti-Grav Belt Capacity"] = {
    "Anti-Grav Belt",
    "Anti-Grav Belt Capacity",
    "Progressive Anti-Grav Belt",
}

traps = {
    "Low Health Trap": ItemDef(
        "Low Health Trap",
        net_id(500),
        "trap",
        {"trap": "lowhealth", "duration": 1, "grace": 2000},
        silent=True,
    ),
    "Death Trap": ItemDef(
        "Death Trap",
        net_id(501),
        "trap",
        {"trap": "death", "duration": 1, "grace": 5000},
        silent=True,
    ),
    "Mouse Trap": ItemDef(
        "Mouse Trap",
        net_id(503),
        "trap",
        {"trap": "mouse", "duration": 500, "grace": 2000},
        silent=True,
    ),
    "Sound Trap": ItemDef(
        "Sound Trap",
        net_id(504),
        "trap",
        {"trap": "sound", "duration": 3000, "grace": 1000},
        silent=True,
    ),
    "Jump Trap": ItemDef(
        "Jump Trap",
        net_id(505),
        "trap",
        {"trap": "jump", "duration": 500, "grace": 1000},
        silent=True,
    ),
}

# These don't have defined values and exist solely to be replaced by unique, seed specifically generated items
dynamic_items = {
    f"Dynamic{i +1}": ItemDef(
        f"Dynamic{i + 1}", net_id(600 + i), "filler", {}, silent=True
    )
    for i in range(16)
}

all_items: Dict[str, ItemDef] = {
    **junk_items,
    **goal_items,
    **weapons,
    **progressive_weapons,
    **weapon_capacity,
    **ammo,
    **healing_items,
    **inventory_items,
    **inventory_items_capacity,
    **inventory_items_progressive,
    **abilities,
    **dynamic_level_items,
    **traps,
    **dynamic_items,
}
