import unittest
import os


class TestPackages(unittest.TestCase):
    def test_packages_have_required_files(self):
        """Test that all world folders containing .py files also have a Register.py and pyproject.toml file,
        to ensure proper package structure.
        """
        import Utils

        # Ignore directories with these names.
        ignore_dirs = {".github", "Lib", "Wheels"}

        worlds_path = Utils.local_path("worlds")
        for dirpath, dirnames, filenames in os.walk(worlds_path):
            # Drop ignored directories from dirnames, excluding them from walking.
            dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
            
            # Only test directories that contain .py files
            if any(file.endswith(".py") for file in filenames):
                with self.subTest(directory=dirpath):
                    has_register = "Register.py" in filenames
                    has_pyproject = "pyproject.toml" in filenames
                    
                    self.assertTrue(has_register, f"Directory {dirpath} missing Register.py")
                    self.assertTrue(has_pyproject, f"Directory {dirpath} missing pyproject.toml")
