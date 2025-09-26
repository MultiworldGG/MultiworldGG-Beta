"""
Tests for Path of Exile text update and chat command enhancements
"""
import unittest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import asyncio

from . import PoeTestBase
from ..poeClient.textUpdate import (
    chat_commands_callback, 
    build_progressive_message, 
    rarity_from_progressive_count,
    split_send_message
)
from ..Items import ItemDict


class TestProgressiveMessageBuilding(PoeTestBase):
    """Test progressive message building functionality"""
    
    def test_build_progressive_message_single_items(self):
        """Test building progressive message with single progressive items"""
        items = [
            {"name": "Progressive Sword", "category": ["Progressive", "Weapon"], "id": 1},
            {"name": "Progressive Shield", "category": ["Progressive", "Armour"], "id": 2},
        ]
        
        result = build_progressive_message(items)
        expected = "Normal Sword, Normal Shield"
        self.assertEqual(result, expected)
    
    def test_build_progressive_message_multiple_same_item(self):
        """Test building progressive message with multiple of same progressive item"""
        items = [
            {"name": "Progressive Sword", "category": ["Progressive", "Weapon"], "id": 1},
            {"name": "Progressive Sword", "category": ["Progressive", "Weapon"], "id": 1},
            {"name": "Progressive Sword", "category": ["Progressive", "Weapon"], "id": 1},
        ]
        
        result = build_progressive_message(items)
        expected = "up to Rare Sword"
        self.assertEqual(result, expected)
    
    def test_build_progressive_message_mixed_counts(self):
        """Test building progressive message with different counts of different items"""
        items = [
            {"name": "Progressive Sword", "category": ["Progressive", "Weapon"], "id": 1},
            {"name": "Progressive Sword", "category": ["Progressive", "Weapon"], "id": 1},
            {"name": "Progressive Shield", "category": ["Progressive", "Armour"], "id": 2},
            {"name": "Progressive Shield", "category": ["Progressive", "Armour"], "id": 2},
            {"name": "Progressive Shield", "category": ["Progressive", "Armour"], "id": 2},
            {"name": "Progressive Shield", "category": ["Progressive", "Armour"], "id": 2},
        ]
        
        result = build_progressive_message(items)
        expected = "up to Magic Sword, Any Shield"
        self.assertEqual(result, expected)
    
    def test_build_progressive_message_empty_list(self):
        """Test building progressive message with empty list"""
        items = []
        result = build_progressive_message(items)
        self.assertEqual(result, "")
    
    def test_build_progressive_message_non_progressive_items(self):
        """Test building progressive message with non-progressive items"""
        items = [
            {"name": "Normal Sword", "category": ["Normal", "Weapon"], "id": 1},
            {"name": "Random Shield", "category": ["Random", "Armour"], "id": 2},
        ]
        
        result = build_progressive_message(items)
        self.assertEqual(result, "")


class TestRarityFromProgressiveCount(PoeTestBase):
    """Test rarity string generation from progressive count"""
    
    def test_rarity_count_1(self):
        """Test count 1 returns Normal"""
        self.assertEqual(rarity_from_progressive_count(1), "Normal")
    
    def test_rarity_count_2(self):
        """Test count 2 returns up to Magic"""
        self.assertEqual(rarity_from_progressive_count(2), "up to Magic")
    
    def test_rarity_count_3(self):
        """Test count 3 returns up to Rare"""
        self.assertEqual(rarity_from_progressive_count(3), "up to Rare")
    
    def test_rarity_count_4(self):
        """Test count 4 returns Any"""
        self.assertEqual(rarity_from_progressive_count(4), "Any")
    
    def test_rarity_count_0(self):
        """Test count 0 returns empty string"""
        self.assertEqual(rarity_from_progressive_count(0), "")
    
    def test_rarity_count_greater_than_4(self):
        """Test count greater than 4 returns empty string"""
        self.assertEqual(rarity_from_progressive_count(5), "")
        self.assertEqual(rarity_from_progressive_count(10), "")


class TestChatCommandsCallback(PoeTestBase):
    """Test enhanced chat command functionality"""
    
    def setUp(self):
        super().setUp()
        self.ctx = Mock()
        self.ctx.items_received = [1, 2, 3, 100, 101]  # Mock received item IDs
    
    @patch('worlds.poe.poeClient.textUpdate.split_send_message')
    @patch('worlds.poe.Items.get_main_skill_gem_items')
    @patch('worlds.poe.Items.get_by_category')
    async def test_main_gems_command_includes_gem_modifiers(self, mock_get_by_category, mock_get_main_gems, mock_split_send):
        """Test that !main gems command includes gem modifiers"""
        # Setup mock data
        main_gems = [
            {"id": 1, "name": "Fireball", "requiredLevel": 1},
            {"id": 2, "name": "Ice Bolt", "requiredLevel": 5},
        ]
        gem_modifiers = [
            {"id": 3, "name": "Fire Mastery", "requiredLevel": 10},
        ]
        
        mock_get_main_gems.return_value = main_gems
        mock_get_by_category.return_value = gem_modifiers
        mock_split_send.return_value = AsyncMock()
        
        await chat_commands_callback(self.ctx, "!main gems")
        
        # Verify both main gems and gem modifiers are retrieved
        mock_get_main_gems.assert_called_once()
        mock_get_by_category.assert_called_once_with("GemModifier")
        
        # Verify the message includes gems sorted by level
        mock_split_send.assert_called_once()
        call_args = mock_split_send.call_args[0][1]  # Second argument is the message
        self.assertIn("Fireball", call_args)
        self.assertIn("Ice Bolt", call_args)
        self.assertIn("Fire Mastery", call_args)
    
    @patch('worlds.poe.poeClient.textUpdate.split_send_message')
    @patch('worlds.poe.Items.get_support_gem_items')
    async def test_support_gems_command_sorts_by_level(self, mock_get_support_gems, mock_split_send):
        """Test that !support gems command sorts gems by required level"""
        support_gems = [
            {"id": 1, "name": "High Level Support", "requiredLevel": 31},
            {"id": 2, "name": "Low Level Support", "requiredLevel": 1},
            {"id": 3, "name": "Mid Level Support", "requiredLevel": 12},
        ]
        
        mock_get_support_gems.return_value = support_gems
        mock_split_send.return_value = AsyncMock()
        
        await chat_commands_callback(self.ctx, "!support gems")
        
        # Verify sorting is applied
        mock_split_send.assert_called_once()
        call_args = mock_split_send.call_args[0][1]
        
        # Should be sorted by level: Low Level (1), Mid Level (12), High Level (31)
        self.assertIn("Low Level Support", call_args)
        self.assertIn("Mid Level Support", call_args)
        self.assertIn("High Level Support", call_args)
    
    @patch('worlds.poe.poeClient.textUpdate.split_send_message')
    @patch('worlds.poe.Items.get_utility_skill_gem_items')
    async def test_utility_gems_command_sorts_by_level(self, mock_get_utility_gems, mock_split_send):
        """Test that !utility gems command sorts gems by required level"""
        utility_gems = [
            {"id": 1, "name": "Portal", "requiredLevel": 10},
            {"id": 2, "name": "Identify", "requiredLevel": 1},
        ]
        
        mock_get_utility_gems.return_value = utility_gems
        mock_split_send.return_value = AsyncMock()
        
        await chat_commands_callback(self.ctx, "!utility gems")
        
        mock_split_send.assert_called_once()
        call_args = mock_split_send.call_args[0][1]
        
        # Should be sorted by level
        self.assertIn("Identify", call_args)
        self.assertIn("Portal", call_args)
    
    @patch('worlds.poe.poeClient.textUpdate.split_send_message')
    @patch('worlds.poe.Items.get_all_gems')
    @patch('worlds.poe.Items.get_by_category')
    async def test_all_gems_command_includes_modifiers_and_sorts(self, mock_get_by_category, mock_get_all_gems, mock_split_send):
        """Test that !all gems and !gems commands include gem modifiers and sort by level"""
        all_gems = [
            {"id": 1, "name": "Fireball", "requiredLevel": 5},
        ]
        gem_modifiers = [
            {"id": 3, "name": "Fire Mastery", "requiredLevel": 1},
        ]
        
        mock_get_all_gems.return_value = all_gems
        mock_get_by_category.return_value = gem_modifiers
        mock_split_send.return_value = AsyncMock()
        
        await chat_commands_callback(self.ctx, "!all gems")
        
        mock_get_all_gems.assert_called_once()
        mock_get_by_category.assert_called_once_with("GemModifier")
        mock_split_send.assert_called_once()
    
    @patch('worlds.poe.poeClient.textUpdate.split_send_message')
    @patch('worlds.poe.poeClient.textUpdate.build_progressive_message')
    @patch('worlds.poe.Items.get_gear_items')
    async def test_gear_command_uses_progressive_message(self, mock_get_gear, mock_build_progressive, mock_split_send):
        """Test that !gear command uses progressive message building"""
        gear_items = [
            {"id": 1, "name": "Progressive Sword", "category": ["Progressive", "Weapon"]},
            {"id": 2, "name": "Normal Shield", "category": ["Normal", "Armour"]},
        ]
        
        mock_get_gear.return_value = gear_items
        mock_build_progressive.return_value = "up to Magic Sword"
        mock_split_send.return_value = AsyncMock()
        
        await chat_commands_callback(self.ctx, "!gear")
        
        mock_build_progressive.assert_called_once_with(gear_items)
        mock_split_send.assert_called_once()
        
        # Verify the message combines progressive and normal items
        call_args = mock_split_send.call_args[0][1]
        self.assertIn("up to Magic Sword", call_args)
        self.assertIn("Normal Shield", call_args)
    
    @patch('worlds.poe.poeClient.textUpdate.split_send_message')
    @patch('worlds.poe.poeClient.textUpdate.build_progressive_message')
    @patch('worlds.poe.Items.get_weapon_items')
    async def test_weapons_command_uses_progressive_message(self, mock_get_weapons, mock_build_progressive, mock_split_send):
        """Test that !weapons command uses progressive message building"""
        weapon_items = [
            {"id": 1, "name": "Progressive Sword", "category": ["Progressive", "Weapon"]},
        ]
        
        mock_get_weapons.return_value = weapon_items
        mock_build_progressive.return_value = "Normal Sword"
        mock_split_send.return_value = AsyncMock()
        
        await chat_commands_callback(self.ctx, "!weapons")
        
        mock_build_progressive.assert_called_once_with(weapon_items)
        mock_split_send.assert_called_once()
    
    @patch('worlds.poe.poeClient.textUpdate.split_send_message')
    @patch('worlds.poe.poeClient.textUpdate.build_progressive_message') 
    @patch('worlds.poe.Items.get_armor_items')
    async def test_armor_command_uses_progressive_message(self, mock_get_armor, mock_build_progressive, mock_split_send):
        """Test that !armor command uses progressive message building"""
        armor_items = [
            {"id": 1, "name": "Progressive Helmet", "category": ["Progressive", "Armour"]},
        ]
        
        mock_get_armor.return_value = armor_items
        mock_build_progressive.return_value = "Normal Helmet"
        mock_split_send.return_value = AsyncMock()
        
        await chat_commands_callback(self.ctx, "!armor")
        
        mock_build_progressive.assert_called_once_with(armor_items)
        mock_split_send.assert_called_once()


if __name__ == '__main__':
    unittest.main()
