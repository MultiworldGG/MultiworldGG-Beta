__all__ = ('MWColorFilter', 'DefaultTheme', 'RegisterFonts')

import os
import re
import sys
# Add the parent directory to the Python path to find NetUtils
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from NetUtils import DEFAULT_TEXT_COLORS
from dataclasses import dataclass
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivy.metrics import sp, Metrics
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, BoundedNumericProperty
from kivy.config import Config
from kivy.lang import Builder
from kivy.utils import hex_colormap

try:
    from .kivydi import md_icons
except ImportError:
    from kivydi import md_icons

from PIL import Image
import numpy as np

from Utils import local_path

# Overwriting default style.kv
Builder.load_string('''
<Selector>:
    color: app.theme_cls.inversePrimaryColor
''')
# The names of these colors are from Material Design
# and will be the input for primary_palette
# The colors in hex are actual color for the theme
THEME_OPTIONS = {
    "Dark": [("Purple","551353"), #default
             ("Pink","5f112a"),
             ("Brown","5f1414"),
             ("Cyan","003737"),
             ("Green","003a00")],
    "Light": [("Gray","97f0ff"), #default
              ("Chocolate","ffdbc9"),
              ("Goldenrod","ffdea0"),
              ("Pink","ffd9df"),
              ("Olivedrab","cbef86")]
}

@dataclass
class MarkupTagsTheme:
    default_color: list[str]
    location_color: list[str]
    player1_color: list[str]
    player2_color: list[str]
    entrance_color: list[str]
    trap_item_color: list[str]
    regular_item_color: list[str]
    useful_item_color: list[str]
    skip_item_color: list[str]
    progression_skip_item_color: list[str]
    progression_item_color: list[str]
    command_echo_color: list[str]

    def __init__(self, **kwargs):
        # Dark, Light
        self.default_color=["080808","fafafa"]
        self.location_color=["006f10","00c51b"]
        self.player1_color=["b42f88","ff87d7"]
        self.player2_color=["206cb8","5fafff"]
        self.entrance_color=["2985a0","60b7e8"]
        self.trap_item_color=["8f1515","d75f5f"]
        self.regular_item_color=["3b3b3b","b2b2b2"]
        self.useful_item_color=["419F44","6EC471"]
        self.skip_item_color=["419F44","6EC471"]
        self.progression_skip_item_color=["A59C3B","d4cd87"]
        self.progression_item_color=["9f8a00","FFC500"]
        self.command_echo_color=["a75600","ff9334"]

    def name(self, color_attr):
        if color_attr == self.default_color: return "Default Text:"
        if color_attr == self.location_color: return "Location:"
        if color_attr == self.player1_color: return "Slot:"
        if color_attr == self.player2_color: return "Other Players:"
        if color_attr == self.entrance_color: return "Entrance:"
        if color_attr == self.trap_item_color: return "Trap Item:"
        if color_attr == self.regular_item_color: return "Regular Item:"
        if color_attr == self.useful_item_color: return "Useful Item:"
        if color_attr == self.skip_item_color: return "Necessary Duplicate Item:"
        if color_attr == self.progression_skip_item_color: return "Progression Skip Item:"
        if color_attr == self.progression_item_color: return "Progression Item:"
        if color_attr == self.command_echo_color: return "Broadcast:"

    def save_color(self, app_config, color_name, color_value):
        """Save a single color value to the config file"""
        app_config.set('markup_tags', color_name, ','.join(color_value))
        app_config.write()

    def load_color(self, app_config, color_name, default_value):
        """Load a single color value from the config file"""
        value = app_config.get('markup_tags', color_name, fallback=','.join(default_value))
        return value.split(',')

    def save_all_colors(self, app_config):
        """Save all color values to the config file"""
        for color_name in DEFAULT_TEXT_COLORS.keys():
            color_value = getattr(self, color_name)
            self.save_color(app_config, color_name, color_value)

    def load_all_colors(self, app_config):
        """Load all color values from the config file"""
        for color_name, default_value in DEFAULT_TEXT_COLORS.items():
            loaded_value = self.load_color(app_config, color_name, default_value)
            setattr(self, color_name, loaded_value)

class DefaultTheme(ThemableBehavior):
    markup_tags_theme: MarkupTagsTheme
    _theme_style: StringProperty
    _primary_palette: StringProperty
    dynamic_scheme_name: StringProperty
    compact_mode: BooleanProperty
    _font_scale: BoundedNumericProperty
    app_config: None
    def __init__(self, app_config):
        super().__init__()
        self._font_scale = BoundedNumericProperty(1.0, min=0.8, max=1.2)
        self.app_config = app_config
        self.init_global_theme()
        self.markup_tags_theme = MarkupTagsTheme()
        self.markup_tags_theme.load_all_colors(app_config)

    @property
    def theme_style(self):
        return self._theme_style
    @theme_style.setter
    def theme_style(self, value):
        self.primary_palette = THEME_OPTIONS[value][0][0]
        self._theme_style = value

    @property
    def primary_palette(self):
        return self._primary_palette
    @primary_palette.setter
    def primary_palette(self, value):
        self._primary_palette = value

    @property
    def font_scale(self):
        return self._font_scale
    
    @font_scale.setter
    def font_scale(self, value):
        self._font_scale = value
        Metrics.fontscale = value
        RegisterFonts(MDApp.get_running_app())

    def save_markup_color(self, color_name, color_value):
        """Save a single markup color to the config"""
        if not self.app_config.has_section('markup_tags'):
            self.app_config.add_section('markup_tags')
        self.app_config.set('markup_tags', color_name, ','.join(color_value))
        self.app_config.write()

    def load_markup_color(self, color_name):
        """Load a single markup color from the config"""
        default_value = DEFAULT_TEXT_COLORS[color_name]
        return self.markup_tags_theme.load_color(self.app_config, color_name, default_value)

    def recolor_atlas(self):
        """Recolor the atlas image by replacing pixels close to target colors with their respective theme colors.
        """
        try:
            # Get the base directory for assets
            base_dir = os.path.dirname(os.path.abspath(__file__))
            atlas_path = os.path.join(base_dir, "data", "defaulttheme-0.png")
            output_path = os.path.join(os.environ["KIVY_HOME"], "images","defaulttheme-0.png")

            # Open and convert the image
            atlas = Image.open(atlas_path)
            atlas = atlas.convert("RGBA")
            data = np.array(atlas)

            # Define the target colors and their replacements
            color_pairs = [
                (np.array([50, 164, 206]), np.array(self.theme_cls.primaryColor[:3]) * 255, 100),      # cyanish -> primary
                (np.array([141, 178, 200]), np.array(self.theme_cls.secondaryColor[:3]) * 255, 40),    # blueish -> secondary
                (np.array([10, 72, 77]), np.array(self.theme_cls.onPrimaryColor[:3]) * 255, 21),       # tealish -> onPrimary
                (np.array([32, 72, 77]), np.array(self.theme_cls.onSecondaryColor[:3]) * 255, 15),       # alphatealish -> onPrimary
            ]
            
            # Process each color pair sequentially
            for old_color, new_color, tolerance in color_pairs:
                # Calculate color distances for this color
                rgb_data = data[:, :, :3]
                color_diff = np.sqrt(np.sum((rgb_data - old_color) ** 2, axis=2))
                
                # Create a mask for pixels within tolerance
                mask = color_diff < tolerance
                
                # First, replace exact matches
                exact_match = np.all(rgb_data == old_color, axis=2)
                data[exact_match, :3] = new_color
                
                # Then handle all other pixels within tolerance
                for i in range(data.shape[0]):
                    for j in range(data.shape[1]):
                        if mask[i, j] and not exact_match[i, j]:  # Skip exact matches
                            current_pixel = rgb_data[i, j]
                            direction = current_pixel - old_color
                            direction_norm = np.linalg.norm(direction)
                            if direction_norm > 0:  # Avoid division by zero
                                direction = direction / direction_norm
                                # Apply the same direction from the new color
                                replacement_color = new_color + direction * color_diff[i, j]
                                # Ensure values stay within valid range
                                replacement_color = np.clip(replacement_color, 0, 255)
                                data[i, j, :3] = replacement_color
            
            # Convert back to image and save
            new_atlas = Image.fromarray(data)
            new_atlas.save(output_path)
            
        except Exception as e:
            print(f"Error recoloring atlas: {str(e)}")
            # You might want to log this error or handle it differently

    def init_global_theme(self):
        # Get theme settings from app_config
        # Get theme style with Dark as fallback
        theme_style = self.app_config.get('client', 'theme_style', fallback='Dark')
        if theme_style.lower() not in ["light","dark"]:
            theme_style = 'Dark'
        self.theme_style = theme_style
        
        # Get primary palette with first option as fallback
        primary_palette = self.app_config.get('client', 'primary_palette', fallback=THEME_OPTIONS[theme_style][0][0]).capitalize()
        valid_palettes = [
            name_color.capitalize() for name_color in hex_colormap.keys()
        ]
        if primary_palette not in valid_palettes:
            primary_palette = THEME_OPTIONS[theme_style][0][0]
        self.primary_palette = primary_palette
        
        # Get compact mode setting
        compact_mode = self.app_config.getboolean('client', 'compact_mode', fallback=False)
        self.compact_mode = compact_mode
        
        font_scale = self.app_config.get('client', 'font_scale', fallback='1.0')
        self.font_scale = float(font_scale)

        # Save default markup colors if they don't exist
        if not self.app_config.has_section('markup_tags'):
            self.app_config.add_section('markup_tags')
            for color_name, default_value in DEFAULT_TEXT_COLORS.items():
                self.app_config.set('markup_tags', color_name, ','.join(default_value))
            self.app_config.write()
        
        # Dynamic scheme name remains unchanged as per comment
        self.dynamic_scheme_name = "RAINBOW"
        #self.theme_cls.sync_theme_styles()

### Full unicode fonts, finally
def RegisterFonts(app: MDApp):
    LabelBase.register('Inter',
                        os.path.join(local_path(),"data","fonts","Inter-Regular.ttf"),
                        os.path.join(local_path(),"data","fonts","Inter-Italic.ttf"),
                        os.path.join(local_path(),"data","fonts","Inter-Bold.ttf"),
                        os.path.join(local_path(),"data","fonts","Inter-BoldItalic.ttf"))
    LabelBase.register('MonaspaceArgon',
                        os.path.join(local_path(),"data","fonts","MonaspaceArgonFrozen-Regular.ttf"),
                        os.path.join(local_path(),"data","fonts","MonaspaceArgonFrozen-Italic.ttf"),
                        os.path.join(local_path(),"data","fonts","MonaspaceArgonFrozen-ExtraBold.ttf"),
                        os.path.join(local_path(),"data","fonts","MonaspaceArgonFrozen-ExtraBoldItalic.ttf"))
    LabelBase.register('GothicA1',
                        os.path.join(local_path(),"data","fonts","GothicA1-Regular.ttf"),
                        None,
                        os.path.join(local_path(),"data","fonts","GothicA1-Bold.ttf"),
                        None)
    LabelBase.register('Mincho',
                       os.path.join(local_path(),"data","fonts","Mincho-Regular.ttf"),
                       )
    LabelBase.register('LibreFranklin',
                       os.path.join(local_path(),"data","fonts","LibreFranklin-ExtraBold.ttf"),
                       )
    LabelBase.register('Icons',
                       fn_regular=os.path.join(local_path(),"data","fonts","materialdesignicons-fa-webfont.ttf"),
                       )
    app.theme_cls.font_styles = {
        "Icon": {
            "large": {
                "line-height": 1,
                "font-name": "Icons",
                "font-size": sp(24),
            },
        },
        "Display": {
            "large": {
                "line-height": 1.64,
                "font-name": "GothicA1",
                "font-size": sp(57),
            },
            "medium": {
                "line-height": 1.52,
                "font-name": "GothicA1",
                "font-size": sp(45),
            },
            "small": {
                "line-height": 1.40,
                "font-name": "GothicA1",
                "font-size": sp(36),
            },
        },
        "Headline": {
            "large": {
                "line-height": 1.40,
                "font-name": "GothicA1",
                "font-size": sp(32),
            },
            "medium": {
                "line-height": 1.36,
                "font-name": "GothicA1",
                "font-size": sp(28),
            },
            "small": {
                "line-height": 1.32,
                "font-name": "GothicA1",
                "font-size": sp(24),
            },
        },
        "Title": {
            "large": {
                "line-height": 1.28,
                "font-name": "Inter",
                "font-size": sp(22),
            },
            "medium": {
                "line-height": 1.24,
                "font-name": "Inter",
                "font-size": sp(16),
            },
            "small": {
                "line-height": 1.20,
                "font-name": "Inter",
                "font-size": sp(14),
            },
        },
        "Body": {
            "large": {
                "line-height": 1.24,
                "font-name": "Inter",
                "font-size": sp(16),
            },
            "medium": {
                "line-height": 1.20,
                "font-name": "Inter",
                "font-size": sp(14),
            },
            "small": {
                "line-height": 1.16,
                "font-name": "Inter",
                "font-size": sp(12),
            },
        },
        "Label": {
            "large": {
                "line-height": 1.20,
                "font-name": "Inter",
                "font-size": sp(14),
            },
            "medium": {
                "line-height": 1.16,
                "font-name": "Inter",
                "font-size": sp(12),
            },
            "small": {
                "line-height": 1.16,
                "font-name": "Inter",
                "font-size": sp(11),
            },
        },
        "TitleBar": {
            "large": {
                "line-height": 1.20,
                "font-name": "LibreFranklin",
                "font-size": sp(20),
            },
            "medium": {
                "line-height": 1.20,
                "font-name": "LibreFranklin",
                "font-size": sp(19),
            },
            "small": {
                "line-height": 1.20,
                "font-name": "LibreFranklin",
                "font-size": sp(18),
            },
        },
        "monospace": {
            "large": {
                "line-height": 2.0,
                "font-name": "MonaspaceArgon",
                "font-size": sp(14),
            },
            "medium": {
                "line-height": 1.6,
                "font-name": "MonaspaceArgon",
                "font-size": sp(12),
            },
            "small": {
                "line-height": 1.5,
                "font-name": "MonaspaceArgon",
                "font-size": sp(10),
            },
        },
    }
