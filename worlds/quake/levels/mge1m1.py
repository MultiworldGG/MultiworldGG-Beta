from BaseClasses import Region

from ..base_classes import Q1Level


class mge1m1(Q1Level):
    name = "The Pain Drain"
    mapfile = "mge1m1"
    keys = ["Silver", "Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Secret (1)",
            "classname": "trigger_secret",
            "uuid": 8463944131160219331,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 1597988200351705141,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Secret (3)",
            "classname": "trigger_secret",
            "uuid": 4344855294524047103,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Secret (4)",
            "classname": "trigger_secret",
            "uuid": 1959199981736276332,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Supershotgun (5)",
            "classname": "weapon_supershotgun",
            "uuid": 7351165024917869124,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Shells (6)",
            "classname": "item_shells",
            "uuid": 1617755847355131620,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Shells (7)",
            "classname": "item_shells",
            "uuid": 879611248606352519,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Shells (8)",
            "classname": "item_shells",
            "uuid": 14823270386967441160,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Spikes (9)",
            "classname": "item_spikes",
            "uuid": 13832293970203159973,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Large Medkit (10)",
            "classname": "item_health",
            "uuid": 8517514333343429368,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Large Medkit (11)",
            "classname": "item_health",
            "uuid": 2381318778104167995,
            "mp": 0,
        },
        {
            "id": 12,
            "name": "Spikes (12)",
            "classname": "item_spikes",
            "uuid": 14885281584903296037,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Shells (13)",
            "classname": "item_shells",
            "uuid": 4377175023329490302,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Large Medkit (14)",
            "classname": "item_health",
            "uuid": 17536485232958311741,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Large Medkit (15)",
            "classname": "item_health",
            "uuid": 13624472716970358586,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Large Medkit (16)",
            "classname": "item_health",
            "uuid": 8273663545344436040,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Large Medkit (17)",
            "classname": "item_health",
            "uuid": 2540477820223768341,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Large Medkit (18)",
            "classname": "item_health",
            "uuid": 5554054463095913013,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Large Medkit (19)",
            "classname": "item_health",
            "uuid": 7371206509807633255,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Large Medkit (20)",
            "classname": "item_health",
            "uuid": 3499585276062693896,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Large Medkit (21)",
            "classname": "item_health",
            "uuid": 1121886289511393239,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Silver Key (22)",
            "classname": "item_key1",
            "uuid": 7751641546966175476,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Quad Damage (23)",
            "classname": "item_artifact_super_damage",
            "uuid": 18242309492698347385,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Biosuit (24)",
            "classname": "item_artifact_envirosuit",
            "uuid": 2284134567198907390,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Spikes (25)",
            "classname": "item_spikes",
            "uuid": 14228461162167433990,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Supernailgun (26)",
            "classname": "weapon_supernailgun",
            "uuid": 2879147529077537220,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Large Medkit (27)",
            "classname": "item_health",
            "uuid": 3210252663189211499,
            "mp": 0,
        },
        {
            "id": 28,
            "name": "Large Medkit (28)",
            "classname": "item_health",
            "uuid": 9706719036450170350,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Spikes (29)",
            "classname": "item_spikes",
            "uuid": 1790803720341449808,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Shells (30)",
            "classname": "item_shells",
            "uuid": 2455670055914170656,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Nailgun (31)",
            "classname": "weapon_nailgun",
            "uuid": 11376770006476830460,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Spikes (32)",
            "classname": "item_spikes",
            "uuid": 8783769517173897605,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Gold Key (33)",
            "classname": "item_key2",
            "uuid": 15703380152555761837,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Shells (34)",
            "classname": "item_shells",
            "uuid": 17116310249775922522,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Green Armor (35)",
            "classname": "item_armor1",
            "uuid": 6656940746303092082,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Spikes (36)",
            "classname": "item_spikes",
            "uuid": 7556421169898503622,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Gold Key (37)",
            "classname": "item_key2",
            "uuid": 10939466139253823482,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Shells (38)",
            "classname": "item_shells",
            "uuid": 9576769077962021833,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Small Medkit (39)",
            "classname": "item_health",
            "uuid": 7576235473345958565,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Small Medkit (40)",
            "classname": "item_health",
            "uuid": 3494418882655329388,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Large Medkit (41)",
            "classname": "item_health",
            "uuid": 9070243078524280739,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Shells (42)",
            "classname": "item_shells",
            "uuid": 83094577208852946,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Spikes (43)",
            "classname": "item_spikes",
            "uuid": 198117972014671633,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Spikes (44)",
            "classname": "item_spikes",
            "uuid": 4725220517744849265,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Shells (45)",
            "classname": "item_shells",
            "uuid": 535196217111850673,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Large Medkit (46)",
            "classname": "item_health",
            "uuid": 15149034456863730714,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Large Medkit (47)",
            "classname": "item_health",
            "uuid": 846608682113712210,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Shells (48)",
            "classname": "item_shells",
            "uuid": 9499741250641393569,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Grenadelauncher (49)",
            "classname": "weapon_grenadelauncher",
            "uuid": 5159559864100063779,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Spikes (50)",
            "classname": "item_spikes",
            "uuid": 16128485371107275488,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Megahealth (51)",
            "classname": "item_health",
            "uuid": 408917753581879787,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Grenadelauncher (52)",
            "classname": "weapon_grenadelauncher",
            "uuid": 844039328482532686,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Large Medkit (53)",
            "classname": "item_health",
            "uuid": 7184145313995964140,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Large Medkit (54)",
            "classname": "item_health",
            "uuid": 14679115695242985462,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Rockets (55)",
            "classname": "item_rockets",
            "uuid": 13578889932912663458,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Shells (56)",
            "classname": "item_shells",
            "uuid": 7885414097047410838,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Spikes (57)",
            "classname": "item_spikes",
            "uuid": 15486351335179011551,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Shells (58)",
            "classname": "item_shells",
            "uuid": 3250417071977480883,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Nailgun (59)",
            "classname": "weapon_nailgun",
            "uuid": 5250929835890656513,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Spikes (60)",
            "classname": "item_spikes",
            "uuid": 4791862600146067742,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Shells (61)",
            "classname": "item_shells",
            "uuid": 3314021758209696424,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Shells (62)",
            "classname": "item_shells",
            "uuid": 2776691051479557564,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Large Medkit (63)",
            "classname": "item_health",
            "uuid": 9313752961840720024,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Spikes (64)",
            "classname": "item_spikes",
            "uuid": 2392587878545011199,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Shells (65)",
            "classname": "item_shells",
            "uuid": 442706630951940170,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Spikes (66)",
            "classname": "item_spikes",
            "uuid": 9128484706615454635,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Spikes (67)",
            "classname": "item_spikes",
            "uuid": 11554137871881963127,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Large Medkit (68)",
            "classname": "item_health",
            "uuid": 13441738627190281687,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Rockets (69)",
            "classname": "item_rockets",
            "uuid": 10574066836105076669,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Biosuit (70)",
            "classname": "item_artifact_envirosuit",
            "uuid": 15965619048884804357,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Large Medkit (71)",
            "classname": "item_health",
            "uuid": 6315228903879762873,
            "mp": 0,
        },
        {
            "id": 72,
            "name": "Large Medkit (72)",
            "classname": "item_health",
            "uuid": 16256380253103548887,
            "mp": 0,
        },
        {
            "id": 73,
            "name": "Secret (73)",
            "classname": "trigger_secret",
            "uuid": 5798262308022438945,
            "mp": 0,
        },
        {
            "id": 74,
            "name": "Secret Exit",
            "classname": "trigger_changelevel",
            "uuid": 1868218469401539464,
            "mp": 0,
        },
        {
            "id": 75,
            "name": "Green Armor (75)",
            "classname": "item_armor1",
            "uuid": 16352773038739892765,
            "mp": 0,
        },
        {
            "id": 76,
            "name": "Large Medkit (76)",
            "classname": "item_health",
            "uuid": 8930380254885320942,
            "mp": 0,
        },
        {
            "id": 77,
            "name": "Green Armor (77)",
            "classname": "item_armor1",
            "uuid": 1350779183368303071,
            "mp": 0,
        },
        {
            "id": 78,
            "name": "Megahealth (78)",
            "classname": "item_health",
            "uuid": 12194062823664683468,
            "mp": 0,
        },
        {
            "id": 79,
            "name": "Secret (79)",
            "classname": "trigger_secret",
            "uuid": 15202576435172477967,
            "mp": 0,
        },
        {
            "id": 80,
            "name": "Spikes (80)",
            "classname": "item_spikes",
            "uuid": 2902003549602015900,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Shells (81)",
            "classname": "item_shells",
            "uuid": 10536140859696939110,
            "mp": 0,
        },
        {
            "id": 82,
            "name": "Shells (82)",
            "classname": "item_shells",
            "uuid": 16117336030198069892,
            "mp": 0,
        },
        {
            "id": 83,
            "name": "All Kills (83)",
            "classname": "all_kills",
            "uuid": 10259995725130780640,
            "mp": 0,
        },
    ]
    must_bio = True
    must_invuln = True

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [],
        )

        past_door_area = self.region(
            "Past Door Area",
            [
                "Large Medkit (63)",
                "Green Armor (75)",
                "Shells (7)",
                "Spikes (29)",
                "Shells (30)",
                "Spikes (67)",
                "Large Medkit (76)",
                "Nailgun (59)",
                "Spikes (60)",
                "Shells (62)",
                "Spikes (32)",
                "Nailgun (31)",
            ],
        )
        self.connect(ret, past_door_area, r.can_door)
        self.restrict("Large Medkit (76)", r.jump)

        past_button_area = self.region(
            "Past Button Area",
            [
                "Supershotgun (5)",
                "Shells (6)",
                "Large Medkit (27)",
                "Large Medkit (28)",
                "Large Medkit (20)",
                "Large Medkit (72)",
                "Large Medkit (21)",
                "Large Medkit (15)",
                "Large Medkit (14)",
                "Large Medkit (46)",
                "Large Medkit (47)",
                "Spikes (36)",
                "Gold Key (33)",
                "Biosuit (24)",
            ],
        )
        self.connect(past_door_area, past_button_area, r.can_button)
        self.restrict("Biosuit (24)", r.jump)

        swim_area = self.region(
            "Swim Area",
            [
                "Megahealth (51)",
                "Secret (3)",
                "Secret (4)",
                "Large Medkit (53)",
                "Large Medkit (54)",
                "Spikes (80)",
                "Shells (56)",
                "Spikes (57)",
                "Shells (58)",
                "Grenadelauncher (52)",
                "Rockets (55)",
            ],
        )
        self.connect(past_button_area, swim_area, r.jump & (r.biosuit(1) | r.invuln(1)))

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Shells (13)",
                "Large Medkit (17)",
                "Large Medkit (71)",
                "Large Medkit (16)",
                "Spikes (12)",
                "Quad Damage (23)",
                "Spikes (25)",
                "Supernailgun (26)",
                "Spikes (66)",
                "Shells (8)",
                "Large Medkit (10)",
                "Large Medkit (11)",
                "Shells (38)",
                "Shells (34)",
                "Spikes (9)",
                "Silver Key (22)",
                "Secret (1)",
                "Green Armor (35)",
            ],
        )
        self.connect(past_button_area, past_gold_door_area, self.gold_key)
        self.restrict("Secret (1)", r.can_shootswitch)
        self.restrict("Green Armor (35)", r.can_shootswitch)

        past_silver_door_area = self.region(
            "Past Silver Door",
            [
                "Large Medkit (41)",
                "Spikes (43)",
                "Shells (42)",
                "Shells (61)",
                "Small Medkit (39)",
                "Small Medkit (40)",
                "Shells (48)",
                "Spikes (44)",
                "Gold Key (37)",
                "Large Medkit (68)",
                "Shells (45)",
                "Biosuit (70)",
                "Secret Exit",
                "Secret (73)",
                "Rockets (69)",
            ],
        )
        self.connect(past_gold_door_area, past_silver_door_area, self.silver_key)
        self.restrict("Biosuit (70)", r.can_shootswitch)
        self.restrict("Secret Exit", r.can_dive & (r.biosuit(1) | r.invuln(1)))
        self.restrict("Gold Key (37)", (r.can_shootswitch | r.bigjump_hard) & r.jump)
        self.restrict(
            "Large Medkit (68)", (self.gold_key & r.can_shootswitch) | r.bigjump_hard
        )
        self.restrict(
            "Shells (45)", (self.gold_key & r.can_shootswitch) | r.bigjump_hard
        )
        self.restrict("Rockets (69)", r.can_jump | r.can_rj_hard | r.can_gj_extr)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Grenadelauncher (49)",
                "Spikes (50)",
                "Green Armor (77)",
                "Secret (79)",
                "Megahealth (78)",
                "Spikes (64)",
                "Shells (65)",
                "Exit",
                "All Kills (83)",
            ],
        )
        self.connect(past_silver_door_area, past_gold_door_area, self.gold_key)
        self.restrict("Green Armor (77)", r.jump)
        self.restrict("Secret (79)", r.jump)
        self.restrict("All Kills (83)", r.difficult_combat)

        return ret
