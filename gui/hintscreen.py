from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, NumericProperty, ListProperty, ObjectProperty, StringProperty, DictProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.chip import MDChip
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.appbar import MDTopAppBar
from kivymd.theming import ThemableBehavior
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.textfield import MDTextField
#from kivymd.uix.dropdown import MarkupDropdown
from kivy.uix.label import Label
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.menu.menu import MDDropdownTextItem
from kivymd.uix.dropdownitem import MDDropDownItem, MDDropDownItemText
from kivymd.uix.behaviors import HoverBehavior
from kivy.utils import escape_markup
from kivy.core.clipboard import Clipboard
from NetUtils import HintStatus, MWGGUIHintStatus
from .testdict import testdict
import typing

# Builder.load_string(
#     '''
#     <HintLayout>
#         orientation: "vertical"
#     '''
# )

class AutocompleteHintInput(MDTextField):
    """Text input field with autocomplete functionality for hint commands.
    
    This class provides an input field that automatically suggests item names
    as the user types, specifically designed for hint commands. It shows
    matching items in a dropdown and allows quick selection.
    
    Attributes:
        min_chars (int): Minimum number of characters before showing suggestions (3)
    """
    min_chars = NumericProperty(3)
    item_names: list[str] = []
    location_names: list[str] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dropdown = MDDropdownMenu(caller=self, position="bottom", border_margin=dp(2), width=self.width)
        self.bind(on_text_validate=self.on_message)
        self.bind(width=lambda instance, x: setattr(self.dropdown, "width", x))

    def on_message(self, instance):
        if instance.text in self.item_names:
            MDApp.get_running_app().commandprocessor("!hint "+instance.text)
        elif instance.text in self.location_names:
            MDApp.get_running_app().commandprocessor("!hint_location "+instance.text)
        self.item_names = []
        self.location_names = []

    def on_text(self, instance, value):
        if len(value) >= self.min_chars:
            self.dropdown.items.clear()
            ctx = MDApp.get_running_app().ctx
            if not ctx.game:
                return
            self.item_names = ctx.item_names._game_store[ctx.game].values()
            self.location_names = ctx.location_names._game_store[ctx.game].values()

            def on_press(text):
                split_text = Label(text=text).markup
                self.set_text(self, "".join(text_frag for text_frag in split_text
                                            if not text_frag.startswith("[")))
                self.dropdown.dismiss()
                self.focus = True

            lowered = value.lower()
            for hint_name in self.item_names + self.location_names:
                try:
                    index = hint_name.lower().index(lowered)
                except ValueError:
                    pass  # substring not found
                else:
                    text = escape_markup(hint_name)
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

class HintScreen(MDScreen):
    pass

class HintLayout(MDBoxLayout):
    """Layout container for hint input and display components.
    
    This class provides a vertical layout that contains the hint input
    field and related components for the hint system interface.
    
    Attributes:
        orientation (str): Layout orientation, set to "vertical"
    """
    orientation = "vertical"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        boxlayout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40))
        boxlayout.add_widget(MDLabel(text="New Hint:", size_hint_x=None, size_hint_y=None,
                                     height=dp(40), width=dp(75), halign="center", valign="center"))
        #boxlayout.add_widget(AutocompleteHintInput())
        self.add_widget(boxlayout)

    def fix_heights(self):
        for child in self.children:
            fix_func = getattr(child, "fix_heights", None)
            if fix_func:
                fix_func()

mwggstatus_icons: typing.Dict[MWGGUIHintStatus, str] = {
    MWGGUIHintStatus.HINT_UNSPECIFIED: "",
    MWGGUIHintStatus.HINT_SHOP: "shop",
    MWGGUIHintStatus.HINT_GOAL: "flag_checkered",
    MWGGUIHintStatus.HINT_BK_MODE: "food"
}
"""Mapping of MWGG hint status values to their corresponding icon names."""

mwggstatus_names: typing.Dict[MWGGUIHintStatus, str] = {
    MWGGUIHintStatus.HINT_UNSPECIFIED: "",
    MWGGUIHintStatus.HINT_SHOP: "Shop",
    MWGGUIHintStatus.HINT_GOAL: "Goal",
    MWGGUIHintStatus.HINT_BK_MODE: "BK Mode",
}
"""Mapping of MWGG hint status values to their corresponding display names."""

mwggstatus_colors: typing.Dict[MWGGUIHintStatus, str] = {
    MWGGUIHintStatus.HINT_UNSPECIFIED: "",
    MWGGUIHintStatus.HINT_SHOP: "gray",
    MWGGUIHintStatus.HINT_GOAL: "gold",
    MWGGUIHintStatus.HINT_BK_MODE: "red",
}
"""Mapping of MWGG hint status values to their corresponding color names for display."""

status_icons = {
    HintStatus.HINT_NO_PRIORITY: "information",
    HintStatus.HINT_PRIORITY: "exclamation-thick",
    HintStatus.HINT_AVOID: "alert"
}
"""Mapping of hint status values to their corresponding icon names."""

status_names: typing.Dict[HintStatus, str] = {
    HintStatus.HINT_FOUND: "Found",
    HintStatus.HINT_UNSPECIFIED: "Unspecified",
    HintStatus.HINT_NO_PRIORITY: "No Priority",
    HintStatus.HINT_AVOID: "Avoid",
    HintStatus.HINT_PRIORITY: "Priority",
}
"""Mapping of hint status values to their human-readable display names."""

status_colors: typing.Dict[HintStatus, str] = {
    HintStatus.HINT_FOUND: "green",
    HintStatus.HINT_UNSPECIFIED: "white",
    HintStatus.HINT_NO_PRIORITY: "lightgray",
    HintStatus.HINT_AVOID: "salmon",
    HintStatus.HINT_PRIORITY: "gold",
}
"""Mapping of hint status values to their color names for display."""

status_sort_weights: dict[HintStatus | MWGGUIHintStatus, int] = {
    HintStatus.HINT_FOUND: 0,
    MWGGUIHintStatus.HINT_SHOP: 1,
    MWGGUIHintStatus.HINT_GOAL: 2,
    HintStatus.HINT_AVOID: 3,
    HintStatus.HINT_UNSPECIFIED: 4,
    MWGGUIHintStatus.HINT_UNSPECIFIED: 5,
    HintStatus.HINT_NO_PRIORITY: 6,
    HintStatus.HINT_PRIORITY: 7,
    MWGGUIHintStatus.HINT_BK_MODE: 8,
}
"""Mapping of hint status values to their sort weights for ordering hints."""

class HintLog(MDRecycleView):
    """Recyclable view for displaying and managing hint information.
    
    This class provides a table-like view for displaying hints with
    sortable columns and interactive functionality. It shows information
    about receiving player, item, finding player, location, entrance,
    and status for each hint.
    
    Attributes:
        header (dict): Header row configuration with column definitions
        data (list): List of hint data items to display
        sort_key (str): Current column used for sorting
        reversed (bool): Whether sorting is in reverse order
    """
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
    sort_key: str = ""
    reversed: bool = True

    def __init__(self, parser):
        super(HintLog, self).__init__()
        self.data = [self.header]
        self.parser = parser

    def refresh_hints(self, hints):
        if not hints:  # Fix the scrolling looking visually wrong in some edge cases
            self.scroll_y = 1.0
        data = []
        ctx = MDApp.get_running_app().ctx
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
                })},
                "entrance": {"text": self.parser.handle_node({"type": "color" if hint["entrance"] else "text",
                                                              "color": 'entrancecolor', "text": hint["entrance"]
                                                              if hint["entrance"] else "Vanilla"})},
                "status": {
                    "text": hint_status_node,
                    "hint": hint,
                },
            })

        data.sort(key=self.hint_sorter, reverse=self.reversed)
        for i in range(0, len(data), 2):
            data[i]["striped"] = True
        data.insert(0, self.header)
        self.data = data

    @staticmethod
    def hint_sorter(element: dict) -> str:
        return element["status"]["hint"]["status"]  # By status by default

class HintLabel(MDBoxLayout):
    """Recyclable label widget for displaying hint information in a table format.
    
    This class represents a single row in the hint log table, displaying
    information about hints including receiving player, item, finding player,
    location, entrance, and status. It supports selection, sorting, and
    status modification through dropdown menus.
    
    Attributes:
        selected (bool): Whether this hint row is currently selected
        striped (bool): Whether this row should have striped background
        index (int): The index of this item in the recycle view
        dropdown (MDDropdownMenu): Dropdown menu for status selection
    """
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
            status_button = MDDropDownItem(MDDropDownItemText(text=name), size_hint_y=None, height=dp(50))
            status_button.status = status
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
                        return
                    ctx = MDApp.get_running_app().ctx
                    if ctx.slot_concerns_self(self.hint["receiving_player"]):  # If this player owns this hint
                        # open a dropdown
                        self.dropdown.open()
                elif self.selected:
                    self.parent.clear_selection()
                else:
                    text = "".join((self.receiving_text, "\'s ", self.item_text, " is at ", self.location_text, " in ",
                                    self.finding_text, "\'s World", (" at " + self.entrance_text)
                                    if self.entrance_text != "Vanilla"
                                    else "", ". (", self.status_text.lower(), ")"))
                    temp = Label(text).markup
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
                    key = child.sort_key
                    if key == "status":
                        parent.hint_sorter = lambda element: status_sort_weights[element["status"]["hint"]["status"]]
                    # else:
                        # parent.hint_sorter = lambda element: (
                        #     remove_between_brackets.sub("", element[key]["text"]).lower()
                        # )
                    if key == parent.sort_key:
                        # second click reverses order
                        parent.reversed = not parent.reversed
                    else:
                        parent.sort_key = key
                        parent.reversed = False
                    MDApp.get_running_app().update_hints()

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        if self.index:
            self.selected = is_selected