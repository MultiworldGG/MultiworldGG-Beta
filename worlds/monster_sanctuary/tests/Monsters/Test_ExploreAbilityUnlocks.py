from typing import Dict

from worlds.monster_sanctuary import encounters as ENCOUNTERS
from worlds.monster_sanctuary import items as ITEMS
from worlds.monster_sanctuary.tests.Monsters.Test_MonsterRandomizerBase import TestMonsterRandomizerBase


class TestMonsterExploreItemValidity(TestMonsterRandomizerBase):
    run_default_tests = False
    options = {
        "randomize_monsters": 0
    }

    def test_all_monsters_have_species_items(self):
        for monster_data in ENCOUNTERS.monster_data.values():
            with self.subTest(f"Testing that {monster_data.name} has a valid Species explore item"):
                self.assertTrue(monster_data.species_explore_item is not None)
                self.assertTrue(monster_data.species_explore_item != "")
                self.assertIn(monster_data.species_explore_item, ITEMS.item_data.keys())

    def test_all_monsters_have_ability_items(self):
        for monster_data in ENCOUNTERS.monster_data.values():
            with self.subTest(f"Testing that {monster_data.name} has valid Ability explore item"):
                self.assertTrue(monster_data.ability_explore_item is not None)
                self.assertTrue(monster_data.ability_explore_item != "")
                self.assertIn(monster_data.ability_explore_item, ITEMS.item_data.keys())

    def test_all_monsters_have_type_items(self):
        for monster_data in ENCOUNTERS.monster_data.values():
            with self.subTest(f"Testing that {monster_data.name} a valid Type explore item"):
                self.assertTrue(monster_data.type_explore_item is not None)
                self.assertTrue(monster_data.type_explore_item != "")
                self.assertIn(monster_data.type_explore_item, ITEMS.item_data.keys())

    def test_all_monsters_have_progression_items(self):
        for monster_data in ENCOUNTERS.monster_data.values():
            with self.subTest(f"Testing that {monster_data.name} has a valid Progression explore item"):
                self.assertTrue(monster_data.progressive_explore_item[0] is not None)
                self.assertTrue(monster_data.progressive_explore_item[0] != "")
                self.assertGreaterEqual(monster_data.progressive_explore_item[1], 1)
                self.assertIn(monster_data.progressive_explore_item[0], ITEMS.item_data.keys())

    def test_all_monsters_have_combo_items(self):
        for monster_data in ENCOUNTERS.monster_data.values():
            with self.subTest(f"Testing that {monster_data.name} has valid Combo explore items"):
                for item_name, quantity in monster_data.combo_explore_item.items():
                    self.assertTrue(item_name is not None)
                    self.assertTrue(item_name != "")
                    self.assertGreaterEqual(quantity, 1)
                    self.assertIn(item_name, ITEMS.item_data.keys())


class ExploreAbilityTests(TestMonsterRandomizerBase):
    run_default_tests = False

    def test_explore_items_are_in_item_pool(self):
        if self.options.get("lock_explore_abilities") is None:
            return

        item_pool = [item.name for item in self.multiworld.itempool]
        item_data = [item.name for item in ITEMS.get_explore_ability_items(self.options["lock_explore_abilities"])]
        type_items: Dict[str, int] = { item: item_data.count(item) for item in item_data }

        for item, count in type_items.items():
            with self.subTest(f"{item} is in the item pool {count} time(s)"):
                self.assertIn(item, item_pool)
                self.assertEqual(item_pool.count(item), count)

    def test_monsters_require_item_to_use_explore_ability(self):
        if self.options.get("lock_explore_abilities") is None:
            return

        for monster_name, monster_data in ENCOUNTERS.monster_data.items():
            if self.multiworld.worlds[1].options.lock_explore_abilities == 0:
                self.assert_ability_is_usable(monster_name)
            elif self.multiworld.worlds[1].options.lock_explore_abilities == 1:
                self.assert_explore_item_is_required(monster_name, monster_data.type_explore_item)
            elif self.multiworld.worlds[1].options.lock_explore_abilities == 2:
                self.assert_explore_item_is_required(monster_name, monster_data.ability_explore_item)
            if self.multiworld.worlds[1].options.lock_explore_abilities == 3:
                self.assert_explore_item_is_required(monster_name, monster_data.species_explore_item)
            if self.multiworld.worlds[1].options.lock_explore_abilities == 4:
                self.assert_explore_progression_is_required(monster_name,
                                                            monster_data.progressive_explore_item[0],
                                                            monster_data.progressive_explore_item[1])
            if self.multiworld.worlds[1].options.lock_explore_abilities == 5:
                self.assert_explore_combo_is_required(monster_name, monster_data.combo_explore_item)


class TestExploreAbilities_Type(ExploreAbilityTests):
    options = {
        "lock_explore_abilities": 1
    }


class TestExploreAbilities_Ability(ExploreAbilityTests):
    options = {
        "lock_explore_abilities": 2
    }


class TestExploreAbilities_Species(ExploreAbilityTests):
    options = {
        "lock_explore_abilities": 3
    }


class TestExploreAbilities_Progression(ExploreAbilityTests):
    options = {
        "lock_explore_abilities": 4
    }


class TestExploreAbilities_Combo(ExploreAbilityTests):
    options = {
        "lock_explore_abilities": 5
    }
