"""
Dialog class - MessageBox override for dialogs
"""
from __future__ import annotations
__all__ = ("MessageBox", "show_info_dialog", "show_error_dialog")

from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.metrics import dp

class MessageBox(MDDialog):
    """
    A simple KivyMD dialog class that can be used throughout the codebase.
    
    Args:
        title (str): The dialog title
        message (str): The dialog message content
        is_error (bool): If True, shows error styling
    """
    
    def __init__(self, title="", message="", is_error=False):
        super().__init__()
        self.title = title
        self.message = message
        self.is_error = is_error
        self.app = MDApp.get_running_app()
        self.dialog = None
    
    def _ok(self, instance):
        self.dialog.dismiss()
        self.dialog = None
        
    def open(self):
        """Opens the dialog and displays it to the user."""
        # Create the dialog
        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text=self.title,
            ),
            MDDialogSupportingText(
                text=self.message,
                theme_text_color="Custom" if self.is_error else "Primary",
                text_color=self.app.theme_cls.errorColor if self.is_error else self.app.theme_cls.onSurfaceColor,
            ),
            MDDialogButtonContainer(
                Widget(),
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


# Convenience functions for common use cases
def show_info_dialog(title, message):
    """Show an information dialog."""
    message_box = MessageBox(title=title, message=message, is_error=False)
    message_box.open()
    return message_box


def show_error_dialog(title, message):
    """Show an error dialog."""
    message_box = MessageBox(title=title, message=message, is_error=True)
    message_box.open()
    return message_box
