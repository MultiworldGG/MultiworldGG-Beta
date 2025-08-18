from BaseClasses import Region

from ..base_classes import Q1Level


class mgend(Q1Level):
    name = "Chthon's Vengeance"
    mapfile = "mgend"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Lightning (1)",
            "classname": "weapon_lightning",
            "uuid": 13822602016788061505,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Supershotgun (2)",
            "classname": "weapon_supershotgun",
            "uuid": 7591452529433359684,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Shells (3)",
            "classname": "item_shells",
            "uuid": 15920940356243296560,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Shells (4)",
            "classname": "item_shells",
            "uuid": 12465904410648982812,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Green Armor (5)",
            "classname": "item_armor1",
            "uuid": 1198171888687660249,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Large Medkit (6)",
            "classname": "item_health",
            "uuid": 2667784459812601095,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Gold Key (7)",
            "classname": "item_key2",
            "uuid": 4435571511600007897,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Silver Key (8)",
            "classname": "item_key1",
            "uuid": 16134965808906236298,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Supernailgun (9)",
            "classname": "weapon_supernailgun",
            "uuid": 5527860496783854796,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Yellow Armor (10)",
            "classname": "item_armor2",
            "uuid": 6092994750981648939,
            "mp": 0,
        },
        # kept ingame as ammo resupply for the boss fight
        # {
        #    "id": 11,
        #    "name": "Cells (11)",
        #    "classname": "item_cells",
        #    "uuid": 15823753587973952172,
        #    "mp": 0,
        # },
        {
            "id": 12,
            "name": "Large Medkit (12)",
            "classname": "item_health",
            "uuid": 3132003672884157454,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Cells (13)",
            "classname": "item_cells",
            "uuid": 13218246192230946097,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Cells (14)",
            "classname": "item_cells",
            "uuid": 16669024058842951423,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Rockets (15)",
            "classname": "item_rockets",
            "uuid": 45631114403722295,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Spikes (16)",
            "classname": "item_spikes",
            "uuid": 18256876319376116774,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Nailgun (17)",
            "classname": "weapon_nailgun",
            "uuid": 17962920585722427173,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Spikes (18)",
            "classname": "item_spikes",
            "uuid": 17477960781247985186,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Spikes (19)",
            "classname": "item_spikes",
            "uuid": 16833195903034845951,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Grenadelauncher (20)",
            "classname": "weapon_grenadelauncher",
            "uuid": 10821746923498099706,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Cells (21)",
            "classname": "item_cells",
            "uuid": 7148471757578829170,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Cells (22)",
            "classname": "item_cells",
            "uuid": 2455749603914879668,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Cells (23)",
            "classname": "item_cells",
            "uuid": 12863730798033170326,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Cells (24)",
            "classname": "item_cells",
            "uuid": 6379121949485357500,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 7093997467164386208,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Cells (26)",
            "classname": "item_cells",
            "uuid": 2441527960241703198,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Cells (27)",
            "classname": "item_cells",
            "uuid": 8597687046250691782,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Rocketlauncher (28)",
            "classname": "weapon_rocketlauncher",
            "uuid": 14198617424254563189,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Quad Damage (29)",
            "classname": "item_artifact_super_damage",
            "uuid": 2348919846617555799,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Small Medkit (30)",
            "classname": "item_health",
            "uuid": 2487139437961450781,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Large Medkit (31)",
            "classname": "item_health",
            "uuid": 2316576172828670774,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Large Medkit (32)",
            "classname": "item_health",
            "uuid": 4377449901982202885,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Spikes (33)",
            "classname": "item_spikes",
            "uuid": 9952660045281966983,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Large Medkit (34)",
            "classname": "item_health",
            "uuid": 10046081705082417679,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Shells (35)",
            "classname": "item_shells",
            "uuid": 11054508552404614886,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Shells (36)",
            "classname": "item_shells",
            "uuid": 9036768327033424313,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Rockets (37)",
            "classname": "item_rockets",
            "uuid": 17672710410396642388,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Rockets (38)",
            "classname": "item_rockets",
            "uuid": 17464897589640003626,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Large Medkit (39)",
            "classname": "item_health",
            "uuid": 344402287820573146,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Shells (40)",
            "classname": "item_shells",
            "uuid": 12494033361135578154,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Shells (41)",
            "classname": "item_shells",
            "uuid": 15295137378802918861,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Secret (42)",
            "classname": "trigger_secret",
            "uuid": 11677129214314422977,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Small Medkit (43)",
            "classname": "item_health",
            "uuid": 16673641721683842125,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Small Medkit (44)",
            "classname": "item_health",
            "uuid": 10868420216265834562,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "All Kills (45)",
            "classname": "all_kills",
            "uuid": 15154186285274240270,
            "mp": 0,
        },
    ]
    has_boss = True

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [],
        )

        past_door_area = self.region(
            "Past Door Area",
            [
                "Lightning (1)",
                "Shells (4)",
                "Shells (3)",
                "Supershotgun (2)",
                "Small Medkit (30)",
                "Cells (27)",
                "Cells (13)",
                "Large Medkit (12)",
                "Cells (14)",
                "Cells (26)",
                "Spikes (33)",
                "Rockets (15)",
                "Large Medkit (6)",
                "Grenadelauncher (20)",
                "Green Armor (5)",
                "Large Medkit (32)",
                "Cells (23)",
                "Cells (22)",
                "Cells (21)",
                "Cells (24)",
                "Large Medkit (31)",
                "Nailgun (17)",
                "Spikes (18)",
                "Spikes (19)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)

        silverkey_area = self.region(
            "Silverkey Area",
            [
                "Rocketlauncher (28)",
                "Small Medkit (43)",
                "Secret (42)",
                "Large Medkit (39)",
                "Shells (41)",
                "Shells (40)",
                "Quad Damage (29)",
                "Silver Key (8)",
            ],
        )
        self.connect(past_door_area, silverkey_area, r.thunderbolt)
        self.restrict("Rocketlauncher (28)", r.jump)
        self.restrict("Silver Key (8)", r.can_button | r.bigjump_hard)

        goldkey_area = self.region(
            "Goldkey Area",
            [
                "Silver Key (8)",
                "Yellow Armor (10)",
                "Shells (36)",
                "Shells (35)",
                "Small Medkit (44)",
                "Rockets (38)",
                "Rockets (37)",
                "Supernailgun (9)",
                "Spikes (16)",
                "Large Medkit (34)",
                "Gold Key (7)",
                "Exit",
                "All Kills (45)",
            ],
        )
        self.connect(ret, goldkey_area, r.bigjump_hard)
        self.connect(silverkey_area, goldkey_area, self.silver_key & r.can_button)

        self.restrict(
            "Exit", self.silver_key & self.gold_key & r.can_button & r.thunderbolt
        )
        self.restrict("All Kills (45)", r.difficult_combat)

        return ret
