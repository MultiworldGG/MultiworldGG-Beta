import unittest
from unittest.mock import Mock, patch, MagicMock
from BaseClasses import ItemClassification, MultiWorld
import copy

from . import PoeTestBase
from .. import Items, Locations, Options
from ..Options import PathOfExileOptions
from .. import setup_early_items, setup_character_items, get_goal_act
from ..data import ItemTable


class TestSetupEarlyItems(PoeTestBase):
    """Test setup_early_items function"""
    
    def setUp(self):
        super().setUp()
        
        # Create a mock world object with the necessary attributes
        self.world = Mock()
        self.world.goal_act = 5
        self.world.player = 1
        
        # Create properly structured mock items for items_to_place
        self.world.items_to_place = {
            1: {"id": 1, "name": "Random Sword", "category": ["Random Gear"]},
            2: {"id": 2, "name": "Progressive Sword", "category": ["Progressive Gear"]},
            3: {"id": 3, "name": "Life Flask", "category": ["Flask"]},
            100: {"id": 100, "name": "Progressive passive point", "category": ["Passive"], "count": 10},
            101: {"id": 101, "name": "Low Level Gem", "category": ["MainSkillGem"], "reqLevel": 10},
            102: {"id": 102, "name": "High Level Gem", "category": ["SupportGem"], "reqLevel": 80},
            200: {"id": 200, "name": "Progressive max links - Weapon", "category": ["max links"], "count": 1},
            300: {"id": 300, "name": "Juggernaut", "category": ["Ascendancy", "Marauder Class"]},
            301: {"id": 301, "name": "Berserker", "category": ["Ascendancy", "Marauder Class"]},
            302: {"id": 302, "name": "Chieftain", "category": ["Ascendancy", "Marauder Class"]},
            400: {"id": 400, "name": "Ascendant", "category": ["Ascendancy", "Scion Class"]},
            500: {"id": 500, "name": "Marauder", "category": ["Marauder Class"]},
            501: {"id": 501, "name": "Witch", "category": ["Witch Class"]},
            502: {"id": 502, "name": "Ranger", "category": ["Ranger Class"]},
            600: {"id": 600, "name": "Progressive Flask Slots", "category": ["Flask"], "count": 5}
        }
        
        self.world.item_name_to_id = {item["name"]: item["id"] for item in self.world.items_to_place.values()}
        self.world.remove_and_create_item_by_itemdict = Mock()
        self.world.precollect = Mock()
        self.world.random = Mock()
        
        # Mock options
        self.mock_options = Mock(spec=PathOfExileOptions)
        self.mock_options.progressive_gear = Mock()
        self.mock_options.progressive_gear.value = 0
        self.mock_options.progressive_gear.option_enabled = 0
        self.mock_options.progressive_gear.option_disabled = 1
        self.mock_options.progressive_gear.option_progressive_except_for_unique = 2
        
        self.mock_options.gucci_hobo_mode = Mock()
        self.mock_options.gucci_hobo_mode.value = 0
        self.mock_options.gucci_hobo_mode.option_disabled = 0
        self.mock_options.gucci_hobo_mode.option_allow_one_slot_of_normal_rarity = 1
        self.mock_options.gucci_hobo_mode.option_no_non_unique_items = 2
        
        self.mock_options.add_passive_skill_points_to_item_pool = Mock()
        self.mock_options.add_passive_skill_points_to_item_pool.value = True
        
        self.mock_options.gear_upgrades = Mock()
        self.mock_options.gear_upgrades.value = 0
        self.mock_options.gear_upgrades.option_no_gear_unlocked = 0
        self.mock_options.gear_upgrades.option_all_gear_unlocked_at_start = 1
        self.mock_options.gear_upgrades.option_all_normal_and_unique_gear_unlocked = 2
        self.mock_options.gear_upgrades.option_all_normal_gear_unlocked = 3
        self.mock_options.gear_upgrades.option_all_uniques_unlocked = 4
        
        self.mock_options.add_flasks_to_item_pool = Mock()
        self.mock_options.add_flasks_to_item_pool.value = True
        
        self.mock_options.add_max_links_to_item_pool = Mock()
        self.mock_options.add_max_links_to_item_pool.value = True
        
        self.mock_options.add_skill_gems_to_item_pool = True
        self.mock_options.add_support_gems_to_item_pool = True

        
    @patch('worlds.poe.setup_character_items')
    @patch('worlds.poe.Items.get_gear_items')
    @patch('worlds.poe.Items.item_table')
    def test_progressive_gear_enabled_removes_random_gear(self, mock_item_table, mock_get_gear, mock_setup_character):
        """Test progressive gear enabled removes random gear items"""
        self.mock_options.progressive_gear.value = self.mock_options.progressive_gear.option_enabled
        
        # Mock the item_table to return empty for unique checks
        mock_item_table.values.return_value = []
        
        # Mock get_gear_items to return empty list to avoid the category KeyError
        mock_get_gear.return_value = []
        
        # Mock some items in items_to_place
        self.world.items_to_place = {
            1: {"id": 1, "name": "Random Sword", "category": ["Random Gear"]},
            2: {"id": 2, "name": "Progressive Sword", "category": ["Progressive Gear"]},
            3: {"id": 3, "name": "Life Flask", "category": ["Flask"]}
        }
        self.world.item_name_to_id = {
            "Random Sword": 1,
            "Progressive Sword": 2,
            "Life Flask": 3
        }
        
        with patch('worlds.poe.Items.get_by_category') as mock_get_category:
            mock_get_category.return_value = [{"name": "Random Sword", "id": 1}]
            with patch('worlds.poe.Locations.acts', {5: {"maxMonsterLevel": 50}}):
                with patch('worlds.poe.Items.get_by_name', return_value=None):
                    setup_early_items(self.world, self.mock_options)
        
        # Random gear should be removed
        self.assertNotIn(1, self.world.items_to_place)
        self.assertIn(2, self.world.items_to_place)  # Progressive gear should remain
        
    @patch('worlds.poe.setup_character_items')
    @patch('worlds.poe.Items.get_gear_items')
    @patch('worlds.poe.Items.item_table')
    def test_progressive_gear_disabled_removes_progressive_gear(self, mock_item_table, mock_get_gear, mock_setup_character):
        """Test progressive gear disabled removes progressive gear items"""
        self.mock_options.progressive_gear.value = self.mock_options.progressive_gear.option_disabled
        
        # Mock the item_table to return empty for unique checks
        mock_item_table.values.return_value = []
        
        # Mock get_gear_items to return empty list to avoid the category KeyError
        mock_get_gear.return_value = []
        
        self.world.items_to_place = {
            1: {"id": 1, "name": "Random Sword", "category": ["Random Gear"]},
            2: {"id": 2, "name": "Progressive Sword", "category": ["Progressive Gear"]},
        }
        self.world.item_name_to_id = {
            "Random Sword": 1,
            "Progressive Sword": 2,
        }
        
        with patch('worlds.poe.Items.get_by_category') as mock_get_category:
            mock_get_category.return_value = [{"name": "Progressive Sword", "id": 2}]
            with patch('worlds.poe.Locations.acts', {5: {"maxMonsterLevel": 50}}):
                with patch('worlds.poe.Items.get_by_name', return_value=None):
                    setup_early_items(self.world, self.mock_options)
        
        # Progressive gear should be removed
        self.assertNotIn(2, self.world.items_to_place)
        self.assertIn(1, self.world.items_to_place)  # Random gear should remain
        
    @patch('worlds.poe.setup_character_items')
    def test_gucci_hobo_mode_upgrades_uniques(self, mock_setup_character):
        """Test gucci hobo mode upgrades unique items to progression"""
        self.mock_options.gucci_hobo_mode.value = self.mock_options.gucci_hobo_mode.option_no_non_unique_items
        
        with patch('worlds.poe.Items.item_table') as mock_item_table:
            unique_item = {"category": ["Unique"], "classification": ItemClassification.filler}
            mock_item_table.values.return_value = [unique_item]
            
            with patch('worlds.poe.Items.get_gear_items') as mock_get_gear:
                mock_get_gear.return_value = []
                with patch('worlds.poe.Locations.acts', {5: {"maxMonsterLevel": 50}}):
                    setup_early_items(self.world, self.mock_options)
        
        # Unique item should be upgraded to progression
        self.assertEqual(unique_item["classification"], ItemClassification.progression)

    @patch('worlds.poe.setup_character_items')
    def test_gem_level_filtering(self, mock_setup_character):
        """Test high level gems are removed from item pool"""
        self.world.items_to_place = {
            1: {"id": 1, "name": "Low Level Gem", "category": ["MainSkillGem"], "reqLevel": 10},
            2: {"id": 2, "name": "High Level Gem", "category": ["SupportGem"], "reqLevel": 80},
            3: {"id": 3, "name": "Normal Item", "category": ["Gear"], "reqLevel": 10}
        }
        
        with patch('worlds.poe.Locations.acts', {5: {"maxMonsterLevel": 50}}):
            setup_early_items(self.world, self.mock_options)
        
        # High level gem should be removed
        self.assertIn(1, self.world.items_to_place)  # Low level gem remains
        self.assertNotIn(2, self.world.items_to_place)  # High level gem removed
        self.assertIn(3, self.world.items_to_place)  # Non-gem item remains


class TestSetupCharacterItems(PoeTestBase):
    """Test setup_character_items function"""
    
    def setUp(self):
        super().setUp()
        
        # Create a mock world object
        self.world = Mock()
        self.world.goal_act = 5
        self.world.player = 1
        
        # Create properly structured mock items for items_to_place
        self.world.items_to_place = {
            1: {"id": 1, "name": "Iron Sword", "category": ["Weapon"]},
            100: {"id": 100, "name": "Progressive max links - Weapon", "category": ["max links"], "count": 1},
            200: {"id": 200, "name": "Life Flask", "category": ["Flask"], "count": 5},
            300: {"id": 300, "name": "Juggernaut", "category": ["Ascendancy", "Marauder Class"]},
            301: {"id": 301, "name": "Berserker", "category": ["Ascendancy", "Marauder Class"]},
            302: {"id": 302, "name": "Chieftain", "category": ["Ascendancy", "Marauder Class"]},
            400: {"id": 400, "name": "Ascendant", "category": ["Ascendancy", "Scion Class"]},
            500: {"id": 500, "name": "Marauder", "category": ["Marauder Class"]},
            501: {"id": 501, "name": "Witch", "category": ["Witch Class"]},
            502: {"id": 502, "name": "Ranger", "category": ["Ranger Class"]},
            600: {"id": 600, "name": "Progressive Flask Slots", "category": ["Flask"], "count": 5}
        }
        
        self.world.item_name_to_id = {item["name"]: item["id"] for item in self.world.items_to_place.values()}
        self.world.items_procollected = {}
        self.world.remove_and_create_item_by_name = Mock()
        self.world.precollect = Mock()
        self.world.create_item = Mock()
        self.world.random = Mock()
        
        # Mock multiworld state
        self.world.multiworld = Mock()
        self.world.multiworld.state = Mock()
        self.world.multiworld.state.count = Mock(return_value=0)
        
        # Mock options
        self.mock_options = Mock(spec=PathOfExileOptions)
        self.mock_options.starting_character = Mock()
        self.mock_options.starting_character.value = 1
        self.mock_options.starting_character.option_scion = 1
        self.mock_options.starting_character.option_marauder = 2
        self.mock_options.starting_character.option_duelist = 3
        self.mock_options.starting_character.option_ranger = 4
        self.mock_options.starting_character.option_shadow = 5
        self.mock_options.starting_character.option_witch = 6
        self.mock_options.starting_character.option_templar = 7
        
        self.mock_options.usable_starting_gear = Mock()
        self.mock_options.usable_starting_gear.value = 0
        self.mock_options.usable_starting_gear.option_starting_weapon_flask_and_gems = 0
        self.mock_options.usable_starting_gear.option_starting_weapon_and_gems = 1
        self.mock_options.usable_starting_gear.option_starting_weapon = 2
        self.mock_options.usable_starting_gear.option_starting_weapon_and_flask_slots = 3
        
        self.mock_options.allow_unlock_of_other_characters = Mock()
        self.mock_options.allow_unlock_of_other_characters.value = True
        
        self.mock_options.ascendancies_available_per_class = Mock()
        self.mock_options.ascendancies_available_per_class.value = 3
        

class TestGetGoalAct(PoeTestBase):
    """Test get_goal_act function"""
    
    def setUp(self):
        super().setUp()
        self.world = Mock()
        self.options = Mock()
        self.options.goal = Mock()
        
        # Set up all goal options
        self.options.goal.option_complete_act_1 = 1
        self.options.goal.option_complete_act_2 = 2
        self.options.goal.option_complete_act_3 = 3
        self.options.goal.option_complete_act_4 = 4
        self.options.goal.option_kauri_fortress_act_6 = 5
        self.options.goal.option_complete_act_6 = 6
        self.options.goal.option_complete_act_7 = 7
        self.options.goal.option_complete_act_8 = 8
        self.options.goal.option_complete_act_9 = 9
        self.options.goal.option_complete_the_campaign = 10
        
    def test_all_goal_act_mappings(self):
        """Test all goal act mappings return correct values"""
        test_cases = [
            (self.options.goal.option_complete_act_1, 1),
            (self.options.goal.option_complete_act_2, 2),
            (self.options.goal.option_complete_act_3, 3),
            (self.options.goal.option_complete_act_4, 4),
            (self.options.goal.option_kauri_fortress_act_6, 5),
            (self.options.goal.option_complete_act_6, 6),
            (self.options.goal.option_complete_act_7, 7),
            (self.options.goal.option_complete_act_8, 8),
            (self.options.goal.option_complete_act_9, 9),
            (self.options.goal.option_complete_the_campaign, 10),
        ]
        
        for goal_value, expected_act in test_cases:
            with self.subTest(goal=goal_value, expected=expected_act):
                self.options.goal.value = goal_value
                result = get_goal_act(self.world, self.options)
                self.assertEqual(result, expected_act)
                
    def test_unknown_goal_returns_11(self):
        """Test unknown goal value returns 11"""
        self.options.goal.value = 999  # Unknown goal
        result = get_goal_act(self.world, self.options)
        self.assertEqual(result, 11)


if __name__ == '__main__':
    unittest.main()