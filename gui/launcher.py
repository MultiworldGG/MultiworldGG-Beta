from __future__ import annotations
__all__ = ['LauncherScreen', 'LauncherLayout']
import asynckivy
from textwrap import wrap
from kivy.metrics import dp
from kivy.properties import StringProperty, DictProperty, ObjectProperty, BooleanProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivymd.uix.sliverappbar import MDSliverAppbar, MDSliverAppbarHeader, MDSliverAppbarContent
from kivymd.uix.appbar import MDTopAppBar
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import *
from kivymd.uix.expansionpanel import *
from .kivydi.expansionlist import *
from kivymd.uix.textfield import MDTextField, MDTextFieldHelperText, MDTextFieldHintText, MDTextFieldLeadingIcon, MDTextFieldTrailingIcon
import logging
from typing import Any

from kivy.clock import Clock
from kivy.app import App
from data.game_index import GameIndex

from .bottomappbar import BottomAppBar
from .launcher_sliver_appbar import LauncherSliverAppbar, SearchBar, LauncherTextField

from Utils import discover_and_launch_module

import sys

game_index = GameIndex()
logger = logging.getLogger("Client")

Builder.load_string('''
<LauncherScreen>:
    size_hint: 1,1
    pos_hint: {"center_x": 0.5, "center_y": 0.5}

<LauncherLayout>:
    id: launcher_layout
    y: 82
    size_hint_y: 1-(185/Window.height)

<LauncherView>:
    id: launcher_view
    server_layout: server_layout
    module_name: ""
    orientation: 'horizontal'
    padding: dp(50)
    MDBoxLayout:
        orientation: 'vertical'
        spacing: 30
        padding: dp(30)
        theme_bg_color: "Custom"
        md_bg_color: app.theme_cls.surfaceVariantColor
        MDBoxLayout:
            orientation: 'vertical'
            MDBoxLayout:
                orientation: 'vertical'
                spacing: 10
                size_hint_y: None
                height: dp(120)
                MDLabel:
                    text: "Welcome to Multiworld!"
                    halign: 'center'
                    font_style: "Title"
                    role: "small"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.onSurfaceVariantColor
            MDBoxLayout:
                orientation: 'horizontal'
                spacing: 10
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)
                    MDButton:
                        id: connect_button
                        pos_hint: {"center_x": 0.5}
                        on_release: app.launcher_screen.connect()
                        MDButtonText:
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.onSurfaceVariantColor
                            text: 'Connect & Play'
                            halign: 'center'
                        MDButtonIcon:
                            icon: "play-network"
                    MDButton:
                        id: game_patch_button
                        pos_hint: {"center_x": 0.5}
                        MDButtonText:
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.onSurfaceVariantColor
                            text: 'Patch Game'
                            halign: 'center'
                        MDButtonIcon:
                            icon: "file-edit"
                    MDButton:
                        id: game_yaml_button
                        pos_hint: {"center_x": 0.5}
                        MDButtonText:
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.onSurfaceVariantColor
                            text: 'Create YAML'
                            halign: 'center'
                        MDButtonIcon:
                            icon: "code-block-brackets"
                    MDButton:
                        id: generate_button
                        on_release: app.root.current = 'generate'
                        pos_hint: {"center_x": 0.5}
                        MDButtonText:
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.onSurfaceVariantColor
                            text: 'Generate'
                            halign: 'center'
                        MDButtonIcon:
                            icon: "gamepad-square-outline"
                    MDButton:
                        id: host_button
                        on_release: app.root.current = 'host'
                        pos_hint: {"center_x": 0.5}
                        MDButtonText:
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.onSurfaceVariantColor
                            text: 'Host'
                            halign: 'center'
                        MDButtonIcon:
                            icon: "router-network"
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: dp(5)
                    width: dp(10)
                    size_hint_x: None
                    MDDivider:
                        size_hint_y: .8
                        pos_hint: {"center_y": 0.5}
                        orientation: "vertical"
                        color: app.theme_cls.outlineColor
                MDBoxLayout:
                    id: server_layout
                    orientation: 'vertical'
                    spacing: dp(15)
                    LauncherAuthTextField:
                        id: server
                        size_hint_x: 0.8
                        pos_hint: {"center_x": 0.5}
                        text: app.app_config.get("client", "hostname", fallback="")
                        MDTextFieldLeadingIcon:
                            theme_icon_color: "Custom"
                            icon: 'router-network'
                            icon_color_focus: self.parent.icon_color_focus
                            icon_color_normal: self.parent.icon_color_normal
                        MDTextFieldHintText:
                            text: "Server Address"
                        # MDTextFieldHelperText:
                        #     theme_text_color: "Custom"
                        #     text_color_focus: self.parent.text_color_focus
                        #     text_color_normal: self.parent.text_color_normal
                        #     text: "multiworld.gg"
                        #     mode: "persistent"
                    LauncherAuthTextField:
                        id: port
                        size_hint_x: 0.8
                        pos_hint: {"center_x": 0.5}
                        text: app.app_config.get("client", "port", fallback="")
                        MDTextFieldLeadingIcon:
                            theme_icon_color: "Custom"
                            icon: 'numeric'
                            icon_color_focus: self.parent.icon_color_focus
                            icon_color_normal: self.parent.icon_color_normal
                        MDTextFieldHintText:
                            text: "Port"
                        # MDTextFieldHelperText:
                        #     theme_text_color: "Custom"
                        #     text_color_focus: self.parent.text_color_focus
                        #     text_color_normal: self.parent.text_color_normal
                        #     text: "38281"
                        #     mode: "persistent"
                    LauncherAuthTextField:
                        id: slot_name
                        size_hint_x: 0.8
                        pos_hint: {"center_x": 0.5}
                        text: app.app_config.get("client", "slot_name", fallback="")
                        MDTextFieldLeadingIcon:
                            theme_icon_color: "Custom"
                            icon_color_focus: self.parent.icon_color_focus
                            icon_color_normal: self.parent.icon_color_normal
                            icon: 'ticket-account'
                        MDTextFieldHintText:
                            text: "Username"
                    LauncherAuthTextField:
                        id: slot_password
                        password: True
                        size_hint_x: 0.8
                        pos_hint: {"center_x": 0.5}
                        text: app.app_config.get("client", "slot_password", fallback="")
                        MDTextFieldLeadingIcon:
                            theme_icon_color: "Custom"
                            icon_color_focus: self.parent.icon_color_focus
                            icon_color_normal: self.parent.icon_color_normal
                            icon: 'lock'    
                        MDTextFieldHintText:
                            text: "Password"
                        # MDTextFieldHelperText:
                        #     theme_text_color: "Custom"
                        #     text_color_focus: self.parent.text_color_focus
                        #     text_color_normal: self.parent.text_color_normal
                        #     text: "Password"
                        #     mode: "persistent"

<TagChip>:
    type: "filter"
    MDChipText:
        text: root.text
        icon: root.icon

<LauncherAuthTextField>:
    theme_font_name: "Custom"
    theme_font_style: "Custom"
    theme_icon_color: "Custom"
    theme_text_color: "Custom"
    theme_bg_color: "Custom"
    text_color_focus: app.theme_cls.onSecondaryContainerColor
    text_color_normal: app.theme_cls.onSurfaceVariantColor
    icon_color_focus: app.theme_cls.primaryColor
    icon_color_normal: app.theme_cls.onPrimaryColor
    fill_color_focus: app.theme_cls.surfaceContainerHighestColor
    fill_color_normal: app.theme_cls.surfaceVariantColor
    font_name: app.theme_cls.font_styles[self.font_style][self.role]["font-name"]
    font_size: app.theme_cls.font_styles[self.font_style][self.role]["font-size"]
    mode: "filled"
    write_tab: False

''')
class LauncherLayout(MDFloatLayout):
    pass

class LauncherView(MDBoxLayout):
    slot_layout: ObjectProperty
    server_layout: ObjectProperty

class LauncherAuthTextField(MDTextField):
    pass


class LauncherScreen(MDScreen, ThemableBehavior):
    '''
    This is the main screen for the launcher.
    Left side has the game list/sorter
    Right contains the previously selected game
    with options to connect to the MW server
    '''
    name = "launcher"
    launcher_hero_from: ObjectProperty
    launchergrid: LauncherLayout
    important_appbar: MDSliverAppbar
    launcher_view: LauncherView
    game_filter: list
    game_tag_filter: StringProperty
    bottom_appbar: BottomAppBar
    selected_game: StringProperty = ""
    app: App
    result: Any
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.game_filter = []
        self.games_mdlist = MDList(width=260)
        self.game_tag_filter = "popular"
        self.selected_game = ""
        self.app = App.get_running_app()

        self.bottom_appbar = BottomAppBar(screen_name="launcher")
        self.important_appbar = LauncherSliverAppbar()
        self.launcher_view = LauncherView()
        Clock.schedule_once(lambda x: self.init_important())

        asynckivy.start(self.set_game_list())

    def init_important(self):
        self.launchergrid = LauncherLayout()

        self.add_widget(self.launchergrid)
        self.add_widget(self.bottom_appbar)

        self.launcher_hero_from = self.important_appbar.launcher_hero_from
        self.heroes_from = [self.launcher_hero_from]

        self.important_appbar.size_hint_x = 260/Window.width
        self.important_appbar.size_hint_y=1
        self.launcher_view.size_hint_x = 1-(264/Window.width)
        self.launcher_view.size_hint_y =1

        self.important_appbar.ids.scroll.scroll_wheel_distance = 40
        #self.important_appbar.ids.scroll.y = 82

        self.important_appbar.content.add_widget(self.games_mdlist)

        self.launchergrid.add_widget(self.important_appbar)
        self.launcher_view.pos_hint={"y": 0, "x": 260/Window.width}
        self.launchergrid.add_widget(self.launcher_view)

    async def set_game_list(self):
        game_index = GameIndex()
        matching_games = game_index.search(self.game_tag_filter)
        self.games_mdlist.clear_widgets()
        for module_name, game_data in matching_games.items():
            await asynckivy.sleep(0)
            game = GameListPanel(
                item_name=module_name, 
                item_data=game_data,
                on_game_select=lambda x, name=module_name: self.on_game_selected(name)
            )
            self.games_mdlist.add_widget(game)

    def on_game_selected(self, module_name):
        """Handle game selection from the game list"""
        self.selected_game = module_name
        logger.info(f"Selected game: {module_name}")
        # Update the launcher view to show the selected game
        self.launcher_view.module_name = module_name

    def set_filter(self, active, tag):
        if active:
            self.game_filter.append((self.game_tag_filter.text, tag))
        else:
            self.game_filter.remove((self.game_tag_filter.text, tag))

    def on_game_tag_filter_text(self, instance):
        self.game_filter = [(self.game_tag_filter.text, tag) for tag in GameIndex.search(self.game_tag_filter.text)]
    
    def connect(self):
        """Connect to server and launch the selected game module"""
        logger.info("Connect method called!")
        
        if not self.selected_game:
            logger.warning("No game selected")
            return
        
        # Get connection details from the UI
        server_field = self.launcher_view.ids.server
        port_field = self.launcher_view.ids.port
        slot_name_field = self.launcher_view.ids.slot_name
        slot_password_field = self.launcher_view.ids.slot_password

        if not server_field.text:
            server_field.text = server_field.hint_text
        if not port_field.text:
            port_field.text = port_field.hint_text
        if not slot_name_field.text:
            slot_name_field.text = slot_name_field.hint_text
        
        server_address = f"{server_field.text}:{port_field.text}" if server_field.text and port_field.text else None
        slot_name = slot_name_field.text if slot_name_field.text else None
        password = slot_password_field.text if slot_password_field.text else None
        
        logger.info(f"Attempting to launch module: {self.selected_game}")
        logger.info(f"Server: {server_address}, Password: {'*' * len(password) if password else 'None'}")
        
        try:
            # Switch to console screen first to ensure it's created before connection
            self.app.client_console_init()
            
            # Show loading screen
            #Clock.schedule_once(lambda dt: self.app.loading_layout.show_loading(speed=0.033), 0)

            # Define ready callback to hide loading layout and initialize console
            def ready_callback():
                self.app.loading_layout.hide_loading()
                # Initialize console after context switch
                Clock.schedule_once(lambda x: self.app.console_init())
            discover_and_launch_module(
                    self.selected_game, server_address = server_address, slot_name = slot_name, \
                    password = password, ready_callback=ready_callback
            )
                
        except Exception as e:
            logger.error(f"Failed to launch {self.selected_game} module: {e}")
            # Hide loading layout on error
            self.app.loading_layout.hide_loading()
            # You might want to show an error dialog here
            # from .dialog import show_error_dialog
            # show_error_dialog("Launch Error", f"Failed to launch {self.selected_game}: {str(e)}")
