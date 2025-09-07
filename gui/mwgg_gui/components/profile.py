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
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
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
                               MDDialogIcon, 
                               MDDialogContentContainer, 
                               MDDialogHeadlineText, 
                               MDDialogSupportingText, 
                               MDDialogButtonContainer)
from kivymd.uix.list import (MDListItem, 
                             MDListItemLeadingAvatar,
                             MDListItemLeadingIcon, 
                             MDListItemSupportingText)
from kivymd.uix.divider import MDDivider
from kivymd.uix.widget import Widget

from mwgg_gui.components.guidataclasses import UIPlayerData
from Utils import user_path
from FileUtils import FileUtils
from kivy.lang import Builder
from typing import TYPE_CHECKING, Any, Optional
        
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
        self.profile_input.text = self.app.app_config.get('client', self.settings_name, fallback='')

    @property
    def icon(self):
        return self.ids.profile_input_icon.icon
    
    @icon.setter
    def icon(self, value):
        self.ids.profile_input_icon.icon = value

    def save_profile_field(self, instance):
        """Save profile field to config"""
        self.app.app_config.set('client', self.settings_name, instance.text)
        self.app.app_config.write()
        setattr(self.local_player_data, self.settings_name, instance.text)

class ProfileSwitch(MDBoxLayout):
    """Profile switch section"""
    label = StringProperty("")
    settings_name = StringProperty("")
    profile_switch: ObjectProperty = None
    #icon: StringProperty = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.local_player_data = self.app.local_player_data
        self.profile_switch = self.ids.profile_switch
        #self.icon = self.ids.profile_switch.icon

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
        self.size_hint_x = 0.4
        self.pos_hint = {"center_x": 0.5}
        
        # Avatar display (100x100 circular)
        self.avatar_display = AvatarImage(
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            radius=[dp(50), dp(50), dp(50), dp(50)],  # Circular
            source=self.get_avatar_path(),
            pos_hint={"center_x": 0.5}
        )
        self.avatar_display.bind(on_release=self.on_select_avatar)
        self.add_widget(self.avatar_display)
    
    def get_avatar_path(self):
        """Get the current avatar file path"""
        avatar_file = self.app.app_config.get('client', 'avatar', fallback='')
        if avatar_file and os.path.exists(avatar_file):
            return avatar_file
        return ""
    
    def on_select_avatar(self, instance):
        """Select an avatar"""
        self.avatar_display.source = FileUtils.open_file_input_dialog(
            title="Select Avatar",
            filetypes=[("Image Files", ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.webp"])],
            suggest=user_path()
        )
        self.save_avatar(self.avatar_display.source)
    
    def save_avatar(self, avatar_path: str):
        """Save avatar path to config"""
        self.app.app_config.set('client', 'avatar', avatar_path)
        self.app.app_config.write()
        self.local_player_data.avatar = avatar_path

class ProfileAlias(ProfileField):
    """Profile alias section"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = "Alias"
        self.settings_name = self.label.lower()
        self.hint_text = "Enter your alias"
        self.icon = "rename"

class ProfilePronouns(ProfileField):
    """Profile pronouns section"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = "Pronouns"
        self.settings_name = self.label.lower()
        self.hint_text = "Enter your pronouns"
        self.icon = "human-greeting-variant"

class ProfileBK(ProfileSwitch):
    """Profile status section"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = "BK Mode"
        self.settings_name = "in_bk"
        self.icon = "fast-food"

class ProfileInCall(ProfileSwitch):
    """Profile status section"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = "In Call"
        self.settings_name = "in_call"
        self.icon = "phone"

class ProfileDialog(MDDialog):
    """Profile dialog, overriding some stupid stuff"""
    def add_widget(self, widget):
        if isinstance(widget, ProfileAvatar):
            self.ids.headline_container.add_widget(widget)
            return True
        else:
            super().add_widget(widget)
            return True

def show_profile():
    """Show the profile dialog"""
    app = MDApp.get_running_app()
    app.profile_dialog = ProfileDialog(
        # ----------------------------Icon-----------------------------
        # MDDialogIcon(
        #     icon="refresh",
        # ),
        # -----------------------Headline text-------------------------
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
                MDButtonText(text="Edit"),
                style="text",
                on_release=lambda x: app.profile_dialog.dismiss(),
            ),
            MDButton(
                MDButtonText(text="Save"),
                style="text",
                on_release=lambda x: app.profile_dialog.dismiss(),
            ),
            spacing="8dp",
        ),
        # -------------------------------------------------------------
        auto_dismiss=False,
    )
    app.profile_dialog.open()