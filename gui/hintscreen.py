from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty, StringProperty, DictProperty
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
from NetUtils import HintStatus
from .testdict import testdict
import typing

# Builder.load_string(
#     '''
#     <HintLayout>
#         orientation: "vertical"
#     '''
# )
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

status_icons = {
    HintStatus.HINT_NO_PRIORITY: "information",
    HintStatus.HINT_PRIORITY: "exclamation-thick",
    HintStatus.HINT_AVOID: "alert"
}

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
status_sort_weights: dict[HintStatus, int] = {
    HintStatus.HINT_FOUND: 0,
    HintStatus.HINT_UNSPECIFIED: 1,
    HintStatus.HINT_NO_PRIORITY: 2,
    HintStatus.HINT_AVOID: 3,
    HintStatus.HINT_PRIORITY: 4,
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
