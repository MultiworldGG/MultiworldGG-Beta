import os
import logging
import sys
import typing
import re
import io
import pkgutil
import asyncio
import subprocess
import time

from collections import deque
from PIL import Image as PILImage, ImageSequence


# from worlds.alttp.Rom import text_addresses

# Check if we're in a test environment
import sys
import os

# Allow Kivy to be imported during testing
if "pytest" not in sys.modules and "unittest" not in sys.modules and "test" not in sys.argv[0]:
    assert "kivy" not in sys.modules, "gui needs instansiation first"

sys.path.append(os.path.join(os.path.dirname(__file__), "kivydi"))

if sys.platform == "win32":
    #import ctypes

    # kivy 2.2.0 introduced DPI awareness on Windows, but it makes the UI enter an infinitely recursive re-layout
    # by setting the application to not DPI Aware, Windows handles scaling the entire window on its own, ignoring kivy's
    from ctypes import windll, c_int64
    windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))
    
# from CommonClient import console_loop
# from MultiServer import console
# apname = "Archipelago" if not Utils.archipelago_name else Utils.archipelago_name

# if Utils.is_frozen():
from Utils import local_path

from kivy.config import Config as MWKVConfig
from kivy.config import ConfigParser

#####
##### The config is an ACTUAL FILE THAT CAN SAVE ANY SETTING
##### THERE IS EVEN A VIEW FOR IT
##### AND WE CAN ADD OUR OWN SHIT
#####

MWKVConfig.set("input", "mouse", "mouse,disable_multitouch")
MWKVConfig.set("kivy", "exit_on_escape", "0")
MWKVConfig.set("kivy", "default_font", ['Inter', 
                                    os.path.join(local_path(),"data","fonts","Inter-Regular.ttf"), 
                                    os.path.join(local_path(),"data","fonts","Inter-Italic.ttf"),
                                    os.path.join(local_path(),"data","fonts","Inter-Bold.ttf"),
                                    os.path.join(local_path(),"data","fonts","Inter-BoldItalic.ttf")])
MWKVConfig.set("graphics", "width", "1099")
MWKVConfig.set("graphics", "height", "699")
MWKVConfig.set("graphics", "custom_titlebar", "1")
MWKVConfig.set("graphics", "window_icon", os.path.join(local_path(),"data", "icon.png"))
MWKVConfig.set("graphics", "minimum_height", "700")
MWKVConfig.set("graphics", "minimum_width", "600")
MWKVConfig.set("graphics", "shaped", 0)
MWKVConfig.set("graphics", "focus", "False")

from kivy.core.window import Window
Window.opacity = 0
Window.clearcolor = [0,0,0,0]
Window.borderless = True
Window.set_title("MultiWorldGG")

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.appbar import MDBottomAppBar
from kivy.uix.effectwidget import EffectWidget
from kivymd.uix.textfield import MDTextField

from NetUtils import KivyMarkupJSONtoTextParser, JSONMessagePart, SlotType, HintStatus
# from Utils import async_start, get_input_text_from_response
from .mw_theme import RegisterFonts, DefaultTheme

from .titlebar import Titlebar
from .console import ConsoleScreen
from .hintscreen import HintScreen
from .settings_screen import SettingsScreen
from .topappbar import TopAppBarLayout
from .launcher import LauncherScreen
from .kivydi.loadinglayout import MWGGLoadingLayout
from .bottomappbar import BottomAppBar, BottomBarTextInput
from .kvui_functions import MW_ServerLabel

if typing.TYPE_CHECKING:
    import CommonClient

    context_type = CommonClient.CommonContext
else:
    context_type = object

class MainLayout(MDAnchorLayout):
    pass

class NavLayout(MDNavigationLayout):
    pass

class MainScreenMgr(MDScreenManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.transition = MDFadeSlideTransition()

class MultiMDApp(MDApp): 

    logging_pairs = [
        ("Client", "Archipelago"),
    ]

    title = "MultiWorldGG"

    title_bar: Titlebar
    main_layout: MainLayout
    navigation_layout: NavLayout
    loading_layout: MWGGLoadingLayout
    top_appbar_layout: TopAppBarLayout
    screen_manager: MainScreenMgr

    console_screen: ConsoleScreen
    hint_screen: HintScreen
    settings_screen: SettingsScreen
    launcher_screen: LauncherScreen

    bottom_appbar: BottomAppBar
    launcher_text_input: BottomBarTextInput
    console_text_input: BottomBarTextInput
    hint_text_input: BottomBarTextInput
    
    theme_mw: DefaultTheme
    top_appbar_menu: MDDropdownMenu
    pixelate_effect: EffectWidget
    ui_console: ObjectProperty

    def __init__(self, ctx: context_type, **kwargs):
        super().__init__(**kwargs)
        # Use the existing Kivy Config singleton for Kivy settings
        self.config = MWKVConfig
        # Create app-specific config
        try:
            self.app_config = ConfigParser(name='app')
        except ValueError:
            # If parser already exists, get the existing one
            self.app_config = ConfigParser.get_configparser('app')

        # Ensure client.ini exists with default values
        config_path = os.path.join(os.environ["KIVY_HOME"], "client.ini")
        if os.path.exists(config_path):
            # Read existing config file
            self.app_config.read(config_path)
        else:
            self.build_config(self.app_config)
            self.app_config.write()

        RegisterFonts(self, self.app_config.get('client', 'monospace_font', fallback='Argon'))
        
        self.ctx = ctx

        self.icon = os.path.join(os.path.curdir, "icon.ico")
        self.theme_mw = DefaultTheme(self.app_config)
        
        # Buffer for messages before console is initialized
        self._message_buffer = []

    def get_application_config(self):
        """Get the path to the configuration file"""
        return os.path.join(os.environ["KIVY_HOME"], "client.ini")

    def build_config(self, config):
        """Build the configuration file with default values"""
        config.setdefaults('client', {
            'slot': '',
            'alias': '',
            'pronouns': '',
            'in_call': '0',
            'in_bk': '0',
            'hostname': 'multiworld.gg',
            'port': '38281',
            'password': '',
            'admin_password': '',
            'theme_style': 'Dark',
            'primary_palette': 'Purple',
            'font_scale': '1.0',
            'monospace_font': 'Argon',
            'device_orientation': '0'
        })

    def on_config_change(self, config, section, key, value):
        """Handle configuration changes"""
        if section == 'client':
            if key == 'theme_style':
                self.theme_cls.theme_style = value
            elif key == 'primary_palette':
                self.theme_cls.primary_palette = value
            elif key == 'font_scale':
                # Update font sizes based on scale
                scale_factor = float(value)
                self.theme_cls.font_styles = {
                    style: {
                        size: {
                            **style_data,
                            'font-size': int(style_data['font-size'] * scale_factor)
                        } for size, style_data in sizes.items()
                    } for style, sizes in self.theme_cls.font_styles.items()
                }
        elif section == 'graphics':
            if key == 'fullscreen':
                Window.fullscreen = value == '1'
        
        # Write changes to app config file
        self.app_config.write()

    def set_opacity(self, dt):
        Window.opacity = 1
        Window.size = (1100, 700)
        Window.clearcolor = [0,0,0,1]

    def terminate_splash_screen_wrapper(self):
        """Wrapper to call the terminate_splash_screen function from MultiWorld"""
        from MultiWorld import terminate_splash_screen
        terminate_splash_screen(self.ctx.splash_process)
        Clock.schedule_once(self.set_opacity)

    def on_start(self):
        """Set up additional build necessities that
        cannot be done in the constructor"""

        # titlebar bindings
        Window.bind(on_restore=self.title_bar.tb_onres)
        Window.bind(on_maximize=self.title_bar.tb_onmax)
        Window.bind(on_close=lambda x: self.on_stop())

        # self.ui_console = self.console_screen.ui_console
        # self.ui_console.console()

        self.change_screen("launcher")

        def on_start(*args):
            self.root.md_bg_color = self.theme_cls.surfaceColor
            
            # Initialize and show loading animation
            self.loading_layout = MWGGLoadingLayout()
            self.loading_layout.size = (self.root.width, self.root.height)
            self.loading_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            self.root_layout.add_widget(self.loading_layout)


        super().on_start()
        Clock.schedule_once(on_start)
        # Terminate the splash screen after the UI is fully initialized
        Clock.schedule_once(lambda dt: self.terminate_splash_screen_wrapper())


    def build(self):
        '''
        This is the base app infrastructure for the
        gui. It sets up the theme, layouts, and screens.
        '''

        # Themeing
        self.theme_cls.theme_style = self.theme_mw.theme_style
        self.theme_cls.primary_palette = self.theme_mw.primary_palette
        self.theme_cls.dynamic_scheme_name = self.theme_mw.dynamic_scheme_name
        self.theme_mw.recolor_atlas()
        self.theme_cls.theme_style_switch_animation = True

        # Layouts and screens are in layer order
        # Root layout - specifically to blur everything during loading
        self.root_layout = MDFloatLayout()
        self.pixelate_effect = EffectWidget()

        # Main window layout
        self.main_layout = MainLayout()
        self.main_layout.anchor_x='left'
        self.main_layout.anchor_y='top'

        self.title_bar = Titlebar()
        Window.set_custom_titlebar(self.title_bar)

        # Navigation layout (bottom sheet)
        self.navigation_layout = NavLayout()

        # Top appbar layout
        self.top_appbar_layout = TopAppBarLayout()
        self.top_appbar_menu = None
        self.top_appbar_layout.top_appbar.address_bar_label = MW_ServerLabel()
        
        # Screen manager
        # Screens are under the appbar and titlebar
        self.screen_manager = MainScreenMgr()

        # Set up navigation layout
        self.navigation_layout.add_widget(self.screen_manager)

        # Add user interface elements to main layout
        self.main_layout.add_widget(self.navigation_layout)
        self.main_layout.add_widget(self.top_appbar_layout)
        self.main_layout.add_widget(self.title_bar)

        # Add the main layout to the root layout
        self.pixelate_effect.add_widget(self.main_layout)
        self.root_layout.add_widget(self.pixelate_effect)
        
        return self.root_layout

    def on_stop(self):
        """Handle application shutdown properly"""
        try:
            # Remove console handler from logger to prevent AttributeError during shutdown
            if hasattr(self, 'console_handler') and self.console_handler:
                try:
                    client_logger = logging.getLogger("Client")
                    client_logger.removeHandler(self.console_handler)
                except Exception:
                    pass
            
            # Mark that we're disconnecting intentionally to prevent auto-reconnect
            if hasattr(self.ctx, 'disconnected_intentionally'):
                self.ctx.disconnected_intentionally = True
            
            # Cancel any ongoing tasks
            if hasattr(self.ctx, 'server_task') and self.ctx.server_task:
                self.ctx.server_task.cancel()
            
            if hasattr(self.ctx, 'autoreconnect_task') and self.ctx.autoreconnect_task:
                self.ctx.autoreconnect_task.cancel()
            
            if hasattr(self.ctx, 'keep_alive_task') and self.ctx.keep_alive_task:
                self.ctx.keep_alive_task.cancel()
            
            # Close server connection if it exists
            if hasattr(self.ctx, 'server') and self.ctx.server and hasattr(self.ctx.server, 'socket'):
                if not self.ctx.server.socket.closed:
                    # Schedule the socket close to avoid blocking
                    asyncio.create_task(self.ctx.server.socket.close())
            
            # Set the exit event to signal shutdown
            self.ctx.exit_event.set()
            
        except Exception as e:
            # Log any errors during shutdown but don't let them prevent shutdown
            import logging
            logger = logging.getLogger("gui")
            logger.warning(f"Error during shutdown: {e}")
            # Still set the exit event to ensure shutdown proceeds
            self.ctx.exit_event.set()

    def update_colors(self):
        '''
        This function is called when the theme color is changed.
        It updates the primary palette, forces a background color 
        refresh and recolors the atlas which controls the little 
        teeny graphics in the gui.
        '''
        self.theme_cls.primary_palette = self.theme_mw.primary_palette
        self.root.md_bg_color = self.theme_cls.surfaceColor
        self.theme_mw.recolor_atlas()

    def change_theme(self):
        '''
        This function is called when the theme is changed.
        It updates the theme style (light/dark) and primary palette,
        forces a background color refresh and recolors the atlas
        which controls the little teeny graphics in the gui.
        '''
        self.theme_cls.theme_style = self.theme_mw.theme_style
        self.theme_cls.primary_palette = self.theme_mw.primary_palette
        self.root.md_bg_color = self.theme_cls.surfaceColor
        self.theme_mw.recolor_atlas()

    def change_screen(self, item):
        '''
        This function is called when the screen is changed.
        It updates the current screen and dismisses menu
        with the screen names.
        '''
        self.screen_manager.current_heroes = ["logo"]
        if item in self.screen_manager.screen_names:
            self.screen_manager.current = item
            if self.top_appbar_menu:
                self.top_appbar_menu.dismiss()
        else:
            self._create_screen(item)

    def _create_screen(self, item):
        '''
        This function is called when the screen is changed.
        It updates or creates the current screen and dismisses 
        the menu with the screen names.
        '''
        if item == "settings":
            self.settings_screen = SettingsScreen()
            self.screen_manager.add_widget(self.settings_screen)
            self.screen_manager.current = "settings"
        elif item == "hint":
            self.hint_screen = HintScreen()
            self.screen_manager.add_widget(self.hint_screen)
            self.screen_manager.current = "hint"
            self.hint_text_input = self.hint_screen.bottom_appbar.text_input
            self.hint_text_input.bind(on_enter=self.on_message)
        elif item == "launcher":
            self.launcher_screen = LauncherScreen()
            self.screen_manager.add_widget(self.launcher_screen)
            self.screen_manager.current = "launcher"
            self.launcher_text_input = self.launcher_screen.bottom_appbar.text_input  
            self.launcher_text_input.bind(on_enter=self.on_message)

    def console_init(self):
        self.commandprocessor = self.ctx.command_processor(self.ctx)
        self.ui_console = self.console_screen.ui_console
        self.console_handler = self.ui_console.console_handler()
        
        # Add console handler to Client logger
        client_logger = logging.getLogger("Client")
        client_logger.addHandler(self.console_handler)
        
        # Flush any buffered messages
        if self._message_buffer:
            for message in self._message_buffer:
                self.console_handler.queue.put_nowait(message)
            self._message_buffer.clear()

    def client_console_init(self):
        self.console_screen = ConsoleScreen()
        self.screen_manager.add_widget(self.console_screen)
        self.console_text_input = self.console_screen.bottom_appbar.text_input
        self.console_text_input.bind(on_enter=self.on_message)

    def _create_menu_item(self, item):
        """Create a menu item with proper binding
        to change screens when the item is pressed"""
        return {
            "text": item.capitalize(),
            "divider": None,
            "on_release": lambda x=item: self._menu_item_callback(x)
        }
        
    def _menu_item_callback(self, item):
        """Callback for menu items to change screens"""
        self.change_screen(item.lower())
        
    def open_top_appbar_menu(self, menu_button):
        """Open dropdown menu to change screens 
        when menu button is pressed"""
        if not self.top_appbar_menu:
            menu_items = [
                self._create_menu_item(item)
                for item in ["console", "settings", "launcher"]
            ]

            self.top_appbar_menu = MDDropdownMenu(
                caller=menu_button,
                items=menu_items,
                width_mult=3,
            )
        self.top_appbar_menu.open()

    def update_address_bar(self, text: str):
        if hasattr(self, "top_appbar"):
            self.top_appbar.update_address_bar(text)

    def on_message(self, textinput: MDTextField):
        try:
            input_text = textinput.text.strip()
            if textinput.silent_prefix:
                input_text = textinput.silent_prefix + input_text
            textinput.text = ""
            textinput.update_history(input_text)

            if self.ctx.input_requests > 0:
                self.ctx.input_requests -= 1
                self.ctx.input_queue.put_nowait(input_text)
            elif is_command_input(input_text):
                self.ctx.on_ui_command(input_text)
                self.commandprocessor(input_text)
            elif input_text:
                self.commandprocessor(input_text)

        except Exception as e:
            logging.getLogger("Client").exception(e)

    def focus_textinput(self):
        if self.ctx.slot_info:  # Only focus console if we have slot info
            self.change_screen("console")
            self.console_text_input.animate_text_input(self.bottom_appbar, {"id": "console_text_input"})

    def print_json(self, data: typing.List[JSONMessagePart]):
        self.focus_textinput()
        # Convert the list of JSONMessagePart to a single text message
        # Use KivyMarkupJSONtoTextParser to convert the JSON message parts to Kivy markup with hex colors
        parser = KivyMarkupJSONtoTextParser(self.ctx)
        text = parser(data)
        
        # Check if console_handler exists, if not buffer the message
        if hasattr(self, 'console_handler') and self.console_handler:
            self.console_handler.queue.put_nowait(text)
        else:
            # Buffer the message until console is initialized
            self._message_buffer.append(text)

    def update_hints(self):
        hints = self.ctx.stored_data.get(f"_read_hints_{self.ctx.team}_{self.ctx.slot}", [])
        #self.hint_log.refresh_hints(hints)

def is_command_input(string: str) -> bool:
    return len(string) > 0 and string[0] in "/!"
# KivyMDGUI().run()

# def run_client(*args):
#     class TextContext(GuiContext):
#         tags = {"TextOnly"}
#         game = ""
#         items_handling = 0b111
#         want_slot_data = False

#     async def main(args):
#         ctx = TextContext()
        
#         ctx.run_gui()

#         await ctx.exit_event.wait()
#         await ctx.shutdown()
#         sys.exit()

#     asyncio.run(main(args))

# if __name__ == '__main__':
#     run_client(*sys.argv[1:])