from __future__ import annotations
__all__ = (
    "BottomAppBar"
)
from kivy.uix.widget import Widget
from kivymd.uix.appbar import MDBottomAppBar, MDActionBottomAppBarButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.clock import Clock
#from kivydi import CONSOLE_ACTIONS, LAUNCHER_ACTIONS
CONSOLE_ACTIONS = [
{
    "id":           "console",
    "buttonicon":   "chat-outline",
    "icon":         "chat-outline",
    "prefill":      "!countdown",
    "label":        "Console",
    "indicator":    "blank",
    "type":         "assist",
},
{
    "id":           "hint",
    "buttonicon":   "map-search",
    "icon":         "map-search",
    "prefill":      "!hint",
    "label":        "Hint",
    "indicator":    "widgets",
    "type":         "assist",
},
{
    "id":           "admin",
    "buttonicon":   "account-lock-outline",
    "icon":         "wrench",
    "prefill":      "password",
    "label":        "Host Administration",
    "indicator":    "server-network",
    "type":         "assist",
}]


LAUNCHER_ACTIONS = [
{
    "id":           "generate",
    "buttonicon":   "creation-outline",
    "icon":         "creation-outline",
    "prefill":      "",
    "label":        "Generate",
    "indicator":    "blank",
    "type":         "assist",
},
{
    "id":           "host",
    "buttonicon":   "hand-extended",
    "icon":         "hand-extended",
    "prefill":      "",
    "label":        "Host",
    "indicator":    "blank",
    "type":         "assist",
},
{
    "id":           "patch",
    "buttonicon":   "auto-fix",
    "icon":         "auto-fix",
    "prefill":      "",
    "label":        "Patch",
    "indicator":    "blank",
    "type":         "assist",
},
{
    "id":           "yaml",
    "buttonicon":   "code-brackets",
    "icon":         "code-brackets",
    "prefill":      "",
    "label":        "YAML",
    "indicator":    "blank",
    "type":         "assist",
},
{
    "id":           "connect",
    "buttonicon":   "lan-connect",
    "icon":         "lan-connect",
    "prefill":      "",
    "label":        "Connect",
    "indicator":    "blank",
    "type":         "assist",
},
]

Builder.load_string('''
<BottomAppBar>:
    theme_bg_color: "Custom"
    md_bg_color: app.theme_cls.primaryContainerColor \
                    if app.theme_cls.theme_style == "Light" \
                    else app.theme_cls.onPrimaryColor
    MDFabBottomAppBarButton:
        id: text_input_fab
        icon: "chat-outline"
        on_release: root.show_text_input()
                    
<ConsoleTextInput>:
    height: dp(80)
    width: Window.width
    pos: 0, 0
    MDTextField:
        id: text_input
        hint_text: "Enter text"
        write_tab: False
        on_text_validate: root.on_text_validate(text_input.text)
''')
class ConsoleTextInput(MDFloatLayout):
    pass

class BottomAppBar(MDBottomAppBar):

    def __init__(self, screen_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if screen_name == "console":
            actions = CONSOLE_ACTIONS   
        elif screen_name == "launcher":
            actions = LAUNCHER_ACTIONS
        action_items = []
        for item in actions:
            button = MDActionBottomAppBarButton(id=item["id"], 
                                                icon=item["icon"])
            button.bind(on_release=lambda instance: self.on_bar_action(instance))
            action_items.append(button)
        Clock.schedule_once(lambda dt: self.set_actions(action_items), 0)

    def set_actions(self, action_items: list[MDActionBottomAppBarButton]):
        self.action_items = action_items

    def on_bar_action(self, instance):
        print(instance)
        pass
