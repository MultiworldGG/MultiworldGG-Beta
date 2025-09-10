import unittest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
import asyncio
from dataclasses import dataclass
from typing import Dict, Any, List

import sys
import os

# Add vendor libraries to path for dependencies like pygetwindow
current_dir = os.path.dirname(__file__)
poe_dir = os.path.dirname(current_dir)
worlds_dir = os.path.dirname(poe_dir)
archipelago_dir = os.path.dirname(worlds_dir)
poe_client_vendor_dir = os.path.join(archipelago_dir, "lib", "poe_client_vendor")

if poe_client_vendor_dir not in sys.path:
    sys.path.insert(0, poe_client_vendor_dir)

from . import PoeTestBase
from .. import Items, Locations, Options
from ..poeClient import validationLogic, gggAPI


class TestValidationLogic(PoeTestBase):

    def setUp(self):
        """Set up test fixtures"""
        super().setUp()
        
        # Mock character data
        self.mock_character = Mock(spec=gggAPI.Character)
        self.mock_character.class_ = "Marauder"
        self.mock_character.level = 10
        self.mock_character.inventory = []
        self.mock_character.equipment = []
        
        # Mock passives attribute for character
        self.mock_passives = Mock()
        self.mock_passives.hashes = []  # Empty list for no passive points used
        self.mock_character.passives = self.mock_passives
        
        # Mock context
        self.mock_ctx = Mock()
        self.mock_ctx.character_name = "TestCharacter"
        self.mock_ctx.game_options = {
            "goal": Options.Goal.option_complete_act_1,
            "passivePointsAsItems": True,
            "gucciHobo": 0,
            "ProgressiveGear": True,
            "add_leveling_up_to_location_pool": True,
            "bosses_for_goal": []
        }
        self.mock_ctx.items_received = []
        self.mock_ctx.missing_locations = set()
        self.mock_ctx.locations_info = {}
        self.mock_ctx.slot = 1
        self.mock_ctx.tts_options = Mock()
        self.mock_ctx.tts_options.enable = True
        self.mock_ctx.tts_options.speed = 250
        
        # Mock items
        self.mock_items = [
            {"name": "Marauder", "id": 1},
            {"name": "Progressive passive point", "id": 2},
            {"name": "Progressive Normal Flask", "id": 3},
            {"name": "Progressive Magic Flask", "id": 4},
            {"name": "Progressive BodyArmour", "id": 5},
            {"name": "Normal BodyArmour", "id": 6},
            {"name": "Magic BodyArmour", "id": 7},
            {"name": "Rare BodyArmour", "id": 8},
            {"name": "Unique BodyArmour", "id": 9}
        ]

    def test_unit_test_works(self):
        """Basic test to ensure test framework is working"""
        assert True

    def test_rarity_check_with_progressive_gear_normal(self):
        """Test rarity check with progressive gear for normal items"""
        total_received_items_names = ["Progressive BodyArmour"]
        
        # Should allow normal gear with 1+ progressive items
        result = validationLogic.rarity_check(total_received_items_names, "Normal", "BodyArmour")
        self.assertIsNone(result)
        
        # Should reject without progressive items
        result = validationLogic.rarity_check([], "Normal", "BodyArmour")
        self.assertEqual(result, "BodyArmour")

    def test_rarity_check_with_progressive_gear_magic(self):
        """Test rarity check with progressive gear for magic items"""
        total_received_items_names = ["Progressive BodyArmour", "Progressive BodyArmour"]
        
        # Should allow magic gear with 2+ progressive items
        result = validationLogic.rarity_check(total_received_items_names, "Magic", "BodyArmour")
        self.assertIsNone(result)
        
        # Should reject with only 1 progressive item
        result = validationLogic.rarity_check(["Progressive BodyArmour"], "Magic", "BodyArmour")
        self.assertEqual(result, "BodyArmour")

    def test_rarity_check_with_progressive_gear_rare(self):
        """Test rarity check with progressive gear for rare items"""
        total_received_items_names = ["Progressive BodyArmour"] * 3
        
        # Should allow rare gear with 3+ progressive items
        result = validationLogic.rarity_check(total_received_items_names, "Rare", "BodyArmour")
        self.assertIsNone(result)
        
        # Should reject with only 2 progressive items
        result = validationLogic.rarity_check(["Progressive BodyArmour"] * 2, "Rare", "BodyArmour")
        self.assertEqual(result, "BodyArmour")

    def test_rarity_check_with_progressive_gear_unique(self):
        """Test rarity check with progressive gear for unique items"""
        total_received_items_names = ["Progressive BodyArmour"] * 4
        
        # Should allow unique gear with 4+ progressive items
        result = validationLogic.rarity_check(total_received_items_names, "Unique", "BodyArmour")
        self.assertIsNone(result)
        
        # Should reject with only 3 progressive items
        result = validationLogic.rarity_check(["Progressive BodyArmour"] * 3, "Unique", "BodyArmour")
        self.assertEqual(result, "BodyArmour")

    def test_validate_passive_points_with_items_enabled(self):
        """Test passive point validation when passive points as items is enabled"""
        self.mock_character.level = 5
        
        # Mock character with 3 passive points allocated but only 2 received
        self.mock_passives.hashes = [1, 2, 3]  # 3 passives allocated
        total_received_items = [
            {"name": "Progressive passive point"},
            {"name": "Progressive passive point"}
        ]
        
        # Should have errors if not enough passive points (3 used vs 2 available)
        errors = validationLogic.validate_passive_points(
            self.mock_character, self.mock_ctx, total_received_items, 0
        )
        self.assertGreater(len(errors), 0, f"Expected passive point errors, got: {errors}")
        
        # Add enough passive points (should now have 5 total)
        total_received_items.extend([{"name": "Progressive passive point"}] * 3)
        errors = validationLogic.validate_passive_points(
            self.mock_character, self.mock_ctx, total_received_items, 0
        )
        self.assertEqual(len(errors), 0, f"Should have no errors with enough passives, got: {errors}")

    def test_validate_passive_points_with_items_disabled(self):
        """Test passive point validation when passive points as items is disabled"""
        self.mock_ctx.game_options["passivePointsAsItems"] = False
        self.mock_character.level = 5
        
        # Should have no errors regardless of items when disabled
        errors = validationLogic.validate_passive_points(
            self.mock_character, self.mock_ctx, [], 0
        )
        self.assertEqual(len(errors), 0)

    @patch('worlds.poe.poeClient.validationLogic.Items.item_table')
    def test_validate_char_equipment_missing_class(self, mock_item_table):
        """Test character validation when missing starting class"""
        mock_item_table.get.return_value = None
        
        # Provide some items but not the character class
        total_received_items = [{"name": "Some Other Item"}]
        
        errors = validationLogic.validate_char_equipment(
            self.mock_character, self.mock_ctx, total_received_items
        )
        
        # Should have error for missing class
        class_errors = [e for e in errors if e is not None and "Marauder" in str(e)]
        self.assertGreater(len(class_errors), 0, f"Expected Marauder class error, got: {errors}")

    def test_validate_char_equipment_flask_validation(self):
        """Test flask validation logic"""
        # Test with flasks to exceed the amount allowed
        mock_flasks = []
        for i in range(5):  # Create 5 normal flasks
            mock_flask = Mock()
            mock_flask.rarity = "Normal"
            mock_flask.baseType = f"Life Flask {i}"
            mock_flask.inventoryId = "Flask"
            mock_flask.socketedItems = []
            mock_flask.properties = []
            mock_flasks.append(mock_flask)
        
        self.mock_character.equipment = mock_flasks
        
        # With no flask unlocks (no Progressive Normal Flask items)
        total_received_items = [{"name": "Marauder"}]
        
        errors = validationLogic.validate_char_equipment(
            self.mock_character, self.mock_ctx, total_received_items
        )

        non_none_errors = [e for e in errors if e is not None]
        flask_errors = [e for e in non_none_errors if "flask" in str(e).lower()]
        self.assertGreater(len(flask_errors), 0, f"Expected flask errors, got: {non_none_errors}")

    def test_validate_char_equipment_magic_flask_validation(self):
        """Test flask validation logic"""
        # Test with flasks to exceed the amount allowed
        mock_flasks = []
        for i in range(2):  # Create 2 Magic flasks
            mock_flask = Mock()
            mock_flask.rarity = "Magic"
            mock_flask.baseType = f"Life Flask {i}"
            mock_flask.inventoryId = "Flask"
            mock_flask.socketedItems = []
            mock_flask.properties = []
            mock_flasks.append(mock_flask)

        self.mock_character.equipment = mock_flasks

        # With no flask unlocks (no Progressive Normal Flask items)
        total_received_items = [{"name": "Marauder"},
                                {"name": "Progressive Flask Unlock"},
                                {"name": "Progressive Flask Unlock"},
                                {"name": "Progressive Flask Unlock"},
                                {"name": "Progressive Flask Unlock"},
                                {"name": "Progressive Flask Unlock"},
                                {"name": "Progressive Flask Unlock"},
                                {"name": "Progressive Flask Unlock"},
                                ]

        errors = validationLogic.validate_char_equipment(
            self.mock_character, self.mock_ctx, total_received_items
        )

        non_none_errors = [e for e in errors if e is not None]
        flask_errors = [e for e in non_none_errors if "flask" in str(e).lower()]
        self.assertEqual(len(flask_errors), 0, f"Expected flask errors, got: {non_none_errors}")

    def test_validate_char_equipment_gucci_hobo_mode(self):
        """Test Gucci Hobo Mode validation"""
        self.mock_ctx.game_options["gucciHobo"] = 3  # No non-unique items
        
        # Mock character with non-unique gear
        mock_gear = Mock()
        mock_gear.rarity = "Normal"
        mock_gear.baseType = "Simple Robe"
        mock_gear.inventoryId = "BodyArmour"
        mock_gear.socketedItems = []  # Empty list, not None
        mock_gear.properties = []  # Empty list for properties
        self.mock_character.equipment = [mock_gear]
        
        total_received_items = [{"name": "Marauder"}]
        
        errors = validationLogic.validate_char_equipment(
            self.mock_character, self.mock_ctx, total_received_items
        )
        
        # Should have Gucci Hobo Mode error
        non_none_errors = [e for e in errors if e is not None]
        self.assertGreater(len(non_none_errors), 0)

    def test_get_held_item_names_ilvls_from_char(self):
        """Test extraction of item names and item levels from character"""
        # Mock items in inventory
        mock_item1 = Mock()
        mock_item1.name = "Iron Sword"
        mock_item1.ilvl = 5
        
        mock_item2 = Mock()
        mock_item2.name = "Leather Cap"
        mock_item2.ilvl = 3
        
        self.mock_character.inventory = [mock_item1, mock_item2]
        
        result = validationLogic.get_held_item_names_ilvls_from_char(self.mock_character)
        
        expected = [("Iron Sword", 5), ("Leather Cap", 3)]
        self.assertEqual(result, expected)

    @patch('worlds.poe.poeClient.validationLogic.Locations.base_item_locations_by_base_item_name')
    def test_get_found_base_item_locations(self, mock_locations):
        """Test finding base item locations from character inventory"""
        # Mock locations mapping
        mock_locations = {
            "Iron Sword": {"name": "Iron Sword", "id": 100},
            "Leather Cap": {"name": "Leather Cap", "id": 101}
        }
        
        # Mock character inventory
        mock_item1 = Mock()
        mock_item1.baseType = "Iron Sword"
        mock_item2 = Mock()
        mock_item2.baseType = "Leather Cap"
        mock_item3 = Mock()
        mock_item3.baseType = "Unknown Item"
        
        self.mock_character.inventory = [mock_item1, mock_item2, mock_item3]
        self.mock_character.equipment = []
        
        with patch('worlds.poe.poeClient.validationLogic.Locations.base_item_locations_by_base_item_name', mock_locations):
            result = validationLogic.get_found_base_item_locations(self.mock_character)
        
        # Should find 2 known items, ignore unknown
        self.assertEqual(len(result), 2)
        names = [item["name"] for item in result]
        self.assertIn("Iron Sword", names)
        self.assertIn("Leather Cap", names)

    def test_check_for_victory_act_completion(self):
        """Test victory condition checking for act completion goals"""
        # Test Act 1 completion - patch the async task creation to avoid event loop issues
        with patch('asyncio.create_task') as mock_create_task:
            mock_task = Mock()
            mock_create_task.return_value = mock_task
            
            result = validationLogic.check_for_victory(
                self.mock_ctx, "The Southern Forest", self.mock_character
            )
            
            # Should return a task for victory
            self.assertIsNotNone(result)
            self.assertEqual(result, mock_task)

    def test_check_for_victory_wrong_zone(self):
        """Test victory condition checking in wrong zone"""
        result = validationLogic.check_for_victory(
            self.mock_ctx, "Wrong Zone", self.mock_character
        )
        
        # Should not trigger victory
        self.assertIsNone(result)

    def test_check_for_victory_boss_goal(self):
        """Test victory condition checking for boss defeat goals"""
        self.mock_ctx.game_options["goal"] = Options.Goal.option_defeat_bosses
        self.mock_ctx.game_options["bosses_for_goal"] = ["shaper", "elder"]
        
        # Mock held items that don't match boss drops
        mock_item = Mock()
        mock_item.name = "Random Item"
        mock_item.ilvl = 80
        self.mock_character.inventory = [mock_item]
        
        result = validationLogic.check_for_victory(
            self.mock_ctx, "Atlas", self.mock_character
        )
        
        # Should not trigger victory without boss items
        self.assertIsNone(result)

    @patch('worlds.poe.poeClient.validationLogic.Items.item_table')
    async def test_validate_and_update_basic_flow(self, mock_item_table):
        """Test the main validate_and_update function flow"""
        # Mock item table
        mock_item_table.get.side_effect = lambda item_id: self.mock_items[0] if item_id == 1 else None
        
        # Mock network items
        mock_network_item = Mock()
        mock_network_item.item = 1  # Marauder
        mock_network_item.player = 1
        self.mock_ctx.items_received = [mock_network_item]
        
        # Mock missing locations
        self.mock_ctx.missing_locations = {100, 101}
        self.mock_ctx.locations_info = {
            100: mock_network_item,
            101: mock_network_item
        }
        
        found_items_list = [
            {"name": "Test Item", "id": 100}
        ]
        
        with patch('worlds.poe.poeClient.validationLogic.validate_char_equipment') as mock_validate_char, \
             patch('worlds.poe.poeClient.validationLogic.validate_passive_points') as mock_validate_passive, \
             patch('worlds.poe.poeClient.validationLogic.itemFilter') as mock_filter:
            
            mock_validate_char.return_value = []
            mock_validate_passive.return_value = []
            
            result = await validationLogic.validate_and_update(
                self.mock_ctx, self.mock_character, found_items_list
            )
            
            # Should return empty errors for valid character
            self.assertEqual(result, [])
            
            # Should have called validation functions
            mock_validate_char.assert_called_once()
            mock_validate_passive.assert_called_once()

    async def test_validate_and_update_invalid_context(self):
        """Test validate_and_update with invalid context"""
        result = await validationLogic.validate_and_update(None, self.mock_character, [])
        
        # Should return error for None context
        self.assertGreater(len(result), 0)
        self.assertIn("Context is None", result[0])

    async def test_validate_and_update_missing_character_name(self):
        """Test validate_and_update with missing character name"""
        self.mock_ctx.character_name = ""
        
        result = await validationLogic.validate_and_update(self.mock_ctx, self.mock_character, [])
        
        # Should return error for missing character name
        self.assertGreater(len(result), 0)
        self.assertIn("Character name is not set", result[0])

    @patch('worlds.poe.poeClient.validationLogic.update_filter_to_invalid_char_filter')
    async def test_validate_and_update_with_errors(self, mock_update_filter):
        """Test validate_and_update when character has validation errors"""
        # Mock validation returning errors
        with patch('worlds.poe.poeClient.validationLogic.validate_char_equipment') as mock_validate_char, \
             patch('worlds.poe.poeClient.validationLogic.validate_passive_points') as mock_validate_passive:
            
            mock_validate_char.return_value = ["Missing class"]
            mock_validate_passive.return_value = ["Not enough passives"]
            mock_update_filter.return_value = None
            
            result = await validationLogic.validate_and_update(
                self.mock_ctx, self.mock_character, []
            )
            
            # Should return combined errors
            self.assertEqual(len(result), 2)
            self.assertIn("Missing class", result)
            self.assertIn("Not enough passives", result)
            
            # Should update filter for invalid character
            mock_update_filter.assert_called_once()

    @patch('worlds.poe.poeClient.validationLogic.Locations.get_lvl_location_name_from_lvl')
    @patch('worlds.poe.poeClient.validationLogic.Locations.id_by_level_location_name')
    async def test_validate_and_update_with_leveling_locations(self, mock_id_by_level, mock_get_lvl_name):
        """Test validate_and_update with leveling locations enabled"""
        # Mock leveling location functions
        mock_get_lvl_name.side_effect = lambda level: f"Level {level}"
        mock_id_by_level.get.side_effect = lambda name: 200 + int(name.split()[1]) if "Level" in name else None
        
        # Set character level
        self.mock_ctx.last_character_level = 5
        
        # Mock missing locations to include level locations
        self.mock_ctx.missing_locations = {202, 203, 204, 205}
        
        # Mock network items for level locations
        mock_network_item = Mock()
        mock_network_item.item = 2  # Progressive passive point
        mock_network_item.player = 1
        self.mock_ctx.locations_info = {loc_id: mock_network_item for loc_id in self.mock_ctx.missing_locations}
        
        with patch('worlds.poe.poeClient.validationLogic.validate_char_equipment') as mock_validate_char, \
             patch('worlds.poe.poeClient.validationLogic.validate_passive_points') as mock_validate_passive, \
             patch('worlds.poe.poeClient.validationLogic.itemFilter'):
            
            mock_validate_char.return_value = []
            mock_validate_passive.return_value = []
            
            result = await validationLogic.validate_and_update(
                self.mock_ctx, self.mock_character, []
            )
            
            # Should process level locations
            self.assertEqual(result, [])

    def test_rarity_check_edge_cases(self):
        """Test rarity check with edge cases"""
        # Test with empty item list
        result = validationLogic.rarity_check([], "Normal", "BodyArmour")
        self.assertEqual(result, "BodyArmour")
        
        # Test with wrong progressive item name
        result = validationLogic.rarity_check(["Progressive Helmet"], "Normal", "BodyArmour")
        self.assertEqual(result, "BodyArmour")
        
        # Test case sensitivity
        result = validationLogic.rarity_check(["progressive bodyarmour"], "Normal", "BodyArmour")
        self.assertEqual(result, "BodyArmour")

    def test_validate_char_equipment_none_character(self):
        """Test character equipment validation with None character"""
        errors = validationLogic.validate_char_equipment(None, self.mock_ctx, [])
        
        # Should return error for None character
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("character" in str(error).lower() for error in errors))

    def test_validate_char_equipment_empty_items(self):
        """Test character equipment validation with empty received items"""
        errors = validationLogic.validate_char_equipment(self.mock_character, self.mock_ctx, [])
        
        # Should return error for no received items
        self.assertGreater(len(errors), 0)

    async def test_when_enter_new_zone_integration(self):
        """Test the when_enter_new_zone function integration"""
        test_line = "2024/08/26 10:30:45 123456789 abc [INFO Client 12345] Connecting to instance server at 127.0.0.1:6112"
        
        with patch('worlds.poe.poeClient.validationLogic.textUpdate.get_zone_from_line') as mock_get_zone, \
             patch('worlds.poe.poeClient.validationLogic.gggAPI.get_character') as mock_get_char, \
             patch('worlds.poe.poeClient.validationLogic.get_found_base_item_locations') as mock_get_items, \
             patch('worlds.poe.poeClient.validationLogic.validate_and_update') as mock_validate, \
             patch('worlds.poe.poeClient.validationLogic.check_for_victory') as mock_victory:
            
            mock_get_zone.return_value = "early act 1"
            mock_get_char.return_value = self.mock_character
            mock_get_items.return_value = []
            mock_validate.return_value = []
            mock_victory.return_value = None
            
            # Should not raise exception
            await validationLogic.when_enter_new_zone(self.mock_ctx, test_line)
            
            mock_get_zone.assert_called_once_with(self.mock_ctx, test_line)
            mock_validate.assert_called_once()

    async def test_when_enter_new_zone_no_zone(self):
        """Test when_enter_new_zone with no zone detected"""
        test_line = "Invalid log line"
        
        with patch('worlds.poe.poeClient.validationLogic.textUpdate.get_zone_from_line') as mock_get_zone:
            mock_get_zone.return_value = None
            
            # Should return early without processing
            await validationLogic.when_enter_new_zone(self.mock_ctx, test_line)
            
            mock_get_zone.assert_called_once()

    async def test_when_enter_new_zone_no_character_name(self):
        """Test when_enter_new_zone with no character name set"""
        test_line = "2024/08/26 10:30:45 123456789 abc [INFO Client 12345] Connecting to instance server"
        self.mock_ctx.character_name = None
        
        with patch('worlds.poe.poeClient.validationLogic.textUpdate.get_zone_from_line') as mock_get_zone:
            mock_get_zone.return_value = "early act 1"
            
            # Should handle gracefully
            await validationLogic.when_enter_new_zone(self.mock_ctx, test_line)


if __name__ == '__main__':
    unittest.main()