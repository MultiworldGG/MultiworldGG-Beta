from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, NumericProperty, ListProperty, ObjectProperty, StringProperty, DictProperty
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.app import MDApp
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.chip import MDChip
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.theming import ThemableBehavior
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.list import MDListItem, BaseListItemIcon, MDListItemTrailingCheckbox, MDList
from kivy.uix.label import Label
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.menu.menu import MDDropdownTextItem
from kivymd.uix.dropdownitem import MDDropDownItem, MDDropDownItemText
from kivy.utils import escape_markup
from kivy.core.clipboard import Clipboard
from NetUtils import HintStatus, MWGGUIHintStatus, TEXT_COLORS
from .kivydi.expansionlist import HintListItem, IconBadge, SlotListItemHeader, GameListPanel, HintListDropdown
from .UIDataClasses import UIHint
from .bottomappbar import BottomAppBar
import typing
import asynckivy

hint_kv = '''
<HintFeaturebar>:
    hints_hero_to: hints_hero_to
    MDHeroTo:
        id: hints_hero_to
        size_hint: None,None
        size: dp(256), dp(161)
        pos_hint: {"center_x": 0.5, "top": 1}
        FitImage:
            source: "gui/data/logo_bg.png"
            size_hint: None,None
            size: dp(128), dp(80)
            pos_hint: {"x": 0, "top": 1}
'''

if typing.TYPE_CHECKING:
    from CommonClient import CommonContext

class HintFeaturebar(MDBoxLayout):
    """
    Feature bar for the hint screen.
    """
    hints_hero_to: ObjectProperty

class HintScreen(MDScreen):
    '''
    This is the main screen for displaying hints.
    It includes a top app bar, hint list panel, and bottom app bar.
    Takes full window width with no sidebar.
    '''
    name = "hint"
    hints_hero_to: ObjectProperty
    heroes_to = []
    bottom_appbar: BottomAppBar
    hint_layout: "HintLayout"
    app: MDApp
    _updating_hints: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
        # Initialize components
        self.bottom_appbar = BottomAppBar(screen_name="hint")
        self.hint_layout = HintLayout()
        self.hints_mdlist = MDList(size_hint_x=1, size_hint_y=1)
        self.hints_hero_to = self.hint_layout.search_placeholder.hints_hero_to
        self.heroes_to = [self.hints_hero_to]
        # Schedule initialization
        Clock.schedule_once(lambda x: self.init_components())

    def init_components(self):
        """Initialize and add all components to the screen"""
        # Add components to the screen
        self.add_widget(self.hint_layout)
        self.add_widget(self.bottom_appbar)
        
        # Set up hint layout positioning and sizing to take full window width
        self.hint_layout.y = dp(82)  # Account for bottom app bar
        self.hint_layout.size_hint_y = 1 - (dp(185) / Window.height)  # Account for top and bottom bars
        self.hint_layout.size_hint_x = 1  # Full window width
        
        # Add hints list to the hint layout (after the search placeholder)
        self.hint_layout.add_widget(self.hints_mdlist)

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
                    
                    # Create the static header section
                    header_section = SlotListItemHeader(item_data=slot_data, panel=None)
                    header_section.ids.leading_avatar.source = ""  # slot_data['avatar']
                    
                    # Add status icons to header
                    if slot_data.bk_mode:
                        header_section.ids.slot_item_container.add_widget(
                            BaseListItemIcon(icon="food", theme_font_size="Custom", 
                                           font_size=dp(14), pos_hint={"center_y": 0.5}), 1)
                    if slot_data.in_call:
                        header_section.ids.slot_item_container.add_widget(
                            BaseListItemIcon(icon="headphones", theme_font_size="Custom", 
                                           font_size=dp(14), pos_hint={"center_y": 0.5}), 1)
                    if slot_data.game_status == "GOAL":
                        header_section.ids.game_item_container.add_widget(
                            BaseListItemIcon(icon="flag_checkered", theme_font_size="Custom", 
                                           font_size=dp(14), pos_hint={"center_y": 0.5}), 1)
                    
                    # Add the static header to the main list
                    self.hints_mdlist.add_widget(header_section)
                    
                    # Create scrollable hints container
                    hints_container = MDList()
                    
                    # Get theme colors
                    i = 1 if self.app.theme_cls.theme_style == "Dark" else 0
                    item_colors = {
                        "trap": self.app.theme_mw.markup_tags_theme.trap_item_color[i],
                        "regular": self.app.theme_mw.markup_tags_theme.regular_item_color[i],
                        "useful": self.app.theme_mw.markup_tags_theme.useful_item_color[i],
                        "progression_deprioritized": self.app.theme_mw.markup_tags_theme.progression_deprioritized_item_color[i],
                        "progression": self.app.theme_mw.markup_tags_theme.progression_item_color[i],
                        "progression_goal": self.app.theme_mw.markup_tags_theme.progression_goal_item_color[i],
                    }
                    
                    def on_select_status(instance, status: HintStatus):
                        instance.hint.set_status(status=status)
                    
                    # Add individual hint items to the scrollable container
                    for hint in slot_data.hints.values():
                        if hint.hint_status == HintStatus.HINT_FOUND or hint.found:
                            hint.hide = True
                        if hint.hide and not self.app.show_all_hints:
                            continue
                            
                        hint_item = HintListItem(
                            hint_data=hint, 
                            game_status=slot_data.game_status, 
                            shadow_colors=item_colors,
                            hint_icon_status=status_icons[hint.hint_status], 
                            hint_status_text=status_names[hint.hint_status]
                        )
                        hint_item.bind(on_bkmode=lambda x: self.on_bkmode(hint))
                        hint_item.bind(on_goal=lambda x: self.on_goal(hint))
                        hint_item.bind(on_shop=lambda x: self.on_shop(hint))
                        hint_item.dropdown = HintListDropdown(
                            status_names=status_names, 
                            status_icons=status_icons, 
                            dropdown_callback=on_select_status
                        )
                        hint_item.dropdown.bind(on_release=hint_item.dropdown.dismiss)
                        hint_item.dropdown.caller = hint_item.ids["hint_item_status_button"]
                        hints_container.add_widget(hint_item)
                    
                    # Create a scroll view for the hints and add it to the main list
                    # Calculate dynamic height based on available space, but cap it for usability
                    max_height = min(dp(400), len(slot_data.hints) * dp(80) + dp(20))  # Dynamic based on hint count
                    hints_scroll = MDScrollView(size_hint_y=None, height=max_height)
                    hints_scroll.add_widget(hints_container)
                    self.hints_mdlist.add_widget(hints_scroll)
                    
        finally:
            self._updating_hints = False

    def on_bkmode(self, hint: UIHint):
        hint.set_status(mwgg_status=MWGGUIHintStatus.HINT_BK_MODE)
    
    def on_goal(self, hint: UIHint):
        hint.set_status(mwgg_status=MWGGUIHintStatus.HINT_GOAL)
    
    def on_shop(self, hint: UIHint):
        hint.set_status(mwgg_status=MWGGUIHintStatus.HINT_SHOP)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Create placeholder for future search and filter functionality
        self.search_placeholder = HintFeaturebar(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(150),
            spacing=dp(16),
            padding=[dp(16), dp(8), dp(16), dp(8)]
        )
        
        # Add placeholder label for future search functionality
        placeholder_label = MDLabel(
            text="Search & Filter Options (Future Feature)",
            theme_text_color="Hint",
            size_hint_y=None,
            height=dp(40)
        )

        self.show_all_hints_switch = MDSwitch(
            size_hint_y=None,
            height=dp(40),
            icon_inactive="eye-off",
            icon_active="eye",
            on_active=self.on_show_all_hints
        )
        self.search_placeholder.add_widget(placeholder_label)
        self.search_placeholder.add_widget(self.show_all_hints_switch)
        # Add the placeholder to the layout
        self.add_widget(self.search_placeholder)

    def on_show_all_hints(self, instance, value):
        self.app.show_all_hints = value

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
    HintStatus.HINT_FOUND: "Found",
    HintStatus.HINT_UNSPECIFIED: "Unset",
    HintStatus.HINT_NO_PRIORITY: "Doesn't Matter",
    HintStatus.HINT_AVOID: "Don't Get This",
    HintStatus.HINT_PRIORITY: "This is Important",
}
"""Mapping of hint status values to their human-readable display names."""

status_colors: typing.Dict[HintStatus, str] = {
    HintStatus.HINT_FOUND: TEXT_COLORS["location_color"],
    HintStatus.HINT_UNSPECIFIED: TEXT_COLORS["regular_item_color"],
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
        Clock.schedule_once(self.populate_slot_item, 0)

    def populate_slot_item(self, ctx: "CommonContext"):
        """
        Populate the panel with slot items when hints are present.
        
        This method sets up the panel to display slot information
        including the header with avatar and slot items for each hint.
        """

        def on_select_status(instance, status: HintStatus):
            instance.hint.set_status(status=status)

        hint_items = []
        self.panel_header = self.ids.panel_header
        self.panel_content = self.ids.panel_content
        self.panel_header_layout = SlotListItemHeader(item_data=self.item_data, panel=self)
        self.leading_avatar = self.panel_header_layout.ids.leading_avatar
        self.panel_header.add_widget(self.panel_header_layout)
        self.leading_avatar.source = "" #self.item_data['avatar']
        if self.item_data.bk_mode:
            self.panel_header_layout.ids.slot_item_container.add_widget(BaseListItemIcon(icon="food", theme_font_size="Custom", 
                                                                                        font_size=dp(14), pos_hint={"center_y": 0.5}),1)
        if self.item_data.in_call:
            self.panel_header_layout.ids.slot_item_container.add_widget(BaseListItemIcon(icon="headphones", theme_font_size="Custom", 
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
            hint_item.bind(on_bkmode=lambda x: self.on_bkmode(hint))
            hint_item.bind(on_goal=lambda x: self.on_goal(hint))
            hint_item.bind(on_shop=lambda x: self.on_shop(hint))
            hint_item.dropdown = HintListDropdown(status_names=status_names, status_icons=status_icons, dropdown_callback=on_select_status)
            hint_item.dropdown.bind(on_release=hint_item.dropdown.dismiss)
            hint_item.dropdown.caller = hint_item.ids["hint_item_status_button"]
            self.panel_content.add_widget(hint_item)

    def on_bkmode(self, hint: UIHint):
        hint.set_status(mwgg_status=MWGGUIHintStatus.HINT_BK_MODE)
    
    def on_goal(self, hint: UIHint):
        hint.set_status(mwgg_status=MWGGUIHintStatus.HINT_GOAL)
    
    def on_shop(self, hint: UIHint):
        hint.set_status(mwgg_status=MWGGUIHintStatus.HINT_SHOP)

# class HintLabel(MDBoxLayout):
#     """Recyclable label widget for displaying hint information in a table format.
    
#     This class represents a single row in the hint log table, displaying
#     information about hints including receiving player, item, finding player,
#     location, entrance, and status. It supports selection, sorting, and
#     status modification through dropdown menus.
    
#     Attributes:
#         selected (bool): Whether this hint row is currently selected
#         striped (bool): Whether this row should have striped background
#         index (int): The index of this item in the recycle view
#         dropdown (MDDropdownMenu): Dropdown menu for status selection
#     """
#     selected = BooleanProperty(False)
#     striped = BooleanProperty(False)
#     index = None
#     dropdown: MDDropdownMenu
#     hint: UIHint

#     def __init__(self, hint: UIHint, ctx: "CommonContext"):
#         super().__init__()
#         self.hint = hint

#         menu_items = []
#         for status in (HintStatus.HINT_NO_PRIORITY, HintStatus.HINT_PRIORITY, HintStatus.HINT_AVOID):
#             name = status_names[status]
#             status_button = MDDropDownItem(MDDropDownItemText(text=name), size_hint_y=None, height=dp(50))
#             status_button.status = status
#             menu_items.append({
#                 "text": name,
#                 "leading_icon": status_icons[status],
#                 "on_release": lambda x=status: select(self, x)
#             })

#         self.dropdown = MDDropdownMenu(caller=self.ids["status"], items=menu_items)

#         def select(instance, data):
#             self.hint.set_status(status=data)

#         self.dropdown.bind(on_release=self.dropdown.dismiss)

#     def set_height(self, instance, value):
#         self.height = max([child.texture_size[1] for child in self.children])

#     def on_touch_down(self, touch):
#         """ Add selection on touch down """
#         if super(HintLabel, self).on_touch_down(touch):
#             return True
#         if self.index:  # skip header
#             if self.collide_point(*touch.pos):
#                 status_label = self.ids["status"]
#                 if status_label.collide_point(*touch.pos):
#                     if self.hint["status"] == HintStatus.HINT_FOUND:
#                         return
#                     if self.hint.self:# If this player owns this hint
#                         # open a dropdown
#                         self.dropdown.open()
#                 elif self.selected:
#                     self.parent.clear_selection()
#                 else:
#                     text = "".join((self.receiving_text, "\'s ", self.item_text, " is at ", self.location_text, " in ",
#                                     self.finding_text, "\'s World", (" at " + self.entrance_text)
#                                     if self.entrance_text != "Vanilla"
#                                     else "", ". (", self.status_text.lower(), ")"))
#                     temp = Label(text).markup
#                     text = "".join(part for part in temp if not part.startswith("["))
#                     Clipboard.copy(escape_markup(text).replace("&amp;", "&").replace("&bl;", "[").replace("&br;", "]"))
#                     return self.parent.select_with_touch(self.index, touch)
#         else:
#             parent = self.parent
#             parent.clear_selection()
#             parent: HintLog = parent.parent
#             # find correct column
#             for child in self.children:
#                 if child.collide_point(*touch.pos):
#                     key = child.sort_key
#                     if key == "status":
#                         parent.hint_sorter = lambda element: status_sort_weights[element["status"]["hint"]["status"]]
#                     # else:
#                         # parent.hint_sorter = lambda element: (
#                         #     remove_between_brackets.sub("", element[key]["text"]).lower()
#                         # )
#                     if key == parent.sort_key:
#                         # second click reverses order
#                         parent.reversed = not parent.reversed
#                     else:
#                         parent.sort_key = key
#                         parent.reversed = False
#                     MDApp.get_running_app().update_hints()

#     def apply_selection(self, rv, index, is_selected):
#         """ Respond to the selection of items in the view. """
#         if self.index:
#             self.selected = is_selected

Builder.load_string(hint_kv)