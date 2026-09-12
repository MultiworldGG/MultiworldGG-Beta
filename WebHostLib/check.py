import os
import zipfile
import base64
import copy
from collections.abc import Set

from flask import request, flash, redirect, url_for, render_template
from markupsafe import Markup

from WebHostLib import app
from WebHostLib.upload import allowed_options, banned_file

from Generate import apply_meta_weights, roll_settings, PlandoOptions
from Utils import parse_yamls


@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        else:
            files = request.files.getlist('file')
            options = get_yaml_data(files)
            if isinstance(options, str):
                flash(options)
            else:
                results, _ = roll_options(options)
                if len(options) > 1:
                    # offer combined file back
                    combined_yaml = "\n---\n".join(f"# original filename: {file_name}\n{file_content.decode('utf-8-sig')}"
                                                 for file_name, file_content in options.items())
                    combined_yaml = base64.b64encode(combined_yaml.encode("utf-8-sig")).decode()
                else:
                    combined_yaml = ""
                return render_template("checkResult.html",
                                       results=results, combined_yaml=combined_yaml)
    return render_template("check.html")


@app.route('/mysterycheck')
def mysterycheck():
    return redirect(url_for("check"), 301)


def _is_valid_yaml_content(content: bytes, filename: str) -> tuple[bool, str | None]:
    """Check if content is valid YAML with required fields.

    Returns (is_valid, error_message).
    """
    # Block .apworld files — these should use the APWorld upload button, not the YAML checker.
    if filename.endswith('.apworld'):
        return False, f"'{filename}' is an APWorld file. In a lobby, use the APWorld upload button instead."

    try:
        yaml_datas = tuple(parse_yamls(content))
        if not yaml_datas:
            return False, f"'{filename}' contains no valid YAML documents"

        for yaml_data in yaml_datas:
            if yaml_data is None:
                continue
            # Check for required fields: 'name' and 'game'
            if 'game' not in yaml_data:
                return False, f"'{filename}' is missing required field 'game'"
            if 'name' not in yaml_data:
                return False, f"'{filename}' is missing required field 'name'"

        return True, None
    except Exception as e:
        return False, f"'{filename}' is not valid YAML: {e}"


def get_yaml_data(files) -> dict[str, str] | str | Markup:
    options = {}
    for uploaded_file in files:
        if banned_file(uploaded_file.filename):
            return ("Uploaded data contained a rom file, which is likely to contain copyrighted material. "
                    "Your file was deleted.")
        # If the user does not select file, the browser will still submit an empty string without a file name.
        elif uploaded_file.filename == "":
            return "No selected file."
        elif uploaded_file.filename in options:
            return f"Conflicting files named {uploaded_file.filename} submitted."
        elif uploaded_file:
            if uploaded_file.filename.endswith(".zip"):
                if not zipfile.is_zipfile(uploaded_file):
                    return f"Uploaded file {uploaded_file.filename} is not a valid .zip file and cannot be opened."

                uploaded_file.seek(0)  # offset from is_zipfile check
                with zipfile.ZipFile(uploaded_file, "r") as zfile:
                    for file in zfile.infolist():
                        # Remove folder pathing from str (e.g. "__MACOSX/" folder paths from archives created by macOS).
                        base_filename = os.path.basename(file.filename)

                        if base_filename.endswith(".archipelago"):
                            return Markup("Error: Your .zip file contains an .archipelago file. "
                                          'Did you mean to <a href="/uploads">host a game</a>?')
                        elif base_filename.endswith(".zip"):
                            return "Nested .zip files inside a .zip are not supported."
                        elif banned_file(base_filename):
                            return ("Uploaded data contained a rom file, which is likely to contain copyrighted "
                                    "material. Your file was deleted.")
                        # Ignore dot-files.
                        elif not base_filename.startswith(".") and allowed_options(base_filename):
                            options[file.filename] = zfile.open(file, "r").read()
            else:
                # Accept any file extension - validate by content
                content = uploaded_file.read()
                is_valid, error = _is_valid_yaml_content(content, uploaded_file.filename)
                if is_valid:
                    options[uploaded_file.filename] = content
                elif error:
                    return error

    if not options:
        return "Did not find any valid YAML files with required fields 'name' and 'game'"
    return options


def parse_meta_yaml(content: bytes) -> dict:
    """Validate a lobby meta file without rolling its weights or loading custom worlds."""
    from Options import CommonOptions
    from worlds.AutoWorld import AutoWorldRegister

    documents = tuple(parse_yamls(content))
    if len(documents) != 1 or not isinstance(documents[0], dict):
        raise ValueError("meta.yaml must contain exactly one YAML mapping")
    meta = documents[0].copy()
    if "meta_description" not in meta:
        raise ValueError("meta.yaml must include meta_description")
    meta.pop("meta_description")
    for game, category in meta.items():
        if game is not None and (not isinstance(game, str) or not game):
            raise ValueError("Meta categories must be world names or null")
        if not isinstance(category, dict):
            raise ValueError(f"Meta category {game!r} must contain an option mapping")
        world = AutoWorldRegister.world_types.get(game)
        option_types = world.options_dataclass.type_hints if world else CommonOptions.type_hints if game is None else None
        for key, value in category.items():
            if not isinstance(key, str):
                raise ValueError("Meta option names must be strings")
            if key == "triggers" and game is not None:
                if not isinstance(value, list) or any(not isinstance(trigger, dict) for trigger in value):
                    raise ValueError("Meta triggers must be a list of mappings")
                continue
            if option_types is not None:
                if key not in option_types:
                    raise ValueError(f"Unknown meta option {key!r} for {game or 'common options'}")
                if option_types[key].supports_weighting and isinstance(value, dict) and value:
                    try:
                        weights = [int(weight) for weight in value.values()]
                    except (ValueError, TypeError, OverflowError) as exc:
                        raise ValueError(f"Invalid weights for meta option {key!r}") from exc
                    if min(weights) < 0 or sum(weights) <= 0:
                        raise ValueError(f"Meta weights for {key!r} must be nonnegative with a positive total")
    return meta


def roll_options(options: dict[str, dict | str],
                 plando_options: Set[str] = frozenset({"bosses", "items", "connections", "texts"}),
                 meta_weights: dict | None = None) -> \
        tuple[dict[str, str | bool], dict[str, dict]]:
    plando_options = PlandoOptions.from_set(set(plando_options))
    results: dict[str, str | bool] = {}
    rolled_results: dict[str, dict] = {}
    parsed_options = {}
    for filename, text in options.items():
        try:
            if type(text) is dict:
                yaml_datas = (text, )
            else:
                yaml_datas = tuple(parse_yamls(text))
        except Exception as e:
            results[filename] = f"Failed to parse YAML data in {filename}: {e}"
        else:
            parsed_options[filename] = yaml_datas

    if meta_weights:
        try:
            parsed_options = copy.deepcopy(parsed_options)
            apply_meta_weights({name: tuple(y for y in yamls if y is not None)
                                for name, yamls in parsed_options.items()}, meta_weights)
        except Exception as e:
            results["meta.yaml"] = f"Failed to apply meta.yaml: {e}"
            return results, {}

    for filename, yaml_datas in parsed_options.items():
        try:
            if len(yaml_datas) == 1:
                rolled_results[filename] = roll_settings(yaml_datas[0], plando_options=plando_options)
            else:
                for i, yaml_data in enumerate(yaml_datas):
                    if yaml_data is not None:
                        rolled_results[f"{filename}/{i + 1}"] = roll_settings(yaml_data, plando_options=plando_options)
        except Exception as e:
            if e.__cause__:
                results[filename] = f"Failed to generate options in {filename}: {e} - {e.__cause__}"
            else:
                results[filename] = f"Failed to generate options in {filename}: {e}"
        else:
            results[filename] = True
    return results, rolled_results
