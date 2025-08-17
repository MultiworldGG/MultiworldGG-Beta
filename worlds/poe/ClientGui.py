import asyncio
import kvui
from typing import TYPE_CHECKING

from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.filemanager import MDFileManager

from kvui import GameManager
from pathlib import Path

if TYPE_CHECKING:
    from .Client import PathOfExileContext


class PoeOptionsTab(MDBoxLayout):
    """Tab containing Path of Exile specific controls."""

    def __init__(self, manager: "PoeManager", **kwargs) -> None:
        super().__init__(orientation="vertical", spacing=dp(5), padding=dp(10), **kwargs)
        self.manager = manager
        self.ctx: "PathOfExileContext" = manager.ctx

        # Initialize file manager
        self.file_manager = MDFileManager(
            exit_manager=self.close_file_manager,
            select_path=self.select_client_path,
        )

        # client.txt path
        client_path_layout = MDBoxLayout(orientation="horizontal", spacing=dp(5))

        set_client_btn = MDButton(MDButtonText(text="Set Client Path"), style="filled", size_hint_x=None)
        set_client_btn.width = dp(120)  # Fixed width for the button
        set_client_btn.bind(on_release=self.open_file_manager)
        client_path_layout.add_widget(set_client_btn)

        # Display the currently selected path (read-only)
        self.client_path_label = MDLabel(
            text=self.ctx.client_text_path if self.ctx.client_text_path else "No path selected",
            halign="left",
            size_hint_x=1,
        )
        client_path_layout.add_widget(self.client_path_label)

        self.add_widget(client_path_layout)

        # base filter path
        filter_layout = MDBoxLayout(orientation="horizontal", spacing=dp(5))

        # Set filter button
        set_filter_btn = MDButton(MDButtonText(text="Set Filter"), style="filled", size_hint_x=None)
        set_filter_btn.width = dp(120)  # Fixed width for the button
        set_filter_btn.bind(on_release=self.set_filter)
        filter_layout.add_widget(set_filter_btn)

        # Filter input text field
        self.filter_input = MDTextField(
            hint_text="Base Item Filter",
            size_hint_x=1,  # Textbox takes remaining space
            width=dp(300),  # Minimum width for the text box
        )
        if self.ctx.base_item_filter:
            self.filter_input.text = self.ctx.base_item_filter
        filter_layout.add_widget(self.filter_input)

        # Add the layout to the main container
        self.add_widget(filter_layout)

        # auth button
        auth_btn = MDButton(MDButtonText(text="Auth"), style="filled")
        auth_btn.bind(on_release=lambda *_: self.manager.commandprocessor._cmd_poe_auth())
        self.add_widget(auth_btn)

        # start/stop buttons
        start_btn = MDButton(MDButtonText(text="Start Client"), style="filled")
        start_btn.bind(on_release=lambda *_: self.manager.commandprocessor._cmd_start_poe())
        self.add_widget(start_btn)

        stop_btn = MDButton(MDButtonText(text="Stop Client"), style="filled")
        stop_btn.bind(on_release=lambda *_: self.manager.commandprocessor._cmd_stop())
        self.add_widget(stop_btn)

        # status label
        self.status_label = MDLabel(text="Client not running")
        self.add_widget(self.status_label)
        Clock.schedule_interval(self.update_status, 1)

        # TTS controls
        tts_layout = MDBoxLayout(orientation="horizontal", spacing=dp(5), adaptive_width=False)
        tts_speed_btn = MDButton(MDButtonText(text="Set TTS Speed"), style="filled")
        tts_speed_btn.bind(on_release=self.set_tts_speed)
        tts_layout.add_widget(tts_speed_btn)

        self.tts_speed_input = MDTextField(hint_text="TTS Speed", input_filter="int")
        if self.ctx.tts_options.speed:
            self.tts_speed_input.text = str(self.ctx.tts_options.speed)
        tts_layout.add_widget(self.tts_speed_input)
        self.add_widget(tts_layout)

        generate_tts_btn = MDButton(MDButtonText(text="Generate TTS"), style="filled")
        generate_tts_btn.bind(on_release=lambda *_: self.manager.commandprocessor._cmd_generate_tts())
        self.add_widget(generate_tts_btn)

    def open_file_manager(self, *_):
        """Open the file manager to select a file."""
        self.file_manager.show("/")  # Start at the root directory
        
    def open_file_manager_for_client_txt(self, *_):
        """Open the file manager to select a file."""
        possible_paths = [
            Path("D:/games/Path of Exile/logs/client.txt"),
            Path("D:/games/Path of Exile/logs/client.txt"),
            Path("D:/games/Path of Exile/logs/client.txt"),
            Path("D:/games/Path of Exile/logs/client.txt"),
            Path("D:/games/poe/logs/client.txt"),
        ]
        self.file_manager.show("/")  # Start at the root directory
        self.file_manager.ext = ["Client.txt"]

    def close_file_manager(self, *_):
        """Close the file manager."""
        self.file_manager.close()

    def select_client_path(self, path: str):
        """Handle the selected file path."""
        self.client_path_label.text = path  # Update the label with the selected path
        self.manager.commandprocessor._cmd_set_client_text_path(path)  # Update the context
        self.close_file_manager()

    def set_filter(self, *_):
        filt = self.filter_input.text.strip()
        if filt:
            self.manager.commandprocessor._cmd_base_item_filter(filt)

    def set_tts_speed(self, *_):
        speed = self.tts_speed_input.text.strip()
        if speed:
            self.manager.commandprocessor._cmd_tts_speed(speed)

    def update_status(self, _dt):
        if self.ctx.running_task and not self.ctx.running_task.done():
            self.status_label.text = "Client running"
        else:
            self.status_label.text = "Client not running"


class PoeManager(GameManager):
    logging_pairs = [
        ("Client", "Archipelago"),
    ]
    base_title = "Archipelago Path of Exile Client"
    ctx: "PathOfExileContext"

    def build(self):
        container = super().build()
        self.add_client_tab("Path of Exile client", PoeOptionsTab(self))
        return container


def start_gui(context: "PathOfExileContext") -> None:
    context.ui = PoeManager(context)
    context.ui_task = asyncio.create_task(context.ui.async_run(), name="UI")