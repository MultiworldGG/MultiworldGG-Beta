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
    from mwgg_gui.overrides.markuptextfield import MarkupTextField as ResizableTextField

    from mwgg_gui.app import MultiMDApp as ThemedApp, MainScreenMgr as MDScreenManagerBase
    # Legacy widget shapes for world kv files that reference them by bare class name;
    # importing registers them with the kivy Factory and keeps the old import path working.
    from mwgg_gui.legacy import SelectableLabel, SelectableRecycleBoxLayout
    from NetUtils import HintStatus, KivyRefJSONtoTextParser as KivyJSONtoTextParser
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

    remove_between_brackets = re.compile(r"\[.*?]")

    # kivymd's HoverBehavior shares an MRO-incompatible base with the widgets worlds
    # mix it into; this plain object-based mixin (the original MWGG one) linearizes cleanly.
    class HoverBehavior(object):
        """originally from https://stackoverflow.com/a/605348110"""
        hovered = BooleanProperty(False)
        border_point = ObjectProperty(None)

        def __init__(self, **kwargs):
            self.register_event_type("on_enter")
            self.register_event_type("on_leave")
            Window.bind(mouse_pos=self.on_mouse_pos)
            Window.bind(on_cursor_leave=self.on_cursor_leave)
            super(HoverBehavior, self).__init__(**kwargs)

        def on_mouse_pos(self, window, pos):
            if not self.get_root_window():
                return  # Abort if not displayed
            # to_widget translates window pos to within widget pos
            inside = self.collide_point(*self.to_widget(*pos))
            if self.hovered == inside:
                return  # We have already done what was needed
            self.border_point = pos
            self.hovered = inside
            if inside:
                self.dispatch("on_enter")
            else:
                self.dispatch("on_leave")

        def on_cursor_leave(self, *args):
            # if the mouse left the window, it is no longer inside the hover widget.
            self.hovered = BooleanProperty(False)
            self.border_point = ObjectProperty(None)
            self.dispatch("on_leave")

    Factory.register("HoverBehavior", HoverBehavior)

    # ------------------------------------------------------------------
    # Classic hint screen cluster, restored from the pre-split kvui.py.
    # Layout/behavior are verbatim MAIN; colors are theme-mapped (see the
    # Builder.load_string block and status_colors below).
    # ------------------------------------------------------------------

    class ToolTip(MDTooltipPlain):
        markup = True

    class HovererableLabel(HoverBehavior, MDLabel):
        pass

    class TooltipLabel(HovererableLabel, MDTooltip):
        tooltip_display_delay = 0.1

        def create_tooltip(self, text, x, y):
            text = text.replace("<br>", "\n").replace("&amp;", "&").replace("&bl;", "[").replace("&br;", "]")
            # position float layout
            center_x, center_y = self.to_window(self.center_x, self.center_y)
            self.shift_y = y - center_y
            shift_x = center_x - x
            if shift_x > 0:
                self.shift_left = shift_x
            else:
                self.shift_right = shift_x

            if self._tooltip:
                # update
                self._tooltip.text = text
            else:
                self._tooltip = ToolTip(text=text, pos_hint={})
                self.display_tooltip()

        def on_mouse_pos(self, window, pos):
            if not self.get_root_window():
                return  # Abort if not displayed
            if self.disabled:
                return
            super().on_mouse_pos(window, pos)
            if self.refs and self.hovered:

                tx, ty = self.to_widget(*pos, relative=True)
                # Why TF is Y flipped *within* the texture?
                ty = self.texture_size[1] - ty
                hit = False
                for uid, zones in self.refs.items():
                    for zone in zones:
                        x, y, w, h = zone
                        if x <= tx <= w and y <= ty <= h:
                            self.create_tooltip(uid.split("|", 1)[1], *pos)
                            hit = True
                            break
                if not hit:
                    self.remove_tooltip()

        def on_enter(self):
            pass

        def on_leave(self):
            self.remove_tooltip()
            self._tooltip = None

    class MarkupDropdownTextItem(MDDropdownTextItem):
        def __init__(self):
            super().__init__()
            for child in self.children:
                if child.__class__ == MDLabel:
                    child.markup = True
        # Currently, this only lets us do markup on text that does not have any icons
        # Create new TextItems as needed

    class MarkupDropdown(MDDropdownMenu):
        def on_items(self, instance, value: list) -> None:
            """
            The method sets the class that will be used to create the menu item.
            """

            items = []
            viewclass = "MarkupDropdownTextItem"

            for data in value:
                if "viewclass" not in data:
                    if (
                        "leading_icon" not in data
                        and "trailing_icon" not in data
                        and "trailing_text" not in data
                    ):
                        viewclass = "MarkupDropdownTextItem"
                    elif (
                        "leading_icon" in data
                        and "trailing_icon" not in data
                        and "trailing_text" not in data
                    ):
                        viewclass = "MDDropdownLeadingIconItem"
                    elif (
                        "leading_icon" not in data
                        and "trailing_icon" in data
                        and "trailing_text" not in data
                    ):
                        viewclass = "MDDropdownTrailingIconItem"
                    elif (
                        "leading_icon" not in data
                        and "trailing_icon" in data
                        and "trailing_text" in data
                    ):
                        viewclass = "MDDropdownTrailingIconTextItem"
                    elif (
                        "leading_icon" in data
                        and "trailing_icon" in data
                        and "trailing_text" in data
                    ):
                        viewclass = "MDDropdownLeadingTrailingIconTextItem"
                    elif (
                        "leading_icon" in data
                        and "trailing_icon" in data
                        and "trailing_text" not in data
                    ):
                        viewclass = "MDDropdownLeadingTrailingIconItem"
                    elif (
                        "leading_icon" not in data
                        and "trailing_icon" not in data
                        and "trailing_text" in data
                    ):
                        viewclass = "MDDropdownTrailingTextItem"
                    elif (
                        "leading_icon" in data
                        and "trailing_icon" not in data
                        and "trailing_text" in data
                    ):
                        viewclass = "MDDropdownLeadingIconTrailingTextItem"

                    data["viewclass"] = viewclass

                if "height" not in data:
                    data["height"] = dp(48)

                items.append(data)

            self._items = items
            # Update items in view
            if hasattr(self, "menu"):
                self.menu.data = self._items

    class AutocompleteHintInput(ResizableTextField):
        min_chars = NumericProperty(3)

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            self.dropdown = MarkupDropdown(caller=self, position="bottom", border_margin=dp(2), width=self.width)
            self.bind(on_text_validate=self.on_message)
            self.bind(width=lambda instance, x: setattr(self.dropdown, "width", x))

        def on_message(self, instance):
            MDApp.get_running_app().commandprocessor("!hint "+instance.text)

        def on_text(self, instance, value):
            if len(value) >= self.min_chars:
                self.dropdown.items.clear()
                ctx = MDApp.get_running_app().ctx
                if not ctx.game:
                    return
                item_names = ctx.item_names._game_store[ctx.game].values()

                def on_press(text):
                    split_text = MarkupLabel(text=text).markup
                    self.set_text(self, "".join(text_frag for text_frag in split_text
                                                if not text_frag.startswith("[")))
                    self.dropdown.dismiss()
                    self.focus = True

                lowered = value.lower()
                for item_name in item_names:
                    try:
                        index = item_name.lower().index(lowered)
                    except ValueError:
                        pass  # substring not found
                    else:
                        text = escape_markup(item_name)
                        text = text[:index] + "[b]" + text[index:index+len(value)]+"[/b]"+text[index+len(value):]
                        self.dropdown.items.append({
                            "text": text,
                            "on_release": lambda txt=text: on_press(txt),
                            "markup": True
                        })
                if not self.dropdown.parent:
                    self.dropdown.open()
            else:
                self.dropdown.dismiss()

    status_icons = {
        HintStatus.HINT_NO_PRIORITY: "information",
        HintStatus.HINT_PRIORITY: "exclamation-thick",
        HintStatus.HINT_AVOID: "alert"
    }

    class HintLabel(RecycleDataViewBehavior, MDBoxLayout):
        selected = BooleanProperty(False)
        striped = BooleanProperty(False)
        index = None
        dropdown: MDDropdownMenu

        def __init__(self):
            super(HintLabel, self).__init__()
            self.receiving_text = ""
            self.item_text = ""
            self.finding_text = ""
            self.location_text = ""
            self.entrance_text = ""
            self.status_text = ""
            self.hint = {}

            ctx = MDApp.get_running_app().ctx
            menu_items = []

            for status in (HintStatus.HINT_NO_PRIORITY, HintStatus.HINT_PRIORITY, HintStatus.HINT_AVOID):
                name = status_names[status]
                menu_items.append({
                    "text": name,
                    "leading_icon": status_icons[status],
                    "on_release": lambda x=status: select(self, x)
                })

            self.dropdown = MDDropdownMenu(caller=self.ids["status"], items=menu_items)

            def select(instance, data):
                ctx.update_hint(self.hint["location"],
                                self.hint["finding_player"],
                                data)

            self.dropdown.bind(on_release=self.dropdown.dismiss)

        def set_height(self, instance, value):
            self.height = max([child.texture_size[1] for child in self.children])

        def refresh_view_attrs(self, rv, index, data):
            self.index = index
            self.striped = data.get("striped", False)
            self.receiving_text = data["receiving"]["text"]
            self.item_text = data["item"]["text"]
            self.finding_text = data["finding"]["text"]
            self.location_text = data["location"]["text"]
            self.entrance_text = data["entrance"]["text"]
            self.status_text = data["status"]["text"]
            self.hint = data["status"]["hint"]
            return super(HintLabel, self).refresh_view_attrs(rv, index, data)

        def on_touch_down(self, touch):
            """ Add selection on touch down """
            if super(HintLabel, self).on_touch_down(touch):
                return True
            if self.index:  # skip header
                if self.collide_point(*touch.pos):
                    status_label = self.ids["status"]
                    if status_label.collide_point(*touch.pos):
                        if self.hint["status"] == HintStatus.HINT_FOUND:
                            return True
                        ctx = MDApp.get_running_app().ctx
                        if ctx.slot_concerns_self(self.hint["receiving_player"]):  # If this player owns this hint
                            # open a dropdown
                            self.dropdown.open()
                            return True
                    elif self.selected:
                        self.parent.clear_selection()
                        return True
                    else:
                        text = "".join((self.receiving_text, "\'s ", self.item_text, " is at ", self.location_text, " in ",
                                        self.finding_text, "\'s World", (" at " + self.entrance_text)
                                        if self.entrance_text != "Vanilla"
                                        else "", ". (", self.status_text.lower(), ")"))
                        temp = MarkupLabel(text).markup
                        text = "".join(part for part in temp if not part.startswith("["))
                        Clipboard.copy(escape_markup(text).replace("&amp;", "&").replace("&bl;", "[").replace("&br;", "]"))
                        return self.parent.select_with_touch(self.index, touch)
            else:
                parent = self.parent
                parent.clear_selection()
                parent: HintLog = parent.parent
                # find correct column
                for child in self.children:
                    if child.collide_point(*touch.pos):
                        if parent.sort_by_key(child.sort_key):
                            MDApp.get_running_app().update_hints()
                            return True
                        return False
            return False

        def apply_selection(self, rv, index, is_selected):
            """ Respond to the selection of items in the view. """
            if self.index:
                self.selected = is_selected

    class HintLayout(MDBoxLayout):
        orientation = "vertical"

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            boxlayout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40))
            boxlayout.add_widget(MDLabel(text="New Hint:", size_hint_x=None, size_hint_y=None,
                                         height=dp(40), width=dp(75), halign="center", valign="center"))
            boxlayout.add_widget(AutocompleteHintInput())
            self.add_widget(boxlayout)

        def fix_heights(self):
            for child in self.children:
                fix_func = getattr(child, "fix_heights", None)
                if fix_func:
                    fix_func()

    status_names: typing.Dict[HintStatus, str] = {
        HintStatus.HINT_FOUND: "Found",
        HintStatus.HINT_UNSPECIFIED: "Unspecified",
        HintStatus.HINT_NO_PRIORITY: "No Priority",
        HintStatus.HINT_AVOID: "Avoid",
        HintStatus.HINT_PRIORITY: "Priority",
    }
    # Theme-mapped: MAIN hard-coded dark-palette color names (green/white/
    # lightgray/salmon/gold); these resolve through the MarkupTagsTheme-managed
    # TEXT_COLORS entries instead, matching the new hint screen's palette
    # semantics so Light mode stays coherent.
    status_colors: typing.Dict[HintStatus, str] = {
        HintStatus.HINT_FOUND: "location_color",
        HintStatus.HINT_UNSPECIFIED: "default_color",
        HintStatus.HINT_NO_PRIORITY: "regular_item_color",
        HintStatus.HINT_AVOID: "trap_item_color",
        HintStatus.HINT_PRIORITY: "progression_item_color",
    }
    status_sort_weights: dict[HintStatus, int] = {
        HintStatus.HINT_FOUND: 0,
        HintStatus.HINT_UNSPECIFIED: 1,
        HintStatus.HINT_NO_PRIORITY: 2,
        HintStatus.HINT_AVOID: 3,
        HintStatus.HINT_PRIORITY: 4,
    }

    class ColumnSorter:
        key: str
        sort_func: typing.Callable[[dict], typing.Any]
        reverse: bool

        def __init__(self, key: str, sort_func: typing.Callable[[dict], typing.Any], reverse: bool = False):
            self.key = key
            self.sort_func = sort_func
            self.reverse = reverse

        def sort(self, data: list[typing.Any]):
            data.sort(key=self.sort_func, reverse=self.reverse)

    class ColumnSortMixin:
        column_sorters: list[ColumnSorter]

        def __init__(self):
            self.column_sorters = []

        def sort_by_key(self, key: str) -> bool:
            found_sorter: ColumnSorter | None = None
            for sorter in self.column_sorters:
                if sorter.key == key:
                    found_sorter = sorter
                    break
            if found_sorter:
                idx = self.column_sorters.index(found_sorter)
                if idx == len(self.column_sorters) - 1:  # reverse the order if already primarily sorted by this key
                    found_sorter.reverse = not found_sorter.reverse
                else:
                    self.column_sorters.append(self.column_sorters.pop(idx))  # move this sorter to the end
                return True
            return False

        def sort_columns(self, data):
            for sorter in self.column_sorters:
                sorter.sort(data)

    class HintLog(MDRecycleView, ColumnSortMixin):
        header = {
            "receiving": {"text": "[u]Receiving Player[/u]"},
            "item": {"text": "[u]Item[/u]"},
            "finding": {"text": "[u]Finding Player[/u]"},
            "location": {"text": "[u]Location[/u]"},
            "entrance": {"text": "[u]Entrance[/u]"},
            "status": {"text": "[u]Status[/u]",
                       "hint": {"receiving_player": -1, "location": -1, "finding_player": -1, "status": ""}},
            "striped": True,
        }
        data: list[typing.Any]

        def __init__(self, parser):
            super(HintLog, self).__init__()
            self.data = [self.header]
            self.parser = parser
            # Setup default sorters for each key in a sensible default order
            # The last in the list will end up being the 'primary' sort, as each sorter is applied in-order.
            # Custom clients should be able to modify these and add additional sorters
            for key in ["entrance", "receiving", "finding", "item", "location"]:
                self.column_sorters.append(ColumnSorter(
                    key,
                    lambda element, k=key: remove_between_brackets.sub("", element[k]["text"]).lower(),
                ))
            self.column_sorters.append(ColumnSorter(
                "status",
                lambda element: status_sort_weights[element["status"]["hint"]["status"]],
                True
            ))

        def refresh_hints(self, hints):
            if not hints:  # Fix the scrolling looking visually wrong in some edge cases
                self.scroll_y = 1.0
            data = []
            app = MDApp.get_running_app()
            if app is None:
                return  # App is shutting down, skip hint refresh
            ctx = app.ctx
            for hint in hints:
                if not hint.get("status"): # Allows connecting to old servers
                    hint["status"] = HintStatus.HINT_FOUND if hint["found"] else HintStatus.HINT_UNSPECIFIED
                hint_status_node = self.parser.handle_node({"type": "color",
                                                            "color": status_colors.get(hint["status"], "red"),
                                                            "text": status_names.get(hint["status"], "Unknown")})
                if hint["status"] != HintStatus.HINT_FOUND and ctx.slot_concerns_self(hint["receiving_player"]):
                    hint_status_node = f"[u]{hint_status_node}[/u]"
                data.append({
                    "receiving": {"text": self.parser.handle_node({"type": "player_id", "text": hint["receiving_player"]})},
                    "item": {"text": self.parser.handle_node({
                        "type": "item_id",
                        "text": hint["item"],
                        "flags": hint["item_flags"],
                        "player": hint["receiving_player"],
                    })},
                    "finding": {"text": self.parser.handle_node({"type": "player_id", "text": hint["finding_player"]})},
                    "location": {"text": self.parser.handle_node({
                        "type": "location_id",
                        "text": hint["location"],
                        "player": hint["finding_player"],
                    }) if not hint.get("hidden") else "Hidden"},
                    "entrance": {"text": self.parser.handle_node({"type": "color" if hint["entrance"] else "text",
                                                                  "color": 'entrance_color', "text": hint["entrance"]
                                                                  if hint["entrance"] else "Vanilla"})
                                 if not hint.get("hidden") else "Hidden"},
                    "status": {
                        "text": hint_status_node,
                        "hint": hint,
                    },
                })

            self.sort_columns(data)

            for i in range(0, len(data), 2):
                data[i]["striped"] = True
            data.insert(0, self.header)
            self.data = data

        def fix_heights(self):
            """Workaround fix for divergent texture and layout heights"""
            for element in self.children[0].children:
                max_height = max(child.texture_size[1] for child in element.children)
                element.height = max_height

    # KV rules ported from the pre-split data/client.kv (:58-63, :113-182,
    # :190-214, :217-222). Layout is verbatim; the hard-coded navy backgrounds,
    # green selection overlay and stripe-border colors are theme-mapped onto
    # theme_cls like the rest of the mwgg_gui kv. MAIN's dead
    # <MarkupDropdownItem> rule (names a class that doesn't exist) is dropped.
    Builder.load_string("""
<TooltipLabel>:
    adaptive_height: True
    theme_font_size: "Custom"
    font_size: "20dp"
    markup: True
    halign: "left"
<HintLabel>:
    canvas.before:
        Color:
            rgba: (self.theme_cls.primaryColor[0], self.theme_cls.primaryColor[1], self.theme_cls.primaryColor[2], .3) if self.selected else self.theme_cls.surfaceContainerHighColor if self.striped else self.theme_cls.surfaceContainerLowColor
        Rectangle:
            size: self.size
            pos: self.pos
    height: self.minimum_height
    receiving_text: "Receiving Player"
    item_text: "Item"
    finding_text: "Finding Player"
    location_text: "Location"
    entrance_text: "Entrance"
    status_text: "Status"
    TooltipLabel:
        id: receiving
        sort_key: 'receiving'
        text: root.receiving_text
        halign: 'center'
        valign: 'center'
        pos_hint: {"center_y": 0.5}
    TooltipLabel:
        id: item
        sort_key: 'item'
        text: root.item_text
        halign: 'center'
        valign: 'center'
        pos_hint: {"center_y": 0.5}
    TooltipLabel:
        id: finding
        sort_key: 'finding'
        text: root.finding_text
        halign: 'center'
        valign: 'center'
        pos_hint: {"center_y": 0.5}
    TooltipLabel:
        id: location
        sort_key: 'location'
        text: root.location_text
        halign: 'center'
        valign: 'center'
        pos_hint: {"center_y": 0.5}
    TooltipLabel:
        id: entrance
        sort_key: 'entrance'
        text: root.entrance_text
        halign: 'center'
        valign: 'center'
        pos_hint: {"center_y": 0.5}
    TooltipLabel:
        id: status
        sort_key: 'status'
        text: root.status_text
        halign: 'center'
        valign: 'center'
        pos_hint: {"center_y": 0.5}
<HintLog>:
    cols: 1
    viewclass: 'HintLabel'
    scroll_y: self.height
    scroll_type: ["content", "bars"]
    bar_width: dp(12)
    effect_cls: "ScrollEffect"
    background_color: self.theme_cls.surfaceContainerLowestColor
    SelectableRecycleBoxLayout:
        default_size: None, dp(20)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
<ToolTip>:
    size: self.texture_size
    size_hint: None, None
    theme_font_size: "Custom"
    font_size: dp(18)
    pos_hint: {'center_y': 0.5, 'center_x': 0.5}
    halign: "left"
    theme_text_color: "Custom"
    text_color: app.theme_cls.onSecondaryContainerColor
    canvas.before:
        Color: # tooltip bgcolor
            rgba: app.theme_cls.secondaryContainerColor
        Rectangle:
            size: self.size
            pos: self.pos
        Color: # bigger line in stripe border of tooltip
            rgba: app.theme_cls.primaryColor
        Line:
            width: 3
            rectangle: self.x-2, self.y-2, self.width+4, self.height+4
        Color: # teeny line in stripe border of tooltip
            rgba: app.theme_cls.secondaryColor
        Line:
            width: 1
            rectangle: self.x-2, self.y-2, self.width+4, self.height+4
<AutocompleteHintInput>:
    size_hint_y: None
    height: "30dp"
    multiline: False
    write_tab: False
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
""")

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
            self.hint_layout = HintLayout(self.hint_log, size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
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
