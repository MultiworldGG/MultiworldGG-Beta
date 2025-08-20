import os
import sys
import json

# with open(os.path.join(os.path.abspath("tools"), "output", "game_details.json"), "r") as f:
#     game_index = json.load(f)

worldsdir = os.path.abspath("worlds")
#for file in os.listdir(worldsdir):

with open("python_paths.txt", "r") as f:
    python_paths = f.readlines()
    for file in python_paths:
        file = file.strip().split("/")[0]  # Get the top-level world directory
        print(file)
        try:
            if os.path.exists(f"{worldsdir}/{file}/Register.py"):
                print(f"Fixing {file}")
                with open(f"{worldsdir}/{file}/Register.py", "r") as registerworldfile:
                    registerworld = registerworldfile.readlines()
                    for index, line in enumerate(registerworld):
                        if "CLIENT_FUNCTION = None" in line:
                            registerworld[index] = "CLIENT_FUNCTION = launch\n"
                            if os.path.exists(f"{worldsdir}/{file}/pyproject.toml"):
                                with open(f"{worldsdir}/{file}/pyproject.toml", "r") as pyprojectfile:
                                    pyprojectdata = pyprojectfile.readlines()
                                    for pyprojectindex, pyprojectline in enumerate(pyprojectdata):
                                        if "project.entry-points" in pyprojectline:
                                            break
                                        if "tool.setuptools.packages.find" in pyprojectline:
                                            pyprojectdata[pyprojectindex-2] = f'\n[project.entry-points."mwgg.client"]\n{file}.Client = "{file}.Register:CLIENT_FUNCTION"\n\n'
                                with open(f"{worldsdir}/{file}/pyproject.toml", "w") as pyprojectfile:
                                    pyprojectfile.writelines(pyprojectdata)
                with open(f"{worldsdir}/{file}/Register.py", "w") as registerworldfile:
                    registerworldfile.writelines(registerworld)
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue