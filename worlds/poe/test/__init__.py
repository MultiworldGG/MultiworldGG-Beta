"""
Path of Exile test module for Archipelago
"""

try:
    from test.bases import WorldTestBase
    
    class PoeTestBase(WorldTestBase):
        game = "Path of Exile"
        
except ImportError:
    # Fallback for when running tests outside of normal Archipelago structure
    import unittest
    
    class PoeTestBase(unittest.TestCase):
        game = "Path of Exile"
        
        def setUp(self):
            super().setUp()


