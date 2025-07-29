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

#os.environ["KCFG_GRAPHICS_WINDOW_STATE"] = "visible"
os.environ["KIVY_NO_CONSOLELOG"] = "0"
os.environ["KIVY_NO_FILELOG"] = "0"
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_LOG_ENABLE"] = "1"

# from CommonClient import console_loop
# from MultiServer import console
# apname = "Archipelago" if not Utils.archipelago_name else Utils.archipelago_name

# if Utils.is_frozen():
from Utils import local_path
os.environ["KIVY_DATA_DIR"] = os.path.join(local_path(),"venv","Lib","site-packages","kivy","data")
os.environ["KIVY_HOME"] = os.path.join(local_path(),"data", "kivy_home")
os.makedirs(os.environ["KIVY_HOME"], exist_ok=True)

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

from NetUtils import KivyMarkupJSONtoTextParser, JSONMessagePart, SlotType, HintStatus
# from Utils import async_start, get_input_text_from_response
from .mw_theme import RegisterFonts, DefaultTheme

from .titlebar import Titlebar
from .console import ConsoleScreen
from .hintscreen import HintScreen
from .settings_screen import SettingsScreen
from .topappbar import TopAppBarLayout, TopAppBar
from .launcher import LauncherScreen
from .kivydi.loadinglayout import MWGGLoadingLayout

if typing.TYPE_CHECKING:
    import CommonClient

    context_type = CommonClient.CommonContext
else:
    context_type = object

class BottomAppBar(MDBottomAppBar):
    def hide_me(self, *args):
        self.hide_bar()
    def show_me(self, *args):
        self.show_bar()

class MainLayout(MDAnchorLayout):
    pass

class NavLayout(MDNavigationLayout):
    pass

class MainScreenMgr(MDScreenManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.transition = MDFadeSlideTransition()

# class GuiContext:
#     def __init__(self):
#         self.loop = asyncio.get_event_loop()
#         self.exit_event = asyncio.Event()
#         self.splash_process = None

#     def run_gui(self):
#         """Run the GUI as self.ui_task."""
#         self.ui = MultiMDApp(self)
#         # Launch splash screen before starting the UI
#         self.ui.launch_splash_screen()
#         self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

#     async def shutdown(self):
#         if self.ui_task:
#             await self.ui_task

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
    
    theme_mw: DefaultTheme
    top_appbar_menu: MDDropdownMenu
    splash_process = None
    pixelate_effect: EffectWidget
    ui_console: ObjectProperty

    def __init__(self, ctx: context_type, **kwargs):
        super().__init__(**kwargs)
        RegisterFonts(self)
        self.ctx = ctx
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
            
        self.icon = os.path.join(os.path.curdir, "icon.ico")
        self.theme_mw = DefaultTheme(self.app_config)

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

    def launch_splash_screen(self):
        """Launch the splash screen as a separate process"""
        try:
            # Get the directory of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            splash_path = os.path.join(script_dir, "splashscreen.py")
            
            # Launch the splash screen process
            if sys.platform == "win32":
                self.splash_process = subprocess.Popen(
                    [sys.executable, splash_path],
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                self.splash_process = subprocess.Popen(
                    [sys.executable, splash_path]
                )
            
            logging.info(f"Splash screen launched with PID: {self.splash_process.pid}")
            return self.splash_process
        except Exception as e:
            logging.error(f"Failed to launch splash screen: {e}")
            return None

    def terminate_splash_screen(self):
        """Send termination signal to the splash screen"""
        try:
            # Create a termination file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            flag_path = os.path.join(script_dir, "terminate_splash.flag")
            
            with open(flag_path, "w") as f:
                f.write("terminate")
            
            logging.info("Termination signal sent to splash screen")
            
            # Clean up the flag file
            if os.path.exists(flag_path):
                os.remove(flag_path)
                
            # If the process is still running, terminate it
            if self.splash_process and self.splash_process.poll() is None:
                self.splash_process.terminate()
                self.splash_process.wait(timeout=2)

        except Exception as e:
            logging.error(f"Failed to terminate splash screen: {e}")
        Clock.schedule_once(self.set_opacity)

    def set_opacity(self, dt):
        Window.opacity = 1
        Window.size = (1100, 700)
        Window.clearcolor = [0,0,0,1]

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
        Clock.schedule_once(lambda dt: self.terminate_splash_screen())


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
        elif item == "launcher":
            self.launcher_screen = LauncherScreen()
            self.screen_manager.add_widget(self.launcher_screen)
            self.screen_manager.current = "launcher"

    def _console_init(self):
        self.commandprocessor = self.ctx.command_processor(self.ctx)
        self.ui_console = self.console_screen.ui_console
        self.console_handler = self.ui_console.console_handler()

    def client_console_init(self):
        self.console_screen = ConsoleScreen()
        self.screen_manager.add_widget(self.console_screen)
        Clock.schedule_once(lambda x: self._console_init())

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

    def focus_textinput(self):
        self.change_screen("console")

    def print_json(self, data: typing.List[JSONMessagePart]):
        self.focus_textinput()
        # Convert the list of JSONMessagePart to a single text message
        # Use KivyMarkupJSONtoTextParser to convert the JSON message parts to Kivy markup with hex colors
        parser = KivyMarkupJSONtoTextParser(self.ctx)
        print(data)
        text = parser(data)
        print(text)
        # Put the text string into the queue instead of the list
        self.console_handler.queue.put_nowait(text)

    def on_message(self):
        try:
            input_text = self.bottom_sheet.input_field.text.strip()
            self.bottom_sheet.input_field.text = ""
            #self.bottom_sheet.input_field.update_history(input_text)

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