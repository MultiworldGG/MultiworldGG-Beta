from __future__ import annotations
"""
Settings Components to be used for the following screens:

settings
settings_compact

ConnectionSettings - Connection settings section
ThemingSettings - Theming settings section
InterfaceSettings - Interface settings section
"""

__all__ = ("ConnectionSettings", "ThemingSettings", "InterfaceSettings")

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ColorProperty, BooleanProperty, NumericProperty
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.config import Config as MWKVConfig

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField, MDTextFieldHelperText
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText 

from mwgg_gui.components.mw_theme import THEME_OPTIONS, DEFAULT_TEXT_COLORS, RegisterFonts
from mwgg_gui.overrides.colorpicker import MWColorPicker
from mwgg_gui.components.dialog import MessageBox

from dataclasses import fields
import logging
from Utils import persistent_store, persistent_load
logger = logging.getLogger("Client")

# KV string for settings components
KV = '''
<SettingsSection>:
    orientation: "vertical"
    padding: [dp(16), dp(8)]
    spacing: dp(8)
    size_hint_y: None
    height: self.minimum_height

<LabeledSwitch>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(48)
    MDLabel:
        theme_text_color: "Secondary"
        text: root.text
        size_hint_x: 0.7
    MDSwitch:
        id: switch

<LightDarkSwitch>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(48)
    MDLabel:
        theme_text_color: "Secondary"
        text: root.text
    MDSwitch:
        id: light_dark_mode_switch
        active: root.theme_cls.theme_style == "Light"
        icon_active: "weather-sunny"
        icon_active_color: "white"
        icon_inactive: "weather-night"
        icon_inactive_color: "grey"
        thumb_color_active: [.7, .7, .7, 1]
        thumb_color_inactive: [.1, .1, .1, 1]
        track_color_active: [.9, .9, .9, 1]
        track_color_inactive: [.3, .3, .3, 1]
        on_active: root.on_switch(self, self.active)

<PaletteSection>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(55)
    padding: dp(4)
    spacing: dp(4)
    MDLabel:
        text: root.text
        theme_text_color: "Primary"
        size_hint_x: 1
    PaletteButtonLayout:
        id: palette_buttons
        orientation: "horizontal"
        pos_hint: {"right": 1, "center_y": 0.5}
        width: dp(395)
        spacing: dp(4)

<PaletteButton>:
    style: "filled"
    size: dp(75), dp(40)
    theme_bg_color: "Custom"
    md_bg_color: root.md_bg_color
    MDButtonIcon:
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        icon: "palette"
        theme_icon_color: "Custom"
        icon_color: [.8, .8, .8, 1] if sum(root.md_bg_color[:3]) < 1.5 else [.2, .2, .2, 1]

<LabeledDropdown>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(48)
    MDLabel:
        theme_text_color: "Secondary"
        text: root.text
        size_hint_x: 0.7
    MDButton:
        id: dropdown_button
        on_release: root.show_menu()
        MDButtonText:
            text: root.current_item

<LabeledSlider>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(48)
    slider: slider.value
    MDLabel:
        theme_text_color: "Secondary"
        text: root.text
        size_hint_x: 0.7
    MDSlider:
        id: slider
        min: root.min
        max: root.max
        step: root.step
        on_value: root.on_slide(self,self.value)
        MDSliderHandle:
        MDSliderValueLabel:

<ColorBox>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(48)
    padding: dp(4)
    spacing: dp(4)
    MDLabel:
        id: text_color_label
        theme_text_color: "Custom"
        text_color: root.color
        font_style: "Monospace"
        role: "medium"
        text: root.text
        size_hint_x: 0.8
    ColorPreviewBox:
        id: color_preview_box
        index: root.index
        color_attr: root.color_attr
        color: root.color
        attr_name: root.attr_name
        size_hint_x: None
        pos_hint: {"top": 1}
    MDButton:
        style: "filled"
        size: dp(50), dp(32)
        theme_bg_color: "Custom"
        md_bg_color: root.default_color
        on_release: root.reset_color()
        size_hint_x: None
        pos_hint: {"top": 1}
        MDButtonText:
            theme_text_color: "Custom"
            text_color: app.theme_cls.surfaceContainerLowColor
            text: "Reset"

<ColorPreviewBox>:
    orientation: "horizontal"
    height: dp(48)
    MDButton:
        style: "filled"
        size: dp(50), dp(32)
        pos_hint: {"top": 1}
        theme_bg_color: "Custom"
        md_bg_color: root.color
        on_release: root.open_color_picker(root.color, root.index, root.color_attr, self.pos)

<SettingsScrollBox>:
    pos_hint: {"center_x": 0.5}
    MDBoxLayout:
        id: layout
        orientation: "vertical"
        padding: [dp(16), dp(8)]
        spacing: dp(8)
        size_hint_y: None
        size_hint_x: .8
        height: self.minimum_height
        pos_hint: {"top": 1}
'''

Builder.load_string(KV)

class SettingsSection(MDBoxLayout):
    """Base class for settings sections"""
    name = StringProperty("")
    title = StringProperty("")

class LabeledSwitch(MDBoxLayout):
    """Switch with a label"""
    text = StringProperty("")
    active = BooleanProperty(False)
    on_switch = ObjectProperty(None)

    def __init__(self, active: bool = False, on_switch=None, *args, **kwargs):
        self.active = active
        super().__init__(*args, **kwargs)
        if on_switch:
            self.on_switch = on_switch
        self.ids.switch.active = self.active
        self.ids.switch.bind(active=self._on_switch_change)

    def _on_switch_change(self, instance, value):
        if self.on_switch:
            self.on_switch(self, value)

class LightDarkSwitch(MDBoxLayout):
    """Switch for light/dark mode"""
    text = StringProperty("")
    on_switch = ObjectProperty(None)

    def __init__(self, on_switch, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_switch = on_switch

class LabeledDropdown(MDBoxLayout):
    """Dropdown with a label"""
    text = StringProperty("")
    items = ObjectProperty([])
    current_item = StringProperty("")
    on_select = ObjectProperty(None)

    def __init__(self, on_select=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if on_select:
            self.on_select = on_select

    def show_menu(self):
        menu_items = [
            {
                "text": item, 
                "theme_text_color": "Secondary",
                "on_release": lambda x=item: self.select_item(x),
            } for item in self.items
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.dropdown_button,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def select_item(self, item):
        self.current_item = item
        if self.on_select:
            self.on_select(item)
        self.menu.dismiss()

class LabeledSlider(MDBoxLayout):
    """Slider with a label"""
    text = StringProperty("")
    step = NumericProperty(1)
    min = NumericProperty(0)
    max = NumericProperty(20)
    slider = ObjectProperty(None)
    on_slide = ObjectProperty(None)

    def __init__(self, value, on_slide, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_slide = on_slide
        self.slider = value

class PaletteSection(MDBoxLayout):
    """Section containing palette color buttons with a label"""
    text = StringProperty("")

class PaletteButton(MDButton):
    """Individual palette color button"""
    hex_color = StringProperty("")
    palette_name = StringProperty("")
    md_bg_color = ColorProperty([0,0,0,0])
    on_release = ObjectProperty(None)
    set_palette = ObjectProperty(None)
    is_current = BooleanProperty(False)

    def __init__(self, hex_color, palette_name, md_bg_color, is_current, set_palette, **kwargs):
        super().__init__(**kwargs)
        self.hex_color = hex_color
        self.palette_name = palette_name
        self.md_bg_color = md_bg_color
        self.is_current = is_current
        self.set_palette = set_palette
        self._update_style()
        
    def _update_style(self):
        if self.is_current:
            self.theme_line_color = "Custom"
            self.line_color = self.theme_cls.inversePrimaryColor
        else:
            self.theme_line_color = "Primary"
        
    def on_release(self):
        if self.set_palette:
            self.set_palette(self, self.palette_name)
            self.parent.set_current_button(self)

class PaletteButtonLayout(MDBoxLayout):
    """Layout containing palette color buttons"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buttons = []

    def add_palette_button(self, hex_color, palette_name, md_bg_color, is_current, set_palette):
        button = PaletteButton(
            hex_color=hex_color,
            palette_name=palette_name,
            md_bg_color=md_bg_color,
            is_current=is_current,
            set_palette=set_palette
        )
        self.buttons.append(button)
        self.add_widget(button)

    def set_current_button(self, current_button):
        for button in self.buttons:
            button.is_current = (button == current_button)
            button._update_style()

class ColorPreviewBox(MDBoxLayout):
    """Box showing a color preview"""
    color = ColorProperty([0,0,0,0]) #actual color
    color_attr = ObjectProperty(None) #link to color in theme
    attr_name = StringProperty("") #name of the variable in the theme
    color_attr_old = ObjectProperty(None) #previous choice of color
    index = NumericProperty(0) #index (light/dark)
    text = StringProperty("") #text of the label
    on_color_change = ObjectProperty(None)

    def open_color_picker(self, color, index, color_attr, pos):
        # Create a new color picker each time to avoid binding issues
        self.color_attr = color_attr
        self.color_attr_old = [i for i in color_attr]
        self.index = index
        self.text = self.parent.text
        self.color_picker = MWColorPicker(self.color_attr_old[self.index])
        
        def on_color(instance, value):
            try:
                hex_color = instance.hex_color#.lstrip('#')[:-2]
                # Update the appropriate color in the list based on theme style
                self.color_attr[self.index] = hex_color
                #Clock.schedule_once(lambda dt: self.app.theme_cls.refresh(), 0.5)
                self.color = instance.color
                # Trigger the color change event
                if self.on_color_change:
                    self.on_color_change(self.attr_name, self.color_attr)
            except Exception as e:
                logger.error(f"Error updating color: {e}", exc_info=True)
        
        # Bind to the color property
        self.color_picker.bind(color=on_color)

        # Create popup with color picker
        dialog = MDDialog(
            MDDialogHeadlineText(
                text="Choose Color"
            ),
            MDDialogSupportingText(
                text=self.text
            ),
            MDDialogContentContainer(
                self.color_picker
            ),
        )
        # The dialog is a child of a button, 
        # so I need to set the alpha here to 0 to avoid button behavior
        dialog.state_press = 0
        
        def apply(self, *args):
            dialog.dismiss()
        
        self.color_picker.info_layout.apply_color_button.bind(on_release=apply)
        self.color_picker.info_layout.revert_color_button.bind(on_release=lambda x: Clock.schedule_once(apply, 0.5))

        # Get current color and set it
        try:
            current_color = self.color
            self.color_picker.color = current_color
        except Exception as e:
            logger.error(f"Error setting initial color: {e}", exc_info=True)
            self.color_picker.color = (1, 1, 1, 1)  # Default to white if there's an error
        
        # Show the popup
        dialog.open()

class ColorBox(MDBoxLayout):
    """Box showing a color preview"""
    text = StringProperty("")
    color = ColorProperty([0,0,0,0])
    default_color = ColorProperty([0,0,0,0])
    color_attr = ObjectProperty(None)
    attr_name = StringProperty("")
    index = NumericProperty(0)
    on_reset = ObjectProperty(None)
    _initialized = BooleanProperty(False)

    def __init__(self, text, color, color_attr, attr_name, index, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.color_attr = color_attr
        self.attr_name = attr_name
        self.index = index
        self.color = color
        self.default_color = DEFAULT_TEXT_COLORS[self.attr_name][self.index]
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self._initialized = True

    def reset_color(self, *args):
        if not self._initialized:
            return
        default_value = DEFAULT_TEXT_COLORS[self.attr_name]
        # Only reset the specific index (light/dark) that's being modified
        self.color_attr[self.index] = default_value[self.index]
        self.color = get_color_from_hex(self.color_attr[self.index])
        if self.on_reset:
            self.on_reset(self.attr_name, self.color_attr)

class SettingsScrollBox(MDScrollView):
    """Scrollable box for settings"""
    layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = self.ids.layout

class ConnectionSettings(SettingsScrollBox):
    """Connection settings section
    This is the settings section for the connection settings.
    It includes the profile settings, status settings, and host settings.
    
    TODO: pull from the profile component"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
        # Profile section
        profile_section = SettingsSection(name="profile_settings", title="Profile")

        # Avatar link
        # TODO: needs proper upload functionality here
        avatar_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(55), padding=dp(4), spacing=dp(4))
        avatar_box.add_widget(MDLabel(text="Avatar URL", theme_text_color="Primary", size_hint_x=0.7))
        self.avatar_input = MDTextField(
            text=self.app.app_config.get('client', 'avatar', fallback=''),
            on_text_validate=self.save_avatar
        )
        avatar_box.add_widget(self.avatar_input)
        profile_section.add_widget(avatar_box)
        
        # Alias
        alias_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(55), padding=dp(4), spacing=dp(4))
        alias_box.add_widget(MDLabel(text="Alias", theme_text_color="Primary", size_hint_x=0.7))
        self.alias_input = MDTextField(
            text=self.app.app_config.get('client', 'alias', fallback=''),
            on_text_validate=self.save_alias
        )
        alias_box.add_widget(self.alias_input)
        profile_section.add_widget(alias_box)
        
        # Pronouns
        pronouns_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(55), padding=dp(4), spacing=dp(4))
        pronouns_box.add_widget(MDLabel(text="Pronouns", theme_text_color="Primary", size_hint_x=0.7))
        self.pronouns_input = MDTextField(
            MDTextFieldHelperText(
                text="he/him she/her they/them any/any - freeform",
                mode="persistent",
                theme_text_color="Secondary",
            ),
            text=self.app.app_config.get('client', 'pronouns', fallback=''),
            on_text_validate=self.save_pronouns
        )
        pronouns_box.add_widget(self.pronouns_input)
        profile_section.add_widget(pronouns_box)
        
        # Status toggles
        status_section = SettingsSection(name="status_settings", title="Status")
        self.in_call_switch = LabeledSwitch(
            text="In Call",
            on_switch=self.toggle_in_call
        )
        # Set initial state from config
        self.in_call_switch.ids.switch.active = self.app.app_config.getboolean('client', 'deafened', fallback=False)
        status_section.add_widget(self.in_call_switch)
        
        self.in_bk_switch = LabeledSwitch(
            text="In BK",
            on_switch=self.toggle_in_bk
        )
        # Set initial state from config
        self.in_bk_switch.ids.switch.active = self.app.app_config.getboolean('client', 'in_bk', fallback=False)
        status_section.add_widget(self.in_bk_switch)
        
        # Host settings
        host_section = SettingsSection(name="multiworld_settings", title="Multiworld Settings")
        
        # Hostname & Port
        hostname_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(55), padding=dp(4), spacing=dp(4))
        hostname_box.add_widget(MDLabel(text="Hostname", theme_text_color="Primary"))
        self.hostname_input = MDTextField(
            text=persistent_load().get('client', {}).get('last_server_hostname', 'multiworld.gg'),
            on_text_validate=self.save_hostname
        )
        hostname_box.add_widget(self.hostname_input)
        hostname_box.add_widget(MDLabel(text="Port", theme_text_color="Primary"))
        self.port_input = MDTextField(
            text=str(persistent_load().get('client', {}).get('last_server_port', 38281)),
            on_text_validate=self.save_port
        )
        hostname_box.add_widget(self.port_input)
        host_section.add_widget(hostname_box)
 
        # Player Slot
        slot_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(55), padding=dp(4), spacing=dp(4))
        slot_box.add_widget(MDLabel(text="Player Slot", theme_text_color="Primary"))
        self.slot_input = MDTextField(
            text=persistent_load().get('client', {}).get('last_username', ''),
            on_text_validate=self.save_slot
        )
        slot_box.add_widget(self.slot_input)
        slot_box.add_widget(MDLabel(text="Password", theme_text_color="Primary"))
        self.password_input = MDTextField(
            text='',
            password=True,
            on_text_validate=self.save_password
        )
        slot_box.add_widget(self.password_input)
        host_section.add_widget(slot_box)
        
        # Admin Password
        admin_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50))
        admin_box.add_widget(MDLabel(text="Admin Password", theme_text_color="Primary", size_hint_x=0.7))
        self.admin_input = MDTextField(
            MDTextFieldHelperText(
                text="Login for the multiworld server to run admin commands",
                mode="persistent",
                theme_text_color="Secondary",
            ),
            text="********" if self.app.app_config.get('client', 'admin_password', fallback='') else '',
            password=True,
            on_text_validate=self.save_admin_password
        )
        admin_box.add_widget(self.admin_input)
        host_section.add_widget(admin_box)
        
        # Add all sections to the layout
        self.layout.add_widget(profile_section)
        self.layout.add_widget(status_section)
        self.layout.add_widget(host_section)

    def show_feedback(self, message: str, is_error: bool = False):
        """Show feedback message to user"""
        try:
            # Create snackbar with message
            snackbar = MDSnackbar(
                MDSnackbarText(
                    text=message,
                ),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.8,
                md_bg_color=self.app.theme_cls.errorColor if is_error else self.app.theme_cls.primaryColor,
            )
            snackbar.open()
        except Exception as e:
            logger.error(f"Error showing feedback: {e}", exc_info=True)
    
    def toggle_in_call(self, instance, value):
        try:
            self.app.app_config.set('client', 'deafened', str(value))
            self.app.app_config.write()
            # Update local player data if it exists
            if hasattr(self.app, 'local_player_data') and self.app.local_player_data:
                self.app.local_player_data.deafened = value
        except Exception as e:
            logger.error(f"Error in toggle_in_call: {e}", exc_info=True)
    
    def toggle_in_bk(self, instance, value):
        try:
            self.app.app_config.set('client', 'in_bk', str(value))
            self.app.app_config.write()
            # Update local player data if it exists
            if hasattr(self.app, 'local_player_data') and self.app.local_player_data:
                self.app.local_player_data.bk_mode = value
        except Exception as e:
            logger.error(f"Error in toggle_in_bk: {e}", exc_info=True)

    def save_avatar(self, instance):
        try:
            self.app.app_config.set('client', 'avatar', instance.text)
            self.app.app_config.write()
            if hasattr(self.app, 'local_player_data') and self.app.local_player_data:
                self.app.local_player_data.avatar = instance.text
            logger.info(f"Avatar saved: {instance.text}")
            self.show_feedback(f"Avatar saved: {instance.text}")
        except Exception as e:
            logger.error(f"Error saving avatar: {e}", exc_info=True)
            self.show_feedback("Error saving avatar", is_error=True)

    def save_alias(self, instance):
        try:
            self.app.app_config.set('client', 'alias', instance.text)
            self.app.app_config.write()
            # Update local player data if it exists
            if hasattr(self.app, 'local_player_data') and self.app.local_player_data:
                self.app.local_player_data.slot_name = instance.text
            logger.info(f"Alias saved: {instance.text}")
            self.show_feedback(f"Alias saved: {instance.text}")
        except Exception as e:
            logger.error(f"Error saving alias: {e}", exc_info=True)
            self.show_feedback("Error saving alias", is_error=True)

    def save_pronouns(self, instance):
        try:
            self.app.app_config.set('client', 'pronouns', instance.text)
            self.app.app_config.write()
            # Update local player data if it exists
            if hasattr(self.app, 'local_player_data') and self.app.local_player_data:
                self.app.local_player_data.pronouns = instance.text
            # Update server tags if connected
            if hasattr(self.app, 'ctx') and self.app.ctx and hasattr(self.app.ctx, 'slot'):
                self.app.set_pronouns()
            logger.info(f"Pronouns saved: {instance.text}")
            self.show_feedback(f"Pronouns saved: {instance.text}")
        except Exception as e:
            logger.error(f"Error saving pronouns: {e}", exc_info=True)
            self.show_feedback("Error saving pronouns", is_error=True)

    def save_hostname(self, instance):
        try:
            persistent_store('client', 'last_server_hostname', instance.text)
            logger.info(f"Hostname saved: {instance.text}")
            self.show_feedback(f"Hostname saved: {instance.text}")
        except Exception as e:
            logger.error(f"Error saving hostname: {e}", exc_info=True)
            self.show_feedback("Error saving hostname", is_error=True)

    def save_port(self, instance):
        try:
            # Validate port number
            port_value = instance.text.strip()
            if port_value:
                port_num = int(port_value)
                if 1 <= port_num <= 65535:
                    persistent_store('client', 'last_server_port', port_num)
                    logger.info(f"Port saved: {port_value}")
                    self.show_feedback(f"Port saved: {port_value}")
                else:
                    error_msg = f"Invalid port: {port_value}. Must be between 1 and 65535."
                    logger.error(error_msg)
                    self.show_feedback(error_msg, is_error=True)
                    instance.text = str(persistent_load().get('client', {}).get('last_server_port', 38281))
            else:
                # Reset to default if empty
                instance.text = '38281'
                persistent_store('client', 'last_server_port', 38281)
                self.show_feedback("Port reset to default: 38281")
        except ValueError:
            error_msg = f"Invalid port: {instance.text}. Must be a number."
            logger.error(error_msg)
            self.show_feedback(error_msg, is_error=True)
            instance.text = str(persistent_load().get('client', {}).get('last_server_port', 38281))
        except Exception as e:
            logger.error(f"Error saving port: {e}", exc_info=True)
            self.show_feedback("Error saving port", is_error=True)

    def save_slot(self, instance):
        try:
            persistent_store('client', 'last_username', instance.text)
            logger.info(f"Slot saved: {instance.text}")
            self.show_feedback(f"Slot saved: {instance.text}")
        except Exception as e:
            logger.error(f"Error saving slot: {e}", exc_info=True)
            self.show_feedback("Error saving slot", is_error=True)

    def save_password(self, instance):
        try:
            self.app.app_config.set('client', 'password', instance.text)
            self.app.app_config.write()
            logger.info("Password saved")
        except Exception as e:
            logger.error(f"Error saving password: {e}", exc_info=True)

    def save_admin_password(self, instance):
        try:
            # Only save if it's not the placeholder text
            if instance.text != "********":
                self.app.app_config.set('client', 'admin_password', instance.text)
                self.app.app_config.write()
                logger.info("Admin password saved")
        except Exception as e:
            logger.error(f"Error saving admin password: {e}", exc_info=True)

class ThemingSettings(SettingsScrollBox):
    """Theming settings section"""
    app_style = {"Light": 0, "Dark": 1}
    light_dark_switch = ObjectProperty(None)
    palette_layout = ObjectProperty(None)
    app: MDApp

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        try:
            self.app = MDApp.get_running_app()
            self.theme_mw = self.app.theme_mw

            # Theme style section
            theme_style_section = SettingsSection(name="theme_style_settings", title="Theme Style")
            current_style = self.app.theme_cls.theme_style
            opposite_style = "Light" if current_style == "Dark" else "Dark" 
            self.light_dark_switch = LightDarkSwitch(
                text=f"Switch to {opposite_style} Mode",
                on_switch=self.change_theme
            )
            theme_style_section.add_widget(self.light_dark_switch)
            
            # Palette section
            palette_section = SettingsSection(name="palette_settings", title="Primary Palette")
            palettes = [color for color in THEME_OPTIONS[current_style]]
            current_palette = self.app.theme_cls.primary_palette
            palette_layout = PaletteSection()
            palette_layout.text = "Primary Color"
            
            self.palette_buttons = palette_layout.ids.palette_buttons
            for name, hc in palettes:
                    self.palette_buttons.add_palette_button(
                        hex_color=hc,
                        palette_name=name,
                        md_bg_color=get_color_from_hex(hc),
                        is_current=(name == current_palette),
                        set_palette=self.update_colors
                    )
            palette_section.add_widget(palette_layout)
                        
            # Custom colors section
            self.custom_colors_section = SettingsSection(name="custom_colors_settings", title="Custom Color Settings")
            color_boxes = self.make_color_boxes()
            for box in color_boxes:
                self.custom_colors_section.add_widget(box)

            # Font size section
            font_section = SettingsSection(name="font_settings", title="Font Settings")
            font_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48), padding=dp(4), spacing=dp(4))
            font_box.add_widget(MDLabel(text="Font Size", theme_text_color="Primary", size_hint_x=0.3))
            
            # Current scale label
            self.font_scale_label = MDLabel(
                text=f"{int(float(self.app.app_config.get('client', 'font_scale', fallback='1.0')) * 10)}0%",
                theme_text_color="Primary",
                size_hint_x=0.2
            )
            font_box.add_widget(self.font_scale_label)
            
            # Decrease button
            decrease_btn = MDIconButton(icon="format-font-size-decrease", theme_icon_color="Primary",
                on_release=lambda x: self.adjust_font_size(-0.1)
            )
            font_box.add_widget(decrease_btn)
            
            # Increase button
            increase_btn = MDIconButton(icon="format-font-size-increase", theme_icon_color="Primary",
                on_release=lambda x: self.adjust_font_size(0.1)
            )
            font_box.add_widget(increase_btn)
            
            # Reset button
            reset_btn = MDIconButton(icon="refresh", theme_icon_color="Primary",
                on_release=lambda x: self.reset_font_size()
            )
            font_box.add_widget(reset_btn)
            
            font_section.add_widget(font_box)
            
            # Monospace font dropdown
            monospace_font_items = ["Argon", "Krypton", "Neon", "Radon", "Xenon"]
            current_monospace_font = self.app.app_config.get('client', 'monospace_font', fallback='Argon')
            font_section.add_widget(LabeledDropdown(
                text="Monospace Font",
                items=monospace_font_items,
                current_item=current_monospace_font,
                on_select=self.on_monospace_font_select
            ))
            
            # Add all sections to the layout
            self.layout.add_widget(theme_style_section)
            self.layout.add_widget(palette_section)
            self.layout.add_widget(font_section)
            self.layout.add_widget(self.custom_colors_section)

        except Exception as e:
            logger.error(f"Error initializing ThemingSettings: {e}", exc_info=True)
    
    def swap_palette_buttons(self):
        palettes = [color for color in THEME_OPTIONS[self.app.theme_cls.theme_style]]
        current_palette = self.app.theme_cls.primary_palette

        for button, color in zip(self.palette_buttons.buttons, palettes):
            button.hex_color = color[1]
            button.palette_name = color[0]
            button.md_bg_color = get_color_from_hex(color[1])
            button.is_current = (color[0] == current_palette)
            if button.is_current:
                button.dispatch('on_release')

    def make_color_boxes(self):
        color_boxes = []
        self.custom_colors_section.clear_widgets()
        for f in fields(self.theme_mw.markup_tags_theme):
            color_attr = getattr(self.theme_mw.markup_tags_theme, f.name)
            color_box = ColorBox(color=get_color_from_hex(color_attr[self.app_style[self.app.theme_cls.theme_style]]), 
                                color_attr=color_attr, 
                                attr_name=f.name,
                                index=self.app_style[self.app.theme_cls.theme_style],
                                text=self.theme_mw.markup_tags_theme.name(color_attr))
            
            # Create a closure that captures the current attr_name
            def make_save_handler(attr_name):
                def save_handler(attr_name, color_attr):
                    print(f"Saving color {attr_name}: {color_attr}")  # Debug print
                    self.theme_mw.save_markup_color(attr_name, color_attr)
                return save_handler
            
            # Bind the handlers with the current attr_name
            color_box.on_reset = make_save_handler(f.name)
            color_box.ids.color_preview_box.on_color_change = make_save_handler(f.name)
            color_boxes.append(color_box)
        return color_boxes

    def change_theme(self, instance, value):
        # Show loading with a delay first
        Clock.schedule_once(lambda dt: self.app.loading_layout.show_loading(speed=0.033), 0)
        # Then make the changes
        Clock.schedule_once(lambda dt: self._do_theme_change(value), 1)

    def _do_theme_change(self, value):
        self.app.theme_mw.theme_style = "Light" if value == True else "Dark"
        self.app.app_config.set('client', 'theme_style', self.app.theme_mw.theme_style)
        self.app.app_config.write()
        self.app.change_theme()
        opposite_style = "Light" if self.app.theme_mw.theme_style == "Dark" else "Dark" 
        self.light_dark_switch.text = f"Switch to {opposite_style} Mode"
        self.swap_palette_buttons()
        color_boxes = self.make_color_boxes()
        for box in color_boxes:
            self.custom_colors_section.add_widget(box)
        self.app.loading_layout.hide_loading()

    def update_colors(self, instance, value):
        # Show loading with a delay first
        Clock.schedule_once(lambda dt: self.app.loading_layout.show_loading(speed=0.033), 0)
        # Then make the changes
        Clock.schedule_once(lambda dt: self._do_color_update(value), 0.5)

    def _do_color_update(self, value):
        self.app.theme_mw.primary_palette = value
        self.app.app_config.set('client', 'primary_palette', value)
        self.app.app_config.write()
        self.app.update_colors()
        self.app.loading_layout.hide_loading()

    def reset_font_size(self):
        """Reset font size to default (1.0)"""
        self.set_font_size(1.0)
        self.app.app_config.set('client', 'font_scale', '1.0')
        self.app.app_config.write()

    def adjust_font_size(self, delta):
        """Adjust font size by the given delta"""
        current_scale = self.theme_mw.font_scale
        new_scale = max(0.8, min(1.2, current_scale + delta))
        self.set_font_size(new_scale)
                
    def set_font_size(self, scale):
        """Set the font scale factor"""
        # Ensure scale is within bounds
        scale = max(0.5, min(2.0, scale))
        
        # Update the label
        self.font_scale_label.text = f"{int(scale * 10)}0%"
        
        # Set the global font scale
        self.theme_mw.font_scale = scale
        
        # Save to config
        self.app.app_config.set('client', 'font_scale', str(scale))
        self.app.app_config.write()
    
    def on_monospace_font_select(self, font_name):
        """Handle monospace font selection"""
        try:
            # Save to config
            self.app.app_config.set('client', 'monospace_font', font_name)
            self.app.app_config.write()
            
            # Re-register fonts with the new monospace font
            RegisterFonts(self.app, font_name)
            
            logger.info(f"Monospace font changed to: {font_name}")
            self.show_feedback(f"Monospace font changed to: {font_name}")
        except Exception as e:
            logger.error(f"Error changing monospace font: {e}", exc_info=True)
            self.show_feedback("Error changing monospace font", is_error=True)
    
    def show_feedback(self, message: str, is_error: bool = False):
        """Show feedback message to user"""
        try:
            # Create snackbar with message
            snackbar = MDSnackbar(
                MDSnackbarText(
                    text=message,
                ),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.8,
                md_bg_color=self.app.theme_cls.errorColor if is_error else self.app.theme_cls.primaryColor,
            )
            snackbar.open()
        except Exception as e:
            logger.error(f"Error showing feedback: {e}", exc_info=True)

class InterfaceSettings(SettingsScrollBox):
    """Interface settings section"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self._scroll_settings = {'scroll_lines': None, 'scroll_velocity': None}
        self._scroll_write_events = {'scroll_lines': None, 'scroll_velocity': None}
        
        # Display section
        display_section = SettingsSection(name="display_settings", title="Display")
        display_section.add_widget(LabeledSwitch(
            text="Fullscreen",
            theme_text_color="Secondary",
            active=bool(MWKVConfig.get('graphics', 'fullscreen', fallback=0)),
            on_switch=self.toggle_fullscreen
        ))
        
        # Layout section
        layout_section = SettingsSection(name="layout_settings", title="Layout")
        layout_section.add_widget(LabeledSwitch(
            text="Compact Mode",
            theme_text_color="Secondary",
            active=self.app.app_config.get('client', 'device_orientation', fallback="Landscape") == "Portrait",
            on_switch=self.toggle_device_orientation
        ))
        layout_section.add_widget(LabeledSwitch(
            text="All Players Chat",
            theme_text_color="Secondary",
            active=bool(self.app.ctx.all_players_chat),
            on_switch=self.toggle_all_players_chat
        ))

        scroll_section = SettingsSection(name="scroll_settings", title="Scroll")
        scroll_section.add_widget(LabeledSlider(
            text="Lines to Scroll",
            value=int(MWKVConfig.get('widgets', 'scroll_lines', fallback="3")),
            on_slide=self.scroll_lines_change
        ))
        scroll_section.add_widget(LabeledSlider(
            text="Scroll Velocity",
            max=20,
            step=1,
            value=int(float(self.app.config.get('client', 'scroll_velocity', fallback="0.5")) * 10),
            on_slide=self.scroll_velocity_change
        ))

        age_filter_section = SettingsSection(name="age_filter_settings", title="Age Filter")
        age_item, age_items = self.get_age_rating()
        age_filter_section.add_widget(LabeledDropdown(
            text="Age Filter",
            items=age_items,
            current_item=age_item,
            on_select=self.on_age_filter_select
        ))
        
        # Add all sections to the layout
        self.layout.add_widget(display_section)
        self.layout.add_widget(layout_section)
        self.layout.add_widget(scroll_section)
        self.layout.add_widget(age_filter_section)
    
    def toggle_fullscreen(self, instance, value):
        def fullscreen_to_string(value: bool) -> str:
            return "1" if value else "0"
        try:
            MWKVConfig.set("graphics", "fullscreen", fullscreen_to_string(value))
            MWKVConfig.write()
        except Exception as e:
            logger.error(f"Error in toggle_fullscreen: {e}", exc_info=True)
    
    def toggle_device_orientation(self, instance, value):
        def orientation_to_string(value: bool) -> str:
            return "Portrait" if value else "Landscape"
        try:
            self.app.app_config.set('client', 'device_orientation', orientation_to_string(value))
            self.app.app_config.write()
        except Exception as e:
            logger.error(f"Error in toggle_device_orientation: {e}", exc_info=True) 

    def toggle_all_players_chat(self, instance, value):
        try:
            self.app.app_config.set('client', 'all_players_chat', str(value))
            self.app.app_config.write()
            self.app.ctx.all_players_chat = value
        except Exception as e:
            logger.error(f"Error in toggle_all_players_chat: {e}", exc_info=True)

    def scroll_lines_change(self, instance, value):
        """Handle scroll lines slider change"""
        self._scroll_setting_change('scroll_lines', value, value_type='int')
    
    def scroll_velocity_change(self, instance, value):
        """Handle scroll velocity slider change (slider value is int, divide by 10 for actual float)"""
        # Store the slider int value; will divide by 10 when writing
        self._scroll_setting_change('scroll_velocity', int(value), value_type='float')
    
    def _scroll_setting_change(self, setting_name, value, value_type='int'):
        """Generic handler for scroll setting changes with debounced config write"""

        self._scroll_settings[setting_name] = int(value)
        
        # Cancel any pending config write for this setting
        if self._scroll_write_events[setting_name] is not None:
            Clock.unschedule(self._scroll_write_events[setting_name])
        
        # Schedule config write after 30 seconds
        self._scroll_write_events[setting_name] = Clock.schedule_once(
            lambda dt, name=setting_name: self._write_scroll_setting(name), 30
        )
    
    def _write_scroll_setting(self, setting_name):
        """Write the stored scroll setting value to config and update console"""
        try:
            if self._scroll_settings[setting_name] is not None:
                value = self._scroll_settings[setting_name]
                
                # For scroll_velocity, divide by 10 to convert from slider int to actual float
                if setting_name == 'scroll_velocity':
                    value = float(value) / 10.0
                
                self.app.app_config.set('client', setting_name, str(value))
                self.app.app_config.write()
                
                # Update console if available
                if hasattr(self.app, 'ui_console') and self.app.ui_console:
                    if setting_name == 'scroll_lines':
                        self.app.ui_console.text_console.lines_to_scroll = int(value)
                    elif setting_name == 'scroll_velocity':
                        self.app.ui_console.text_console.scroll_velocity = float(value)
                
                self._scroll_write_events[setting_name] = None
        except Exception as e:
            logger.error(f"Error writing {setting_name} to config: {e}", exc_info=True)


    def get_age_rating(self):
        items = ["Not Rated", "16 (Teen)", "12 (Everyone)"]
        from importlib.metadata import distribution
        try:
            rating = distribution('mwgg_igdb').name.split('_')[-1]
            if rating == "sixteen":
                return items[1], items
            elif rating == "twelve":
                return items[2], items
            elif rating == "ao":
                return "AO (Adult Only)", items
            return items[0], items
        except Exception as e:
            logger.error(f"Error in get_age_rating: {e}", exc_info=True)
            return items[0], items

    def on_age_filter_select(self, value):
        # Show dialog to confirm age filter selection
        self.age_filter_value = value
        MessageBox(title="Age Filter", message = f'''This will change the age filter for the game list.
This will take a few seconds to complete.
You have selected '{value}' as your age filter.
Are you sure you want to continue?''',
            callback=lambda result: self._dialog_filter_select(result)).open()

    def _dialog_filter_select(self, result):
        if result:
            Clock.schedule_once(lambda dt: self.app.loading_layout.show_loading(speed=0.033), 0)
            # Then make the changes
            Clock.schedule_once(lambda dt: self._do_age_filter_update(self.age_filter_value), 0.5)

    def _do_age_filter_update(self, value):
        self.app.app_config.set('client', 'age_filter', value)
        self.app.app_config.write()
        self.app.set_age_filter(value)
        self.app.loading_layout.hide_loading()