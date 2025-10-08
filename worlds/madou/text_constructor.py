from BaseClasses import ItemClassification, Item
from .data.static_data import char_conversion

line_cap = 28
chest_message = "There's a * here."
found = "Found *!"
generic_spell = "By reading this, the multiworld seems to resonate.+Suddenly, an item falls into your hands."
generic_found = "Found multiworld item!"  # Useful if something is called from multiple points, to avoid confusion.
spell_message = "By reading this, the multiworld seems to resonate.+Suddenly, * falls into your hands."
store_message = "*."

progression_message = {
    ItemClassification.progression | ItemClassification.useful: "Seems REALLY important.",
    ItemClassification.progression | ItemClassification.trap: "A necessary evil.",
    ItemClassification.progression: "Seems important.",
    ItemClassification.progression_skip_balancing: "Seems important.",
    ItemClassification.useful | ItemClassification.trap: "A blessing and a curse",
    ItemClassification.useful: "Seems nice to have.",
    ItemClassification.filler: "Seems okay.",
    ItemClassification.trap: "Seems suspicious...",
}


progression_colors = {
    ItemClassification.progression | ItemClassification.useful: 0x1b,
    ItemClassification.progression | ItemClassification.trap: 0x18,
    ItemClassification.progression: 0x27,
    ItemClassification.progression_skip_balancing: 0x27,
    ItemClassification.useful | ItemClassification.trap: 0x19,
    ItemClassification.useful: 0x14,
    ItemClassification.filler: 0x01,
    ItemClassification.trap: 0x13,
}


def message_byte_constructor(item: Item, container: str) -> bytes:
    item_name = item.name[:45].rstrip()
    if item.game == "Hollow Knight":
        item_name.replace("_", " ")  # Sorry Hollow Knight your naming convention blows.
    if item.classification not in progression_message:
        extra_message = "Who knows!"
    else:
        extra_message = progression_message[item.classification]
    if " " not in item.name:
        item_name = item.name[:15] + " " + item_name[15:]  # break the item in half because it'd break the message box otherwise.
    if container == "Chest":
        initial_message = chest_message.replace("*", item_name)
    elif container == "Spell":
        initial_message = spell_message.replace("*", item_name)
    elif container == "Shop":
        initial_message = store_message.replace("*", item_name) + "  " + extra_message
    elif container == "Generic":
        initial_message = generic_found  # TODO: Find a way to make these generic calls unnecessary; its jarring.
    elif container == "Generic Spell":
        initial_message = generic_spell
    else:
        initial_message = found.replace("*", item_name) + "  " + extra_message
    final_message = ""
    messages = initial_message.split("+")
    for i in range(len(messages)):
        if i != 0:
            final_message += "+"
        remaining_text = messages[i]
        while remaining_text != "":
            if len(remaining_text) > 28:
                cutoff = find_first_space(remaining_text, 27)
                final_message += remaining_text[:cutoff] + "\n"
                remaining_text = remaining_text[(cutoff + 1):]
            else:
                final_message += remaining_text
                remaining_text = ""

    output_string = determine_classification_bytes(item.classification)
    for char in final_message:
        if char not in char_conversion:
            char = "."
        value = char_conversion[char]
        output_string.extend([value])
    output_string.extend(([0xFE, 0xFF]))
    return bytes(output_string)


def determine_classification_bytes(classification: ItemClassification):
    if classification not in progression_colors:
        return bytearray([0xFC, 0x0D])
    return bytearray([0xFC, progression_colors[classification]])


def find_first_space(message: str, start: int):
    spot = start
    while spot != 0:
        if message[spot] == " ":
            break
        spot -= 1
    return spot

