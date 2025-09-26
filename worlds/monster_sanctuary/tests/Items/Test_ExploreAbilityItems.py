from typing import List

from worlds.AutoWorld import call_all
from worlds.monster_sanctuary import items as ITEMS
from worlds.monster_sanctuary.tests import MonsterSanctuaryTestBase


class TestExploreAbilityItems_Disabled(MonsterSanctuaryTestBase):
    run_default_tests = False
    options = {
        "lock_explore_abilities": 0
    }

    def test_no_explore_items_are_in_the_item_pool(self):
        pool = [item.name for item in self.multiworld.itempool]
        ability_items = [item for item in pool
                         if ITEMS.get_item_type(item) == ITEMS.MonsterSanctuaryItemCategory.ABILITY]

        self.assertEqual(len(ability_items), 0)


class TestExploreAbilityItems_Type(MonsterSanctuaryTestBase):
    run_default_tests = False
    options = {
        "lock_explore_abilities": 1
    }

    def test_type_explore_items_are_in_the_item_pool(self):
        pool = [item.name for item in self.multiworld.itempool]
        ability_items = [item for item in pool
                         if ITEMS.get_item_type(item) == ITEMS.MonsterSanctuaryItemCategory.ABILITY]

        self.assertEqual(len(ability_items), len(ITEMS.explore_ability_types))

        for explore_item in ITEMS.explore_ability_types:
            with self.subTest(f"{explore_item} is in the item pool"):
                self.assertIn(explore_item, ability_items)



class TestExploreAbilityItems_Ability(MonsterSanctuaryTestBase):
    run_default_tests = False
    options = {
        "lock_explore_abilities": 2
    }

    def test_ability_explore_items_are_in_the_item_pool(self):
        pool = [item.name for item in self.multiworld.itempool]
        ability_items = [item for item in pool
                         if ITEMS.get_item_type(item) == ITEMS.MonsterSanctuaryItemCategory.ABILITY]

        explore_ability_items = [item.name for item in ITEMS.item_data.values()
                                 if item.category == ITEMS.MonsterSanctuaryItemCategory.ABILITY
                                 and "Ability - " in item.name]

        self.assertEqual(len(ability_items), 41)
        self.assertEqual(len(explore_ability_items), 41)

        for explore_item in explore_ability_items:
            with self.subTest(f"{explore_item} is in the item pool"):
                self.assertIn(explore_item, ability_items)


class TestExploreAbilityItems_Species(MonsterSanctuaryTestBase):
    run_default_tests = False
    options = {
        "lock_explore_abilities": 3
    }

    def test_species_explore_items_are_in_the_item_pool(self):
        pool = [item.name for item in self.multiworld.itempool]
        ability_items = [item for item in pool
                         if ITEMS.get_item_type(item) == ITEMS.MonsterSanctuaryItemCategory.ABILITY]

        explore_ability_items = [item.name for item in ITEMS.item_data.values()
                                 if item.category == ITEMS.MonsterSanctuaryItemCategory.ABILITY
                                 and "Ability - " not in item.name
                                 and "Progressive" not in item.name
                                 and "Combo" not in item.name
                                 and item.name not in ITEMS.explore_ability_types]

        self.assertEqual(len(explore_ability_items), len(ability_items))

        for explore_item in explore_ability_items:
            with self.subTest(f"{explore_item} is in the item pool"):
                self.assertIn(explore_item, ability_items)


class TestExploreAbilityItems_Progressive(MonsterSanctuaryTestBase):
    run_default_tests = False
    options = {
        "lock_explore_abilities": 4
    }

    def test_progressive_explore_items_are_in_the_item_pool(self):
        pool = [item.name for item in self.multiworld.itempool]
        ability_items = [item for item in pool
                         if ITEMS.get_item_type(item) == ITEMS.MonsterSanctuaryItemCategory.ABILITY]
        explore_item = {tuple[0]:tuple[1] for tuple in ITEMS.explore_ability_progression}

        self.assertEqual(sum(explore_item.values()), len(ability_items))

        for explore_item, count in explore_item.items():
            with self.subTest(f"{explore_item} is in the item pool {count} times"):
                self.assertEqual(count, ability_items.count(explore_item))


class TestExploreAbilityItems_Combo(MonsterSanctuaryTestBase):
    run_default_tests = False
    options = {
        "lock_explore_abilities": 5
    }

    def test_combo_explore_items_are_in_the_item_pool(self):
        pool = [item.name for item in self.multiworld.itempool]
        ability_items = [item for item in pool
                         if ITEMS.get_item_type(item) == ITEMS.MonsterSanctuaryItemCategory.ABILITY]
        explore_item = {tuple[0]:tuple[1] for tuple in ITEMS.explore_ability_combo}

        self.assertEqual(sum(explore_item.values()), len(ability_items))

        for explore_item, count in explore_item.items():
            with self.subTest(f"{explore_item} is in the item pool {count} times"):
                self.assertEqual(count, ability_items.count(explore_item))