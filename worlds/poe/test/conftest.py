"""
pytest configuration for Path of Exile tests
Sets up vendor module paths before test collection
"""
import sys
import os
from pathlib import Path

def setup_vendor_paths():
    """Set up vendor module paths for pywinctl/pymonctl dependencies"""
    # Get paths relative to conftest.py location
    current_dir = os.path.dirname(__file__)
    poe_dir = os.path.dirname(current_dir)
    worlds_dir = os.path.dirname(poe_dir)
    archipelago_dir = os.path.dirname(worlds_dir)

    # Add Archipelago root to path for test.bases import
    if archipelago_dir not in sys.path:
        sys.path.insert(0, archipelago_dir)

    # Use the existing vendor module loading system
    try:
        # Add the poeClient module to path so we can import fileHelper
        poe_client_dir = os.path.join(poe_dir, "poeClient")
        if poe_client_dir not in sys.path:
            sys.path.insert(0, poe_client_dir)
        
        # Import and use the existing vendor loading system
        from fileHelper import load_vendor_modules
        load_vendor_modules()
        
    except Exception as e:
        print(f"Warning: Could not load vendor modules: {e}")
        # Fallback to manual path setup
        vendor_dirs = [
            os.path.join(archipelago_dir, "lib", "poe_client_vendor"),
        ]
        
        for poe_client_vendor_dir in vendor_dirs:
            # Set up vendor module paths
            if poe_client_vendor_dir not in sys.path:
                sys.path.insert(0, poe_client_vendor_dir)

            # Add vendor subdirectories (critical for pywinctl/pymonctl structure)
            if Path(poe_client_vendor_dir).exists():
                for subdir in Path(poe_client_vendor_dir).iterdir():
                    if subdir.is_dir():
                        subdir_str = str(subdir)
                        if subdir_str not in sys.path:
                            sys.path.insert(0, subdir_str)
                        
                        # Add nested subdirectories (e.g., pymonctl inside pywinctl)
                        for nested_subdir in subdir.iterdir():
                            if nested_subdir.is_dir():
                                nested_str = str(nested_subdir)
                                if nested_str not in sys.path:
                                    sys.path.insert(0, nested_str)

# Execute setup immediately when conftest.py is imported
setup_vendor_paths()
