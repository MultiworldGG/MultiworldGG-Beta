from __future__ import annotations
"""
CONSOLE SCREEN
ConsoleSliverAppbar - Left side has the players, with expansion for hints TODO: rename and move to components (profile/hintlist)
ConsoleLayout - Right contains the console
"""
__all__ = ("ConsoleScreen", "ConsoleSliverAppbar", "ConsoleLayout")
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card.card import MDRelativeLayout
from .textconsole import ConsoleView

from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.sliverappbar import MDSliverAppbar, MDSliverAppbarContent
from kivymd.uix.list import MDList
from kivymd.theming import ThemableBehavior

from mwgg_gui.overrides.expansionlist import *
from mwgg_gui.components.bottomappbar import BottomAppBar
from mwgg_gui.components.mw_theme import AutoAdjustHeightBehavior

import asynckivy

Builder.load_string('''
<ConsoleLayout>:
    id: console_layout
    pos: 0,82

<ConsoleSliverAppbar>:
    pos_hint: {"x": 0, "top": 1}
    width: dp(260)
    size_hint_x: None
    adaptive_height: True
    hide_appbar: True
    deafened_icon: "headphones"
    background_color: app.theme_cls.secondaryContainerColor
    MDSliverAppbarHeader:
        AsyncImage:
            source: app.logo_png
            pos_hint: {"top": 1}
            fit_mode: "cover"
    MDTopAppBar:
        type: "small"
        pos_hint: {"center_x": 0.5, "top": 1}
        padding: dp(4),0,dp(4),dp(4)
        MDTopAppBarLeadingButtonContainer:
            MDActionTopAppBarButton:
                icon: "refresh"
                on_release: app.ctx.ui.update_hints()
        MDTopAppBarTitle:
            text: "Flags"
            halign: "center"
            font_style: "Body"
            role: "medium"
        MDTopAppBarTrailingButtonContainer:
            MDActionTopAppBarButton:
                icon: "food"
                on_release: root.set_bk()
            MDActionTopAppBarButton:
                icon: root.deafened_icon
                on_release: root.set_deafen()
''')

class ConsoleLayout(AutoAdjustHeightBehavior, MDRelativeLayout):
    adjust_title_bar = True
    adjust_app_bar = True
    adjust_bottom_appbar = True
    adjust_custom = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = 1

class ConsoleSliverAppbar(MDSliverAppbar):
    content: MDSliverAppbarContent
    app: MDApp
    deafened_icon: StringProperty

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.content = MDSliverAppbarContent(orientation="vertical")
        self.content.id = "content"
        self.add_widget(self.content)

    def set_bk(self):
        self.app.ctx.ui.set_bk()
    
    def set_deafen(self):
        '''
        Trigger deafened toggle, and set the icon to the opposite of what it is currently
        Function call takes too long to set the icon "correctly", so we go backwards.
        '''
        preemptive_deafened = not self.app.ctx.ui.local_player_data.deafened
        self.deafened_icon = "headphones-off" if preemptive_deafened else "headphones"

        self.app.ctx.ui.set_deafen()




class ConsoleScreen(MDScreen, ThemableBehavior):
    '''
    This is the main screen for the console.
    Left side has the players, with expansion for hints
    Right contains the console
    '''
    name = "console"
    app: MDApp
    consolegrid: MDBoxLayout
    important_appbar: MDSliverAppbar
    ui_console: ConsoleView
    bottom_appbar: BottomAppBar


    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        self.size_hint = (1,1)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        super().__init__(**kwargs)
        self.slots_mdlist = MDList(width=260)

        self.bottom_appbar = BottomAppBar(screen_name="console")

        self.important_appbar = ConsoleSliverAppbar()

        Clock.schedule_once(lambda x: self.init_important())

    def update_slots_list(self):
        """Update the slots list when hints data becomes available"""
        asynckivy.start(self.set_slots_list())


    def init_important(self):
        self.consolegrid = ConsoleLayout(width=Window.width, height=Window.height-185)
        self.add_widget(self.consolegrid)
        self.add_widget(self.bottom_appbar)


        self.important_appbar.size_hint_x = 260/Window.width
        self.important_appbar.size_hint_y=1-(8/Window.height)

        self.ui_console = ConsoleView(pos_hint={"y": 0, "center_x": .5+(130/Window.width)},
                                      size_hint_x=1-(264/Window.width), 
                                      size_hint_y=1-(8/Window.height))
        self.important_appbar.ids.scroll.scroll_wheel_distance = 40

        self.important_appbar.content.add_widget(self.slots_mdlist)

        self.consolegrid.add_widget(self.important_appbar)
        self.consolegrid.add_widget(self.ui_console)

    def _get_slot_priority(self, slot_data) -> tuple[bool, int]:
        """
        Calculate priority for sorting slots.
        Returns (has_hints, -priority_value) where:
        - has_hints: True if slot has any visible hints, False otherwise
        - priority_value: negative of highest elevation level (for proper sorting)
        Priority order: 5 (highest), 4, 6, 3, 2, 1, 0
        """
        visible_hints = [
            hint for hint in slot_data.hints.values()
            if not hint.hide or self.app.show_all_hints
        ]
        
        if not visible_hints:
            return (False, 0)  # No hints, goes to end
        
        # Calculate elevation levels for each hint
        priority_order = {5: 0, 4: 1, 6: 2, 3: 3, 2: 4, 1: 5, 0: 6}
        highest_priority = 6  # Default to lowest priority
        
        for hint in visible_hints:
            classification = hint.assigned_classification if hint.assigned_classification else hint.classification
            
            # Determine elevation level based on classification
            if hint.found == "Found":
                elevation = 0
            elif classification == "Progression - Requried for Goal":
                elevation = 6
            elif classification == "Progression":
                elevation = 5
            elif classification == "Progression - Logically Relevant":
                elevation = 4
            elif classification == "Useful":
                elevation = 3
            elif classification == "Filler":
                elevation = 2
            elif classification == "Trap":
                elevation = 1
            else:
                elevation = 0
            
            # Update if this is higher priority
            if elevation in priority_order:
                if priority_order[elevation] < highest_priority:
                    highest_priority = priority_order[elevation]
        
        return (True, -highest_priority)  # Negative for proper sorting (lower is better)

    async def set_slots_list(self):
        self.slots_mdlist.clear_widgets()
        
        # Filter and collect slots
        slots_to_add = [
            (slot_id, slot_data)
            for slot_id, slot_data in self.app.ctx.ui.ui_player_data.items()
            if slot_data.slot_name != "Archipelago"
        ]
        
        # Sort by priority (has hints first, then by elevation priority)
        slots_to_add.sort(key=lambda x: self._get_slot_priority(x[1]), reverse=True)
        
        # Add sorted slots
        for slot_id, slot_data in slots_to_add:
            await asynckivy.sleep(0)
            slot = GameListPanel(item_name=slot_id, item_data=slot_data)
            self.slots_mdlist.add_widget(slot)
