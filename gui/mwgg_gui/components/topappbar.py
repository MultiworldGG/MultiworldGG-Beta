from __future__ import annotations
"""
TopAppBar class - creates the top app bar that will be added to
the top of the screen.  Additionally creates helper functions to bind
to the mouse and window events to display the appropriate icon
"""
from kivymd.app import App
from kivymd.uix.appbar import MDTopAppBar, MDTopAppBarTitle
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from kivymd.uix.tooltip import MDTooltip
from time import time, strftime, gmtime
from Utils import async_start

__all__ = ("TopAppBarLayout", "TopAppBar")

Builder.load_string('''
<Timer>:

<ServerLabel>:

<ServerTooltip>:
    MDTooltipRich:
        id: server_tooltip_label
        MDTooltipRichSubhead:
            text: root.server_tooltip
        MDTooltipRichSupportingText:
            text: root.game_tooltip
        MDTooltipRichActionButton:
            on_press: root.next()
            MDButtonText:
                text: "More"

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
    ServerLabel:
        size_hint_x: .7
        id: address_bar_label
        text: "Not Connected"
    Timer:
        id: timer
        size_hint_x: .3
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
    slot_info = ObjectProperty(None)
    has_been_started = BooleanProperty(False)  # Track if timer has ever been started
    ctx = ObjectProperty(None)
    _update_event = ObjectProperty(None)  # Store the scheduled event

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_font_style = "Custom"
        self.font_style = "Monospace"
        self.role = "large"
        self.text = "00:00:00"
        # Bind the elapsed_time property to update the display
        self.bind(elapsed_time=self.on_elapsed_time)
        
    def on_ui_built(self):
        self.ctx = App.get_running_app().ctx
        self.slot_info = self.ctx.slot_info
        # Only schedule if not already scheduled
        if self._update_event is None:
            self._update_event = Clock.schedule_interval(self._update_timer_wrapper, 0.1)
    
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

    def _update_timer_wrapper(self, dt):
        """Non-blocking wrapper for timer updates"""
        try:
            self.update_timer()
        except Exception as e:
            print(f"Timer update error: {e}")
    
    def update_timer(self):
        """Update the elapsed time and check for goal condition"""
        # Check for countdown timer from server first
        if hasattr(self.ctx, 'countdown_timer') and self.ctx.countdown_timer:
            if self.ctx.countdown_timer > 0 and not self.has_been_started:
                # Server provided a countdown - start timer as negative
                self.elapsed_time = -self.ctx.countdown_timer  # Negative countdown
                self.start_time = time() + self.ctx.countdown_timer  # Adjusted start time
                self.is_running = True
                self.has_been_started = True
                return
        
        # Normal timer operation
        if self.is_running:
            self.elapsed_time = time() - self.start_time
            # Check for goal completion
            if self.slot_info and self.slot_info.get('game_status') == "GOAL":
                self.stop()
                return


    def on_elapsed_time(self, instance, value):
        """Called when elapsed_time property changes"""
        # Handle negative time (countdown) and positive time
        if value < 0:
            # Negative countdown - show with minus sign
            abs_value = abs(value)
            self.text = "-" + strftime("%H:%M:%S", gmtime(abs_value))
        else:
            # Positive time - normal display
            self.text = strftime("%H:%M:%S", gmtime(value))
    
    def on_parent(self, instance, parent):
        """Clean up scheduled events when widget is removed"""
        if parent is None and self._update_event:
            Clock.unschedule(self._update_event)
            self._update_event = None
 

class ServerTooltip(MDTooltip):
    """
    Tooltip for the server and information
    """
    server_tooltip: StringProperty
    game_tooltip: StringProperty
    tooltip_pages: ListProperty
    current_tooltip_page: NumericProperty

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tooltip_display_delay = 4 

    def next(self):
        if len(self.tooltip_pages) > 1:
            self.current_tooltip_page = (self.current_tooltip_page + 1) % len(self.tooltip_pages)
            self.game_tooltip = self.tooltip_pages[self.current_tooltip_page]
        else:
            self.game_tooltip = self.tooltip_pages[0] if self.tooltip_pages else "No information available"

class ServerLabel(ServerTooltip, MDTopAppBarTitle):
    """
    Label for the server and information
    """
    ctx: ObjectProperty
    server_name: StringProperty
    game_info: StringProperty
    game_pages: ListProperty
    current_page: NumericProperty
    _connected: BooleanProperty(False)

    def __init__(self, **kwargs):
        self._connected = False
        super().__init__(**kwargs)
        self.game_pages = self.tooltip_pages = ["No current server connection. \nPlease connect to a server."]
        self.game_info = self.game_tooltip = self.game_pages[0]
        self.server_name = self.server_tooltip = "Not Connected"
        self.current_page = self.current_tooltip_page = 0
        self.theme_font_style = "Custom"
        self.font_style = "Monospace"
        self.role = "large"

    def on_ui_built(self):
        self.ctx = App.get_running_app().ctx
        self.slot_info = self.ctx.slot_info
        self._connected = True
        # Update server info immediately on connection
        self.update_server_info()

    def on_open(self):
        # Don't open tooltip until ui_built() has been called
        if not self._connected:
            return
        if self.ctx.slot is None:
            return
        # We have a valid connection, proceed with tooltip setup
        # Rebuild tooltip data to ensure it's current
        self._build_tooltip_data(self.ctx)
        super().on_open()

    def update_server_info(self, ctx=None):
        """Update server info display - called directly from on_connect"""
        if not ctx:
            ctx = self.ctx
        if not ctx:
            return
        
        # Rebuild complete tooltip data
        self._build_tooltip_data(ctx)
        
        # Update main label text
        if ctx.slot is not None:
            name = ctx.player_names[ctx.slot]
            # if ctx.alias:
            #     name = ctx.alias
            self.text = f"{ctx.server_address}, Hello {name}"
        else:
            self.text = f"{ctx.server_address}"
    
    def _build_tooltip_data(self, ctx):
        """Build complete tooltip data from context"""
        self.game_pages = self.tooltip_pages = []  # Reset pages
        
        if ctx.slot is None:
            self.server_name = self.server_tooltip = f"{ctx.server_address}"
            self.game_pages = self.tooltip_pages = [f"You are not authenticated yet."]
        else:
            name = ctx.player_names[ctx.slot]
            # if ctx.alias:
            #     name = ctx.alias
            self.server_name = self.server_tooltip = f"{ctx.server_address}, Hello {name}"
            
            if ctx.total_locations:
                self.game_pages.append(
                    f"""You are Slot Number {ctx.slot} named {name}.
You have received {len(ctx.items_received)} items.
You can list them in order with /received.
You have checked {len(ctx.checked_locations)} out of {ctx.total_locations} locations.
You can get more info on missing checks with /missing.
""")
            if ctx.permissions:
                txt = "Permissions:\n"
                txt += "".join([f'{permission_name}: {permission_data}\n' for permission_name, permission_data in ctx.permissions.items()])
                self.game_pages.append(txt)
            if ctx.hint_cost is not None and ctx.total_locations:
                min_cost = int(ctx.server_version >= (0, 3, 9))
                self.game_pages.append(f"""A new !hint <itemname> or !hint_location <locationname> costs {ctx.hint_cost}% of checks made.
For you this means every {max(min_cost, int(ctx.hint_cost * 0.01 * ctx.total_locations))} location checks.
You currently have {ctx.hint_points} points.""")
        
        # Sync both sets of properties
        self.tooltip_pages = self.game_pages.copy()
        self.current_page = self.current_tooltip_page = 0
        self.game_info = self.game_tooltip = self.game_pages[0] if self.game_pages else "No information available"
    
    def on_disconnect(self):
        """Called when disconnected from server"""
        self._connected = False
        self.server_name = self.server_tooltip = "Not Connected"
        self.text = "Not Connected"  # Update main label text
        self.game_pages = self.tooltip_pages = [f"No current server connection. \nPlease connect to a server."]
        self.current_page = self.current_tooltip_page = 0
        self.game_info = self.game_tooltip = self.game_pages[self.current_page]

    def next(self):
        if len(self.game_pages) > 1:
            self.current_page = (self.current_page + 1) % len(self.game_pages)
            self.game_info = self.game_pages[self.current_page]
            # Also update tooltip properties
            self.current_tooltip_page = self.current_page
            self.game_tooltip = self.game_info
        else:
            self.game_info = self.game_pages[0] if self.game_pages else "No information available"
            self.game_tooltip = self.game_info
    
    def on_parent(self, instance, parent):
        """Clean up when widget is removed"""
        if parent is None:
            self._connected = False

    # def previous(self):
    #     if len(self.game_pages) > 1:
    #         self.current_page = (self.current_page - 1) % len(self.game_pages)
    #         self.game_info = self.game_pages[self.current_page]
    #     else:
    #         self.current_page = 0
    #         self.game_info = self.game_pages[0]


class TopAppBar(MDTopAppBar):
    timer: ObjectProperty
    address_bar_label: ObjectProperty

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer = self.ids.timer
        self.address_bar_label = self.ids.address_bar_label

    def toggle_timer(self):
        """Toggle timer on/off (pause/resume)"""
        if self.timer.is_running:
            self.timer.stop()  # Pause
        else:
            self.timer.start()  # Start or resume
    
    def reset(self):
        """Reset the timer (called on long press)"""
        self.timer.reset()

    def ui_built(self):
        self.timer.on_ui_built()
        self.address_bar_label.on_ui_built()
    
    def update_server_info(self, ctx):
        """Update server info from on_connect - called from Gui.py"""
        self.address_bar_label.update_server_info(ctx)
    
    def on_disconnect(self):
        """Handle disconnect - called from Gui.py"""
        self.address_bar_label.on_disconnect()

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


