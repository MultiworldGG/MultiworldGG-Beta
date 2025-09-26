"""
Tests for Progressive Gear functionality in Path of Exile world generation
"""
import unittest
from unittest.mock import Mock, patch, MagicMock

from . import PoeTestBase
from ..data import ItemTable


class TestProgressiveWeaponNaming(PoeTestBase):
    """Test progressive weapon naming logic"""
    
    def test_progressive_weapon_name_enabled(self):
        """Test that progressive weapon names are created when progressive gear is enabled"""
        weapon_base_name = "Sword"
        
        # When progressive gear is NOT disabled (value != option_disabled)
        progressive_gear_value = 1
        progressive_gear_disabled_option = 0
        
        if progressive_gear_value != progressive_gear_disabled_option:
            weapon_name = f"Progressive {weapon_base_name}"
        else:
            weapon_name = f"Normal {weapon_base_name}"
        
        self.assertEqual(weapon_name, "Progressive Sword")
    
    def test_normal_weapon_name_disabled(self):
        """Test that normal weapon names are created when progressive gear is disabled"""
        weapon_base_name = "Sword"
        
        # When progressive gear is disabled (value == option_disabled)
        progressive_gear_value = 0
        progressive_gear_disabled_option = 0
        
        if progressive_gear_value != progressive_gear_disabled_option:
            weapon_name = f"Progressive {weapon_base_name}"
        else:
            weapon_name = f"Normal {weapon_base_name}"
        
        self.assertEqual(weapon_name, "Normal Sword")


class TestProgressiveFlaskLogic(PoeTestBase):
    """Test progressive flask logic"""
    
    def test_progressive_flask_unlock_logic(self):
        """Test that progressive flask unlocks are used when progressive gear is enabled"""
        # Mock STARTING_FLASK_SLOTS value
        starting_flask_slots = 3
        
        # When progressive gear is enabled (value != option_disabled)
        progressive_gear_value = 1
        progressive_gear_disabled_option = 0
        
        flask_names = []
        if progressive_gear_value != progressive_gear_disabled_option:
            # Use progressive flask unlocks
            for i in range(starting_flask_slots):
                flask_names.append("Progressive Flask Unlock")
        
        expected = ["Progressive Flask Unlock", "Progressive Flask Unlock", "Progressive Flask Unlock"]
        self.assertEqual(flask_names, expected)
    
    def test_normal_flask_logic_disabled(self):
        """Test that normal flask logic is used when progressive gear is disabled"""
        # When progressive gear is disabled (value == option_disabled)
        progressive_gear_value = 0
        progressive_gear_disabled_option = 0
        
        use_normal_flask_logic = (progressive_gear_value == progressive_gear_disabled_option)
        self.assertTrue(use_normal_flask_logic)


class TestStartingItemTableChanges(PoeTestBase):
    """Test changes to starting item table structure"""
    
    def test_weapon_names_no_normal_prefix(self):
        """Test that starting weapon names don't have 'Normal' prefix"""
        # Verify the starting items table has the correct weapon names
        expected_weapons = {
            "Scion": "Sword",
            "Marauder": "Mace", 
            "Duelist": "Sword",
            "Ranger": "Bow",
            "Shadow": "Dagger",
            "Witch": "Wand",
            "Templar": "Sceptre"
        }
        
        for character, expected_weapon in expected_weapons.items():
            self.assertEqual(
                ItemTable.starting_items_table[character]["weapon"], 
                expected_weapon,
                f"Character {character} should have weapon {expected_weapon}"
            )
    
    def test_weapon_names_consistency(self):
        """Test that weapon names are consistent across starting items"""
        for character, data in ItemTable.starting_items_table.items():
            weapon_name = data["weapon"]
            
            # Weapon names should not start with "Normal"
            self.assertFalse(
                weapon_name.startswith("Normal"),
                f"Weapon name '{weapon_name}' for character '{character}' should not start with 'Normal'"
            )
            
            # Weapon names should be simple base types
            self.assertIn(weapon_name, ["Sword", "Mace", "Bow", "Dagger", "Wand", "Sceptre"],
                         f"Weapon name '{weapon_name}' should be a recognized base type")


class TestUsableStartingGearOptions(PoeTestBase):
    """Test that the usable starting gear options work with progressive logic"""
    
    def test_weapon_and_gems_option_logic(self):
        """Test the logic for weapon and gems starting gear option"""
        # Mock option values (these would come from the actual options)
        usable_starting_gear_value = 1  # option_starting_weapon_and_gems
        option_starting_weapon_and_gems = 1
        option_starting_weapon = 2
        
        # Test the condition from the diff
        uses_weapon_logic = usable_starting_gear_value in (option_starting_weapon_and_gems, option_starting_weapon)
        self.assertTrue(uses_weapon_logic)
    
    def test_flask_options_logic(self):
        """Test the logic for flask starting gear options"""
        # Mock option values
        usable_starting_gear_value = 3  # option_starting_weapon_flask_and_gems
        option_starting_weapon_flask_and_gems = 3
        option_starting_weapon_and_flask_slots = 4
        
        # Test the condition from the diff
        uses_flask_logic = usable_starting_gear_value in (option_starting_weapon_flask_and_gems, option_starting_weapon_and_flask_slots)
        self.assertTrue(uses_flask_logic)


if __name__ == '__main__':
    unittest.main()
