# Release Notes

Bundled APWorlds are Gone
-------------------------

MultiworldGG no longer ships per-game world code as part of the core distribution. The `worlds/` tree in this repo now contains only the shared infrastructure — `_bizhawk`, `_manual`, `_sni`, `_tracker`, `_debug`, plus `generic/` — and per-game worlds can be moved out to their own upstream repositories, resolved at install/run time through the MultiworldGG-Index. **World authors**: see the [MultiworldGG-Index documentation](https://github.com/MultiworldGG/MultiworldGG-Index) for how to take control of your world. The `custom_worlds/` folder continues to work as before.


Running executables does not import all worlds
----------------------------------------------

 Two things have changed. First, because per-game worlds are no longer bundled, the universe of "what could be imported" is at most scoped to what you have actually installed — via the index or `custom_worlds/` — instead of an ever-growing static list inside the executable. Second, the launcher, in-game clients, and other entry points that don't need world classes no longer pay that startup cost. **Cold-start time is substantially lower**.


We have rewritten the GUI and added a TUI
-----------------------------------------

 The Kivy-based desktop interface has moved into a separate module and can be released on its own cadence. A new textual based alternative provides a terminal-first experience for headless machines or users who want a lightweight experience. The active frontend is selected at runtime via the `MWGG_FRONTEND` environment variable (`"gui"` or `"tui"`) or with `--frontend=tui` arguments.
