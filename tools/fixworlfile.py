import os
import sys
import json

# with open(os.path.join(os.path.abspath("tools"), "output", "game_details.json"), "r") as f:
#     game_index = json.load(f)

worldsdir = os.path.abspath("worlds")
for file in os.listdir(worldsdir):
    try:
        if os.path.exists(f"{worldsdir}/{file}/Register.py"):
            with open(f"{worldsdir}/{file}/Register.py", "r") as f:
                data = f.readlines()
                for index, line in enumerate(data):
                    if not "CLIENT_FUNCTION = None" in line:
                        if os.path.exists(f"{worldsdir}/{file}/pyproject.toml"):
                            with open(f"{worldsdir}/{file}/pyproject.toml", "r") as f:
                                data = f.readlines()
                                for index, line in enumerate(data):
                                    if "project.entry-points" in line:
                                        break
                                    if "tool.setuptools.packages.find" in line:
                                        data[index-1].append(f'\n[project.entry-points."mwgg.client"]\n{file}.Client = "{file}.Register:CLIENT_FUNCTION"\n\n')
                                        break
                with open(f"{worldsdir}/{file}/pyproject.toml", "w") as f:
                    f.writelines(data)
    except:
        continue