from BaseClasses import Region

from ..base_classes import Q1Level


class e5m5(Q1Level):
    name = "The Stronghold"
    mapfile = "e5m5"
    keys = ["Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Small Medkit (1)",
            "classname": "item_health",
            "uuid": 2654555341536953702,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Small Medkit (2)",
            "classname": "item_health",
            "uuid": 12923988230496946467,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Spikes (3)",
            "classname": "item_spikes",
            "uuid": 2969844355534365452,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Spikes (4)",
            "classname": "item_spikes",
            "uuid": 8860138512074434084,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Supernailgun (5)",
            "classname": "weapon_supernailgun",
            "uuid": 13582694177938030341,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Gold Key (6)",
            "classname": "item_key2",
            "uuid": 417473926965250036,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Quad Damage (7)",
            "classname": "item_artifact_super_damage",
            "uuid": 4803988662742999478,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Grenadelauncher (8)",
            "classname": "weapon_grenadelauncher",
            "uuid": 809862838605584834,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Rockets (9)",
            "classname": "item_rockets",
            "uuid": 3247609939815808285,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Invisibility (10)",
            "classname": "item_artifact_invisibility",
            "uuid": 17153515665923537025,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Supershotgun (11)",
            "classname": "weapon_supershotgun",
            "uuid": 3157274741974229804,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Shells (12)",
            "classname": "item_shells",
            "uuid": 14655519009929509273,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Secret (13)",
            "classname": "trigger_secret",
            "uuid": 14757420867161794551,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Secret (14)",
            "classname": "trigger_secret",
            "uuid": 13417557538802368419,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Nailgun (15)",
            "classname": "weapon_nailgun",
            "uuid": 9976946485779838699,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Megahealth (16)",
            "classname": "item_health",
            "uuid": 11653914085708698078,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Secret (17)",
            "classname": "trigger_secret",
            "uuid": 15110555610749312717,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Spikes (18)",
            "classname": "item_spikes",
            "uuid": 2984477170236833398,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Red Armor (19)",
            "classname": "item_armorInv",
            "uuid": 6965323355924601013,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Secret (20)",
            "classname": "trigger_secret",
            "uuid": 11816261418650202241,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Secret (21)",
            "classname": "trigger_secret",
            "uuid": 15891676896623274414,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Megahealth (22)",
            "classname": "item_health",
            "uuid": 4500194512330245052,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Rocketlauncher (23)",
            "classname": "weapon_rocketlauncher",
            "uuid": 5950445154395925451,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Shells (24)",
            "classname": "item_shells",
            "uuid": 1041153782699969841,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Spikes (25)",
            "classname": "item_spikes",
            "uuid": 12663907403942101474,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Spikes (26)",
            "classname": "item_spikes",
            "uuid": 5147339497757999156,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Shells (27)",
            "classname": "item_shells",
            "uuid": 12440428161243428677,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Lightning (28)",
            "classname": "weapon_lightning",
            "uuid": 5518088673990507122,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Rockets (29)",
            "classname": "item_rockets",
            "uuid": 14847712774584613900,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Shells (30)",
            "classname": "item_shells",
            "uuid": 354900419037926817,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Shells (31)",
            "classname": "item_shells",
            "uuid": 1907035897722584449,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Large Medkit (32)",
            "classname": "item_health",
            "uuid": 16231145985851476872,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Small Medkit (33)",
            "classname": "item_health",
            "uuid": 4258964131446550641,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Large Medkit (34)",
            "classname": "item_health",
            "uuid": 6376877898877920702,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Large Medkit (35)",
            "classname": "item_health",
            "uuid": 10165914731040261915,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Rockets (36)",
            "classname": "item_rockets",
            "uuid": 13509540510372068696,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Lightning (37)",
            "classname": "weapon_lightning",
            "uuid": 15702433399026648386,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Large Medkit (38)",
            "classname": "item_health",
            "uuid": 6000359309716396932,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 10376426750472668757,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Shells (40)",
            "classname": "item_shells",
            "uuid": 2545850152698457723,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Shells (41)",
            "classname": "item_shells",
            "uuid": 14635723233293804905,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Spikes (42)",
            "classname": "item_spikes",
            "uuid": 2355027958653609029,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Spikes (43)",
            "classname": "item_spikes",
            "uuid": 1867291428249617692,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Rockets (44)",
            "classname": "item_rockets",
            "uuid": 627804397606390664,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "All Kills (45)",
            "classname": "all_kills",
            "uuid": 3467355274774154559,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Supershotgun (11)",
                "Shells (12)",
                "Rockets (9)",
                "Grenadelauncher (8)",
            ],
        )

        past_button_area = self.region(
            "Past Button Area",
            [
                "Secret (13)",
                "Invisibility (10)",
                "Nailgun (15)",
                "Spikes (18)",
                "Rockets (29)",
                "Shells (31)",
                "Spikes (25)",
                "Spikes (26)",
                "Secret (14)",
                "Quad Damage (7)",
                "Supernailgun (5)",
                "Spikes (4)",
                "Spikes (3)",
                "Small Medkit (1)",
                "Shells (27)",
                "Secret (21)",
                "Lightning (28)",
                "Shells (30)",
                "Small Medkit (2)",
                "Secret (20)",
                "Red Armor (19)",
                "Small Medkit (33)",
                "Large Medkit (34)",
                "Gold Key (6)",
                "Rocketlauncher (23)",
                "Large Medkit (32)",
                "Megahealth (16)",
                "Secret (17)",
            ],
        )
        self.connect(ret, past_button_area, r.can_button)

        self.restrict("Secret (20)", r.can_shootswitch & r.jump)
        self.restrict("Red Armor (19)", r.can_shootswitch & r.jump)
        # item is a bit tricky to grab in water because of squished hitbox
        self.restrict("Invisibility (10)", r.can_dive | r.difficulty("medium"))

        self.restrict("Small Medkit (33)", r.can_door | r.bigjump_hard)
        self.restrict("Large Medkit (34)", r.can_door | r.bigjump_hard)
        self.restrict("Gold Key (6)", r.can_door | r.bigjump_hard)

        self.restrict("Rocketlauncher (23)", r.can_dive)
        self.restrict("Large Medkit (32)", r.can_dive)

        self.restrict("Megahealth (16)", r.can_shootswitch | r.bigjump_hard)
        self.restrict("Secret (17)", r.can_shootswitch | r.bigjump_hard)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Shells (24)",
                "Megahealth (22)",
                "Large Medkit (35)",
                "Rockets (36)",
                "Large Medkit (38)",
                "Lightning (37)",
                "Spikes (42)",
                "Spikes (43)",
                "Shells (41)",
                "Shells (40)",
                "Rockets (44)",
                "Exit",
                "All Kills (45)",
            ],
        )
        self.connect(past_button_area, past_gold_door_area, self.gold_key)

        self.restrict(
            "All Kills (45)", r.difficult_combat & (r.can_shootswitch | r.bigjump_hard)
        )

        return ret
