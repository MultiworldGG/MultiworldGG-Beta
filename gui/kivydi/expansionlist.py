from __future__ import annotations
__all__ = ['GameListPanel', 
           'GameListItem', 
           'GameListItemLongText', 
           'GameListItemShortText', 
           'GameTrailingPressedIconButton',
           'SlotListItemHeader',
           'SlotListItem',
           ]
import asynckivy
from textwrap import wrap

from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, DictProperty, ObjectProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import RotateBehavior, CommonElevationBehavior
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.badge import MDBadge

from kivymd.uix.list import *
from kivymd.uix.expansionpanel import *

from kivymd.uix.tooltip import MDTooltip

import logging
from kivy.logger import Logger
from kivy.lang import Builder
import os
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from NetUtils import HintStatus
    from CommonClient import CommonContext

logger = logging.getLogger(__name__)

with open(os.path.join(os.path.dirname(__file__), "expansionlist.kv"), encoding="utf-8") as kv_file:
    Builder.load_string(kv_file.read())

class IconBadge(MDBadge):
    """
    A custom badge widget for displaying icons.
    """
    pass

class SlotListItemHeader(MDBoxLayout, CommonElevationBehavior):
    """
    Header widget for displaying slot item information, it 
    contains slot name and game information.
    
    Attributes:
        slot_name (StringProperty): The name of the slot
        game (StringProperty): The name of the game
        panel (ObjectProperty): Reference to the parent panel
    """
    slot_name: StringProperty
    game: StringProperty
    panel: ObjectProperty

    def __init__(self, game_data, panel, **kwargs):
        """
        Initialize the SlotListItemHeader.
        
        Args:
            game_data (dict): Dictionary containing slot and game information
            panel: Reference to the parent panel
        """
        self.panel = panel
        self.game_data = game_data
        for item in self.game_data:
            if item == "slot_name":
                self.slot_name = self.game_data[item]
            elif item == "game":
                self.game = self.game_data[item]

        super().__init__(**kwargs)


class GameListItemHeader(MDBoxLayout, ButtonBehavior, ThemableBehavior):
    """
    Header widget for displaying game item information in the game list.
    
    Attributes:
        game_tag (StringProperty): The tag identifier for the game
        game_data (DictProperty): Dictionary containing game information
        panel (ObjectProperty): Reference to the parent panel
        on_game_select (ObjectProperty): Callback function for game selection
    """
    game_module: StringProperty
    game_data: DictProperty
    panel: ObjectProperty
    on_game_select: ObjectProperty = None

    def __init__(self, game_module, game_data, panel, on_game_select=None, **kwargs):
        """
        Initialize the GameListItemHeader.
        
        Args:
            game_tag (str): The tag identifier for the game
            game_data (dict): Dictionary containing game information
            panel: Reference to the parent panel
            on_game_select: Callback function for game selection
        """
        self.game_module = game_module
        self.game_data = game_data
        self.panel = panel
        self.on_game_select = on_game_select
        self.style = "Tonal"
        super().__init__(**kwargs)

    def on_release(self, *args):
        """Handle press event for game selection"""
        if self.on_game_select:
            self.on_game_select(self.game_module)

    def list_tooltip(self, item_list: list[str]) -> dict[str, str]:
        """
        Create tooltip text for a list of items.
        
        Wraps the text to fit within specified width constraints and creates
        both a label (shortened) and tooltip (full) version.
        
        Args:
            item_list (list[str]): List of items to create tooltip for
            
        Returns:
            dict[str, str]: Dictionary with 'label' (shortened text) and 
                           'tooltip' (full text) keys
        """
        full_list = ", ".join(item_list).rstrip(", ")
        wrapped_list = wrap(full_list, width=17, break_on_hyphens=False, max_lines=3)
        item_dict = {
            "label": "\n".join(wrapped_list).rstrip("\n"),
            "tooltip": "\n".join(wrap(full_list, width=40, break_on_hyphens=False)).rstrip("\n")
        }
        return item_dict

class SlotListItem(MDBoxLayout, CommonElevationBehavior):
    """
    Widget for displaying individual slot items in the slot list.
    
    This class is used to display a slot item in the slot list.
    Displays entrance, location, item, and goal information.
    
    Attributes:
        slot_icon_entrance (ObjectProperty): Icon widget for entrance
        slot_text_entrance (ObjectProperty): Text widget for entrance name
        slot_icon_location (ObjectProperty): Icon widget for location
        slot_text_location (ObjectProperty): Text widget for location name
        slot_icon_item (ObjectProperty): Icon widget for item
        slot_text_item (ObjectProperty): Text widget for item name
        slot_icon_goal (ObjectProperty): Icon widget for goal
        item_name (StringProperty): Name of the item
        location_name (StringProperty): Name of the location
        entrance_name (StringProperty): Name of the entrance
        game_status (StringProperty): Current status of the game
        for_bk_mode (StringProperty): Indicates if item is for BK mode
        for_goal (StringProperty): Indicates if item is for their goal
        from_shop (StringProperty): Indicates if item is from a shop
        prog_level (StringProperty): Progression level
        assigned_level (StringProperty): Assigned level
    """
    slot_icon_entrance: ObjectProperty
    slot_text_entrance: ObjectProperty
    slot_icon_location: ObjectProperty
    slot_text_location: ObjectProperty
    slot_icon_item: ObjectProperty
    slot_text_item: ObjectProperty
    slot_icon_goal: ObjectProperty
    item_name: StringProperty
    location_name: StringProperty
    entrance_name: StringProperty
    game_status: StringProperty
    for_bk_mode: StringProperty
    for_goal: StringProperty
    from_shop: StringProperty
    prog_level: StringProperty
    assigned_level: StringProperty
    found: StringProperty

    def __init__(self, user_data: dict, game_status: str, shadow_colors: dict, hint_status: "HintStatus", **kwargs):
        """
        Initialize the SlotListItem.
        
        Args:
            game_status (str): Current status of the game
            game_data (dict): Dictionary containing stored data
        """
        self.user_data = user_data
        self.hint_data = self.user_data["hints"]
        self.game_status = game_status
        for item in self.hint_data:
            if item == "entrance":
                self.entrance_name = self.hint_data[item]
            elif item == "location":
                self.location_name = self.hint_data[item]
            elif item == "item":
                self.item_name = self.hint_data[item]
            elif item == "prog_level":
                self.prog_level = self.hint_data[item]
            elif item == "found":
                self.found = self.hint_data[item]
            elif item == "status":
                if self.hint_data[item] == HintStatus.HINT_FOUND:
                    self.found = "Found"
                elif self.hint_data[item] == HintStatus.HINT_UNSPECIFIED:
                    self.found = "Unspecified"
                elif self.hint_data[item] == HintStatus.HINT_NO_PRIORITY:
                    self.from_shop = "Shop"
                elif self.hint_data[item] == HintStatus.HINT_AVOID:
                    self.for_goal = "Avoid"
                elif self.hint_data[item] == HintStatus.HINT_PRIORITY:
                    self.for_bk_mode = "BK Mode"

        super().__init__(**kwargs)

        self.slot_icon_location = self.ids.slot_icon_location
        self.slot_text_location = self.ids.slot_text_location
        self.slot_icon_item = self.ids.slot_icon_item
        self.slot_text_item = self.ids.slot_text_item
        self.slot_icon_goal = self.ids.slot_icon_goal
        badge_text = ""
        if self.for_bk_mode:
            badge_text += md_icons["food"] + " "
        if self.for_goal:
            badge_text += md_icons["flag_checkered"] + " "
        if self.from_shop:
            badge_text += md_icons["shop"] + " "
        if badge_text != "":
            self.slot_icon_item.add_widget(IconBadge(text=badge_text.rstrip()))
        Clock.schedule_once(lambda x: self.populate_slot_item())
        Clock.schedule_once(lambda x: self.set_prio_behavior(shadow_colors), .5)

    def populate_slot_item(self):
        """
        Populate the slot item with entrance, location, item, and goal information.
        
        This method sets up the visual elements of the slot item including
        entrance information, location text, item text, and goal icon.
        """
        if self.entrance_name != "":
            self.slot_text_entrance = (MDListItemSupportingText(text=self.entrance_name, do_wrap=False))
            self.slot_icon_entrance = (MDListItemLeadingIcon(icon="door-open", pos_hint={"center_y": 0.5}))
            self.ids.slot_item_top_container.add_widget(self.slot_icon_entrance)
            self.ids.slot_item_top_container.add_widget(self.slot_text_entrance)
        self.slot_text_location.text = self.location_name
        self.slot_text_item.text = self.item_name
        self.slot_icon_goal.icon = "flag_checkered" if self.game_status == "GOAL" else "blank"

    def set_prio_behavior(self, item_colors: dict[str, list[str]]):
        if self.prog_level == "Trap":
            self.elevation_level = 1
            self.shadow_color = item_colors["trap"]
        if self.prog_level == "Trash":
            self.elevation_level = 2
            self.shadow_color = item_colors["regular"]
        if self.prog_level == "Useful":
            self.elevation_level = 3
            self.shadow_color = item_colors["useful"]
        if self.prog_level == "Important":
            self.elevation_level = 4
            self.shadow_color = item_colors["progression"]
        if self.found == "Found":
            self.elevation_level = 0

    def list_tooltip(self, item_list: list[str]) -> dict[str, str]:
        """
        Create tooltip text for a list of items.
        
        Wraps the text to fit within specified width constraints and creates
        both a label (shortened) and tooltip (full) version.
        
        Args:
            item_list (list[str]): List of items to create tooltip for
            
        Returns:
            dict[str, str]: Dictionary with 'label' (shortened text) and 
                           'tooltip' (full text) keys
        """
        full_list = ", ".join(item_list).rstrip(", ")
        wrapped_list = wrap(full_list, width=17, break_on_hyphens=False, max_lines=3)
        item_dict = {
            "label": "\n".join(wrapped_list).rstrip("\n"),
            "tooltip": "\n".join(wrap(full_list, width=40, break_on_hyphens=False)).rstrip("\n")
        }
        return item_dict

class GameListItemTooltip(MDTooltip):
    """
    Base class for tooltip behavior.
    
    Provides tooltip functionality for game list items.
    """
    pass

class GameListItemLongText(GameListItemTooltip, MDListItemSupportingText):
    """
    List item with tooltip behavior for long text.
    
    Implements a list item with tooltip behavior for text that may be
    truncated and needs a tooltip to show the full content.
    
    Attributes:
        text (StringProperty): The display text
        tooltip_text (StringProperty): The full text shown in tooltip
    """
    text = StringProperty("")
    tooltip_text = StringProperty("")

    def __init__(self, text, tooltip_text, **kwargs):
        """
        Initialize the GameListItemLongText.
        
        Args:
            text (str): The display text
            tooltip_text (str): The tooltip text for long items
        """
        self.text = text
        self.tooltip_text = tooltip_text
        super().__init__(**kwargs)


class GameListItemShortText(MDListItemSupportingText):
    """
    List item with no tooltip behavior for short text.

    Implements a list item without tooltip behavior for text that
    fits within the display area without truncation.
    
    Attributes:
        text (StringProperty): The display text
    """
    text = StringProperty("")
    
    def __init__(self, text, **kwargs):
        """
        Initialize the GameListItemShortText.
        
        Args:
            text (str): The display text
        """
        self.text = text
        super().__init__(**kwargs)

class GameListItem(MDListItem, CommonElevationBehavior):
    """
    Widget for displaying individual game items in the game list.
    
    This displays a single item from a dictionary (genre, theme, etc).
    Supports both long text with tooltips and short text without tooltips.
    
    Attributes:
        text (StringProperty): The display text
        icon (StringProperty): The icon to display
        tooltip_text (StringProperty): The tooltip text for long items
    """
    text = StringProperty("")
    icon = StringProperty("")
    tooltip_text = StringProperty("")
    
    def __init__(self, text="", icon="blank", tooltip_text="", **kwargs):
        """
        Initialize the GameListItem.
        
        Args:
            text (str): The display text
            icon (str): The icon to display (default: "blank")
            tooltip_text (str): The tooltip text for long items (default: "")
        """
        super().__init__(**kwargs)
        self.text = text
        self.icon = icon
        self.tooltip_text = tooltip_text
        self.width = 256
        self.pos_hint = {"center_y": 0.5}

        Clock.schedule_once(lambda x: self.remove_extra_container())
            # Create and add the text widget
        if "..." in self.text:
            text_widget = GameListItemLongText(text, tooltip_text)
        else:
            text_widget = GameListItemShortText(text)
        self.add_widget(text_widget)

    def remove_extra_container(self):
        """
        Remove the extra trailing container from the list item.
        
        This method cleans up the widget structure by removing
        unnecessary container elements.
        """
        try:
            self.remove_widget(self.ids.trailing_container)
        except:
            pass

class GameListPanel(MDExpansionPanel):
    """
    Expansion panel for displaying game information in the game or hintlist.
    
    This class is used to display a game item in the game list.
    It is a subclass of MDExpansionPanel and can display either
    slot items (if hints are present) or game metadata.
    
    Attributes:
        item_name (StringProperty): The name of the item
        item_data (DictProperty): Dictionary containing item information
        icon (StringProperty): The icon to display (default: "game-controller")
        leading_avatar (MDListItemLeadingAvatar): Avatar widget for the item
        panel_header (MDExpansionPanelHeader): Header widget for the panel
        panel_content (MDExpansionPanelContent): Content widget for the panel
        panel_header_layout (ObjectProperty): Layout for the panel header
        on_game_select (ObjectProperty): Callback function for game selection
    """
    item_name: StringProperty
    item_data: DictProperty
    icon = StringProperty("game-controller")
    leading_avatar: MDListItemLeadingAvatar
    panel_header: MDExpansionPanelHeader
    panel_content: MDExpansionPanelContent
    panel_header_layout: ObjectProperty
    on_game_select: ObjectProperty = None
    app: MDApp
    
    def __init__(self, item_name, item_data, on_game_select=None, **kwargs):
        """
        Initialize the GameListPanel.
        
        Args:
            item_name (str): The name of the item
            item_data (dict): Dictionary containing item information
            on_game_select: Callback function for game selection
            **kwargs: Additional keyword arguments for MDExpansionPanel
        """
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.item_name = item_name
        self.item_data = item_data
        self.on_game_select = on_game_select
        self.width = 256
        self.pos_hint = {"center_y": 0.5}
        if "found" in self.item_data:
            Clock.schedule_once(lambda x: self.populate_slot_item(ctx=self.app.ctx))
        else:
            Clock.schedule_once(lambda x: self.populate_game_item())

    def populate_slot_item(self, ctx: "CommonContext"):
        """
        Populate the panel with slot items when hints are present.
        
        This method sets up the panel to display slot information
        including the header with avatar and slot items for each hint.
        """
        self.panel_header = self.ids.panel_header
        self.panel_content = self.ids.panel_content
        self.panel_header_layout = SlotListItemHeader(item_data=ctx.player_names, panel=self)
        self.leading_avatar = self.panel_header_layout.ids.leading_avatar
        self.panel_header.add_widget(self.panel_header_layout)
        self.leading_avatar.source = "https://multiworld.gg/favicon.ico" #self.item_data['avatar']
        for item, data in self.item_data.items():
            if item == "bk_mode" and data:
                self.panel_header_layout.ids.slot_item_container.add_widget(BaseListItemIcon(icon="food", theme_font_size="Custom", font_size=dp(14), pos_hint={"center_y": 0.5}),1)
            elif item == "in_call" and data:
                self.panel_header_layout.ids.slot_item_container.add_widget(BaseListItemIcon(icon="headphones", theme_font_size="Custom", font_size=dp(14), pos_hint={"center_y": 0.5}),1)
            elif item == "game_status" and data == "GOAL":
                self.panel_header_layout.ids.game_item_container.add_widget(BaseListItemIcon(icon="flag_checkered", theme_font_size="Custom", font_size=dp(14), pos_hint={"center_y": 0.5}),1)
        for item in self.item_data:
            i = 1 if self.app.theme_cls.theme_style == "Dark" else 0
            item_colors = {
                "trap": self.app.theme_mw.markup_tags_theme.trap_item_color[i],
                "regular": self.app.theme_mw.markup_tags_theme.regular_item_color[i],
                "currency": self.app.theme_mw.markup_tags_theme.skip_balancing_item_color[i],
                "useful": self.app.theme_mw.markup_tags_theme.useful_item_color[i],
                "logically_required": self.app.theme_mw.markup_tags_theme.progression_deprioritized_skip_balancing_item_color[i],
                "progression": self.app.theme_mw.markup_tags_theme.progression_item_color[i], # also progression_skip_balancing
            }
            self.panel_content.add_widget(SlotListItem(game_data=item, game_status=self.item_data['game_status'], shadow_colors=item_colors))

    def populate_game_item(self):
        """
        Populate the panel with game metadata when no hints are present.
        
        This method sets up the panel to display game information
        including genres, themes, keywords, player perspectives, ratings,
        and release dates.
        """
        self.panel_header = self.ids.panel_header
        self.panel_content = self.ids.panel_content
        self.panel_header_layout = GameListItemHeader(
            game_module=self.item_name, 
            game_data=self.item_data, 
            panel=self,
            on_game_select=self.on_game_select
        )
        self.leading_avatar = self.panel_header_layout.ids.leading_avatar
        self.panel_header.add_widget(self.panel_header_layout)
        self.leading_avatar.source = self.item_data['cover_url']
        for item in self.item_data:
            if item == "genres" and self.item_data['genres']:
                list_tooltip = self.list_tooltip(self.item_data['genres'])
                self.panel_content.add_widget(GameListItem(text=list_tooltip['label'], icon="dice-multiple", tooltip_text=list_tooltip['tooltip']))
            elif item == "themes" and self.item_data['themes']:
                list_tooltip = self.list_tooltip(self.item_data['themes'])
                self.panel_content.add_widget(GameListItem(text=list_tooltip['label'], icon="sword", tooltip_text=list_tooltip['tooltip']))
            # elif item == "keywords" and self.item_data['keywords']:
            #     list_tooltip = self.list_tooltip(self.item_data['keywords'])
            #     self.panel_content.add_widget(GameListItem(text=list_tooltip['label'], icon="tag-outline", tooltip_text=list_tooltip['tooltip']))
            elif item == "player_perspectives" and self.item_data['player_perspectives']:
                list_tooltip = self.list_tooltip(self.item_data['player_perspectives'])
                self.panel_content.add_widget(GameListItem(text=list_tooltip['label'], icon="eye-outline", tooltip_text=list_tooltip['tooltip']))
            elif item == "rating" and self.item_data['rating']:
                list_tooltip = self.list_tooltip(self.item_data['rating'])
                self.panel_content.add_widget(GameListItem(text=list_tooltip['label'], icon="alert-box-outline", tooltip_text=list_tooltip['tooltip']))
            elif item == "release_date" and self.item_data['release_date']:
                self.panel_content.add_widget(GameListItem(text=str(self.item_data['release_date']), icon="calendar-month", tooltip_text=str(self.item_data['release_date'])))
                
    def list_tooltip(self, item_list: list[str]) -> dict[str, str]:
        """
        Create tooltip text for a list of items.
        
        Wraps the text to fit within specified width constraints and creates
        both a label (shortened) and tooltip (full) version.
        
        Args:
            item_list (list[str]): List of items to create tooltip for
            
        Returns:
            dict[str, str]: Dictionary with 'label' (shortened text) and 
                           'tooltip' (full text) keys
        """
        full_list = ", ".join(item_list).rstrip(", ")
        wrapped_list = wrap(full_list, width=25, break_on_hyphens=False, max_lines=3)
        item_dict = {
            "label": "\n".join(wrapped_list).rstrip("\n"),
            "tooltip": "\n".join(wrap(full_list, width=40, break_on_hyphens=False)).rstrip("\n")
        }
        return item_dict

    def toggle_expansion(self, instance):
        """
        Toggle the expansion state of the panel.
        
        Animates the padding change and opens/closes the panel
        with appropriate chevron icon updates.
        
        Args:
            instance: The widget instance that triggered the toggle
        """
        Animation(
            padding=[dp(4), dp(12), dp(4), dp(12)]
            if not self.is_open
            else [dp(8),dp(4),dp(8),dp(4)],
            d=0.2,
        ).start(self)
        self.open() if not self.is_open else self.close()
        self.set_chevron_up(instance) if self.is_open else self.set_chevron_down(instance)

class GameTrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
):
    """
    A button widget that combines button behavior, rotation behavior,
    and trailing icon functionality for game list items.
    
    This class provides an interactive icon button that can be pressed
    and rotated, typically used for trailing icons in list items.
    """
    ...