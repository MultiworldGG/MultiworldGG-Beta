from typing import Dict

from worlds.monster_sanctuary import encounters as ENCOUNTERS, MonsterSanctuaryWorld
from worlds.monster_sanctuary.tests.Monsters.Test_MonsterRandomizerBase import TestMonsterRandomizerBase


class TestMonsterRandomizerShuffle(TestMonsterRandomizerBase):
    options = {
        "randomize_monsters": 2
    }

    def test_monsters_are_where_they_are_supposed_to_be(self):
        """Ensures that all monster locations contain the correct monster based on the shuffle logic"""
        for encounter_name, encounter in ENCOUNTERS.encounter_data.items():
            for i in range(len(encounter.monsters)):
                location_name = f"{encounter_name}_{i}"
                location = self.multiworld.get_location(location_name, 1)
                expected = self.multiworld.worlds[1].species_swap[encounter.monsters[i].name]

                with self.subTest(f"Monster should be {expected.name}",
                                  actual=location.item.name,
                                  location_name=location_name):
                    self.assertEqual(expected.name, location.item.name)

    def test_all_monsters_shuffled(self):
        for name, monster in ENCOUNTERS.monster_data.items():
            with self.subTest("Should be shuffled", name=name):
                self.assertIn(name, self.multiworld.worlds[1].species_swap)

    def test_monsters_only_appear_once(self):
        swapped_names = [monster.name for name, monster in self.multiworld.worlds[1].species_swap.items()]
        for name, monster in ENCOUNTERS.monster_data.items():
            with self.subTest("Should only show up once", name=name):
                self.assertEqual(1, swapped_names.count(name))

    def test_monster_eggs_in_item_pool(self):
        world = self.multiworld.worlds[1]
        item_names = [item.name for item in self.multiworld.itempool]

        def test_egg_is_in_item_pool(monster_name, swap_species: bool = True):
            monster = world.species_swap[monster_name] if swap_species else ENCOUNTERS.get_monster(monster_name)
            with self.subTest("Egg is in item pool", monster=monster.name):
                self.assertIn(monster.egg_name(), item_names)

        test_egg_is_in_item_pool("Mad Lord")
        test_egg_is_in_item_pool("Plague Egg")
        test_egg_is_in_item_pool("Tanuki")
        test_egg_is_in_item_pool("Sizzle Knight")
        test_egg_is_in_item_pool("Ninki")

        test_egg_is_in_item_pool("Akhlut", False)
        test_egg_is_in_item_pool("Krakaturtle", False)
        test_egg_is_in_item_pool("Gryphonix", False)

    def test_shuffled_tanuki_is_available(self):
        monster = self.multiworld.worlds[1].species_swap["Tanuki"]
        location = self.multiworld.get_location("Menu_0_0", self.player)
        self.assertEqual(location.item.name, monster.name)
