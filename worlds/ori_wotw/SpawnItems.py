"""Function for handling spawn items for random spawn."""

from .Options import StartingLocation

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import WotWWorld

spawn_names = ["MarshSpawn.Main",  # Name of the region linked to the teleporter
               "MidnightBurrows.Teleporter",
               "HowlsDen.Teleporter",
               "EastHollow.Teleporter",
               "GladesTown.Teleporter",
               "InnerWellspring.Teleporter",
               "WoodsEntry.Teleporter",
               "WoodsMain.Teleporter",
               "LowerReach.Teleporter",
               "UpperDepths.Teleporter",
               "EastPools.Teleporter",
               "WestPools.Teleporter",
               "LowerWastes.WestTP",
               "LowerWastes.EastTP",
               "UpperWastes.NorthTP",
               "WindtornRuins.RuinsTP",
               "WillowsEnd.InnerTP",]

def spawn_items(world: "WotWWorld", spawn: int, difficulty: int) -> list[str]:
    """
    Returns a set of spawn items for the chosen spawn point and difficulty.

    The items are stored in a list of dimension 3 for each difficulty ;
    with spawn location, item groups, items along 1st, 2nd, 3rd indexes respectively.
    """
    moki: list[list[list[str]]] = [
            [["Inkwater Marsh TP"]],
            [["Midnight Burrows TP", "Bash", "Double Jump"],
             ["Midnight Burrows TP", "Bash", "Dash"],
             ["Midnight Burrows TP", "Bash", "Glide"]],
            [["Howl's Den TP", "Double Jump"],
             ["Howl's Den TP", "Bash", "Grenade", "Sword"],
             ["Howl's Den TP", "Bash", "Grenade", "Hammer"]],
            [["Kwolok's Hollow TP", "Sword", "Dash", "Double Jump", "Regenerate", "Health Fragment", "Health Fragment",
              "Health Fragment", "Health Fragment"]],
            [["Glades TP", "Double Jump", "Dash", "Bash"],
             ["Glades TP", "Clean Water", "Water Dash"]],
            [["Wellspring TP"]],
            [["Woods Entrance TP", "Regenerate", "Health Fragment", "Health Fragment", "Health Fragment"]],
            [["Woods Exit TP", "Double Jump", "Grapple", "Glide", "Regenerate", "Health Fragment", "Health Fragment",
              "Health Fragment"],
             ["Woods Exit TP", "Dash", "Grapple", "Glide", "Regenerate", "Health Fragment", "Health Fragment",
              "Health Fragment"]],
            [["Baur's Reach TP", "Flap", "Double Jump", "Bash", "Grenade", "Regenerate", "Health Fragment",
              "Health Fragment", "Health Fragment"]],
            [["Mouldwood Depths TP", "Glide", "Regenerate", "Health Fragment", "Health Fragment", "Health Fragment"]],
            [["Central Luma TP", "Clean Water", "Bash", "Regenerate", "Health Fragment", "Health Fragment",
              "Health Fragment"]],
            [["Luma Boss TP", "Clean Water", "Water Dash", "Water Breath", "Bash", "Regenerate", "Health Fragment",
              "Health Fragment", "Health Fragment"]],
            [["Feeding Grounds TP", "Double Jump", "Grapple", "Regenerate", "Health Fragment", "Health Fragment",
              "Health Fragment", "Health Fragment",
              "Health Fragment"],
             ["Feeding Grounds TP", "Double Jump", "Burrow", "Regenerate", "Health Fragment", "Health Fragment",
              "Health Fragment", "Health Fragment",
              "Health Fragment"]],
            [["Central Wastes TP", "Burrow", "Regenerate", "Health Fragment", "Health Fragment", "Health Fragment",
              "Health Fragment", "Health Fragment"]],
            [["Outer Ruins TP", "Burrow", "Regenerate", "Health Fragment", "Health Fragment", "Health Fragment",
              "Health Fragment", "Health Fragment"]],
            [["Inner Ruins TP", "Burrow", "Double Jump", "Dash", "Grapple", "Regenerate", "Health Fragment",
              "Health Fragment", "Health Fragment",
              "Health Fragment", "Health Fragment"],
             ["Inner Ruins TP", "Burrow", "Glide", "Dash", "Grapple", "Regenerate", "Health Fragment",
              "Health Fragment", "Health Fragment", "Health Fragment", "Health Fragment"],
             ["Inner Ruins TP", "Burrow", "Double Jump", "Glide", "Grapple", "Regenerate", "Health Fragment",
              "Health Fragment", "Health Fragment", "Health Fragment", "Health Fragment"]],
            [["Willow's End TP", "Grapple", "Launch", "Glide", "Regenerate", "Health Fragment",
              "Health Fragment", "Health Fragment", "Health Fragment", "Health Fragment", "Health Fragment",
              "Health Fragment"]],
            ]

    gorlek: list[list[list[str]]] = [
              [["Inkwater Marsh TP"]],
              [["Midnight Burrows TP", "Bash", "Double Jump"],
               ["Midnight Burrows TP", "Bash", "Dash"],
               ["Midnight Burrows TP", "Bash", "Glide"],
               ["Midnight Burrows TP", "Bash", "Hammer"],
               ["Midnight Burrows TP", "Bash", "Sword"]],
              [["Howl's Den TP", "Double Jump"],
               ["Howl's Den TP", "Bash", "Grenade", "Sword"],
               ["Howl's Den TP", "Hammer"]],
              [["Kwolok's Hollow TP", "Sword", "Double Jump", "Bash", "Regenerate", "Health Fragment",
                "Health Fragment"],
               ["Kwolok's Hollow TP", "Hammer", "Double Jump", "Bash", "Regenerate", "Health Fragment",
                "Health Fragment"]],
              [["Glades TP", "Double Jump", "Dash", "Bash"],
               ["Glades TP", "Clean Water", "Water Dash"],
               ["Glades TP", "Clean Water", "Double Jump"],
               ["Glades TP", "Hammer"]],
              [["Wellspring TP"]],
              [["Woods Entrance TP", "Regenerate"]],
              [["Woods Exit TP", "Double Jump", "Grapple", "Glide", "Regenerate"],
               ["Woods Exit TP", "Dash", "Grapple", "Glide", "Regenerate"]],
              [["Baur's Reach TP", "Flap", "Double Jump", "Bash", "Grenade", "Regenerate"]],
              [["Mouldwood Depths TP", "Glide", "Regenerate"]],
              [["Central Luma TP", "Clean Water", "Bash", "Regenerate"]],
              [["Luma Boss TP", "Clean Water", "Water Dash", "Bash", "Regenerate"]],
              [["Feeding Grounds TP", "Double Jump", "Grapple", "Regenerate"],
               ["Feeding Grounds TP", "Double Jump", "Burrow", "Regenerate"],
               ["Feeding Grounds TP", "Double Jump", "Triple Jump", "Regenerate"],
               ["Feeding Grounds TP", "Dash", "Grapple", "Regenerate"]],
              [["Central Wastes TP", "Burrow", "Regenerate"]],
              [["Outer Ruins TP", "Burrow", "Regenerate"]],
              [["Inner Ruins TP", "Burrow", "Double Jump", "Sword", "Grapple", "Regenerate"],
               ["Inner Ruins TP", "Burrow", "Glide", "Sword", "Grapple", "Regenerate"],
               ["Inner Ruins TP", "Burrow", "Double Jump", "Hammer", "Grapple", "Regenerate"],
               ["Inner Ruins TP", "Burrow", "Glide", "Hammer", "Grapple", "Regenerate"]],
              [["Willow's End TP", "Launch", "Grapple", "Glide", "Regenerate"]],
              ]

    kii: list[list[list[str]]] = [
           [["Inkwater Marsh TP"]],
           [["Midnight Burrows TP", "Bash"]],
           [["Howl's Den TP", "Double Jump"],
            ["Howl's Den TP", "Sword", "Flash"],
            ["Howl's Den TP", "Sword", "Sentry"]],
           [["Kwolok's Hollow TP", "Bash"],
            ["Kwolok's Hollow TP", "Sword", "Grapple", "Double Jump", "Regenerate", "Health Fragment",
             "Health Fragment"],
            ["Kwolok's Hollow TP", "Hammer", "Grapple", "Double Jump", "Regenerate", "Health Fragment",
             "Health Fragment"]],
           [["Glades TP", "Sword", "Bash"],
            ["Glades TP", "Clean Water", "Double Jump"],
            ["Glades TP", "Hammer"]],
           [["Wellspring TP"]],
           [["Woods Entrance TP", "Regenerate"]],
           [["Woods Exit TP", "Double Jump", "Grapple", "Glide", "Regenerate"],
            ["Woods Exit TP", "Dash", "Grapple", "Glide", "Regenerate"],
            ["Woods Exit TP", "Dash", "Double Jump", "Regenerate"]],
           [["Baur's Reach TP", "Flap", "Double Jump", "Grenade", "Regenerate"],
            ["Baur's Reach TP", "Flap", "Bash", "Grenade", "Regenerate"]],
           [["Mouldwood Depths TP", "Glide", "Regenerate"]],
           [["Central Luma TP", "Clean Water", "Regenerate"]],
           [["Luma Boss TP", "Clean Water", "Water Dash", "Bash", "Regenerate"]],
           [["Feeding Grounds TP", "Hammer", "Grapple", "Regenerate"],
            ["Feeding Grounds TP", "Double Jump", "Sword", "Regenerate"],
            ["Feeding Grounds TP", "Double Jump", "Triple Jump", "Regenerate"],
            ["Feeding Grounds TP", "Dash", "Grapple", "Regenerate"]],
           [["Central Wastes TP", "Burrow", "Regenerate"]],
           [["Outer Ruins TP", "Burrow", "Regenerate"]],
           [["Inner Ruins TP", "Burrow", "Double Jump", "Dash", "Regenerate"],
            ["Inner Ruins TP", "Burrow", "Glide", "Grapple", "Regenerate"],
            ["Inner Ruins TP", "Burrow", "Hammer", "Dash", "Regenerate"],
            ["Inner Ruins TP", "Burrow", "Double Jump", "Grapple", "Regenerate"]],
           [["Willow's End TP", "Launch", "Double Jump", "Regenerate"]],
           ]

    unsafe: list[list[list[str]]] = [
              [["Inkwater Marsh TP"]],
              [["Midnight Burrows TP", "Bash"]],
              [["Howl's Den TP", "Double Jump"],
               ["Howl's Den TP", "Sword"]],
              [["Kwolok's Hollow TP", "Bash"],
               ["Kwolok's Hollow TP", "Sword", "Grapple", "Double Jump"],
               ["Kwolok's Hollow TP", "Hammer", "Double Jump"]],
              [["Glades TP", "Sword", "Bash"],
               ["Glades TP", "Clean Water"],
               ["Glades TP", "Hammer"]],
              [["Wellspring TP"]],
              [["Woods Entrance TP"]],
              [["Woods Exit TP", "Grapple", "Glide"],
               ["Woods Exit TP", "Grapple", "Glide"],
               ["Woods Exit TP", "Dash", "Double Jump"]],
              [["Baur's Reach TP", "Flap", "Double Jump", "Grenade"],
               ["Baur's Reach TP", "Flap", "Bash", "Grenade"]],
              [["Mouldwood Depths TP", "Glide"]],
              [["Central Luma TP", "Clean Water"]],
              [["Luma Boss TP", "Clean Water", "Water Dash"]],
              [["Feeding Grounds TP", "Hammer", "Grapple"],
               ["Feeding Grounds TP", "Double Jump"],
               ["Feeding Grounds TP", "Dash", "Grapple"],
               ["Feeding Grounds TP", "Sword", "Burrow"]],
              [["Central Wastes TP", "Burrow"]],
              [["Outer Ruins TP", "Burrow"]],
              [["Inner Ruins TP", "Burrow", "Double Jump", "Dash"],
               ["Inner Ruins TP", "Burrow", "Glide", "Grapple"],
               ["Inner Ruins TP", "Burrow", "Hammer", "Dash"],
               ["Inner Ruins TP", "Burrow", "Double Jump", "Grapple"]],
              [["Willow's End TP", "Launch"]],
              ]

    if difficulty == 0:
        sets = moki[spawn]
    elif difficulty == 1 or difficulty == 2:
        sets = gorlek[spawn]
    elif difficulty == 3 or difficulty == 4:
        sets = kii[spawn]
    else:
        sets = unsafe[spawn]
    i = world.random.randrange(len(sets))
    return sets[i]


def early_items(world: "WotWWorld", spawn: int) -> tuple[list[str], int]:
    """Return a list of items to put on sphere 1, and the amount of keystones to put on sphere 1."""
    item_list: list[list[list[str]]] = [
        [[]],  # Marsh
        [["Hammer"],  # Burrows
         ["Sword"]],
        [[]],  # Howl's Den
        [[]],  # Hollow
        [["Grapple"]],  # Glades
        [["Grapple", "Glide"],  # Wellspring
         ["Grapple", "Double Jump"],
         ["Grapple", "Dash"],
         ["Grapple", "Clean Water"]],
        [["Clean Water", "Bash"],  # Woods entrance
         ["Double Jump"],
         ["Glide"],
         ["Dash"]],
        [["Burrow"]],  # Woods exit
        [[]],  # Reach
        [["Flash"]],  # Depths
        [["Water Dash"]],  # Central Luma
        [["Sword"],  # Luma Boss
         ["Hammer"]],
        [["Burrow", "Glide"]],  # Feeding grounds
        [["Keystone", "Keystone", "Bash"],  # Central wastes
         ["Keystone", "Keystone", "Double Jump"]],
        [["Keystone", "Keystone", "Double Jump"]],  # Outer ruins
        [["Keystone", "Keystone"]],  # Inner ruins
        [["Bash", "Glide"],  # Willow
         ["Bash", "Double Jump"],
         ["Bash", "Dash"]],
    ]

    early_keystones: dict[int, int] = {
        StartingLocation.option_marsh: 2,
        StartingLocation.option_burrows: 0,
        StartingLocation.option_howlsden: 2,
        StartingLocation.option_hollow: 0,
        StartingLocation.option_glades: 0,
        StartingLocation.option_wellspring: 0,
        StartingLocation.option_westwoods: 2,
        StartingLocation.option_eastwoods: 0,
        StartingLocation.option_reach: 0,
        StartingLocation.option_depths: 2,
        StartingLocation.option_eastpools: 0,
        StartingLocation.option_westpools: 0,
        StartingLocation.option_westwastes: 0,
        StartingLocation.option_eastwastes: 2,
        StartingLocation.option_outerruins: 2,
        StartingLocation.option_innerruins: 2,
        StartingLocation.option_willow: 0,
    }

    i = world.random.randrange(len(item_list[spawn]))
    return item_list[spawn][i], early_keystones[spawn]
