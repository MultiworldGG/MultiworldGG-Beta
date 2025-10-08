from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from . import MadouWorld


def setup_options_from_slot_data(world: "MadouWorld"):
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if "Madou Monogatari Hanamaru Daiyouchienji" in world.multiworld.re_gen_passthrough:
            world.passthrough = world.multiworld.re_gen_passthrough["Madou Monogatari Hanamaru Daiyouchienji"]

            world.seed = world.passthrough["ut_seed"]
        else:
            world.using_ut = False
    else:
        world.using_ut = False
