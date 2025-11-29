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
from kivy.properties import ObjectProperty, NumericProperty
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList
from kivymd.uix.behaviors import CommonElevationBehavior
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
        size_hint: None,None
        size: dp(128), dp(80)
        pos_hint: {"x": 0, "top": 1}

<-HintListPanel>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    padding: dp(8),dp(4),dp(8),dp(4)
    id: game_item
    MDExpansionPanelHeader:
        padding: dp(8),0,dp(8),0
        radius: dp(8),0,dp(8),0
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
                padding: dp(12), 0, dp(12), dp(12)
                spacing: dp(8)


<RecycleExpansionPanelContent>:

# <HintListItem_Hidden@HintListItem>:
# <HintListItem_Finding@HintListItem>:
# <HintListItem_Receiving@HintListItem>:
'''

Builder.load_string(KV)

if typing.TYPE_CHECKING:
    from CommonClient import CommonContext

class HintFeaturebar(MDBoxLayout):
    """
    Feature bar for the hint screen.
    """
    pass

class RecycleExpansionPanelContent(RecycleBoxLayout):
    """
    Override to make the panel a recycle view
    Recycle view for the hint list panel.
    """
    pass
    # _panel = ObjectProperty(None, allownone=True)
    # _updating_height = False
    
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.bind(minimum_height=self._on_height_change, height=self._on_height_change)
    
    # def _on_height_change(self, instance, value):
    #     """Update panel's original content height when layout height changes"""
    #     # Prevent infinite loops by checking if we're already updating
    #     if self._updating_height:
    #         return
    #     if self._panel and hasattr(self._panel, '_update_original_content_height'):
    #         self._updating_height = True
    #         # Schedule on next frame to ensure height is fully calculated
    #         Clock.schedule_once(lambda dt: self._panel._update_original_content_height(self), 0)
    #         # Reset flag after a short delay
    #         Clock.schedule_once(lambda dt: setattr(self, '_updating_height', False), 0.1)

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
        finally:
            self._updating_hints = False

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
        scroll_height = 1/self.search_placeholder.height
        self.hint_scroll = MDScrollView(size_hint_y=self.size_hint_y-scroll_height, size_hint_x=1)
        # Add placeholder label for future search functionality
        placeholder_label = MDLabel(
            text="Search & Filter Options (Future Feature)"
        )

        self.show_all_hints_switch = MDSwitch(
            icon_inactive="eye-off",
            icon_active="eye",
            on_active=self.on_show_all_hints
        )
        
        self.refresh_button = MDIconButton(
            icon="refresh",
            on_release=self.on_refresh_hints
        )
        
        self.search_placeholder.add_widget(placeholder_label)
        self.search_placeholder.add_widget(self.show_all_hints_switch)
        self.search_placeholder.add_widget(self.refresh_button)

        self.add_widget(self.search_placeholder)
        self.add_widget(self.hint_scroll)

    def on_show_all_hints(self, instance, value):
        self.app.show_all_hints = value
    
    def on_refresh_hints(self, instance):
        """Refresh the hints list when refresh button is clicked"""
        # Get the hint screen from the app
        self.app.update_hints()

hint_icons: typing.Dict[str, str] = {
    "Finding": "map-pin",
    "Receiving": "map-clock-outline",
    "Hidden": "eye-off",
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
    HintStatus.HINT_NO_PRIORITY: "altimeter", #bottle-tonic
    HintStatus.HINT_PRIORITY: "baguette", #bottle-tonic-plus
    HintStatus.HINT_AVOID: "hand-middle-finger" #"sign-caution" #biohazard #bottle-tonic-skull
}
"""Mapping of hint status values to their corresponding icon names."""

status_names: typing.Dict[HintStatus, str] = {
    HintStatus.HINT_NO_PRIORITY: "Doesn't Matter",
    HintStatus.HINT_AVOID: "Don't Get This",
    HintStatus.HINT_PRIORITY: "This is Important",
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
        self.featurebar_height = featurebar_height
        self.hint_item_height = dp(72)  # TODO: screw hardcodingggggg (from expansionlist.kv)
        # GameListPanel requires item_name as first positional arg
        super().__init__(item_name=hint_type, item_data=item_data, *args, **kwargs)
        # Set properties after super().__init__() so widget tree is built
        self.panel_header_height = dp(50)
        self.content_height = dp(8)
        self.content_min_height = dp(96) # TODO: screw hardcodinggggggs (hint_item_height + spacing, padding, other random crap)
        self.padding = (dp(16), dp(16), dp(16), dp(16))
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
        self.panel_header_layout = HintListItemHeader(hint_icon=hint_icons[self.hint_type], hint_text=self.hint_type, panel=self, height=self.panel_header_height)
        
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
                        #  "for_bk_mode": hint.mwgg_hint_status & MWGGUIHintStatus.HINT_BK_MODE,
                        #  "for_goal": hint.mwgg_hint_status & MWGGUIHintStatus.HINT_GOAL,
                        #  "from_shop": hint.mwgg_hint_status & MWGGUIHintStatus.HINT_SHOP,
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
        # Force RecycleView to refresh and create widgets
        if self.hint_content:
            self.hint_content.refresh_from_data()
