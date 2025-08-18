import json
import pkgutil
# two-toned boots and fleshripper were duplicates.

base_item_location_array = json.loads(pkgutil.get_data("worlds.poe.data", "BaseItems.json").decode("utf-8"))
base_item_location_table = {}
for i, item in enumerate(base_item_location_array, start=1):
    item["id"] = i
    base_item_location_table[i] = item

base_item_set = set(item["baseItem"] for item in base_item_location_array)

level_location_array = json.loads(pkgutil.get_data("worlds.poe.data", "LevelLocations.json").decode("utf-8"))
level_location_table = {}
for i, item in enumerate(level_location_array,
                         start=(len(base_item_location_array) + 1)):# start counting ids at the end of the base item list
    item["id"] = i
    level_location_table[i] = item

data = pkgutil.get_data("worlds.poe.data", "Bosses.json")
bosses = json.loads(data.decode("utf-8"))


if __name__ == "__main__":
    full_location_table = base_item_location_table | level_location_table
    import json
    #print(json.dumps(full_location_table, indent=4))
    print(json.dumps(bosses, indent=4, ensure_ascii=False))