"""
Theme class - this works alongside app.theme_cls to provide
text colors, font options and sizes, and other theme-related
settings and overrides.
"""
from __future__ import annotations
__all__ = ('DefaultTheme', 
           'RegisterFonts', 
           'DEFAULT_TEXT_COLORS',
           'adjust_height',
           'AutoAdjustHeightBehavior')


import os
from dataclasses import dataclass
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivy.metrics import sp, dp, Metrics
from kivy.properties import StringProperty, BooleanProperty, BoundedNumericProperty
from kivy.lang import Builder
from kivy.utils import hex_colormap
from kivy.core.window import Window

try:
    from mwgg_gui.overrides import md_icons
except ImportError:
    from ..overrides import md_icons

from PIL import Image
import numpy

from NetUtils import TEXT_COLORS
from BaseUtils import local_path

DEFAULT_TEXT_COLORS = {
    "default_color":["080808", "fafafa"],
    "command_echo_color":["a75600", "ff9334"],
    "player1_color":["b42f88", "ff87d7"],
    "player2_color":["206cb8", "5fafff"],
    "progression_goal_item_color":["a56c00", "ffa700"],
    "progression_item_color":["a46a00", "ffbe00"],
    "progression_deprioritized_item_color":["6a8300", "d2ff49"],
    "useful_item_color":["419F44", "6EC471"],
    "regular_item_color":["3b3b3b", "b2b2b2"],
    "trap_item_color":["8f1515", "d75f5f"],
    "location_color":["006f10", "00c51b"],
    "entrance_color":["2985a0", "60b7e8"]
}
''' Default markup text colors
[Light Mode, Dark Mode]
'''
# Overwriting or adding to default styles.kv
Builder.load_string('''
<Selector>:
    color: app.theme_cls.inversePrimaryColor

<MDTextField>:
    theme_font_name: "Custom"
    theme_font_style: "Custom"
    font_name: app.theme_cls.font_styles[self.font_style][self.role]["font-name"]
    font_size: app.theme_cls.font_styles[self.font_style][self.role]["font-size"]

<MDTextFieldLeadingIcon>:
    theme_icon_color: "Custom"
    icon_color_focus: app.theme_cls.primaryColor
    icon_color_normal: app.theme_cls.onPrimaryColor

<MDTextFieldHintText>:
    theme_font_name: "Custom"
    theme_font_style: "Custom"
    font_name: app.theme_cls.font_styles[self.font_style][self.role]["font-name"]
    font_size: app.theme_cls.font_styles[self.font_style][self.role]["font-size"]
''')
# The names of these colors are from Material Design
# and will be the input for primary_palette
# The colors in hex are actual color for the theme
THEME_OPTIONS = {
    "Light": [("Gray","97f0ff"), #default
              ("Chocolate","ffdbc9"),
              ("Goldenrod","ffdea0"),
              ("Pink","ffd9df"),
              ("Olivedrab","cbef86")],
    "Dark": [("Purple","551353"), #default
             ("Pink","5f112a"),
             ("Brown","5f1414"),
             ("Cyan","003737"),
             ("Green","003a00")]
}

@dataclass
class MarkupTagsTheme:
    default_color: list[str]
    command_echo_color: list[str]
    player1_color: list[str]
    player2_color: list[str]
    progression_goal_item_color: list[str]
    progression_item_color: list[str]
    progression_deprioritized_item_color: list[str]
    useful_item_color: list[str]
    regular_item_color: list[str]
    trap_item_color: list[str]  
    location_color: list[str]
    entrance_color: list[str]

    def __init__(self, **kwargs):
        # Light, Dark
        self.default_color=DEFAULT_TEXT_COLORS["default_color"]
        self.command_echo_color=DEFAULT_TEXT_COLORS["command_echo_color"]
        self.player1_color=DEFAULT_TEXT_COLORS["player1_color"]
        self.player2_color=DEFAULT_TEXT_COLORS["player2_color"]
        self.progression_goal_item_color=DEFAULT_TEXT_COLORS["progression_goal_item_color"]
        self.progression_item_color=DEFAULT_TEXT_COLORS["progression_item_color"]
        self.progression_deprioritized_item_color=DEFAULT_TEXT_COLORS["progression_deprioritized_item_color"]
        self.useful_item_color=DEFAULT_TEXT_COLORS["useful_item_color"]
        self.regular_item_color=DEFAULT_TEXT_COLORS["regular_item_color"]
        self.trap_item_color=DEFAULT_TEXT_COLORS["trap_item_color"]
        self.location_color=DEFAULT_TEXT_COLORS["location_color"]
        self.entrance_color=DEFAULT_TEXT_COLORS["entrance_color"]

    def name(self, color_attr):
        if color_attr == self.default_color: return "Default Text:"
        if color_attr == self.command_echo_color: return "Command Echo:"
        if color_attr == self.player1_color: return "Your Player Slot:"
        if color_attr == self.player2_color: return "Other Players:"
        if color_attr == self.progression_goal_item_color: return "Goal Item:"
        if color_attr == self.progression_item_color: return "Required Item:"
        if color_attr == self.progression_deprioritized_item_color: return "Logically Required Item:"
        if color_attr == self.useful_item_color: return "Useful Item:"
        if color_attr == self.regular_item_color: return "Regular or Filler Item:"
        if color_attr == self.trap_item_color: return "Trap Item:"
        if color_attr == self.location_color: return "Location:"
        if color_attr == self.entrance_color: return "Entrance:"

    def save_color(self, app_config, color_name, color_value):
        """Save a single color value to the config file"""
        app_config.set('markup_tags', color_name, ','.join(color_value))
        app_config.write()

    def load_color(self, app_config, color_name, default_value, theme_style_index):
        """Load a single color value from the config file"""
        value = app_config.get('markup_tags', color_name, fallback=','.join(default_value))
        TEXT_COLORS[color_name] = value.split(',')[theme_style_index]
        return value.split(',')

    def save_all_colors(self, app_config):
        """Save all color values to the config file"""
        for color_name in DEFAULT_TEXT_COLORS.keys():
            color_value = getattr(self, color_name)
            self.save_color(app_config, color_name, color_value)

    def load_all_colors(self, app_config, theme_style_index):
        """Load all color values from the config file"""
        for color_name, default_value in DEFAULT_TEXT_COLORS.items():
            loaded_value = self.load_color(app_config, color_name, default_value, theme_style_index)
            setattr(self, color_name, loaded_value)

class DefaultTheme(ThemableBehavior):
    markup_tags_theme: MarkupTagsTheme
    _theme_style: StringProperty
    _theme_style_index: int
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
        self.markup_tags_theme.load_all_colors(app_config, self._theme_style_index)

    @property
    def theme_style(self):
        return self._theme_style
    @theme_style.setter
    def theme_style(self, value):
        self.primary_palette = THEME_OPTIONS[value][0][0]
        self._theme_style_index = 1 if value == "Dark" else 0
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

    def load_markup_color(self, color_name, theme_style_index):
        """Load a single markup color from the config"""
        default_value = DEFAULT_TEXT_COLORS[color_name]
        return self.markup_tags_theme.load_color(self.app_config, color_name, default_value)

    def recolor_atlas(self):
        """Recolor the atlas image by replacing pixels close to target colors with their respective theme colors.
        """
        try:
            atlas_path = os.path.join(os.getenv("KIVY_DATA_DIR"), "images", "defaulttheme-orig.png")
            output_path = os.path.join(os.getenv("KIVY_DATA_DIR"), "images","defaulttheme-0.png")

            # Open and convert the image
            atlas = Image.open(atlas_path)
            atlas = atlas.convert("RGBA")
            data = numpy.array(atlas)

            # Define the target colors and their replacements
            color_pairs = [
                (numpy.array([50, 164, 206]), numpy.array(self.theme_cls.primaryColor[:3]) * 255, 100),      # cyanish -> primary
                (numpy.array([141, 178, 200]), numpy.array(self.theme_cls.secondaryColor[:3]) * 255, 40),    # blueish -> secondary
                (numpy.array([10, 72, 77]), numpy.array(self.theme_cls.onPrimaryColor[:3]) * 255, 21),       # tealish -> onPrimary
                (numpy.array([32, 72, 77]), numpy.array(self.theme_cls.onSecondaryColor[:3]) * 255, 15),       # alphatealish -> onPrimary
            ]
            
            # Process each color pair sequentially
            for old_color, new_color, tolerance in color_pairs:
                # Calculate color distances for this color
                rgb_data = data[:, :, :3]
                color_diff = numpy.sqrt(numpy.sum((rgb_data - old_color) ** 2, axis=2))
                
                # Create a mask for pixels within tolerance
                mask = color_diff < tolerance
                
                # First, replace exact matches
                exact_match = numpy.all(rgb_data == old_color, axis=2)
                data[exact_match, :3] = new_color
                
                # Then handle all other pixels within tolerance
                for i in range(data.shape[0]):
                    for j in range(data.shape[1]):
                        if mask[i, j] and not exact_match[i, j]:  # Skip exact matches
                            current_pixel = rgb_data[i, j]
                            direction = current_pixel - old_color
                            direction_norm = numpy.linalg.norm(direction)
                            if direction_norm > 0:  # Avoid division by zero
                                direction = direction / direction_norm
                                # Apply the same direction from the new color
                                replacement_color = new_color + direction * color_diff[i, j]
                                # Ensure values stay within valid range
                                replacement_color = numpy.clip(replacement_color, 0, 255)
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
def RegisterFonts(app: MDApp, monospace_font: str = 'Argon'):
    LabelBase.register('Inter',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","Inter-Regular.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","Inter-Italic.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","Inter-Bold.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","Inter-BoldItalic.ttf"))
    LabelBase.register('Neon',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceNeonFrozen-Regular.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceNeonFrozen-Italic.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceNeonFrozen-ExtraBold.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceNeonFrozen-ExtraBoldItalic.ttf")),
    LabelBase.register('Argon',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceArgonFrozen-Regular.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceArgonFrozen-Italic.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceArgonFrozen-ExtraBold.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceArgonFrozen-ExtraBoldItalic.ttf")),
    LabelBase.register('Xenon',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceXenonFrozen-Regular.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceXenonFrozen-Italic.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceXenonFrozen-ExtraBold.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceXenonFrozen-ExtraBoldItalic.ttf")),
    LabelBase.register('Radon',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceRadonFrozen-Regular.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceRadonFrozen-Italic.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceRadonFrozen-ExtraBold.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceRadonFrozen-ExtraBoldItalic.ttf")),
    LabelBase.register('Krypton',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceKryptonFrozen-Regular.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceKryptonFrozen-Italic.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceKryptonFrozen-ExtraBold.ttf"),
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","MonaspaceKryptonFrozen-ExtraBoldItalic.ttf"))
    LabelBase.register('GothicA1',
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","GothicA1-Regular.ttf"),
                        None,
                        os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","GothicA1-Bold.ttf"),
                        None)
    LabelBase.register('Mincho',
                       os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","Mincho-Regular.ttf"),
                       )
    LabelBase.register('LibreFranklin',
                       os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","LibreFranklin-ExtraBold.ttf"),
                       )
    LabelBase.register('Icons',
                       fn_regular=os.path.join(os.getenv("KIVY_DATA_DIR"),"fonts","materialdesignicons-fa-webfont.ttf"),
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
                "font-name": "GothicA1",
                "font-size": sp(22),
            },
            "medium": {
                "line-height": 1.24,
                "font-name": "GothicA1",
                "font-size": sp(16),
            },
            "small": {
                "line-height": 1.20,
                "font-name": "GothicA1",
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
        "Monospace": { # Console font
            "large": {
                "line-height": 2.4,
                "font-name": f"{monospace_font}",
                "font-size": sp(20),
            },
            "medium": {
                "line-height": 2.2,
                "font-name": f"{monospace_font}",
                "font-size": sp(16),
            },
            "small": {
                "line-height": 1.8,
                "font-name": f"{monospace_font}",
                "font-size": sp(14),
            },
        },
        "Monospace-SM": { # Favorites bar font
            "large": {
                "line-height": 1.0,
                "font-name": f"{monospace_font}",
                "font-size": sp(12),
            },
            "medium": {
                "line-height": 1.0,
                "font-name": f"{monospace_font}",
                "font-size": sp(10),
            },
            "small": {
                "line-height": 1.0,
                "font-name": f"{monospace_font}",
                "font-size": sp(8),
            },
        },
    }

class AutoAdjustHeightBehavior:
    """Mixin that automatically adjusts size_hint_y when Window height changes.

    Use for layouts that need to be resizable, while not resizing the menu bars.
    
    Set the height adjustment parameters via class attributes:
        - adjust_title_bar: bool (default True)
        - adjust_app_bar: bool (default True)
        - adjust_bottom_appbar: bool (default False)
        - adjust_custom: int (default 0)
    """
    adjust_title_bar = True
    adjust_app_bar = True
    adjust_bottom_appbar = False
    adjust_custom = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._update_adjusted_height()
        Window.bind(height=self._on_window_height)
    
    def _update_adjusted_height(self, *args):
        self.size_hint_y = adjust_height(
            title_bar=self.adjust_title_bar,
            app_bar=self.adjust_app_bar,
            bottom_appbar=self.adjust_bottom_appbar,
            custom=self.adjust_custom
        )
    
    def _on_window_height(self, instance, value):
        self._update_adjusted_height()


def adjust_height(title_bar: bool=True, 
                  app_bar: bool=True, 
                  bottom_appbar: bool = False, 
                  custom: int = 0) -> float:
    """Returns a float for a size_hint_y value based on the components
    in the layout.
    """
    removed_height = 0
    if title_bar:
        removed_height += dp(43)
    if app_bar:
        removed_height += dp(60)
    if bottom_appbar:
        removed_height += dp(82)
    if custom:
        removed_height += custom
    new_height = Window.height - removed_height
    return new_height/Window.height