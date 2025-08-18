from BaseClasses import Region

from ..base_classes import Q1Level


class mge1m2(Q1Level):
    name = "The Wishing Well"
    mapfile = "mge1m2"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 9130487765779937119,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Gold Key (2)",
            "classname": "item_key2",
            "uuid": 4130794243885849281,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Sigil (3)",
            "classname": "item_sigil",
            "uuid": 8108716020014195300,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Silver Key (4)",
            "classname": "item_key1",
            "uuid": 5035174084875441018,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Megahealth (5)",
            "classname": "item_health",
            "uuid": 5187357260460078267,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Supershotgun (6)",
            "classname": "weapon_supershotgun",
            "uuid": 16353851755775450736,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Shells (7)",
            "classname": "item_shells",
            "uuid": 8358613780284530595,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Nailgun (8)",
            "classname": "weapon_nailgun",
            "uuid": 3150801625436621513,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Spikes (9)",
            "classname": "item_spikes",
            "uuid": 16100546523792762766,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Spikes (10)",
            "classname": "item_spikes",
            "uuid": 12773581783283242158,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Shells (11)",
            "classname": "item_shells",
            "uuid": 12149388036982989899,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Spikes (12)",
            "classname": "item_spikes",
            "uuid": 4366040331679410828,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Shells (13)",
            "classname": "item_shells",
            "uuid": 13821962114359235754,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Shells (14)",
            "classname": "item_shells",
            "uuid": 5747783158257244951,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Spikes (15)",
            "classname": "item_spikes",
            "uuid": 803920845571216661,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Rockets (16)",
            "classname": "item_rockets",
            "uuid": 63888491358277432,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Large Medkit (17)",
            "classname": "item_health",
            "uuid": 16913901930960319234,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Large Medkit (18)",
            "classname": "item_health",
            "uuid": 2358847076270711997,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Megahealth (19)",
            "classname": "item_health",
            "uuid": 14031884517167850720,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Rockets (20)",
            "classname": "item_rockets",
            "uuid": 13817218318737479892,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Large Medkit (21)",
            "classname": "item_health",
            "uuid": 2461170544740542668,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Large Medkit (22)",
            "classname": "item_health",
            "uuid": 15844596014538387444,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Large Medkit (23)",
            "classname": "item_health",
            "uuid": 11059311937899526824,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Large Medkit (24)",
            "classname": "item_health",
            "uuid": 8807377015370000164,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Shells (25)",
            "classname": "item_shells",
            "uuid": 1262829947600858677,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Spikes (26)",
            "classname": "item_spikes",
            "uuid": 15559442100593142577,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Spikes (27)",
            "classname": "item_spikes",
            "uuid": 8547722760441457153,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Shells (28)",
            "classname": "item_shells",
            "uuid": 17288458561345284155,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Shells (29)",
            "classname": "item_shells",
            "uuid": 15315744444253113653,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Spikes (30)",
            "classname": "item_spikes",
            "uuid": 1273862310774677355,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Grenadelauncher (31)",
            "classname": "weapon_grenadelauncher",
            "uuid": 5772680035435496558,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Rockets (32)",
            "classname": "item_rockets",
            "uuid": 5282361020845207111,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Spikes (33)",
            "classname": "item_spikes",
            "uuid": 5506815394418269715,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Large Medkit (34)",
            "classname": "item_health",
            "uuid": 6499058664688799446,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Large Medkit (35)",
            "classname": "item_health",
            "uuid": 16265380381534108953,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Spikes (36)",
            "classname": "item_spikes",
            "uuid": 4653548927060132626,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Shells (37)",
            "classname": "item_shells",
            "uuid": 1942747093885386488,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Spikes (38)",
            "classname": "item_spikes",
            "uuid": 6655329048631508815,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Spikes (39)",
            "classname": "item_spikes",
            "uuid": 12472673688814165693,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Shells (40)",
            "classname": "item_shells",
            "uuid": 10995173664099544023,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Spikes (41)",
            "classname": "item_spikes",
            "uuid": 12497868199083398791,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Shells (42)",
            "classname": "item_shells",
            "uuid": 962773562004819382,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Lightning (43)",
            "classname": "weapon_lightning",
            "uuid": 10343786650767374172,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Cells (44)",
            "classname": "item_cells",
            "uuid": 16766878223859056534,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Secret (45)",
            "classname": "trigger_secret",
            "uuid": 14029285729963320138,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Secret (46)",
            "classname": "trigger_secret",
            "uuid": 4016829363321422795,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Large Medkit (47)",
            "classname": "item_health",
            "uuid": 8911656748019021541,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Secret (48)",
            "classname": "trigger_secret",
            "uuid": 5163270627567951767,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Spikes (49)",
            "classname": "item_spikes",
            "uuid": 13221931784062946716,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Shells (50)",
            "classname": "item_shells",
            "uuid": 2169816581295645051,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Spikes (51)",
            "classname": "item_spikes",
            "uuid": 4173479358303733271,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Large Medkit (52)",
            "classname": "item_health",
            "uuid": 6314164225785579085,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Large Medkit (53)",
            "classname": "item_health",
            "uuid": 18163856420820994991,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Large Medkit (54)",
            "classname": "item_health",
            "uuid": 17052440144161245712,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Large Medkit (55)",
            "classname": "item_health",
            "uuid": 10228955262777065861,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Shells (56)",
            "classname": "item_shells",
            "uuid": 4633964566457074943,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Yellow Armor (57)",
            "classname": "item_armor2",
            "uuid": 11154535731809715017,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Large Medkit (58)",
            "classname": "item_health",
            "uuid": 8535128799715481627,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Secret (59)",
            "classname": "trigger_secret",
            "uuid": 18130250081947739831,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Spikes (60)",
            "classname": "item_spikes",
            "uuid": 17933372753923627687,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Large Medkit (61)",
            "classname": "item_health",
            "uuid": 12291730769691402567,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Spikes (62)",
            "classname": "item_spikes",
            "uuid": 11623349033691687962,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Large Medkit (63)",
            "classname": "item_health",
            "uuid": 5304902611565082682,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Large Medkit (64)",
            "classname": "item_health",
            "uuid": 16576370131961567559,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Large Medkit (65)",
            "classname": "item_health",
            "uuid": 5584255489067084792,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Large Medkit (66)",
            "classname": "item_health",
            "uuid": 5166276498909129438,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Green Armor (67)",
            "classname": "item_armor1",
            "uuid": 16140609662448018727,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Secret (68)",
            "classname": "trigger_secret",
            "uuid": 9964361176470820163,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Secret (69)",
            "classname": "trigger_secret",
            "uuid": 1819347903780715694,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Supernailgun (70)",
            "classname": "weapon_supernailgun",
            "uuid": 11405993791576675930,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Spikes (71)",
            "classname": "item_spikes",
            "uuid": 504627214364587420,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "All Kills (72)",
            "classname": "all_kills",
            "uuid": 13798740430467511494,
            "mp": 0,
        },
    ]

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Supershotgun (6)",
                "Shells (7)",
                "Large Medkit (52)",
                "Large Medkit (66)",
                "Large Medkit (53)",
                "Green Armor (67)",
                "Secret (68)",
            ],
        )

        self.restrict("Green Armor (67)", r.can_shootswitch & r.jump)
        self.restrict("Secret (68)", r.can_shootswitch & r.jump)

        start_upper_area = self.region(
            "Start Upper",
            [
                "Gold Key (2)",
                "Megahealth (19)",
                "Secret (46)",
            ],
        )
        self.connect(ret, start_upper_area, r.bigjump_hard)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Large Medkit (54)",
                "Large Medkit (55)",
                "Supernailgun (70)",
                "Spikes (71)",
                "Shells (40)",
                "Spikes (39)",
                "Shells (37)",
                "Spikes (36)",
                "Grenadelauncher (31)",
                "Rockets (32)",
                "Large Medkit (34)",
                "Large Medkit (64)",
                "Large Medkit (35)",
                "Spikes (38)",
            ],
        )
        self.connect(ret, past_silver_door_area, self.silver_key)

        button_secret_area = self.region(
            "Button Secret Area",
            [
                "Secret (59)",
                "Large Medkit (58)",
                "Cells (44)",
                "Lightning (43)",
                "Spikes (60)",
            ],
        )
        self.connect(past_silver_door_area, button_secret_area, r.can_button)

        silver_upper_area = self.region(
            "Silver Upper",
            [
                "Large Medkit (61)",
                "Spikes (62)",
                "Shells (56)",
            ],
        )
        self.connect(
            past_silver_door_area, silver_upper_area, r.bigjump_hard | r.can_button
        )
        self.restrict("Large Medkit (61)", r.can_button)

        self.connect(silver_upper_area, start_upper_area)

        past_door_area = self.region(
            "Past Door Area",
            [
                "Nailgun (8)",
                "Spikes (9)",
                "Spikes (30)",
                "Shells (29)",
                "Large Medkit (17)",
                "Large Medkit (18)",
                "Spikes (10)",
                "Shells (11)",
                "Secret (45)",
                "Spikes (33)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)

        self.restrict("Secret (45)", r.can_shootswitch & r.jump)
        self.restrict("Spikes (33)", r.can_shootswitch & r.jump)

        shootswitch_area = self.region(
            "Shootswitch Area",
            [
                "Shells (50)",
                "Spikes (51)",
                "Spikes (49)",
                "Yellow Armor (57)",
                "Secret (48)",
            ],
        )
        self.connect(past_door_area, shootswitch_area, r.can_shootswitch)
        self.restrict("Yellow Armor (57)", r.can_button)
        self.restrict("Secret (48)", r.can_button)

        past_button_area = self.region(
            "Past Button Area",
            [
                "Large Medkit (23)",
                "Large Medkit (63)",
                "Large Medkit (47)",
                "Megahealth (5)",
                "Secret (69)",
                "Shells (25)",
                "Spikes (26)",
                "Large Medkit (24)",
                "Spikes (27)",
                "Shells (28)",
                "Silver Key (4)",
            ],
        )
        self.connect(past_door_area, past_button_area, r.can_button)

        self.restrict("Silver Key (4)", r.can_jump | r.can_rj_hard | r.can_gj_extr)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Rockets (20)",
                "Spikes (15)",
                "Shells (14)",
                "Spikes (41)",
                "Shells (42)",
                "Large Medkit (22)",
                "Large Medkit (65)",
                "Large Medkit (21)",
                "Shells (13)",
                "Spikes (12)",
                "Rockets (16)",
                "Sigil (3)",
                "Exit",
                "All Kills (72)",
            ],
        )
        self.connect(past_door_area, past_gold_door_area, self.gold_key)

        self.restrict("Sigil (3)", r.can_button)
        self.restrict("Exit", r.can_button)
        self.restrict("All Kills (72)", r.difficult_combat)

        return ret
