"""Back-compat shim: the component registry lives in top-level LauncherComponents
so launcher-side consumers can import it without initializing the worlds package
(worlds/__init__ runs a one-shot world load that belongs to client processes
only). World modules keep importing worlds.LauncherComponents; both names share
the same objects.
"""
from LauncherComponents import (
    Component,
    ComponentList,
    Type,
    SuffixIdentifier,
    components,
    icon_paths,
    identify,
    find_component,
    builtin_components,
    get_exe,
    get_client_exe,
    launch_exe,
    spawn_client,
    launch,
    launch_subprocess,
    launch_textclient,
    run_component,
    _launch_component,
    run_world_tool,
    WorldTool,
    world_manifest_components,
    world_tool_entries,
    install_apworld,
    open_host_yaml,
    open_patch,
    browse_files,
    export_datapackage,
    processes,
    resolve_icon_path,
)
