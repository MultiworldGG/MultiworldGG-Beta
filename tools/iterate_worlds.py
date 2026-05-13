'''Modify this script as needed to iterate a change over the worlds'''

import os
import sys
import json
from pathlib import Path

# Get the script directory (src/tools)
script_dir = Path(__file__).resolve().parents[1]

# Change to script directory
os.chdir(script_dir)

worlds_dir = script_dir / "src" / "worlds"

# with open(os.path.join(os.path.abspath("tools"), "output", "game_details.json"), "r") as f:
#     game_index = json.load(f)

# for file in os.listdir(worlds_dir):
#     try:
#         if os.path.exists(f"{worlds_dir}/{file}/pyproject.toml"):
#             with open(f"{worlds_dir}/{file}/pyproject.toml", "r") as f:
#                 data = f.readlines()
#                 for index, line in enumerate(data):
#                     if 'Client" = "worlds.' in line:
#                         data[index] = f'"worlds.{line}'
#                         break
#                 with open(f"{worlds_dir}/{file}/pyproject.toml", "w") as f:
#                     f.writelines(data)
#     except:
#         continue