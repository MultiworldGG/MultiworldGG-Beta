"""
Dialog class - MessageBox override for dialogs
"""
from __future__ import annotations
__all__ = ("MessageBox", "ConsoleBox")

from kivymd.uix.dialog import (MDDialog, 
                               MDDialogHeadlineText, 
                               MDDialogSupportingText, 
                               MDDialogButtonContainer, 
                               MDDialogContentContainer)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHelperText
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.properties import ObjectProperty

from typing import Callable
from asyncio import Queue

class MessageBox(MDDialog):
    """
    A simple KivyMD dialog class that can be used throughout the codebase.
    
    Args:
        title (str): The dialog title
        message (str): The dialog message content
        is_error (bool): If True, shows error styling
    """

    cancel_button: ObjectProperty

    def __init__(self, title="", message="", callback: Callable[[bool], None] = None, is_error=False):
        super().__init__()
        self.title = title
        self.message = message
        self.callback = callback
        self.is_error = is_error
        self.app = MDApp.get_running_app()
        self.dialog = None
        self.cancel_button = Widget()
        if self.callback:
            self.cancel_button = MDButton(
                MDButtonText(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.app.theme_cls.onSurfaceColor,
                ),
                on_release=self._cancel,
            ),

    
    def _ok(self, instance):
        self.dialog.dismiss()
        self.dialog = None
        if self.callback:
            self.callback(True)
    
    def _cancel(self, instance):
        self.dialog.dismiss()
        self.dialog = None
        if self.callback:
            self.callback(False)
        
    def open(self):
        """Opens the dialog and displays it to the user."""
        # Create the dialog
        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text=self.title,
            ),
            MDDialogContentContainer(
                MDDialogSupportingText(
                    text=self.message,
                    theme_text_color="Custom" if self.is_error else "Primary",
                    text_color=self.app.theme_cls.errorColor if self.is_error else self.app.theme_cls.onSurfaceColor,
                ),
            ),
            MDDialogButtonContainer(
                self.cancel_button,
                MDButton(
                    MDButtonText(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.app.theme_cls.errorColor if self.is_error else self.app.theme_cls.onSurfaceColor,
                    ),
                    on_release=lambda instance: self._ok(instance),
                ),
                spacing=dp(8),
            ),
        )
        self.dialog.state_press = 0
        self.dialog.open()


class ConsoleBox(MDDialog):
    """
    A dialog for interactive console-style prompts with text input.
    Used for slot name and password prompts in the client.
    
    Args:
        title (str): The dialog title
        prompt (str): The prompt text to display
        ctx: The context object (InitContext or CommonContext)
        is_password (bool): If True, hides the input text (for passwords)
    """
    
    def __init__(self, title="", prompt=""):
        super().__init__()
        self.title = title
        self.prompt = prompt
        self.app = MDApp.get_running_app()
        self.dialog = None
        self.text_input = None
    
    def _submit(self, instance):
        """Handle submit button press."""
        if hasattr(self.app.ctx, 'input_requests') and self.app.ctx.input_requests > 0:
            self.app.ctx.input_requests -= 1
            self.app.ctx.input_queue.put_nowait(self.text_input.text)
        self.dialog.dismiss()
        self.dialog = None
    
    def _cancel(self, instance):
        """Handle cancel button press."""
        # Just dismiss the dialog on cancel
        self.dialog.dismiss()
        self.dialog = None
        
    def open(self):
        """Opens the dialog and displays it to the user."""
        # Create text input field
        if 'password' in self.prompt.lower():
            self.is_password = True
        else:
            self.is_password = False
        self.text_input = MDTextField(
            password=self.is_password,
            mode="outlined",
            size_hint_y=None,
            height=dp(56),
            on_text_validate=self._submit,
        )
        
        # Create button container
        button_container = MDDialogButtonContainer(
            Widget(),
            MDButton(
                MDButtonText(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.app.theme_cls.onSurfaceColor,
                ),
                on_release=self._cancel,
            ),
            MDButton(
                MDButtonText(
                    text="Submit",
                    theme_text_color="Custom",
                    text_color=self.app.theme_cls.primaryColor,
                ),
                on_release=self._submit,
            ),
            spacing=dp(8),
        )
        
        # Create the dialog
        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text=self.title,
            ),
            MDDialogSupportingText(
                text=self.prompt,
                theme_text_color="Primary",
                text_color=self.app.theme_cls.onSurfaceColor,
            ),
            self.text_input,
            button_container,
        )
        self.dialog.state_press = 0
        self.dialog.open()
        
        # Focus the text input
        if self.text_input:
            self.text_input.focus = True
