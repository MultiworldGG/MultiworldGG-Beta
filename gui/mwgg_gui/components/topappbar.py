from __future__ import annotations
"""
TopAppBar class - creates the top app bar that will be added to
the top of the screen.  Additionally creates helper functions to bind
to the mouse and window events to display the appropriate icon
"""
from kivymd.app import MDApp
from kivymd.uix.appbar import MDTopAppBar, MDTopAppBarTitle
from kivymd.uix.tooltip import (
    MDTooltip,
    MDTooltipRich,
    MDTooltipRichSubhead,
    MDTooltipRichSupportingText,
    MDTooltipRichActionButton,
)
from kivymd.uix.button import MDButtonText, MDButton
from kivymd.uix.behaviors import HoverBehavior
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import (ObjectProperty, 
                             StringProperty, 
                             ColorProperty, 
                             NumericProperty, 
                             BooleanProperty,
                             ListProperty)
from .progress_overlay import ProgressOverlay
from .profile import show_profile
from kivy.clock import Clock
from time import time, strftime, gmtime, localtime
from kivy.metrics import dp
import logging
import re
import asyncio

logger = logging.getLogger("MultiWorld")

__all__ = ("TopAppBarLayout", "TopAppBar")

Builder.load_string('''
<MDTooltipRichSubhead>:
    markup: True
<MDTooltipRichSupportingText>:
    markup: True

<Timer>:

<ServerLabel>:

<ServerTooltip>:

<TopAppBarLayout>:

<TopAppBar>:
    MDTopAppBarLeadingButtonContainer:
        MDActionTopAppBarButton:
            icon: "menu"
            id: menu_button
            on_release: app.open_top_appbar_menu(self)
    ServerLabel:
        size_hint_x: .7
        id: server_info_label
        text: "Not Connected"
    ClockLabel:
        id: clock_label
        size_hint_x: .3
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

class ClockLabel(MDTopAppBarTitle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ctx = MDApp.get_running_app().ctx
        self.theme_font_style = "Custom"
        self.font_style = "Monospace"
        self.role = "large"
        self.text = strftime("%H:%M", localtime())
        asyncio.create_task(self.update_clock(), name="Clock")

    async def update_clock(self):
        while not self.ctx.exit_event.is_set():
            self.text = strftime("%H:%M", localtime())
            await asyncio.sleep(60)


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
        self.ctx = MDApp.get_running_app().ctx
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
            logger.exception(e)
    
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
 
class ServerRichTooltip(MDTooltipRich, HoverBehavior):
    """Rich tooltip with hover behavior for ServerLabel"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_label = None  # Will be set by parent
        self.auto_dismiss = False
    
    def on_leave(self, *args):
        """Override to prevent early dismissal while allowing normal KivyMD behavior"""
        # Add a small delay before dismissing to prevent accidental early dismissal
        # This gives users time to move mouse back if they accidentally moved off
        Clock.schedule_once(self._delayed_leave, 1)
    
    def _delayed_leave(self, dt):
        """Delayed leave that calls the parent's on_leave for proper dismissal"""
        # Check if mouse is still outside tooltip bounds
        from kivy.core.window import Window
        mouse_pos = Window.mouse_pos
        
        if not self.collide_point(*mouse_pos):
            # Clean up tooltip reference before dismissing
            if self.server_label:
                self.server_label.tooltip = None
            super().on_leave()

class ServerLabel(MDTooltip, MDTopAppBarTitle):
    """
    Label for the server and information
    """
    ctx: ObjectProperty
    _server_name: StringProperty
    _game_info: StringProperty
    game_pages: ListProperty
    current_page: NumericProperty
    _connected: BooleanProperty(False)

    def __init__(self, **kwargs):
        self._connected = False
        self._server_name = "Not Connected"
        self._game_info = "No current server connection. \nPlease connect to a server."
        super().__init__(**kwargs)
        self.game_pages = ["No current server connection. \nPlease connect to a server."]
        self.game_info = self.game_pages[0]
        self.server_name = "Not Connected"
        self.current_page = 0
        self.theme_font_style = "Custom"
        self.font_style = "Monospace"
        self.role = "large"
        self.tooltip = None  # Single tooltip instance

        self.tooltip_display_delay = 4

        
        # Initialize tooltip content
        self._update_tooltip_content()

    def _update_tooltip_content(self):
        """Update the tooltip widgets based on current state"""
        self.shift_left = dp(220) if len(self.game_pages) == 1 else dp(100)
        self.shift_y = dp(1) if len(self.game_pages) == 1 else dp(-80)
        # Clean up any existing tooltips from window first
        self._cleanup_old_tooltips()
        
        # If tooltip already exists and is displayed, update its content
        if hasattr(self, 'tooltip') and self.tooltip is not None:
            # Clear existing children
            self.tooltip.clear_widgets()
            
            # Add updated content
            self.tooltip.add_widget(MDTooltipRichSubhead(text=self.server_name))
            self.tooltip.add_widget(MDTooltipRichSupportingText(text=self.game_info))
            
            # Add "More" button if multiple pages exist
            if hasattr(self, 'game_pages') and len(self.game_pages) > 1:
                self.tooltip.add_widget(
                    MDTooltipRichActionButton(
                        MDButtonText(text="More"),
                        on_release=lambda x: self.next_page()
                    )
                )
        else:
            # Build base tooltip components
            tooltip_widgets = [
                MDTooltipRichSubhead(text=self.server_name),
                MDTooltipRichSupportingText(text=self.game_info),
            ]
            
            # Add "More" button if multiple pages exist
            if hasattr(self, 'game_pages') and len(self.game_pages) > 1:
                tooltip_widgets.append(
                    MDTooltipRichActionButton(
                        MDButtonText(text="More"),
                        on_release=lambda x: self.next_page()
                    )
                )
            
            # Create the tooltip with all components
            self.tooltip = ServerRichTooltip(*tooltip_widgets)
            self.tooltip.server_label = self  # Back-reference for communication
            self.widgets = [self.tooltip]
    
    def _cleanup_old_tooltips(self):
        """Remove any old ServerRichTooltip instances from the window, except the current one"""
        from kivy.core.window import Window
        
        # Find and remove any ServerRichTooltip instances that aren't our current tooltip
        tooltips_to_remove = []
        for child in Window.children[:]:  # Copy list to avoid modification during iteration
            if isinstance(child, ServerRichTooltip) and child != self.tooltip:
                tooltips_to_remove.append(child)
        
        for old_tooltip in tooltips_to_remove:
            try:
                Window.remove_widget(old_tooltip)
            except Exception as e:
                pass

    @property
    def server_name(self):
        return self._server_name

    @server_name.setter
    def server_name(self, value):
        if self._server_name != value:
            self._server_name = value
            self._update_tooltip_content()  # Update tooltip when server name changes

    @property
    def game_info(self):
        return self._game_info

    @game_info.setter
    def game_info(self, value):
        if self._game_info != value:
            self._game_info = value
            self._update_tooltip_content()  # Update tooltip when game info changes

    def on_ui_built(self):
        self.ctx = MDApp.get_running_app().ctx
        self.slot_info = self.ctx.slot_info
        self._connected = True
        # Update server info immediately on connection
        self.update_server_info()

    def on_open(self, *args):
        """Called when tooltip opens - content should already be current"""
        pass

    def update_server_info(self, ctx=None):
        """Update server info display - called directly from on_connect"""
        if not ctx:
            ctx = self.ctx
        if not ctx:
            return
        
        # Rebuild complete tooltip data
        self._build_tooltip_data(ctx)
        server_address = re.sub(r"^ws?://", "", ctx.server_address)
        # Update main label text
        if ctx.slot is not None:
            name = ctx.player_names[ctx.slot]
            if hasattr(ctx.slot_info[ctx.slot], 'alias') and ctx.slot_info[ctx.slot].alias:
                name = ctx.slot_info[ctx.slot].alias
            self.text = f"{server_address} hosting {name} and friends"
        else:
            self.text = f"{server_address}"
        
    
    def _build_tooltip_data(self, ctx):
        """Build complete tooltip data from context"""
        from NetUtils import TEXT_COLORS
        self.game_pages = []  # Reset pages
        server_address = re.sub(r"^ws?://", "", ctx.server_address)
        if ctx.slot is None:
            self.server_name = f"{server_address}"
            self.game_pages = [f"You are not authenticated yet."]
        else:
            name = ctx.player_names[ctx.slot]
            if hasattr(ctx.slot_info[ctx.slot], 'alias') and ctx.slot_info[ctx.slot].alias:
                name = ctx.slot_info[ctx.slot].alias
            self.server_name = f"{name}@{server_address}"
            
            if ctx.total_locations:
                self.game_pages.append(
                    f"""You are Slot Number {ctx.slot} named [color={TEXT_COLORS['player1_color']}]{name}[/color].
You have received [color={TEXT_COLORS['progression_item_color']}]{len(ctx.items_received)}[/color] items.
You can list them in order with [b][color={TEXT_COLORS['command_echo_color']}]/received[/color][/b].
You have checked [color={TEXT_COLORS['location_color']}]{len(ctx.checked_locations)}[/color] 
    out of [color={TEXT_COLORS['location_color']}]{ctx.total_locations}[/color] locations.
You can get more info on missing checks with [b][color={TEXT_COLORS['command_echo_color']}]/missing[/color][/b].
""")
            if ctx.permissions:
                txt = "Permissions:\n"
                txt += "".join([f'{permission_name}: {permission_data}\n' for permission_name, permission_data in ctx.permissions.items()])
                self.game_pages.append(txt)
            if ctx.hint_cost is not None and ctx.total_locations:
                min_cost = int(ctx.server_version >= (0, 3, 9))
                self.game_pages.append(f"""New hints cost [color={TEXT_COLORS['command_echo_color']}]{ctx.hint_cost}%[/color] of checks made.
Commands are:
[b][color={TEXT_COLORS['command_echo_color']}]!hint[/color] [color={TEXT_COLORS['progression_item_color']}]<itemname>[/color][/b]
[b][color={TEXT_COLORS['command_echo_color']}]!hint_location[/color] [color={TEXT_COLORS['location_color']}]<locationname>[/color][/b]
For you this means every [color={TEXT_COLORS['command_echo_color']}]{max(min_cost, int(ctx.hint_cost * 0.01 * ctx.total_locations))}[/color] location checks.
You currently have [color={TEXT_COLORS['command_echo_color']}]{ctx.hint_points}[/color] points.""")
        
        self.game_info = self.game_pages[0] if self.game_pages else "No information available"
        # Tooltip will be updated automatically via the game_info setter
    
    def on_disconnect(self):
        """Called when disconnected from server"""
        self._connected = False
        self.text = "Not Connected"  # Update main label text
        self.game_pages = [f"No current server connection. \nPlease connect to a server."]
        self.current_page = 0
        self.game_info = self.game_pages[self.current_page]
        self.server_name = self.text

    def next_page(self):
        """Navigate to next page and refresh tooltip"""
        if hasattr(self, 'game_pages') and len(self.game_pages) > 1:
            self.current_page = (self.current_page + 1) % len(self.game_pages)
            self.game_info = self.game_pages[self.current_page]  # This will trigger _update_tooltip_content via setter
        else:
            self.game_info = self.game_pages[0] if hasattr(self, 'game_pages') and self.game_pages else "No information available"
    
    def on_parent(self, instance, parent):
        """Clean up when widget is removed"""
        if parent is None:
            self._connected = False

class TopAppBar(MDTopAppBar):
    """
    Custom top app bar with integrated progress tracking.
    
    Extends MDTopAppBar to include progress tracking functionality that
    updates based on location completion in the connected game session.
    The app bar is made transparent to allow an underlying progress overlay
    to show completion status.
    
    Properties:
        timer: Reference to the timer widget
        server_info_label: Reference to the server information label
        p_width: Current progress width in pixels for the progress bar
    """
    
    timer: ObjectProperty
    server_info_label: ObjectProperty
    p_width: NumericProperty = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.timer = self.ids.timer
        self.server_info_label = self.ids.server_info_label
        self.theme_bg_color = "Custom"
        self.md_bg_color = self.theme_cls.transparentColor
        self.theme_shadow_color = "Custom"
        self.shadow_color = self.theme_cls.transparentColor
        asyncio.create_task(self.update_progress_width(), name="ProgressBar")

    async def update_progress_width(self):
        """
        Continuously update progress bar width based on location completion.
        
        Monitors the connected game session and updates the progress bar width
        to reflect the percentage of locations that have been checked. Updates
        every 30 seconds while the app is running.
        """
        while not self.app.ctx.exit_event.is_set():
            if self.app.ctx and hasattr(self.app.ctx, 'total_locations') and self.app.ctx.total_locations:
                locs = len(self.app.ctx.checked_locations)
                total = self.app.ctx.total_locations
                new_width = self.width * (locs/total) if total > 0 else 0
                if new_width != self.p_width:
                    self.p_width = new_width
            else:
                self.p_width = 0
            await asyncio.sleep(30)

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
        self.server_info_label.on_ui_built()
    
    def update_server_info(self, ctx):
        """Update server info from on_connect - called from Gui.py"""
        self.server_info_label.update_server_info(ctx)
    
    def on_disconnect(self):
        """Handle disconnect - called from Gui.py"""
        self.server_info_label.on_disconnect()

    def open_profile(self):
        """Open user profile interface (placeholder implementation)."""
        show_profile()

class TopAppBarLayout(AnchorLayout):
    """
    Layout container for the top app bar with progress overlay.
    
    Manages the layering and positioning of the progress overlay and
    top app bar components. The progress overlay is positioned behind
    the transparent app bar to provide visual progress feedback.
    
    Properties:
        top_appbar: The main app bar widget
        progress_overlay: The progress tracking overlay widget
    """
    
    top_appbar: ObjectProperty
    progress_overlay: ObjectProperty
    anchor_x = "left"
    anchor_y = "top"
    size_hint_x = 1
    padding = 0,39,0,0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Add progress overlay FIRST (provides both background and progress)
        self.progress_overlay = ProgressOverlay()
        self.progress_overlay.size_hint = (None, None)
        self.add_widget(self.progress_overlay)
        
        # Add the app bar on top of the progress overlay
        self.top_appbar = TopAppBar()
        self.top_appbar.id = "top_appbar"
        self.add_widget(self.top_appbar)
        
        # Size and position the overlay to match the app bar
        self.progress_overlay.size = self.top_appbar.size
        self.progress_overlay.pos = self.top_appbar.pos
        
        # Bind the progress overlay to the app bar's progress and size
        self.top_appbar.bind(p_width=self._update_progress_overlay)
        self.top_appbar.bind(size=self._update_progress_overlay_size)
        self.top_appbar.bind(pos=self._update_progress_overlay_pos)
    
    def _update_progress_overlay(self, instance, value):
        """Update progress overlay width when app bar progress changes"""
        self.progress_overlay.p_width = value
    
    def _update_progress_overlay_size(self, instance, value):
        """Update progress overlay size when app bar size changes"""
        self.progress_overlay.size = self.top_appbar.size
    
    def _update_progress_overlay_pos(self, instance, value):
        """Update progress overlay position when app bar position changes"""
        self.progress_overlay.pos = self.top_appbar.pos

