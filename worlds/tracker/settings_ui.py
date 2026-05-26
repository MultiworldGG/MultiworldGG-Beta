"""Tracker settings panel for the global SettingsScreen.

Plugged in via ``mwgg_gui.settings.register_settings_section("tracker", ...)``.
All host.yaml-persisted values flow through ``TrackerWorld.settings``; runtime-
only toggles (Show Map, Reset Pack Path) talk directly to the live context.
"""
from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from kivy.metrics import dp
from kivy.app import App
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel

from mwgg_gui.settings import (
    SettingsScrollBox,
    SettingsSection,
    LabeledSwitch,
    LabeledDropdown,
)

logger = logging.getLogger("Client")

if TYPE_CHECKING:
    from worlds.tracker import TrackerWorld
    from worlds.tracker.TrackerClient import TrackerGameContext


_DEFERRED_ENTRANCE_CHOICES = ["default", "on", "off"]
_SORTING_METHOD_CHOICES = ["apworld", "location", "region", "label"]


def _tracker_settings():
    """Late-import TrackerWorld so this module can be imported by gui.py
    without forcing the full world registration on launcher startup."""
    from worlds.tracker import TrackerWorld
    return TrackerWorld.settings


def _ctx() -> "TrackerGameContext | None":
    """Return the live TrackerGameContext, if any."""
    app = App.get_running_app()
    if app is None:
        return None
    ctx = getattr(app, "ctx", None)
    # Avoid clinging to the launcher's InitContext; we only care about a
    # TrackerGameContext.
    from worlds.tracker.TrackerClient import TrackerGameContext
    if isinstance(ctx, TrackerGameContext):
        return ctx
    return None


def _save_settings():
    """Mark TrackerWorld.settings dirty and write through to host.yaml.

    The settings system persists on dirty + flush. Setting ``_changed = True``
    is the existing idiom — see ``current_world.settings._changed = True`` in
    TrackerClient.load_pack.
    """
    try:
        st = _tracker_settings()
        st._changed = True
    except Exception:
        logger.exception("Failed to mark TrackerWorld.settings dirty")


class TrackerSettings(SettingsScrollBox):
    """Universal Tracker settings panel for the global SettingsScreen."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        # --- Runtime toggles ----------------------------------------------
        runtime_section = SettingsSection(name="tracker_runtime", title="Runtime")

        ctx = _ctx()
        self._show_map_switch = LabeledSwitch(
            text="Show Map tab",
            on_switch=self._on_show_map,
        )
        self._show_map_switch.ids.switch.active = bool(ctx and ctx._show_map)
        runtime_section.add_widget(self._show_map_switch)

        # Reset pack path: blanks the connected world's external_pack_key so
        # the next reconnect re-runs the load_pack file picker.
        reset_box = MDBoxLayout(orientation="horizontal", size_hint_y=None,
                                height=dp(55), padding=dp(4), spacing=dp(4))
        reset_box.add_widget(MDLabel(
            text="Reset Poptracker pack path",
            theme_text_color="Secondary",
            size_hint_x=0.7,
        ))
        reset_button = MDButton(MDButtonText(text="Reset"), style="filled")
        reset_button.bind(on_release=lambda *_: self._reset_pack_path())
        reset_box.add_widget(reset_button)
        runtime_section.add_widget(reset_box)

        self.layout.add_widget(runtime_section)

        # --- Display options ----------------------------------------------
        display_section = SettingsSection(name="tracker_display", title="Display")
        display_section.add_widget(self._bool_row(
            "Include region names",
            "include_region_name",
        ))
        display_section.add_widget(self._bool_row(
            "Include location names",
            "include_location_name",
        ))
        display_section.add_widget(self._bool_row(
            "Hide excluded locations",
            "hide_excluded_locations",
        ))
        display_section.add_widget(self._bool_row(
            "Show glitched logic",
            "display_glitched_logic",
        ))
        display_section.add_widget(self._bool_row(
            "Use split map icons",
            "use_split_map_icons",
        ))
        self.layout.add_widget(display_section)

        # --- Behavior options ---------------------------------------------
        behavior_section = SettingsSection(name="tracker_behavior", title="Behavior")
        behavior_section.add_widget(self._bool_row(
            "Save manual commands per seed",
            "save_entered_commands",
        ))
        behavior_section.add_widget(self._dropdown_row(
            "Deferred entrances",
            "enforce_deferred_entrances",
            _DEFERRED_ENTRANCE_CHOICES,
        ))
        behavior_section.add_widget(self._dropdown_row(
            "Sort by",
            "sorting_method",
            _SORTING_METHOD_CHOICES,
        ))
        self.layout.add_widget(behavior_section)

    # ---- runtime handlers ------------------------------------------------

    def _on_show_map(self, _switch, value: bool):
        ctx = _ctx()
        if ctx is None:
            logger.info("Show Map toggled with no live tracker context; ignoring.")
            return
        ctx.set_map_visible(bool(value))

    def _reset_pack_path(self):
        """Clear the connected world's poptracker pack setting so the next
        load_pack call re-runs the file picker dialog.

        Important: ``ctx.tracker_world`` is set to None whenever ``load_pack``
        fails (invalid/missing pack, user cancelled the picker, etc.) — which
        is exactly the moment Reset is useful. So we read the pack key from
        the connected World class's ``tracker_world`` dict directly, not from
        the runtime ``ctx.tracker_world`` attribute.
        """
        ctx = _ctx()
        if ctx is None:
            logger.info("No live tracker context; nothing to reset.")
            return
        if not ctx.game:
            logger.info("No game connected; nothing to reset.")
            return

        from worlds import AutoWorld
        connected_cls = AutoWorld.AutoWorldRegister.world_types.get(ctx.game)
        if connected_cls is None:
            logger.info(f"World class for {ctx.game!r} not found; nothing to reset.")
            return

        # tracker_world is typically a dict ClassVar on the World class, but
        # some worlds set it on the per-slot world instance instead.
        tracker_world_data = getattr(connected_cls, "tracker_world", None)
        if not tracker_world_data:
            current_world = ctx.tracker_core.get_current_world() if ctx.tracker_core else None
            if current_world is not None:
                tracker_world_data = getattr(current_world, "tracker_world", None)
        if not tracker_world_data:
            logger.info(f"{ctx.game!r} does not advertise tracker_world; nothing to reset.")
            return

        # tracker_world may be a dict (raw class attr) or a UTMapTabData instance.
        if isinstance(tracker_world_data, dict):
            key = tracker_world_data.get("external_pack_key", "")
        else:
            key = getattr(tracker_world_data, "external_pack_key", "")
        if not key:
            logger.info(f"{ctx.game!r} does not use an external pack key; nothing to reset.")
            return

        current_world = ctx.tracker_core.get_current_world() if ctx.tracker_core else None
        if current_world is None:
            logger.info("No current world instance available to mutate settings on.")
            return
        try:
            current_world.settings[key] = ""
            current_world.settings._changed = True
            logger.info(f"Cleared poptracker pack path ({key}); reconnect to re-prompt for the pack.")
        except Exception:
            logger.exception("Failed to reset poptracker pack path")

    # ---- TrackerWorld.settings helpers -----------------------------------

    def _bool_row(self, label: str, field: str) -> LabeledSwitch:
        st = _tracker_settings()
        current = bool(getattr(st, field, False))
        def _on_change(_switch, value, _field=field):
            setattr(_tracker_settings(), _field, bool(value))
            _save_settings()
        row = LabeledSwitch(text=label, on_switch=_on_change)
        row.ids.switch.active = current
        return row

    def _dropdown_row(self, label: str, field: str, choices: list[str]) -> LabeledDropdown:
        st = _tracker_settings()
        current = str(getattr(st, field, choices[0]))
        def _on_select(value, _field=field):
            setattr(_tracker_settings(), _field, str(value))
            _save_settings()
        return LabeledDropdown(
            text=label,
            items=choices,
            current_item=current,
            on_select=_on_select,
        )
