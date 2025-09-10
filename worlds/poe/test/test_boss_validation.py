import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from pathlib import Path

# Add vendor libraries to path for dependencies like pygetwindow
current_dir = os.path.dirname(__file__)
poe_dir = os.path.dirname(current_dir)
worlds_dir = os.path.dirname(poe_dir)
archipelago_dir = os.path.dirname(worlds_dir)
poe_client_vendor_dir = os.path.join(archipelago_dir, "lib", "poe_client_vendor")
for subdir in Path(poe_client_vendor_dir).iterdir():
    if subdir.is_dir():
        sys.path.insert(0, str(subdir))

if poe_client_vendor_dir not in sys.path:
    sys.path.insert(0, poe_client_vendor_dir)


try:
    from . import PoeTestBase
    from .. import Options
    from ..poeClient import validationLogic
except ImportError:
    import sys
    import os
    
    current_dir = os.path.dirname(__file__)
    poe_dir = os.path.dirname(current_dir)
    worlds_dir = os.path.dirname(poe_dir)
    archipelago_dir = os.path.dirname(worlds_dir)
    
    sys.path.insert(0, archipelago_dir)
    sys.path.insert(0, worlds_dir)
    
    from test.bases import WorldTestBase
    from poe import Options
    from poe.poeClient import validationLogic
    
    class PoeTestBase(WorldTestBase):
        game = "Path of Exile"


class TestBossValidation(PoeTestBase):
    """Comprehensive tests for boss completion validation logic"""

    def create_mock_context(self, game_options=None):
        """Create a mock context with specified game options"""
        context = Mock()
        context.character_name = "TestCharacter"
        context.game_options = game_options or {
            "goal": Options.Goal.option_defeat_bosses,
            "bosses_for_goal": ["shaper", "elder"]
        }
        # Mock items_received as an empty list
        context.items_received = []
        return context

    def create_mock_character(self, inventory_items=None):
        """Create a mock character with specified inventory"""
        character = Mock()
        character.inventory = inventory_items or []
        return character

    def test_check_for_victory_act_completion_goals(self):
        """Test victory check for act completion goals"""
        test_cases = [
            (Options.Goal.option_complete_act_1, "The Southern Forest"),
            (Options.Goal.option_complete_act_2, "The City of Sarn"),
            (Options.Goal.option_complete_act_3, "The Aqueduct"),
            (Options.Goal.option_complete_act_4, "The Slave Pens"),
        ]
        
        for goal, zone in test_cases:
            with self.subTest(goal=goal, zone=zone):
                context = self.create_mock_context({"goal": goal})
                character = self.create_mock_character()
                
                # Mock async task creation to avoid event loop issues
                with patch('asyncio.create_task') as mock_create_task:
                    mock_task = Mock()
                    mock_create_task.return_value = mock_task
                    
                    result = validationLogic.check_for_victory(context, zone, character)
                    # Should return a task for victory
                    self.assertIsNotNone(result)

    def test_check_for_victory_wrong_zone(self):
        """Test victory check in wrong zone"""
        context = self.create_mock_context({"goal": Options.Goal.option_complete_act_1})
        character = self.create_mock_character()
        
        result = validationLogic.check_for_victory(context, "Wrong Zone", character)
        # Should not trigger victory
        self.assertIsNone(result)

    def test_check_for_victory_boss_goal_setup(self):
        """Test that boss goal setup doesn't crash"""
        context = self.create_mock_context({
            "goal": Options.Goal.option_defeat_bosses,
            "bosses_for_goal": ["shaper", "elder"]
        })
        character = self.create_mock_character()
        
        # Mock the Locations.bosses to avoid KeyError and bosses_by_id
        with patch('worlds.poe.poeClient.validationLogic.Locations.bosses', {"shaper": {"id": 1}, "elder": {"id": 2}}), \
             patch('worlds.poe.poeClient.validationLogic.Locations.bosses_by_id', {1: {"name": "Shaper"}, 2: {"name": "Elder"}}):
            
            result = validationLogic.check_for_victory(context, "any_zone", character)
            # Should return None when bosses haven't been defeated (correct behavior)
            self.assertIsNone(result)

    def test_check_for_victory_bosses_defeated(self):
        """Test victory when all required bosses are defeated"""
        # Mock network items representing defeated bosses
        mock_item1 = Mock()
        mock_item1.item = 1  # Shaper ID
        mock_item2 = Mock()
        mock_item2.item = 2  # Elder ID
        
        context = self.create_mock_context({
            "goal": Options.Goal.option_defeat_bosses,
            "bosses_for_goal": ["shaper", "elder"]
        })
        context.items_received = [mock_item1, mock_item2]
        character = self.create_mock_character()
        
        # Mock the Locations to provide boss data - the key is that received_item_names
        # gets populated from bosses_by_id[item_id]["name"] for items received
        # Boss names need "defeat " prefix to match required format
        bosses_by_id = {
            1: {"name": "defeat shaper"},
            2: {"name": "defeat elder"}
        }

        with patch('worlds.poe.poeClient.validationLogic.Locations.bosses', {"shaper": {"id": 1}, "elder": {"id": 2}}), \
             patch('worlds.poe.poeClient.validationLogic.Locations.bosses_by_id', bosses_by_id), \
             patch('asyncio.create_task') as mock_create_task:
            
            mock_task = Mock()
            mock_create_task.return_value = mock_task
            
            result = validationLogic.check_for_victory(context, "any_zone", character)
            # Should return a task when all bosses are defeated
            self.assertIsNotNone(result, "Expected victory task when all required bosses are defeated")

    def test_check_for_victory_no_goal_set(self):
        """Test victory check when no goal is set"""
        context = self.create_mock_context({"goal": -1})
        character = self.create_mock_character()
        
        with self.assertRaises(ValueError):
            validationLogic.check_for_victory(context, "any_zone", character)

if __name__ == '__main__':
    unittest.main()
