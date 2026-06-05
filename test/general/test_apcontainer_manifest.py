"""Behavioral pins for APContainer manifest building and client-function parsing.

These tests document non-obvious facts that previously lived as inline comments
in APContainer.py: the manifest version fields, the player container's default
``server`` value, and what ``parse_client_function`` extracts (and when it
returns ``None``).
"""

from APContainer import (
    APContainer,
    APPlayerContainer,
    container_version,
    parse_client_function,
)


def test_get_manifest_reports_compatible_version_5_and_container_version():
    manifest = APContainer().get_manifest()
    assert manifest["compatible_version"] == 5
    assert manifest["version"] == container_version
    assert container_version == 7


def test_player_container_manifest_server_defaults_to_empty_string():
    manifest = APPlayerContainer().get_manifest()
    assert manifest["server"] == ""


def test_parse_client_function_returns_name_for_client_component_else_none():
    client = (
        'components.append(Component("My Client", '
        "func=launch_client, component_type=Type.CLIENT))"
    )
    assert parse_client_function(client) == "launch_client"

    # Not a components.append(Component(...)) call -> None.
    not_append = (
        'registry.add(Component("My Client", '
        "func=launch_client, component_type=Type.CLIENT))"
    )
    assert parse_client_function(not_append) is None

    # Unparseable input is swallowed and yields None.
    assert parse_client_function("def (((") is None


def test_parse_client_function_requires_both_client_type_and_func():
    missing_func = 'components.append(Component("X", component_type=Type.CLIENT))'
    assert parse_client_function(missing_func) is None

    missing_type = 'components.append(Component("X", func=launch_client))'
    assert parse_client_function(missing_type) is None

    wrong_type = (
        'components.append(Component("X", '
        "func=launch_client, component_type=Type.TOOL))"
    )
    assert parse_client_function(wrong_type) is None

    both = (
        'components.append(Component("X", '
        "func=launch_client, component_type=Type.CLIENT))"
    )
    assert parse_client_function(both) == "launch_client"
