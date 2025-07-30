from argparse import Namespace
from Utils import persistent_load


def get_shuffle_ganon(world, player):
    """Helper function to get shuffle_ganon value regardless of whether world is MultiWorld or ALTTPWorld."""
    # If world has 'worlds' attribute, it's MultiWorld, else it's per-player World
    if hasattr(world, "worlds") and hasattr(world.worlds, "__getitem__"):
        return world.worlds[player].shuffle_ganon
    # Otherwise, assume it's a per-player world instance
    return world.shuffle_ganon


def get_default_adjuster_settings(game_name: str) -> Namespace:
    from worlds.alttp import Adjuster
    adjuster_settings = Namespace()
    if game_name == Adjuster.GAME_ALTTP:
        return Adjuster.get_argparser().parse_known_args(args=[])[0]

    return adjuster_settings


def get_adjuster_settings_no_defaults(game_name: str) -> Namespace:
    return persistent_load().get("adjuster", {}).get(game_name, Namespace())


def get_adjuster_settings(game_name: str) -> Namespace:
    adjuster_settings = get_adjuster_settings_no_defaults(game_name)
    default_settings = get_default_adjuster_settings(game_name)

    # Fill in any arguments from the argparser that we haven't seen before
    return Namespace(**vars(adjuster_settings), **{
        k: v for k, v in vars(default_settings).items() if k not in vars(adjuster_settings)
    }) 