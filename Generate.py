from __future__ import annotations

import argparse
import copy
import json
import logging
import os
import random
import string
import sys
import urllib.parse
import urllib.request
from collections import Counter
from itertools import chain
from typing import Any

# Lightweight "dump option metadata as JSON" mode, used by mwgg-gui's YAML
# creator. Detected as early as possible — before ModuleUpdate configures the
# root logger to stdout — because the GUI captures a single JSON object from
# stdout, so every other byte of output must be diverted to stderr. The real
# stdout is preserved in _JSON_OUT for the final emit.
_YAML_OPTIONS_MODE = "--yaml-options" in sys.argv or "--yaml_options" in sys.argv
_JSON_OUT = sys.stdout
if _YAML_OPTIONS_MODE:
    logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
    sys.stdout = sys.stderr

import ModuleUpdate

import Utils

if Utils.use_worlds_venv():
    venv_site_packages_path = Utils.mwgg_venv_site_packages()
    if venv_site_packages_path not in sys.path:
        sys.path.append(venv_site_packages_path)
    venv_worlds_path = Utils.mwgg_venv_site_packages("worlds")
    if os.path.exists(venv_worlds_path) and venv_worlds_path not in sys.path:
        sys.path.append(venv_worlds_path)

# Hard-require mwgg_igdb: subsequent imports (and BaseUtils.get_archipelago_constants)
# crash with ImportError if the index isn't installed. Mirrors WebHost.py's pattern.
ModuleUpdate.update()

import Options
from BaseClasses import seeddigits, get_seed, PlandoOptions
from Utils import parse_yamls, version_tuple, __version__, tuplize_version, set_game_names
from mwgg_igdb import GameIndex

class _HyphenUnderscoreArgumentParser(argparse.ArgumentParser):
    """Accepts both the hyphen and underscore form of any multi-word long option,
    so e.g. --player-files-path and --player_files_path both parse. The hyphen form
    stays canonical (first option string) for help text and dest derivation."""

    def add_argument(self, *names: str, **kwargs):
        aliased = list(names)
        for name in names:
            if name.startswith("--") and "-" in name[2:]:
                underscored = "--" + name[2:].replace("-", "_")
                if underscored not in aliased:
                    aliased.append(underscored)
        return super().add_argument(*aliased, **kwargs)


def mystery_argparse(argv: list[str] | None = None) -> argparse.Namespace:
    from settings import get_settings
    settings = get_settings()
    defaults = settings.generator

    parser = _HyphenUnderscoreArgumentParser(description="CMD Generation Interface, defaults come from host.yaml.")
    parser.add_argument('--weights-file-path', default=defaults.weights_file_path,
                        help='Path to the weights file to use for rolling game options, urls are also valid')
    parser.add_argument('--sameoptions', help='Rolls options per weights file rather than per player',
                        action='store_true')
    parser.add_argument('--player-files-path', default=defaults.player_files_path,
                        help="Input directory for player files.")
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--multi', default=defaults.players, type=lambda value: max(int(value), 1))
    parser.add_argument('--spoiler', type=int, default=defaults.spoiler)
    parser.add_argument('--outputpath', default=settings.general_options.output_path,
                        help="Path to output folder. Absolute or relative to cwd.")
    parser.add_argument('--outputname', help="Name for the output files.")
    parser.add_argument('--allow-quantity', action="store_true", default=defaults.allow_quantity,
                        help='Allows the use of the quantity option in yamls. Default is the set value in the host.yaml.')
    parser.add_argument('--race', action='store_true', default=defaults.race)
    parser.add_argument('--meta-file-path', default=defaults.meta_file_path)
    parser.add_argument('--log-level', default=defaults.loglevel, help='Sets log level')
    parser.add_argument('--log-time', help="Add timestamps to STDOUT",
                        default=defaults.logtime, action='store_true')
    parser.add_argument("--csv-output", action="store_true",
                        help="Output rolled player options to csv (made for async multiworld).")
    parser.add_argument("--plando", default=defaults.plando_options,
                        help="List of options that can be set manually. Can be combined, for example \"bosses, items\"")
    parser.add_argument("--skip-prog-balancing", action="store_true",
                        help="Skip progression balancing step during generation.")
    parser.add_argument("--skip-output", action="store_true",
                        help="Skips generation assertion and output stages and skips multidata and spoiler output. "
                             "Intended for debugging and testing purposes.")
    parser.add_argument("--spoiler-only", action="store_true",
                        help="Skips generation assertion and multidata, outputting only a spoiler log. "
                             "Intended for debugging and testing purposes.")
    parser.add_argument("--game", dest="yaml_options_game",
                        help="Game name, used by --yaml-options.")
    parser.add_argument("--module", help="World module slug for --yaml-options. Lets custom (non-pip) worlds "
                                         "load without a game-index lookup; falls back to the index when omitted.")
    parser.add_argument("--yaml-options", action="store_true",
                        help="Install/load --game, write its option metadata to stdout as JSON, then exit. "
                             "Used by the YAML creator GUI; no seed is generated.")
    parser.add_argument("--visibility", choices=("simple", "complex"), default="simple",
                        help="Option visibility level for --yaml-options.")
    args = parser.parse_args(argv)

    if args.yaml_options and not args.yaml_options_game:
        parser.error("--yaml-options requires --game")

    if args.skip_output and args.spoiler_only:
        parser.error("Cannot mix --skip-output and --spoiler-only")
    elif args.spoiler == 0 and args.spoiler_only:
        parser.error("Cannot use --spoiler-only when --spoiler=0. Use --skip-output or set --spoiler to a different value")

    if not os.path.isabs(args.weights_file_path):
        args.weights_file_path = os.path.join(args.player_files_path, args.weights_file_path)
    if not os.path.isabs(args.meta_file_path):
        args.meta_file_path = os.path.join(args.player_files_path, args.meta_file_path)
    args.plando = PlandoOptions.from_option_string(args.plando)

    return args


def get_seed_name(random_source) -> str:
    return f"{random_source.randint(0, pow(10, seeddigits) - 1)}".zfill(seeddigits)


def _installed_worlds_count() -> int:
    """Number of pip-installed `worlds*` distributions, read from dist metadata only so it
    never imports the `worlds` package (which would prematurely run its one-shot load loop).
    A jump across set_game_names means a world was installed mid-run."""
    import importlib.metadata
    return sum(1 for dist in importlib.metadata.distributions()
               if (dist.name or "").startswith("worlds"))


def _reexec_for_clean_world_load() -> int:
    """Re-run this generator in a fresh process and return its exit code.

    set_game_names imports the `worlds` package (via find_spec) while probing for
    worlds that aren't installed yet, so this process's one-shot world load loop runs
    before the freshly-installed worlds are queued and can never load them. They are
    on disk now, so a clean process loads them on its first `import worlds`. Stdio is
    inherited so output keeps streaming to the caller; the MWGG_GENERATE_RELOADED env
    guard prevents a reload loop. Frozen cx_Freeze argv[0] is the exe (== sys.executable),
    so drop it; a script run keeps argv[0] (the .py path).
    """
    import subprocess
    env = dict(os.environ)
    env["MWGG_GENERATE_RELOADED"] = "1"
    cmd = [sys.executable, *(sys.argv[1:] if ModuleUpdate.is_frozen() else sys.argv)]
    logging.info("Worlds were installed mid-run; reloading in a fresh process to load them cleanly.")
    for handler in logging.root.handlers:
        handler.flush()
    return subprocess.run(cmd, env=env).returncode


def main(args=None) -> tuple[argparse.Namespace, int]:
    # __name__ == "__main__" check so unittests that already imported worlds don't trip this.
    if __name__ == "__main__" and "worlds" in sys.modules:
        raise Exception("Worlds system should not be loaded before logging init.")

    if not args:
        args = mystery_argparse()

    seed = get_seed(args.seed)

    if __name__ == "__main__":
        Utils.init_logging(f"Generate_{seed}", loglevel=args.log_level, add_timestamp=args.log_time, show_logo=True)
    random.seed(seed)
    seed_name = get_seed_name(random)

    if args.race:
        logging.info("Race mode enabled. Using non-deterministic random source.")
        random.seed()  # reset to time-based random source

    weights_cache: dict[str, tuple[Any, ...]] = {}
    if args.weights_file_path and os.path.exists(args.weights_file_path):
        try:
            weights_cache[args.weights_file_path] = read_weights_yamls(args.weights_file_path)
        except Exception as e:
            raise ValueError(f"File {args.weights_file_path} is invalid. Please fix your yaml.") from e
        logging.info(f"Weights: {args.weights_file_path} >> "
                     f"{get_choice('description', weights_cache[args.weights_file_path][-1], 'No description specified')}")

    if args.meta_file_path and os.path.exists(args.meta_file_path):
        try:
            meta_weights = read_weights_yamls(args.meta_file_path)[-1]
        except Exception as e:
            raise ValueError(f"File {args.meta_file_path} is invalid. Please fix your yaml.") from e
        logging.info(f"Meta: {args.meta_file_path} >> {get_choice('meta_description', meta_weights)}")
        try:  # meta description allows us to verify that the file named meta.yaml is intentionally a meta file
            del(meta_weights["meta_description"])
        except Exception as e:
            raise ValueError("No meta description found for meta.yaml. Unable to verify.") from e
        if args.sameoptions:
            raise Exception("Cannot mix --sameoptions with --meta")
    else:
        meta_weights = None

    player_id: int = 1
    player_files: dict[int, str] = {}
    player_errors: list[str] = []
    allow_quantity: bool = args.allow_quantity or False
    # Create the player-files dir on demand (PlayerFilesPath is an optional
    # folder) and skip documentation/non-config files so a stray README.txt
    # can't break the whole scan.
    os.makedirs(args.player_files_path, exist_ok=True)
    _non_player_suffixes = (".ini", ".txt", ".md")
    for file in os.scandir(args.player_files_path):
        fname = file.name
        if file.is_file() and not fname.startswith(".") and not fname.lower().endswith(_non_player_suffixes) and \
                os.path.join(args.player_files_path, fname) not in {args.meta_file_path, args.weights_file_path}:
            path = os.path.join(args.player_files_path, fname)
            try:
                weights_for_file = []
                for doc_idx, yaml in enumerate(read_weights_yamls(path)):
                    if yaml is None:
                        logging.warning(f"Ignoring empty yaml document #{doc_idx + 1} in {fname}")
                    else:
                        quantity = yaml.get("quantity", 1)
                        if quantity <= 0:
                            raise ValueError("A quantity of 0 or less is invalid. Please change it to at least 1.")
                        if not allow_quantity and quantity > 1:
                            raise ValueError("Quantity greater than 1 is deactivated by host settings.")

                        for _ in range(quantity):
                            weights_for_file.append(yaml)
                weights_cache[fname] = tuple(weights_for_file)

            except Exception as e:
                logging.exception(f"Exception reading weights in file {fname}")
                player_errors.append(
                    f"{len(player_errors) + 1}. "
                    f"File {fname} is invalid. Please fix your yaml.\n{Utils.get_all_causes(e)}"
                )

    # sort dict for consistent results across platforms:
    weights_cache = {key: value for key, value in sorted(weights_cache.items(), key=lambda k: k[0].casefold())}
    for filename, yaml_data in weights_cache.items():
        if filename not in {args.meta_file_path, args.weights_file_path}:
            for yaml in yaml_data:
                logging.info(f"P{player_id} Weights: {filename} >> "
                             f"{get_choice('description', yaml, 'No description specified')}")
                player_files[player_id] = filename
                player_id += 1

    args.multi = max(player_id - 1, args.multi)

    if args.multi == 0:
        if player_errors:
            errors = "\n\n".join(player_errors)
            raise ValueError(f"Encountered {len(player_errors)} error(s) in player files. "
                             f"See logs for full tracebacks.\n\n{errors}")
        raise ValueError(
            "No individual player files found and number of players is 0. "
            "Provide individual player files or specify the number of players via host.yaml or --multi."
        )

    logging.info(f"Generating for {args.multi} player{'s' if args.multi > 1 else ''}, "
                 f"{seed_name} Seed {seed} with plando: {args.plando}")

    if not weights_cache:
        if player_errors:
            errors = "\n\n".join(player_errors)
            raise ValueError(f"Encountered {len(player_errors)} error(s) in player files. "
                             f"See logs for full tracebacks.\n\n{errors}")
        raise Exception(f"No weights found. "
                        f"Provide a general weights file ({args.weights_file_path}) or individual player files. "
                        f"A mix is also permitted.")

    games_to_load = []
    for player_path, yaml in weights_cache.items():
        game_name = yaml[0]['game']
        games_to_load.append(game_name)
        # If YAML has explicit module field, add to game index
        if 'module' in yaml[0]:
            module_name = yaml[0]['module']
            game_module = module_name.replace("worlds.", "")
            logging.info(f"Adding custom module to game index: {game_module} -> {game_name}")
            GameIndex.add_game(game_module, {"game_name": game_name})

    worlds_installed_before = _installed_worlds_count()
    set_game_names(games_to_load)
    if (__name__ == "__main__" and not os.environ.get("MWGG_GENERATE_RELOADED")
            and _installed_worlds_count() > worlds_installed_before):
        # set_game_names pip-installed a world that wasn't present yet, but its find_spec
        # probe imported `worlds` before the new world was queued, so this process's
        # one-shot load loop missed it and roll_settings can't find it. It's installed
        # now — hand off to a fresh process that loads it cleanly, silently retrying
        # instead of erroring out. (Worlds already on disk never reach here, so dev runs
        # and post-install retries proceed in-process unchanged.)
        import atexit
        atexit.unregister(input)  # this proxy process must not prompt "Press enter to close."
        sys.exit(_reexec_for_clean_world_load())
    from worlds.AutoWorld import AutoWorldRegister
    """ Load worlds *after* setting the game names
    """
    args.outputname = seed_name
    args.name = {}

    if meta_weights:
        for category_name, category_dict in meta_weights.items():
            for key in category_dict:
                option = roll_meta_option(key, category_name, category_dict)
                if option is not None:
                    for path in weights_cache:
                        for yaml in weights_cache[path]:
                            if category_name is None:
                                for category in yaml:
                                    if category in AutoWorldRegister.world_types and \
                                            key in Options.CommonOptions.type_hints:
                                        yaml[category][key] = option
                            elif category_name not in yaml:
                                logging.warning(f"Meta: Category {category_name} is not present in {path}.")
                            elif key == "triggers":
                                if "triggers" not in yaml[category_name]:
                                    yaml[category_name][key] = []
                                for trigger in option:
                                    yaml[category_name][key].append(trigger)
                            else:
                                yaml[category_name][key] = option

    settings_cache: dict[str, tuple[argparse.Namespace, ...] | None] = {fname: None for fname in weights_cache}
    if args.sameoptions:
        for fname, yamls in weights_cache.items():
            try:
                settings_cache[fname] = tuple(roll_settings(yaml, args.plando) for yaml in yamls)
            except Exception as e:
                logging.exception(f"Exception reading settings in file {fname}")
                player_errors.append(
                    f"{len(player_errors) + 1}. "
                    f"File {fname} is invalid. Please fix your yaml.\n{Utils.get_all_causes(e)}"
                )
        # Exit early here to avoid throwing the same errors again later
        if player_errors:
            errors = "\n\n".join(player_errors)
            raise ValueError(f"Encountered {len(player_errors)} error(s) in player files. "
                             f"See logs for full tracebacks.\n\n{errors}")

    player_path_cache: dict[int, str] = {}
    for player in range(1, args.multi + 1):
        player_path_cache[player] = player_files.get(player, args.weights_file_path)
    name_counter: Counter[str] = Counter()
    args.player_options = {}

    player = 1
    while player <= args.multi:
        path = player_path_cache[player]
        if not path:
            player_errors.append(f'No weights specified for player {player}')
            player += 1
            continue

        for doc_index, yaml in enumerate(weights_cache[path]):
            name = yaml.get("name")
            try:
                # Use the cached settings object if it exists, otherwise roll settings within the try-catch
                # Invariant: settings_cache[path] and weights_cache[path] have the same length
                cached = settings_cache[path]
                settings_object: argparse.Namespace = (cached[doc_index] if cached else roll_settings(yaml, args.plando))

                for k, v in vars(settings_object).items():
                    if v is not None:
                        try:
                            getattr(args, k)[player] = v
                        except AttributeError:
                            setattr(args, k, {player: v})
                        except Exception as e:
                            raise Exception(f"Error setting {k} to {v} for player {player}") from e

                # name was not specified
                if player not in args.name:
                    if path == args.weights_file_path:
                        # weights file, so we need to make the name unique
                        args.name[player] = f"Player{player}"
                    else:
                        # use the filename
                        args.name[player] = os.path.splitext(os.path.split(path)[-1])[0]
                args.name[player] = handle_name(args.name[player], player, name_counter)

            except Exception as e:
                logging.exception(f"Exception reading settings in file {path} document #{doc_index + 1} "
                                  f"(name: {args.name.get(player, name)})")
                player_errors.append(
                    f"{len(player_errors) + 1}. "
                    f"File {path} document #{doc_index + 1} (name: {args.name.get(player, name)}) is invalid. "
                    f"Please fix your yaml.\n{Utils.get_all_causes(e)}")

            # increment for each yaml document in the file
            player += 1

    if len(set(name.lower() for name in args.name.values())) != len(args.name):
        player_errors.append(
            f"{len(player_errors) + 1}. "
            f"Names have to be unique. Names: {Counter(name.lower() for name in args.name.values())}"
        )

    if player_errors:
        errors = "\n\n".join(player_errors)
        raise ValueError(f"Encountered {len(player_errors)} error(s) in player files. "
                         f"See logs for full tracebacks.\n\n{errors}")

    return args, seed


def read_weights_yamls(path) -> tuple[Any, ...]:
    try:
        if urllib.parse.urlparse(path).scheme in ('https', 'file'):
            yaml = str(urllib.request.urlopen(path).read(), "utf-8-sig")
        else:
            with open(path, 'rb') as f:
                yaml = str(f.read(), "utf-8-sig")
    except Exception as e:
        raise Exception(f"Failed to read weights ({path})") from e

    from yaml.error import MarkedYAMLError
    try:
        return tuple(parse_yamls(yaml))
    except MarkedYAMLError as ex:
        if ex.problem_mark:
            lines = yaml.splitlines()
            if ex.context_mark:
                relevant_lines = "\n".join(lines[ex.context_mark.line:ex.problem_mark.line+1])
            else:
                relevant_lines = lines[ex.problem_mark.line]
            error_line = " " * ex.problem_mark.column + "^"
            raise Exception(f"{ex.context} {ex.problem} on line {ex.problem_mark.line}:"
                            f"\n{relevant_lines}\n{error_line}")
        raise ex


def interpret_on_off(value) -> bool:
    return {"on": True, "off": False}.get(value, value)


def convert_to_on_off(value) -> str:
    return {True: "on", False: "off"}.get(value, value)


def get_choice_legacy(option, root, value=None) -> Any:
    if option not in root:
        return value
    if type(root[option]) is list:
        return interpret_on_off(random.choices(root[option])[0])
    if type(root[option]) is not dict:
        return interpret_on_off(root[option])
    if not root[option]:
        return value
    if any(root[option].values()):
        return interpret_on_off(
            random.choices(list(root[option].keys()), weights=list(map(int, root[option].values())))[0])
    raise RuntimeError(f"All options specified in \"{option}\" are weighted as zero.")


def get_choice(option, root, value=None) -> Any:
    if option not in root:
        return value
    if type(root[option]) is list:
        return random.choices(root[option])[0]
    if type(root[option]) is not dict:
        return root[option]
    if not root[option]:
        return value
    if any(root[option].values()):
        return random.choices(list(root[option].keys()), weights=list(map(int, root[option].values())))[0]
    raise RuntimeError(f"All options specified in \"{option}\" are weighted as zero.")


class SafeFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        if isinstance(key, int):
            if key < len(args):
                return args[key]
            else:
                return "{" + str(key) + "}"
        else:
            return kwargs.get(key, "{" + key + "}")


def handle_name(name: str, player: int, name_counter: Counter[str]):
    name_counter[name.lower()] += 1
    number = name_counter[name.lower()]
    new_name = "%".join([x.replace("%number%", "{number}").replace("%player%", "{player}") for x in name.split("%%")])

    new_name = SafeFormatter().vformat(new_name, (), {"number": number,
                                                      "NUMBER": (number if number > 1 else ''),
                                                      "player": player,
                                                      "PLAYER": (player if player > 1 else '')})
    new_name = new_name.strip()[:16].strip()

    if new_name == "Archipelago" or new_name == "MultiworldGG":
        raise Exception(f"You cannot name yourself \"{new_name}\"")
    return new_name


def update_weights(weights: dict, new_weights: dict, update_type: str, name: str) -> dict:
    logging.debug(f'Applying {new_weights}')
    cleaned_weights = {}
    for option in new_weights:
        option_name = option.lstrip("+-")
        if option.startswith("+") and option_name in weights:
            cleaned_value = weights[option_name]
            new_value = new_weights[option]
            if isinstance(new_value, set):
                cleaned_value.update(new_value)
            elif isinstance(new_value, list):
                cleaned_value.extend(new_value)
            elif isinstance(new_value, dict):
                counter_value = Counter(cleaned_value)
                counter_value.update(new_value)
                cleaned_value = dict(counter_value)
            else:
                raise Exception(f"Cannot apply merge to non-dict, set, or list type {option_name},"
                                f" received {type(new_value).__name__}.")
            cleaned_weights[option_name] = cleaned_value
        elif option.startswith("-") and option_name in weights:
            cleaned_value = weights[option_name]
            new_value = new_weights[option]
            if isinstance(new_value, set):
                cleaned_value.difference_update(new_value)
            elif isinstance(new_value, list):
                for element in new_value:
                    cleaned_value.remove(element)
            elif isinstance(new_value, dict):
                counter_value = Counter(cleaned_value)
                counter_value.subtract(new_value)
                cleaned_value = dict(counter_value)
            else:
                raise Exception(f"Cannot apply remove to non-dict, set, or list type {option_name},"
                                f" received {type(new_value).__name__}.")
            cleaned_weights[option_name] = cleaned_value
        else:
            cleaned_value = copy.deepcopy(new_weights[option])
            cleaned_weights[option_name] = cleaned_value
    new_options = set(cleaned_weights) - set(weights)
    weights.update(cleaned_weights)
    if new_options:
        for new_option in new_options:
            logging.warning(f'{update_type} Suboption "{new_option}" of "{name}" did not '
                            f'overwrite a root option. '
                            f'This is probably in error.')
    return weights


def roll_meta_option(option_key, game: str, category_dict: dict) -> Any:
    from worlds import AutoWorldRegister

    if not game:
        return get_choice(option_key, category_dict)
    if game in AutoWorldRegister.world_types:
        game_world = AutoWorldRegister.world_types[game]
        options = game_world.options_dataclass.type_hints
        if option_key in options:
            if options[option_key].supports_weighting:
                return get_choice(option_key, category_dict)
            return category_dict[option_key]
        if option_key == "triggers":
            return category_dict[option_key]
    raise Options.OptionError(f"Error generating meta option {option_key} for {game}.")


def roll_linked_options(weights: dict) -> dict:
    weights = copy.deepcopy(weights)  # make sure we don't write back to other weights sets in same_settings
    for option_set in weights["linked_options"]:
        if "name" not in option_set:
            raise ValueError("One of your linked options does not have a name.")
        try:
            if Options.roll_percentage(option_set["percentage"]):
                logging.debug(f"Linked option {option_set['name']} triggered.")
                new_options = option_set["options"]
                for category_name, category_options in new_options.items():
                    currently_targeted_weights = weights
                    if category_name:
                        currently_targeted_weights = currently_targeted_weights[category_name]
                    update_weights(currently_targeted_weights, category_options, "Linked", option_set["name"])
            else:
                logging.debug(f"linked option {option_set['name']} skipped.")
        except Exception as e:
            raise ValueError(f"Linked option {option_set['name']} is invalid. "
                             f"Please fix your linked option.") from e
    return weights


def roll_triggers(weights: dict, triggers: list, valid_keys: set) -> dict:
    weights = copy.deepcopy(weights)  # make sure we don't write back to other weights sets in same_settings
    weights["_Generator_Version"] = Utils.__version__
    for i, option_set in enumerate(triggers):
        try:
            currently_targeted_weights = weights
            category = option_set.get("option_category", None)
            if category:
                currently_targeted_weights = currently_targeted_weights[category]
            key = get_choice("option_name", option_set)
            if key not in currently_targeted_weights:
                logging.warning(f'Specified option name {option_set["option_name"]} did not '
                                f'match with a root option. '
                                f'This is probably in error.')
            trigger_result = get_choice("option_result", option_set)
            result = get_choice(key, currently_targeted_weights)
            currently_targeted_weights[key] = result
            if result == trigger_result and Options.roll_percentage(get_choice("percentage", option_set, 100)):
                for category_name, category_options in option_set["options"].items():
                    currently_targeted_weights = weights
                    if category_name:
                        currently_targeted_weights = currently_targeted_weights[category_name]
                    update_weights(currently_targeted_weights, category_options, "Triggered", option_set["option_name"])
            valid_keys.add(key)
        except Exception as e:
            raise ValueError(f"Your trigger number {i + 1} is invalid. "
                             f"Please fix your triggers.") from e
    return weights


def handle_option(ret: argparse.Namespace, game_weights: dict, option_key: str, option: type[Options.Option], plando_options: PlandoOptions):
    try:
        if option_key in game_weights:
            if not option.supports_weighting:
                player_option = option.from_any(game_weights[option_key])
            else:
                player_option = option.from_any(get_choice(option_key, game_weights))
        else:
            player_option = option.from_any(option.default)  # call the from_any here to support default "random"
        setattr(ret, option_key, player_option)
    except Exception as e:
        raise Options.OptionError(f"Error generating option {option_key} in {ret.game}") from e
    else:
        from worlds import AutoWorldRegister
        world_class = AutoWorldRegister.world_types[ret.game]
        if world_class is not None:
            player_option.verify(world_class, ret.name, plando_options)


def roll_settings(weights: dict, plando_options: PlandoOptions = PlandoOptions.bosses):
    """
    Roll options from specified weights, usually originating from a .yaml options file.

    Important note:
    The same weights dict is shared between all slots using the same yaml (e.g. generic weights file for filler slots).
    This means it should never be modified without making a deepcopy first.
    """

    from worlds import AutoWorldRegister

    if "linked_options" in weights:
        weights = roll_linked_options(weights)

    valid_keys = {"triggers"}
    if "triggers" in weights:
        weights = roll_triggers(weights, weights["triggers"], valid_keys)

    requirements = weights.get("requires", {})
    if requirements:
        version = requirements.get("version", __version__)
        if tuplize_version(version) > version_tuple:
            raise Exception(f"Settings reports required version of generator is at least {version}, "
                            f"however generator is of version {__version__}")
        required_plando_options = PlandoOptions.from_option_string(requirements.get("plando", ""))
        if required_plando_options not in plando_options:
            if required_plando_options:
                raise Exception(f"Settings reports required plando module {str(required_plando_options)}, "
                                f"which is not enabled.")
        games = requirements.get("game", {})
        for game, version in games.items():
            if game not in AutoWorldRegister.world_types:
                raise Exception(f"Game {game} not found in world types.")
            if not version:
                raise Exception(f"Invalid version for game {game}: {version}.")
            if isinstance(version, str):
                version = {"min": version}
            if "min" in version and tuplize_version(version["min"]) > AutoWorldRegister.world_types[game].world_version:
                raise Exception(f"Settings reports required version of world \"{game}\" is at least {version['min']}, "
                                f"however world is of version "
                                f"{AutoWorldRegister.world_types[game].world_version.as_simple_string()}.")
            if "max" in version and tuplize_version(version["max"]) < AutoWorldRegister.world_types[game].world_version:
                raise Exception(f"Settings reports required version of world \"{game}\" is no later than {version['max']}, "
                                f"however world is of version "
                                f"{AutoWorldRegister.world_types[game].world_version.as_simple_string()}.")
    ret = argparse.Namespace()
    for option_key in Options.PerGameCommonOptions.type_hints:
        if option_key in weights and option_key not in Options.CommonOptions.type_hints:
            raise Exception(f"Option {option_key} has to be in a game's section, not on its own.")

    ret.game = get_choice("game", weights)
    if not isinstance(ret.game, str):
        if ret.game is None:
            raise Exception('"game" not specified')
        raise Exception(f"Invalid game: {ret.game}")
    
    # Check if there's an explicit module field in the YAML
    if "module" in weights:
        ret.module_name = weights["module"]
        # Extract module name without "worlds." prefix
        game_module = ret.module_name.replace("worlds.", "")
        # Add basic game entry to index for separately installed worlds
        GameIndex.add_game(game_module, {"game_name": ret.game})
    else:
        ret.module_name = GameIndex.get_module_for_game(game_name=ret.game, worlds=True)

    from worlds import failed_world_loads, AutoWorldRegister
    available_worlds = Utils.get_available_worlds()
    
    world_module = sys.modules.get(ret.module_name)
    if world_module is None:
        world_class = None
        raise Exception(f"No world found to handle game {ret.game} with module {ret.module_name}. "
                        f"Check your spelling or installation of that world.")
    else:
        world_class = AutoWorldRegister.world_types.get(ret.game, None)

    if world_class is None:
        picks = Utils.get_fuzzy_results(ret.game, available_worlds + failed_world_loads, limit=1)[0]
        if picks[0] in failed_world_loads:
            raise Exception(f"No functional world found to handle game {ret.game} with module {ret.module_name}. "
                            f"Did you mean '{picks[0]}' ({picks[1]}% sure)? "
                            f"If so, it appears the world failed to initialize correctly.")
        raise Exception(f"No world found to handle game {ret.game}. Did you mean '{picks[0]}' ({picks[1]}% sure)? "
                        f"Check your spelling or installation of that world.")

    if ret.game not in weights:
        raise Exception(f"No game options for selected game \"{ret.game}\" found.")

    world_type = world_class
    game_weights = weights[ret.game]

    for weight in chain(game_weights, weights):
        if weight.startswith("+"):
            raise Exception(f"Merge tag cannot be used outside of trigger contexts. Found {weight}")
        if weight.startswith("-"):
            raise Exception(f"Remove tag cannot be used outside of trigger contexts. Found {weight}")

    if "triggers" in game_weights:
        weights = roll_triggers(weights, game_weights["triggers"], valid_keys)
        game_weights = weights[ret.game]

    ret.name = get_choice('name', weights)
    for option_key, option in Options.CommonOptions.type_hints.items():
        setattr(ret, option_key, option.from_any(get_choice(option_key, weights, option.default)))

    for option_key, option in world_type.options_dataclass.type_hints.items():
        handle_option(ret, game_weights, option_key, option, plando_options)
        valid_keys.add(option_key)

    # log a warning for options within a game section that aren't determined as valid
    for option_key in game_weights:
        if option_key in valid_keys:
            continue
        logging.warning(f"{option_key} is not a valid option name for {ret.game} and is not present in triggers "
                        f"for player {ret.name}.")

    return ret


# ---------------------------------------------------------------------------
# --yaml-options: dump a world's option metadata as JSON (for the YAML creator)
# ---------------------------------------------------------------------------

def _y_serialize_default(value):
    """Coerce option defaults into JSON-safe values."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_y_serialize_default(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _y_serialize_default(v) for k, v in value.items()}
    return str(value)


def _y_clean_docstring(text):
    if not text:
        return ""
    return " ".join(line.strip() for line in text.strip().splitlines() if line.strip())


def _y_choice_extras(option_class):
    """`choices` (key -> machine name) and `display_names` (key -> human label)."""
    lookup = dict(getattr(option_class, "name_lookup", {}) or {})
    choices, display_names = {}, {}
    for key, name in lookup.items():
        if name == "random":
            continue
        choices[str(key)] = name
        try:
            display_names[str(key)] = option_class.get_option_name(key)
        except Exception:
            display_names[str(key)] = name
    return {"choices": choices, "display_names": display_names}


def _y_range_extras(option_class):
    return {
        "range_start": int(getattr(option_class, "range_start", 0)),
        "range_end": int(getattr(option_class, "range_end", 100)),
    }


def _y_describe_option(option_name, option_class):
    """JSON-safe descriptor for one option class. Order matters: subclass first."""
    desc = {
        "name": option_name,
        "display_name": getattr(option_class, "display_name", None) or option_name,
        "docstring": _y_clean_docstring(getattr(option_class, "__doc__", "") or ""),
        "default": _y_serialize_default(getattr(option_class, "default", None)),
    }
    if issubclass(option_class, Options.Toggle):
        desc["type"] = "toggle"
        return desc
    if issubclass(option_class, Options.TextChoice):
        desc["type"] = "text_choice"
        desc.update(_y_choice_extras(option_class))
        return desc
    if issubclass(option_class, Options.Choice):
        desc["type"] = "choice"
        desc.update(_y_choice_extras(option_class))
        return desc
    if issubclass(option_class, Options.NamedRange):
        desc["type"] = "named_range"
        desc.update(_y_range_extras(option_class))
        desc["special_range_names"] = {
            str(k): int(v)
            for k, v in (getattr(option_class, "special_range_names", {}) or {}).items()
        }
        return desc
    if issubclass(option_class, Options.Range):
        desc["type"] = "range"
        desc.update(_y_range_extras(option_class))
        return desc
    if issubclass(option_class, Options.FreeText):
        desc["type"] = "free_text"
        return desc
    if issubclass(option_class, Options.ItemSet):
        desc["type"] = "item_set"
        desc["valid_keys"] = sorted(getattr(option_class, "valid_keys", []) or [])
        return desc
    if issubclass(option_class, Options.LocationSet):
        desc["type"] = "location_set"
        desc["valid_keys"] = sorted(getattr(option_class, "valid_keys", []) or [])
        return desc
    if issubclass(option_class, Options.OptionCounter):
        desc["type"] = "option_counter"
        desc["valid_keys"] = sorted(getattr(option_class, "valid_keys", []) or [])
        desc["verify_item_name"] = bool(getattr(option_class, "verify_item_name", False))
        desc["verify_location_name"] = bool(getattr(option_class, "verify_location_name", False))
        return desc
    if issubclass(option_class, (Options.OptionSet, Options.OptionList)):
        desc["type"] = "option_set"
        desc["valid_keys"] = sorted(getattr(option_class, "valid_keys", []) or [])
        return desc
    if issubclass(option_class, Options.OptionDict):
        desc["type"] = "option_dict"
        return desc
    # Unmodeled subclass — let the GUI fall back to a free-text/raw-YAML field.
    desc["type"] = "free_text"
    return desc


def _y_describe_world(world):
    return {
        "item_names": sorted(getattr(world, "item_names", []) or []),
        "location_names": sorted(getattr(world, "location_names", []) or []),
        "item_name_groups": {
            name: sorted(members or [])
            for name, members in (getattr(world, "item_name_groups", {}) or {}).items()
        },
        "location_name_groups": {
            name: sorted(members or [])
            for name, members in (getattr(world, "location_name_groups", {}) or {}).items()
        },
    }


def _y_emit(payload) -> int:
    _JSON_OUT.write(json.dumps(payload))
    _JSON_OUT.flush()
    return 0


# Exit code that asks the caller to re-run us in a fresh process. Reuses the
# project-wide "bad environment / needs reload" convention (Utils.exit_restart_
# for_update, handled by the launcher) — here it means "world installed, but it
# can't be loaded in this already-`import worlds`-ed process; re-run me".
EXIT_NEEDS_RELOAD = 10


def _y_world_installed(module: str) -> bool:
    """True if `worlds.<module>` is pip-installed, checked WITHOUT importing the
    worlds package (importlib.metadata reads dist-info only)."""
    import importlib.metadata
    try:
        importlib.metadata.distribution(f"worlds.{module}")
        return True
    except importlib.metadata.PackageNotFoundError:
        return False


def _y_custom_world_entry(module: str):
    """A `Utils._worlds_to_load` entry for an already-present *custom* world (one
    with no pip metadata), or None if `module` isn't present on disk.

    The launcher only offers worlds get_available_worlds() found on disk, so a
    selectable custom world already exists — we never install it. Two on-disk
    shapes, in load-precedence order:
      - an apworld previously extracted into the venv worlds dir -> import via
        the string "worlds.<module>" (worlds/__init__ extends __path__ to that
        dir, so the normal file loader finds it).
      - a custom_worlds/<module>.apworld not yet extracted -> an APWorldContainer,
        loaded in-process via zipimport.
    Checked WITHOUT importing `worlds` (path lookups + a zip manifest read only).
    """
    if (ModuleUpdate._venv_worlds_dir() / module).is_dir():
        return f"worlds.{module}"
    apworld_file = ModuleUpdate.custom_worlds_dir / f"{module}.apworld"
    if apworld_file.is_file():
        from APContainer import APWorldContainer
        container = APWorldContainer(apworld_file)
        container.read()  # populate .game from the manifest (for failure reporting)
        return container
    return None


def dump_yaml_options(game_name: str, visibility: str, module: str | None = None) -> int:
    """Install/load `game_name` and write its option metadata to stdout as JSON.

    Runs inside the frozen Generate executable, so worlds load in the real
    bundle environment (C-extension base deps like bsdiff4 import fine).
    Returns a process exit code; the JSON `ok` field carries success/failure.

    Two-call install (index/pip worlds): a world can't be installed and loaded
    in the same process, because importing `worlds` to load it also caches the
    package with its load loop already run against the old queue. So when an
    index world isn't yet installed we install it directly
    (ModuleUpdate.install_worlds, which never imports `worlds`) and exit
    EXIT_NEEDS_RELOAD; the caller re-runs us and the fresh process loads it
    cleanly. Already-installed worlds load in one call.

    Custom worlds (apworld extractions, custom_worlds/*.apworld) have no pip
    metadata and can't be "installed", but the launcher only offers worlds found
    on disk, so they already exist. We queue their load entry onto
    `Utils._worlds_to_load` directly and load them in this same process — no
    install, no reload, no find_spec.
    """
    import traceback
    try:
        if not module:
            module = GameIndex.game_names.get(game_name)
        if module is None:
            return _y_emit({
                "ok": False,
                "error": f"'{game_name}' is not in the game index; it can't be installed or loaded.",
            })

        if _y_world_installed(module):
            # Pip-installed (index) world: set_game_names takes the
            # importlib.metadata path (no find_spec), and `from worlds import` is
            # the first import of the package, so the load loop picks it up.
            set_game_names([game_name], strict=False)
        else:
            entry = _y_custom_world_entry(module)
            if entry is None:
                # Genuinely-missing index world: install directly via
                # ModuleUpdate, which reads importlib.metadata and never imports
                # `worlds` — unlike set_game_names, whose find_spec would import
                # `worlds` before the install is queued, so the load loop misses
                # the new world and the cached module never re-loads. We can't
                # load in this process, so install and ask the caller to re-run;
                # the fresh process sees it installed and loads it cleanly.
                apworlds = ModuleUpdate.install_worlds([module])
                if not _y_world_installed(module) and f"worlds.{module}" not in apworlds:
                    return _y_emit({
                        "ok": False,
                        "error": f"Could not install '{game_name}' (offline, or wheel/apworld missing). See log.",
                    })
                logging.info("Installed '%s'; requesting reload to load it cleanly.", game_name)
                return EXIT_NEEDS_RELOAD
            # Already-present custom world: queue its load entry BEFORE the first
            # `from worlds import` so worlds/__init__'s load loop picks it up,
            # bypassing set_game_names' find_spec (which would import `worlds`
            # before the world is queued and miss it).
            Utils._worlds_to_load.append(entry)

        from worlds import AutoWorldRegister, failed_world_loads

        world = AutoWorldRegister.world_types.get(game_name)
        if world is None:
            if f"worlds.{module}" in failed_world_loads or game_name in failed_world_loads:
                return _y_emit({
                    "ok": False,
                    "error": f"World for '{game_name}' failed to import. See stderr for the traceback.",
                })
            return _y_emit({
                "ok": False,
                "error": f"'{game_name}' did not register a World subclass.",
            })

        visibility_flag = (
            Options.Visibility.complex_ui
            if visibility == "complex"
            else Options.Visibility.simple_ui
        )
        option_groups = Options.get_option_groups(world, visibility_level=visibility_flag)

        groups_out: dict[str, list] = {}
        for group_name, options in option_groups.items():
            descs = []
            for option_name, option_class in (options or {}).items():
                try:
                    descs.append(_y_describe_option(option_name, option_class))
                except Exception as e:
                    logging.warning("describe_option(%s) failed: %s", option_name, e)
            if descs:
                groups_out[group_name] = descs

        return _y_emit({
            "ok": True,
            "game_name": game_name,
            "world": _y_describe_world(world),
            "groups": groups_out,
        })
    except Exception as e:
        logging.error("dump_yaml_options failed", exc_info=True)
        return _y_emit({"ok": False, "error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()})


if __name__ == '__main__':
    import atexit
    import sys

    # YAML-options mode: emit JSON and exit before the generation pipeline (and
    # before the interactive "Press enter" atexit hook, which would hang a
    # subprocess).
    if _YAML_OPTIONS_MODE:
        _y_args = mystery_argparse()
        sys.exit(dump_yaml_options(_y_args.yaml_options_game, _y_args.visibility, _y_args.module))

    confirmation = atexit.register(input, "Press enter to close.")
    try:
        erargs, seed = main()
    except RuntimeError as e:
        logging.error(str(e))
        sys.exit(1)
    from Main import main as ERmain
    multiworld = ERmain(erargs, seed)
    # if __debug__:
    #     import gc
    #     import sys
    #     import weakref
    #     weak = weakref.ref(multiworld)
    #     del multiworld
    #     gc.collect()  # need to collect to deref all hard references
    #     assert not weak(), f"MultiWorld object was not de-allocated, it's referenced {sys.getrefcount(weak())} times." \
    #                        " This would be a memory leak."
    # in case of error-free exit should not need confirmation
    atexit.unregister(confirmation)