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
from kivy.lang import Builder
from PIL import Image as PILImage
from PIL import ImageSequence
import io
import os
import logging
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.app import App
from kivy.uix.effectwidget import PixelateEffect
from kivymd.uix.label import MDLabel

MIN_SPEED = 0.016  # Fastest speed (60fps)
MAX_SPEED = 0.050   # Slowest speed (10fps)
DEFAULT_SPEED = 0.040  # Default speed (40ms)

class CallbackHandler(logging.Handler):
    """Custom logging handler that calls a callback function for each log record."""
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
    
    def emit(self, record):
        try:
            self.callback(record)
        except Exception:
            self.handleError(record)

class UpdateInfoLabel(MDLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.4}
        self.size_hint_x = None
        self.size_hint_y = None
        logger = logging.getLogger("Update")
        logger.addHandler(CallbackHandler(self.on_log_update))

    def on_log_update(self, record):
        Clock.schedule_once(lambda dt: setattr(self, 'text', record.getMessage()), 0)

img_path = os.path.join(os.getenv("KIVY_DATA_DIR"),"images", "loading_animation.png")

class MWGGLoadingLayout(MDRelativeLayout):
    frames = ListProperty([])
    img_box: MDBoxLayout
    loading = BooleanProperty(False)
    current_image: Image
    current_frame = NumericProperty(0)
    app = ObjectProperty(None)
    _clock_event = None
    log_box: ObjectProperty(None)

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
        self.log_box = UpdateInfoLabel(theme_bg_color="Custom", md_bg_color=(0,0,0,0))

    def on_start(self):
        self.size = (self.app.root.width, self.app.root.height)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

    def show_loading(self, display_logs=False, speed=DEFAULT_SPEED):
        # Guard against shutdown state where widgets might be None
        if self.img_box is None or self.app is None:
            return
            
        if not self.loading and not self.img_box.parent:
            self.loading = True
            self.add_widget(self.img_box)
            if display_logs and self.log_box is not None:
                self.add_widget(self.log_box)
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
        if not self.loading or self.img_box is None:
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
            if self.current_image and self.img_box is not None:
                self.img_box.remove_widget(self.current_image)
                self.current_image = None
            if self.log_box and self.log_box.parent:
                self.remove_widget(self.log_box)
                self.log_box = None
            if self.img_box is not None and self.img_box.parent:
                self.remove_widget(self.img_box)
            # Use the new disable_effects method instead of directly clearing effects
            if hasattr(self.app, 'disable_effects'):
                self.app.disable_effects()
            else:
                # Fallback to old method
                self.app.pixelate_effect.effects = []  # Hide blur
