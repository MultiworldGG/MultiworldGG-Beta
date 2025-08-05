from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import ObjectProperty, ColorProperty, NumericProperty, BooleanProperty
from kivymd.app import MDApp
from kivy.uix.textinput import TextInput
from kivy.utils import escape_markup
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDExtendedFabButton, MDExtendedFabButtonText
from .kivydi.markuptextfield import MarkupTextField
from kivy.clock import Clock
from typing import TextIO
import logging
from logging.handlers import QueueHandler
from multiprocessing import Queue
from multiprocessing.queues import Empty
from kivy.utils import get_hex_from_color

__all__ = ('TextConsole', 'ConsoleView',)

## helper class to return both Client and Archipelago logs
class ConsoleFilter(logging.Filter):
    def filter(self, record):
        return record.name == "Client" or record.name == "Archipelago" or record.name == "MultiWorld"
    
class TextConsole(MarkupTextField, ThemableBehavior):
    text_buffer: Queue
    app: MDApp
    #text_color: ColorProperty

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.font_name = self.theme_cls.font_styles.Monospace['small']['font-name'] 
        self.font_size = self.theme_cls.font_styles.Monospace['small']['font-size']
        self.line_spacing = self.theme_cls.font_styles.Monospace['small']['line-height']
        self.selection_color = self.theme_cls.secondaryColor
        self.selection_color[3] = 0.3
        self.text_default_color = self.app.theme_mw.markup_tags_theme.default_color[0 if self.app.theme_mw.theme_style == "Light" else 1]
        self.multiline = True
        self.do_wrap = True
        self.auto_indent = True
        self.use_menu = True
        self.readonly = True
        self.cursor_color = self.theme_cls.primaryColor
        self.text_buffer = Queue(maxsize=1000)

        Clock.schedule_interval(self.add_text_from_buffer, 0.1)

    def add_text_from_buffer(self, dt):
        try:
            text = self.text_buffer.get_nowait()
            # Handle both string and object with msg attribute
            if isinstance(text, str):
                message_text = text
            else:
                message_text = text.msg
            self.text = self.text + "\n" + message_text
        except Empty:
            return
        except Exception as e:
            print(e)
        finally:
            if self.cursor_row == self.line_count-5:
                self.scroll_to_bottom()

    def scroll_to_bottom(self, *args):
        """Scroll the text console to the bottom"""
        self.focus = True
        self.cursor = self.end_cursor

    def on_scroll_y(self, *args):
        pass
    #         return True

class ConsoleView(MDFloatLayout):
    text_console = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_console = TextConsole(pos_hint={"x": 0, "y": 0}, 
                                        size_hint=(1-(4/Window.width),1-(185/Window.height)))
        self.add_widget(self.text_console)
        
        # # Create the "To Bottom" button
        # self.to_bottom_button = MDExtendedFabButton(MDExtendedFabButtonText(text="Current"),
        #     pos_hint={"center_x": 0.5, "y": 0},
        #     on_release=self.scroll_to_bottom
        # )
        # self.add_widget(self.to_bottom_button)
        # self.to_bottom_button.opacity = 0
        # self.to_bottom_button.disabled = True
        # self.text_console.bind(on_scroll_y=lambda x: self._show_to_bottom_button(x))

    # def _show_to_bottom_button(self, value):
    #     if value > self.text_console.cursor_row:
    #         self.to_bottom_button.opacity = 1
    #         self.to_bottom_button.disabled = False

    # def scroll_to_bottom(self, *args):
    #     """Callback for the To Bottom button"""
    #     self.to_bottom_button.opacity = 0
    #     self.to_bottom_button.disabled = True
    #     self.text_console.scroll_to_bottom(self.to_bottom_button.x, self.to_bottom_button.y)

    def console_handler(self) -> QueueHandler:
        """Create a StreamHandler that writes directly to the text_buffer"""
        _console_out = QueueHandler(queue=self.text_console.text_buffer)
        _console_out.setFormatter(logging.Formatter("%(message)s"))
        _console_out.setLevel(logging.INFO)
        _console_out.addFilter(ConsoleFilter())
        return _console_out