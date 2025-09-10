import unittest
from unittest.mock import Mock, patch

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

from pathlib import Path
for subdir in Path(poe_client_vendor_dir).iterdir():
    if subdir.is_dir():
        sys.path.insert(0, str(subdir))

import sys
import os

sys.path.insert(0, archipelago_dir)
sys.path.insert(0, worlds_dir)

from test.bases import WorldTestBase
from ..poeClient import validationLogic
    
class PoeTestBase(WorldTestBase):
    game = "Path of Exile"


class TestRarityValidation(PoeTestBase):
    """Comprehensive tests for rarity validation logic"""

    def test_progressive_gear_normal_rarity(self):
        """Test progressive gear validation for normal rarity items"""
        # Test with sufficient progressive items
        items = ["Progressive BodyArmour"]
        result = validationLogic.rarity_check(items, "Normal", "BodyArmour")
        self.assertIsNone(result, "Should allow normal gear with 1+ progressive items")
        
        # Test with insufficient progressive items
        items = []
        result = validationLogic.rarity_check(items, "Normal", "BodyArmour")
        self.assertEqual(result, "BodyArmour", "Should reject normal gear without progressive items")

    def test_progressive_gear_magic_rarity(self):
        """Test progressive gear validation for magic rarity items"""
        # Test with sufficient progressive items
        items = ["Progressive BodyArmour", "Progressive BodyArmour"]
        result = validationLogic.rarity_check(items, "Magic", "BodyArmour")
        self.assertIsNone(result, "Should allow magic gear with 2+ progressive items")
        
        # Test with insufficient progressive items
        items = ["Progressive BodyArmour"]
        result = validationLogic.rarity_check(items, "Magic", "BodyArmour")
        self.assertEqual(result, "BodyArmour", "Should reject magic gear with only 1 progressive item")

    def test_progressive_gear_rare_rarity(self):
        """Test progressive gear validation for rare rarity items"""
        # Test with sufficient progressive items
        items = ["Progressive BodyArmour"] * 3
        result = validationLogic.rarity_check(items, "Rare", "BodyArmour")
        self.assertIsNone(result, "Should allow rare gear with 3+ progressive items")
        
        # Test with insufficient progressive items
        items = ["Progressive BodyArmour"] * 2
        result = validationLogic.rarity_check(items, "Rare", "BodyArmour")
        self.assertEqual(result, "BodyArmour", "Should reject rare gear with only 2 progressive items")

    def test_progressive_gear_unique_rarity(self):
        """Test progressive gear validation for unique rarity items"""
        # Test with sufficient progressive items
        items = ["Progressive BodyArmour"] * 4
        result = validationLogic.rarity_check(items, "Unique", "BodyArmour")
        self.assertIsNone(result, "Should allow unique gear with 4+ progressive items")
        
        # Test with insufficient progressive items
        items = ["Progressive BodyArmour"] * 3
        result = validationLogic.rarity_check(items, "Unique", "BodyArmour")
        self.assertEqual(result, "BodyArmour", "Should reject unique gear with only 3 progressive items")

    def test_progressive_gear_different_equipment_types(self):
        """Test progressive gear validation across different equipment types"""
        equipment_types = ["BodyArmour", "Helmet", "Gloves", "Boots", "Belt", "Amulet"]
        
        for equipment_type in equipment_types:
            with self.subTest(equipment_type=equipment_type):
                # Test normal rarity
                items = [f"Progressive {equipment_type}"]
                result = validationLogic.rarity_check(items, "Normal", equipment_type)
                self.assertIsNone(result, f"Should allow normal {equipment_type} with 1 progressive item")
                
                # Test magic rarity
                items = [f"Progressive {equipment_type}"] * 2
                result = validationLogic.rarity_check(items, "Magic", equipment_type)
                self.assertIsNone(result, f"Should allow magic {equipment_type} with 2 progressive items")

    def test_progressive_gear_mixed_items(self):
        """Test progressive gear with mixed item types in received items"""
        items = [
            "Progressive BodyArmour",
            "Progressive Helmet", 
            "Progressive BodyArmour",
            "Some Other Item",
            "Progressive BodyArmour"
        ]
        
        # Should count only the matching progressive items
        result = validationLogic.rarity_check(items, "Rare", "BodyArmour")
        self.assertIsNone(result, "Should count only matching progressive items")
        
        # Test with helmet (should only have 1 progressive helmet)
        result = validationLogic.rarity_check(items, "Magic", "Helmet")
        self.assertEqual(result, "Helmet", "Should reject magic helmet with only 1 progressive item")

    def test_progressive_gear_case_sensitivity(self):
        """Test that progressive gear matching is case sensitive"""
        items = ["progressive bodyarmour", "Progressive bodyarmour", "PROGRESSIVE BODYARMOUR"]
        
        # Should not match due to case sensitivity
        result = validationLogic.rarity_check(items, "Normal", "BodyArmour")
        self.assertEqual(result, "BodyArmour", "Should be case sensitive")

    def test_progressive_gear_exact_match_only(self):
        """Test that progressive gear requires exact string matching"""
        items = ["Progressive BodyArmour Extra", "Progressive BodyArmour", "BodyArmour Progressive"]
        
        # Should only count the exact match
        result = validationLogic.rarity_check(items, "Magic", "BodyArmour")
        self.assertEqual(result, "BodyArmour", "Should require exact string matching")

    def test_progressive_gear_zero_items(self):
        """Test progressive gear validation with no items"""
        items = []
        
        for rarity in ["Normal", "Magic", "Rare", "Unique"]:
            with self.subTest(rarity=rarity):
                result = validationLogic.rarity_check(items, rarity, "BodyArmour")
                self.assertEqual(result, "BodyArmour", f"Should reject {rarity} gear with no items")

    def test_progressive_gear_boundary_conditions(self):
        """Test progressive gear at exact boundary conditions"""
        # Test exact boundary for each rarity
        test_cases = [
            ("Normal", 1),
            ("Magic", 2), 
            ("Rare", 3),
            ("Unique", 4)
        ]
        
        for rarity, required_count in test_cases:
            with self.subTest(rarity=rarity, required_count=required_count):
                # Test with exact required count (should pass)
                items = ["Progressive BodyArmour"] * required_count
                result = validationLogic.rarity_check(items, rarity, "BodyArmour")
                self.assertIsNone(result, f"Should allow {rarity} with exactly {required_count} items")
                
                # Test with one less than required (should fail)
                if required_count > 0:
                    items = ["Progressive BodyArmour"] * (required_count - 1)
                    result = validationLogic.rarity_check(items, rarity, "BodyArmour")
                    self.assertEqual(result, "BodyArmour", f"Should reject {rarity} with {required_count-1} items")

    def test_progressive_gear_overflow(self):
        """Test progressive gear with more items than needed"""
        # Test with way more items than needed
        items = ["Progressive BodyArmour"] * 10
        
        for rarity in ["Normal", "Magic", "Rare", "Unique"]:
            with self.subTest(rarity=rarity):
                result = validationLogic.rarity_check(items, rarity, "BodyArmour")
                self.assertIsNone(result, f"Should allow {rarity} gear with excess progressive items")

    def test_rarity_check_return_values(self):
        """Test that rarity_check returns correct values"""
        # Test successful validation returns None
        items = ["Progressive BodyArmour"]
        result = validationLogic.rarity_check(items, "Normal", "BodyArmour")
        self.assertIsNone(result, "Successful validation should return None")
        
        # Test failed validation returns equipment_id
        items = []
        result = validationLogic.rarity_check(items, "Normal", "BodyArmour")
        self.assertEqual(result, "BodyArmour", "Failed validation should return equipment_id")
        
        # Test with different equipment_id
        result = validationLogic.rarity_check(items, "Normal", "Helmet")
        self.assertEqual(result, "Helmet", "Failed validation should return correct equipment_id")


if __name__ == '__main__':
    unittest.main()
