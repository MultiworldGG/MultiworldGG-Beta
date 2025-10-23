from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from . import MadouWorld


def setup_options_from_slot_data(world: "MadouWorld"):
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if "Madou Monogatari Hanamaru Daiyouchienji" in world.multiworld.re_gen_passthrough:
            world.passthrough = world.multiworld.re_gen_passthrough["Madou Monogatari Hanamaru Daiyouchienji"]

            world.seed = world.passthrough["ut_seed"]
            world.options.goal.value = world.passthrough["goal"]
            world.options.required_secret_stones.value = world.passthrough["required_secret_stones"]
            world.options.school_lunch.value = world.passthrough["school_lunch"]
            world.options.starting_magic.value = world.passthrough["starting_magic"]
            world.options.souvenir_hunt.value = world.passthrough["souvenir_hunt"]
            world.options.squirrel_stations.value = world.passthrough["squirrel_stations"]
            world.options.bestiary.value = world.passthrough["bestiary"]
            world.options.skip_fairy_search.value = world.passthrough["skip_fairy_search"]
        else:
            world.using_ut = False
    else:
        world.using_ut = False
