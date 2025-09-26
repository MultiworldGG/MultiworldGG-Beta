from BaseClasses import Item, ItemClassification
from typing import Dict, List
from .Locations import raw_location_dict
from .Options import PowerwashSimulatorOptions

class PowerwashSimulatorItem(Item):
    game = "Powerwash Simulator"

unlock_items = [f"{location} Unlock" for location in raw_location_dict]
progression_a_items: List[str] = unlock_items
progression_b_items: List[str] = ["A Job Well Done"]
filler_items: List[str] = ["Dirt", "Grime", "Satisfaction", "Water", "Sponge", "Bubblegum Flavored Soap", "H2O", "Positive Reviews", "C17H35COONa", "Dust Bnuy", "Dust Bunny", "$WashCoin", "Suds", "Washed Grass"]

item_table: Dict[str, ItemClassification] = {
    **{item: ItemClassification.progression for item in progression_a_items},
    **{item: ItemClassification.progression_deprioritized_skip_balancing for item in progression_b_items},
    **{item: ItemClassification.filler for item in filler_items}
}

raw_items = progression_a_items + progression_b_items + filler_items

def create_items(world):
    options: PowerwashSimulatorOptions = world.options
    pool = world.multiworld.itempool
    starting_location = world.starting_location

    for location in options.get_locations():
        if location == starting_location: continue
        pool.append(world.create_item(f"{location} Unlock"))

    for _ in range(world.check_total_mcguffin_count):
        pool.append(world.create_item("A Job Well Done"))

    for _ in range(world.check_total_count - world.check_total_filler_count - world.check_total_progression_count):
        pool.append(world.create_item(world.random.choice(filler_items)))