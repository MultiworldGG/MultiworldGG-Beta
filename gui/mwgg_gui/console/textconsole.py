from __future__ import annotations
"""
TextConsole class - creates the text console to be added to the following screens:
console
console_compact

This is a wrapper around the updated MarkupTextField class, and is used to
display the text console.
"""
from kivy.core.window import Window
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDFabButton
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
import logging
from logging.handlers import QueueHandler
from multiprocessing import Queue
from multiprocessing.queues import Empty
from kivy.utils import get_hex_from_color
from mwgg_gui.overrides.markuptextfield import MarkupTextField
from mwgg_gui.components.guidataclasses import MarkupPair

from NetUtils import TEXT_COLORS

__all__ = ('TextConsole', 'ConsoleView',)

Builder.load_string('''
<BottomScrollButton>:
    id: bottom_scroll_button
    icon: 'arrow-down-bold-outline'
    style: 'small'
''')

class BottomScrollButton(MDFabButton):
    pass

## helper class to return both Client and Archipelago logs
class ConsoleFilter(logging.Filter):
    def filter(self, record):
        if record.name.endswith("Client"):
            return True
        elif record.name == "Archipelago" or record.name == "MultiWorld":
            return True
        return False

class TextConsole(MarkupTextField, ThemableBehavior):
    text_buffer: Queue
    app: MDApp

    def __init__(self, bottom_scroll_button=None, **kwargs):
        super().__init__(bottom_scroll_button=bottom_scroll_button, **kwargs)
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
        self.text_buffer = self.app.text_buffer
        Clock.schedule_once(self.set_all_players_chat, 0)
        # self.lines_to_scroll = int(self.app.config.get('client', 'scroll_lines', fallback=3))

        Clock.schedule_interval(self.add_text_from_buffer, 0)

    def set_all_players_chat(self, dt):
        self.app.ctx.all_players_chat = self.app.app_config.get('client', 'all_players_chat', fallback=True)

    def add_text_from_buffer(self, dt):
        chunk_size = 50  # Process up to 50 items per frame
        text_chunks = []
        plaintext_chunks = []
        
        try:
            # Collect items from queue in chunks
            for _ in range(chunk_size):
                queue_item = self.text_buffer.get_nowait()
                # Handle MarkupPair tuple and string (log record) cases
                if isinstance(queue_item, MarkupPair):
                    text_chunks.append(queue_item.text)
                    plaintext_chunks.append(queue_item.plaintext)
                elif isinstance(queue_item, str):
                    # String comes in as plaintext (no markup) - use tuple with same value for both
                    text_chunks.append(queue_item)
                    plaintext_chunks.append(queue_item)
                else:
                    # Handle objects with msg attribute (log records)
                    if hasattr(queue_item, 'msg'):
                        text_chunks.append(queue_item.msg)
                        plaintext_chunks.append(queue_item.msg)
                    else:
                        raise ValueError(f"Invalid queue item type: {type(queue_item)}")
        except Empty:
            # No more items in queue, process what we collected
            pass
        except Exception as e:
            print(e)
            return
        
        # If we collected any items, set them all at once
        if text_chunks:
            combined_text = "\n".join(text_chunks)
            combined_plaintext = "\n".join(plaintext_chunks)
            self.set_texts(combined_text, combined_plaintext)

class ConsoleView(MDFloatLayout):
    text_console = ObjectProperty(None)
    bottom_scroll_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bottom_scroll_button = BottomScrollButton(opacity=0, x=Window.width - dp(60), y=dp(10))
        self.text_console = TextConsole(bottom_scroll_button=self.bottom_scroll_button, pos_hint={"x": 0, "y": 0}, 
                                        size_hint=(1-(4/Window.width),1-(185/Window.height)))
        self.add_widget(self.text_console)
        self.text_console.fbind('scroll_y', self.set_bottom_scroll_button_opacity)
        self.add_widget(self.bottom_scroll_button)

    def console_handler(self) -> QueueHandler:
        """Create a StreamHandler that writes directly to the text_buffer"""
        _console_out = QueueHandler(queue=self.text_console.text_buffer)
        _console_out.setFormatter(logging.Formatter("%(message)s"))
        _console_out.setLevel(logging.INFO)
        _console_out.addFilter(ConsoleFilter())
        return _console_out

    def set_bottom_scroll_button_opacity(self, instance, value):
        """Show button when not at the bottom of the scroll"""
        max_scroll_y = max(0, self.text_console.minimum_height - self.text_console.height)
        # Show button if scroll_y is less than max_scroll_y (not at bottom)
        # Add small threshold to avoid flickering at the exact bottom
        self.bottom_scroll_button.opacity = 1 if value < max_scroll_y - self.text_console.height else 0