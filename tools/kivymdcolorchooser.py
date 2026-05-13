from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, ColorProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import hex_colormap, get_hex_from_color
from kivymd.dynamic_color import DynamicColor

from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp

from materialyoucolor.utils.platform_utils import SCHEMES

KV = '''
<ThemeInfo>
    md_bg_color: app.theme_cls.secondaryColor
    color: "grey"
    text: root.text
    adaptive_size: True

<ColorCard>
    orientation: "vertical"

    MDLabel:
        text: root.text
        adaptive_height: True

    MDCard:
        theme_bg_color: "Custom"
        color: "grey"
        md_bg_color: root.bg_color

MDScreen:
    md_bg_color: app.theme_cls.backgroundColor

    MDIconButton:
        color: app.theme_cls.onBackgroundColor
        on_release: app.open_menu(self)
        pos_hint: {"top": .98}
        radius: 20
        x: "12dp"
        icon: "menu"

    MDRecycleView:
        id: theme_info
        viewclass: "ThemeInfo"
        size_hint_y: None
        size_hint_x: .8
        height: 20

    MDRecycleView:
        id: card_list
        viewclass: "ColorCard"
        bar_width: 0
        size_hint_y: None
        height: root.height - dp(68)

        RecycleGridLayout:
            cols: 4
            spacing: "16dp"
            padding: "16dp"
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
'''


class ColorCard(BoxLayout):
    text = StringProperty()
    bg_color = ColorProperty() 

class ThemeInfo(MDLabel):
    text = StringProperty()
    bg_color = ColorProperty()

class Example(MDApp):
    menu: MDDropdownMenu = None
    mypalette = "Blue"
    mystyle = "TONAL_SPOT"

    def build(self):
        return Builder.load_string(KV)

    def get_instance_from_menu(self, name_item):
        index = 0
        rv = self.menu.ids.md_menu
        opts = rv.layout_manager.view_opts
        datas = rv.data[0]

        for data in rv.data:
            if data["text"] == name_item:
                index = rv.data.index(data)
                break

        instance = rv.view_adapter.get_view(
            index, datas, opts[index]["viewclass"]
        )

        return instance

    def open_menu(self, menu_button):
        menu_items = []
        for item, method in {
            "Set palette": lambda: self.set_palette(menu_button),
            "Switch light or dark mode": lambda: self.theme_switch(),
            "Set theme style": lambda: self.set_style(menu_button),
            "Set theme contrast": lambda: self.set_contrast(menu_button),
        }.items():
            menu_items.append({"text": item, "on_release": method})
        self.menu = MDDropdownMenu(
            caller=menu_button,
            items=menu_items,
        )
        self.menu.open()
        

    def set_palette(self, menu_button):
        instance_from_menu = self.get_instance_from_menu("Set palette")
        available_palettes = [
            name_color.capitalize() for name_color in hex_colormap.keys()
        ]

        menu_items = []
        for name_palette in available_palettes:
            menu_items.append(
                {
                    "text": name_palette,
                    "on_release": lambda x=name_palette: self.switch_palette(x),
                }
            )
        MDDropdownMenu(
            caller=menu_button,
            items=menu_items,
        ).open()
        self.menu.dismiss()

    def set_style(self, menu_button):
        instance_from_menu = self.get_instance_from_menu("Set theme style")

        menu_items = []
        for scheme_name in SCHEMES.keys():
            menu_items.append(
                {
                    "text": scheme_name,
                    "on_release": lambda x=scheme_name: self.switch_style(x),
                }
            )
        MDDropdownMenu(
            caller=menu_button,
            items=menu_items,
        ).open()
        self.menu.dismiss()

    def set_contrast(self, menu_button):
        instance_from_menu = self.get_instance_from_menu("Set theme contrast")

        menu_items = []
        for i in range(0,10,5):
            menu_items.append(
                {
                    "text": f'{i}',
                    "on_release": lambda x = i: self.switch_contrast(x),
                }
            )
        MDDropdownMenu(
            caller=menu_button,
            items=menu_items,
        ).open()
        self.menu.dismiss()
        
    def switch_palette(self, selected_palette):
        self.mypalette = selected_palette
        self.theme_cls.primary_palette = selected_palette
        Clock.schedule_once(self.generate_cards, 0.5)

    def theme_switch(self) -> None:
        self.theme_cls.switch_theme()
        Clock.schedule_once(self.generate_cards, 0.5)

    def switch_style(self, scheme) -> None:
        self.mystyle = scheme.capitalize()
        self.theme_cls.dynamic_scheme_name = scheme
        #self.second_menu.dismiss()
        Clock.schedule_once(self.generate_cards, 0.5)

    def switch_contrast(self, contrast) -> None:
        self.theme_cls.dynamic_scheme_contrast = contrast
        #self.second_menu.dismiss()
        Clock.schedule_once(self.generate_cards, 0.5)

    def generate_cards(self, rand):
        self.root.ids.theme_info.data = [{
            "md_bg_color": self.theme_cls.secondaryColor, 
            "text": f"{self.mypalette} set to {self.mystyle.capitalize()}",
        }]
        self.root.ids.card_list.data = []
        __schemes_name_colors = []
        for property_name in dir(DynamicColor):
            if '_' not in property_name:
                __schemes_name_colors.append(property_name)
        for color in __schemes_name_colors:
            value = color
            self.root.ids.card_list.data.append(
                {
                    "bg_color": getattr(self.theme_cls, value),
                    "text": value,
                }
            )
            # if value == "onPrimaryColor":
            #     print(f'color (dark): {getattr(self.theme_cls, value)}, {get_hex_from_color(getattr(self.theme_cls, value))}')
            if value == "primaryContainerColor":
                print(f'color (light): {getattr(self.theme_cls, value)}, {get_hex_from_color(getattr(self.theme_cls, value))}')


    def on_start(self):
        Clock.schedule_once(self.generate_cards)


Example().run()