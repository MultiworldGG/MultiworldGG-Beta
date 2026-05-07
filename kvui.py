from mwgg_gui.components.dialog import MessageBox
from mwgg_gui.overrides.screen import CustomScreen

from Gui import (MWGGUIApp as ThemedApp, 
                KivyMarkupJSONtoTextParser as KivyJSONtoTextParser,
                MainScreenMgr as MDScreenManagerBase

                )
from kivymd.uix.scrollview import MDScrollView as ScrollBox
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivymd.uix.appbar import MDAppBarNavigationButton as MDNavigationItemBase
from kivymd.uix.screen import MDScreen
from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDLinearProgressIndicator
from kivymd.uix.floatlayout import MDFloatLayout

class GameManager(ThemedApp):

    def add_client_tab(self, title: str, content: Widget, index: int = -1) -> MDNavigationItemBase:
        '''Stub function for client hook'''
        return self.create_custom_screen(title, content, index)

    def remove_client_tab(self, tab: MDNavigationItemBase) -> None:
        '''Stub function for client hook'''
        self.remove_custom_screen(tab)

    def create_custom_screen(self, title: str, content: Widget, index: int = -1) -> MDNavigationItemBase:
        """
        Adds a new screen to the client window with a given title, and provides a given Widget as its content.
        Returns the new button widget, with the provided content being placed on the screen as content.

        :param title: The title of the screen.
        :param content: The Widget to be added as content for this screen's new MDScreen. Will also be added to the
         returned button as button.content.
        :param index: The index to insert the button at. Defaults to -1, meaning the button will be appended to the end.

        :return: The new navigation item button.
        """
        new_button = MDNavigationItemBase(text=title)
        new_screen = CustomScreen(name=title)
        new_screen.custom_layout.add_widget(content)
        new_screen.bottom_appbar.add_widget(new_button)
        self.screen_manager.add_widget(new_screen, index=index)
        return new_button

    def remove_custom_screen(self, button: MDNavigationItemBase):
        self.screen_manager.remove_screen(button.text)
