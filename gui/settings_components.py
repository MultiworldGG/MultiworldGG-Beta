from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ColorProperty, BooleanProperty, NumericProperty
from kivy.metrics import dp, Metrics
from kivy.utils import get_color_from_hex, get_hex_from_color
from kivy.clock import Clock

from dataclasses import fields
import logging
import os
import sys

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField, MDTextFieldHelperText
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer 

from .mw_theme import THEME_OPTIONS, DEFAULT_TEXT_COLORS, RegisterFonts
from .kivydi.colorpicker import MWColorPicker

logger = logging.getLogger("Client")

# KV string for settings components
settings_components_kv = '''
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
    PaletteButtonLayout:
        id: palette_buttons
        orientation: "horizontal"
        size_hint_x: 0.7
        pos_hint: {"right": 1, "center_y": 0.5}
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

<ColorBox>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(48)
    MDLabel:
        id: text_color_label
        theme_text_color: "Custom"
        text_color: root.color
        text: root.text
        size_hint_x: 0.7
    MDButton:
        id: reset_color_button
        style: "filled"
        size: dp(32), dp(32)
        theme_bg_color: "Custom"
        md_bg_color: root.default_color
        on_release: root.reset_color()
        MDButtonText:
            text: "Reset"
    ColorPreviewBox:
        id: color_preview_box
        index: root.index
        color_attr: root.color_attr
        color: root.color
        attr_name: root.attr_name

<ColorPreviewBox>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(48)
    MDButton:
        style: "filled"
        size: dp(32), dp(32)
        theme_bg_color: "Custom"
        md_bg_color: root.color
        on_release: root.open_color_picker(root.color, root.index, root.color_attr, self.pos)

<SettingsScrollBox>:
    MDBoxLayout:
        id: layout
        orientation: "vertical"
        padding: [dp(16), dp(8)]
        spacing: dp(8)
        size_hint_y: None
        height: self.minimum_height
        pos_hint: {"top": 1}
'''

Builder.load_string(settings_components_kv)

class SettingsSection(MDBoxLayout):
    """Base class for settings sections"""
    name = StringProperty("")
    title = StringProperty("")

class LabeledSwitch(MDBoxLayout):
    """Switch with a label"""
    text = StringProperty("")
    on_switch = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.switch.bind(on_active = lambda x: self.on_switch(self, self.active))

    def on_switch(self, instance, value):
        pass

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
        logger.debug("Initializing SettingsScrollBox")
        self.layout = self.ids.layout
        logger.debug(f"Retrieved layout: {self.layout}")

class ConnectionSettings(SettingsScrollBox):
    """Connection settings section"""
    def __init__(self, **kwargs):
        logger.debug("Initializing ConnectionSettings")
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        logger.debug("Got running app")
        
        # Profile section
        logger.debug("Creating profile section")
        profile_section = SettingsSection(name="profile_settings", title="Profile")
        
        # Alias
        logger.debug("Adding alias field")
        alias_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(55), padding=dp(4), spacing=dp(4))
        alias_box.add_widget(MDLabel(text="Alias", theme_text_color="Primary", size_hint_x=0.7))
        alias_input = MDTextField(
            text=self.app.app_config.get('client', 'alias', fallback=''),
        )
        alias_box.add_widget(alias_input)
        profile_section.add_widget(alias_box)
        
        # Pronouns
        logger.debug("Adding pronouns field")
        pronouns_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(55), padding=dp(4), spacing=dp(4))
        pronouns_box.add_widget(MDLabel(text="Pronouns", theme_text_color="Primary", size_hint_x=0.7))
        pronouns_input = MDTextField(
            MDTextFieldHelperText(
                text="he/him she/her they/them any/any - freeform",
                mode="persistent",
                theme_text_color="Secondary",
            ),
            text=self.app.app_config.get('client', 'pronouns', fallback=''),
        )
        pronouns_box.add_widget(pronouns_input)
        profile_section.add_widget(pronouns_box)
        
        # Status toggles
        logger.debug("Creating status section")
        status_section = SettingsSection(name="status_settings", title="Status")
        status_section.add_widget(LabeledSwitch(
            text="In Call",
            on_switch=self.toggle_in_call
        ))
        status_section.add_widget(LabeledSwitch(
            text="In BK",
            on_switch=self.toggle_in_bk
        ))
        
        # Host settings
        logger.debug("Creating host settings section")
        host_section = SettingsSection(name="multiworld_settings", title="Multiworld Settings")
        
        # Hostname & Port
        logger.debug("Adding hostname field")
        hostname_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(55), padding=dp(4), spacing=dp(4))
        hostname_box.add_widget(MDLabel(text="Hostname", theme_text_color="Primary"))
        hostname_input = MDTextField(
            text=self.app.app_config.get('client', 'hostname', fallback='multiworld.gg'),
        )
        hostname_box.add_widget(hostname_input)
        hostname_box.add_widget(MDLabel(text="Port", theme_text_color="Primary"))
        port_input = MDTextField(
            text=self.app.app_config.get('client', 'port', fallback='38281'),
        )
        hostname_box.add_widget(port_input)
        host_section.add_widget(hostname_box)
 
        # Player Slot
        logger.debug("Adding player slot field")
        slot_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(55), padding=dp(4), spacing=dp(4))
        slot_box.add_widget(MDLabel(text="Player Slot", theme_text_color="Primary"))
        slot_input = MDTextField(
            text=self.app.app_config.get('client', 'slot', fallback=''),
        )
        slot_box.add_widget(slot_input)
        slot_box.add_widget(MDLabel(text="Password", theme_text_color="Primary"))
        slot_input = MDTextField(
            text='',
            password=True,
        )
        slot_box.add_widget(slot_input)
        host_section.add_widget(slot_box)
        
        # Admin Password
        logger.debug("Adding admin password field")
        admin_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50))
        admin_box.add_widget(MDLabel(text="Admin Password", theme_text_color="Primary", size_hint_x=0.7))
        admin_input = MDTextField(
            MDTextFieldHelperText(
                text="Login for the multiworld server to run admin commands",
                mode="persistent",
                theme_text_color="Secondary",
            ),
            text="********" if self.app.app_config.get('client', 'admin_password', fallback='') else '',
            password=True
        )
        admin_box.add_widget(admin_input)
        host_section.add_widget(admin_box)
        
        # Add all sections to the layout
        logger.debug("Adding all sections to layout")
        self.layout.add_widget(profile_section)
        self.layout.add_widget(status_section)
        self.layout.add_widget(host_section)
        logger.debug("Finished initializing ConnectionSettings")
    
    def toggle_in_call(self, instance, value):
        try:
            logger.debug(f"Toggling in_call to {value}")
            self.app.app_config.set('client', 'in_call', str(value))
            self.app.app_config.write()
            logger.debug("In call toggle complete")
        except Exception as e:
            logger.error(f"Error in toggle_in_call: {e}", exc_info=True)
    
    def toggle_in_bk(self, instance, value):
        try:
            logger.debug(f"Toggling in_bk to {value}")
            self.app.app_config.set('client', 'in_bk', str(value))
            self.app.app_config.write()
            logger.debug("In BK toggle complete")
        except Exception as e:
            logger.error(f"Error in toggle_in_bk: {e}", exc_info=True)

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

class InterfaceSettings(SettingsScrollBox):
    """Interface settings section"""
    def __init__(self, **kwargs):
        logger.debug("Initializing InterfaceSettings")
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        logger.debug("Got running app")
        
        # Display section
        logger.debug("Creating display section")
        display_section = SettingsSection(name="display_settings", title="Display")
        display_section.add_widget(LabeledSwitch(
            text="Fullscreen",
            theme_text_color="Secondary",
            on_switch=self.toggle_fullscreen
        ))
        logger.debug("Added fullscreen switch")
        
        # Layout section
        logger.debug("Creating layout section")
        layout_section = SettingsSection(name="layout_settings", title="Layout")
        layout_section.add_widget(LabeledSwitch(
            text="Compact Mode",
            theme_text_color="Secondary",
            on_switch=self.toggle_device_orientation
        ))
        logger.debug("Added device orientation (compact mode) switch")
        
        # Add all sections to the layout
        logger.debug("Adding sections to layout")
        self.layout.add_widget(display_section)
        self.layout.add_widget(layout_section)
        logger.debug("Finished initializing InterfaceSettings")
    
    def toggle_fullscreen(self, instance, value):
        try:
            logger.debug(f"Toggling fullscreen to {value}")
            self.app.config.set('graphics', 'fullscreen', str(value))
            self.app.config.write()
            logger.debug("Fullscreen toggle complete")
        except Exception as e:
            logger.error(f"Error in toggle_fullscreen: {e}", exc_info=True)
    
    def toggle_device_orientation(self, instance, value):
        try:
            logger.debug(f"Toggling device orientation to {value}")
            self.app.app_config.set('client', 'device_orientation', str(value))
            self.app.app_config.write()
            logger.debug("Device orientation toggle complete")
        except Exception as e:
            logger.error(f"Error in toggle_device_orientation: {e}", exc_info=True) 