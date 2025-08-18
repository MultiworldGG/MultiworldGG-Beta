from BaseClasses import Region

from ..base_classes import Q1Level


class e3m7(Q1Level):
    name = "The Haunted Halls"
    mapfile = "e3m7"
    keys = []
    location_defs = [
        {
            "id": 1,
            "name": "Large Medkit (1)",
            "classname": "item_health",
            "uuid": 11901520713837945107,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Large Medkit (2)",
            "classname": "item_health",
            "uuid": 9465373970763202595,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Large Medkit (3)",
            "classname": "item_health",
            "uuid": 4617924921444702371,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Weapon (4)",
            "classname": "item_weapon",
            "uuid": 8875018162710681652,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Weapon (5)",
            "classname": "item_weapon",
            "uuid": 6951118436176888017,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Large Medkit (6)",
            "classname": "item_health",
            "uuid": 8360408649232062023,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Large Medkit (7)",
            "classname": "item_health",
            "uuid": 9870866661613795481,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Large Medkit (8)",
            "classname": "item_health",
            "uuid": 12650868724615134627,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Small Medkit (9)",
            "classname": "item_health",
            "uuid": 17968280644885273436,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Small Medkit (10)",
            "classname": "item_health",
            "uuid": 9925091497873180367,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Weapon (11)",
            "classname": "item_weapon",
            "uuid": 13212639067037365368,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Yellow Armor (12)",
            "classname": "item_armor2",
            "uuid": 16762884923998532781,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Green Armor (13)",
            "classname": "item_armor1",
            "uuid": 3953579477592876671,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Spikes (14)",
            "classname": "item_spikes",
            "uuid": 16643234981793415537,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Nailgun (15)",
            "classname": "weapon_nailgun",
            "uuid": 11533385447242450834,
            "mp": 1,
        },
        {
            "id": 16,
            "name": "Rockets (16)",
            "classname": "item_rockets",
            "uuid": 3197927588568078996,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Rockets (17)",
            "classname": "item_rockets",
            "uuid": 13768579247816539409,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Quad Damage (18)",
            "classname": "item_artifact_super_damage",
            "uuid": 10161959582474454233,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Large Medkit (19)",
            "classname": "item_health",
            "uuid": 7767363031194599668,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Spikes (20)",
            "classname": "item_spikes",
            "uuid": 13428598664325544397,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Secret (21)",
            "classname": "trigger_secret",
            "uuid": 3934671998298599287,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Megahealth (22)",
            "classname": "item_health",
            "uuid": 1482651260900495293,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Quad Damage (23)",
            "classname": "item_artifact_super_damage",
            "uuid": 14336716642286049185,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Yellow Armor (24)",
            "classname": "item_armor2",
            "uuid": 8625233387322397664,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Secret (25)",
            "classname": "trigger_secret",
            "uuid": 18322982498659681858,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Spikes (26)",
            "classname": "item_spikes",
            "uuid": 11571718073759022815,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Invulnerability (27)",
            "classname": "item_artifact_invulnerability",
            "uuid": 15231488414585621908,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Secret (28)",
            "classname": "trigger_secret",
            "uuid": 8311352378447307988,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Large Medkit (29)",
            "classname": "item_health",
            "uuid": 11368138413219290565,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Large Medkit (30)",
            "classname": "item_health",
            "uuid": 15291935840123276789,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Spikes (31)",
            "classname": "item_spikes",
            "uuid": 1934572513757242487,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Rockets (32)",
            "classname": "item_rockets",
            "uuid": 11648715796089165473,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Shells (33)",
            "classname": "item_shells",
            "uuid": 1663918759079789138,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Small Medkit (34)",
            "classname": "item_health",
            "uuid": 3747850309465215847,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Megahealth (35)",
            "classname": "item_health",
            "uuid": 1023212809738744681,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Secret (36)",
            "classname": "trigger_secret",
            "uuid": 7625507360964036013,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Small Medkit (37)",
            "classname": "item_health",
            "uuid": 3648824967125431931,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Large Medkit (38)",
            "classname": "item_health",
            "uuid": 900000167610513783,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Spikes (39)",
            "classname": "item_spikes",
            "uuid": 14935314249063290672,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Large Medkit (40)",
            "classname": "item_health",
            "uuid": 18435361941374421295,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Small Medkit (41)",
            "classname": "item_health",
            "uuid": 17989864294412981216,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 10509471012750371316,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Rocketlauncher (43)",
            "classname": "weapon_rocketlauncher",
            "uuid": 14904681572583979497,
            "mp": 1,
        },
        {
            "id": 44,
            "name": "Invisibility (44)",
            "classname": "item_artifact_invisibility",
            "uuid": 5317022215721583761,
            "mp": 1,
        },
        {
            "id": 45,
            "name": "Red Armor (45)",
            "classname": "item_armorInv",
            "uuid": 13188961613657897903,
            "mp": 1,
        },
        {
            "id": 46,
            "name": "Supernailgun (46)",
            "classname": "weapon_supernailgun",
            "uuid": 6109718645847982808,
            "mp": 1,
        },
        {
            "id": 47,
            "name": "Grenadelauncher (47)",
            "classname": "weapon_grenadelauncher",
            "uuid": 14612795282076537145,
            "mp": 1,
        },
        {
            "id": 48,
            "name": "Rockets (48)",
            "classname": "item_rockets",
            "uuid": 6121847805105433834,
            "mp": 1,
        },
        {
            "id": 49,
            "name": "Rocketlauncher (49)",
            "classname": "weapon_rocketlauncher",
            "uuid": 2498169379708619563,
            "mp": 1,
        },
        {
            "id": 50,
            "name": "All Kills (50)",
            "classname": "all_kills",
            "uuid": 8808661641529010137,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Large Medkit (1)",
                "Large Medkit (2)",
                "Rockets (16)",
                "Weapon (11)",
                "Supernailgun (46)",
                "Green Armor (13)",
            ],
        )

        past_door_area = self.region(
            "Past Door",
            [
                "Rockets (17)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)

        past_button_area = self.region(
            "Past Button",
            [
                "Nailgun (15)",
                "Spikes (14)",
                "Large Medkit (6)",
                "Large Medkit (7)",
                "Small Medkit (9)",
                "Small Medkit (10)",
                "Weapon (5)",
                "Rockets (48)",
                "Grenadelauncher (47)",
            ],
        )
        self.connect(
            past_door_area,
            past_button_area,
            r.can_button | (r.can_rj_hard & r.can_jump),
        )

        self.restrict("Nailgun (15)", r.can_button)
        self.restrict("Spikes (14)", r.can_button)

        past_second_button_area = self.region(
            "Past Second Button",
            [
                "Secret (28)",
                "Quad Damage (18)",
                "Weapon (4)",
                "Yellow Armor (12)",
                "Small Medkit (34)",
                "Spikes (31)",
                "Shells (33)",
                "Rocketlauncher (49)",
                "Rockets (32)",
                "Large Medkit (8)",
                "Large Medkit (30)",
                "Large Medkit (38)",
                "Small Medkit (37)",
                "Spikes (39)",
                "Secret (36)",
                "Megahealth (35)",
            ],
        )
        self.connect(past_button_area, past_second_button_area, r.can_button)

        self.restrict("Secret (28)", r.can_shootswitch)
        self.restrict("Quad Damage (18)", r.can_shootswitch)

        past_shootswitch_area = self.region(
            "Past Shootswitch",
            [
                "Large Medkit (3)",
                "Large Medkit (19)",
                "Spikes (20)",
                "Red Armor (45)",
                "Large Medkit (29)",
                "Secret (21)",
                "Yellow Armor (24)",
                "Quad Damage (23)",
                "Megahealth (22)",
                "Rocketlauncher (43)",
                "Large Medkit (40)",
                "Small Medkit (41)",
                "Invisibility (44)",
                "Secret (25)",
                "Spikes (26)",
                "Invulnerability (27)",
                "Exit",
                "All Kills (50)",
            ],
        )
        self.connect(past_second_button_area, past_shootswitch_area, r.can_shootswitch)

        self.restrict("All Kills (50)", r.difficult_combat)

        return ret
