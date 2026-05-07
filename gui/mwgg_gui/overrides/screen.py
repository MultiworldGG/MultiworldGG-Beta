from __future__ import annotations
"""
CUSTOM SCREEN
CustomLayout
"""
__all__ = ("CustomScreen", "CustomLayout")
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card.card import MDRelativeLayout
from ..console.textconsole import ConsoleView

from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList
from kivymd.theming import ThemableBehavior

from mwgg_gui.overrides.expansionlist import *
from mwgg_gui.components.bottomappbar import BottomAppBar
from mwgg_gui.components.mw_theme import AutoAdjustHeightBehavior


Builder.load_string('''
<CustomLayout>:
    id: custom_layout
    pos: 0,82
''')

class CustomLayout(AutoAdjustHeightBehavior, MDRelativeLayout):
    adjust_title_bar = True
    adjust_app_bar = True
    adjust_bottom_appbar = True
    adjust_custom = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = 1


class CustomScreen(MDScreen, ThemableBehavior):
    '''
    This is the main screen for the custom screen.
    Contains the layouts for the custom screen (Tracker, etc)
    TODO: make this more modular, move SliverAppbar importantappbar here
    and have Console/Hint import it.
    '''
    app: MDApp
    custom_layout: CustomLayout
    bottom_appbar: BottomAppBar


    def __init__(self, name: str, **kwargs):
        self.name = name
        self.app = MDApp.get_running_app()
        self.size_hint = (1,1)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        super().__init__(**kwargs)

        self.bottom_appbar = BottomAppBar(screen_name=self.name)
        self.custom_layout = CustomLayout()
        self.add_widget(self.custom_layout)
        self.add_widget(self.bottom_appbar)