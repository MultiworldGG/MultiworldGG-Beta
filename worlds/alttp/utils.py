from argparse import Namespace
from Utils import get_adjuster_settings_no_defaults

def get_default_adjuster_settings(game_name: str) -> Namespace:
    from worlds.alttp import Adjuster
    adjuster_settings = Namespace()
    if game_name == Adjuster.GAME_ALTTP:
        return Adjuster.get_argparser().parse_known_args(args=[])[0]

    return adjuster_settings

def get_adjuster_settings(game_name: str) -> Namespace:
    adjuster_settings = get_adjuster_settings_no_defaults(game_name)
    default_settings = get_default_adjuster_settings(game_name)

    # Fill in any arguments from the argparser that we haven't seen before
    return Namespace(**vars(adjuster_settings), **{
        k: v for k, v in vars(default_settings).items() if k not in vars(adjuster_settings)
    }) 