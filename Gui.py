import os
import logging
import sys
import typing
import asynckivy
from datetime import datetime, UTC
from multiprocessing import Queue
from logging.handlers import QueueHandler

# Check if we're in a test environment

# Allow Kivy to be imported during testing
if "pytest" not in sys.modules and "unittest" not in sys.modules and "test" not in sys.argv[0]:
    assert "kivy" not in sys.modules, "gui needs instansiation first"

sys.path.append(os.path.join(os.path.dirname(__file__), "kivydi"))

# if sys.platform == "win32":
#     #import ctypes

#     # kivy 2.2.0 introduced DPI awareness on Windows, but it makes the UI enter an infinitely recursive re-layout
#     # by setting the application to not DPI Aware, Windows handles scaling the entire window on its own, ignoring kivy's
#     from ctypes import windll, c_int64
#     windll.user32.SetProcessDpiAwarenessContext(c_int64(-4))
    
# from CommonClient import console_loop
# from MultiServer import console
# apname = "Archipelago" if not Utils.archipelago_name else Utils.archipelago_name

# if Utils.is_frozen():
from BaseUtils import local_path

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
MWKVConfig.set("graphics", "focus", "False")

from kivy.core.window import Window
Window.opacity = 0
Window.clearcolor = [0,0,0,0]
Window.borderless = True
Window.set_title("MultiWorldGG")

from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.appbar import MDBottomAppBar
from kivy.uix.effectwidget import EffectWidget
from kivymd.uix.textfield import MDTextField

from NetUtils import KivyMarkupJSONtoTextParser, JSONMessagePart, SlotType, HintStatus, MWGGUIHintStatus
# from Utils import async_start, get_input_text_from_response
from mwgg_gui.components.mw_theme import RegisterFonts, DefaultTheme

from mwgg_gui.components.titlebar import Titlebar
from mwgg_gui.console.console import ConsoleScreen
from mwgg_gui.hint.hintscreen import HintScreen
from mwgg_gui.settings.settings_screen import SettingsScreen
from mwgg_gui.components.topappbar import TopAppBarLayout
from mwgg_gui.launcher.launcher import LauncherScreen
from mwgg_gui.loadanimlayout import MWGGLoadingLayout
from mwgg_gui.components.bottomappbar import BottomAppBar, BottomBarTextInput
from mwgg_gui.components.guidataclasses import UIPlayerData, UIHint

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

    ui_player_data: dict[int, UIPlayerData]
    ui_hint_data: dict[int, dict[int, list[UIHint]]]
    text_buffer: Queue

    _show_all_hints: BooleanProperty(False)

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
        
        # Buffer for messages
        self.text_buffer = Queue(maxsize=1000) 
        self.ui_hint_data = {}
        self.ui_player_data = {}

        self._show_all_hints = False

    def get_application_config(self):
        """Get the path to the configuration file"""
        return os.path.join(os.environ["KIVY_HOME"], "client.ini")

    def build_config(self, config):
        """Build the configuration file with default values"""
        config.setdefaults('client', {
            'slot': '',
            'alias': '',
            'pronouns': '',
            'in_call': 'False',
            'in_bk': 'False',
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
        terminate_splash_screen()
        Clock.schedule_once(self.set_opacity)

    @staticmethod
    def qotd():
        with open(local_path("data", "QOTD.txt"), "r", encoding="utf-8") as f:
            qotd_lines = f.readlines()
            if qotd_lines:
                todays_qotd = qotd_lines[int(int(datetime.now(UTC).strftime("%m%d")) % len(qotd_lines))]
                return "QOTD for " + datetime.now(UTC).strftime("%m/%d/%Y") + ": " + todays_qotd
        return "Blame TreZ"

    def on_start(self):
        """Set up additional build necessities that
        cannot be done in the constructor"""
        # titlebar bindings
        Window.bind(on_restore=self.title_bar.tb_onres)
        Window.bind(on_maximize=self.title_bar.tb_onmax)
        Window.bind(on_close=lambda x: self.on_stop())

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
        #self.top_appbar_layout.top_appbar.address_bar_label = MW_ServerLabel()
        
        # Screen manager
        # Screens are under the appbar and titlebar
        self.screen_manager = MainScreenMgr()

        # Set up navigation layout
        self.navigation_layout.add_widget(self.screen_manager)

        # Add user interface elements to main layout
        self.main_layout.add_widget(self.navigation_layout)
        self.main_layout.add_widget(self.top_appbar_layout)
        self.main_layout.add_widget(self.title_bar)

        # Add the main layout directly to root layout when no effects are active
        # This prevents matrix transformation interference with StencilView
        self.root_layout.add_widget(self.main_layout)
        
        return self.root_layout

    def enable_effects(self):
        """Enable EffectWidget with pixelate effect for loading screen"""
        if hasattr(self, 'pixelate_effect') and hasattr(self, 'main_layout'):
            # Remove main_layout from root_layout
            self.root_layout.remove_widget(self.main_layout)
            # Add main_layout to EffectWidget
            self.pixelate_effect.add_widget(self.main_layout)
            # Add EffectWidget to root_layout
            self.root_layout.add_widget(self.pixelate_effect)
            # Add pixelate effect
            if hasattr(self, 'loading_layout') and self.loading_layout.loading:
                from kivy.uix.effectwidget import PixelateEffect
                self.loading_layout.effect_app = PixelateEffect(pixel_size=3)
                self.pixelate_effect.effects = [self.loading_layout.effect_app]
            
            # Ensure loading_layout is on top of the EffectWidget (img_box needs to be above pixelated content)
            # Remove from current parent if it exists
            if hasattr(self, 'loading_layout') and self.loading_layout.parent:
                self.loading_layout.parent.remove_widget(self.loading_layout)
            # Add to root_layout to be on top of the EffectWidget
            if hasattr(self, 'loading_layout'):
                self.root_layout.add_widget(self.loading_layout)

    def disable_effects(self):
        """Disable EffectWidget to prevent matrix transformation interference with StencilView"""
        if hasattr(self, 'pixelate_effect') and hasattr(self, 'main_layout'):
            # Remove EffectWidget from root_layout
            self.root_layout.remove_widget(self.pixelate_effect)
            # Remove main_layout from EffectWidget
            self.pixelate_effect.remove_widget(self.main_layout)
            # Add main_layout directly to root_layout
            self.root_layout.add_widget(self.main_layout)
            # Clear effects
            self.pixelate_effect.effects = []
            
            # Ensure loading_layout is on top of the main_layout (img_box needs to be above content)
            # Remove from current parent if it exists
            if hasattr(self, 'loading_layout') and self.loading_layout.parent:
                self.loading_layout.parent.remove_widget(self.loading_layout)
            # Add to root_layout to be on top of the main_layout
            if hasattr(self, 'loading_layout'):
                self.root_layout.add_widget(self.loading_layout)

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
            self.screen_manager.current = item
            if self.top_appbar_menu:
                self.top_appbar_menu.dismiss()

    def _create_screen(self, item):
        '''
        This function is called when the screen is changed.
        It updates or creates the current screen and dismisses 
        the menu with the screen names.
        '''
        if item == "settings":
            self.settings_screen = SettingsScreen()
            self.screen_manager.add_widget(self.settings_screen)
        elif item == "hint":
            self.hint_screen = HintScreen()
            self.screen_manager.add_widget(self.hint_screen)
            self.hint_text_input = self.hint_screen.bottom_appbar.text_input
            self.hint_text_input.bind(on_enter=self.on_message)
        elif item == "launcher":
            self.launcher_screen = LauncherScreen()
            self.screen_manager.add_widget(self.launcher_screen)
            self.launcher_text_input = self.launcher_screen.bottom_appbar.text_input  
            self.launcher_text_input.bind(on_enter=self.on_message)

    def console_init(self):
        '''
        This function is called when the console is initialized.
        It sets up the command processor and the console handler.
        It cannot be called before the console screen is created.
        '''
        # Prevent multiple initializations
        if hasattr(self, 'commandprocessor'):
            return
            
        self.commandprocessor = self.ctx.command_processor(self.ctx)
        self.ui_console = self.console_screen.ui_console
        self.ui_console.text_console.text_default_color = self.theme_mw.markup_tags_theme.default_color[0 if self.theme_mw.theme_style == "Light" else 1]
        self.console_handler = self.ui_console.console_handler()
        
        # Remove any existing console handlers to prevent duplicates
        client_logger = logging.getLogger("Client")
        # Remove handlers that are QueueHandler instances (our console handlers)
        handlers_to_remove = [h for h in client_logger.handlers if isinstance(h, QueueHandler)]
        for handler in handlers_to_remove:
            client_logger.removeHandler(handler)
        
        # Add the new console handler
        client_logger.addHandler(self.console_handler)


    def client_console_init(self):
        '''
        This function is called when the console is initialized.
        It sets up the command processor and the console handler.
        It cannot be called before the connection is established,
        because we need the specific command processor and context.
        '''
        if "console" not in self.screen_manager.screens:
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
        if self.top_appbar_menu:
            self.top_appbar_menu.dismiss()
        
    def open_top_appbar_menu(self, menu_button):
        """Open dropdown menu to change screens 
        when menu button is pressed"""
        if not self.top_appbar_menu:
            menu_items = [
                self._create_menu_item(item)
                for item in list(set(["settings", "launcher"] + self.screen_manager.screen_names))
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
        '''
        This function is called when the text input is focused.
        It changes the screen to the console and focuses the text input.
        '''
        if self.ctx.slot_info:  # Only focus console if we have slot info
            self.change_screen("console")

    def on_connect(self):
        '''
        This function is called when the connection is established.
        It sets up the UI player data and updates the hints.
        '''
          
        pronouns = ""
        in_call = False
        in_bk = False
        
        for slot, name in self.ctx.player_names.items():
            if self.ctx.slot_concerns_self(slot):
                pronouns = self.app_config.get('client', 'pronouns', fallback='')
            self.ui_hint_data[slot] = {}
            self.ui_player_data[slot] = UIPlayerData(
                slot_id=slot,
                slot_name=name,
                avatar="",
                pronouns = pronouns,
                bk_mode=in_bk,
                in_call=in_call,
                end_user=self.ctx.slot_concerns_self(slot),
                game_status="PLAYING",
                game=self.ctx.slot_info[slot].game,
                hints=self.ui_hint_data[slot],
            )

        self.update_mwgg_hints()
        self.update_hints()
        self.set_pronouns()
        self._create_screen("hint")


    def print_json(self, data: typing.List[JSONMessagePart]):
        # Convert the list of JSONMessagePart to a single text message
        # Use KivyMarkupJSONtoTextParser to convert the JSON message parts to Kivy markup with hex colors
        parser = KivyMarkupJSONtoTextParser(self.ctx)
        text = parser(data)
        
        # Always use the text buffer for consistency
        self.text_buffer.put_nowait(text)

    def set_pronouns(self):
        pronouns = self.ui_player_data[self.ctx.slot].pronouns
        tags = list(self.ctx.tags)
        if any(tag.startswith("pronouns") for tag in tags):
            tags.remove(next(tag for tag in tags if tag.startswith("pronouns")))
        tags.append(f"pronouns:{pronouns}")
        asynckivy.start(self.ctx.update_tags(tags))

    def set_deafen(self):
        tags = list(self.ctx.tags)
        if "in_call" in tags:
            tags.remove("in_call")
        else:
            tags.append("in_call")
        asynckivy.start(self.ctx.update_tags(tags))
    
    def set_bk(self):
        tags = list(self.ctx.tags)
        if "in_bk" in tags:
            tags.remove("in_bk")
        else:
            tags.append("in_bk")
        asynckivy.start(self.ctx.update_tags(tags))

    def update_hints(self):
        hints = self.ctx.stored_data.get(f"_read_hints_{self.ctx.team}_{self.ctx.slot}", [])
        mwgg_hints = self.ctx.stored_data.get(f"_read_hints_{self.ctx.team}_{self.ctx.slot}_mwgg", {})
        if hints:
            self.refresh_hints(hints, mwgg_hints)


    def refresh_hints(self, hints, mwgg_hints):
        hints_key = f"_read_hints_{self.ctx.team}_{self.ctx.slot}"
        mwgg_hints_key = f"_read_hints_{self.ctx.team}_{self.ctx.slot}_mwgg"
        
        # Ensure mwgg_hints is a dict, not None
        if mwgg_hints is None:
            mwgg_hints = {}
        
        if hints_key not in self.ctx.stored_data:
            return
        if not self.ctx.location_names or not self.ctx.item_names:
            return

        for hint in hints:
            # Only look up MWGG status if we have stored data for this hint
            key = f"{hint['finding_player']}_{hint['location']}"
            mwgg_status = MWGGUIHintStatus.HINT_UNSPECIFIED  # Default
            if key in mwgg_hints:
                mwgg_status = MWGGUIHintStatus(mwgg_hints[key])
            
            if self.ctx.slot_concerns_self(hint["receiving_player"]):
                if not self.ui_hint_data[hint["finding_player"]]:
                    self.ui_hint_data[hint["finding_player"]] = {}
                if hint["location"] not in self.ui_hint_data[hint["finding_player"]]:
                    self.ui_hint_data[hint["finding_player"]][hint["location"]] = \
                        UIHint(hint, self.ctx.location_names, self.ctx.item_names, hint.get("status"), mwgg_status)
                else:
                    self.ui_hint_data[hint["finding_player"]][hint["location"]].set_status(hint.get("status"), mwgg_status)
            elif self.ctx.slot_concerns_self(hint["finding_player"]):
                if not self.ui_hint_data[hint["receiving_player"]]:
                    self.ui_hint_data[hint["receiving_player"]] = {}
                if hint["location"] not in self.ui_hint_data[hint["receiving_player"]]:
                    self.ui_hint_data[hint["receiving_player"]][hint["location"]] = \
                        UIHint(hint, self.ctx.location_names, self.ctx.item_names, hint.get("status"), mwgg_status)
                else:
                    self.ui_hint_data[hint["receiving_player"]][hint["location"]].set_status(hint.get("status"), mwgg_status)

        # Update ui_player_data hints to match ui_hint_data
        for slot in self.ui_player_data:
            if slot in self.ui_hint_data:
                self.ui_player_data[slot].hints = self.ui_hint_data[slot]

        # Update hints lists if it exists
        if hasattr(self, 'console_screen') and self.console_screen:
            self.console_screen.update_slots_list()
        if hasattr(self, 'hint_screen') and self.hint_screen:
            self.hint_screen.update_hints_list()

    def update_mwgg_hints(self, mwgg_hints: typing.Optional[dict] = None):
        if mwgg_hints is None:
            mwgg_hints = self.ui_hint_data
        
        # Get current stored data to compare
        current_stored = self.ctx.stored_data.get(f"_read_hints_{self.ctx.team}_{self.ctx.slot}_mwgg", {})
        
        # Only store hints that have non-default MWGG status
        mwgg_data_to_store = {}
        has_changes = False
        
        for finding_player, locations in mwgg_hints.items():
            for location_id, hint_data in locations.items():
                key = f"{finding_player}_{location_id}"
                current_status = hint_data.mwgg_hint_status
                
                # Only store if it's not the default unspecified status
                if current_status != MWGGUIHintStatus.HINT_UNSPECIFIED:
                    mwgg_data_to_store[key] = current_status.value
                    # Check if this is a change
                    if key not in current_stored or current_stored[key] != current_status.value:
                        has_changes = True
                elif key in current_stored:
                    # Remove from storage if it was previously stored but is now default
                    has_changes = True
        
        # Only send update if there are actual changes
        if has_changes:
            asynckivy.start(self.ctx.send_msgs([{
                "cmd": "Set",
                "key": f"_read_hints_{self.ctx.team}_{self.ctx.slot}_mwgg",
                "want_reply": False,
                "default": {},
                "operations": [{"operation": "replace", "value": mwgg_data_to_store}]
            }]))

    @property
    def show_all_hints(self):
        return self._show_all_hints

    @show_all_hints.setter
    def show_all_hints(self, value: bool):
        self._show_all_hints = value
        if hasattr(self, 'hint_screen') and self.hint_screen:
            self.hint_screen.update_hints_list()

def is_command_input(string: str) -> bool:
    return len(string) > 0 and string[0] in "/!"
