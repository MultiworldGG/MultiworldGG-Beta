from __future__ import annotations

from kivy.properties import ColorProperty
from kivymd.uix.imagelist import MDSmartTileImage
from kivymd.uix.button import MDIconButton

"""
LAUNCHER FAVORITE BAR

FavoritesCarousel - carousel for displaying favorite games
FavoriteToggleButton - button for toggling a favorite game
Favorite - widget for displaying a favorite game
"""
__all__ = ('FavoritesCarousel', 
           'Favorite'
           )

from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.imagelist import MDSmartTile
import logging
from typing import Any

from kivy.app import App
from mwgg_igdb import GameIndex

logger = logging.getLogger("Client")

Builder.load_string('''

<FavoritesCarousel>:
    do_x_scroll: True
    do_y_scroll: False
    effect_y: "ScrollEffect"
    size_hint_x: None
    size_hint_y: None
    bar_color: [0,0,0,0]
    inactive_bar_color: [0,0,0,0]
    height: dp(65)

<FavoriteToggleButton>:
    style: "standard"
    pos_hint:{"right": 1, "top": 1}
    theme_text_color: "Custom"
    text_color: app.theme_cls.onPrimaryColor

<Favorite>:
    size_hint_x: None
    size_hint_y: None
    width: dp(85)
    height: dp(65)
    pos_hint: {"center_y": 0.5}
    favorite_image: favorite_image

    FavoriteImage:
        source: root.game_cover_url
        id: favorite_image

        canvas:
            Color:
                rgba: app.theme_cls.primaryColor if root.favorite_state == "selected" else app.theme_cls.transparentColor
            BoxShadow:
                inset: True
                size: dp(85), dp(65)
                offset: 0, 0
                spread_radius: 5, 5
                blur_radius: 10

    MDSmartTileOverlayContainer:
        overlap: True
        orientation: 'vertical'
        overlay_mode: 'footer'
        FavoriteToggleButton:
            icon: "heart" if root.game_module in app.launcher_screen.saved_games else "heart-outline"
            on_release: root.toggle_favorite()
        MDLabel:
            pos_hint: {"x": 0, "y": 0}
            size_hint_y: .5
            text: root.game_name
            halign: 'center'
            theme_font_style: "Custom"
            font_style: "Monospace-SM"
            role: "medium"
            bold: True
            outline_color: app.theme_cls.onSurfaceVariantColor
            outline_width: 1
            theme_text_color: "Custom"
            text_color: app.theme_cls.surfaceContainerHighestColor
''')


class FavoritesScroll(MDScrollView):
    favorites: ObjectProperty
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.favorites = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_x=None, size_hint_y=None, height=dp(75), width=dp(1000), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.add_widget(self.favorites)

class FavoriteImage(MDSmartTileImage):
    pass

class FavoriteToggleButton(MDIconButton):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        return False

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            return super().on_touch_up(touch)
        return False

class Favorite(MDSmartTile):
    """Custom Layout for displaying favorite games"""
    game_module = StringProperty("")
    game_name = StringProperty("")
    label_bg_color = ColorProperty([0,0,0,0])
    click_down_pos = ListProperty([])
    app = ObjectProperty()
    favorite_image: ObjectProperty
    favorite_state = StringProperty("normal")
    img_pos = ListProperty([0,0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.favorite_state = "normal"
    @property
    def game_cover_url(self):
        """Get the cover URL for the game"""
        if not self.game_module:
            return ""
        try:
            game_data = GameIndex.get_game(self.game_module)
            return game_data.get('cover_url', "") if game_data else ""
        except:
            return ""

    def on_touch_down(self, touch):
        self.click_down_pos = touch.pos
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.click_down_pos:
            if self.collide_point(*self.click_down_pos):
                self.app.launcher_screen.on_favorite_clicked(self.game_module)
                self.app.launcher_screen.set_favorite_highlight(self)
            self.click_down_pos = []
            return super().on_touch_up(touch)

    def toggle_favorite(self):
        self.app.launcher_screen.toggle_favorite(self.game_module)

    def highlight(self):
        #self.img_pos = self.favorite_image.pos
        self.favorite_state = "selected"

    def unhighlight(self):
        #self.img_pos = self.favorite_image.pos
        self.favorite_state = "normal"