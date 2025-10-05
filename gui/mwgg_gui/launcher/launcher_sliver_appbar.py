from __future__ import annotations
"""
LauncherSliverAppbar: class that provides the games list on the launcher screen

Includes the following:
- SearchBar - search bar for the launcher screen
- LauncherTextField - text field for the search bar
"""
__all__ = ('LauncherSliverAppbar', 'SearchBar', 'LauncherTextField')

from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivymd.uix.sliverappbar import MDSliverAppbar, MDSliverAppbarContent
from kivymd.uix.appbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
import asynckivy

Builder.load_string('''
#:import os os
<LauncherSliverAppbar>:
    pos_hint: {"x": 0, "top": 1}
    width: dp(260)
    padding: 0
    size_hint_x: None
    adaptive_height: True
    hide_appbar: True
    background_color: app.theme_cls.secondaryContainerColor
    MDSliverAppbarHeader:
        Image:
            source: os.path.join(os.getenv("KIVY_DATA_DIR"), "images", "logo_bg.png")
            pos_hint: {"center_y": 0.5}
            fit_mode: "scale-down"
    SearchBar:
        type: "small"
        height: dp(74)
        id: games_search_bar,
        padding: dp(10), dp(0), dp(10), dp(0)
                    
<LauncherTextField>:
    theme_font_name: "Custom"
    theme_font_style: "Custom"
    font_name: app.theme_cls.font_styles[self.font_style][self.role]["font-name"]
    font_size: app.theme_cls.font_styles[self.font_style][self.role]["font-size"]
    MDTextFieldHintText:
        text: root.hint_text
        theme_font_name: "Custom"
        theme_font_style: "Custom"
        font_name: app.theme_cls.font_styles[self.font_style][self.role]["font-name"]
        font_size: app.theme_cls.font_styles[self.font_style][self.role]["font-size"]
''')

class LauncherSliverAppbar(MDSliverAppbar):
    '''
    Games list on the launcher screen
    '''
    content: MDSliverAppbarContent

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = MDSliverAppbarContent(orientation="vertical", padding=0)
        self.content.id = "content"
        self.add_widget(self.content)
        self.ids.scroll.y = dp(82)
        self.ids.header.pos_hint = {"top": 1}

class LauncherTextField(MDTextField):
    hint_text = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hint_text = kwargs.get("hint_text", "")

class SearchBar(MDTopAppBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_box = LauncherTextField(
            id="game_tag_filter",
            hint_text = "Game Search", 
            pos_hint = {"center_y": 0.5}
        )
        self.add_widget(self.search_box)
        self.search_box.bind(on_text_validate=self.on_enter)

    def add_widget(self, widget):
        if isinstance(widget, MDTextField):
            widget._appbar = self
            self.appbar_title = widget
            Clock.schedule_once(lambda x: self._add_title(widget))
        else:
            super().add_widget(widget)

    def _add_title(self, widget):
        super()._add_title(widget)

    def on_enter(self, instance):
        # Get the parent screen to access the game list
        screen = App.get_running_app().screen_manager.current_screen
        # Import here to avoid circular import
        from .launcher import LauncherScreen
        if isinstance(screen, LauncherScreen):
            # Clear existing game list
            screen.games_mdlist.clear_widgets()
            # Update the filter and trigger new search
            screen.game_tag_filter = instance.text
            asynckivy.start(screen.set_game_list()) 