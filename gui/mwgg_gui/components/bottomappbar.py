"""
BottomAppBar class - creates the bottom app bar that will be added to
the bottom of the screen.  Additionally creates helper functions to bind
to the mouse and window events to display the appropriate icons and 
text input fields.
"""
from __future__ import annotations

__all__ = (
    "BottomAppBar",
    "BottomBarTextInput"
)
from kivymd.uix.appbar import MDBottomAppBar, MDActionBottomAppBarButton
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from mwgg_gui.constants import CONSOLE_ACTIONS, LAUNCHER_ACTIONS

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
    leading_icon: leading_icon
    MDTextFieldLeadingIcon:
        id: leading_icon
    MDTextFieldHintText:
        text: root.hint_text
''')

def is_command_input(string: str) -> bool:
    return len(string) > 0 and string[0] in "/!"

class BottomBarTextInput(MDTextField):
    action_type: StringProperty
    leading_icon: ObjectProperty
    icon: StringProperty
    hint_text: StringProperty
    silent_prefix: StringProperty
    app: MDApp

    #hint autocomplete
    min_chars = NumericProperty(3)
    item_names: list[str] = []
    location_names: list[str] = []
    
    #BottomAppBar is a MDFloatLayout already, so we can place the TextField in it without shenanigans
    def __init__(self, *args, **kwargs):
        self.hint_text = ""
        self.silent_prefix = ""
        self.action_type = "console"
        self.app = MDApp.get_running_app()
        super().__init__(*args, **kwargs)
        self.leading_icon = self.ids.leading_icon
        self.icon = "blank"
        self.dropdown = MDDropdownMenu(caller=self, position="top", border_margin=dp(2), width=self.width)
        self.bind(on_text_validate=self.on_fork)
        self.bind(width=lambda instance, x: setattr(self.dropdown, "width", x))
        self.write_tab = False

    def on_fork(self, instance):
        self.hint_text = ""
        self.dropdown.items.clear()
        if self.action_type == "hint":
            self.on_hint_search(instance.text)
        elif self.action_type == "admin":
            self.on_admin_message(instance.text)
        else:
            self.on_message(instance.text)
        self.text = ""

    @property
    def icon(self):
        return self.leading_icon.icon

    @icon.setter
    def icon(self, value):
        self.leading_icon.icon = value

    def on_admin_message(self, text):
        if "login" in text.lower() or "logout" in text.lower():
            self.app.on_message("!admin "+text, self)
        else:
            self.app.on_message("!admin /"+text, self)

    def on_hint_search(self, text):
        if text in self.item_names:
            self.app.on_message("!hint "+text, self)
            self.item_names = []
            self.location_names = []
        elif text in self.location_names:
            self.app.on_message("!hint_location "+text, self)
            self.item_names = []
            self.location_names = []

    def on_message(self, text):
        self.app.on_message(text, self)

    def on_text(self, instance, value):
        if self.action_type == "admin":
            self.on_admin_input(instance, value)
        if self.action_type == "hint":
            self.on_hint_input(instance, value)
        else:
            return

    def on_admin_input(self, instance, value):
        self.dropdown.items.clear()
        ctx = self.app.ctx
        if not ctx.server:
            return

        self.admin_commands = {"login": "Login to the server"} if not ctx.admin else {
            'collect': 'Usage: collect <username>', 
            'release': 'Usage: release <username>', 
            'send_location': 'Usage: send_location <user_with_location> <location_name>', 
            'hint': 'Usage: hint <username> <item_name>', 
            'hint_location': 'Usage: hint_location <username> <location_name>', 
            'option': 'Usage: option <server_option_name> <server_option_value>',
            'logout': 'Usage: logout'
        }
        
        # Add commands to dropdown
        for command in sorted(self.admin_commands.items()):
            self.dropdown.items.append({
                "text": command[0],
                "on_release": lambda x, cmd=command: self._select_admin_command(cmd),
            })

    def _select_admin_command(self, command):
        """Handle selection of an admin command from the dropdown"""
        self.text = command[0]
        self.hint_text = command[1]
        self.dropdown.dismiss()
    
    def on_hint_input(self, instance, value):
        if len(value) >= self.min_chars:
            self.dropdown.items.clear()
            ctx = self.app.ctx
            if not ctx.game:
                return
            # TODO: Grab the flag, too to set the color in the dropdown
            self.item_names = [item for item in ctx.item_names._game_store[ctx.game].values()]
            self.location_names = [location for location in ctx.location_names._game_store[ctx.game].values()]

            def on_press(text):
                self.text = text
                self.dropdown.dismiss()
                self.focus = True

            lowered = value.lower()
            for hint_name in self.item_names + self.location_names:
                try:
                    index = hint_name.lower().index(lowered)
                except ValueError:
                    pass  # substring not found
                else:
                    # text = escape_markup(hint_name)
                    # text = text[:index]+text[index:index+len(value)]+text[index+len(value):]
                    self.dropdown.items.append({
                        "text": hint_name, #text to add markup
                        "on_release": lambda txt=hint_name: on_press(txt),
                        "leading_icon": "map-marker" if hint_name in self.location_names else "treasure-chest",
                        "markup": True
                    })
                    if len(self.dropdown.items) >= 10:
                        break
            if not self.dropdown.parent:
                self.dropdown.open()
            # else:
            #     Clock.schedule_once(self.dropdown.check_ver_growth, 0.1)
        else:
            self.dropdown.dismiss()

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """
        Override the keyboard_on_key_down method to handle up and down arrow keys for history navigation
        """
        key, key_string = keycode

        if key == 273 and key_string == 'up':
            self._change_to_history_text_if_available(self.app._command_history_index + 1)
            return True
        if key == 274 and key_string == 'down':
            self._change_to_history_text_if_available(self.app._command_history_index - 1)
            return True
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

    def _change_to_history_text_if_available(self, new_index: int) -> None:
        if new_index < -1:
            return
        if new_index >= len(self.app._command_history):
            return
        self.app._command_history_index = new_index
        if new_index == -1:
            self.text = ""
            return
        self.text = self.app._command_history[self.app._command_history_index]

class BottomAppBar(MDBottomAppBar):
    text_input: BottomBarTextInput

    def __init__(self, screen_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_name = screen_name  # Store screen_name for later use
        if screen_name == "console" or screen_name == "hint":
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
        # Toggle: if text input is already visible, hide it. Otherwise, show it.
        if self.text_input.parent and self.text_input.y > -50 and "fab" in instance.id:
            self.hide_text_input()
        else:
            self.animate_text_input(instance.id)

    def on_gui_focus(self):
        self.animate_text_input(self.text_input.id)

    def animate_text_input(self, id_name: str):
        """Animate the text input with properties from the clicked action item"""
        # Find the action data for this button
        action_data = None
        if self.screen_name == "console" or self.screen_name == "hint":
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