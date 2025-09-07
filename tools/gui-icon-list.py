from kivy.lang import Builder
from kivy.properties import StringProperty
import os

from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.list import MDListItem
from base_fonts import RegisterFonts
from fa_icons import md_icons
from kivy.core.text import LabelBase
from kivy.metrics import sp
from kivymd.theming import ThemableBehavior


os.environ["KIVY_DATA_DIR"] = os.path.join(os.path.dirname(__file__), "..", "kivy", "data")

Builder.load_string('''
#:import images_path kivymd.images_path


<IconItem>

    MDListItemLeadingIcon:
        icon: root.icon

    MDListItemSupportingText:
        text: root.text

    MDListItemTertiaryText:
        text: root.unicode_value


<PreviousMDIcons>
    md_bg_color: self.theme_cls.backgroundColor

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)

        MDBoxLayout:
            adaptive_height: True

            MDIconButton:
                icon: 'magnify'
                pos_hint: {'center_y': .5}

            MDTextField:
                id: search_field
                #hint_text: 'Search icon'
                on_text: root.set_list_md_icons(self.text, True)
                MDTextFieldHintText:
                    text: 'anything goes'
                MDTextFieldHelperText:
                    text: 'Search'
                    mode: "persistent"
                MDTextFieldLeadingIcon:
                    icon: 'magnify'
                MDTextFieldTrailingIcon:
                    icon: 'close'


        RecycleView:
            id: rv
            key_viewclass: 'viewclass'
            key_size: 'height'

            RecycleBoxLayout:
                padding: dp(10), dp(10), 0, dp(10)
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
'''
)

class IconItem(MDListItem):
    icon = StringProperty()
    text = StringProperty()
    unicode_value = StringProperty()


class PreviousMDIcons(MDScreen, ThemableBehavior):
    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''

        def add_icon_item(name_icon):
            unicode_char = md_icons.get(name_icon, "")
            # Convert unicode character to escape sequence
            unicode_escape = repr(unicode_char)[1:-1] if unicode_char else ""
            self.ids.rv.data.append(
                {
                    "viewclass": "IconItem",
                    "icon": name_icon,
                    "text": name_icon,
                    "unicode_value": unicode_escape,
                    "callback": lambda x: x,
                }
            )

        self.ids.rv.data = []
        for name_icon in md_icons.keys():
            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        RegisterFonts(self)
        self.theme_cls.theme_style = "Dark"
        self.screen = PreviousMDIcons()

    def build(self):
        
        return self.screen

    def on_start(self):
        self.screen.set_list_md_icons()


MainApp().run()