from BaseClasses import Region

from ..base_classes import Q1Level


class e2m5(Q1Level):
    name = "The Wizard's Manse"
    mapfile = "e2m5"
    keys = ["Gold"]
    location_defs = [
        {
            "id": 1,
            "name": "Large Medkit (1)",
            "classname": "item_health",
            "uuid": 4738560481768993637,
            "mp": 0,
        },
        {
            "id": 2,
            "name": "Large Medkit (2)",
            "classname": "item_health",
            "uuid": 3554933176472582356,
            "mp": 0,
        },
        {
            "id": 3,
            "name": "Exit",
            "classname": "trigger_changelevel",
            "uuid": 2403491584117897987,
            "mp": 0,
        },
        {
            "id": 4,
            "name": "Large Medkit (4)",
            "classname": "item_health",
            "uuid": 10135538089100529648,
            "mp": 0,
        },
        {
            "id": 5,
            "name": "Large Medkit (5)",
            "classname": "item_health",
            "uuid": 16404429428509767619,
            "mp": 0,
        },
        {
            "id": 6,
            "name": "Shells (6)",
            "classname": "item_shells",
            "uuid": 7947222547908586074,
            "mp": 0,
        },
        {
            "id": 7,
            "name": "Shells (7)",
            "classname": "item_shells",
            "uuid": 15541079641597510126,
            "mp": 0,
        },
        {
            "id": 8,
            "name": "Shells (8)",
            "classname": "item_shells",
            "uuid": 6462881635451732737,
            "mp": 0,
        },
        {
            "id": 9,
            "name": "Shells (9)",
            "classname": "item_shells",
            "uuid": 10800488869907519570,
            "mp": 0,
        },
        {
            "id": 10,
            "name": "Spikes (10)",
            "classname": "item_spikes",
            "uuid": 4128459308717560707,
            "mp": 0,
        },
        {
            "id": 11,
            "name": "Nailgun (11)",
            "classname": "weapon_nailgun",
            "uuid": 1298939240582388699,
            "mp": 1,
        },
        {
            "id": 12,
            "name": "Spikes (12)",
            "classname": "item_spikes",
            "uuid": 10366111934710994425,
            "mp": 0,
        },
        {
            "id": 13,
            "name": "Shells (13)",
            "classname": "item_shells",
            "uuid": 15931418154857225846,
            "mp": 0,
        },
        {
            "id": 14,
            "name": "Spikes (14)",
            "classname": "item_spikes",
            "uuid": 9441101181394374560,
            "mp": 0,
        },
        {
            "id": 15,
            "name": "Large Medkit (15)",
            "classname": "item_health",
            "uuid": 206018731030559406,
            "mp": 0,
        },
        {
            "id": 16,
            "name": "Large Medkit (16)",
            "classname": "item_health",
            "uuid": 12271963840606887255,
            "mp": 0,
        },
        {
            "id": 17,
            "name": "Large Medkit (17)",
            "classname": "item_health",
            "uuid": 15220329853833279076,
            "mp": 0,
        },
        {
            "id": 18,
            "name": "Large Medkit (18)",
            "classname": "item_health",
            "uuid": 10426795978730306217,
            "mp": 0,
        },
        {
            "id": 19,
            "name": "Spikes (19)",
            "classname": "item_spikes",
            "uuid": 13464655871892557738,
            "mp": 0,
        },
        {
            "id": 20,
            "name": "Shells (20)",
            "classname": "item_shells",
            "uuid": 10853000355604269602,
            "mp": 0,
        },
        {
            "id": 21,
            "name": "Shells (21)",
            "classname": "item_shells",
            "uuid": 9309142584096356704,
            "mp": 0,
        },
        {
            "id": 22,
            "name": "Quad Damage (22)",
            "classname": "item_artifact_super_damage",
            "uuid": 16350000381410665973,
            "mp": 0,
        },
        {
            "id": 23,
            "name": "Rockets (23)",
            "classname": "item_rockets",
            "uuid": 13382383917129136517,
            "mp": 0,
        },
        {
            "id": 24,
            "name": "Large Medkit (24)",
            "classname": "item_health",
            "uuid": 7900365832814790235,
            "mp": 0,
        },
        {
            "id": 25,
            "name": "Megahealth (25)",
            "classname": "item_health",
            "uuid": 8603862709201134395,
            "mp": 0,
        },
        {
            "id": 26,
            "name": "Biosuit (26)",
            "classname": "item_artifact_envirosuit",
            "uuid": 5555804284698660623,
            "mp": 0,
        },
        {
            "id": 27,
            "name": "Grenadelauncher (27)",
            "classname": "weapon_grenadelauncher",
            "uuid": 3251709328125874080,
            "mp": 1,
        },
        {
            "id": 28,
            "name": "Rockets (28)",
            "classname": "item_rockets",
            "uuid": 10517780956591759850,
            "mp": 0,
        },
        {
            "id": 29,
            "name": "Shells (29)",
            "classname": "item_shells",
            "uuid": 15646249481608112063,
            "mp": 0,
        },
        {
            "id": 30,
            "name": "Large Medkit (30)",
            "classname": "item_health",
            "uuid": 11883125383214652841,
            "mp": 0,
        },
        {
            "id": 31,
            "name": "Small Medkit (31)",
            "classname": "item_health",
            "uuid": 5462939365263539705,
            "mp": 0,
        },
        {
            "id": 32,
            "name": "Red Armor (32)",
            "classname": "item_armorInv",
            "uuid": 8171090851879941689,
            "mp": 0,
        },
        {
            "id": 33,
            "name": "Green Armor (33)",
            "classname": "item_armor1",
            "uuid": 11133924778766868986,
            "mp": 0,
        },
        {
            "id": 34,
            "name": "Large Medkit (34)",
            "classname": "item_health",
            "uuid": 6260291393243942116,
            "mp": 0,
        },
        {
            "id": 35,
            "name": "Large Medkit (35)",
            "classname": "item_health",
            "uuid": 800507806592980801,
            "mp": 0,
        },
        {
            "id": 36,
            "name": "Large Medkit (36)",
            "classname": "item_health",
            "uuid": 11757514977159505539,
            "mp": 0,
        },
        {
            "id": 37,
            "name": "Large Medkit (37)",
            "classname": "item_health",
            "uuid": 6838861064455663312,
            "mp": 0,
        },
        {
            "id": 38,
            "name": "Large Medkit (38)",
            "classname": "item_health",
            "uuid": 10708229066232379163,
            "mp": 0,
        },
        {
            "id": 39,
            "name": "Shells (39)",
            "classname": "item_shells",
            "uuid": 4549676822991688418,
            "mp": 0,
        },
        {
            "id": 40,
            "name": "Large Medkit (40)",
            "classname": "item_health",
            "uuid": 7644690546801570104,
            "mp": 0,
        },
        {
            "id": 41,
            "name": "Large Medkit (41)",
            "classname": "item_health",
            "uuid": 17747103319628047185,
            "mp": 0,
        },
        {
            "id": 42,
            "name": "Rockets (42)",
            "classname": "item_rockets",
            "uuid": 2696296995894764243,
            "mp": 0,
        },
        {
            "id": 43,
            "name": "Gold Key (43)",
            "classname": "item_key2",
            "uuid": 10582003314321759246,
            "mp": 0,
        },
        {
            "id": 44,
            "name": "Large Medkit (44)",
            "classname": "item_health",
            "uuid": 4691545437624463202,
            "mp": 0,
        },
        {
            "id": 45,
            "name": "Large Medkit (45)",
            "classname": "item_health",
            "uuid": 16531167325940091235,
            "mp": 0,
        },
        {
            "id": 46,
            "name": "Large Medkit (46)",
            "classname": "item_health",
            "uuid": 18281887123674706767,
            "mp": 0,
        },
        {
            "id": 47,
            "name": "Large Medkit (47)",
            "classname": "item_health",
            "uuid": 7831132566042823148,
            "mp": 0,
        },
        {
            "id": 48,
            "name": "Large Medkit (48)",
            "classname": "item_health",
            "uuid": 7136492856303340620,
            "mp": 0,
        },
        {
            "id": 49,
            "name": "Rockets (49)",
            "classname": "item_rockets",
            "uuid": 3713195612501045037,
            "mp": 0,
        },
        {
            "id": 50,
            "name": "Spikes (50)",
            "classname": "item_spikes",
            "uuid": 13086099064670852903,
            "mp": 0,
        },
        {
            "id": 51,
            "name": "Shells (51)",
            "classname": "item_shells",
            "uuid": 1259096933837752695,
            "mp": 0,
        },
        {
            "id": 52,
            "name": "Shells (52)",
            "classname": "item_shells",
            "uuid": 948017047401040567,
            "mp": 0,
        },
        {
            "id": 53,
            "name": "Spikes (53)",
            "classname": "item_spikes",
            "uuid": 11496162848755318088,
            "mp": 0,
        },
        {
            "id": 54,
            "name": "Spikes (54)",
            "classname": "item_spikes",
            "uuid": 9313842715883172341,
            "mp": 0,
        },
        {
            "id": 55,
            "name": "Shells (55)",
            "classname": "item_shells",
            "uuid": 10780739603901522054,
            "mp": 0,
        },
        {
            "id": 56,
            "name": "Spikes (56)",
            "classname": "item_spikes",
            "uuid": 1047584068757482130,
            "mp": 0,
        },
        {
            "id": 57,
            "name": "Spikes (57)",
            "classname": "item_spikes",
            "uuid": 15985374079126586444,
            "mp": 0,
        },
        {
            "id": 58,
            "name": "Spikes (58)",
            "classname": "item_spikes",
            "uuid": 16802005622323820341,
            "mp": 0,
        },
        {
            "id": 59,
            "name": "Spikes (59)",
            "classname": "item_spikes",
            "uuid": 1329298418373029403,
            "mp": 0,
        },
        {
            "id": 60,
            "name": "Spikes (60)",
            "classname": "item_spikes",
            "uuid": 4899550433928732395,
            "mp": 0,
        },
        {
            "id": 61,
            "name": "Red Armor (61)",
            "classname": "item_armorInv",
            "uuid": 8128929694129582348,
            "mp": 0,
        },
        {
            "id": 62,
            "name": "Quad Damage (62)",
            "classname": "item_artifact_super_damage",
            "uuid": 16678698024332217743,
            "mp": 0,
        },
        {
            "id": 63,
            "name": "Secret (63)",
            "classname": "trigger_secret",
            "uuid": 140536753017994299,
            "mp": 0,
        },
        {
            "id": 64,
            "name": "Secret (64)",
            "classname": "trigger_secret",
            "uuid": 5423884632808767001,
            "mp": 0,
        },
        {
            "id": 65,
            "name": "Large Medkit (65)",
            "classname": "item_health",
            "uuid": 11576036856526875735,
            "mp": 0,
        },
        {
            "id": 66,
            "name": "Large Medkit (66)",
            "classname": "item_health",
            "uuid": 8573063559761961391,
            "mp": 0,
        },
        {
            "id": 67,
            "name": "Large Medkit (67)",
            "classname": "item_health",
            "uuid": 16799130227856789660,
            "mp": 0,
        },
        {
            "id": 68,
            "name": "Large Medkit (68)",
            "classname": "item_health",
            "uuid": 5394793675774740554,
            "mp": 0,
        },
        {
            "id": 69,
            "name": "Large Medkit (69)",
            "classname": "item_health",
            "uuid": 14888165006751084028,
            "mp": 0,
        },
        {
            "id": 70,
            "name": "Rocketlauncher (70)",
            "classname": "weapon_rocketlauncher",
            "uuid": 11666994208776049458,
            "mp": 0,
        },
        {
            "id": 71,
            "name": "Supernailgun (71)",
            "classname": "weapon_supernailgun",
            "uuid": 13160139171917665207,
            "mp": 1,
        },
        {
            "id": 72,
            "name": "Quad Damage (72)",
            "classname": "item_artifact_super_damage",
            "uuid": 18203381285713061730,
            "mp": 1,
        },
        {
            "id": 73,
            "name": "Supershotgun (73)",
            "classname": "weapon_supershotgun",
            "uuid": 4960424232955347803,
            "mp": 1,
        },
        {
            "id": 74,
            "name": "Lightning (74)",
            "classname": "weapon_lightning",
            "uuid": 2667854217696700341,
            "mp": 1,
        },
        {
            "id": 75,
            "name": "Cells (75)",
            "classname": "item_cells",
            "uuid": 709617619265879533,
            "mp": 1,
        },
        {
            "id": 76,
            "name": "Cells (76)",
            "classname": "item_cells",
            "uuid": 4434028462766901918,
            "mp": 1,
        },
        {
            "id": 77,
            "name": "Cells (77)",
            "classname": "item_cells",
            "uuid": 13375655814034975599,
            "mp": 1,
        },
        {
            "id": 78,
            "name": "Cells (78)",
            "classname": "item_cells",
            "uuid": 17718995331729000213,
            "mp": 1,
        },
        {
            "id": 79,
            "name": "Lightning (79)",
            "classname": "weapon_lightning",
            "uuid": 7591494304197261259,
            "mp": 0,
        },
        {
            "id": 80,
            "name": "Cells (80)",
            "classname": "item_cells",
            "uuid": 15310584948060466359,
            "mp": 0,
        },
        {
            "id": 81,
            "name": "Invulnerability (81)",
            "classname": "item_artifact_invulnerability",
            "uuid": 8821618101057095151,
            "mp": 1,
        },
        {
            "id": 82,
            "name": "Invisibility (82)",
            "classname": "item_artifact_invisibility",
            "uuid": 1084390958740763712,
            "mp": 1,
        },
        {
            "id": 83,
            "name": "All Kills (83)",
            "classname": "all_kills",
            "uuid": 15383799816635148176,
            "mp": 0,
        },
    ]

    must_bio = True

    def main_region(self) -> Region:
        r = self.rules

        ret = self.region(
            self.name,
            [
                "Large Medkit (4)",
                "Shells (6)",
                "Large Medkit (5)",
                "Cells (78)",
                "Cells (77)",
                "Rocketlauncher (70)",
                "Shells (7)",
                "Quad Damage (72)",
                "Spikes (56)",
                "Large Medkit (18)",
                "Nailgun (11)",
                "Spikes (10)",
                "Large Medkit (16)",
                "Shells (9)",
                "Supershotgun (73)",
                "Spikes (12)",
            ],
        )

        shallow_dive_area = self.region(
            "Shallow Dive Area",
            [
                "Spikes (57)",
                "Spikes (54)",
                "Large Medkit (35)",
                "Shells (55)",
                "Large Medkit (34)",
                "Large Medkit (36)",
            ],
        )
        self.connect(ret, shallow_dive_area, r.can_dive | r.difficulty("hard"))

        dive_secret_area = self.region(
            "Dive Secret Area",
            [
                "Secret (64)",
                "Shells (8)",
            ],
        )
        # can_door because edict is linked to wall opening
        self.connect(ret, dive_secret_area, r.can_dive & r.can_door)

        past_button_area = self.region(
            "Past Button Area",
            [
                "Green Armor (33)",
                "Large Medkit (17)",
                "Shells (13)",
                "Large Medkit (15)",
                "Spikes (14)",
            ],
        )
        self.connect(
            ret, past_button_area, r.can_button | (r.jump & r.difficulty("hard"))
        )

        first_floor_area = self.region(
            "First Floor",
            [
                "Red Armor (32)",
                "Large Medkit (37)",
                "Spikes (19)",
                "Shells (20)",
                "Shells (21)",
                "Biosuit (26)",
                "Lightning (79)",
                "Grenadelauncher (27)",
                "Cells (80)",
                "Rockets (28)",
                "Megahealth (25)",
                "Large Medkit (24)",
                "Rockets (23)",
                "Gold Key (43)",
                "Large Medkit (69)",
                "Large Medkit (68)",
                "Rockets (49)",
                "Spikes (58)",
                "Quad Damage (22)",
            ],
        )
        self.connect(
            past_button_area,
            first_floor_area,
            r.bigjump_hard | r.can_button,
        )
        self.restrict("Red Armor (32)", r.can_button)
        self.restrict("Large Medkit (37)", r.can_button)
        self.restrict("Large Medkit (68)", r.can_dive)
        self.restrict("Large Medkit (69)", r.can_dive)
        self.restrict("Rockets (49)", (r.can_dive | r.difficulty("hard")))
        self.restrict("Spikes (58)", (r.can_dive | r.difficulty("hard")))
        self.restrict("Quad Damage (22)", (r.can_dive | r.difficulty("hard")))

        wall_secret_area = self.region(
            "Wall Secret Area",
            [
                "Quad Damage (62)",
                "Red Armor (61)",
                "Secret (63)",
            ],
        )
        self.connect(
            first_floor_area,
            wall_secret_area,
            r.can_shootswitch | r.bigjump_hard,
        )

        dive_hallway = self.region(
            "Dive Hallway",
            [
                "Large Medkit (1)",
                "Large Medkit (2)",
                "Spikes (50)",
            ],
        )
        self.connect(
            first_floor_area,
            dive_hallway,
            (r.biosuit(1) & r.can_dive) | r.bigjump_hard,
        )
        past_acid_lake = self.region(
            "Past Acid Lake",
            [
                "Shells (51)",
                "Shells (29)",
                "Shells (52)",
                "Large Medkit (44)",
                "Large Medkit (45)",
                "Supernailgun (71)",
                "Spikes (59)",
                "Large Medkit (46)",
                "Spikes (60)",
                "Spikes (53)",
                "Shells (39)",
                "Large Medkit (38)",
                "Large Medkit (48)",
                "Cells (75)",
                "Cells (76)",
                "Large Medkit (47)",
                "Lightning (74)",
            ],
        )
        self.connect(
            first_floor_area,
            past_acid_lake,
            r.can_shootswitch & r.jump | r.bigjump_hard,
        )

        past_elevator_area = self.region(
            "Past Elevator",
            [
                "Large Medkit (30)",
                "Invulnerability (81)",
                "Small Medkit (31)",
                "Large Medkit (66)",
                "Large Medkit (65)",
                "Large Medkit (67)",
            ],
        )
        self.connect(past_acid_lake, past_elevator_area, r.can_button)
        self.restrict("Large Medkit (66)", r.can_door)
        self.restrict("Large Medkit (65)", r.can_door)
        self.restrict("Large Medkit (67)", r.can_door)

        past_gold_door_area = self.region(
            "Past Gold Door",
            [
                "Large Medkit (41)",
                "Invisibility (82)",
                "Large Medkit (40)",
                "Rockets (42)",
                "Exit",
                "All Kills (83)",
            ],
        )
        self.connect(past_elevator_area, past_gold_door_area, self.gold_key)
        self.restrict("Exit", r.can_door)
        self.restrict("All Kills (83)", r.difficult_combat)

        return ret
