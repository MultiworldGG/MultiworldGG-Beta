from typing import List, Dict

from BaseClasses import CollectionState, ItemClassification
from test.bases import WorldTestBase
from worlds.monster_sanctuary.rules import can_use_ability
from worlds.monster_sanctuary import encounters as ENCOUNTERS


class TestMonsterRandomizerBase(WorldTestBase):
    game = "Monster Sanctuary"
    player: int = 1

    def collect_pre_evolution(self, monster_name: str, state: CollectionState):
        monster = ENCOUNTERS.get_monster(monster_name)
        if monster.is_evolved():
            state.collect(self.multiworld.worlds[1].create_item("Tree of Evolution Access"))
            state.collect(self.multiworld.worlds[1].create_item(monster.pre_evolutions[0].monster))
            item = self.multiworld.worlds[1].create_item(monster.pre_evolutions[0].catalyst)
            item.classification = ItemClassification.progression
            state.collect(item)

    def assert_ability_is_usable(self, monster_name: str):
        with self.subTest(f"{monster_name}'s ability is usable"):
            state = CollectionState(self.multiworld)
            self.assertFalse(can_use_ability(monster_name, state, self.player))

            state.collect(self.multiworld.worlds[1].create_item(monster_name))
            self.assertTrue(can_use_ability(monster_name, state, self.player))

    def assert_explore_item_is_required(self, monster_name: str, explore_item: str):
        with self.subTest(f"{monster_name} requires {explore_item} to use ability"):
            # Instantiate a new collection state so each run can have its own
            state = CollectionState(self.multiworld)
            self.assertFalse(can_use_ability(monster_name, state, self.player))

            state.collect(self.multiworld.worlds[1].create_item(monster_name))
            self.assertFalse(can_use_ability(monster_name, state, self.player))

            if self.multiworld.worlds[1].options.lock_explore_abilities != 0:
                self.collect_pre_evolution(monster_name, state)

                state.collect(self.multiworld.worlds[1].create_item(explore_item))
                can_use = can_use_ability(monster_name, state, self.player)
                if not can_use:
                    pass

                self.assertTrue(can_use)

    def assert_explore_progression_is_required(self, monster_name: str, explore_item: str, quantity: int):
        with self.subTest(f"{monster_name} requires {quantity} {explore_item} to use ability"):
            # Instantiate a new collection state so each run can have its own
            state = CollectionState(self.multiworld)
            state.collect(self.multiworld.worlds[1].create_item(monster_name))
            self.assertFalse(can_use_ability(monster_name, state, self.player))

            self.collect_pre_evolution(monster_name, state)

            # +1 here because we want to loop from 0 to the quantity, including that value
            # as when i == quantity, we should be asserting that the monster can use its ability
            for i in range(quantity + 1):
                can_use = can_use_ability(monster_name, state, self.player)
                should_be_able_to_use = i == quantity
                self.assertEqual(can_use, should_be_able_to_use)
                state.collect(self.multiworld.worlds[1].create_item(explore_item))

    def assert_explore_combo_is_required(self, monster_name: str, combo_items: Dict[str, int]):
        text = " and ".join([f"{quant} {name}" for name, quant in combo_items.items()])
        with self.subTest(f"{monster_name} requires {text} to use ability"):
            state = CollectionState(self.multiworld)
            state.collect(self.multiworld.worlds[1].create_item(monster_name))
            self.assertFalse(can_use_ability(monster_name, state, self.player))

            self.collect_pre_evolution(monster_name, state)

            requirements = []
            for name, quant in combo_items.items():
                for i in range(quant):
                    requirements.append(name)

            for i in range(len(requirements)):
                can_use = can_use_ability(monster_name, state, self.player)
                should_be_able_to_use = i == len(requirements)
                self.assertEqual(can_use, should_be_able_to_use)
                state.collect(self.multiworld.worlds[1].create_item(requirements[i]))

    def test_all_monster_locations_exist(self):
        for encounter_name, encounter in self.multiworld.worlds[1].encounters.items():
            for i in range(len(encounter.monsters)):
                location_name = f"{encounter_name}_{i}"

                with self.subTest("Location should exist", location_name=location_name):
                    location = self.multiworld.get_location(location_name, 1)
                    self.assertIsNotNone(location)

    def test_special_monsters_are_not_placed(self):
        special_monsters = ["Spectral Wolf", "Spectral Toad", "Spectral Eagle", "Spectral Lion", "Bard"]
        for encounter_name, encounter in self.multiworld.worlds[1].encounters.items():
            for monster in encounter.monsters:
                with self.subTest("Monster is not a special monster", monster=monster.name):
                    self.assertTrue(monster not in special_monsters)

    def test_no_monsters_placed_where_they_should_not_be(self):
        for encounter_name, encounter in self.multiworld.worlds[1].encounters.items():
            for monster in encounter.monsters:
                with self.subTest("Monster is not placed where it shouldn't be", monster=monster.name):
                    self.assertTrue(monster not in encounter.monster_exclusions)

    def test_required_monsters_are_placed(self):
        def test_monsters(msg: str, abilities: List[str]):
            with self.subTest(msg):
                found: bool = False
                for monster in monsters:
                    if set(abilities) & set(monster.groups):
                        found = True
                        break
                self.assertTrue(found)

        monsters = [monster for monster in ENCOUNTERS.get_monsters_in_area(
            self.multiworld.worlds[1],
            "MountainPath", "BlueCave")]
        test_monsters("Breakable Walls shows up in Mountain Path or Blue Caves", ["Breakable Walls"])
        test_monsters("Flying shows up in Mountain Path or Blue Caves", ["Flying"])

        monsters = [monster for monster in ENCOUNTERS.get_monsters_in_area(
            self.multiworld.worlds[1],
            "MountainPath", "BlueCave", "StrongholdDungeon", "AncientWoods", "SnowyPeaks", "SunPalace")]
        test_monsters("Mount shows up before Magma Chamber",
                      ["Mount", "Charging Mount", "Tar Mount", "Sonar Mount"])

        monsters = [monster for monster in ENCOUNTERS.get_monsters_in_area(
            self.multiworld.worlds[1],
            "MountainPath", "BlueCave", "StrongholdDungeon", "SnowyPeaks", "SunPalace", "AncientWoods")]
        test_monsters("Water Orb shows up before Horizon Beach", ["Water Orbs"])
        test_monsters("Fire Orb shows up before Horizon Beach", ["Fire Orbs"])
        test_monsters("Lightning Orb shows up before Horizon Beach", ["Lightning Orbs"])
        test_monsters("Earth Orb shows up before Horizon Beach", ["Earth Orbs"])

    def test_evolved_monster_only_unlock_pre_evolved_ability(self):
        if self.options.get("lock_explore_abilities") is not None:
            return

        for monster_data in ENCOUNTERS.monster_data.values():
            if not monster_data.is_evolved():
                continue

            for evo_data in monster_data.pre_evolutions:
                with self.subTest(f"Testing that {monster_data.name}'s ability is only usable if you can evolve {evo_data.monster}"):
                    state = CollectionState(self.multiworld)
                    self.assertFalse(can_use_ability(monster_data.name, state, 1))

                    state.collect(self.multiworld.worlds[1].create_item("Tree of Evolution Access"))
                    self.assertFalse(can_use_ability(monster_data.name, state, 1))

                    state.collect(self.multiworld.worlds[1].create_item(evo_data.monster))
                    self.assertFalse(can_use_ability(monster_data.name, state, 1))

                    item = self.multiworld.worlds[1].create_item(evo_data.catalyst)
                    item.classification = ItemClassification.progression
                    state.collect(item)
                    self.assertTrue(can_use_ability(monster_data.name, state, 1))

    def test_dodo_egg_is_in_item_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]

        def test_item_is_in_item_pool(egg_name):
            with self.subTest("Egg is in item pool", egg=egg_name):
                self.assertIn(egg_name, item_names)

        test_item_is_in_item_pool("Dodo Egg")
        test_item_is_in_item_pool("Light-Shifted Dodo Egg")
        test_item_is_in_item_pool("Dark-Shifted Dodo Egg")



class TestMonsterRandomizerOff(TestMonsterRandomizerBase):
    options = {
        "randomize_monsters": 0
    }

    def test_monsters_are_not_randomized(self):
        for encounter_name, encounter in ENCOUNTERS.encounter_data.items():
            for i in range(len(encounter.monsters)):
                location_name = f"{encounter.name}_{i}"
                location = self.multiworld.get_location(location_name, 1)

                with self.subTest("Monsters should match", name=encounter.monsters[i].name):
                    self.assertIsNotNone(location)
                    self.assertEqual(location.item.name, encounter.monsters[i].name)