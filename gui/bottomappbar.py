from __future__ import annotations

from kivymd.uix.menu.menu import MDDropdownTextItem
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
from kivy.utils import escape_markup
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
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
    MDTextFieldLeadingIcon:
        icon: root.icon
    MDTextFieldHintText:
        text: root.hint_text
''')

def is_command_input(string: str) -> bool:
    return len(string) > 0 and string[0] in "/!"

class BottomBarTextInput(MDTextField):
    action_type: StringProperty
    icon: StringProperty
    hint_text: StringProperty
    silent_prefix: StringProperty
    MAXIMUM_HISTORY_MESSAGES = 50

    #hint autocomplete
    min_chars = NumericProperty(3)
    item_names: list[str] = []
    location_names: list[str] = []
    
    #BottomAppBar is a MDFloatLayout already, so we can place the TextField in it without shenanigans
    def __init__(self, *args, **kwargs):
        self.icon = "blank"
        self.hint_text = "Enter text"
        self.silent_prefix = ""
        self.action_type = "console"
        super().__init__(*args, **kwargs)
        self.dropdown = MDDropdownMenu(caller=self, position="top", border_margin=dp(2), width=self.width)
        self.bind(on_text_validate=self.on_fork)
        self.bind(width=lambda instance, x: setattr(self.dropdown, "width", x))
        self.write_tab = False
        self._command_history_index = -1
        self._command_history: Deque[str] = deque(maxlen=BottomBarTextInput.MAXIMUM_HISTORY_MESSAGES)
            
    def update_history(self, new_entry: str) -> None:
        self._command_history_index = -1
        if is_command_input(new_entry):
            self._command_history.appendleft(new_entry)

    def on_fork(self, instance):
        if self.action_type == "hint":
            self.on_message(instance)
        elif self.action_type == "admin":
            self.on_admin_message(instance)
        else:
            MDApp.get_running_app().on_message(instance)

    def on_admin_message(self, instance):
        MDApp.get_running_app().commandprocessor("!admin "+instance.text)

    def on_message(self, instance):
        if instance.text in self.item_names:
            MDApp.get_running_app().commandprocessor("!hint "+instance.text)
        elif instance.text in self.location_names:
            MDApp.get_running_app().commandprocessor("!hint_location "+instance.text)
        self.item_names = []
        self.location_names = []

    def on_text(self, instance, value):
        if self.action_type != "hint":
            return
        if len(value) >= self.min_chars:
            self.dropdown.items.clear()
            ctx = MDApp.get_running_app().ctx
            if not ctx.game:
                return
            self.item_names = [item for item in ctx.item_names._game_store[ctx.game].values()]
            self.location_names = [location for location in ctx.location_names._game_store[ctx.game].values()]

            def on_press(text):
                split_text = MDDropdownTextItem(text=text)
                self.set_text(self, "".join(text_frag for text_frag in split_text
                                            ))
                self.dropdown.dismiss()
                self.focus = True

            lowered = value.lower()
            for hint_name in self.item_names + self.location_names:
                try:
                    index = hint_name.lower().index(lowered)
                except ValueError:
                    pass  # substring not found
                else:
                    text = escape_markup(hint_name)
                    text = text[:index]+text[index:index+len(value)]+text[index+len(value):]
                    self.dropdown.items.append({
                        "text": text,
                        "on_release": lambda txt=text: on_press(txt),
                        "leading_icon": "map-marker" if hint_name in self.location_names else "treasure-chest"
                    })
            if not self.dropdown.parent:
                self.dropdown.open()
            else:
                self.dropdown.check_ver_growth()
        else:
            self.dropdown.dismiss()

    def on_text_validate(self):
        super().on_text_validate()

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
        self.ids.console_text_input_fab.id = "console_fab_button"
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
        self.text_input.action_type = action_data["id"]
        
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