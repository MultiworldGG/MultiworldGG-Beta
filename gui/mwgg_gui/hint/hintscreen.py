from __future__ import annotations

"""
HINT SCREEN

HintScreen - main screen for displaying hints
HintLayout - layout for the hint screen
HintListPanel - panel for displaying hint information
"""
__all__ = ("HintScreen", "HintLayout", "HintListPanel", "HintFeaturebar")

from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.metrics import dp
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty, DictProperty
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.chip import MDChip, MDChipText
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList
from kivymd.uix.behaviors import CommonElevationBehavior
from kivy.uix.recycleview import RecycleDataModel, RecycleDataModelBehavior, RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from NetUtils import HintStatus, MWGGUIHintStatus, TEXT_COLORS
from mwgg_gui.overrides.expansionlist import HintListItem, IconBadge, HintListItemHeader, GameListPanel, HintListDropdown
from mwgg_gui.components.guidataclasses import UIHint
from mwgg_gui.components.bottomappbar import BottomAppBar
from mwgg_gui.components.mw_theme import AutoAdjustHeightBehavior, md_icons

import typing
import asynckivy

KV = '''
#:import os os
<HintFeaturebar>:
    FitImage:
        source: os.path.join(os.getenv("KIVY_DATA_DIR"), "images", "logo_bg.png")
        size_hint: None, None
        height: root.height
        mode: "contain"
        pos_hint: {"x": 0, "top": 1}

<RDMSearchChips>:
    orientation: "horizontal"
    spacing: dp(12)
    size_hint_x: 1
    size_hint_y: None
    height: self.minimum_height
    chips: []
    recycleview: app.hint_screen.filter_chip_box

<RVSearchChips>:
    viewclass: "RDMSearchChips"
    remaining_chips: []
    size_hint_x: 1
    size_hint_y: None
    height: dp(80)
    RecycleBoxLayout:
        id: rv_layout
        orientation: "vertical"
        default_size: None, dp(40)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        spacing: dp(1)
        padding: dp(8), 0, dp(8), 0

<-HintListPanel>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    padding: dp(8),dp(4),dp(8),dp(4)
    id: game_item
    MDExpansionPanelHeader:
        padding: dp(8),0,dp(8),0
        radius: dp(16)
        height: root.panel_header_height
        id: panel_header
    MDExpansionPanelContent:
        id: panel_content
        orientation: 'vertical'
        height: root.content_height
        padding: dp(12), 0, dp(12), dp(12)
        spacing: dp(8)
        MDLabel:
            height: 0
            size_hint_y: None
            padding: 0
        RecycleView:
            id: rv
            viewclass: "HintListItem_"+root.hint_type
            RecycleExpansionPanelContent:
                id: recycle_layout
                orientation: 'vertical'
                default_size: None, dp(72)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                padding: dp(8), dp(0), dp(8), dp(0)
                spacing: dp(8)


<RecycleExpansionPanelContent>:

'''

Builder.load_string(KV)

if typing.TYPE_CHECKING:
    from CommonClient import CommonContext

class HintFeaturebar(MDBoxLayout):
    """
    Feature bar for the hint screen.
    """
    pass

class MDChip(MDChip):
    '''
    Override to toggle active state on press instead of long press
    '''
    def on_release(self, *args) -> None:
        """Toggle active state on release for filter chips"""
        if self.type == "filter":
            self.active = not self.active
        self._on_release(args)

    def on_press(self, *args) -> None:
        """Call parent's on_press to maintain other behaviors"""
        self._on_press(args)

class RVSearchChips(RecycleDataViewBehavior, RecycleView):
    remaining_chips = DictProperty(default_factory=lambda: {"chips": [], "width": None})
    # viewclass can be string or class object - will be set to class object after definition
    hint_layout = ObjectProperty(None, allownone=True)

class RDMSearchChips(RecycleDataModelBehavior, MDBoxLayout):
    """Recyclable BoxLayout for search filter chips.
    
    Each instance represents a row of chips that fit within the available width.
    Chips that don't fit are stored in remaining_chips for the next row.
    """
    chips = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.bind(width=self.on_width)
        self.size_hint_x = 1
        self.size_hint_y = None
        self.fbind('chips', self._create_chips)
    
    def _create_chips(self, instance=None, chips: list[MDChip] = []):
        """Create chips and add them to the layout
        instance: The instance of the RDMSearchChips
        chips: The list of chips to create
        """
        chips_width = 0
        if self.width > dp(100):
            self.clear_widgets()
            # Check if we're in a refresh cycle to prevent recursion
            hint_layout = getattr(self.recycleview, 'hint_layout', None)
            is_refreshing = getattr(hint_layout, '_refreshing_chips', False) if hint_layout else False
            
            for i, chip in enumerate(self.chips):
                chips_width += chip.width + self.spacing # chip icon width
                if chips_width > self.width:
                    # Only set remaining_chips if not already refreshing
                    if not is_refreshing:
                        self.recycleview.remaining_chips = {"chips": self.chips[i:], "width": self.width}
                    break
                else:
                    if chip.parent is not None:
                        chip.parent.remove_widget(chip)
                    self.add_widget(chip)

    def refresh_view_attrs(self, rv, index, data):
        """Update view when RecycleView data changes - this is called by RecycleView when creating/updating views"""
        self.index = index
        # Set chips from data dict
        self.chips = data.get("chips", [])

        super().refresh_view_attrs(rv, index, data)

    def on_width(self, instance, value):
        """Handle width changes - not used for fitting logic, but kept for compatibility"""
        self._create_chips(instance=instance, chips=self.chips)

class RecycleExpansionPanelContent(RecycleBoxLayout):
    """
    Override to make the panel a recycle view
    Recycle view for the hint list panel.
    """
    pass

class HintListItem_Hidden(HintListItem):
    pass

class HintListItem_Finding(HintListItem):
    pass

class HintListItem_Receiving(HintListItem):
    pass

class HintScreen(MDScreen):
    '''
    This is the main screen for displaying hints.
    It includes a top app bar, hint list panel, and bottom app bar.
    Takes full window width
    '''
    name = "hint"
    bottom_appbar: BottomAppBar
    hint_layout: "HintLayout"
    hints_by_type: dict[str, list[(int, str, UIHint)]]
    app: MDApp
    _updating_hints: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.size = (Window.width, Window.height-185)
        
        # Initialize components
        self.bottom_appbar = BottomAppBar(screen_name="hint")
        self.hint_layout = HintLayout()
        self.filter_chip_box = self.hint_layout.filter_chip_box
        self.hint_scroll = self.hint_layout.hint_scroll
        self.hints_mdlist = MDList(size_hint_y=None, size_hint_x=1)
        # Schedule initialization
        Clock.schedule_once(lambda x: self.init_components())

    def populate_hints_by_type(self):
        """Initialize and add all components to the screen"""
        # Clear existing data to prevent duplicates on refresh
        self.hints_by_type = {"Hidden": [], "Receiving": [], "Finding": []}
        # Reorganizing hints for the hint screen
        for slot_id, slot_data in self.app.ctx.ui.ui_player_data.items():
            if hasattr(slot_data, 'hints') and slot_data.hints:
                for hint in slot_data.hints.values():
                    if hint.hint_status == HintStatus.HINT_FOUND or hint.found:
                        hint.hide = True
                    if slot_id == self.app.ctx.slot:
                        if hint.hide:
                            self.hints_by_type["Hidden"].append((slot_id, slot_data, hint))
                        else:
                            self.hints_by_type["Receiving"].append((slot_id, slot_data, hint))
                            self.hints_by_type["Finding"].append((slot_id, slot_data, hint))
                    else:
                        if hint.hide:
                            self.hints_by_type["Hidden"].append((slot_id, slot_data, hint))
                        elif hint.my_item:
                            self.hints_by_type["Receiving"].append((slot_id, slot_data, hint))
                        else:
                            self.hints_by_type["Finding"].append((slot_id, slot_data, hint))

    def init_components(self):
        # Add components to the screen
        self.add_widget(self.hint_layout)
        self.add_widget(self.bottom_appbar)
        
        # Add hints list to the hint layout (after the search placeholder)
        self.hint_scroll.add_widget(self.hints_mdlist)

    def update_hints_list(self):
        """Update the hints list when hint data becomes available"""
        if not self._updating_hints:
            asynckivy.start(self.set_hints_list())

    async def set_hints_list(self):
        """Async method to populate the hints list"""
        if self._updating_hints:
            return  # Prevent concurrent updates
            
        self._updating_hints = True
        self.populate_hints_by_type()
        try:
            self.hints_mdlist.clear_widgets()
            await asynckivy.sleep(0)  # Allow UI to process the clear

            for hint_type in hint_icons.keys():  
                await asynckivy.sleep(0)  # Yield control for smooth UI
                hint_panel = HintListPanel(
                    hint_type=hint_type, 
                    item_data=self.hints_by_type[hint_type],
                    hint_layout=self.hint_layout,
                    featurebar_height=self.hint_layout.search_placeholder.height
                )
                self.hints_mdlist.add_widget(hint_panel)
            
            # Store reference to hint_screen in hint_layout for sorting
            self.hint_layout._hint_screen_ref = self
            
            # Apply current sort if one is active
            if self.hint_layout.active_sort_key:
                self.hint_layout.apply_sort_to_all_panels(self.hint_layout.active_sort_key)
        finally:
            self._updating_hints = False

FILTER_CHIPS = [
            {"filter_text": "All", "sort_key": "", "active": True},
            {"filter_text": "Player", "sort_key": "player_name", "active": False},
            {"filter_text": "Item", "sort_key": "item_name", "active": False},
            {"filter_text": "Location", "sort_key": "location_name", "active": False},
            {"filter_text": "Entrance", "sort_key": "entrance_name", "active": False},
            {"filter_text": "BK Mode", "sort_key": "for_bk_mode", "active": False},
            {"filter_text": "Goal", "sort_key": "for_goal", "active": False},
            {"filter_text": "Shop", "sort_key": "from_shop", "active": False},
]

class HintLayout(AutoAdjustHeightBehavior, MDBoxLayout):
    """Layout container for hint display components.
    
    This class provides a vertical layout that contains the placeholder
    for future search functionality and the hint list display.
    Takes full window width with no sidebar.
    
    Attributes:
        orientation (str): Layout orientation, set to "vertical"
        search_placeholder (MDBoxLayout): Placeholder for future search features
    """
    adjust_title_bar = True
    adjust_app_bar = True
    adjust_bottom_appbar = True
    adjust_custom = 0
    
    orientation = "vertical"
    app: MDApp
    hint_scroll: MDScrollView
    active_sort_key = StringProperty("")
    active_filter_text = StringProperty("")  # Store selected filter_text (e.g., player name)
    sort_reverse = False  # Toggle for reverse sort direction
    _default_filter_chips:  list[MDChip] = []
    _search_width = NumericProperty(dp(100))
    _hint_screen_ref: ObjectProperty = None
    _refreshing_chips = False  # Guard flag to prevent recursive refresh calls
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
        self.y = 82
        # Create placeholder for future search and filter functionality
        self.search_placeholder = HintFeaturebar(
            height=dp(80),
            size_hint_y=None,
            size_hint_x=1,
            orientation="horizontal",
            spacing=dp(16),
            padding=[dp(16), dp(8), dp(16), dp(8)]
        )
        # self.search_placeholder.bind(height=self.on_search_placeholder_height_changed)
        scroll_height = 1/self.search_placeholder.height
        self.hint_scroll = MDScrollView(size_hint_y=self.size_hint_y-scroll_height, 
                                        size_hint_x=1,
                                        bar_width=dp(4))
        for chip_data in FILTER_CHIPS:
            chip = MDChip(MDChipText(text = chip_data["filter_text"]),
                                             type="filter", 
                                             pos_hint={"x": 0, "center_y": 0.5}, 
                                             active=chip_data["active"])
            chip.bind(active=lambda inst, value, chip_data=chip_data: self.on_filter_chip_selected(value, chip_data))

            self._default_filter_chips.append(chip)
        self.search_placeholder.bind(width=self.on_search_width_changed)

        self.filter_chip_box = RVSearchChips()
        self.filter_chip_box.hint_layout = self
        # Set viewclass to the actual class object, not string
        # This must be done after RDMSearchChips is defined
        self.filter_chip_box.viewclass = RDMSearchChips
        self.search_placeholder.add_widget(self.filter_chip_box)
        # Set "All" as default selected
        self.filter_chip_box.bind(remaining_chips=self.on_remaining_chips_changed)
        Clock.schedule_once(lambda x: self.add_chips(filter_data=self._default_filter_chips.copy(), width=self._search_width), 0)

        self.action_box = MDGridLayout(
            width=dp(128),
            size_hint_x=None,
            cols=2,
            spacing=dp(4),
            padding=dp(0)
        )
        self.action_box.add_widget(MDSwitch(
            icon_inactive="eye-off",
            icon_active="eye",
            size_hint_x=.5,
            on_active=self.on_show_all_hints
        ))
                
        self.action_box.add_widget(MDSwitch(
            icon_inactive="sort-ascending",
            icon_active="sort-descending",
            size_hint_x=.5,
            on_active=self.on_sort_reverse
        ))
        self.action_box.add_widget(MDIconButton(
            icon="refresh",
            size_hint_x=.5,
            on_release=self.on_refresh_hints
        ))

        # self.search_placeholder.add_widget(placeholder_label)
        self.search_placeholder.add_widget(self.action_box)

        self.add_widget(self.search_placeholder)
        self.add_widget(self.hint_scroll)

    def add_chips(self, filter_data: list[MDChip], width: int):
        if self._refreshing_chips:
            return
        self._refreshing_chips = True
        if filter_data:
            # Replace data instead of appending to ensure single row
            self.filter_chip_box.data = [{"chips": filter_data, "width": width}]
            self.filter_chip_box.refresh_from_data()
        else:
            # Clear data if no chips
            self.filter_chip_box.data = []
            self.filter_chip_box.refresh_from_data()
        Clock.schedule_once(lambda dt: setattr(self, '_refreshing_chips', False), 0.1)
    
    def on_remaining_chips_changed(self, instance, value):
        """Handle when remaining chips are detected - add a new row
        current data: [{"chips": [MDChip, MDChip, MDChip], "width": dp(100)}{...}]
             This is the set of data that is already in the recycle view and not clipped
             We will be truncating the chip list, so that only the chips that fit are in the 
             data dictionary.
        value: {"chips": [MDChip, MDChip, MDChip], "width": int}
            This is the set of chips that are remaining and need to be placed in a new row
        """
        if self._refreshing_chips or not value:
            return
        self._refreshing_chips = True
        truncated_chips = self.filter_chip_box.data[-1]["chips"][len(value["chips"]):]
        new_data = self.filter_chip_box.data[:len(self.filter_chip_box.data)-1] or []
        new_data.append({"chips": truncated_chips, "width": value["width"]})
        new_data.append(value)

        self.filter_chip_box.data = new_data
        self.filter_chip_box.refresh_from_data()
        Clock.schedule_once(lambda dt: setattr(self, '_refreshing_chips', False), 0.1)

    def on_search_width_changed(self, instance, value):
        self._search_width = dp(100) if not value > dp(308) else value - dp(208)

    # def on_filter_chip_data_changed(self, instance, value):
    #     """Handle filter chip data changed"""
    #     for chip in value:
    #         if chip["active"]:
    #             self.active_filter_text = chip["filter_text"]
    #             self.active_sort_key = chip["sort_key"]
    #             break

    # def on_search_placeholder_height_changed(self, instance, value):
    #     if value > dp(100):
    #         self.filter_chip_box.rows = int(value/dp(30))
    #     else:
    #         self.filter_chip_box.rows = 2

    def on_show_all_hints(self, instance, value):
        self.app.show_all_hints = value
    
    def on_refresh_hints(self, instance):
        """Refresh the hints list when refresh button is clicked"""
        # Get the hint screen from the app
        self.app.update_hints()
    
    def on_sort_reverse(self, instance, value):
        """Handle sort reverse toggle"""
        self.sort_reverse = value
        if self.active_sort_key:
            self.apply_sort_to_all_panels(self.active_sort_key)

    def on_filter_chip_selected(self, active: bool, chip_data: dict):
        """Handle filter chip selection - update sort key and apply sorting"""
        if self._refreshing_chips:
            return

        self.active_sort_key = chip_data["sort_key"]
        self.active_filter_text = chip_data["filter_text"]

        self._refreshing_chips = True
        if self.active_filter_text == "Player":
            # Create new chips list with player chips - create new instances to avoid modifying originals
            new_chips = self.filter_chip_box.data[-1]["chips"]
            # Add player chips
            for slot_id, player in self.app.ctx.ui.ui_player_data.items():
                chip = MDChip(MDChipText(text = player.slot_name),
                    type="filter",
                    pos_hint={"x": 0, "center_y": 0.5},
                    active=False)
                chip.bind(active=lambda inst, value, chip_data={"filter_text": player.slot_name, "sort_key": "player_name", "active": False}: self.on_filter_chip_selected(value, chip_data))
                new_chips.append(chip)
            # Update RecycleView data and refresh
            self.filter_chip_box.data[-1]["chips"] = new_chips
            self.filter_chip_box.refresh_from_data()
        else:
            # Reset to default filter chips - create new instances
            # This handles "All" and other non-player filter chips
            self.filter_chip_box.data = [{"chips": self._default_filter_chips.copy(), "width": self._search_width}]
            self.filter_chip_box.refresh_from_data()
        Clock.schedule_once(lambda dt: setattr(self, '_refreshing_chips', False), 0.1)
 
        # Apply sorting to all panels
        self.apply_sort_to_all_panels(self.active_sort_key)
    
    def _get_status_sort_weight(self, hint_item: dict) -> int:
        """Get the status sort weight for a hint item"""
        hint = hint_item.get("hint_data")
        if not hint:
            return 999  # Default to end if no hint data
        
        hint_status = getattr(hint, 'hint_status', HintStatus.HINT_UNSPECIFIED)

        # Check if hint is found first (highest priority for sorting)
        if getattr(hint, 'found', False) or getattr(hint, 'hint_status', hint_status) == HintStatus.HINT_FOUND:
            return status_sort_weights[HintStatus.HINT_FOUND]
        
        # Get MWGG flags weight by iterating through flags
        mwgg_status = getattr(hint, 'mwgg_hint_status', None)
        status_weight = 999
        if mwgg_status:
            # These are different sizes, but it will leave off HINT_FOUND which we've already checked
            for mwgg_hint, hint in zip(MWGGUIHintStatus, HintStatus):
                mw = mwgg_status & mwgg_hint
                hw = hint_status & hint
                if mw or hw:
                    status_weight = min(status_weight, min(status_sort_weights[hint], status_sort_weights[mwgg_hint]))
        return min(status_weight, status_sort_weights[HintStatus.HINT_FOUND])
    
    def apply_sort_to_all_panels(self, sort_key: str):
        """Apply sorting to all HintListPanel RecycleViews"""
        if not self._hint_screen_ref:
            return
        
        # Find all HintListPanel widgets in the hints_mdlist
        for panel in self._hint_screen_ref.hints_mdlist.children:
            if isinstance(panel, HintListPanel) and hasattr(panel, 'hint_content'):
                self._sort_panel_data(panel, sort_key)
    
    def _sort_panel_data(self, panel: "HintListPanel", sort_key: str):
        """Sort the data in a specific panel's RecycleView with simplified logic"""
        if not panel.hint_content or not panel.hint_content.data:
            return
        
        hint_items = panel.hint_content.data.copy()
        
        # Define key functions for each sort type
        key_functions = {
            "player_name": lambda item: item.get("player_name", "").lower(),
            "item_name": lambda item: item.get("item_name", "").lower(),
            "location_name": lambda item: item.get("location_name", "").lower(),
            "entrance_name": lambda item: item.get("entrance_name", "").lower(),
            "for_bk_mode": lambda item: not item.get("for_bk_mode", False),  # True first
            "for_goal": lambda item: not item.get("for_goal", False),  # True first
            "from_shop": lambda item: not item.get("from_shop", False),  # True first
        }
        
        # Get secondary key function
        secondary_key = key_functions.get(sort_key) if sort_key else None
        
        # Determine if we're filtering by a specific value (e.g., specific player name)
        # When a specific player chip is clicked, prioritize that player's items first
        filter_value = self.active_filter_text if sort_key == "player_name" and self.active_filter_text and self.active_filter_text != "Player" else None
        
        def sort_key_func(item: dict):
            """Create sort key function with priority, status, and sort_key"""
            # Priority: If filtering by specific player name, matching items come first
            priority = 0
            if filter_value:
                item_player = item.get("player_name", "")
                if item_player.lower() != filter_value.lower():
                    priority = 1  # Non-matching items go after matching ones
            
            # Primary sort: status_weight (always used, lower = higher priority)
            status_weight = self._get_status_sort_weight(item)
            
            # Secondary sort: selected sort_key (if any)
            if secondary_key:
                sort_value = secondary_key(item)
                return (priority, status_weight, sort_value)
            else:
                return (priority, status_weight)
        
        # Sort with optional reverse
        sorted_items = sorted(hint_items, key=sort_key_func, reverse=self.sort_reverse)
        
        # Update the RecycleView data
        panel.hint_content.data = sorted_items
        panel.hint_content.refresh_from_data()

hint_icons: typing.Dict[str, str] = {
    "Finding": ["Items to Get from My World", "map_pin"],
    "Receiving": ["What I need from other Worlds", "map-clock-outline"],
    "Hidden": ["Hidden Items", "eye-off"],
}

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
    MWGGUIHintStatus.HINT_SHOP: TEXT_COLORS["regular_item_color"],
    MWGGUIHintStatus.HINT_GOAL: TEXT_COLORS["progression_item_color"],
    MWGGUIHintStatus.HINT_BK_MODE: TEXT_COLORS["trap_item_color"],
}
"""Mapping of MWGG hint status values to their corresponding color names for display."""

status_icons = {
    HintStatus.HINT_NO_PRIORITY: "peace", #bottle-tonic altimeter
    HintStatus.HINT_PRIORITY: "key-variant", #bottle-tonic-plus heart
    HintStatus.HINT_AVOID: "hand_middle_finger" #"sign-caution" #biohazard #bottle-tonic-skull
}
"""Mapping of hint status values to their corresponding icon names."""

status_names: typing.Dict[HintStatus, str] = {
    HintStatus.HINT_NO_PRIORITY: "",
    HintStatus.HINT_AVOID: "Avoid",
    HintStatus.HINT_PRIORITY: "Important",
}
"""Mapping of hint status values to their human-readable display names."""

status_colors: typing.Dict[HintStatus, str] = {
    HintStatus.HINT_NO_PRIORITY: TEXT_COLORS["regular_item_color"],
    HintStatus.HINT_AVOID: TEXT_COLORS["trap_item_color"],
    HintStatus.HINT_PRIORITY: TEXT_COLORS["progression_item_color"],
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

class HintListPanel(GameListPanel):
    """
    Expansion panel for displaying hint information in the hint list.
    
    This class is used to display a set of "finding", "receiving", "hidden" hints.
    """
    content_height = NumericProperty(dp(8))
    panel_header_height = NumericProperty(dp(50))

    def __init__(self, hint_type: str, item_data, hint_layout=None, featurebar_height=dp(80), *args, **kwargs):
        # Set hint_type before super().__init__() so KV can access it
        self.hint_type = hint_type
        # Store references for height calculations
        self.hint_layout = hint_layout
        self.hint_filter_chip_box = hint_layout.filter_chip_box
        self.featurebar_height = featurebar_height
        self.hint_item_height = dp(72)  # TODO: screw hardcodingggggg (from expansionlist.kv)
        # GameListPanel requires item_name as first positional arg
        super().__init__(item_name=hint_type, item_data=item_data, *args, **kwargs)
        # Set properties after super().__init__() so widget tree is built
        self.panel_header_height = dp(50)
        self.content_height = dp(8)
        self.content_min_height = dp(96) # TODO: screw hardcodinggggggs (hint_item_height + spacing, padding, other random crap)
        self.spacing = dp(8)
        self._populated = False
        Clock.schedule_once(lambda x: self.populate_slot_item(self.app.ctx), 0)
        
        # Bind to layout height changes for height recalculation
        if self.hint_layout:
            self.hint_layout.bind(height=self._on_layout_height_changed)
    
    def populate_game_item(self):
        """Override to prevent GameListPanel from trying to populate game data"""
        # HintListPanel uses populate_slot_item instead
        pass
    
    def _calculate_content_height(self):
        """Calculate content height based on hint count and available space"""
        # Get hint count from RecycleView data
        hint_count = len(self.hint_content.data) if hasattr(self, 'hint_content') and self.hint_content and self.hint_content.data else 0
        
        # Calculate height needed for all hints
        hints_height = hint_count * (self.hint_item_height + self.spacing) + self.padding[0] + self.padding[2]
        
        # Calculate maximum available height
        if self.hint_layout:
            max_height = self.hint_layout.height - self.featurebar_height - self.panel_header_height
        else:
            # Fallback to Window height if hint_layout not available
            max_height = Window.height - self.featurebar_height - self.panel_header_height
        
        # Use minimum of hints height and max available height
        calculated_height = min(hints_height, max_height) if max_height > 0 else self.content_min_height
        
        # Ensure minimum height
        return max(calculated_height, dp(8))
    
    def _set_content_height(self, *args):
        """Override to calculate content height based on hint count"""
        calculated_height = self._calculate_content_height()
        self._original_content_height = calculated_height
        self._content.height = 0

    def _update_original_content_height(self, widget):
        """Override to recalculate content height when data or layout changes"""
        calculated_height = self._calculate_content_height()
        self._original_content_height = calculated_height
    
    def _on_data_changed(self, instance, value):
        """Recalculate height when hint data changes"""
        if self.is_open:
            Clock.schedule_once(lambda dt: self._update_original_content_height(None), 0.1)
    
    def _on_layout_height_changed(self, instance, value):
        """Recalculate height when layout height changes"""
        if self.is_open:
            Clock.schedule_once(lambda dt: self._update_original_content_height(None), 0.1)

    def populate_slot_item(self, ctx: "CommonContext"):
        """
        Populate the panel with slot items when hints are present.
        
        This method sets up the panel to display slot information
        including the header with avatar and slot items for each hint.
        """
        
        # Guard against multiple population
        if self._populated:
            return
        self._populated = True

        def on_select_status(hint: UIHint, status: HintStatus):
            hint.set_status(hint_status=status)

        hint_items = []
        self.panel_header = self.ids.panel_header
        self.panel_content = self.ids.panel_content
        self.hint_content = self.ids.rv
        self.panel_header_layout = HintListItemHeader(hint_icon=hint_icons[self.hint_type][1], 
                                                      hint_text=hint_icons[self.hint_type][0], 
                                                      panel=self, 
                                                      height=self.panel_header_height)
        
        # Set up bindings for height recalculation after hint_content is available
        if self.hint_content:
            self.hint_content.bind(data=self._on_data_changed)
        # self.leading_avatar = self.panel_header_layout.ids.leading_avatar
        self.panel_header.add_widget(self.panel_header_layout)
        # self.leading_avatar.source = "" if not self.item_data['avatar'] else self.item_data['avatar']

        i = 1 if self.app.theme_cls.theme_style == "Dark" else 0
        item_bg_color = self.app.theme_cls.surfaceContainerColor
        item_colors = {
            "trap": get_color_from_hex(self.app.theme_mw.markup_tags_theme.trap_item_color[i]),
            "regular": get_color_from_hex(self.app.theme_mw.markup_tags_theme.regular_item_color[i]),
            "useful": get_color_from_hex(self.app.theme_mw.markup_tags_theme.useful_item_color[i]),
            "progression_deprioritized": get_color_from_hex(self.app.theme_mw.markup_tags_theme.progression_deprioritized_item_color[i]),
            "progression": get_color_from_hex(self.app.theme_mw.markup_tags_theme.progression_item_color[i]),
            "progression_goal": get_color_from_hex(self.app.theme_mw.markup_tags_theme.progression_goal_item_color[i]),
        }

        def get_prio_behavior(classification: str):
            behavior = {"elevation_level": 0, "shadow_color": item_colors["regular"]}
            if classification == "Trap":
                behavior["elevation_level"] = 1
                behavior["shadow_color"] = item_colors["trap"]
            if classification == "Filler":
                behavior["elevation_level"] = 2
                behavior["shadow_color"] = item_colors["regular"]
            if classification == "Useful":
                behavior["elevation_level"] = 3
                behavior["shadow_color"] = item_colors["useful"]
            if classification == "Progression - Logically Relevant":
                behavior["elevation_level"] = 4
                behavior["shadow_color"] = item_colors["progression_deprioritized"]
            if classification == "Progression":
                behavior["elevation_level"] = 5
                behavior["shadow_color"] = item_colors["progression"]
            if classification == "Progression - Requried for Goal":
                behavior["elevation_level"] = 6
                behavior["shadow_color"] = item_colors["progression_goal"]
            if classification == "Found":
                behavior["elevation_level"] = 0
                behavior["shadow_color"] = item_colors["regular"]
            return behavior

        for slot_id, slot_data, hint in self.item_data:
            
            item_badge_text = ""
            location_badge_text = ""
            prio_behavior = get_prio_behavior(hint.classification)
            if not hint.my_item:
                if hint.mwgg_hint_status & MWGGUIHintStatus.HINT_BK_MODE:
                    item_badge_text += md_icons["food"] + " "
                if hint.mwgg_hint_status & MWGGUIHintStatus.HINT_GOAL:
                    item_badge_text += md_icons["flag_checkered"] + " "
                if hint.mwgg_hint_status & MWGGUIHintStatus.HINT_SHOP:
                    location_badge_text += md_icons["shop"]

            hint_item = {"player_name": slot_data.slot_name, 
                         "player_avatar": slot_data.avatar, 
                         "location_name": hint.location, 
                         "item_name": hint.item, 
                         "entrance_name": hint.entrance if hint.entrance else "Vanilla",
                         "game_status": slot_data.game_status, 
                         "item_badge_text": item_badge_text, 
                         "location_badge_text": location_badge_text,   
                         "hint_icon_status": status_icons.get(hint.hint_status, "blank"), 
                         "hint_status_text": status_names.get(hint.hint_status, ""),
                         "for_bk_mode": hint.for_bk_mode,
                         "for_goal": hint.for_goal,
                         "from_shop": hint.from_shop,
                         "hint_data": hint,
                         "hide": hint.hide if hasattr(hint, 'hide') else False,
                         "md_bg_color": item_bg_color,
                         "shadow_color": prio_behavior["shadow_color"],
                         "elevation_level": prio_behavior["elevation_level"],
                         }
            # Only add editable flag for non-found items (dropdown created in refresh_view_attrs)
            if not (hint.hint_status == HintStatus.HINT_FOUND or hint.found or not hint.my_item):
                hint_item["editable"] = True
                hint_item["bk_check"] = hint.for_bk_mode
                hint_item["goal_check"] = hint.for_goal
                hint_item["shop_check"] = hint.from_shop
            else:
                hint_item["editable"] = False
                hint_item["bk_icon"] = "food" if hint.for_bk_mode else "blank"
                hint_item["goal_icon"] = "flag_checkered" if hint.for_goal else "blank"
                hint_item["shop_icon"] = "shop" if hint.from_shop else "blank"

            hint_items.append(hint_item)

        self.hint_content.data = hint_items
        
        # Apply sorting if hint_layout has an active sort key
        if self.hint_layout and self.hint_layout.active_sort_key:
            self.hint_layout._sort_panel_data(self, self.hint_layout.active_sort_key)
        
        # Force RecycleView to refresh and create widgets
        if self.hint_content:
            self.hint_content.refresh_from_data()

