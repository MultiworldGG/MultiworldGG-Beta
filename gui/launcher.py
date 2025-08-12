from __future__ import annotations
__all__ = ['LauncherScreen', 'LauncherLayout']
import asynckivy
from textwrap import wrap
from kivy.metrics import dp
from kivy.properties import StringProperty, DictProperty, ObjectProperty, BooleanProperty, ListProperty
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
from kivymd.uix.swiper import MDSwiper, MDSwiperItem
from kivy.animation import Animation
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


<Favorites>:
    game_module: ""
    game_name: ""
    adaptive_height: True
    MDBoxLayout:
        orientation: 'vertical'
        width: dp(100)
        FitImage:
            source: root.game_cover_url
            radius: [dp(20),]
            fit_mode: "scale-down"
        MDLabel:
            text: root.game_name
            halign: 'center'
            theme_font_style: "Custom"
            font_style: "Body"
            role: "small"
            theme_text_color: "Custom"
            text_color: app.theme_cls.onSurfaceVariantColor

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
                    text: app.qotd()
                    halign: 'center'
                    theme_font_style: "Custom"
                    font_style: "Title"
                    role: "small"
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.onSurfaceVariantColor
                MDSwiper:
                    id: favorites_swiper
                    items_spacing: dp(10)
                    width_mult: 1
                    #width: dp(100)
                    # size_hint_y: None
                    # height: dp(100)
                    # y: root.height - self.height - dp(100) # root-50-30-20
                        
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
                        width: dp(200)
                        radius: dp(10)
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
                        width: dp(200)
                        radius: dp(10)
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
                        width: dp(200)
                        radius: dp(10)
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
                        width: dp(200)
                        radius: dp(10)
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
                        width: dp(200)
                        radius: dp(10)
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
                    LauncherAuthTextField:
                        id: port
                        input_filter: 'int'
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

class Favorites(MDSwiperItem):
    """Custom MDSwiperItem for displaying favorite games"""
    game_module = StringProperty("")
    game_name = StringProperty("")
    
    @property
    def game_cover_url(self):
        """Get the cover URL for the game"""
        if not self.game_module:
            return ""
        
        try:
            game_index = GameIndex()
            game_data = game_index.get_game(self.game_module)
            return game_data.get('cover_url', "") if game_data else ""
        except:
            return ""

    def _selected_size(self):
        size = [
            self._root.parent.size[0]
            - self._root.items_spacing * self._root.width_mult * 2,
            self._root.height,
        ]
        anim = Animation(
            size=size, d=self._root.size_duration, t=self._root.size_transition
        )
        anim.start(self)

    def _dismiss_size(self):
        size = [
            self._root.parent.size[0]
            - self._root.items_spacing * (1 + self._root.width_mult) * 2,
            self._root.height - self._root.items_spacing * 2,
        ]
        anim = Animation(
            size=size, d=self._root.size_duration, t=self._root.size_transition
        )
        anim.start(self)

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
    selected_game: tuple[str, str] = ("", "")
    app: App
    result: Any
    favorite_games: ListProperty = ListProperty([])

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.game_filter = []
        self.games_mdlist = MDList(width=260)
        self.game_tag_filter = "popular"
        self.selected_game = ""
        self.app = App.get_running_app()

        # Load favorite games from config
        self.load_favorite_games()

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
        
        # Update button text based on initial context
        Clock.schedule_once(lambda dt: self.update_connect_button_text(), 0.2)
        #Clock.schedule_once(lambda dt: self.update_selected_game(), 0.2)
        Clock.schedule_once(lambda dt: self.populate_favorites_swiper(), 0.2)

    async def set_game_list(self):
        game_index = GameIndex()
        matching_games = game_index.search(self.game_tag_filter)
        self.games_mdlist.clear_widgets()
        for module_name, game_data in matching_games.items():
            await asynckivy.sleep(0)
            game = GameListPanel(
                item_name=module_name, 
                item_data=game_data,
                on_game_select=lambda x, name=module_name, game_name=game_data['game_name']: self.on_game_selected((name, game_name))
            )
            self.games_mdlist.add_widget(game)

    def on_game_selected(self, game_info: tuple[str, str]):
        """Handle game selection from the game list"""
        self.selected_game = game_info
        logger.info(f"Selected game: {game_info[1]}")
        # Update the launcher view to show the selected game
        self.launcher_view.module_name = game_info[0]
        # Update button text based on context
        self.update_connect_button_text()
        
        # Handle favorites - add to favorites if not already there, or swipe to it if it is
        module_name = game_info[0]
        if self.is_favorite(module_name):
            # Game is already a favorite, swipe to it
            self.swipe_to_favorite(module_name)
        else:
            # Game is not a favorite, add it
            self.add_to_favorites(module_name)
            self.swipe_to_favorite(module_name)
   
    def set_filter(self, active, tag):
        if active:
            self.game_filter.append((self.game_tag_filter.text, tag))
        else:
            self.game_filter.remove((self.game_tag_filter.text, tag))

    def on_game_tag_filter_text(self, instance):
        self.game_filter = [(self.game_tag_filter.text, tag) for tag in GameIndex.search(self.game_tag_filter.text)]

    def update_connect_button_text(self):
        """Update the connect button text based on current context"""
        current_ctx = self.app.ctx
        connect_button = self.launcher_view.ids.connect_button
        
        # Check if we're in initial state by checking if ctx has a 'game' attribute
        if not hasattr(current_ctx, 'game'):
            # Initial state - launch new game
            connect_button._button_text.text = 'Connect & Play'
            connect_button._button_icon.icon = 'play-network'
        else:
            # Game context - reconnect
            game_name = getattr(current_ctx, 'game', 'Unknown Game')
            connect_button._button_text.text = f'Reconnect ({game_name})'
            connect_button._button_icon.icon = 'refresh'

    # def update_selected_game(self):
    #     current_ctx = self.app.ctx
    #     game_bar = self.launcher_view.ids.game_bar
    #     game_selected = self.launcher_view.ids.game_selected

    #     if not hasattr(current_ctx, 'game'):
    #         game_selected.elevation = 0
    #     else:
    #         game_selected.elevation = 10
    #         game_selected.game_name = current_ctx.game
    #         game_selected.shadow_color = self.app.theme_cls.primaryColor
    #         game_selected.shadow_offset = (0, 0)
    #         game_selected.shadow_opacity = 0.5
    #         game_selected.shadow_radius = 10
    #         game_selected.shadow_elevation = 5

    def load_favorite_games(self):
        """Load favorite games from app config"""
        try:
            favorites_str = self.app.app_config.get('game_settings', 'favorite_games', fallback='')
            if favorites_str:
                self.favorite_games = favorites_str.split(',')
            else:
                self.favorite_games = []
        except (KeyError):
            self.favorite_games = []
        logger.debug(f"Loaded {len(self.favorite_games)} favorite games")

    def save_favorite_games(self):
        """Save favorite games to app config"""
        try:
            self.app.app_config.set('game_settings', 'favorite_games', ','.join(self.favorite_games))
            self.app.app_config.write()
            logger.debug(f"Saved {len(self.favorite_games)} favorite games")
        except Exception as e:
            logger.error(f"Failed to save favorite games: {e}")

    def populate_favorites_swiper(self):
        """Populate the favorites swiper with favorite games"""
        try:
            swiper = self.launcher_view.ids.favorites_swiper
            swiper.clear_widgets()
            
            if not self.favorite_games:
                # Add a placeholder item when no favorites
                placeholder = Favorites(
                    game_module="",
                    game_name=""
                )
                swiper.add_widget(placeholder)
                return
            
            game_index = GameIndex()
            for module_name in self.favorite_games:
                try:
                    game_data = game_index.get_game(module_name)
                    if game_data:
                        favorite_item = Favorites(
                            game_module=module_name,
                            game_name=game_data.get('game_name', module_name)
                        )
                        favorite_item.bind(on_release=lambda x=module_name: self.on_favorite_clicked(x))
                        swiper.add_widget(favorite_item)
                except Exception as e:
                    logger.error(f"Failed to add favorite {module_name}: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to populate favorites swiper: {e}")

    def add_to_favorites(self, module_name: str):
        """Add a game to favorites"""
        if module_name not in self.favorite_games:
            self.favorite_games.append(module_name)
            self.save_favorite_games()
            self.populate_favorites_swiper()
            logger.info(f"Added {module_name} to favorites")

    def remove_from_favorites(self, module_name: str):
        """Remove a game from favorites"""
        if module_name in self.favorite_games:
            self.favorite_games.remove(module_name)
            self.save_favorite_games()
            self.populate_favorites_swiper()
            logger.info(f"Removed {module_name} from favorites")

    def toggle_favorite(self, module_name: str):
        """Toggle favorite status for a game"""
        if module_name in self.favorite_games:
            self.remove_from_favorites(module_name)
        else:
            self.add_to_favorites(module_name)

    def is_favorite(self, module_name: str) -> bool:
        """Check if a game is in favorites"""
        return module_name in self.favorite_games

    def swipe_to_favorite(self, module_name: str):
        """Swipe to a specific favorite game"""
        try:
            swiper = self.launcher_view.ids.favorites_swiper
            if not self.favorite_games:
                return
                
            # Find the index of the favorite
            try:
                index = self.favorite_games.index(module_name)
                swiper.current = index
                logger.info(f"Swiped to favorite {module_name} at index {index}")
            except ValueError:
                logger.warning(f"Game {module_name} not found in favorites")
                
        except Exception as e:
            logger.error(f"Failed to swipe to favorite: {e}")

    def on_favorite_clicked(self, module_name: str):
        """Handle clicking on a favorite item in the swiper"""
        try:
            game_index = GameIndex()
            game_data = game_index.get_game(module_name)
            if game_data:
                game_name = game_data.get('game_name', module_name)
                self.on_game_selected((module_name, game_name))
                logger.info(f"Selected favorite game: {game_name}")
        except Exception as e:
            logger.error(f"Failed to select favorite game {module_name}: {e}")


    def connect(self):
        """Connect to server and launch the selected game module"""
        logger.info("Connect method called!")
        
        # Get the current app context
        current_ctx = self.app.ctx
        
        # Check if we're in initial state by checking if ctx has a 'game' attribute
        if not hasattr(current_ctx, 'game'):
            if not self.selected_game:
                from .dialog import show_error_dialog
                show_error_dialog("No Game Selected", "Please select a game before connecting.")
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
            
            logger.info(f"Attempting to launch module: {self.selected_game[1]}")
            logger.info(f"Server: {server_address}, Password: {'*' * len(password) if password else 'None'}")
            
            try:
                # Show loading screen
                Clock.schedule_once(lambda dt: self.app.loading_layout.show_loading(speed=0.033), 0)

                # Define ready callback to hide loading layout and switch to console
                def ready_callback():
                    self.app.loading_layout.hide_loading()
                    # Switch to console after successful connection
                    Clock.schedule_once(lambda x: self.app.console_init())
                    Clock.schedule_once(lambda x: self.app.change_screen("console"))
                
                # Define error callback to handle connection failures
                def error_callback():
                    self.app.loading_layout.hide_loading()
                    # Stay on launcher screen, don't switch to console
                    # Error dialog will be shown by the context's handle_connection_loss
                
                self.app.client_console_init()

                discover_and_launch_module(
                        self.selected_game[0], server_address = server_address, slot_name = slot_name, \
                        password = password, ready_callback=ready_callback, error_callback=error_callback
                )
                    
            except Exception as e:
                logger.error(f"Failed to launch {self.selected_game[1]} module: {e}")
                # Hide loading layout on error
                self.app.loading_layout.hide_loading()
                # Show error dialog and stay on launcher screen
                from .dialog import show_error_dialog
                show_error_dialog("Launch Error", f"Failed to launch {self.selected_game[1]}: {str(e)}")
        
        else:
            # We're in a game context, check if the selected game matches the current context
            if hasattr(current_ctx, 'game') and current_ctx.game != self.selected_game[1]:
                # Game mismatch - need to rebuild to InitContext first
                logger.info(f"Game mismatch: current={current_ctx.game}, selected={self.selected_game[1]}")
                from .dialog import show_error_dialog
                show_error_dialog("Game Mismatch", 
                                f"Current game ({current_ctx.game}) doesn't match selected game ({self.selected_game[1]}). "
                                "Please restart the client to change games.")
                return
            
            # Game matches, try to connect using the current context
            try:
                # Get connection details from the UI
                server_field = self.launcher_view.ids.server
                port_field = self.launcher_view.ids.port
                
                if not server_field.text:
                    server_field.text = server_field.hint_text
                if not port_field.text:
                    port_field.text = port_field.hint_text
                
                server_address = f"{server_field.text}:{port_field.text}" if server_field.text and port_field.text else None
                
                if not server_address:
                    from .dialog import show_error_dialog
                    show_error_dialog("Connection Error", "Please enter a valid server address and port.")
                    return
                
                logger.info(f"Attempting to connect to: {server_address}")
                
                # Show loading screen
                Clock.schedule_once(lambda dt: self.app.loading_layout.show_loading(speed=0.033), 0)
                
                # Use the context's connect method
                import asyncio
                asyncio.create_task(current_ctx.connect(server_address))
                
                # Hide loading screen after a short delay (connection will handle its own UI updates)
                Clock.schedule_once(lambda dt: self.app.loading_layout.hide_loading(), 2)
                
            except Exception as e:
                logger.error(f"Failed to connect: {e}")
                self.app.loading_layout.hide_loading()
                from .dialog import show_error_dialog
                show_error_dialog("Connection Error", f"Failed to connect: {str(e)}")
