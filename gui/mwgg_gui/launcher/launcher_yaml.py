from __future__ import annotations

from kivymd.uix.behaviors import HoverBehavior, MotionDialogBehavior
"""
YAML DIALOG

OptionsViewer - displays game options similar to the web interface
YamlDialog - dialog for creating YAML files

This module provides functionality to display game options in a GUI format
similar to the web interface, allowing users to view and configure game settings.
"""

__all__ = ('YamlDialog',)

import logging
import os
import yaml
from typing import Dict, Any, Optional, Union
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, ListProperty, BooleanProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.sliverappbar import MDSliverAppbar
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch
from kivymd.uix.slider import MDSlider
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.divider import MDDivider
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDIconButton

import Options
from Utils import local_path, set_game_names

logger = logging.getLogger("Client")

with open(os.path.join(os.path.dirname(__file__), "launcher_yaml.kv"), encoding="utf-8") as kv_file:
    Builder.load_string(kv_file.read())

class OptionLabel(MDLabel):
    pass

class OptionDescription(MDLabel):
    """Label for option descriptions with support for rich text"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.markup = True  # Enable markup for rich text

class OptionDict(MDBoxLayout):
    """Widget for handling OptionDict type options"""
    current_value = ObjectProperty({})
    
    def __init__(self, option_instance=None, **kwargs):
        super().__init__(**kwargs)
        self.option_instance = option_instance
        self.dict_inputs = {}
        self.setup_dict_widget()
    
    def setup_dict_widget(self):
        """Setup the dictionary widget with key-value pairs"""
        try:
            if hasattr(self.option_instance, 'value') and isinstance(self.option_instance.value, dict):
                dict_data = self.option_instance.value
            elif hasattr(self.option_instance, '__iter__') and not isinstance(self.option_instance, str):
                dict_data = dict(self.option_instance)
            else:
                dict_data = {}
            
            self.current_value = dict_data.copy()
            
            # Clear existing widgets
            grid = self.ids.dict_grid
            grid.clear_widgets()
            self.dict_inputs.clear()
            
            # Create label-input pairs for each key-value pair
            for key, value in dict_data.items():
                # Create label
                label = MDLabel(
                    text=str(key),
                )
                grid.add_widget(label)
                
                # Create text input
                text_input = TextInput(
                    text=str(value),
                    multiline=False
                )
                text_input.bind(text=lambda instance, value, key=key: self.on_dict_value_changed(key, value))
                self.dict_inputs[key] = text_input
                grid.add_widget(text_input)
                
        except Exception as e:
            logger.error(f"Error setting up OptionDict: {e}")
            self.current_value = {}
            
    def on_dict_value_changed(self, key, value):
        """Handle value changes from OptionDict text inputs"""
        if isinstance(self.current_value, dict):
            try:
                # Try to convert the value to the appropriate type
                if value.isdigit():
                    self.current_value[key] = int(value)
                elif value.replace('.', '').isdigit():
                    self.current_value[key] = float(value)
                else:
                    self.current_value[key] = value
            except (ValueError, AttributeError):
                self.current_value[key] = value

class ListBasedOption(MDBoxLayout):
    """Widget for handling list-based options like PlandoItems, LocalItems, etc."""
    current_value = ListProperty([])
    
    def __init__(self, option_instance=None, **kwargs):
        super().__init__(**kwargs)
        self.option_instance = option_instance
        self.is_plando = False
        self.is_location_list = False
        self.is_item_list = False
        self.pending_item = None
        self.setup_list_widget()
    
    def setup_list_widget(self):
        """Setup the list-based widget"""
        try:
            # Determine option type
            option_class = getattr(self.option_instance, '__class__', None)
            if option_class:
                self.is_plando = option_class.__name__ == 'PlandoItems'
                self.is_location_list = 'location' in option_class.__name__.lower()
                self.is_item_list = 'item' in option_class.__name__.lower() or option_class.__name__ == 'StartHints'
            
            # Setup search layout
            self.setup_search_layout()
            
            # Get current items
            current_items = self.option_instance.value if self.option_instance.value else []
            self.current_value = list(current_items)
            
            # Populate selected items grid
            self.populate_selected_grid()
            
            # Create dropdown menu
            self.search_dropdown = MDDropdownMenu(
                items=[]
            )
            
        except Exception as e:
            logger.error(f"Error setting up ListBasedOption: {e}")
            self.current_value = []
    
    def setup_search_layout(self):
        """Setup the search layout based on option type"""
        search_layout = self.ids.search_layout
        search_layout.clear_widgets()
        
        if self.is_plando:
            # Dual search for plando items
            self.item_search = MDTextField(
                hint_text="Search items...",
                size_hint_x=0.5,
            )
            self.location_search = MDTextField(
                hint_text="Search locations...",
                size_hint_x=0.5,
            )
            self.item_search.bind(text=self.on_item_search)
            self.location_search.bind(text=self.on_location_search)
            search_layout.add_widget(self.item_search)
            search_layout.add_widget(self.location_search)
        else:
            # Single search
            search_hint = "Search locations..." if self.is_location_list else "Search items..."
            self.single_search = MDTextField(
                hint_text=search_hint,
            )
            self.single_search.bind(text=self.on_single_search)
            search_layout.add_widget(self.single_search)
    
    def populate_selected_grid(self):
        """Populate the selected items grid"""
        selected_grid = self.ids.selected_grid
        selected_grid.clear_widgets()
        
        for item in self.current_value:
            self.add_selected_item_to_grid(item, selected_grid)
    
    def add_selected_item_to_grid(self, item, grid_layout):
        """Add a selected item to the grid layout"""
        try:
            if self.is_plando:
                # Plando item: show item name, location name, remove button
                items_text = ', '.join(item.get('items', [])) if isinstance(item, dict) else str(item)
                locations_text = ', '.join(item.get('locations', [])) if isinstance(item, dict) else ""
                
                # Item name label
                item_label = MDLabel(
                    text=items_text or "No items",
                )
                grid_layout.add_widget(item_label)
                
                # Location name label
                location_label = MDLabel(
                    text=locations_text or "No locations",
                )
                grid_layout.add_widget(location_label)
                
                # Remove button
                remove_btn = MDIconButton(
                    icon="trash-can",
                    on_release=lambda x, item=item: self.remove_item(item)
                )
                grid_layout.add_widget(remove_btn)
            else:
                # Single item: show item name, remove button
                item_text = str(item)
                
                # Item name label
                item_label = MDLabel(
                    text=item_text,
                )
                grid_layout.add_widget(item_label)
                
                # Remove button
                remove_btn = MDIconButton(
                    icon="trash-can",
                    on_release=lambda x, item=item: self.remove_item(item)
                )
                grid_layout.add_widget(remove_btn)
                
        except Exception as e:
            logger.error(f"Error adding item to grid: {e}")
    
    def remove_item(self, item):
        """Remove an item from the list"""
        try:
            if item in self.current_value:
                self.current_value.remove(item)
                self.populate_selected_grid()
        except Exception as e:
            logger.error(f"Error removing item: {e}")
    
    def on_item_search(self, instance, value):
        """Handle item search text changes"""
        if len(value) >= 2:
            self.perform_search(value, 'item')
        else:
            self.search_dropdown.dismiss()
    
    def on_location_search(self, instance, value):
        """Handle location search text changes"""
        if len(value) >= 2:
            self.perform_search(value, 'location')
        else:
            self.search_dropdown.dismiss()
    
    def on_single_search(self, instance, value):
        """Handle single search text changes"""
        if len(value) >= 2:
            search_type = 'location' if self.is_location_list else 'item'
            self.perform_search(value, search_type)
        else:
            self.search_dropdown.dismiss()
    
    def perform_search(self, search_text, search_type):
        """Perform search and show dropdown results"""
        try:
            if search_type == 'item':
                names = self.get_item_names()
                icon = "treasure-chest"
            else:  # location
                names = self.get_location_names()
                icon = "sign-direction"
            
            # Filter names based on search text
            search_lower = search_text.lower()
            matching_names = [name for name in names if search_lower in name.lower()]
            
            # Create dropdown items
            menu_items = []
            for name in matching_names[:10]:  # Limit to 10 results
                menu_items.append({
                    "text": name,
                    "leading_icon": icon,
                    "on_release": lambda x, name=name: self.add_item_from_search(name, search_type)
                })
            
            # Update dropdown
            self.search_dropdown.items = menu_items
            if menu_items:
                # Set caller to the appropriate search field
                if hasattr(self, 'item_search') and search_type == 'item':
                    self.search_dropdown.caller = self.item_search
                elif hasattr(self, 'location_search') and search_type == 'location':
                    self.search_dropdown.caller = self.location_search
                elif hasattr(self, 'single_search'):
                    self.search_dropdown.caller = self.single_search
                
                self.search_dropdown.open()
            else:
                self.search_dropdown.dismiss()
                
        except Exception as e:
            logger.error(f"Error performing search: {e}", exc_info=True, stack_info=True)
    
    def add_item_from_search(self, name, search_type):
        """Add an item from search results"""
        try:
            if self.is_plando:
                # For plando items, we need both item and location
                if search_type == 'item':
                    # Store the selected item and wait for location
                    self.pending_item = name
                    # Clear item search and focus location search
                    self.item_search.text = ""
                    self.location_search.focus = True
                else:  # location
                    # Create plando item with both item and location
                    if hasattr(self, 'pending_item'):
                        plando_item = {
                            'items': [self.pending_item],
                            'locations': [name]
                        }
                        self.add_plando_item(plando_item)
                        delattr(self, 'pending_item')
                    else:
                        # Just location, create with empty items
                        plando_item = {
                            'items': [],
                            'locations': [name]
                        }
                        self.add_plando_item(plando_item)
            else:
                # Single type list
                if name not in self.current_value:
                    self.current_value.append(name)
                    self.add_selected_item_to_grid(name, self.ids.selected_grid)
            
            self.search_dropdown.dismiss()
        except Exception as e:
            logger.error(f"Error adding item from search: {e}", exc_info=True, stack_info=True)
    
    def add_plando_item(self, plando_item):
        """Add a plando item to the list"""
        if plando_item not in self.current_value:
            self.current_value.append(plando_item)
            self.add_selected_item_to_grid(plando_item, self.ids.selected_grid)
    
    def get_item_names(self):
        """Get available item names from AutoWorld"""
        try:
            from gui.mwgg_gui.launcher.launcher import get_current_game
            current_game = get_current_game()
            if not current_game:
                return []
            
            world_module = __import__(f'worlds.{current_game}', fromlist=['World'])
            world_class = getattr(world_module, 'World', None)
            if world_class and hasattr(world_class, 'item_name_to_id'):
                return list(world_class.item_name_to_id.keys())
            return []
        except Exception as e:
            logger.error(f"Error getting item names: {e}", exc_info=True, stack_info=True)
            return []
    
    def get_location_names(self):
        """Get available location names from AutoWorld"""
        try:
            from gui.mwgg_gui.launcher.launcher import get_current_game
            current_game = get_current_game()
            if not current_game:
                return []
            
            world_module = __import__(f'worlds.{current_game}', fromlist=['World'])
            world_class = getattr(world_module, 'World', None)
            if world_class and hasattr(world_class, 'location_name_to_id'):
                return list(world_class.location_name_to_id.keys())
            return []
        except Exception as e:
            logger.error(f"Error getting location names: {e}", exc_info=True, stack_info=True)
            return []

class ChoiceOption(MDBoxLayout):
    """Widget for handling Choice type options"""
    current_value = ObjectProperty(None)
    
    def __init__(self, option_instance=None, **kwargs):
        super().__init__(**kwargs)
        self.option_instance = option_instance
        self.dropdown_menu = None
        self.setup_choice_widget()
    
    def setup_choice_widget(self):
        """Setup the choice widget with dropdown"""
        try:
            option_class = getattr(self.option_instance, '__class__', None)
            if not option_class:
                return
            
            choices = getattr(option_class, 'name_lookup', {})
            if not choices:
                return
            
            # Get current value
            current_value = getattr(self.option_instance, 'value', None)
            if current_value is not None and current_value in choices:
                self.current_value = current_value
                current_display_name = choices[current_value]
            else:
                # Get default value
                default_value = getattr(option_class, 'default', None)
                if default_value is not None and default_value in choices:
                    self.current_value = default_value
                    current_display_name = choices[default_value]
                elif choices:
                    # Use first available choice as fallback
                    self.current_value = list(choices.keys())[0]
                    current_display_name = choices[self.current_value]
                else:
                    self.current_value = None
                    current_display_name = "Select Option"
            
            # Update button text
            button = self.ids.choice_button
            button.clear_widgets()
            button.add_widget(MDButtonText(text=current_display_name))
            
            # Create menu items
            menu_items = []
            for key, name in choices.items():
                if name != "random":  # Skip random option like the web template
                    menu_items.append({
                        "text": name,
                        "on_release": lambda val=key, display=name: self.set_choice_value(val, display),
                    })
            
            # Create dropdown menu
            self.dropdown_menu = MDDropdownMenu(
                caller=button,
                items=menu_items,
            )

        except Exception as e:
            logger.error(f"Error setting up ChoiceOption: {e}", exc_info=True, stack_info=True)
    
    def open_dropdown(self):
        """Open the dropdown menu"""
        if self.dropdown_menu:
            self.dropdown_menu.open()
    
    def set_choice_value(self, value, display_name):
        """Set the choice value when selected from dropdown menu"""
        self.current_value = value
        
        # Update button text to show selected value
        button = self.ids.choice_button
        button.clear_widgets()
        button.add_widget(MDButtonText(text=display_name))
        
        # Close the dropdown menu
        if self.dropdown_menu:
            self.dropdown_menu.dismiss()

class RangeOption(MDBoxLayout):
    """Widget for handling Range type options"""
    current_value = ObjectProperty(0)
    
    def __init__(self, option_instance=None, **kwargs):
        super().__init__(**kwargs)
        self.option_instance = option_instance
        self.setup_range_widget()
    
    def setup_range_widget(self):
        """Setup the range widget with slider"""
        try:
            option_class = getattr(self.option_instance, '__class__', None)
            if not option_class:
                return
            
            range_start = getattr(option_class, 'range_start', 0)
            range_end = getattr(option_class, 'range_end', 100)
            current_value = getattr(self.option_instance, 'value', range_start)
            
            slider = self.ids.range_slider
            slider.min = range_start
            slider.max = range_end
            slider.value = current_value
            self.current_value = current_value
            
        except Exception as e:
            logger.error(f"Error setting up RangeOption: {e}", exc_info=True, stack_info=True)
            self.current_value = 0
    
    def on_value_changed(self, instance, value):
        """Handle value changes from slider"""
        self.current_value = value

class ToggleOption(MDBoxLayout):
    """Widget for handling Toggle type options"""
    current_value = BooleanProperty(False)
    
    def __init__(self, option_instance=None, **kwargs):
        super().__init__(**kwargs)
        self.option_instance = option_instance
        self.setup_toggle_widget()
    
    def setup_toggle_widget(self):
        """Setup the toggle widget with switch"""
        try:
            current_value = bool(self.option_instance) if self.option_instance else False
            switch = self.ids.toggle_switch
            switch.active = current_value
            self.current_value = current_value
            
        except Exception as e:
            logger.error(f"Error setting up ToggleOption: {e}", exc_info=True, stack_info=True)
            self.current_value = False
    
    def on_value_changed(self, instance, value):
        """Handle value changes from switch"""
        self.current_value = value

class FreeTextOption(MDBoxLayout):
    """Widget for handling FreeText type options"""
    current_value = StringProperty("")
    
    def __init__(self, option_instance=None, **kwargs):
        super().__init__(**kwargs)
        self.option_instance = option_instance
        self.setup_text_widget()
    
    def setup_text_widget(self):
        """Setup the text widget with text field"""
        try:
            text_value = str(self.option_instance) if self.option_instance else ""
            text_field = self.ids.text_field
            text_field.text = text_value
            self.current_value = text_value
            
        except Exception as e:
            logger.error(f"Error setting up FreeTextOption: {e}", exc_info=True, stack_info=True)
            self.current_value = ""
            
    def on_value_changed(self, instance, value):
        """Handle value changes from text field"""
        self.current_value = value

class OptionItem(MDCard):
    """Individual option item widget"""
    option_name = StringProperty("")
    option_type = StringProperty("")
    option_description = StringProperty("")
    current_value = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        # Extract option_value before calling super().__init__ to avoid Kivy property binding issues
        self.option_value = kwargs.pop('option_value', None)
        super().__init__(**kwargs)
        self.option_widget = None
        
        # Add option name label
        if self.option_name:
            name_label = OptionLabel(text=self.option_name)
            self.add_widget(name_label)
        
        # Add option description if available
        if self.option_description:
            desc_label = OptionDescription(text=self.option_description)
            self.add_widget(desc_label)
        
        self.setup_option_widget()
    
    def setup_option_widget(self):
        """Setup the appropriate widget based on option type"""
        # Import the base option classes for proper inheritance checking
        from Options import Toggle, Range, Choice, FreeText, TextChoice, NamedRange
        
        # Get the option class from the stored class reference
        option_class = getattr(self.option_value, '__class__', None)
        if not option_class or self.option_value is None:
            # Fallback to text field if we can't determine the class or value is None
            self.option_widget = FreeTextOption(option_instance=self.option_value)
            self.current_value = self.option_widget.current_value
            self.option_widget.bind(current_value=self.on_value_changed)
            self.add_widget(self.option_widget)
            return
        
        # Create a safe option instance for value extraction
        try:
            safe_option_instance = self.option_value
        except Exception as e:
            logger.warning(f"Error accessing option instance: {e}", exc_info=True, stack_info=True)
            # Fallback to text field
            self.option_widget = FreeTextOption(option_instance=None)
            self.current_value = self.option_widget.current_value
            self.option_widget.bind(current_value=self.on_value_changed)
            self.add_widget(self.option_widget)
            return
        
        # Check inheritance hierarchy to determine widget type
        if issubclass(option_class, Toggle):
            # Handle Toggle and DefaultOnToggle
            self.option_widget = ToggleOption(option_instance=safe_option_instance)
            self.current_value = self.option_widget.current_value
            self.option_widget.bind(current_value=self.on_value_changed)
            
        elif issubclass(option_class, (Range, NamedRange)):
            # Handle Range and NamedRange
            self.option_widget = RangeOption(option_instance=safe_option_instance)
            self.current_value = self.option_widget.current_value
            self.option_widget.bind(current_value=self.on_value_changed)
            
        elif issubclass(option_class, Choice):
            # Handle Choice and TextChoice
            self.option_widget = ChoiceOption(option_instance=safe_option_instance)
            self.current_value = self.option_widget.current_value
            self.option_widget.bind(current_value=self.on_value_changed)
            
        elif issubclass(option_class, FreeText):
            # Handle FreeText
            self.option_widget = FreeTextOption(option_instance=safe_option_instance)
            self.current_value = self.option_widget.current_value
            self.option_widget.bind(current_value=self.on_value_changed)
            
        elif issubclass(option_class, Options.OptionDict):
            # Handle OptionDict
            self.option_widget = OptionDict(option_instance=safe_option_instance)
            self.current_value = self.option_widget.current_value
            self.option_widget.bind(current_value=self.on_value_changed)
            
        elif issubclass(option_class, Options.Option) and hasattr(safe_option_instance, 'value') and isinstance(safe_option_instance.value, list):
            # Handle list-based options like PlandoItems, LocalItems, etc.
            self.option_widget = ListBasedOption(option_instance=safe_option_instance)
            self.current_value = self.option_widget.current_value
            self.option_widget.bind(current_value=self.on_value_changed)
            
        else:
            # Default to text field for unknown types
            self.option_widget = FreeTextOption(option_instance=safe_option_instance)
            self.current_value = self.option_widget.current_value
            self.option_widget.bind(current_value=self.on_value_changed)
        
        if self.option_widget:
            self.add_widget(self.option_widget)
    
    def on_value_changed(self, instance, value):
        """Handle value changes from widgets"""
        self.current_value = value
    
    def get_current_value(self):
        """Get the current value of this option"""
        return self.current_value

class OptionGroupCard(MDCard):
    """Card containing a group of options"""
    group_name = StringProperty("")
    options_data = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.option_items = {}  # Store references to option items
        self.setup_group()
    
    def setup_group(self):
        """Setup the option group with its options"""
        # Add group title
        title = OptionLabel(text=self.group_name)
        self.add_widget(title)
        
        # Add divider
        divider = MDDivider()
        self.add_widget(divider)
        
        # Add options
        for option_name, option_data in self.options_data:
            option_item = OptionItem(
                option_name=option_name,
                option_type=option_data.get('type', 'Unknown'),
                option_value=option_data.get('value'),
                option_description=option_data.get('description', '')
            )
            self.option_items[option_name] = option_item
            self.add_widget(option_item)
    
    def get_option_values(self):
        """Get all option values from this group"""
        values = {}
        for option_name, option_item in self.option_items.items():
            values[option_name] = option_item.get_current_value()
        return values

class OptionsScroll(MDScrollView):
    """Custom scroll view for options with proper configuration"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure proper scrolling behavior
        self.do_scroll_x = False
        self.do_scroll_y = True
        self.bar_width = dp(10)
        self.bar_color = [0.5, 0.5, 0.5, 0.5]
        # Initialize scroll effect properly
        self.effect_y.bounds = (0, None)
        self.effect_y.value = 0

class OptionsLayout(MDBoxLayout):
    """Main options viewer widget"""
    module_name = StringProperty("")
    game_name = StringProperty("")
    option_groups = ListProperty([])
    dismiss = BooleanProperty(False)
    
    def __init__(self, selected_game: tuple, **kwargs):
        self.module_name = selected_game[0]
        self.game_name = selected_game[1]
        self.dismiss = False
        super().__init__(**kwargs)
        self.group_cards = {}  # Store references to group cards
        self.setup_options()
    
    def setup_options(self):
        """Setup the options display"""
        if not self.module_name:
            return
            
        try:
            # Add player name input at the top
            self.add_player_name_input()
            
            # Get option groups data
            groups_data = get_option_groups_data(self.game_name)
            
            for group_name, options in groups_data.items():
                if options:  # Only add groups with options
                    group_card = OptionGroupCard(
                        group_name=group_name,
                        options_data=list(options.items())
                    )
                    self.group_cards[group_name] = group_card
                    self.add_widget(group_card)
            
            # Add save button at the bottom
            self.add_cancel_button()
            self.add_save_button()
                    
        except Exception as e:
            logger.error(f"Failed to setup options for {self.game_name}: {e}", exc_info=True, stack_info=True)
    
    def add_player_name_input(self):
        """Add a player name input field"""
        player_name_label = OptionLabel(text="Player Name:")
        self.add_widget(player_name_label)
        
        self.player_name_field = MDTextField(
            text="Player",
            hint_text="Enter player name",
            size_hint=(None, None),
            size=(dp(300), dp(50)),
            pos_hint={"center_x": 0.5}
        )
        self.add_widget(self.player_name_field)
    
    def add_cancel_button(self):
        """Add a cancel button to return to the launcher screen"""
        cancel_button = MDButton(
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={"center_x": 0.5}
        )
        cancel_button.add_widget(MDButtonText(text="Cancel"))
        cancel_button.bind(on_release=self.cancel)
        self.add_widget(cancel_button)
    
    def add_save_button(self):
        """Add a save button to create the YAML file"""
        save_button = MDButton(
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={"center_x": 0.5}
        )
        save_button.add_widget(MDButtonText(text="Save YAML"))
        save_button.bind(on_release=self.save_yaml)
        self.add_widget(save_button)
    
    def _convert_to_serializable(self, value):
        """Convert a value to a YAML-serializable format"""
        if value is None:
            return None
        
        # Check if it's a Kivy property object
        if hasattr(value, '__class__') and 'Property' in str(value.__class__):
            # It's a Kivy property, get its actual value
            if hasattr(value, 'value'):
                return self._convert_to_serializable(value.value)
            else:
                # Fallback: convert to string representation
                return str(value)
        
        # Handle different Python types
        if isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, (list, tuple)):
            return [self._convert_to_serializable(item) for item in value]
        elif isinstance(value, dict):
            return {str(k): self._convert_to_serializable(v) for k, v in value.items()}
        else:
            # For any other type, convert to string
            return str(value)
    
    def save_yaml(self, instance):
        """Save the current options as a YAML file"""
        try:
            # Collect all option values and convert to serializable format
            all_options = {}
            for group_name, group_card in self.group_cards.items():
                group_values = group_card.get_option_values()
                # Convert Kivy properties to plain Python values
                serializable_values = {}
                for key, value in group_values.items():
                    serializable_values[key] = self._convert_to_serializable(value)
                all_options.update(serializable_values)
            
            # Create YAML structure
            player_name = self.player_name_field.text.strip() or "Player"
            yaml_data = {
                "name": player_name,
                "game": self.game_name,
                "description": f"Generated by MultiworldGG for {player_name}",
                self.game_name: all_options
            }
            
            # Save to Players directory
            players_dir = local_path("Players")
            os.makedirs(players_dir, exist_ok=True)
            
            filename = f"{player_name}_{self.module_name}.yaml"
            filepath = os.path.join(players_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)
            
            logger.info(f"YAML file saved: {filepath}")
            self.dismiss = True
            # Show success message TODO: FIX
            self.app.message_box("Success", f"YAML file saved to:\n{filepath}").open()
            
        except Exception as e:
            logger.error(f"Failed to save YAML: {e}", exc_info=True, stack_info=True)
            self.gui.message_box("Save Error", f"Failed to save YAML: {str(e)}", is_error=True).open()
    
    def cancel(self, instance):
        """Cancel the YAML creation and remove the layout"""
        self.dismiss = True

class OptionsView(MDRelativeLayout, ThemableBehavior, HoverBehavior):
    """Main Layout for displaying game options"""
    module_name = StringProperty("")
    options_layout: OptionsLayout
    app: MDApp
    dismiss = BooleanProperty(False)
    
    def __init__(self, selected_game: tuple, **kwargs):
        self.module_name = selected_game[0]
        self.game_name = selected_game[1]
        self.dismiss = False
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        # Create options viewer
        self.options_scroll = OptionsScroll(
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.options_layout = OptionsLayout(selected_game=selected_game)
        self.options_layout.bind(dismiss=self.on_dismiss)
        self.options_scroll.add_widget(self.options_layout)
        self.add_widget(self.options_scroll)
        
        # Add back button
        back_button = MDButton(
            pos_hint={"top": 1, "right": 1},
            size_hint=(None, None),
            size=(dp(100), dp(40))
        )
        back_button.add_widget(MDButtonText(text="Back"))
        back_button.add_widget(MDButtonIcon(icon="arrow-left"))
        back_button.bind(on_release=self.on_dismiss)
        self.add_widget(back_button)
    
    def on_dismiss(self, *args):
        """Return to previous screen"""
        self.dismiss = True
    
    def set_world(self, world_name: str):
        """Set the world to display options for"""
        self.world_name = world_name
        if self.options_viewer:
            self.options_viewer.world_name = world_name
            self.options_viewer.clear_widgets()
            self.options_viewer.setup_options()

class YamlDialog(MDFloatLayout, HoverBehavior):
    """Dialog for creating YAML files"""
    selected_game: tuple
    app: MDApp
    dismiss = BooleanProperty(False)
    on_dismiss = ObjectProperty(None)
    
    def __init__(self, selected_game: tuple, **kwargs):
        self.selected_game = selected_game
        self.dismiss = False
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.options_view = OptionsView(selected_game=selected_game)
        self.add_widget(self.options_view)
        self.options_view.bind(dismiss=self._on_dismiss)
    
    def _on_dismiss(self, *args):
        self.dismiss = True
        if self.on_dismiss:
            self.on_dismiss()

    def on_touch_down(self, touch):
        if not self.options_view.collide_point(*touch.pos):
            return True
        return super().on_touch_down(touch)

def get_option_groups_data(game_name: str, is_complex: bool = False) -> Dict[str, Dict[str, Any]]:
    """
    Get option groups data for a world, similar to the web interface
    
    Args:
        world_name: Name of the world/game
        is_complex: Whether to show complex UI options
        
    Returns:
        Dictionary of option groups with their options
    """
    try:
        # Load the specific world first
        games_to_load = [game_name]
        set_game_names(games_to_load)
        
        # Import AutoWorldRegister after setting game names
        from worlds import AutoWorldRegister
        
        if game_name not in AutoWorldRegister.world_types:
            logger.warning(f"World {game_name} not found in AutoWorldRegister")
            return {}
        
        world = AutoWorldRegister.world_types[game_name]
        
        # Set visibility level
        visibility_flag = Options.Visibility.complex_ui if is_complex else Options.Visibility.simple_ui
        
        # Get option groups using the same logic as the web interface
        option_groups = Options.get_option_groups(world, visibility_level=visibility_flag)
        
        # Convert to a more GUI-friendly format
        groups_data = {}
        for group_name, options in option_groups.items():
            if options:  # Only include groups with options
                groups_data[group_name] = {}
                for option_name, option_class in options.items():
                    try:
                        # Get default value
                        default_value = getattr(option_class, 'default', None)
                        
                        # Get option type
                        option_type = option_class.__name__
                        
                        # Get description if available
                        description = getattr(option_class, '__doc__', '')
                        if description:
                            # Clean up the description - take first line and strip whitespace
                            description = description.strip().split('\n')[0].strip()
                            # Convert basic reStructuredText to simple markup
                            # Convert **text** to [b]text[/b] for Kivy markup
                            description = description.replace('**', '[b]').replace('**', '[/b]')
                            # Convert *text* to [i]text[/i] for Kivy markup  
                            description = description.replace('*', '[i]').replace('*', '[/i]')
                        
                        # Create an instance of the option class with default value
                        try:
                            # Always try to get a valid default value first
                            class_default = getattr(option_class, 'default', None)
                            
                            if default_value is not None:
                                option_instance = option_class.from_any(default_value)
                            elif class_default is not None:
                                option_instance = option_class.from_any(class_default)
                            else:
                                # For Choice-based options, try to use the first available option
                                if hasattr(option_class, 'options') and option_class.options:
                                    first_option_value = list(option_class.options.values())[0]
                                    option_instance = option_class.from_any(first_option_value)
                                else:
                                    # Fallback: create with 0 for numeric options, empty string for text
                                    if hasattr(option_class, 'range_start'):
                                        option_instance = option_class.from_any(0)
                                    else:
                                        option_instance = option_class.from_any("")
                        except Exception as e:
                            logger.warning(f"Failed to create option instance for {option_name}: {e}")
                            # Create a minimal safe instance to avoid None comparisons
                            try:
                                if hasattr(option_class, 'default') and option_class.default is not None:
                                    option_instance = option_class.from_any(option_class.default)
                                elif hasattr(option_class, 'options') and option_class.options:
                                    first_option_value = list(option_class.options.values())[0]
                                    option_instance = option_class.from_any(first_option_value)
                                else:
                                    option_instance = None
                            except:
                                option_instance = None
                        
                        groups_data[group_name][option_name] = {
                            'type': option_type,
                            'value': option_instance,  # Store the instance, not just the default value
                            'default_value': default_value,
                            'class_default': class_default,
                            'description': description,
                            'class': option_class
                        }
                    except Exception as e:
                        logger.warning(f"Failed to process option {option_name}: {e}")
                        continue
        
        return groups_data
        
    except Exception as e:
        logger.error(f"Failed to get option groups for {game_name}: {e}")
        return {}