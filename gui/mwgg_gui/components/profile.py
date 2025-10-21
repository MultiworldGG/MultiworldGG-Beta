from __future__ import annotations
"""
PROFILE DISPLAY

Widgets to display each part of the profile.

ProfileAvatar:
    Displays the avatar image and allows the user to select a new one.
    Also allows the user to remove the current avatar.
ProfileAlias:
    Displays the alias and allows the user to edit it.
ProfilePronouns:
    Displays the pronouns and allows the user to edit it.
ProfileBK:
    Displays a switch to enable/disable BK mode.
ProfileInCall:
    Displays a switch to enable/disable in call mode.
"""

__all__ = ("ProfileAvatar", 
           "ProfileAlias", 
           "ProfilePronouns", 
           "ProfileBK", 
           "ProfileInCall",
           "show_profile")
import logging
import os
from Utils import persistent_load
from Utils import persistent_store
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldHelperText, MDTextFieldHintText
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.app import MDApp
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import CircularRippleBehavior
from kivy.metrics import dp

from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.fitimage import FitImage
from kivymd.uix.dialog import (MDDialog,
                               MDDialogContentContainer, 
                               MDDialogHeadlineText, 
                               MDDialogSupportingText, 
                               MDDialogButtonContainer)
from kivymd.uix.divider import MDDivider
from kivymd.uix.widget import Widget

from kivy.lang import Builder
import urllib.request
        
logger = logging.getLogger("MultiWorld")

KV = """
<ProfileField>:
    orientation: "horizontal"
    pos_hint: {"center_x": 0.5, "top": 1}
    size_hint_x: 0.8
    size_hint_y: None
    height: dp(80)
    padding: dp(4)
    spacing: dp(4)
    profile_input: profile_input
    profile_input_icon: profile_input_icon
    MDLabel:
        text: root.label
        size_hint_x: 0.3
    MDTextField:
        id: profile_input
        on_text_validate: root.save_profile_field(self.text)
        MDTextFieldLeadingIcon:
            id: profile_input_icon
        MDTextFieldHelperText:
            text: root.hint_text

<ProfileSwitch>:
    orientation: "horizontal"
    size_hint_x: 0.8
    size_hint_y: None
    pos_hint: {"center_x": 0.5}
    height: dp(55)
    padding: dp(4)
    spacing: dp(4)
    profile_switch: profile_switch
    MDLabel:
        text: root.label
        theme_text_color: "Primary"
        size_hint_x: 0.3
    MDSwitch:
        id: profile_switch
        on_active: root.save_profile_switch(self.active)
"""

Builder.load_string(KV)

class ProfileField(MDBoxLayout):
    """Profile field section"""
    label = StringProperty("")
    settings_name = StringProperty("")
    hint_text = StringProperty("")
    profile_input: ObjectProperty = None
    profile_input_icon: ObjectProperty = None
    icon: StringProperty = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.local_player_data = self.app.local_player_data
        self.profile_input = self.ids.profile_input
        self.profile_input_icon = self.ids.profile_input_icon
        self.icon = self.ids.profile_input_icon.icon
        self.profile_input.text = persistent_load().get('client', {}).get(self.settings_name, '')

    def save_profile_field(self, instance):
        """Save profile field to config"""
        if isinstance(instance, MDTextField):
            text = instance.text
        elif isinstance(instance, MDSwitch):
            text = instance.active
        persistent_store('client', self.settings_name, text)
        setattr(self.local_player_data, self.settings_name, text)

    @property
    def icon(self):
        return self.ids.profile_input_icon.icon
    
    @icon.setter
    def icon(self, value):
        self.ids.profile_input_icon.icon = value

class ProfileSwitch(MDBoxLayout):
    """Profile switch section"""
    label = StringProperty("")
    settings_name = StringProperty("")
    profile_switch: ObjectProperty = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.local_player_data = self.app.local_player_data
        self.profile_switch = self.ids.profile_switch

    def save_profile_switch(self, value: bool):
        """Save profile switch value"""
        setattr(self.local_player_data, self.settings_name, value)

class AvatarImage(CircularRippleBehavior, ButtonBehavior, FitImage):
    """Mixin for the avatar image"""
    def __init__(self, **kwargs):
        self.ripple_scale = 0.85
        super().__init__(**kwargs)
    
    def on_release(self):
        pass

class ProfileAvatar(MDBoxLayout):
    """Profile avatar section with local file management"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.local_player_data = self.app.local_player_data
        self.adaptive_height = True
        self.size_hint_x = 0.6
        self.pos_hint = {"center_x": 0.5}
        self.orientation = "vertical"
        self.spacing = dp(8)
        
        # Avatar display (100x100 circular)
        self.avatar_display = AvatarImage(
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            radius=[dp(50), dp(50), dp(50), dp(50)],  # Circular
            source=persistent_load().get('client', {}).get('avatar', ''),
            pos_hint={"center_x": 0.5}
        )
        self.avatar_url_input = MDTextField(
            MDTextFieldHintText(text="https://example.com/avatar.png"),
            id="avatar_url_input",
            mode="outlined",
            size_hint_x=1,
            text=persistent_load().get('client', {}).get('avatar', ''),
        )
        self.avatar_url_input.bind(on_text_validate=lambda instance: self.on_select_avatar_from_url(instance))
        self.avatar_display.bind(on_release=lambda x: setattr(self.avatar_url_input, 'focus', True))
        self.add_widget(self.avatar_display)
        self.add_widget(self.avatar_url_input)
      
    def on_select_avatar_from_url(self, instance):
        """Set avatar from URL input"""
        url = instance.text.strip()
        
        if url:
            # run a request to the url, check if response is an image
            # additionally check image size is less than 1MB
            try:
                response = urllib.request.urlopen(url)
                if response.status == 200:
                    if response.headers['Content-Type'].startswith('image/'):
                        if response.length < 1024 * 1024:
                            self.avatar_display.source = url
                            self.save_avatar(url)
                            return

                self.avatar_url_input.error = True
                self.avatar_url_input.add_widget(MDTextFieldHelperText(
                    text="""Invalid image URL. Please ensure
that the image is no larger than 1MB.
and the image must be a valid image format."""))
                self.avatar_display.source = ""
                self.save_avatar("")
            except Exception as e:
                self.avatar_display.source = ""
                self.save_avatar("")
        return
    
    def save_avatar(self, avatar_path: str):
        """Save avatar path to config"""
        persistent_store('client', 'avatar', avatar_path)
        self.local_player_data.avatar = avatar_path

class ProfileAlias(ProfileField):
    """Profile alias section"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = "Alias"
        self.settings_name = self.label.lower()
        self.hint_text = "Enter your alias"
        self.icon = "rename"
        self.bind(on_text_validate=self.save_profile_field)

class ProfilePronouns(ProfileField):
    """Profile pronouns section"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = "Pronouns"
        self.settings_name = self.label.lower()
        self.hint_text = "Enter your pronouns"
        self.icon = "human-greeting-variant"
        self.bind(on_text_validate=self.save_profile_field)
        
class ProfileBK(ProfileSwitch):
    """Profile status section"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = "BK Mode"
        self.settings_name = "in_bk"
        self.icon = "fast-food"
        self.bind(on_text_validate=self.save_profile_switch)

class ProfileInCall(ProfileSwitch):
    """Profile status section"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = "In Call"
        self.settings_name = "deafened"
        self.icon = "phone"
        self.bind(on_text_validate=self.save_profile_switch)

class ProfileDialog(MDDialog):
    """Profile dialog, overriding some stupid stuff"""
    def add_widget(self, widget):
        if isinstance(widget, ProfileAvatar):
            self.ids.headline_container.add_widget(widget)
            return True
        else:
            super().add_widget(widget)
            return True
    def save_button_release(self):
        """Save button release
        This is so jank."""
        for widget in self.ids.content_container.children[0].children:
            if isinstance(widget, ProfileField):
                widget.save_profile_field(widget.profile_input)
            elif isinstance(widget, ProfileSwitch):
                widget.save_profile_switch(widget.profile_switch.active)
        self.dismiss()

def show_profile():
    """Show the profile dialog"""
    app = MDApp.get_running_app()
    app.profile_dialog = ProfileDialog(
        ProfileAvatar(), MDDialogHeadlineText(
            text=f"{app.local_player_data.slot_name}", size_hint_x=0.6
        ),
        # -----------------------Supporting text-----------------------
        MDDialogSupportingText(
            text=f"""{app.local_player_data.pronouns}
            {app.local_player_data.game}
            {app.local_player_data.game_status}""".replace("  ", ""),
        ),
        # -----------------------Custom content------------------------
        MDDialogContentContainer(
            MDDivider(),
            ProfileAlias(),
            ProfilePronouns(),
            MDDivider(),
            ProfileBK(),
            ProfileInCall(),
            orientation="vertical",
            pos_hint={"center_x": 0.5},
        ),
        # ---------------------Button container------------------------
        MDDialogButtonContainer(
            Widget(),
            MDButton(
                MDButtonText(text="Cancel"),
                style="text",
                on_release=lambda x: app.profile_dialog.dismiss(),
            ),
            MDButton(
                MDButtonText(text="Save"),
                style="text",
                on_release=lambda x: app.profile_dialog.save_button_release(),
            ),
            spacing="8dp",
        ),
        # -------------------------------------------------------------
        auto_dismiss=False,
    )
    app.profile_dialog.open()