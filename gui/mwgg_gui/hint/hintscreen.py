from __future__ import annotations
"""
HINT SCREEN

HintScreen - main screen for displaying hints
HintLayout - layout for the hint screen
HintListPanel - panel for displaying hint information
"""
__all__ = ("HintScreen", "HintLayout", "HintListPanel", "HintFeaturebar")

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import BaseListItemIcon, MDList
from NetUtils import HintStatus, MWGGUIHintStatus, TEXT_COLORS
from mwgg_gui.overrides.expansionlist import HintListItem, IconBadge, SlotListItemHeader, GameListPanel, HintListDropdown
from mwgg_gui.components.guidataclasses import UIHint
from mwgg_gui.components.bottomappbar import BottomAppBar
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
'''

Builder.load_string(KV)

if typing.TYPE_CHECKING:
    from CommonClient import CommonContext

class HintFeaturebar(MDBoxLayout):
    """
    Feature bar for the hint screen.
    """
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
        self.hints_mdlist = MDList()
        # Schedule initialization
        Clock.schedule_once(lambda x: self.init_components())

    def init_components(self):
        """Initialize and add all components to the screen"""
        # Add components to the screen
        self.add_widget(self.hint_layout)
        self.add_widget(self.bottom_appbar)
        
        # Set up hint layout positioning and sizing to take full window width
        self.hint_layout.y = dp(82)  # Account for bottom app bar # Account for top and bottom bars
        self.hint_layout.size_hint = (1, 1)
        
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
        try:
            self.hints_mdlist.clear_widgets()
            await asynckivy.sleep(0)  # Allow UI to process the clear
            
            for slot_id, slot_data in self.app.ctx.ui.ui_player_data.items():
                if hasattr(slot_data, 'hints') and slot_data.hints:
                    await asynckivy.sleep(0)  # Yield control for smooth UI
                    hint_panel = HintListPanel(item_name=slot_id, item_data=slot_data)
                    self.hints_mdlist.add_widget(hint_panel)
        finally:
            self._updating_hints = False

class HintLayout(MDBoxLayout):
    """Layout container for hint display components.
    
    This class provides a vertical layout that contains the placeholder
    for future search functionality and the hint list display.
    Takes full window width with no sidebar.
    
    Attributes:
        orientation (str): Layout orientation, set to "vertical"
        search_placeholder (MDBoxLayout): Placeholder for future search features
    """
    orientation = "vertical"
    app: MDApp
    hint_scroll: MDScrollView

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
        self.hint_scroll = MDScrollView(size_hint_y=.9, size_hint_x=1)
        # Create placeholder for future search and filter functionality
        self.search_placeholder = HintFeaturebar(
            size_hint_y=.1,
            orientation="horizontal",
            spacing=dp(16),
            padding=[dp(16), dp(8), dp(16), dp(8)]
        )
        
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
        # Add the placeholder to the layout
        self.add_widget(self.search_placeholder)
        self.add_widget(self.hint_scroll)

    def on_show_all_hints(self, instance, value):
        self.app.show_all_hints = value
    
    def on_refresh_hints(self, instance):
        """Refresh the hints list when refresh button is clicked"""
        # Get the hint screen from the app
        hint_screen = self.app.screen_manager.get_screen("hint")
        hint_screen.update_hints_list()

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
    
    This class is used to display a hint item in the hint list.
    It is a subclass of GameListPanel and can display either
    slot items (if hints are present) or game metadata.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.padding = (dp(16), dp(16), dp(16), dp(16))
        self.spacing = dp(8)
        self._populated = False
        Clock.schedule_once(self.populate_slot_item, 0)

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
        self.panel_header_layout = SlotListItemHeader(item_data=self.item_data, panel=self)
        self.leading_avatar = self.panel_header_layout.ids.leading_avatar
        self.panel_header.add_widget(self.panel_header_layout)
        self.leading_avatar.source = "" if not self.item_data['avatar'] else self.item_data['avatar']
        if self.item_data.bk_mode:
            self.panel_header_layout.ids.slot_item_container.add_widget(BaseListItemIcon(icon="food", theme_font_size="Custom", 
                                                                                        font_size=dp(14), pos_hint={"center_y": 0.5}),1)
        if self.item_data.deafened:
            self.panel_header_layout.ids.slot_item_container.add_widget(BaseListItemIcon(icon="headphones-off", theme_font_size="Custom", 
                                                                                        font_size=dp(14), pos_hint={"center_y": 0.5}),1)
        if self.item_data.game_status == "GOAL":
            self.panel_header_layout.ids.game_item_container.add_widget(BaseListItemIcon(icon="flag_checkered", theme_font_size="Custom", 
                                                                                        font_size=dp(14), pos_hint={"center_y": 0.5}),1)

        i = 1 if self.app.theme_cls.theme_style == "Dark" else 0
        item_colors = {
            "trap": self.app.theme_mw.markup_tags_theme.trap_item_color[i],
            "regular": self.app.theme_mw.markup_tags_theme.regular_item_color[i],
            "useful": self.app.theme_mw.markup_tags_theme.useful_item_color[i],
            "progression_deprioritized": self.app.theme_mw.markup_tags_theme.progression_deprioritized_item_color[i],
            "progression": self.app.theme_mw.markup_tags_theme.progression_item_color[i],
            "progression_goal": self.app.theme_mw.markup_tags_theme.progression_goal_item_color[i],
        }

        
        for hint in self.item_data.hints.values():
            if hint.hint_status == HintStatus.HINT_FOUND or hint.found:
                hint.hide = True
            if hint.hide and not self.app.show_all_hints:
                continue
            
            hint_item = HintListItem(hint_data=hint, game_status=self.item_data.game_status, shadow_colors=item_colors,
                                     hint_icon_status=status_icons[hint.hint_status], hint_status_text=status_names[hint.hint_status]
                                     )
            hint_item.bind(on_bkmode=lambda instance, value: self.on_bkmode(hint))
            hint_item.bind(on_goal=lambda instance, value: self.on_goal(hint))
            hint_item.bind(on_shop=lambda instance, value: self.on_shop(hint))
            
            # Only add dropdown for non-found items
            if not (hint.hint_status == HintStatus.HINT_FOUND or hint.found):
                hint_item.dropdown = HintListDropdown(
                    caller=hint_item.ids["hint_item_status_button"],
                    status_names=status_names, 
                    status_icons=status_icons, 
                    dropdown_callback=lambda status: on_select_status(hint, status)
                )
            
            self.panel_content.add_widget(hint_item)

    def on_bkmode(self, hint: UIHint):
        hint.set_status(mwgg_status=MWGGUIHintStatus.HINT_BK_MODE)
    
    def on_goal(self, hint: UIHint):
        hint.set_status(mwgg_status=MWGGUIHintStatus.HINT_GOAL)
    
    def on_shop(self, hint: UIHint):
        hint.set_status(mwgg_status=MWGGUIHintStatus.HINT_SHOP)
