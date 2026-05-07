from openpyxl.xml.constants import PACKAGE_CHARTSHEETS_RELS
from mwgg_gui.components.dialog import MessageBox
from mwgg_gui.overrides.screen import CustomScreen
from mwgg_gui.console.console import ConsoleSliverAppbar as HintLog
from mwgg_gui.overrides.expansionlist import HintListItem as HintLabel, HintListItemLabel as TooltipLabel, HintListDropdown as MarkupDropdown
from mwgg_gui.overrides.markuptextfield import MarkupTextField as ResizableTextField

from Gui import (MultiMDApp as ThemedApp,
                KivyMarkupJSONtoTextParser as KivyJSONtoTextParser,
                MainScreenMgr as MDScreenManagerBase,
                logging
                )
from kivymd.uix.scrollview import MDScrollView as ScrollBox
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivymd.uix.appbar import MDFabBottomAppBarButton as MDNavigationItemBase
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout as MainLayout
from kivymd.uix.floatlayout import MDFloatLayout as ContainerLayout
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDLinearProgressIndicator
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDButton as ToggleButton

from kivy.uix.image import AsyncImage as ApAsyncImage
from kivymd.uix.tooltip import MDTooltipPlain as ToolTip

class GameManager(ThemedApp):

    async def async_run(self):
        ''' Changing this 'run' to instead do the client takeover loop '''
        if self.ctx._can_takeover_existing_gui():
            await self.ctx._takeover_existing_gui() 
        else:
            logging.critical("Client did not launch properly, exiting.")
            return

    def run(self):
        ''' Stubbing this to catch a 'rerun' of the app (which is already running) '''
        pass

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
        new_button.bind(on_release=lambda *_: setattr(self.screen_manager, "current", title))
        self.screen_manager.add_widget(new_screen, index=index)
        return new_button

    def remove_custom_screen(self, button: MDNavigationItemBase):
        screen = self.screen_manager.get_screen(button.text)
        self.screen_manager.remove_widget(screen)
