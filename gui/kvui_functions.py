'''
Moving the functions from kvui.py that are useful for the new client here,
so that they can be overridden if needed.
'''
from kivy.properties import StringProperty
from kvui import *

__all__ = ["MW_ServerLabel", 
           "MW_MarkupDropdownTextItem",
           "MW_MarkupDropdown",
           "MW_AutocompleteHintInput",
           "MW_HintLabel",
           "MW_ConnectBarTextInput",
           "MW_CommandPromptTextInput",
           "MW_MessageBoxLabel",
           "MW_MessageBox",
           "MW_MDNavigationItemBase",
           "MW_ButtonsPrompt",
           "MW_CommandButton",
           "MW_HintLayout",
           "MW_HintLog",
           "MW_E",
           "MW_KivyJSONtoTextParser",
           "mw_is_command_input",
           "mw_fade_in_animation",
           "mw_remove_between_brackets",
           "mw_status_icons",
           "mw_status_names",
           "mw_status_colors",
           "mw_status_sort_weights"]

class MW_ServerLabel(ServerLabel):
    pass

class MW_MarkupDropdownTextItem(MarkupDropdownTextItem):
    pass

class MW_MarkupDropdown(MarkupDropdown):
    pass

class MW_AutocompleteHintInput(AutocompleteHintInput):
    pass

class MW_HintLabel(HintLabel):
    pass

class MW_ConnectBarTextInput(ConnectBarTextInput):
    pass

class MW_CommandPromptTextInput(CommandPromptTextInput):
    pass

class MW_MessageBoxLabel(MessageBoxLabel):
    pass

class MW_MessageBox(MessageBox):
    pass

class MW_MDNavigationItemBase(MDNavigationItemBase):
    pass

class MW_ButtonsPrompt(ButtonsPrompt):
    pass

class MW_CommandButton(CommandButton):
    pass

class MW_HintLayout(HintLayout):
    pass

class MW_HintLog(HintLog):
    pass

class MW_E(E):
    pass

class MW_KivyJSONtoTextParser(KivyJSONtoTextParser):
    pass

mw_is_command_input = is_command_input
mw_fade_in_animation = fade_in_animation
mw_remove_between_brackets = remove_between_brackets
mw_status_icons = status_icons
mw_status_names = status_names
mw_status_colors = status_colors
mw_status_sort_weights = status_sort_weights