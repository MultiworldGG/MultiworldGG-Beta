__all__ = ("MWColorPicker",)
from kivy.properties import ColorProperty, StringProperty, ObjectProperty
from PIL import ImageGrab
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextFieldHintText
from kivymd.uix.fitimage import FitImage
from kivy.lang import Builder
from kivymd.theming import ThemableBehavior
from kivy.utils import get_hex_from_color, get_color_from_hex
from kivy.core.window import Window
import os
import re
import logging

logger = logging.getLogger("MultiWorld")

KV = """
<ColorInfoLayout>:
    apply_color_button: apply_color_button
    revert_color_button: revert_color_button
    color_text: color_text
    cols: 2
    row_force_default: True
    row_default_height: 80
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    spacing: 5
    padding: 
    MDLabel:
        width: 60
        size_hint_x: None
        text: "Color:"
        pos_hint: {"right": .9, "center_y": 0.5}
    BoxLayout:
        canvas.before:
            Color:
                rgba: root.theme_cls.surfaceContainerLowestColor
            RoundedRectangle:
                size: 160, 55
                pos: self.pos
                radius: [5, 5, 5, 5]
        MDTextField:
            id: color_text
            size_hint_x: None
            width: 160
            padding: 5
            pos_hint: {"x": 0, "y": 0}
            theme_font_name: "Custom"
            font_name: app.theme_cls.font_styles.Monospace['large']['font-name'] 
            theme_font_size: "Custom"
            font_size: app.theme_cls.font_styles.Monospace['large']['font-size']
            theme_line_spacing: "Custom"
            line_spacing: app.theme_cls.font_styles.Monospace['large']['line-height']
            theme_text_color: "Custom"
            text_color_focus: root.color
            text_color_normal: root.color
            on_text_validate: root.on_text_field_change(self.text)
            keyboard_suggestions: False
            MDTextFieldLeadingIcon:
                theme_icon_color: "Custom"
                icon_color_normal: self.theme_cls.onSurfaceColor
                icon_color_focus: self.theme_cls.onSurfaceColor
                icon: "palette"
            ColorHintText:
                text_color_normal: root.old_color
                text_color_focus: root.old_color
                text: root.old_hex_color
                bold: True

    Widget:
        width: 60
        size_hint_x: None
        canvas.before:
            Color:
                rgba: root.color
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [10, 10, 10, 10]
        size_hint: None, None
        size: 50, 50
    MDBoxLayout:
        orientation: "horizontal"
        spacing: 5
        padding: 5
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        MDButton:
            id: apply_color_button
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            MDButtonText:
                theme_text_color: "Primary"
                text: "Apply"
        MDButton:
            id: revert_color_button
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            MDButtonText:
                theme_text_color: "Primary"
                text: "Revert"

"""

# Load KV string once at module level
Builder.load_string(KV)

class ColorHintText(MDTextFieldHintText, ThemableBehavior):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_text_color = "Custom"
        self.text_color_focus = self.text_color_normal = self.text_color
        self.outline_color = self.theme_cls.onSurfaceColor
        self.outline_width = 1


class ColorInfoLayout(MDGridLayout, ThemableBehavior):
    color = ColorProperty([0, 0, 0, 0])
    old_color = ColorProperty([0, 0, 0, 0])
    hex_color = StringProperty("#000000")
    old_hex_color = StringProperty("#000000")
    apply_color_button = ObjectProperty(None)
    revert_color_button = ObjectProperty(None)
    color_text = ObjectProperty(None)
    _updating = False  # Flag to prevent update loops

    def __init__(self, old_hex_color, **kwargs):
        super().__init__(**kwargs)
        self.old_hex_color = old_hex_color
        self.old_color = get_color_from_hex(old_hex_color)
        self.bind(color=self._on_color_change)
        self.bind(hex_color=self._on_hex_color_change)

    def on_parent(self, *args):
        if self.parent:
            self.color = self.parent.color
            self.hex_color = self.parent.hex_color
            self.revert_color_button.bind(on_press=lambda x: self.revert_color())

    def _on_color_change(self, instance, value):
        if self._updating:
            return
        try:
            self._updating = True
            # Convert color to hex and strip alpha
            hex_color = get_hex_from_color(value).lstrip('#')[:6]
            if self.color_text:
                self.color_text.text = f"#{hex_color}"
                self.color_text.text_color_focus = value
                self.color_text.text_color_normal = value
            # Update hex_color through the parent MWColorPicker
            if hasattr(self.parent, 'hex_color'):
                self.parent.hex_color = hex_color
                self.hex_color = hex_color
            if hasattr(self.parent, 'color'):
                self.parent.color = value
                self.color = value
        except Exception as e:
            logger.error(f"Error in _on_color_change: {e}", exc_info=True)
        finally:
            self._updating = False

    def _on_hex_color_change(self, instance, value):
        if self._updating:
            return
        logger.debug(f"Hex color changed to: {value}")
        try:
            self._updating = True
            if self.color_text:
                if not value.startswith('#'):
                    value = f"#{value}"
                self.color_text.text = value
                self.color_text.text_color_focus = value
                self.color_text.text_color_normal = value
        except Exception as e:
            logger.error(f"Error in _on_hex_color_change: {e}", exc_info=True)
        finally:
            self._updating = False

    def on_text_field_change(self, text):
        if self._updating:
            return
        logger.debug(f"ColorInfoLayout on_text_field_change called with text: {text}")
        try:
            self._updating = True
            # Validate hex color format
            hex_pattern = r'^(?:#)?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$'
            if re.match(hex_pattern, text):
                # Remove # if present and ensure 6 characters
                clean_text = text.lstrip('#')
                if len(clean_text) == 3:
                    # Convert 3-digit hex to 6-digit
                    clean_text = ''.join(c + c for c in clean_text)
                
                logger.debug(f"Valid hex color detected: {clean_text}")
                # Update hex_color through the parent MWColorPicker
                if hasattr(self.parent, 'hex_color'):
                    logger.debug(f"Updating parent hex_color to: {clean_text}")
                    self.parent.hex_color = clean_text
                    # Also update our own hex_color to keep KV in sync
                    self.hex_color = clean_text
        except Exception as e:
            logger.error(f"Error in on_text_field_change: {e}", exc_info=True)
        finally:
            self._updating = False

    def revert_color(self, *args):
        self.color = self.old_color

class MWColorPicker(MDBoxLayout):
    orientation = "horizontal"
    color = ColorProperty([0, 0, 0, 0])
    hex_color = StringProperty("#000000")
    _updating = False  # Flag to prevent update loops

    def __init__(self, old_hex_color, **kwargs):
        logger.debug("Initializing MWColorPicker")
        super().__init__(**kwargs)
        self.old_hex_color = old_hex_color
        self.size_hint = (1, None)
        self.height = 250  # Set a fixed height for the color picker
        
        # Create and configure the image
        self.image = FitImage(source=os.path.join(os.getenv("KIVY_DATA_DIR"), "images", "palette.png"), fit_mode='scale-down')  
        # Create and configure the info layout
        self.info_layout = ColorInfoLayout(old_hex_color=self.old_hex_color)
        
        self.add_widget(self.info_layout)
        self.add_widget(self.image)
        self.bind(color=self._on_color_change)
        self.bind(hex_color=self._on_hex_color_change)

    def _on_color_change(self, instance, value):
        if self._updating:
            return
        logger.debug(f"Color changed to: {value}")
        try:
            self._updating = True
            self.info_layout.color = value
        except Exception as e:
            logger.error(f"Error in _on_color_change: {e}", exc_info=True)
        finally:
            self._updating = False

    def _on_hex_color_change(self, instance, value):
        if self._updating:
            return
        logger.debug(f"Hex color changed to: {value}")
        try:
            self._updating = True
            # Update the color based on the new hex value
            if not value.startswith('#'):
                value = '#' + value
            color = get_color_from_hex(value)
            self.color = (color[0], color[1], color[2], 1)  # Force alpha to 1
            # Update the info layout's hex_color to keep KV in sync
            self.info_layout.hex_color = value.lstrip('#')
        except Exception as e:
            logger.error(f"Error in _on_hex_color_change: {e}", exc_info=True)
        finally:
            self._updating = False

    def on_touch_down(self, touch):
        try:
            # Check if touch is within the image's bounds
            if self.image.collide_point(touch.x, touch.y):

                # Convert touch position to window coordinates
                window_pos = self.to_window(touch.x, touch.y)
                
                # Add window location offsets
                screen_x = Window.left + window_pos[0] # Window.left is 410
                # Get the "inverse" position of the window because kivy is weird
                screen_y = Window.height - window_pos[1] + Window.top 
                
                # Get the color at the screen coordinates
                pixel = ImageGrab.grab(bbox=(screen_x, screen_y-1, screen_x+1, screen_y)).load()[0,0]
            
                # Convert to normalized color
                color = (pixel[0]/255, pixel[1]/255, pixel[2]/255, 1)
                
                # Update the color
                self.color = color
                return True
            elif self.info_layout.color_text.collide_point(touch.x, touch.y):
                super().on_touch_down(touch)
                return True
            elif self.info_layout.apply_color_button.collide_point(touch.x, touch.y):
                super().on_touch_down(touch)
                return True
            elif self.info_layout.revert_color_button.collide_point(touch.x, touch.y):
                super().on_touch_down(touch)
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Error in on_touch_down: {e}", exc_info=True)
            return False
