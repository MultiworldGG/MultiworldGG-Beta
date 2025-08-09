from typing import Dict, Optional, List

from BaseClasses import ItemClassification, Item, Location
from worlds.AutoWorld import World

item_categories: Dict[ItemClassification, str] = {
    ItemClassification.filler: "useless",
    ItemClassification.useful: "useful",
    ItemClassification.trap: "valuable",  # It's a trap, so let's pretend it's a progression item
    ItemClassification.progression: "valuable",
    ItemClassification.progression_deprioritized: "valuable",
    ItemClassification.progression_skip_balancing: "valuable",
    ItemClassification.progression_deprioritized_skip_balancing: "valuable",
}


class HintData:
    name: str
    id: int
    text: str
    ignore_other_text: bool
    item_name: Optional[str] = None
    item_location: Optional[str] = None

    def __init__(self, json_data):
        self.name = json_data["name"]
        self.id = json_data["id"]
        self.text = json_data["text"]
        self.ignore_other_text = json_data["ignore_other_text"]
        if "item_name" in json_data:
            self.item_name = json_data["item_name"]
        if "item_location" in json_data:
            self.item_location = json_data["item_location"]


class Hint:
    id: int
    text: str
    ignore_other_text: bool

    def __str__(self):
        return f"{self.id}: {self.text}"


hint_data: Dict[int, HintData] = {}


def generate_hints(world: World):
    world.hints = []

    for hint_id, hintdata in hint_data.items():
        location: Optional[Location] = None

        if hintdata.item_location is not None:
            location = world.multiworld.get_location(hintdata.item_location, world.player)
        if hintdata.item_name is not None:
            choices = world.multiworld.find_item_locations(hintdata.item_name, world.player)
            if len(choices) > 0:
                location = world.hint_rng.choice(choices)

        if location is None:
            continue

        hint = Hint()
        hint.id = hint_id
        hint.ignore_other_text = hintdata.ignore_other_text
        hint.text = (hintdata.text
                     .replace('{area}', get_area_name_for_location(world, location, world.player))
                     .replace('{category}', get_category_for_item(location.item))
                     .replace("{item}", f"{{{location.item.name}}}"))
        world.hints.append(hint)

    sanctuary_hints = build_sanctuary_token_hints(world, world.player)
    world.hints.extend(sanctuary_hints)


def build_sanctuary_token_hints(world: World, player: int) -> List[Hint]:
    locations = world.multiworld.find_item_locations("Sanctuary Token", player)
    counts: Dict[str, int] = {}

    for location in locations:
        area = get_area_name_for_location(world, location, player)
        if area not in counts:
            counts[area] = 0
        counts[area] += 1

    # First build a straight list of the hint texts
    hints: List[str] = [
        "I have a hunch about where we can find the items required to open this door"
    ]
    for area, count in counts.items():
        verb = "is" if count == 1 else "are"
        hints.append(f"{count} {verb} {area}")

    # Now we merge hint texts down so that we get 2 at a time in a single dialog box
    merged_hints = []
    append = True
    for hint in hints:
        if append:
            # if this is the last hint, prepend "and" to the front
            if hint == hints[-1]:
                hint = f"and {hint}."
            merged_hints.append(hint)
        else:
            join = ","
            end = ","
            # if it's the first hint, add a colon
            if hint == hints[1]:
                join = ":"
            # If it's the last hint, add an and
            if hint == hints[-1]:
                join = ", and"
                end = "."

            merged_hints[-1] = f"{merged_hints[-1]}{join} {hint}{end}"
        append = not append

    # Lastly, now we set assign the dialog id to these
    # With only 5 locations, we'll have at most three hints
    dialog_ids = {
        0: [29300009, 29300013],
        1: [29300010, 29300014],
        2: [29300011, 29300016]
    }
    final_hints: List[Hint] = []
    for i in range(len(merged_hints)):
        for dialog_id in dialog_ids[i]:
            hint = Hint()
            hint.id = dialog_id
            hint.text = merged_hints[i]
            hint.ignore_other_text = False

            if i == len(merged_hints) - 1:
                hint.ignore_other_text = True

            final_hints.append(hint)

    return final_hints


def get_area_name_for_location(world: World, location: Location, player: int) -> str:
    if location.player != player:
        return get_another_world_text(world, location.player)

    return get_readable_area_name(get_trimmed_area_name(location, player))


def get_another_world_text(world: World, player: int):
    return f"in {world.multiworld.player_name[player]}'s world"


def get_trimmed_area_name(location: Location, player: int) -> str:
    if player != location.player:
        return location.name

    # converge item and monster location naming structures by getting rid of
    # spaces and converting hyphens to underscores
    return location.name.replace(' ', '').replace('-', '_').split('_')[0]


def get_readable_area_name(area: str) -> str:
    if area == "MountainPath":
        return "on the {Mountain Path}"
    elif area == "BlueCave":
        return "in the {Blue Caves}"
    elif area == "KeeperStronghold":
        return "in the {Keeper Stronghold}"
    elif area == "StrongholdDungeon":
        return "in the {Stronghold Dungeon}"
    elif area == "SnowyPeaks":
        return "on {Snowy Peaks}"
    elif area == "SunPalace":
        return "in {Sun Palace}"
    elif area == "AncientWoods":
        return "in the {Ancient Woods}"
    elif area == "HorizonBeach":
        return "at {Horizon Beach}"
    elif area == "MagmaChamber":
        return "in {Magma Chamber}"
    elif area == "BlobBurg":
        return "in {Blob Burg}"
    elif area == "Underworld":
        return "in the {Underworld}"
    elif area == "MysticalWorkshop":
        return "in the {Mystical Workshop}"
    elif area == "ForgottenWorld":
        return "in the {Forgotten World}"
    elif area == "AbandonedTower":
        return "in the {Abandoned Tower}"

    return "in an unknown location"


def get_category_for_item(item: Item) -> str:
    if ItemClassification.progression in item.classification:
        return "Progression"
    elif ItemClassification.useful in item.classification:
        return "Useful"
    elif ItemClassification.trap in item.classification:
        return "Progression"
    else:
        return "Filler"
