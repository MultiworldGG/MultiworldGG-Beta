import os
import logging

if os.environ.get("MWGG_FRONTEND", "gui") == "tui":
    # Per-world clients still `from kvui import <kivy names>`; importing Kivy here
    # would open a rogue window over the TUI, so serve inert non-Kivy stand-ins.
    # Safe because the Kivy per-world UI is never built under the TUI; GameManager
    # stays a real class so the takeover in its async_run() keeps working.

    class _InertMeta(type):
        """Metaclass so stand-in *classes* tolerate attribute access too, e.g.
        ``Clock.schedule_interval`` or ``App.get_running_app`` used on the class."""

        def __getattr__(cls, name):
            if name.startswith("__") and name.endswith("__"):
                raise AttributeError(name)
            return _INERT

    class _Inert(metaclass=_InertMeta):
        """Universal inert stand-in for a Kivy/KivyMD object under the TUI frontend.

        Usable as a base class; instances accept any constructor args and tolerate
        being called, attribute-accessed, indexed or iterated. Calling the class
        (e.g. ``StringProperty("")``) returns an inert instance.
        """

        def __init__(self, *args, **kwargs):
            pass

        def __call__(self, *args, **kwargs):
            return _INERT

        def __getattr__(self, name):
            if name.startswith("__") and name.endswith("__"):
                raise AttributeError(name)
            return _INERT

        def __getitem__(self, key):
            return _INERT

        def __bool__(self):
            return False

        def __iter__(self):
            return iter(())

    _INERT = _Inert()

    def dp(value):
        """kivy.metrics.dp stand-in -- density is meaningless without a window, and
        worlds use dp() in class bodies (e.g. ``height=dp(30)``), so return the value."""
        return value

    sp = dp
    Clock = _INERT
    Window = _INERT

    class GameManager:
        logging_pairs: list = []
        base_title: str = ""

        def __init__(self, ctx, *args, **kwargs):
            self.ctx = ctx

        def __getattr__(self, name):
            # Subclasses reach for Kivy-app attributes the GUI build would supply;
            # under the TUI build() never runs, so answer inertly instead of crashing.
            if name.startswith("__") and name.endswith("__"):
                raise AttributeError(name)
            return _INERT

        async def async_run(self):
            if self.ctx._can_takeover_existing_ui():
                await self.ctx._takeover_existing_ui()
            else:
                logging.critical("Client did not launch properly, exiting.")
                error_callback = getattr(self.ctx, "_error_callback", None)
                if error_callback is not None:
                    error_callback()
                return

        def run(self):
            pass

        def add_client_tab(self, title, content, index=-1):
            return None

        def remove_client_tab(self, tab):
            pass

        def create_custom_screen(self, title, content, index=-1):
            return None

        def remove_custom_screen(self, button):
            pass

    def __getattr__(name):
        """Serve an inert stand-in for any Kivy/KivyMD name a world client imports from
        kvui under the TUI frontend (PEP 562). Cached as a module global so the class
        identity is stable across imports -- multiple inheritance and any isinstance/
        issubclass checks depend on it. Never imports Kivy."""
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        stub = _InertMeta(name, (_Inert,), {})
        globals()[name] = stub
        logging.getLogger("kvui").debug("kvui(tui): served inert stand-in for %r", name)
        return stub

else:
    import re
    import typing

    from mwgg_gui.components.dialog import MessageBox
    from mwgg_gui.overrides.screen import CustomScreen
    from kivymd.uix.textfield import MDTextField as ResizableTextField

    from mwgg_gui.app import MultiMDApp as ThemedApp, MainScreenMgr as MDScreenManagerBase
    # Legacy widget shapes for world kv files that reference them by bare class name;
    # importing registers them with the kivy Factory and keeps the old import path working.
    from mwgg_gui.legacy import SelectableLabel, SelectableRecycleBoxLayout
    from NetUtils import HintStatus, KivyMarkupJSONtoTextParser as KivyJSONtoTextParser
    from kivymd.uix.scrollview import MDScrollView as ScrollBox
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty
    from kivy.metrics import dp
    from kivy.uix.widget import Widget
    from kivy.app import App
    from kivymd.uix.appbar import MDFabBottomAppBarButton as MDNavigationItemBase
    from kivymd.uix.screen import MDScreen
    from kivymd.uix.gridlayout import MDGridLayout as MainLayout
    from kivymd.uix.floatlayout import MDFloatLayout as ContainerLayout
    from kivymd.uix.recycleview import MDRecycleView
    from kivymd.uix.divider import MDDivider
    from kivymd.uix.label import MDLabel
    from kivymd.uix.progressindicator import MDLinearProgressIndicator
    from kivymd.uix.floatlayout import MDFloatLayout
    from kivymd.uix.button import MDButton as ToggleButton

    from kivy.uix.image import AsyncImage as ApAsyncImage

    # Compatibility re-exports: worlds import these canonical kivy/kivymd names from
    # kvui; the GUI imports above bind some only under MWGG aliases or not at all.
    from kivy.clock import Clock
    from kivy.core.clipboard import Clipboard
    from kivy.core.text.markup import MarkupLabel
    from kivy.core.window import Window
    from kivy.factory import Factory
    from kivy.lang import Builder
    from kivy.uix.recycleview.views import RecycleDataViewBehavior
    from kivy.utils import escape_markup
    from kivymd.app import MDApp
    from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
    from kivymd.uix.gridlayout import MDGridLayout
    from kivymd.uix.menu import MDDropdownMenu
    from kivymd.uix.menu.menu import MDDropdownTextItem
    from kivymd.uix.textfield.textfield import MDTextField
    from kivymd.uix.tooltip import MDTooltip, MDTooltipPlain
    from kivymd.uix.behaviors import HoverBehavior as MDHoverBehavior

    from mwgg_gui.hint.legacyhint import *

    from mwgg_gui.hint.legacyhint import RefToolTip as ToolTip
    from mwgg_gui.hint.legacyhint import HintTooltipLabel as TooltipLabel
    MarkupToolTip = ToolTip

    from mwgg_gui.components.columns import (
        ColumnSorter, ColumnSortMixin, ColumnFilter, ColumnFilterMixin,
        ColumnFilterMulti, ColumnFilterItemClassification, ExtraColumn,
    )
    from mwgg_gui.overrides import HoverLabel as HovererableLabel

    class HoverBehavior(MDHoverBehavior):
        hovered = BooleanProperty(False)
        def __init__(self, **kwargs):
            self.register_event_type("on_enter")
            self.register_event_type("on_leave")
            Window.bind(mouse_pos=self.on_mouse_pos)
            self.bind(hover_visible=lambda instance, value: setattr(self, 'hovered', value))
            super(HoverBehavior, self).__init__(**kwargs)

        def on_mouse_pos(self, *args):
            self.on_mouse_update(*args)

        def on_enter(self):
            self.dispatch("on_enter")

        def on_leave(self):
            self.dispatch("on_leave")

    Factory.register("HoverBehavior", HoverBehavior)

    class ClassicHintScreen(CustomScreen):
        """Classic (pre-split) hint table wrapped in a CustomScreen.

        Duck-types the surface MultiMDApp expects of its hint screen: MDScreen
        name "hint", update_hints_list(), and bottom_appbar.text_input (supplied
        by CustomScreen's BottomAppBar).
        """

        def __init__(self, **kwargs):
            super().__init__(name="hint", **kwargs)
            self.parser = KivyJSONtoTextParser(self.app.ctx)
            self.hint_log = HintLog(self.parser)
            # CustomLayout is an MDRelativeLayout: children need explicit
            # size/pos or they render tiny in the bottom-left corner (same fix
            # as the tracker's build_tracker_view).
            self.hint_layout = HintLayout(self.hint_log, size_hint=(1, 1), pos_hint={"x": 0, "y": 0}, padding=[dp(20),dp(20),dp(20),dp(20)])
            self.custom_layout.add_widget(self.hint_layout)

        def update_hints_list(self):
            ctx = self.app.ctx
            hints = ctx.stored_data.get(f"_read_hints_{ctx.team}_{ctx.slot}", []) or []
            self.hint_log.refresh_hints(hints)

    class GameManager:
        logging_pairs: list = []
        base_title: str = ""

        def __init__(self, ctx, app: App | None = None, **kwargs):
            self.ctx = ctx
            self._running_app = app
            self._json_to_kivy_parser = None

        @property
        def json_to_kivy_parser(self) -> KivyJSONtoTextParser:
            """Legacy parser surface some per-world clients read (e.g. dkc2 uses
            ctx.ui.json_to_kivy_parser.color_codes for palette strings)."""
            if self._json_to_kivy_parser is None:
                self._json_to_kivy_parser = KivyJSONtoTextParser(self.ctx)
            return self._json_to_kivy_parser

        @json_to_kivy_parser.setter
        def json_to_kivy_parser(self, parser: KivyJSONtoTextParser) -> None:
            # world clients may assign a custom parser; keep the surface writable
            self._json_to_kivy_parser = parser

        def attach_live_app(self, app: App) -> None:
            self._running_app = app

        @classmethod
        def build_for_live_app(cls, ctx, app: App):
            from ClientState import ClientState

            previous_state = getattr(ctx, "_state", None)
            ctx._state = ClientState.LEGACY_KVUI
            try:
                manager = cls(ctx)
                manager.attach_live_app(app)

                root_layout = getattr(app, "root_layout", None) or app.root
                manager.screen_manager = app.screen_manager
                manager.container = root_layout
                manager.root_layout = root_layout
                manager.grid = app.main_layout

                manager.build()
                app._legacy_kvui_manager = manager
                return manager
            finally:
                if previous_state is not None:
                    ctx._state = previous_state

        def _get_running_app(self):
            if self._running_app is None:
                self._running_app = App.get_running_app()
            return self._running_app

        def __getattr__(self, name):
            try:
                return getattr(self._get_running_app(), name)
            except RuntimeError as e:
                raise AttributeError(name) from e

        async def async_run(self):
            ''' Changing this 'run' to instead do the client takeover loop '''
            if self.ctx._can_takeover_existing_ui():
                await self.ctx._takeover_existing_ui()
            else:
                logging.critical("Client did not launch properly, exiting.")
                error_callback = getattr(self.ctx, "_error_callback", None)
                if error_callback is not None:
                    error_callback()
                return

        def run(self):
            ''' Stubbing this to catch a 'rerun' of the app (which is already running) '''
            pass

        def build(self):
            '''Return the already-running frontend root instead of building a second MDApp.'''
            return self._get_running_app().root

        def add_client_tab(self, title: str, content: Widget, index: int = -1) -> MDNavigationItemBase:
            '''Stub function for client hook'''
            return self._get_running_app().add_client_tab(title, content, index)

        def remove_client_tab(self, tab: MDNavigationItemBase) -> None:
            '''Stub function for client hook'''
            self._get_running_app().remove_client_tab(tab)

        def create_custom_screen(self, title: str, content: Widget, index: int = -1) -> MDNavigationItemBase:
            """
            Adds a new screen to the client window with a given title, and provides a given Widget as its content.
            Returns the new button widget, with the provided content being placed on the screen as content.

            :param title: The title of the screen.
            :param content: The Widget to be added as content for this screen's new MDScreen. Will also be added to the
             returned button as button.content.
            :param index: The index to insert the button at. Defaults to -1, meaning the button will be appended to the end.

            :return: The new navigation item button.
            """
            return self._get_running_app().create_custom_screen(title, content, index)

        def remove_custom_screen(self, button: MDNavigationItemBase):
            self._get_running_app().remove_custom_screen(button)
