import hashlib
import logging
import os
import typing
from random import Random

import settings
from .data.static_data import endings
from .data.item_data import item_by_group
from .data.location_data import text_lookup
from .text_constructor import message_byte_constructor

import Utils
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

logger = logging.getLogger("Madou Monogatari Hanamaru Daiyouchienji")

base_save_offset = 0x12724
text_space_offset = 0x19bd20
text_space_offset_ram = 0x33bd20
HASH = 'fe6af670466c1e64538a4d14ad033440'

if typing.TYPE_CHECKING:
    from . import MadouWorld


class RomData:
    def __init__(self, file: bytes, name: typing.Optional[str] = None):
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_bytes(self, offset: int, length: int) -> bytearray:
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int) -> None:
        self.file[offset] = value

    def write_bytes(self, offset: int, values: typing.Sequence[int]) -> None:
        self.file[offset:offset + len(values)] = values

    def get_bytes(self) -> bytes:
        return bytes(self.file)


class MadouProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH]
    game = "Madou Monogatari Hanamaru Daiyouchienji"
    patch_file_ending = ".apmmhd"
    procedure = [
        ("apply_tokens", ["token_patch.bin"]),
        ("calc_snes_crc", [])
    ]
    name: bytes  # used to pass to __init__

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def initial_patch(world: "MadouWorld", patch: MadouProcedurePatch):
    # Create new method, which does not increment $1333 if the item's ID is $00; this is placed on all items that will be dummied out.
    patch.write_token(APTokenTypes.WRITE, 0x007090, bytes([
        0xa5, 0x1e,  # LDA $1e
        0xc9, 0x00,  # CMP #$00
        0xf0, 0x08,  # BEQ +8
        0x18,  # CLC
        0x99, 0x00, 0x00,  # LDA $0000, y
        0x5c, 0x3d, 0xcf, 0x01,  # JSL $01cf3d, which is the increment code
        0x18,  # CLC
        0x5c, 0x40, 0xcf, 0x01,  # JL $01cf40, which is one after the increment code
        0x6b,  # RTL; not needed necessarily but who knows.
    ]))
    # Modify the encounter rate code, so that the stored encounter
    # Add a jump to the item code, which jumps to the above.
    patch.write_token(APTokenTypes.WRITE, 0xcf38, bytes([
        0x5c, 0x90, 0xf0, 0x00,  # JSL $00f090, which should be the above.
    ]))
    # Fix bug where checking for Bayohihihi checks for Braindumbed instead.
    patch.write_token(APTokenTypes.WRITE, 0xc7c6, bytes([0x0e]))
    # Patch every in-game instance where an item is added to inventory, to instead call $00, so the above is triggered, effectively making it so no item is given.
    patch.write_token(APTokenTypes.WRITE, 0x183e92, bytes([0x00]))  # Dark Orb
    patch.write_token(APTokenTypes.WRITE, 0x17911a, bytes([0x00]))  # Elephant Head
    patch.write_token(APTokenTypes.WRITE, 0x176223, bytes([0x00]))  # Magical Staff Lofu
    patch.write_token(APTokenTypes.WRITE, 0x175fbf, bytes([0x00]))  # Yellow Gem
    patch.write_token(APTokenTypes.WRITE, 0x184354, bytes([0x00]))  # Ripe Cucumber
    patch.write_token(APTokenTypes.WRITE, 0x175f63, bytes([0x00]))  # Green Gem
    patch.write_token(APTokenTypes.WRITE, 0x1761c7, bytes([0x00]))  # Magical Ring Rele
    patch.write_token(APTokenTypes.WRITE, 0x182f95, bytes([0x00]))  # Light Orb
    patch.write_token(APTokenTypes.WRITE, 0x1649f0, bytes([0x00]))  # Dark Flower
    patch.write_token(APTokenTypes.WRITE, 0x17601b, bytes([0x00]))  # Cyan Gem
    patch.write_token(APTokenTypes.WRITE, 0x1793fd, bytes([0x00]))  # Mandrake Leaf
    patch.write_token(APTokenTypes.WRITE, 0x17627f, bytes([0x00]))  # Magic Crystal
    patch.write_token(APTokenTypes.WRITE, 0x176337, bytes([0x00]))  # Dragon Meat
    patch.write_token(APTokenTypes.WRITE, 0x1762db, bytes([0x00]))  # Soy Veggies
    patch.write_token(APTokenTypes.WRITE, 0x176393, bytes([0x00]))  # Cotton Ball Grass
    patch.write_token(APTokenTypes.WRITE, 0x186f36, bytes([0x00]))  # Turtle Heart
    patch.write_token(APTokenTypes.WRITE, 0x187015, bytes([0x00]))  # VIP Pass
    patch.write_token(APTokenTypes.WRITE, 0x1872b0, bytes([0x00]))  # Cotton Ball Grass (Ancient Village)
    patch.write_token(APTokenTypes.WRITE, 0x1871dd, bytes([0x00]))  # Stroll Grass
    patch.write_token(APTokenTypes.WRITE, 0x18710a, bytes([0x00]))  # Crown Grass
    patch.write_token(APTokenTypes.WRITE, 0x18739a, bytes([0x00]))  # Dragon Meat but Ancient Village
    patch.write_token(APTokenTypes.WRITE, 0x175f07, bytes([0x00]))  # Purple Gem
    patch.write_token(APTokenTypes.WRITE, 0x16f740, bytes([0x00]))  # Bouquet
    patch.write_token(APTokenTypes.WRITE, 0x17616b, bytes([0x00]))  # Blue Gem
    patch.write_token(APTokenTypes.WRITE, 0x165149, bytes([0x00]))  # Bazaar Pass
    patch.write_token(APTokenTypes.WRITE, 0x16ee03, bytes([0x00]))  # Firefly Egg 1
    patch.write_token(APTokenTypes.WRITE, 0x1651eb, bytes([0x00]))  # Firefly Egg 2
    patch.write_token(APTokenTypes.WRITE, 0x163700, bytes([0x00]))  # White Gem
    patch.write_token(APTokenTypes.WRITE, 0x176077, bytes([0x00]))  # Red Gem
    # Patch every spell instance so it never adds anything.
    patch.write_token(APTokenTypes.WRITE, 0x175d32, bytes([0x00]))  # Jugem
    patch.write_token(APTokenTypes.WRITE, 0x180a97, bytes([0x00]))  # Bayohihihii
    patch.write_token(APTokenTypes.WRITE, 0x180a47, bytes([0x00]))  # BAYOEEEEEEEEEEEEEEEN
    patch.write_token(APTokenTypes.WRITE, 0x180a6f, bytes([0x00]))  # Braindumbed
    patch.write_token(APTokenTypes.WRITE, 0x175997, bytes([0x00]))  # Fire Magic (N-S Cave)
    patch.write_token(APTokenTypes.WRITE, 0x175c82, bytes([0x00]))  # Heedon
    patch.write_token(APTokenTypes.WRITE, 0x175b4f, bytes([0x00]))  # Healing Magic (Ruins)
    patch.write_token(APTokenTypes.WRITE, 0x181ddf, bytes([0x00]))  # Ice Storm Magic (Wolves)
    patch.write_token(APTokenTypes.WRITE, 0x181e1d, bytes([0x00]))  # Thunder Magic (Dark Forest)
    patch.write_token(APTokenTypes.WRITE, 0x175ba3, bytes([0x00]))  # Diacute Magic (Dark Forest)
    patch.write_token(APTokenTypes.WRITE, 0x180b28, bytes([0x00]))  # Fire Magic (Library)
    patch.write_token(APTokenTypes.WRITE, 0x181e1d, bytes([0x00]))  # Thunder Magic (N-S Cave)
    patch.write_token(APTokenTypes.WRITE, 0x175b82, bytes([0x00]))  # Diacute Magic (N-S Cave Lower)  (Might be also another one)
    patch.write_token(APTokenTypes.WRITE, 0x1759ef, bytes([0x00]))  # Ice Storm Magic (N-S Cave Lower)
    patch.write_token(APTokenTypes.WRITE, 0x175dac, bytes([0x00]))  # Ice Storm Magic (Library Secret)
    patch.write_token(APTokenTypes.WRITE, 0x175af7, bytes([0x00]))  # Healing Magic (N-S Cave Lower)
    patch.write_token(APTokenTypes.WRITE, 0x175cda, bytes([0x00]))  # Revia Magic
    patch.write_token(APTokenTypes.WRITE, 0x175a9f, bytes([0x00]))  # Healing Magic (Dragon Shrine)
    patch.write_token(APTokenTypes.WRITE, 0x181da5, bytes([0x00]))  # Fire Magic (Library Secret)
    patch.write_token(APTokenTypes.WRITE, 0x175a47, bytes([0x00]))  # Thunder Magic (???)
    patch.write_token(APTokenTypes.WRITE, 0x175df0, bytes([0x00]))  # Thunder Magic (Library Secret)
    # Make it so "fast" is the default for text speed.
    patch.write_token(APTokenTypes.WRITE, base_save_offset + 0x06, bytes([0x00]))
    # Neuter the possibility of the game giving the player a tool.
    patch.write_token(APTokenTypes.WRITE, 0x160a2a, bytes([0x6b]))
    #  Sets the flag for reading all the books in the library.
    patch.write_token(APTokenTypes.WRITE, base_save_offset + 0xa5, bytes([0xf0, 0xff]))
    # Make Carbuncle show up immediately.
    patch.write_token(APTokenTypes.WRITE, 0x16fa8b, bytes([0x88, 0x01]))
    #  Forces the situation where the orb in light forest is dark by patching out the intro setting it to 0x03.
    patch.write_token(APTokenTypes.WRITE, 0x180136, bytes([0x88, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x180139, bytes([0x88, 0x01]))
    #  Skips the kindergarten intro, since its tedious.
    patch.write_token(APTokenTypes.WRITE, base_save_offset + 0x79, bytes([0x0e]))
    #  Skips most of the frog stuff and skips the puzzle.
    patch.write_token(APTokenTypes.WRITE, base_save_offset + 0x7c, bytes([0x05]))
    # Makes it so that the frog does not show up to "remove" the boots when you leave without fighting Sukiyapodes.
    patch.write_token(APTokenTypes.WRITE, 0x150ad4, bytes([0x3a]))
    # Also makes it so the frog does not give you the boots at all, just in case.  It just writes to something already having this flag.
    # There's a few other instances of this.  I know that at some point the game naturally sets 13b4 to 1, and then 2, and 2 lets you jump up more stuff,
    # but where this happens I'm not aware yet.  Hopefully this deals with it.
    patch.write_token(APTokenTypes.WRITE, 0x182b7c, bytes([0x88, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x182aa1, bytes([0x88, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x182420, bytes([0x88, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x181f0c, bytes([0x88, 0x01]))
    # Patch out situation where Sukiyapodes fight removes your shoes for whatever reason.
    patch.write_token(APTokenTypes.WRITE, 0x1823ff, bytes([0x9a]))
    patch.write_token(APTokenTypes.WRITE, 0x182404, bytes([0x28, 0x01]))
    # Skips when Suketoudora runs away from Ancient Ruins.
    patch.write_token(APTokenTypes.WRITE, base_save_offset + 0x9F, bytes([0x20])),
    # Skips part where Suketoudora moves to his house.
    patch.write_token(APTokenTypes.WRITE, base_save_offset + 0x8a, bytes([0x02])),
    # Puts Scorpion Guy in the boat.
    patch.write_token(APTokenTypes.WRITE, 0x1515b3, bytes([0x88, 0x01]))
    # Patches for the school incident.  Makes the school frozen, and moves the victory read for entering the headmaster room elsewhere.
    patch.write_token(APTokenTypes.WRITE, base_save_offset + 0x7f, bytes([0x08])),
    patch.write_token(APTokenTypes.WRITE, 0x150735, bytes([0x0f, 0x01]))
    # Change flag that would usually be set given the book.
    patch.write_token(APTokenTypes.WRITE, 0x17a6d9, bytes([0x88, 0x01]))
    # Force harpy door to be open
    patch.write_token(APTokenTypes.WRITE, 0x17b1d7, bytes([0x88, 0x01]))
    # Modify where the "fail" saves in the villages go so regardless of what you do you get everything.
    patch.write_token(APTokenTypes.WRITE, 0x17d43c, bytes([0x88, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x17d4c2, bytes([0x88, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x17d540, bytes([0x88, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x17d5be, bytes([0x88, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x17d63c, bytes([0x88, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x17d6ba, bytes([0x88, 0x01]))
    # Change setting flag for being given Bouquet.
    patch.write_token(APTokenTypes.WRITE, 0x16f704, bytes([0xFB, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x16f782, bytes([0xFB, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x16f734, bytes([0xFB, 0x00]))
    # Removes all secret stone increments.
    patch.write_token(APTokenTypes.WRITE, 0x162a98, bytes([0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x16f2ef, bytes([0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x17830c, bytes([0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x17b649, bytes([0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x17bdec, bytes([0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x17d3a6, bytes([0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x182496, bytes([0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x184d7a, bytes([0x00]))
    # Removes all in-game attempts to add secret stones to the inventory icons.  Moves setting to zero to 139A, so never use it for anything!
    patch.write_token(APTokenTypes.WRITE, 0x18248f, bytes([0x9a, 0x13, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x178305, bytes([0x9a, 0x13, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x184d73, bytes([0x9a, 0x13, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x17bde5, bytes([0x9a, 0x13, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x17b642, bytes([0x9a, 0x13, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x17d3bf, bytes([0x9a, 0x13, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x16f2e8, bytes([0x9a, 0x13, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x162a91, bytes([0x9a, 0x13, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x17d39f, bytes([0x9a, 0x13, 0x00]))
    # Patch out toggles for in-game item icons that are in the status bar.
    patch.write_token(APTokenTypes.WRITE, 0x181f07, bytes([0x9a, 0x13, 0x00]))  # Ribbit Boots
    patch.write_token(APTokenTypes.WRITE, 0x17eeec, bytes([0x9a, 0x13, 0x00]))  # Magic Bracelet
    patch.write_token(APTokenTypes.WRITE, 0x183096, bytes([0x9a, 0x13, 0x00]))  # Panotty Flute
    patch.write_token(APTokenTypes.WRITE, 0x183f1a, bytes([0x9a, 0x13, 0x00]))  # HAMMER
    patch.write_token(APTokenTypes.WRITE, 0x17a6dc, bytes([0x9a, 0x13, 0x00]))  # Magical Dictionary
    patch.write_token(APTokenTypes.WRITE, 0x175e93, bytes([0x9a, 0x13, 0x00]))  # Ribbon
    patch.write_token(APTokenTypes.WRITE, 0x165171, bytes([0x9a, 0x13, 0x00]))  # Toy Elephant
    # Patch Carbuncle interaction to refer to another flag.
    patch.write_token(APTokenTypes.WRITE, 0x16fa92, bytes([0xF9, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x16fb2f, bytes([0xF9, 0x00]))
    # Patch the explosion event to give the book instead.
    patch.write_token(APTokenTypes.WRITE, 0x179dc5, bytes([0xFD, 0x00]))
    # Make it so Wood Man always shows up
    patch.write_token(APTokenTypes.WRITE, base_save_offset + 0x9d, bytes([0x80]))
    # Change the VIP flag
    patch.write_token(APTokenTypes.WRITE, 0x18700d, bytes([0xFC, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x186ff7, bytes([0xFC, 0x00]))
    # Patch the shop item locations so the flags aren't tied.
    patch.write_token(APTokenTypes.WRITE, 0x1650f3, bytes([0xF4, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x165155, bytes([0xF4, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x1651e1, bytes([0xF5, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x1651bc, bytes([0xF5, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x165103, bytes([0xF5, 0x00]))
    # Patch the final exam certificate chest to refer instead to the flag that opens the gate.
    patch.write_token(APTokenTypes.WRITE, 0x1760d4, bytes([0x6b, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x17610f, bytes([0x6b, 0x01]))
    # Make the dragon always show up in the Bazaar.
    patch.write_token(APTokenTypes.WRITE, base_save_offset + 0x82, bytes([0x01]))
    # Patch the check for whether the egg is in your inventory first time.
    patch.write_token(APTokenTypes.WRITE, 0x16e310, bytes([0xF6, 0x00]))
    # Patch the check for adding firefly egg so its always in the shop.
    patch.write_token(APTokenTypes.WRITE, 0x172167, bytes([0x88, 0x01]))
    # Patch chest items which give important items that are flag relevant.
    # Elephant Head
    patch.write_token(APTokenTypes.WRITE, 0x17912b, bytes([0xF8, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x17907c, bytes([0xF8, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x1790fc, bytes([0xF8, 0x00]))
    # Ripe Cucumber
    patch.write_token(APTokenTypes.WRITE, 0x184323, bytes([0xFA, 0x00]))
    patch.write_token(APTokenTypes.WRITE, 0x184365, bytes([0xFA, 0x00]))
    # Move all flags on the library secret door.
    patch.write_token(APTokenTypes.WRITE, 0x1807de, bytes([0x08, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x1807e5, bytes([0x09, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x1807ec, bytes([0x0a, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x1807f3, bytes([0x0b, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x1807fa, bytes([0x0c, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x180801, bytes([0x0d, 0x01]))
    patch.write_token(APTokenTypes.WRITE, 0x180808, bytes([0x0e, 0x01]))
    # Change the $13e3 checks for giving a stone, checking if Suketoudara shows up, or if the fairy quest starts,
    # where it checks your current stone count, to instead chest $1397, $1398, $1399 instead.  The client will set these value on its on when necessary.
    patch.write_token(APTokenTypes.WRITE, 0x1626fc, bytes([0x97, 0x13]))
    patch.write_token(APTokenTypes.WRITE, 0x1630ae, bytes([0x98, 0x13]))
    patch.write_token(APTokenTypes.WRITE, 0x186415, bytes([0x99, 0x13]))
    from Utils import __version__
    patch_name = bytearray(
        f'Madou{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch_name.extend([0] * (21 - len(patch_name)))
    patch.name = bytes(patch_name)
    patch.write_token(APTokenTypes.WRITE, 0x3C000, patch.name)

    patch.write_token(APTokenTypes.COPY, 0x7FC0, (21, 0x3C000))


def text_patch(world: "MadouWorld", patch: MadouProcedurePatch):
    # Patch Mandrake text so leaves -> item, or multiworld item:
    patch.write_token(APTokenTypes.WRITE, 0x5a55e, bytes([
        0x1b, 0x26, 0x17, 0x1f
    ]))
    patch.write_token(APTokenTypes.WRITE, 0x5a59e, bytes([
        0x1b, 0x26, 0x17, 0x1f
    ]))
    patch.write_token(APTokenTypes.WRITE, 0x5a5b4, bytes([
        0x1b, 0x26, 0x17, 0x1f
    ]))
    patch.write_token(APTokenTypes.WRITE, 0x5a5d7, bytes([
        0x1b, 0x26, 0x17, 0x1f
    ]))
    # King Frog refers to an item.
    patch.write_token(APTokenTypes.WRITE, 0x18d917, bytes([
        0x15, 0x21, 0x21, 0x1e, 0x00, 0x1b, 0x26, 0x17, 0x1f, 0x49, 0x00, 0x00, 0x00
    ]))
    patch.write_token(APTokenTypes.WRITE, 0x18dac4, bytes([
        0x45, 0x21, 0x27, 0x00, 0x15, 0x13, 0x20, 0x00, 0x1a, 0x13, 0x28, 0x17, 0x00, 0x26, 0x1a,
        0x1b, 0x25, 0xf9, 0x1f, 0x27, 0x1e, 0x26, 0x1b, 0x29, 0x21, 0x24, 0x1e, 0x16, 0x00, 0x1b,
        0x26, 0x17, 0x1f, 0x47, 0x00, 0x00
    ]))
    # Add text for all the general locations, usually reading a tablet, opening a chest, etc.
    current_position = 0
    for location in world.get_locations():
        if location.address not in text_lookup:
            continue
        if text_lookup[location.address] is None:
            continue
        if not world.options.souvenir_hunt and location.address in range(130, 140):
            continue
        for container in text_lookup[location.address]:
            if container.hex_address == 0:
                logger.warning(f"Could not find a valid address for location {location.name} for Player {location.player}, of type {container.container}.  Skipping.")
                continue
            message = message_byte_constructor(location.item, container.container)
            patch.write_token(APTokenTypes.WRITE, text_space_offset + current_position, message)
            patch.write_token(APTokenTypes.WRITE, container.hex_address, (text_space_offset_ram + current_position).to_bytes(3, "little"))
            current_position += len(message)


def patch_rom(world: "MadouWorld", random: Random, patch: MadouProcedurePatch) -> None:
    initial_patch(world, patch)
    text_patch(world, patch)
    # Written slot data.
    ending = world.options.goal.value
    goal_address = endings[ending][0]
    goal_flag = endings[ending][1]
    required_stones = world.options.required_secret_stones.value
    skip_fairy = world.options.skip_fairy_search.value

    patch.write_token(APTokenTypes.WRITE, 0x0070c0, bytes(
        [
            goal_address, goal_flag, required_stones, 0x00, skip_fairy  # Fourth value will be exp rate later.
        ]
    ))
    starting_spells = world.options.starting_magic.value
    if "Healing" not in starting_spells:
        patch.write_token(APTokenTypes.WRITE, base_save_offset + 0x37, bytes([0x00]))
    if "Fire" not in starting_spells:
        patch.write_token(APTokenTypes.WRITE, base_save_offset + 0x39, bytes([0x00]))
    if "Ice Storm" not in starting_spells:
        patch.write_token(APTokenTypes.WRITE, base_save_offset + 0x3A, bytes([0x00]))
    if "Thunder" not in starting_spells:
        patch.write_token(APTokenTypes.WRITE, base_save_offset + 0x3B, bytes([0x00]))
    if world.options.squirrel_stations:  # Move the station flags to write to a free spot in save memory.
        patch.write_token(APTokenTypes.WRITE, 0x150330, bytes([0xEE, 0x00]))
        patch.write_token(APTokenTypes.WRITE, 0x152815, bytes([0xE8, 0x00]))
        patch.write_token(APTokenTypes.WRITE, 0x1515a7, bytes([0xEF, 0x00]))
        patch.write_token(APTokenTypes.WRITE, 0x150b80, bytes([0xE9, 0x00]))
        patch.write_token(APTokenTypes.WRITE, 0x171446, bytes([0xEA, 0x00]))
    if world.options.souvenir_hunt:
        patch.write_token(APTokenTypes.WRITE, 0x16545a, bytes([0x00]))  # Ruins Souvenir 1
        patch.write_token(APTokenTypes.WRITE, 0x165482, bytes([0x00]))  # Ruins Souvenir 2
        patch.write_token(APTokenTypes.WRITE, 0x1654aa, bytes([0x00]))  # Ruins Souvenir 3
        patch.write_token(APTokenTypes.WRITE, 0x1654d2, bytes([0x00]))  # Ruins Souvenir 4
        patch.write_token(APTokenTypes.WRITE, 0x1655bc, bytes([0x00]))  # Wolves 1
        patch.write_token(APTokenTypes.WRITE, 0x1655e4, bytes([0x00]))  # Wolves 2
        patch.write_token(APTokenTypes.WRITE, 0x165547, bytes([0x00]))  # Bazaar 1
        patch.write_token(APTokenTypes.WRITE, 0x165121, bytes([0x00]))  # Bazaar 2
    if world.options.school_lunch == world.options.school_lunch.option_consumables:
        consumables = item_by_group["Consumable"] + item_by_group["Equipment"]
        chosen_items = random.sample(consumables, 4)
        patch.write_token(APTokenTypes.WRITE, 0x1272d, bytes([
            chosen_items[0].hex_info[0].value, chosen_items[1].hex_info[0].value, chosen_items[2].hex_info[0].value, chosen_items[3].hex_info[0].value,
        ]))
    elif world.options.school_lunch == world.options.school_lunch.option_anything:
        patch.write_token(APTokenTypes.WRITE, 0x1272d, bytes([
            0x00, 0x00, 0x00, 0x00
        ]))
    if world.options.reduced_encounters:
        # Make new method that just doubles the encounter cap for the map.
        patch.write_token(APTokenTypes.WRITE, 0x007080, bytes([
            0xB9, 0x01, 0x00,  # LDA $0001, y
            0x0A,  # ASL
            0x8D, 0x0C, 0x14,  # STA $140C
            0x5C, 0x7E, 0x8a, 0x02  # JSL $02A783
        ]))
        patch.write_token(APTokenTypes.WRITE, 0x10a78, bytes([0x5C, 0x80, 0xf0, 0x00]))
    cookies = world.options.starting_cookies.value.to_bytes(2, "little")
    patch.write_token(APTokenTypes.WRITE, 0x1272b, cookies)
    patch.write_file("token_patch.bin", patch.get_token_binary())
    required_stones = world.options.required_secret_stones.value
    patch.write_token(APTokenTypes.WRITE, 0x186417, required_stones.to_bytes(1, "little"))


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if HASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom is not the patched english version.')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["madou_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
