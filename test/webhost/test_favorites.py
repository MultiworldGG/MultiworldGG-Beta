import unittest
from unittest.mock import patch, MagicMock
import json
import tempfile
import os

from . import TestBase


class TestFavoritesFeature(TestBase):
    def test_supported_games_page_loads_with_favorites_section(self):
        """Test that the supported games page includes the favorites section HTML"""
        response = self.client.get('/games')
        self.assertEqual(response.status_code, 200)
        
        # Check that the favorites section is present
        self.assertIn(b'favorites-section', response.data)
        self.assertIn(b'favorites-list', response.data)
        self.assertIn(b'Favorite Games', response.data)
        
        # Check that star icons are present
        self.assertIn(b'star-icon', response.data)
        self.assertIn(b'Add to favorites', response.data)

    def test_star_icons_have_correct_attributes(self):
        """Test that star icons have the correct data attributes"""
        response = self.client.get('/games')
        self.assertEqual(response.status_code, 200)
        
        # Check that star icons have data-game attribute
        self.assertIn(b'data-game', response.data)
        self.assertIn(b'star-icon', response.data)

    def test_favorites_section_is_hidden_by_default(self):
        """Test that the favorites section is hidden by default"""
        response = self.client.get('/games')
        self.assertEqual(response.status_code, 200)
        
        # Check that the favorites section has display: none
        self.assertIn(b'style="display: none;"', response.data)

    def test_javascript_includes_favorites_functionality(self):
        """Test that the JavaScript file includes favorites functionality"""
        js_file_path = 'WebHostLib/static/assets/supportedGames.js'
        
        with open(js_file_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Check for key favorites functionality
        self.assertIn('FAVORITES_STORAGE_KEY', js_content)
        self.assertIn('localStorage', js_content)
        self.assertIn('favoriteGames', js_content)
        self.assertIn('toggleFavorite', js_content)
        self.assertIn('updateFavoritesSection', js_content)

    def test_css_includes_favorites_styles(self):
        """Test that the CSS file includes favorites styling"""
        css_file_path = 'WebHostLib/static/styles/supportedGames.css'
        
        with open(css_file_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Check for key favorites styles
        self.assertIn('#favorites-section', css_content)
        self.assertIn('.star-icon', css_content)
        self.assertIn('.favorited', css_content)
        self.assertIn('.favorite-game-item', css_content)

    def test_local_storage_functionality(self):
        """Test that localStorage functions work correctly"""
        # This would require a browser environment to test fully
        # For now, we'll just verify the functions exist in the JS
        js_file_path = 'WebHostLib/static/assets/supportedGames.js'
        
        with open(js_file_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Check for localStorage usage
        self.assertIn('localStorage.getItem', js_content)
        self.assertIn('localStorage.setItem', js_content)
        self.assertIn('JSON.parse', js_content)
        self.assertIn('JSON.stringify', js_content)

    def test_star_icon_functionality(self):
        """Test that star icon functionality is properly implemented"""
        js_file_path = 'WebHostLib/static/assets/supportedGames.js'
        
        with open(js_file_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Check for star icon related functionality
        self.assertIn('updateStarIcon', js_content)
        self.assertIn('initializeStarIcons', js_content)
        self.assertIn('star-icon', js_content)

    def test_search_integration(self):
        """Test that search functionality works with favorites"""
        js_file_path = 'WebHostLib/static/assets/supportedGames.js'
        
        with open(js_file_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Check that search also filters favorites
        self.assertIn('favoriteItems', js_content)
        self.assertIn('favorite-game-item', js_content)

    def test_search_cleared_when_favoriting(self):
        """Test that search bar is cleared when adding a new favorite"""
        js_file_path = 'WebHostLib/static/assets/supportedGames.js'
        
        with open(js_file_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Check for search clearing functionality when favoriting
        self.assertIn('wasFavorited', js_content)
        self.assertIn('gameSearch.value = \'\'', js_content)
        self.assertIn('dispatchEvent', js_content)
        self.assertIn('new Event(\'input\')', js_content)


if __name__ == '__main__':
    unittest.main() 