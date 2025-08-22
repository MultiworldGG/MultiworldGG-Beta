from __future__ import annotations
"""
MWGGLoadingLayout

Creates the loading animation within the application
that is displayed when the application is loading various
resources.
"""
__all__ = ("MWGGLoadingLayout",)

from kivy.properties import ListProperty, BooleanProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from PIL import Image as PILImage
from PIL import ImageSequence
import io
import os
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.app import App
from kivy.uix.effectwidget import PixelateEffect

MIN_SPEED = 0.016  # Fastest speed (60fps)
MAX_SPEED = 0.050   # Slowest speed (10fps)
DEFAULT_SPEED = 0.040  # Default speed (40ms)

try:
    img_path = os.path.join(os.getenv("KIVY_HOME"),"images", "loading_animation.png")
except:
    img_path = os.path.join(os.path.dirname(__file__), "images", "loading_animation.png")


class MWGGLoadingLayout(MDRelativeLayout):
    frames = ListProperty([])
    img_box: MDBoxLayout
    loading = BooleanProperty(False)
    current_image: Image
    current_frame = NumericProperty(0)
    app = ObjectProperty(None)
    _clock_event = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = App.get_running_app()
        
        # Create the image box for the loading animation
        self.img_box = MDBoxLayout(theme_bg_color="Custom", md_bg_color=(0,0,0,0), pos_hint={'center_x': 0.5, 'center_y': 0.5}, size=(200,200))
        img = PILImage.open(img_path)
        for i, frame in enumerate(ImageSequence.Iterator(img)):
            new_frame = io.BytesIO()
            frame.save(new_frame,format="png", bitmap_format="png")
            new_frame.seek(0)  # Reset buffer position
            core_image = CoreImage(new_frame, ext='png', filename=f"frame_{i}.png")
            self.frames.append(Image(texture=core_image.texture))
        self.current_image = None
        self.current_frame = 0

    def on_start(self):
        self.size = (self.app.root.width, self.app.root.height)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

    def show_loading(self, speed=DEFAULT_SPEED):
        if not self.loading and not self.img_box.parent:
            self.loading = True
            self.add_widget(self.img_box)
            # Use the new enable_effects method instead of directly setting effects
            if hasattr(self.app, 'enable_effects'):
                self.app.enable_effects()
            else:
                # Fallback to old method
                self.app.pixelate_effect.effects = [PixelateEffect(pixel_size=3)]
            self._clock_event = Clock.schedule_interval(self.update_frame, speed)
    
    def set_speed(self, speed):
        """Set the animation speed. Speed should be between MIN_SPEED and MAX_SPEED."""
        if not self.loading:
            return
            
        # Clamp speed between MIN_SPEED and MAX_SPEED
        speed = max(self.MIN_SPEED, min(self.MAX_SPEED, speed))
        
        # Cancel existing clock event
        if self._clock_event:
            self._clock_event.cancel()
        
        # Schedule new clock event with new speed
        self._clock_event = Clock.schedule_interval(self.update_frame, speed)
    
    def update_frame(self, dt):
        if not self.loading:
            return False
        
        if self.current_image:
            self.img_box.remove_widget(self.current_image)
        
        self.current_image = self.frames[self.current_frame]
        self.img_box.add_widget(self.current_image)
        
        self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def hide_loading(self, *args):
        if self.loading:
            self.loading = False
            if self._clock_event:
                self._clock_event.cancel()
                self._clock_event = None
            if self.current_image:
                self.img_box.remove_widget(self.current_image)
                self.current_image = None
            if self.img_box.parent:
                self.remove_widget(self.img_box)
            # Use the new disable_effects method instead of directly clearing effects
            if hasattr(self.app, 'disable_effects'):
                self.app.disable_effects()
            else:
                # Fallback to old method
                self.app.pixelate_effect.effects = []  # Hide blur

