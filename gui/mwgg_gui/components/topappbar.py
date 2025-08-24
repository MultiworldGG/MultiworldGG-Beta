from __future__ import annotations
"""
TopAppBar class - creates the top app bar that will be added to
the top of the screen.  Additionally creates helper functions to bind
to the mouse and window events to display the appropriate icon
"""
from kivymd.uix.appbar import MDTopAppBar, MDTopAppBarTitle
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock

from time import time, strftime, gmtime

__all__ = ("TopAppBarLayout", "TopAppBar")

Builder.load_string('''
<Timer>:

<TopAppBar>:
    type: "small"
    padding: 0,0,0,0
    spacing: dp(10)
    size_hint_x: 1
    md_bg_color: app.theme_cls.backgroundColor
    MDTopAppBarLeadingButtonContainer:
        MDActionTopAppBarButton:
            icon: "menu"
            id: menu_button
            on_release: app.open_top_appbar_menu(self)
    MDTopAppBarTitle:
        size_hint_x: .5
        id: address_bar_label
        text: root.address_bar
    Timer:
        id: timer
        size_hint_x: .5
        text: "00:00:00"


    MDTopAppBarTrailingButtonContainer:
        MDActionTopAppBarButton:
            icon: "timer-outline"
            on_release: root.toggle_timer()
        MDActionTopAppBarButton:
            icon: "account-circle-outline"
            on_release: root.open_profile()
''')

class Timer(MDTopAppBarTitle):
    # Properly declare properties
    start_time = NumericProperty(0)
    elapsed_time = NumericProperty(0)
    is_running = BooleanProperty(False)
    slot_data = ObjectProperty(None)
    has_been_started = BooleanProperty(False)  # Track if timer has ever been started
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_font_style = "Custom"
        self.font_style = "Monospace"
        self.role = "large"
        self.text = "00:00:00"
        # Bind the elapsed_time property to update the display
        self.bind(elapsed_time=self.on_elapsed_time)
    
    def start(self):
        """Start the timer (initial start or resume from pause)"""
        if not self.is_running:
            if not self.has_been_started:
                # Initial start - set the start time
                self.start_time = time()
                self.has_been_started = True
            else:
                # Resume from pause - adjust start time to account for elapsed time
                self.start_time = time() - self.elapsed_time
            
            self.is_running = True
            Clock.schedule_interval(self.update_timer, 0.1)  # Update every 100ms for smoother display

    def stop(self):
        """Pause the timer (doesn't reset)"""
        if self.is_running:
            self.is_running = False
            Clock.unschedule(self.update_timer)

    def reset(self):
        """Reset the timer to 00:00:00 and set new start time"""
        self.stop()
        self.elapsed_time = 0
        self.text = "00:00:00"
        self.has_been_started = False
        self.start_time = 0

    def update_timer(self, dt):
        """Update the elapsed time and check for goal condition"""
        if self.is_running:
            self.elapsed_time = time() - self.start_time
            
            # Check if game has reached goal state
            if self.slot_data and self.slot_data.get('game_status') == "GOAL":
                self.stop()

    def on_elapsed_time(self, instance, value):
        """Called when elapsed_time property changes"""

        # Format as HH:MM:SS
        self.text = strftime("%H:%M:%S", gmtime(value))
    
    def set_slot_data(self, slot_data):
        """Set the slot_data and check if timer should stop"""
        self.slot_data = slot_data
        if self.slot_data and self.slot_data.get('game_status') == "GOAL":
            self.stop()

class TopAppBar(MDTopAppBar):
    timer: ObjectProperty
    address_bar: StringProperty
    address_bar_label: ObjectProperty

    def __init__(self, **kwargs):
        self.address_bar = "Not Connected"
        super().__init__(**kwargs)
        self.timer = self.ids.timer
        self.address_bar_label = self.ids.address_bar_label
        self.item_data = None

    def toggle_timer(self):
        """Toggle timer on/off (pause/resume)"""
        if self.timer.is_running:
            self.timer.stop()  # Pause
        else:
            self.timer.start()  # Start or resume
    
    def reset(self):
        """Reset the timer (called on long press)"""
        self.timer.reset()
    
    def update_slot_data(self, slot_data):
        """Update slot_data in the timer"""
        self.timer.set_slot_data(slot_data)

    def update_address_bar(self, text: str):
        if self.address_bar_label:
            self.address_bar = text

    def open_profile(self):
        print("open profile")

class TopAppBarLayout(AnchorLayout):
    top_appbar: ObjectProperty
    anchor_x = "left"
    anchor_y = "top"
    size_hint_x = 1
    padding = 0,39,0,0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_appbar = TopAppBar()
        self.top_appbar.id = "top_appbar"
        self.add_widget(self.top_appbar)


