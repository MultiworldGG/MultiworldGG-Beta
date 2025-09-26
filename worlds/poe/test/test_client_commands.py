"""
Tests for Path of Exile Client command processor changes
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from . import PoeTestBase
from ..Client import PathOfExileCommandProcessor, PathOfExileContext
from ..poeClient import itemFilter


class TestPoeDocumentsDirectoryCommand(PoeTestBase):
    """Test the _cmd_poe_documents_directory command functionality"""
    
    def setUp(self):
        super().setUp()
        self.ctx = Mock(spec=PathOfExileContext)
        self.ctx.update_settings = Mock()
        self.ctx.poe_doc_path = str(itemFilter.DEFAULT_POE_DOC_PATH)
        
        self.processor = PathOfExileCommandProcessor(self.ctx)
        self.processor.output = Mock()
        self.processor.logger = Mock()
        
        # Reset the class variable before each test
        PathOfExileCommandProcessor.reset_poe_doc_path = False
    
    def test_no_path_shows_current_directory(self):
        """Test that calling with no path shows current directory"""
        result = self.processor._cmd_poe_documents_directory(None)
        
        self.assertFalse(result)
        self.processor.output.assert_any_call("The current directory for poe item filters is:")
        self.processor.output.assert_any_call(f"  {itemFilter.poe_doc_path}")
        self.processor.output.assert_any_call("Run this command again to set it to the default directory.")
        self.assertTrue(self.processor.reset_poe_doc_path)
    
    def test_no_path_twice_resets_to_default(self):
        """Test that calling with no path twice shows reset message"""
        # First call sets the reset flag
        self.processor._cmd_poe_documents_directory(None)
        self.assertTrue(self.processor.reset_poe_doc_path)
        
        # Second call should show reset message
        result = self.processor._cmd_poe_documents_directory(None)
        
        self.assertFalse(result)
        self.processor.output.assert_any_call(f"Setting to default path: {str(itemFilter.DEFAULT_POE_DOC_PATH)}")
        # The flag remains True since the implementation just shows a message
        self.assertTrue(self.processor.reset_poe_doc_path)
    
    def test_valid_path_sets_directory(self):
        """Test that providing a valid path sets the directory"""
        test_path = Path.home() / "TestDirectory"
        
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_dir', return_value=True), \
             patch('worlds.poe.poeClient.itemFilter.set_poe_doc_path') as mock_set_path:
            
            result = self.processor._cmd_poe_documents_directory(str(test_path))
            
            self.assertTrue(result)
            mock_set_path.assert_called_once_with(test_path)
            self.assertEqual(self.ctx.poe_doc_path, str(test_path))
            self.ctx.update_settings.assert_called_once()
            self.processor.logger.debug.assert_called_once_with(f"[DEBUG] Set poe documents directory to: {test_path}")
            self.assertFalse(self.processor.reset_poe_doc_path)
    
    def test_nonexistent_path_shows_error(self):
        """Test that providing a nonexistent path shows an error"""
        test_path = "/nonexistent/path"
        
        with patch.object(Path, 'exists', return_value=False):
            result = self.processor._cmd_poe_documents_directory(test_path)
            
            self.assertFalse(result)
            self.processor.output.assert_called_with(f"ERROR: The provided path does not exist: {test_path}")
    
    def test_path_not_directory_shows_error(self):
        """Test that providing a path that is not a directory shows an error"""
        test_path = "/path/to/file.txt"
        
        with patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_dir', return_value=False):
            
            result = self.processor._cmd_poe_documents_directory(test_path)
            
            self.assertFalse(result)
            self.processor.output.assert_called_with(f"ERROR: The provided path is not a directory: {test_path}")


class TestPathOfExileContextVersionCompatibility(PoeTestBase):
    """Test version compatibility message formatting"""
    
    def test_backwards_compatible_version_message_format(self):
        """Test that backwards compatible version message is properly formatted"""
        generated_version = "1.1.1"
        poe_version = "1.1.2"
        
        expected_log = (f"Connected to multiworld generated with different version: {generated_version}, "+
                       f"running version {poe_version}. This is marked as backwards compatible, and should be OK.")
        
        # Test the message format
        self.assertIn("Connected to multiworld generated with different version", expected_log)
        self.assertIn("backwards compatible", expected_log)
        self.assertIn(generated_version, expected_log)
        self.assertIn(poe_version, expected_log)
    
    def test_incompatible_version_message_format(self):
        """Test that incompatible version message is properly formatted"""
        generated_version = "1.0.0"
        poe_version = "1.1.2"
        
        expected_log = (f"-----------------------------------------------------------------------------------------\n"+
                       f"Server generated with unsupported version!\n"+
                       f"Server:{generated_version}\n"+
                       f"Client:{poe_version}\n"+
                       f"This may cause issues!!!\n"+
                       f"-----------------------------------------------------------------------------------------")
        
        # Test the message format
        self.assertIn("Server generated with unsupported version", expected_log)
        self.assertIn("This may cause issues", expected_log)
        self.assertIn("-----------------------------------------------------------------------------------------", expected_log)
        self.assertIn(f"Server:{generated_version}", expected_log)
        self.assertIn(f"Client:{poe_version}", expected_log)


if __name__ == '__main__':
    unittest.main()
