from BaseClasses import Item, ItemClassification
from typing import Dict, List
from .Locations import raw_location_dict
from .Options import PowerwashSimulatorOptions

class PowerwashSimulatorItem(Item):
    game = "Powerwash Simulator"

unlock_items = [f"{location} Unlock" for location in raw_location_dict]
progression_items: List[str] = unlock_items + ["A Job Well Done"]
filler_items: List[str] = ["Dirt", "Grime", "Satisfaction", "Water", "Sponge", "Bubblegum Flavored Soap", "H2O", "Positive Reviews", "C17H35COONa", "Dust Bnuy", "Dust Bunny", "$WashCoin", "Suds"]

item_table: Dict[str, ItemClassification] = {
    **{item: ItemClassification.progression for item in progression_items},
    **{item: ItemClassification.filler for item in filler_items}
}

raw_items = progression_items + filler_items

def create_items(world):
    options: PowerwashSimulatorOptions = world.options
    pool = world.multiworld.itempool
    starting_location = world.player_starting_location[world.player_name]

    if options.goal_type == 1:
        for location in options.get_locations():
            if location == starting_location: continue
            pool.append(world.create_item(f"{location} Unlock"))

    item_steps = world.player_item_steps[world.player_name]
    for _ in range(item_steps["total mcguffins"]):
        pool.append(world.create_item("A Job Well Done"))

    for _ in range(item_steps["total"] - item_steps["filler"] - item_steps["total progression"]):
        pool.append(world.create_item(world.random.choice(filler_items)))

    if item_steps["added filler"] <= 0: return
    for _ in range(item_steps["added filler"]):
        pool.append(world.create_item(world.random.choice(filler_items)))