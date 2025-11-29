from enum import Flag, auto
from typing import Dict, NamedTuple, Optional, Callable

from BaseClasses import Location, CollectionState
from worlds.phoa import PhoaOptions
from worlds.phoa.LogicExtensions import PhoaLogic


class PhoaFlag(Flag):
    DEFAULT = auto()
    NPCGIFTS = auto()
    MISC = auto()
    SHOPSANITY = auto()
    SMALLANIMALS = auto()
    RINCHESTS = auto()
    RINCONTAINERS = auto()


class PhoaLocation(Location):
    game: str = "Phoenotopia: Awakening"


class PhoaLocationData(NamedTuple):
    region: str
    address: Optional[int]
    rule: Optional[Callable[[CollectionState], bool]] = None
    flags: PhoaFlag = PhoaFlag.DEFAULT


def get_location_data(player: Optional[int], options: Optional[PhoaOptions]) -> Dict[str, PhoaLocationData]:
    logic = PhoaLogic(player)

    locations: Dict[str, PhoaLocationData] = {
        "Panselo Watchtower (East)": PhoaLocationData(
            region="Overworld",
            address=7676000,
            # Locked by Bat
        ),  # Heart Ruby
        "Panselo Rutea's laboratory": PhoaLocationData(
            region="Overworld",
            address=7676001,
            rule=lambda state: state.has("Slingshot", player) or
                               state.has("Bombs", player),
        ),  # Heart Ruby
        "End of Secret Fishing Spot": PhoaLocationData(
            region="Overworld",
            address=7676002,
        ),  # Energy Gem
        "Northeastern Treetops": PhoaLocationData(
            region="Overworld",
            address=7676003,
            rule=lambda state: state.has("Slingshot", player) or
                               state.has("Bombs", player),
        ),  # Moonstone
        "Underneath Boulder": PhoaLocationData(
            region="Overworld",
            address=7676004,
            rule=lambda state: state.has("Bombs", player),
        ),  # Moonstone
        "Overworld Encounter Near Sunflower Road": PhoaLocationData(
            region="Overworld",
            address=7676005,
            rule=lambda state: state.has("Slingshot", player) or
                               state.has("Bombs", player),
        ),  # Moonstone
        "Cave Blocked by Destructable Blocks": PhoaLocationData(
            region="Overworld",
            address=7676006,
            rule=lambda state: state.has("Bombs", player),
        ),  # Moonstone
        # "On Top of Anuri Temple": PhoaLocationData(
        #     region="Overworld",
        #     address=7676009,
        #     rule=lambda state: state.has("Sonic Spear", player),
        # ), # Moonstone
        "Fish Underneath Anuri Temple": PhoaLocationData(
            region="Overworld",
            address=7676007,
            rule=lambda state: state.has("Fishing Rod", player),
        ),  # Dragon's Scale
        "Gift from Alex": PhoaLocationData(
            region="Overworld",
            address=7676008,
        ),  # Slingshot
        "Skeleton Above First Gate": PhoaLocationData(
            region="Anuri Temple",
            address=7676009,
            rule=lambda state: logic.has_anuri_temple_access(state),
        ),  # Anuri Pearlstone
        "Maze with Scabers": PhoaLocationData(
            region="Anuri Temple",
            address=7676010,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Slingshot", player),
        ),  # Anuri Pearlstone
        "Press the Switches with Pots and Fruits": PhoaLocationData(
            region="Anuri Temple",
            address=7676011,
            rule=lambda state: logic.has_anuri_temple_access(state),
        ),  # Anuri Pearlstone
        "Carry Pot Across the Water and Bats": PhoaLocationData(
            region="Anuri Temple",
            address=7676012,
            rule=lambda state: logic.has_anuri_temple_access(state),
            # Requires Slingshot or Bombs
        ),  # Energy Gem
        "Stackable Pots Room": PhoaLocationData(
            region="Anuri Temple",
            address=7676013,
            rule=lambda state: logic.has_anuri_temple_access(state),
        ),  # Moonstone
        "Sprint-jump on Timed Switches": PhoaLocationData(
            region="Anuri Temple",
            address=7676014,
            rule=lambda state: logic.has_anuri_temple_access(state),
        ),  # Anuri Pearlstone
        "Tall Tower Puzzle Behind Locked Door": PhoaLocationData(
            region="Anuri Temple",
            address=7676015,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Anuri Pearlstone", player, 10),
            # Requires 1 pearlstone to enter
        ),  # Heart Ruby
        "Fight toads in treasure room": PhoaLocationData(
            region="Anuri Temple",
            address=7676016,
            rule=lambda state: logic.has_anuri_temple_access(state),
        ),  # Lunar Vase
        "Moveable Bridges Room": PhoaLocationData(
            region="Anuri Temple",
            address=7676017,
            rule=lambda state: logic.has_anuri_temple_access(state),
            # Requires Slingshot or Bombs
        ),  # Moonstone
        "Slingshot the switch and surfacing Toads": PhoaLocationData(
            region="Anuri Temple",
            address=7676018,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Slingshot", player),
        ),  # Anuri Pearlstone
        "Three Switches With Lots of Pots": PhoaLocationData(
            region="Anuri Temple",
            address=7676019,
            rule=lambda state: logic.has_anuri_temple_access(state),
        ),  # Anuri Pearlstone
        "Hit the Switch Hidden Under a Breakable Tomb": PhoaLocationData(
            region="Anuri Temple",
            address=7676020,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Bombs", player),
        ),  # Anuri Pearlstone
        "Push the Metal Pot Onto the Switch From Above": PhoaLocationData(
            region="Anuri Temple",
            address=7676021,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Bombs", player),
        ),  # Anuri Pearlstone
        "Within Sarcophagus": PhoaLocationData(
            region="Anuri Temple",
            address=7676022,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Bombs", player),
        ),  # Moonstone
        "Defeat the Glowing Slargummy": PhoaLocationData(
            region="Anuri Temple",
            address=7676023,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Bombs", player) and
                               state.has("Crank Lamp", player),
        ),  # Anuri Pearlstone
        "Time the gates through Scaber funnel": PhoaLocationData(
            region="Anuri Temple",
            address=7676024,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Anuri Pearlstone", player, 10),
            # Requires 1 pearlstone to enter
        ),  # Moonstone
        # "Fishing Spot After Slargummy": PhoaLocationData(
        #     region="Anuri Temple",
        #     address=7676025,
        #     rule=lambda state: logic.has_anuri_temple_access(state) and
        #                        state.has("Anuri Pearlstone", player, 6),
        #     # Requires 3 pearlstones to enter
        # ), # Moonstone
        # For some reason, the fish with the moonstone doesn't spawn on the first visit
        "Use Slingshot to Hit the Switches Below": PhoaLocationData(
            region="Anuri Temple",
            address=7676026,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Slingshot", player) and
                               state.has("Anuri Pearlstone", player, 9),
            # Requires 6 pearlstones to enter
        ),  # Anuri Pearlstone
        "Dive down in long vertical room": PhoaLocationData(
            region="Anuri Temple",
            address=7676027,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Anuri Pearlstone", player, 10) and
                               state.has("Life Saver", player),
            # Requires 7 pearlstones to enter
        ),  # Lunar Frog
        "West Panselo on top of roof": PhoaLocationData(
            region="Overworld",
            address=7676028,
            flags=PhoaFlag.MISC,
        ),  # Dandelion
        "East Panselo on top of roof": PhoaLocationData(
            region="Overworld",
            address=7676029,
            flags=PhoaFlag.MISC,
        ),  # Dandelion
        "Panselo coop egg": PhoaLocationData(
            region="Overworld",
            address=7676030,
            flags=PhoaFlag.MISC,
        ),  # Perro egg
        "Panselo Watchtower (West) hidden in box": PhoaLocationData(
            region="Overworld",
            address=7676031,
            flags=PhoaFlag.MISC,
        ),  # Cheese
        "Panselo on table in girls room": PhoaLocationData(
            region="Overworld",
            address=7676032,
            flags=PhoaFlag.MISC,
        ),  # Berry Fruit
        "On top of GEO house Panselo region": PhoaLocationData(
            region="Overworld",
            address=7676033,
            flags=PhoaFlag.MISC,
        ),  # Dandelion
        "On top of Franway panselo region": PhoaLocationData(
            region="Overworld",
            address=7676034,
            flags=PhoaFlag.MISC,
        ),  # Dandelion
        "Doki Forest cave guarded by gummies first item": PhoaLocationData(
            region="Overworld",
            address=7676035,
            flags=PhoaFlag.MISC,
        ),  # Doki Herb
        "Doki Forest cave guarded by gummies second item": PhoaLocationData(
            region="Overworld",
            address=7676036,
            flags=PhoaFlag.MISC,
        ),  # Doki Herb
        "Doki Forest cave guarded by gummies third item": PhoaLocationData(
            region="Overworld",
            address=7676037,
            flags=PhoaFlag.MISC,
        ),  # Doki Herb
        "Side entrance first item": PhoaLocationData(
            region="Anuri Temple",
            address=7676038,
            flags=PhoaFlag.MISC,
        ),  # Doki Herb
        "Side entrance second item": PhoaLocationData(
            region="Anuri Temple",
            address=7676039,
            flags=PhoaFlag.MISC,
        ),  # Doki Herb
        "Tall Tower Puzzle side item": PhoaLocationData(
            region="Anuri Temple",
            address=7676040,
            flags=PhoaFlag.MISC,
        ),  # Doki Herb
        "Lizard Panselo Left Tower": PhoaLocationData(
            region="Overworld",
            address=7676041,
            flags=PhoaFlag.SMALLANIMALS,
        ),  # Mystery Meat
        "Doki Forest cave guarded by gummies Lizard": PhoaLocationData(
            region="Overworld",
            address=7676042,
            flags=PhoaFlag.SMALLANIMALS,
        ),  # Mystery Meat
        "Doki Forest Lizard at climbable roots": PhoaLocationData(
            region="Overworld",
            address=7676043,
            flags=PhoaFlag.SMALLANIMALS,
        ),  # Mystery Meat
        "Doki Forest Lizard in Alcove": PhoaLocationData(
            region="Overworld",
            address=7676044,
            flags=PhoaFlag.SMALLANIMALS,
        ),  # Mystery Meat
        "Doki Forest First Lizard in Campfire Cave": PhoaLocationData(
            region="Overworld",
            address=7676045,
            flags=PhoaFlag.SMALLANIMALS,
        ),  # Mystery Meat
        "Doki Forest Second Lizard in Campfire Cave": PhoaLocationData(
            region="Overworld",
            address=7676046,
            flags=PhoaFlag.SMALLANIMALS,
        ),  # Mystery Meat
        "Lizard on Top of Climbable Vines at the Entrance": PhoaLocationData(
            region="Anuri Temple",
            address=7676047,
            flags=PhoaFlag.SMALLANIMALS,
            rule=lambda state: logic.has_anuri_temple_access(state)
        ),  # Mystery Meat
        "Lizard Behind Bombable Blocks": PhoaLocationData(
            region="Anuri Temple",
            address=7676048,
            flags=PhoaFlag.SMALLANIMALS,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Bombs", player),
        ),  # Mystery Meat
        "Lizard Right of Anuri Throne": PhoaLocationData(
            region="Anuri Temple",
            address=7676049,
            flags=PhoaFlag.SMALLANIMALS,
            rule=lambda state: logic.has_anuri_temple_access(state)
        ),  # Mystery Meat
        "Lizard Left of Anuri Throne": PhoaLocationData(
            region="Anuri Temple",
            address=7676050,
            flags=PhoaFlag.SMALLANIMALS,
            rule=lambda state: logic.has_anuri_temple_access(state)
        ),  # Mystery Meat
        "Lizard at the End of Treasure Room": PhoaLocationData(
            region="Anuri Temple",
            address=7676051,
            flags=PhoaFlag.SMALLANIMALS,
            rule=lambda state: logic.has_anuri_temple_access(state)
        ),  # Mystery Meat
        "Lizard in Movable Bridge Room": PhoaLocationData(
            region="Anuri Temple",
            address=7676052,
            flags=PhoaFlag.SMALLANIMALS,
            rule=lambda state: logic.has_anuri_temple_access(state)
        ),  # Mystery Meat
        "Lizard in Many Pots Room": PhoaLocationData(
            region="Anuri Temple",
            address=7676053,
            flags=PhoaFlag.SMALLANIMALS,
            rule=lambda state: logic.has_anuri_temple_access(state)
        ),  # Mystery Meat
        "Lizard in Water Steps Room": PhoaLocationData(
            region="Anuri Temple",
            address=7676054,
            flags=PhoaFlag.SMALLANIMALS,
            rule=lambda state: logic.has_anuri_temple_access(state)
        ),  # Mystery Meat
        "First Lizard in Side Entrance Room": PhoaLocationData(
            region="Anuri Temple",
            address=7676055,
            flags=PhoaFlag.SMALLANIMALS,
            rule=lambda state: logic.has_anuri_temple_access(state)
        ),  # Mystery Meat
        "Second Lizard in Side Entrance Room": PhoaLocationData(
            region="Anuri Temple",
            address=7676056,
            flags=PhoaFlag.SMALLANIMALS,
            rule=lambda state: logic.has_anuri_temple_access(state)
        ),  # Mystery Meat
        "Lizard at Treasure Room Before Century Toad": PhoaLocationData(
            region="Anuri Temple",
            address=7676057,
            flags=PhoaFlag.SMALLANIMALS,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Anuri Pearlstone", player, 9),
        ),  # Mystery Meat
        "Pot in Boys Room": PhoaLocationData(
            region="Overworld",
            address=7676058,
            flags=PhoaFlag.RINCONTAINERS,
        ),  # 5 Rin
        "Box Right Side of Orphanage Hall": PhoaLocationData(
            region="Overworld",
            address=7676059,
            flags=PhoaFlag.RINCONTAINERS,
        ),  # 9 Rin
        "Orphanage Attic Chest": PhoaLocationData(
            region="Overworld",
            address=7676060,
            flags=PhoaFlag.RINCHESTS,
        ),  # 35 Rin
        "Panselo Watchtower (West) Chest": PhoaLocationData(
            region="Overworld",
            address=7676061,
            flags=PhoaFlag.RINCHESTS,
        ),  # 35 Rin
        "Panselo Warehouse Chest": PhoaLocationData(
            region="Overworld",
            address=7676062,
            flags=PhoaFlag.RINCHESTS,
        ),  # 25 Rin
        "Doki Forest Chest in Alcove through Crawl Space": PhoaLocationData(
            region="Overworld",
            address=7676063,
            flags=PhoaFlag.RINCHESTS,
        ),  # 35 Rin
        "Anuri Skeleton at Bottom of Right Elevator Room": PhoaLocationData(
            region="Anuri Temple",
            address=7676064,
            flags=PhoaFlag.RINCONTAINERS,
            rule=lambda state: logic.has_anuri_temple_access(state),
        ),  # 15 Rin
        "Anuri Skeleton at Top Left Side of Many Pots Room": PhoaLocationData(
            region="Anuri Temple",
            address=7676065,
            flags=PhoaFlag.RINCONTAINERS,
            rule=lambda state: logic.has_anuri_temple_access(state),
        ),  # 15 Rin
        # "High up Right Pot in Maze Room": PhoaLocationData(
        #     region="Anuri Temple",
        #     address=7676066,
        #     flags=PhoaFlag.RINCONTAINERS,
        #     rule=lambda state: logic.has_anuri_temple_access(state),
        # ),  # 15 Rin
        "Big pot in Tomb Tunnel in Basement": PhoaLocationData(
            region="Anuri Temple",
            address=7676067,
            flags=PhoaFlag.RINCONTAINERS,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Bombs", player),
        ),  # 20 Rin
        "Nana's Pumpkin Muffin": PhoaLocationData(
            region="Overworld",
            address=7676068,
            flags=PhoaFlag.NPCGIFTS,
        ),  # Pumpkin Muffin
        "Jon's Potato": PhoaLocationData(
            region="Overworld",
            address=7676069,
            flags=PhoaFlag.NPCGIFTS,
        ),  # Panselo Potato
        "Free Gift from Panselo Shop Keeper Tao": PhoaLocationData(
            region="Overworld",
            address=7676070,
            flags=PhoaFlag.NPCGIFTS,
        ),  # Fruit Jam
        "Seth's Mystery Meat Gift": PhoaLocationData(
            region="Overworld",
            address=7676071,
            flags=PhoaFlag.NPCGIFTS,
        ),  # Mystery Meat
        "Panselo Shop Item 1": PhoaLocationData(
            region="Overworld",
            address=7676072,
            flags=PhoaFlag.SHOPSANITY,
        ),  # Perro egg
        "Panselo Shop Item 2": PhoaLocationData(
            region="Overworld",
            address=7676073,
            flags=PhoaFlag.SHOPSANITY,
        ),  # Milk
        "Panselo Shop Item 3": PhoaLocationData(
            region="Overworld",
            address=7676074,
            flags=PhoaFlag.SHOPSANITY,
        ),  # Panselo Potato
        "Bart's Head Crater": PhoaLocationData(
            region="Anuri Temple",
            address=7676075,
        ),  # Broken Golem Hat
        "Strange Urn": PhoaLocationData(
            region="Anuri Temple",
            address=None,
            rule=lambda state: logic.has_anuri_temple_access(state) and
                               state.has("Anuri Pearlstone", player, 9),
            # Requires 6 pearlstones to enter
        ),
    }

    if not options:
        return locations

    filters = [
        (options.enable_npc_gifts <= 0, PhoaFlag.NPCGIFTS),
        (options.enable_misc <= 0, PhoaFlag.MISC),
        (options.shop_sanity <= 0, PhoaFlag.SHOPSANITY),
        (options.enable_small_animal_drops <= 0, PhoaFlag.SMALLANIMALS),
        (options.enable_rin_locations <= 0, PhoaFlag.RINCHESTS),
        (options.enable_rin_locations <= 1, PhoaFlag.RINCONTAINERS),
    ]

    for option, flag in filters:
        if option:
            locations = {
                name: data for name, data in locations.items() if data.flags != flag
            }

    return locations
