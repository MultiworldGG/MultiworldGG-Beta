# This is a list of hex changes that should be made when patching the ROM.  Names are what they are for future help.
# The game's template save data is stored at 0x1271a to 0x1290b
#  Which places the current save's information at 0x001300 to 0x0014E9

save_offset = 0x12724

# The following are already off-set, so the above should slot into the appropriate spot.
static_patches = {
    0x0000A5: 0xF0,  # Skip Library Books, first half
    0x0000A6: 0xFF,  # Skip Library Books, second half
    0x000079: 0x0f,  # Skips the entire Kindergarten intro and makes harpy steal your stuff (0x07 + 0x08).
    0x00007c: 0x05,  # Skips meeting King Frog and solving the annoying puzzle.
    0x00009F: 0x20,  # Skips when Suketoudora runs away from Ancient Ruins.
    0x00008A: 0x02,  # Skips part where Suketoudora moves to his house.
    0x000037: 0x10,  # Puts Scorpion Guy in the boat.  However this also triggers the cutscene where Zoh slams the door on you.
    0x00007f: 0x08,  # Turns everyone in school to stone and the headmaster stinky.
    0x00008b: 0x04,  # Places Suketoudora at the school to fight.  Put this behind 7 stones.
}

# certificate ending should be 0xa2, 0x08
endings = {
    0: (0xa2, 0x08),
    1: (0xa1, 0x80),
    2: (0x88, 0x02),
    3: (0x9c, 0x01),
}

#  EXP gained is stored at 0x00175a from the point at 0x01af13 (_ in ROM).  We can manipulate this for rates.

#  Whenever a new save is created, this part of memory is read to be copied to working RAM.  It should be modified if some starting spells are removed.
initialized_save_slot_data = {
    "Healing": 0x000037,
    "Fire": 0x000039,
    "Ice Storm": 0x00003a,
    "Thunder": 0x00003b,
    "Cookie": 0x000007  # if the number is larger than FF, it pushes over to the next value, 8
}

#  The item slots go up to 42.  This start at 0x001309, up to 0x001332.  0x001333 denotes how many items you have.  So when adding an item it should
#  check 1309, and so on.  There's likely an in-game method for it.  However, we should have two checks.  One, if a duplicate special item is given, so
#  it is skipped being given entirely, and, if the inventory is full, find the first slot in inventory which is "junk" and get rid of it.  Its mean but
#  it'll work.  Another solution is to "reserve" a number of slots.  In the worst case, ~24 items would need to be reserved, reducing the "junk" slots to 18.
#  So if the item is junk and the number is over 18, it says its full.  Otherwise its added.
#  0x02925e (address _ in the ROM) handles adding item ID stored at memory 0x00001e to the inventory.

status_item_icons = {
    "Panotty's Flute": 0x0000dc,
    "Magic Bracelet": 0x0000dd,
    "Sukiyapodes' Hammer": 0x0000de,
    "Magical Dictionary": 0x0000df,
    "Ribbit Boots Icon": 0x0000e0,
    "Magic Ribbon": 0x0000e1,
    "Toy Elephant": 0x0000e2,
    "Secret Stone Count": 0x0000e3,
    "Secret Stone Icon 1": 0x0000e4,
    "Secret Stone Icon 2": 0x0000e5,
    "Secret Stone Icon 3": 0x0000e6,
    "Secret Stone Icon 4": 0x0000e7,
    "Secret Stone Icon 5": 0x0000e8,
    "Secret Stone Icon 6": 0x0000e9,
    "Secret Stone Icon 7": 0x0000ea,
    "Secret Stone Icon 8": 0x0000eb,
}

special_case_items = {
    "Suketoudara's Terrorism": (0x00137f, 0x10),  # This address should be changed to avoid a softlock out of block maze due to headmaster.
    "Carbuncle": (0x00138d, 0x00),  #
    "Magical Dictionary": (0x00137b, 0x01)  # This also needs to be set, for some reason, so the book actually works.
}

#  Call at 0x028268 (_ in ROM) pulls value from Y to before determining how to modify the flag.
#  We could catch these early and stop them from being set by this sort of call.
flag_to_block = {
    0x00138e: 0x00,  # Flight flag for Magic Village...I hope.
    0x00138f: 0x00,  # Flight flag for Ruins Town
    0x00138d: 0x00,  # Meeting Carbuncle, but we need some other way to denote this happened?
}

#  Should note now, not later, that it seems common for the tools to have calls associated reading from 0x2f003c with 0x2f003e as the bank.
#  This will denote the values associated with calling for certain things.
tool_calls = {
    0x8a2a: 0x2c,  # Call for finding the first tool slot and fills it with the item stored at 0x00000b.
}

#  A lot of conditions check not for the item in your inventory, but if you checked the location.  These flags are like this.
flag_to_item = {
    (0x001388, 0x01): 0x5c,  # Cyan Gem
    (0x001382, 0x40): 0x4d,  # Bouquet
    (0x001382, 0x10): 0x4e,  # Firefly Egg
    #  Do the rest.
}

hidden_stats = {
    "Health": 0x000046,
    "Mana": 0x000048,
    "Experience": 0x000043,
    "Attack": 0x00004a,
    "Defense": 0x00004b,
    "Speed": 0x00004c,
}

# The way secret stone text works is that it reads your current stones count and does a lookup based on it.  Of course, having 8 causes a bug, but also, this means
# its hard to pinpoint a way to write custom text for those locations.  But here's the address for where the calls are stored at:
secret_stone_master_list_offset = 0x162702
counts_offset = 0x56f3

#  It turns out that instead of checking inventory, the game checks for if you checked the location.  Since this is a read,
#  it's possible to make a patch jump at around 0x029476, or _ in the ROM, which is where the game reads if a flag is set, and simply
#  check something else.  It may be prudent, then, to make a method to check inventory.  We can use 0x01cef7 to find the item.  If at
#  the end of the call, we get 0x01 in A, it did not find it, otherwise, if it finds the item in question, then the value stored at 0x00001e is the slot
#  the item is in.  Checking this, we can return a true, 0x00, or a false, 0x01.  This should put the game in the same state as if it was checking the flag.
#  We may have to do other things with items not in the standard inventory.  Documented below are the items where this is a problem.

special_item_checks = {
    (0x01379, 0x10):  0x4b,  # Throwing the head onto the platform checks for the chest, not the item.
}

#  Similarly to above, there's cases where a flag is read for more than one instance.  Sometimes the flag is good to have in one case, another not.
special_flag_checks = {
    (0x0137a, 0x10): 0x832f,  # The Zoh hallway checks this as does scorpion, but Zoh has this last value set in Y.
}

char_conversion = {
    ' ': 0x00,
    'a': 0x13,
    'b': 0x14,
    'c': 0x15,
    'd': 0x16,
    'e': 0x17,
    'f': 0x18,
    'g': 0x19,
    'h': 0x1a,
    'i': 0x1b,
    'j': 0x1c,
    'k': 0x1d,
    'l': 0x1e,
    'm': 0x1f,
    'n': 0x20,
    'o': 0x21,
    'p': 0x22,
    'q': 0x23,
    'r': 0x24,
    's': 0x25,
    't': 0x26,
    'u': 0x27,
    'v': 0x28,
    'w': 0x29,
    'x': 0x2a,
    'y': 0x2b,
    'z': 0x2c,
    'A': 0x2d,
    'B': 0x2e,
    'C': 0x2f,
    'D': 0x30,
    'E': 0x31,
    'F': 0x32,
    'G': 0x33,
    'H': 0x34,
    'I': 0x35,
    'J': 0x36,
    'K': 0x37,
    'L': 0x38,
    'M': 0x39,
    'N': 0x3a,
    'O': 0x3b,
    'P': 0x3c,
    'Q': 0x3d,
    'R': 0x3e,
    'S': 0x3f,
    'T': 0x40,
    'U': 0x41,
    'V': 0x42,
    'W': 0x43,
    'X': 0x44,
    'Y': 0x45,
    'Z': 0x46,
    '.': 0x47,
    ',': 0x48,
    '!': 0x49,
    '\'': 0x4a,
    ':': 0x4b,
    '?': 0x4c,
    '~': 0x4d,
    '\"': 0x4e,
    '(': 0x4f,
    ')': 0x50,
    '\n': 0xf9,
    '+': 0xfe,
    '-': 0x0b,
    # Page Break is 0xfe.
}
