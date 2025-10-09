from __future__ import annotations
"""
SETTINGS SCREEN

Creates the settings screen that will be displayed
when the user clicks the settings button in the
top right corner of the screen.
"""

__all__ = ("SettingsScreen",)
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.metrics import dp
import logging
import os

from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawerMenu, MDNavigationDrawerDivider
from kivymd.uix.navigationdrawer.navigationdrawer import MDNavigationDrawerItem, MDNavigationDrawerLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.label import MDLabel

from mwgg_gui.settings.settings_components import (
    ConnectionSettings,
    ThemingSettings,
    InterfaceSettings,
)

logger = logging.getLogger("Client")

settings_dict = {
    "Connection": [
        {"name": "Profile", "icon": "account"},
        {"name": "Hostname", "icon": "earth"},
        {"name": "Host Authentication", "icon": "shield-account"},
    ],
    "Theming": [
        {"name": "Dark/Light Mode", "icon": "theme-light-dark"},
        {"name": "Color Palette", "icon": "palette"},
        {"name": "Text Colors", "icon": "format-paint"},
        {"name": "Font Sizes", "icon": "format-font"}
    ],
    "Interface": [
        {"name": "Display", "icon": "monitor"},
        {"name": "Layout", "icon": "page-layout-sidebar-left"}
    ],
}

# Define custom widgets in kv language
KV = '''
SettingsNavLayout:
    size_hint_y: None
    height: Window.height-103
    settings_nav_menu: settings_nav_menu

    MDScreenManager:
        id: settings_screen_manager
    MDNavigationDrawer:
        id: settings_nav_drawer
        radius: 0, dp(16), dp(16), 0
        drawer_type: "standard"
        anchor: "left"
        elevation: 10
        md_bg_color: app.theme_cls.surfaceContainerLowColor
        
        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(8)
            padding: [dp(4), dp(4), dp(4), dp(4)]
            
            FitImage:
                source: os.path.join(os.getenv("KIVY_DATA_DIR"), "images", "logo_bg.png")
                size_hint: None,None
                size: dp(256), dp(161)
                pos_hint: {"center_x": 0.5, "top": 1}
            
            NavDrawerMenu:
                id: settings_nav_menu


<NavDrawerMenu>:
    orientation: "vertical"

<NavDrawerLabel>:
    font_style: "Title"
    bold: True
    padding: [0, dp(16), 0, 0]
    theme_text_color: "Custom"
    text_color: app.theme_cls.primaryColor

<NavDrawerItem>:
    MDNavigationDrawerItemLeadingIcon:
        icon: root.icon
        theme_icon_color: "Custom"
        icon_color: app.theme_cls.onPrimaryContainerColor
    MDNavigationDrawerItemText:
        text: root.text
        shorten: True
        theme_text_color: "Custom"
        text_color: app.theme_cls.onSecondaryContainerColor
    MDNavigationDrawerItemTrailingText:
        text: root.trailing_text
        width: dp(32)
        theme_text_color: "Custom"
        text_color: app.theme_cls.onTertiaryContainerColor

<SettingsScreenSection>:
    orientation: "vertical"
    size_hint_y: None
    pos_hint: {"center_x": 0.5}
    height: Window.height-103
    md_bg_color: app.theme_cls.backgroundColor
'''

class SettingsNavLayout(MDNavigationLayout):
    settings_nav_menu: ObjectProperty

class NavDrawerMenu(MDNavigationDrawerMenu):
    menu_label = StringProperty("")

    def on_start(self):
        self.ids.menu.size_hint_x = None
        self.ids.menu.width = self.width - dp(8)

class NavDrawerLabel(MDNavigationDrawerLabel):
    """
    Setting labels (Connection, Theming, Interface)

    TODO: This isn't quite right, needs to be redesigned
    """
    pass

class NavDrawerItem(MDNavigationDrawerItem):
    """
    Setting items (Hostname, Host Authentication, etc.)
    """
    icon = StringProperty("")
    text = StringProperty("")
    trailing_text = StringProperty("")
    screen = StringProperty("")
    manager = ObjectProperty(None)


    def __init__(self, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.bind(on_release=self.screen_callback)

    def screen_callback(self, *args):
        try:
            logger.debug(f"Navigating to screen: {self.screen}")
            self.manager.current = self.screen
            logger.debug("Navigation complete")
        except Exception as e:
            logger.error(f"Error during navigation: {e}", exc_info=True)

class SettingsScreenSection(MDScreen):
    '''
    Generic settings section screen
    For use only on the settings screen, not as a standalone screen
    '''
    name = StringProperty("")
    title = StringProperty("")
    nav_drawer = ObjectProperty(None)

    def __init__(self, name, title, nav_drawer, **kwargs):
        super().__init__(**kwargs)
        logger.debug(f"Initializing SettingsScreenSection: {name}")
        self.nav_drawer = nav_drawer
        self.name = name
        self.title = title
        Clock.schedule_once(lambda x: self.nav_drawer.set_state("open"))
        
        # Create the appropriate settings component based on the section name
        try:
            logger.debug(f"Creating settings component for section: {name.lower()}")
            if name.lower() == "connection":
                logger.debug("Creating ConnectionSettings component")
                self.add_widget(ConnectionSettings())
            elif name.lower() == "theming":
                logger.debug("Creating ThemingSettings component")
                self.add_widget(ThemingSettings())
            elif name.lower() == "interface":
                logger.debug("Creating InterfaceSettings component")
                self.add_widget(InterfaceSettings())
            else:
                logger.warning(f"Unknown section name: {name.lower()}. Expected one of: connection, theming, interface")
                # Add a placeholder widget with a warning message
                warning_box = MDBoxLayout(orientation="vertical", padding=dp(16))
                warning_box.add_widget(MDLabel(
                    text=f"Unknown section: {name}",
                    theme_text_color="Error"
                ))
                self.add_widget(warning_box)
        except Exception as e:
            logger.error(f"Error creating settings component for {name}: {e}", exc_info=True)
            # Add an error widget
            error_box = MDBoxLayout(orientation="vertical", padding=dp(16))
            error_box.add_widget(MDLabel(
                text=f"Error loading section: {name}",
                theme_text_color="Error"
            ))
            self.add_widget(error_box)

class SettingsScreen(MDScreen):
    '''
    Main settings screen to call from the application
    '''
    settings_nav_drawer: ObjectProperty
    settings_screen_manager: MDScreenManager
    nav_layout: SettingsNavLayout
    nav_menu: NavDrawerMenu
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.debug("Initializing SettingsScreen")
        self.name = "settings"
        self.nav_layout = Builder.load_string(KV)
        logger.debug(f"Loaded nav_layout: {self.nav_layout}")
        
        self.settings_nav_drawer = self.nav_layout.ids.settings_nav_drawer
        self.settings_nav_drawer.type = "standard"
        logger.debug(f"Retrieved nav_drawer: {self.settings_nav_drawer}")
        
        self.settings_screen_manager = self.nav_layout.ids.settings_screen_manager
        self.setup_sections()
        logger.debug(f"Retrieved screen_manager: {self.settings_screen_manager}")
        
        self.add_widget(self.nav_layout)
        
        logger.debug("Added nav_layout to screen")
        
        # Set up the navigation menu after everything else is initialized
        Clock.schedule_once(self.setup_navigation_menu)
    
    def setup_sections(self, *args):
        logger.debug("Setting up settings sections")
        for section in settings_dict:
            logger.debug(f"Adding section: {section}")
            section_name = section.lower()
            logger.debug(f"Section name (lowercase): {section_name}")
            self.settings_screen_manager.add_widget(SettingsScreenSection(name=section_name, title=section, nav_drawer=self.settings_nav_drawer))
        self.settings_screen_manager.current = "interface"
        logger.debug("Finished setting up sections")
    
    def setup_navigation_menu(self, *args):
        """Set up the navigation menu with all its items."""
        logger.debug("Setting up navigation menu")
        self.nav_menu = self.nav_layout.settings_nav_menu
        self.nav_menu.on_start()
        
        for screen_name in self.settings_screen_manager.screen_names:
            logger.debug(f"Adding menu item for screen: {screen_name}")
            # Add section
            self.nav_menu.add_widget(NavDrawerLabel(
                text=screen_name.capitalize()    
            ))

            for item in settings_dict[screen_name.capitalize()]:
                logger.debug(f"Adding menu item: {item['name']}")
                self.nav_menu.add_widget(NavDrawerItem(
                    manager=self.settings_screen_manager,
                    icon=item["icon"],
                    text=item["name"],
                    screen=screen_name
                ))
            
            # Add divider
            if screen_name != "interface":
                self.nav_menu.add_widget(MDNavigationDrawerDivider())
        logger.debug("Finished setting up navigation menu")
