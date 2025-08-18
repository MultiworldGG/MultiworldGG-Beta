from BaseClasses import Region

from ..base_classes import Q1Level


class hipstart(Q1Level):
    name = "Command HQ"
    mapfile = "start_hipnotic"
    keys = []
    location_defs = [
        {
            "id": 1,
            "name": "Invulnerability (1)",
            "classname": "item_artifact_invulnerability",
            "uuid": 9087739236899698575,
            "mp": 1,
        },
        # {
        #    "id": 2,
        #    "name": "Exit",
        #    "classname": "trigger_changelevel",
        #    "uuid": 16053576832577788024,
        #    "mp": 0,
        # },
        # {
        #    "id": 3,
        #    "name": "Exit",
        #    "classname": "trigger_changelevel",
        #    "uuid": 909804445490971279,
        #    "mp": 0,
        # },
        # {
        #    "id": 4,
        #    "name": "Exit",
        #    "classname": "trigger_changelevel",
        #    "uuid": 16717283616145769957,
        #    "mp": 0,
        # },
        {
            "id": 5,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 13977961920456529443,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Large Medkit (6)",
            "classname": "item_health",
            "uuid": 17475921339755820592,
            "mp": 1,
        },
        {
            "id": 7,
            "name": "Large Medkit (7)",
            "classname": "item_health",
            "uuid": 12595543790744276088,
            "mp": 1,
        },
        {
            "id": 8,
            "name": "Supershotgun (8)",
            "classname": "weapon_supershotgun",
            "uuid": 15529027862457137038,
            "mp": 1,
        },
        {
            "id": 9,
            "name": "Rockets (9)",
            "classname": "item_rockets",
            "uuid": 6169261905948995870,
            "mp": 1,
        },
        {
            "id": 10,
            "name": "Small Medkit (10)",
            "classname": "item_health",
            "uuid": 4306893707955004470,
            "mp": 1,
        },
        {
            "id": 11,
            "name": "Laser (11)",
            "classname": "weapon_laser_gun",
            "uuid": 843505240306592622,
            "mp": 1,
        },
        {
            "id": 12,
            "name": "Small Medkit (12)",
            "classname": "item_health",
            "uuid": 13318753610608797397,
            "mp": 1,
        },
        {
            "id": 13,
            "name": "Small Medkit (13)",
            "classname": "item_health",
            "uuid": 15886729002238892108,
            "mp": 1,
        },
        {
            "id": 14,
            "name": "Cells (14)",
            "classname": "item_cells",
            "uuid": 9643275365833731522,
            "mp": 1,
        },
        {
            "id": 15,
            "name": "Cells (15)",
            "classname": "item_cells",
            "uuid": 3697981220509081772,
            "mp": 1,
        },
        {
            "id": 16,
            "name": "Grenadelauncher (16)",
            "classname": "weapon_grenadelauncher",
            "uuid": 4055992907454758878,
            "mp": 1,
        },
        {
            "id": 17,
            "name": "Spikes (17)",
            "classname": "item_spikes",
            "uuid": 4141573951906522486,
            "mp": 1,
        },
        {
            "id": 18,
            "name": "Rocketlauncher (18)",
            "classname": "weapon_rocketlauncher",
            "uuid": 7050129856728800891,
            "mp": 1,
        },
        {
            "id": 19,
            "name": "Megahealth (19)",
            "classname": "item_health",
            "uuid": 17458890134333750303,
            "mp": 1,
        },
        {
            "id": 20,
            "name": "Yellow Armor (20)",
            "classname": "item_armor2",
            "uuid": 11213318331853846765,
            "mp": 1,
        },
        {
            "id": 21,
            "name": "Nailgun (21)",
            "classname": "weapon_nailgun",
            "uuid": 1126259712343732975,
            "mp": 1,
        },
        {
            "id": 22,
            "name": "Spikes (22)",
            "classname": "item_spikes",
            "uuid": 18219324083986871708,
            "mp": 1,
        },
        {
            "id": 23,
            "name": "Spikes (23)",
            "classname": "item_spikes",
            "uuid": 1748937938863599675,
            "mp": 1,
        },
        {
            "id": 24,
            "name": "Red Armor (24)",
            "classname": "item_armorInv",
            "uuid": 14582791156761296780,
            "mp": 1,
        },
        {
            "id": 25,
            "name": "Supernailgun (25)",
            "classname": "weapon_supernailgun",
            "uuid": 12887335575265402198,
            "mp": 1,
        },
        {
            "id": 26,
            "name": "Rockets (26)",
            "classname": "item_rockets",
            "uuid": 18386395306397043037,
            "mp": 1,
        },
        {
            "id": 27,
            "name": "Invisibility (27)",
            "classname": "item_artifact_invisibility",
            "uuid": 10583421165234077513,
            "mp": 1,
        },
        {
            "id": 28,
            "name": "Supershotgun (28)",
            "classname": "weapon_supershotgun",
            "uuid": 4027730287064940411,
            "mp": 1,
        },
        {
            "id": 29,
            "name": "Large Medkit (29)",
            "classname": "item_health",
            "uuid": 7868834874188037283,
            "mp": 1,
        },
        {
            "id": 30,
            "name": "Lightning (30)",
            "classname": "weapon_lightning",
            "uuid": 15057291659018730239,
            "mp": 1,
        },
        {
            "id": 31,
            "name": "Cells (31)",
            "classname": "item_cells",
            "uuid": 71450614157453269,
            "mp": 1,
        },
        {
            "id": 32,
            "name": "Cells (32)",
            "classname": "item_cells",
            "uuid": 14834293400783687661,
            "mp": 1,
        },
        {
            "id": 33,
            "name": "Mjolnir (33)",
            "classname": "weapon_mjolnir",
            "uuid": 414287501019648404,
            "mp": 1,
        },
        {
            "id": 34,
            "name": "Shells (34)",
            "classname": "item_shells",
            "uuid": 11283523662737126834,
            "mp": 1,
        },
        {
            "id": 35,
            "name": "Quad Damage (35)",
            "classname": "item_artifact_super_damage",
            "uuid": 5278044135772777960,
            "mp": 1,
        },
        {
            "id": 36,
            "name": "Rockets (36)",
            "classname": "item_rockets",
            "uuid": 13215005602727812580,
            "mp": 1,
        },
        {
            "id": 37,
            "name": "Rockets (37)",
            "classname": "item_rockets",
            "uuid": 7835964102771888836,
            "mp": 1,
        },
        {
            "id": 38,
            "name": "Green Armor (38)",
            "classname": "item_armor1",
            "uuid": 8016563392480693273,
            "mp": 1,
        },
        {
            "id": 39,
            "name": "Proximity (39)",
            "classname": "weapon_proximity_gun",
            "uuid": 3764682109272616997,
            "mp": 1,
        },
        {
            "id": 40,
            "name": "Rockets (40)",
            "classname": "item_rockets",
            "uuid": 5064053332081622005,
            "mp": 1,
        },
        {
            "id": 41,
            "name": "Megahealth (41)",
            "classname": "item_health",
            "uuid": 224364119275418085,
            "mp": 1,
        },
        {
            "id": 42,
            "name": "All Kills (42)",
            "classname": "all_kills",
            "uuid": 11891092947304516721,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Large Medkit (6)",
                "Supershotgun (8)",
                "Large Medkit (7)",
                "All Kills (42)",
            ],
        )

        past_button_area = self.region(
            "Past Button Area",
            [
                "Spikes (17)",
                "Shells (34)",
                "Mjolnir (33)",
                "Megahealth (41)",
                "Large Medkit (29)",
                "Supershotgun (28)",
                "Supernailgun (25)",
                "Rockets (26)",
                "Megahealth (19)",
                "Rocketlauncher (18)",
                "Yellow Armor (20)",
                "Nailgun (21)",
                "Spikes (23)",
                "Spikes (22)",
                "Lightning (30)",
                "Cells (32)",
                "Cells (31)",
                "Red Armor (24)",
                "Invisibility (27)",
            ],
        )
        self.connect(ret, past_button_area, r.can_button)
        self.restrict("Red Armor (24)", r.jump)
        self.restrict("Invisibility (27)", r.jump)

        hard_area = self.region(
            "Hard Area",
            [
                "Cells (14)",
                "Cells (15)",
                "Laser (11)",
                "Small Medkit (13)",
                "Small Medkit (12)",
                "Invulnerability (1)",
                "Exit",
            ],
        )
        self.connect(ret, hard_area, r.jump)

        nightmare_area = self.region(
            "Nightmare Area",
            [
                "Quad Damage (35)",
                "Rockets (37)",
                "Rockets (36)",
                "Green Armor (38)",
                "Small Medkit (10)",
                "Grenadelauncher (16)",
                "Rockets (9)",
                "Rockets (40)",
            ],
        )
        # can clip up boxes with auto-step to get to nightmare area
        # hard diff because obscure
        self.connect(past_button_area, nightmare_area, r.jump | r.difficulty("hard"))

        return ret
