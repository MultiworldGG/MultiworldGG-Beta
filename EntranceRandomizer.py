#!/usr/bin/env python3
import argparse
import copy
import textwrap
import shlex

"""Legacy module, undergoing dismantling."""


class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)


def parse_arguments(argv, no_defaults=False):
    def defval(value):
        return value if not no_defaults else None

    # we need to know how many players we have first
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--multi', default=defval(1), type=lambda value: max(int(value), 1))
    multiargs, _ = parser.parse_known_args(argv)

    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--count', help='''\
                             Use to batch generate multiple seeds with same settings.
                             If --seed is provided, it will be used for the first seed, then
                             used to derive the next seed (i.e. generating 10 seeds with
                             --seed given will produce the same 10 (different) roms each
                             time).
                             ''', type=int)

    parser.add_argument('--multi', default=defval(1), type=lambda value: max(int(value), 1))
    parser.add_argument('--names', default=defval(''))
    parser.add_argument('--outputpath')
    parser.add_argument('--game', default="Archipelago")
    parser.add_argument('--race', default=defval(False), action='store_true')
    parser.add_argument('--outputname')
    if multiargs.multi:
        for player in range(1, multiargs.multi + 1):
            parser.add_argument(f'--p{player}', default=defval(''), help=argparse.SUPPRESS)

    ret = parser.parse_args(argv)

    # cannot be set through CLI currently

    if multiargs.multi:
        defaults = copy.deepcopy(ret)
        for player in range(1, multiargs.multi + 1):
            playerargs = parse_arguments(shlex.split(getattr(ret, f"p{player}")), True)

            for name in ["game"]:
                value = getattr(defaults, name) if getattr(playerargs, name) is None else getattr(playerargs, name)
                if player == 1:
                    setattr(ret, name, {1: value})
                else:
                    getattr(ret, name)[player] = value

    return ret
