from BaseClasses import Region

from ..base_classes import Q1Level


class hip1m1(Q1Level):
    name = "The Pumping Station"
    mapfile = "hip1m1"
    keys = ["Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Secret (1)",
            "classname": "trigger_secret",
            "uuid": 8230029439015093384,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Gold Key (2)",
            "classname": "item_key2",
            "uuid": 13103771360232164771,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Secret (3)",
            "classname": "trigger_secret",
            "uuid": 4568347580286040740,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 1996496533729685934,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Supershotgun (5)",
            "classname": "weapon_supershotgun",
            "uuid": 14977783749578525480,
            "mp": 1,
        },
        {
            "id": 6,
            "name": "Nailgun (6)",
            "classname": "weapon_nailgun",
            "uuid": 13341618192329118100,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Laser (7)",
            "classname": "weapon_laser_gun",
            "uuid": 16596965427228176586,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Supernailgun (8)",
            "classname": "weapon_supernailgun",
            "uuid": 12266385763991799312,
            "mp": 1,
        },
        {
            "id": 9,
            "name": "Grenadelauncher (9)",
            "classname": "weapon_grenadelauncher",
            "uuid": 9363854272598932201,
            "mp": 1,
        },
        {
            "id": 10,
            "name": "Nailgun (10)",
            "classname": "weapon_nailgun",
            "uuid": 7392125412670718995,
            "mp": 1,
        },
        {
            "id": 11,
            "name": "Supernailgun (11)",
            "classname": "weapon_supernailgun",
            "uuid": 16890440783343179689,
            "mp": 1,
        },
        {
            "id": 12,
            "name": "Nailgun (12)",
            "classname": "weapon_nailgun",
            "uuid": 903688802985225392,
            "mp": 1,
        },
        {
            "id": 13,
            "name": "Rocketlauncher (13)",
            "classname": "weapon_rocketlauncher",
            "uuid": 1550895472368425743,
            "mp": 1,
        },
        {
            "id": 14,
            "name": "Invulnerability (14)",
            "classname": "item_artifact_invulnerability",
            "uuid": 3466990716567130298,
            "mp": 1,
        },
        {
            "id": 15,
            "name": "Quad Damage (15)",
            "classname": "item_artifact_super_damage",
            "uuid": 13633158852686291632,
            "mp": 1,
        },
        {
            "id": 16,
            "name": "Lightning (16)",
            "classname": "weapon_lightning",
            "uuid": 4824212538608227970,
            "mp": 1,
        },
        {
            "id": 17,
            "name": "Grenadelauncher (17)",
            "classname": "weapon_grenadelauncher",
            "uuid": 7383249989115631159,
            "mp": 1,
        },
        {
            "id": 18,
            "name": "Large Medkit (18)",
            "classname": "item_health",
            "uuid": 14388986496737073064,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Rocketlauncher (19)",
            "classname": "weapon_rocketlauncher",
            "uuid": 17843280396351370090,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Supershotgun (20)",
            "classname": "weapon_supershotgun",
            "uuid": 5917548526762494243,
            "mp": 1,
        },
        {
            "id": 21,
            "name": "Yellow Armor (21)",
            "classname": "item_armor2",
            "uuid": 4673567739410900984,
            "mp": 1,
        },
        {
            "id": 22,
            "name": "Supershotgun (22)",
            "classname": "weapon_supershotgun",
            "uuid": 12306164173226259299,
            "mp": 1,
        },
        {
            "id": 23,
            "name": "Large Medkit (23)",
            "classname": "item_health",
            "uuid": 8168728090656907264,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Shells (24)",
            "classname": "item_shells",
            "uuid": 240434121891189276,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Shells (25)",
            "classname": "item_shells",
            "uuid": 8688961781095349714,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Rockets (26)",
            "classname": "item_rockets",
            "uuid": 95084779009911138,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Large Medkit (27)",
            "classname": "item_health",
            "uuid": 1136016522946047239,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Megahealth (28)",
            "classname": "item_health",
            "uuid": 3666363610328406728,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Cells (29)",
            "classname": "item_cells",
            "uuid": 11540877814610199883,
            "mp": 1,
        },
        {
            "id": 30,
            "name": "Cells (30)",
            "classname": "item_cells",
            "uuid": 10961747917137517547,
            "mp": 1,
        },
        {
            "id": 31,
            "name": "Shells (31)",
            "classname": "item_shells",
            "uuid": 16754763099062317404,
            "mp": 1,
        },
        {
            "id": 32,
            "name": "Spikes (32)",
            "classname": "item_spikes",
            "uuid": 2703639169310566654,
            "mp": 1,
        },
        {
            "id": 33,
            "name": "Shells (33)",
            "classname": "item_shells",
            "uuid": 11709947016882396104,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Small Medkit (34)",
            "classname": "item_health",
            "uuid": 13578365020736734439,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Small Medkit (35)",
            "classname": "item_health",
            "uuid": 6424391957215530995,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Red Armor (36)",
            "classname": "item_armorInv",
            "uuid": 12059510127803057722,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Rockets (37)",
            "classname": "item_rockets",
            "uuid": 7428236416052067947,
            "mp": 1,
        },
        {
            "id": 38,
            "name": "Spikes (38)",
            "classname": "item_spikes",
            "uuid": 12953701640233404260,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Small Medkit (39)",
            "classname": "item_health",
            "uuid": 10011257266401063312,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Small Medkit (40)",
            "classname": "item_health",
            "uuid": 10934885983157271949,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Shells (41)",
            "classname": "item_shells",
            "uuid": 12754770695196248008,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Spikes (42)",
            "classname": "item_spikes",
            "uuid": 2148908848130727481,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Small Medkit (43)",
            "classname": "item_health",
            "uuid": 16475357691660642928,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Small Medkit (44)",
            "classname": "item_health",
            "uuid": 12084255062415534369,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Small Medkit (45)",
            "classname": "item_health",
            "uuid": 8321060115646671623,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Small Medkit (46)",
            "classname": "item_health",
            "uuid": 11834731082422668686,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Rockets (47)",
            "classname": "item_rockets",
            "uuid": 5248736897946577340,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Small Medkit (48)",
            "classname": "item_health",
            "uuid": 3851807991862417659,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Shells (49)",
            "classname": "item_shells",
            "uuid": 5770246723377345999,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Large Medkit (50)",
            "classname": "item_health",
            "uuid": 14190433208534533004,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Megahealth (51)",
            "classname": "item_health",
            "uuid": 1614884408885782003,
            "mp": 1,
        },
        {
            "id": 52,
            "name": "Shells (52)",
            "classname": "item_shells",
            "uuid": 9968491700759392054,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Large Medkit (53)",
            "classname": "item_health",
            "uuid": 1384673887238406156,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Large Medkit (54)",
            "classname": "item_health",
            "uuid": 14728346901298228076,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Spikes (55)",
            "classname": "item_spikes",
            "uuid": 5651185494506105914,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Spikes (56)",
            "classname": "item_spikes",
            "uuid": 13019958038978285294,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Spikes (57)",
            "classname": "item_spikes",
            "uuid": 4580724552419283035,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Spikes (58)",
            "classname": "item_spikes",
            "uuid": 2318130013205454316,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Rockets (59)",
            "classname": "item_rockets",
            "uuid": 6821044953900765530,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Shells (60)",
            "classname": "item_shells",
            "uuid": 2499987769528264045,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Proximity (61)",
            "classname": "weapon_proximity_gun",
            "uuid": 18637071237081808,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Spikes (62)",
            "classname": "item_spikes",
            "uuid": 8519490829678963495,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Rockets (63)",
            "classname": "item_rockets",
            "uuid": 5853557514500976825,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Cells (64)",
            "classname": "item_cells",
            "uuid": 12000620826484459583,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Secret (65)",
            "classname": "trigger_secret",
            "uuid": 7007802096052623991,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Invisibility (66)",
            "classname": "item_artifact_invisibility",
            "uuid": 2593838668450401863,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Secret (67)",
            "classname": "trigger_secret",
            "uuid": 11378404119911801677,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Spikes (68)",
            "classname": "item_spikes",
            "uuid": 1287508114302376281,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Shells (69)",
            "classname": "item_shells",
            "uuid": 3558314139811515134,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Shells (70)",
            "classname": "item_shells",
            "uuid": 10990114674887190373,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Spikes (71)",
            "classname": "item_spikes",
            "uuid": 7928209153114399002,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Shells (72)",
            "classname": "item_shells",
            "uuid": 6803610906179061590,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Secret (73)",
            "classname": "trigger_secret",
            "uuid": 18338282508528349969,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Megahealth (74)",
            "classname": "item_health",
            "uuid": 5860058421481858457,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Mjolnir (75)",
            "classname": "weapon_mjolnir",
            "uuid": 14818872296560922692,
            "mp": 1,
        },
        {
            "id": 76,
            "name": "Wetsuit (76)",
            "classname": "item_artifact_wetsuit",
            "uuid": 12500454105329173360,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "All Kills (77)",
            "classname": "all_kills",
            "uuid": 1965040492323622617,
            "mp": 0,
        },
    ]

    events = ["Pipe Broken"]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Supershotgun (5)",
            ],
        )

        past_door_area = self.region(
            "Past Door Area",
            [
                "Nailgun (6)",
                "Spikes (38)",
                "Small Medkit (40)",
                "Small Medkit (39)",
                "Shells (70)",
                "Shells (72)",
                "Spikes (71)",
                "Rockets (59)",
                "Shells (69)",
                "Spikes (68)",
                "Laser (7)",
                "Shells (41)",
                "Large Medkit (50)",
                "Rockets (37)",
                "Shells (49)",
                "Spikes (58)",
                "Small Medkit (46)",
                "Nailgun (10)",
                "Small Medkit (45)",
                "Small Medkit (48)",
                "Spikes (55)",
                "Supernailgun (11)",
                "Supershotgun (20)",
                "Rocketlauncher (19)",
                "Rockets (47)",
                "Spikes (56)",
                "Supershotgun (22)",
                "Shells (52)",
                "Large Medkit (23)",
                "Spikes (57)",
                "Shells (24)",
                "Rocketlauncher (13)",
                "Shells (25)",
                "Large Medkit (27)",
                "Large Medkit (54)",
                "Rockets (26)",
                "Large Medkit (53)",
                "Spikes (32)",
                "Cells (30)",
                "Cells (29)",
                "Shells (31)",
                "Pipe Broken",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)

        self.restrict("Spikes (32)", r.can_dive | r.difficulty("hard"))
        self.restrict("Cells (30)", r.can_dive | r.difficulty("hard"))
        self.restrict("Cells (29)", r.can_dive | r.difficulty("hard"))
        self.restrict("Shells (31)", r.can_dive | r.difficulty("hard"))

        self.restrict(
            "Pipe Broken",
            ((r.rocketlauncher | r.grenadelauncher) & r.difficulty("hard"))
            | ((r.rocketlauncher | r.grenadelauncher) & r.can_dive),
        )

        shootswitch_area = self.region(
            "Shootswitch Area",
            [
                "Secret (3)",
                "Red Armor (36)",
                "Secret (1)",
                "Invulnerability (14)",
                "Megahealth (28)",
                "Secret (65)",
                "Rockets (63)",
                "Cells (64)",
                "Spikes (62)",
                "Proximity (61)",
                "Shells (60)",
                "Secret (67)",
                "Invisibility (66)",
            ],
        )
        self.connect(past_door_area, shootswitch_area, r.can_shootswitch)

        self.restrict("Invisibility (66)", r.jump)

        past_button_area = self.region(
            "Past Button Area",
            [
                "Yellow Armor (21)",
            ],
        )
        self.connect(ret, past_button_area, r.can_button)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Grenadelauncher (9)",
                "Supernailgun (8)",
                "Small Medkit (44)",
                "Small Medkit (43)",
                "Spikes (42)",
                "Exit",
            ],
        )
        self.connect(
            past_button_area,
            past_gold_door_area,
            self.gold_key | (r.bigjump & r.difficulty("extreme")),
        )

        exit_secret_area = self.region(
            "Exit Secret",
            [
                "Secret (73)",
                "Mjolnir (75)",
                "Megahealth (74)",
            ],
        )
        self.connect(
            past_gold_door_area,
            exit_secret_area,
            (r.can_jump & r.can_shootswitch) | r.can_gj_extr | r.can_rj_hard,
        )

        pump_room_area = self.region(
            "Pump Area",
            [
                "Wetsuit (76)",
                "Shells (33)",
                "Megahealth (51)",
                "Large Medkit (18)",
                "Small Medkit (35)",
                "Small Medkit (34)",
                "Grenadelauncher (17)",
                "Gold Key (2)",
                "All Kills (77)",
            ],
        )
        self.connect(past_door_area, pump_room_area, self.event("Pipe Broken"))

        self.restrict(
            "All Kills (77)",
            r.backpack(5) & (self.gold_key | (r.bigjump & r.difficulty("extreme"))),
        )

        return ret
