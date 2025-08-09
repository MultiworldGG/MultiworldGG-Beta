from __future__ import annotations
__all__ = (
    "BottomAppBar"
)
from kivy.uix.widget import Widget
from kivymd.uix.appbar import MDBottomAppBar, MDActionBottomAppBarButton, MDFabBottomAppBarButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDButton
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.textfield import MDTextField
from collections import deque
from typing import Deque
#from kivydi import CONSOLE_ACTIONS, LAUNCHER_ACTIONS
CONSOLE_ACTIONS = [
{
    "id":           "console",
    "buttonicon":   "chat-outline",
    "icon":         "chat-outline",
    "prefill":      "",
    "label":        "Console",
    "indicator":    "blank",
    "type":         "assist",
},
{
    "id":           "hint",
    "buttonicon":   "map-search",
    "icon":         "map-search",
    "prefill":      "!hint ",
    "label":        "Hint",
    "indicator":    "widgets",
    "type":         "assist",
},
{
    "id":           "admin",
    "buttonicon":   "account-lock-outline",
    "icon":         "wrench",
    "prefill":      "!admin ",
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
        id: console_text_input_fab
        icon: "chat-outline"
        on_release: root.on_bar_action(self)
                    
<BottomBarTextInput>:
    id: text_input
    hint_text: "Enter text"
    write_tab: False
    on_text_validate: app.on_message(self)
    MDTextFieldLeadingIcon:
        icon: root.icon
    MDTextFieldHintText:
        text: root.hint_text
''')

def is_command_input(string: str) -> bool:
    return len(string) > 0 and string[0] in "/!"

class BottomBarTextInput(MDTextField):
    icon: StringProperty
    hint_text: StringProperty
    silent_prefix: StringProperty
    MAXIMUM_HISTORY_MESSAGES = 50
    
    #BottomAppBar is a MDFloatLayout already, so we can place the TextField in it without shenanigans
    def __init__(self, *args, **kwargs):
        self.icon = "blank"
        self.hint_text = "Enter text"
        self.silent_prefix = ""
        super().__init__(*args, **kwargs)
        self.write_tab = False
        self._command_history_index = -1
        self._command_history: Deque[str] = deque(maxlen=BottomBarTextInput.MAXIMUM_HISTORY_MESSAGES)
            
    def update_history(self, new_entry: str) -> None:
        self._command_history_index = -1
        if is_command_input(new_entry):
            self._command_history.appendleft(new_entry)

class BottomAppBar(MDBottomAppBar):
    text_input: BottomBarTextInput

    def __init__(self, screen_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_name = screen_name  # Store screen_name for later use
        if screen_name == "console":
            actions = CONSOLE_ACTIONS   
        elif screen_name == "launcher":
            actions = LAUNCHER_ACTIONS
        action_items = []
        text_inputs = []
        for item in actions:
            button = MDActionBottomAppBarButton(id=item["id"], 
                                                icon=item["icon"])
            button.bind(on_release=lambda instance: self.on_bar_action(instance))
            action_items.append(button)
        self.text_input = BottomBarTextInput(id=f'{screen_name}_text_input')
        Clock.schedule_once(lambda dt: self.set_actions(action_items), 0)

    def set_actions(self, action_items: list[MDActionBottomAppBarButton]):
        self.action_items = action_items

    def add_widget(self, widget, index=0, canvas=None):
        """Override add_widget to handle MDTextField widgets"""
        if isinstance(widget, MDTextField):
            # Call MDFloatLayout's add_widget directly
            MDFloatLayout.add_widget(self, widget, index, canvas)
        else:
            super().add_widget(widget, index, canvas)

    def on_bar_action(self, instance):
        self.animate_text_input(instance.id)

    def on_gui_focus(self):
        self.animate_text_input(self.text_input.id)

    def animate_text_input(self, id_name: str):
        """Animate the text input with properties from the clicked action item"""
        # Find the action data for this button
        action_data = None
        if self.screen_name == "console":
            actions = CONSOLE_ACTIONS
        elif self.screen_name == "launcher":
            actions = LAUNCHER_ACTIONS
        else:
            return
        
        # Find the matching action data
        for action in actions:
            if action["id"] in id_name:
                action_data = action
                break
        
        if not action_data:
            return
        
        # Update text input properties
        self.text_input.icon = action_data["icon"]
        self.text_input.hint_text = action_data["label"]
        self.text_input.silent_prefix = action_data["prefill"]
        
        # Show the text input with animation
        if not self.text_input.parent:
            # Add text input to the layout if not already present
            self.add_widget(self.text_input)
        
        # Set position and animate in
        self.text_input.y = -60
        self.text_input.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.text_input.size_hint = (0.4, None)
        
        # Animate the text input appearing
        def animate_in(dt):
            Animation(y=13, duration=0.2).start(self.text_input)
        
        Clock.schedule_once(animate_in, 0.1)
        self.text_input.focus = True
    
    def hide_text_input(self):
        """Hide the text input with animation"""
        if self.text_input.parent:
            def animate_out(dt):
                Animation(y=-60, duration=0.2).start(self.text_input)
                def remove_widget(dt2):
                    if self.text_input.parent:
                        self.remove_widget(self.text_input)
                Clock.schedule_once(remove_widget, 0.2)
            Clock.schedule_once(animate_out, 0.1)