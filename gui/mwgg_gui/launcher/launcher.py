from __future__ import annotations
"""
LAUNCHER SCREEN

LauncherScreen - main screen for displaying the launcher
LauncherLayout - layout for the launcher screen
LauncherView - view for the launcher screen

Includes the following:
- FavoritesCarousel - carousel for displaying favorite games
"""

__all__ = ('LauncherScreen', 
           'LauncherLayout', 
           'LauncherView', 
           'LauncherAuthTextField'
           )
import asynckivy
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivymd.uix.sliverappbar import MDSliverAppbar
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText


import logging
from typing import Any
import tempfile
import shutil
import zipfile
import os
import sys
from pathlib import Path
import subprocess
import threading
import urllib.parse

from kivymd.app import MDApp
from mwgg_igdb import GameIndex

from mwgg_gui.overrides.expansionlist import *
from mwgg_gui.components.bottomappbar import BottomAppBar
from mwgg_gui.launcher.launcher_sliver_appbar import LauncherSliverAppbar
from mwgg_gui.launcher.launcher_favorite_bar import FavoritesScroll, Favorite
from mwgg_gui.launcher.launcher_yaml import YamlDialog
from mwgg_gui.components.dialog import MessageBox

from Utils import (discover_and_launch_module, 
                   get_available_worlds, 
                   user_path,
                   local_path,
                   is_frozen,
                   is_windows)

from FileUtils import FileUtils

logger = logging.getLogger("Client")

with open(os.path.join(os.path.dirname(__file__), "launcher.kv"), encoding="utf-8") as kv_file:
    Builder.load_string(kv_file.read())

class LauncherLayout(MDFloatLayout):
    pass

class LauncherView(MDBoxLayout):
    slot_layout: ObjectProperty
    server_layout: ObjectProperty
    title_layout: ObjectProperty

class LauncherAuthTextField(MDTextField):
    pass

class LauncherGenerateContent(MDBoxLayout):
    pass

class LauncherHostContent(MDBoxLayout):
    pass

class LauncherPatchContent(MDBoxLayout):
    pass

class LauncherScreen(MDScreen, ThemableBehavior):
    '''
    This is the main screen for the launcher.
    Left side has the game list/sorter
    Right contains the previously selected game
    with options to connect to the MW server
    '''
    name = "launcher"
    launchergrid: LauncherLayout
    important_appbar: MDSliverAppbar
    launcher_view: LauncherView
    game_filter: list
    available_games: list
    game_tag_filter: StringProperty
    bottom_appbar: BottomAppBar
    selected_game: tuple[str, str] = ("", "")
    highlighted_favorite: ObjectProperty(None, allownone=True)
    app: MDApp
    result: Any
    favorite_games: ListProperty = ListProperty([])
    saved_games: ListProperty = ListProperty([])
    yaml_dialog_layout: ObjectProperty = ObjectProperty(None)
    _password_as_text: bool = False # True to show password as text, False to show password as asterisks

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.game_filter = []
        self.games_mdlist = MDList(width=260)
        self.game_tag_filter = "popular"
        self.selected_game = ""
        self.highlighted_favorite = None
        self.app = MDApp.get_running_app()
        self.available_games = []
        # Load favorite games from config

        self.bottom_appbar = BottomAppBar(screen_name="launcher")
        self.important_appbar = LauncherSliverAppbar()
        self.launcher_view = LauncherView()
        Clock.schedule_once(lambda x: self.init_important())

    def show_snackbar(self, message: str, is_error: bool = False):
        """Show a snackbar notification"""
        snackbar = MDSnackbar(
            MDSnackbarText(
                text=message,
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
            md_bg_color=self.app.theme_cls.errorColor if is_error else self.app.theme_cls.primaryColor,
        )
        snackbar.open()

    def init_important(self):
        """Initialize the bigger parts of the launcher screen"""
        self.launchergrid = LauncherLayout()

        self.add_widget(self.launchergrid)
        self.add_widget(self.bottom_appbar)

        self.important_appbar.size_hint_x = 260/Window.width
        self.important_appbar.size_hint_y=1
        self.launcher_view.size_hint_x = 1-(264/Window.width)
        self.launcher_view.size_hint_y =1

        self.important_appbar.ids.scroll.scroll_wheel_distance = 40
        #self.important_appbar.ids.scroll.y = 82

        self.important_appbar.content.add_widget(self.games_mdlist)

        self.launchergrid.add_widget(self.important_appbar)
        self.launcher_view.pos_hint={"y": 0, "x": 260/Window.width}
        self.launchergrid.add_widget(self.launcher_view)

        fave_scroll = FavoritesScroll()
        self.favorites_layout = fave_scroll.favorites
        self.launcher_view.ids.title_layout.add_widget(fave_scroll)
        fave_scroll.size = (self.launcher_view.ids.title_layout.width, dp(100))
        
        self.available_games = get_available_worlds()
        self.load_favorite_games()
        # Update button text based on initial context
        Clock.schedule_once(lambda dt: self.update_connect_button_text(), 0.2)
        #Clock.schedule_once(lambda dt: self.update_selected_game(), 0.2)
        Clock.schedule_once(lambda dt: self.populate_favorites(), 0.2)
        # Start game list population after available_games is populated
        asynckivy.start(self.set_game_list())

    async def set_game_list(self):
        """Set the game list based on the game tag filter"""
        matching_games = GameIndex.search(self.game_tag_filter)
        not_in_available_games = [game_module for game_module in matching_games.keys() \
                                  if game_module not in self.available_games]
        for game_module in not_in_available_games:
            matching_games.pop(game_module)
        self.games_mdlist.clear_widgets()
        for module_name, game_data in matching_games.items():
            await asynckivy.sleep(0)
            game = GameListPanel(
                item_name=module_name, 
                item_data=game_data,
                on_game_select=lambda x, name=module_name, game_name=game_data['game_name']: self.on_game_selected((name, game_name))
            )
            self.games_mdlist.add_widget(game)

    def on_game_selected(self, game_info: tuple[str, str]):
        """Handle game selection from the game list"""
        self.selected_game = game_info
        logger.info(f"Selected game: {game_info[1]}")
        # Update the launcher view to show the selected game
        self.launcher_view.module_name = game_info[0]
        # Update button text based on context
        self.update_connect_button_text()

        if not self.is_favorite(game_info[0]):
            self.add_to_favorite_bar(game_info[0])
   
    def set_filter(self, active, tag):
        """Set the game search filter based on the game tag filter"""
        if active:
            self.game_filter.append((self.game_tag_filter.text, tag))
        else:
            self.game_filter.remove((self.game_tag_filter.text, tag))

    def on_game_tag_filter_text(self, instance):
        """Set the game search filter based on the game tag filter"""
        self.game_filter = [(self.game_tag_filter.text, tag) for tag in GameIndex.search(self.game_tag_filter.text)]

    def update_connect_button_text(self):
        """Update the connect button text based on current context"""
        current_ctx = self.app.ctx
        connect_button = self.launcher_view.ids.connect_button
        
        # Check if we're in initial state by checking if ctx has a 'game' attribute
        if not hasattr(current_ctx, 'game'):
            # Initial state - launch new game
            connect_button._button_text.text = 'Connect & Play'
            connect_button._button_icon.icon = 'play-network'
        else:
            # Game context - reconnect
            game_name = getattr(current_ctx, 'game', 'Unknown Game')
            connect_button._button_text.text = f'Reconnect ({game_name})'
            connect_button._button_icon.icon = 'refresh'

    def load_favorite_games(self):
        """Load favorite games from app config"""
        try:
            favorites_str = self.app.app_config.get('game_settings', 'favorite_games', fallback='')
            if favorites_str:
                self.saved_games = favorites_str.split(',')
                self.favorite_games = self.saved_games.copy()
            else:
                self.saved_games = []
                self.favorite_games = []
        except (KeyError):
            self.favorite_games = []
            self.saved_games = []
        logger.debug(f"Loaded {len(self.favorite_games)} favorite games")

    def save_favorite_games(self, module_name: str = None):
        """Save favorite games to app config"""
        try:
            if module_name:
                self.saved_games.append(module_name)
            if not self.app.app_config.has_section('game_settings'):
                self.app.app_config.add_section('game_settings')
            self.app.app_config.set('game_settings', 'favorite_games', ','.join(self.saved_games).lstrip(","))
            self.app.app_config.write()
            logger.debug(f"Saved {len(self.favorite_games)} favorite games")
        except Exception as e:
            logger.error(f"Failed to save favorite games: {e}")

    def populate_favorites(self, game_module: str = None):
        """Populate the favorites with favorite games"""
        try:
            self.favorites_layout.clear_widgets()
            
            if not self.favorite_games and not game_module:
                # Add a placeholder item when no favorites
                placeholder = Favorite(game_name="", game_module="")
                self.favorites_layout.add_widget(placeholder)
                return
            
            for name in self.favorite_games:

                try:
                    game_name = GameIndex.get_game_name_for_module(name)
                    if game_name:
                        favorite_tab = Favorite(game_name=game_name, game_module=name)
                        self.favorites_layout.add_widget(favorite_tab)
                        if game_module and game_module == name:
                            self.set_favorite_highlight(favorite_tab)
                except Exception as e:
                    logger.error(f"Failed to add favorite {name}: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to populate favorites tabs: {e}")

    def add_to_favorite_bar(self, module_name: str):
        """Add a game to favorites"""
        if module_name not in self.favorite_games:
            self.favorite_games.append(module_name)
            self.populate_favorites(module_name)

    def remove_from_favorites(self, module_name: str):
        """Remove a game from favorites"""
        if module_name in self.saved_games:
            self.saved_games.remove(module_name)
            self.save_favorite_games()
            self.populate_favorites()
            logger.info(f"Removed {module_name} from favorites")

    def toggle_favorite(self, module_name: str):
        """Toggle favorite status for a game"""
        if module_name in self.saved_games:
            self.remove_from_favorites(module_name)
        else:
            self.save_favorite_games(module_name)

    def is_favorite(self, module_name: str) -> bool:
        """Check if a game is in favorites"""
        return module_name in self.saved_games

    def swipe_to_favorite(self, module_name: str):
        """Switch to a specific favorite game tab"""
        try:
            if not self.favorite_games:
                return
                
            # Find the game name for this module
            game_name = GameIndex.get_game_name_for_module(module_name)
            if game_name:
                self.favorites_layout.switch_tab(text=game_name)
                logger.info(f"Switched to favorite {module_name}")
            else:
                logger.warning(f"Game {module_name} not found in favorites")
                
        except Exception as e:
            logger.error(f"Failed to switch to favorite: {e}")

    def on_favorite_clicked(self, module_name: str):
        """Handle clicking on a favorite item in the tabs"""
        try:
            game_data = GameIndex.get_game(module_name)
            if game_data:
                game_name = game_data.get('game_name', module_name)
                self.on_game_selected((module_name, game_name))
                logger.info(f"Selected favorite game: {game_name}")
        except Exception as e:
            logger.error(f"Failed to select favorite game {module_name}: {e}")
    
    def set_favorite_highlight(self, favorite_widget):
        """Set which favorite is highlighted, unhighlighting the previous one"""
        # Unhighlight the previously highlighted favorite
        if self.highlighted_favorite and self.highlighted_favorite != favorite_widget:
            self.highlighted_favorite.unhighlight()
        
        # Set and highlight the new favorite
        self.highlighted_favorite = favorite_widget
        if favorite_widget:
            favorite_widget.highlight()

    def generate(self):
        """Generate a new game"""
        # Step 1: Select files (multiple .zip/.yaml files)
        selected_files = self._select_generation_files()
        if not selected_files:
            return
        
        # Step 2: Create temporary directory and process files
        temp_dir = self._create_temp_workspace(selected_files)
        if not temp_dir:
            return
            
        # Store temp_dir for later use
        self._generation_temp_dir = temp_dir
            
        # Step 3: Show generation options dialog
        self._show_generation_options()

    def _select_generation_files(self):
        """Select multiple .zip/.yaml files for generation"""
        # Show file dialog for .zip and .yaml files
        result = FileUtils.open_file_input_dialog(
            title="Select Generation Files (.zip/.yaml)",
            filetypes=[("YAML Files", ["*.yaml", "*.yml"]), ("ZIP Files", ["*.zip"]), ("All Supported", ["*.yaml", "*.yml", "*.zip"])],
            multiple=True,
            suggest=user_path("Players")
        )
        
        if not result:
            return []
            
        # Handle both single file and multiple files
        if isinstance(result, str):
            selected_files = [result]
        else:
            selected_files = result
            
        # Show confirmation of selected files
        if len(selected_files) == 1:
            self.show_snackbar(f"Selected: {os.path.basename(selected_files[0])}")
        else:
            self.show_snackbar(f"Selected {len(selected_files)} files for generation")
            
        return selected_files

    def _create_temp_workspace(self, selected_files):
        """Create temporary directory and copy/extract files"""
        temp_dir = tempfile.mkdtemp(prefix="mwgg_generate_")
        
        for file_path in selected_files:
            if file_path.lower().endswith('.zip'):
                # Extract zip file
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            else:
                # Copy yaml file
                shutil.copy2(file_path, temp_dir)
        
        return temp_dir

    def _show_generation_options(self):
        """Show dialog with generation options"""
        # Create dialog content
        content = LauncherGenerateContent()
        seed_field = content.ids.seed
        output_field = content.ids.output
        
        # Create dialog
        dialog = MDDialog(
            MDDialogHeadlineText(
                text="Generation Options",
            ),
            content,
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="CANCEL"),
                    on_release=lambda x: self._on_generation_options_cancel(dialog)
                ),
                MDButton(
                    MDButtonText(text="GENERATE"),
                    on_release=lambda x: self._on_generation_options_confirm(dialog, seed_field, output_field)
                ),
                spacing=dp(8)
            )
        )
        
        # Store dialog reference and open it
        self._generation_dialog = dialog
        self._generation_result = None
        dialog.open()

    def _on_generation_options_cancel(self, dialog):
        """Handle generation options cancellation"""
        dialog.dismiss()
        # Cleanup temp directory
        self._cleanup_temp_dir(self._generation_temp_dir)
        delattr(self, '_generation_temp_dir')

    def _on_generation_options_confirm(self, dialog, seed_field, output_field):
        """Handle generation options confirmation"""
        try:
            seed = seed_field.text.strip()
            seed_value = int(seed) if seed else None
        except ValueError:
            self.show_snackbar("Seed must be a number or empty for random", is_error=True)
            return
            
        output_path = output_field.text.strip()
        if not output_path:
            output_path = os.path.join(os.getcwd(), 'output')
            
        self._generation_result = {
            'seed': seed_value,
            'output_path': output_path
        }
        
        dialog.dismiss()
        # Continue with generation
        self._continue_generation()

    def _continue_generation(self):
        """Continue with generation after options are confirmed"""
        if not hasattr(self, '_generation_result') or not self._generation_result:
            self._cleanup_temp_dir(self._generation_temp_dir)
            return
            
        # Step 4: Execute MultiworldGGGenerate.exe
        # Note: cleanup happens in the background thread after completion
        self._execute_generation(self._generation_temp_dir, self._generation_result)

    def _execute_generation(self, temp_dir, options):
        """Execute MultiworldGGGenerate.exe with options in background thread"""
        from BaseUtils import is_frozen, local_path, is_windows
        
        # Build command
        if is_frozen():
            exe_path = local_path("MultiworldGGGenerate.exe") if is_windows else local_path("MultiworldGGGenerate")
            cmd = [str(exe_path), "--player-files-path", temp_dir]
            cwd = os.path.dirname(exe_path)
            env = None
        else:
            exe_path = Path(sys.executable)
            file_path = Path(local_path("Generate.py"))
            cmd = [str(exe_path), str(file_path), "--player-files-path", temp_dir]
            cwd = os.path.dirname(file_path)
            # Also set KIVY_NO_ARGS to disable Kivy's argument parser
            env = os.environ.copy()
            env['KIVY_NO_ARGS'] = '1'
        
        if options.get('seed'):
            cmd.extend(["--seed", str(options['seed'])])
            
        if options.get('output_path'):
            cmd.extend(["--outputpath", options['output_path']])
        
        # Ensure temp directory exists before starting generation
        if not os.path.exists(temp_dir):
            logger.error(f"Temp directory {temp_dir} does not exist!")
            MessageBox("Generation Error", f"Temp directory does not exist: {temp_dir}").open()
            return
            
        logger.info(f"Starting generation with command: {' '.join(cmd)}")
        logger.info(f"Using temp directory: {temp_dir}")
        
        # Show loading screen
        Clock.schedule_once(lambda dt: self.app.loading_layout.show_loading(display_logs=True), 0)
        
        def run_generation():
            """Run generation in background thread and stream output to logger"""
            
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=cwd,
                    bufsize=1,  # Line buffered
                    universal_newlines=True,
                    env=env
                )
                
                # Stream stdout
                for line in process.stdout:
                    line = line.rstrip()
                    if line:
                        logger.info(f"[Generate] {line}")
                
                # Wait for process to complete
                process.wait()
                
                # Capture any remaining stderr
                stderr = process.stderr.read()
                if stderr:
                    for line in stderr.splitlines():
                        if line.strip():
                            logger.error(f"[Generate Error] {line}")
                
                # Hide loading screen and schedule UI update on main thread
                def show_success_dialog(dt):
                    self.app.loading_layout.hide_loading()
                    MessageBox("Generation Complete", 
                               "Game generation completed successfully!").open()
                    # Cleanup after success
                    self._cleanup_temp_dir(temp_dir)
                    if hasattr(self, '_generation_temp_dir'):
                        delattr(self, '_generation_temp_dir')
                    if hasattr(self, '_generation_result'):
                        delattr(self, '_generation_result')
                
                def show_failure_dialog(dt):
                    self.app.loading_layout.hide_loading()
                    MessageBox("Generation Failed", 
                               f"Generation failed with code {process.returncode}:\n{error_msg}").open()
                    # Cleanup after failure
                    self._cleanup_temp_dir(temp_dir)
                    if hasattr(self, '_generation_temp_dir'):
                        delattr(self, '_generation_temp_dir')
                    if hasattr(self, '_generation_result'):
                        delattr(self, '_generation_result')

                def show_restart_dialog(dt):
                    self.app.loading_layout.hide_loading()
                    MessageBox("Restart Required", 
                               "You will need to restart the launcher to apply updates.",
                               error=True, 
                               callback=lambda x: self.restart_launcher()).open()

                
                if process.returncode == 0:
                    Clock.schedule_once(show_success_dialog, 0)
                    logger.info("Generation completed successfully")
                elif process.returncode == 10:
                    # Exit code 10 means "wrong environment" - library updates needed
                    logger.info("Generation requested launcher restart for environment refresh")
                    Clock.schedule_once(show_restart_dialog, 0)
                else:
                    error_msg = stderr if stderr else "Unknown error"
                    Clock.schedule_once(show_failure_dialog, 0)
                    logger.error(f"Generation failed with return code {process.returncode}")
                    
            except Exception as e:
                logger.exception(f"Failed to execute generation: {e}")
                def show_error_dialog(dt):
                    self.app.loading_layout.hide_loading()
                    MessageBox("Generation Error", 
                               f"Failed to execute generation: {str(e)}").open()
                    # Cleanup after error
                    self._cleanup_temp_dir(temp_dir)
                    if hasattr(self, '_generation_temp_dir'):
                        delattr(self, '_generation_temp_dir')
                    if hasattr(self, '_generation_result'):
                        delattr(self, '_generation_result')
                Clock.schedule_once(show_error_dialog, 0)
        
        # Start generation in background thread
        thread = threading.Thread(target=run_generation, daemon=True)
        thread.start()

    def _prepare_connect_args(self, game_module, server_address=None):
        """Prepare command line arguments for reconnecting after restart"""
        args = sys.argv.copy()
        
        # Add game module argument
        game_arg = f"--game={game_module}"
        if game_arg not in args:
            args.append(game_arg)
        
        # Add connection parameters using standard argument formats
        if server_address not in args and server_address:
            args.append(f"--server-address={server_address}")
            
        return args

    def restart_launcher(self, connect_args=None):
        """Restart the launcher with the same arguments, optionally with connection args"""
        logger.info("Restarting launcher due to environment refresh...")
        
        # Use connect_args if provided, otherwise use sys.argv
        restart_args = connect_args if connect_args else sys.argv
        
        # Ensure the new process is fully detached from the parent
        if is_windows():
            subprocess.Popen([sys.executable] + restart_args,
                           cwd=os.getcwd(),
                           creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_CONSOLE)
        
        # Flush all logging handlers to ensure messages are displayed
        for handler in logging.root.handlers:
            handler.flush()
        
        # Use sys.exit to bypass cleanup and immediately terminate
        sys.exit(10)

    def _cleanup_temp_dir(self, temp_dir):
        """Clean up temporary directory"""
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            logger.warning(f"Failed to clean up temp directory {temp_dir}: {e}")

    def host(self):
        """Host a new game"""
        # Show host options dialog
        self._show_host_options()

    def _show_host_options(self):
        """Show dialog with host options"""
        # Create dialog content
        content = LauncherHostContent()
        port_field = content.ids.port
        admin_password_field = content.ids.admin_password
        
        # Create dialog
        dialog = MDDialog(
            MDDialogHeadlineText(
                text="Server Options",
            ),
            content,
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="CANCEL"),
                    on_release=lambda x: dialog.dismiss()
                ),
                MDButton(
                    MDButtonText(text="START SERVER"),
                    on_release=lambda x: self._on_host_options_confirm(dialog, port_field, admin_password_field)
                ),
                spacing=dp(8)
            )
        )
        
        # Store dialog reference and open it
        self._host_dialog = dialog
        self._host_result = None
        dialog.open()

    def _on_host_options_confirm(self, dialog, port_field, admin_password_field):
        """Handle host options confirmation"""
        port = port_field.text.strip()
        admin_password = admin_password_field.text.strip()
        
        # Validate port
        if port:
            try:
                port_value = int(port)
                if not (1 <= port_value <= 65535):
                    self.show_snackbar("Port must be between 1 and 65535", is_error=True)
                    return
            except ValueError:
                self.show_snackbar("Port must be a number", is_error=True)
                return
        
        self._host_result = {
            'port': port if port else None,
            'server-password': admin_password if admin_password else None
        }
        
        dialog.dismiss()
        # Continue with hosting
        self._execute_host(self._host_result)

    def _execute_host(self, options):
        """Execute MultiworldGGServer with options - detached from client"""
        # Build command
        if is_frozen():
            exe_path = local_path("MultiWorldGGServer.exe") if is_windows else local_path("MultiWorldGGServer")
            cmd = [str(exe_path)]
            cwd = os.path.dirname(exe_path)
            env = None
        else:
            exe_path = Path(sys.executable)
            file_path = Path(local_path("MultiServer.py"))
            cmd = [str(exe_path), str(file_path)]
            cwd = os.path.dirname(file_path)
            # Also set KIVY_NO_ARGS to disable Kivy's argument parser
            env = os.environ.copy()
            env['KIVY_NO_ARGS'] = '1'
        
        if options.get('port'):
            cmd.extend(["--port", str(options['port'])])
            
        if options.get('server-password'):
            cmd.extend(["--server-password", options['server-password']])
        
        logger.info(f"Starting detached server with command: {' '.join(cmd)}")
        
        # Launch server - console app will spawn its own terminal
        try:
            subprocess.Popen(
                cmd,
                cwd=cwd,
                env=env
            )
            MessageBox("Server Started", "MultiWorldGG Server has been started in a new terminal window.").open()
            logger.info("Server launched successfully (detached)")
            if hasattr(self, '_host_result'):
                delattr(self, '_host_result')
        except Exception as e:
            logger.exception(f"Failed to start server: {e}")
            MessageBox("Server Error", f"Failed to start server: {str(e)}").open()
            if hasattr(self, '_host_result'):
                delattr(self, '_host_result')
    
    def patch_game(self):
        """Patch the selected game"""
        # Step 1: Select patch file (.apbp)
        selected_file = self._select_patch_file()
        if not selected_file:
            return
        
        # Store selected file
        self._patch_file = selected_file
        
        # Step 2: Show patch options dialog
        self._show_patch_options()

    def _select_patch_file(self):
        """Select .ap file for patching"""
        # Show file dialog for .ap files
        result = FileUtils.open_file_input_dialog(
            title="Select Patch File (.ap*)",
            filetypes=[("All Files", ["*.*"])],
            multiple=False,
            suggest=user_path("output")
        )
        
        if not result:
            return None
            
        # Show confirmation
        self.show_snackbar(f"Selected: {os.path.basename(result)}")
        return result

    def _show_patch_options(self):
        """Show dialog with patch options"""
        # Create dialog content
        content = LauncherPatchContent()
        output_field = content.ids.output
        
        # Create dialog
        dialog = MDDialog(
            MDDialogHeadlineText(
                text="Patch Options",
            ),
            content,
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="CANCEL"),
                    on_release=lambda x: self._on_patch_options_cancel(dialog)
                ),
                MDButton(
                    MDButtonText(text="PATCH"),
                    on_release=lambda x: self._on_patch_options_confirm(dialog, output_field)
                ),
                spacing=dp(8)
            )
        )
        
        # Store dialog reference and open it
        self._patch_dialog = dialog
        self._patch_result = None
        dialog.open()

    def _on_patch_options_cancel(self, dialog):
        """Handle patch options cancellation"""
        dialog.dismiss()
        if hasattr(self, '_patch_file'):
            delattr(self, '_patch_file')

    def _on_patch_options_confirm(self, dialog, output_field):
        """Handle patch options confirmation"""
        output_path = output_field.text.strip()
        if not output_path:
            output_path = os.path.join(os.getcwd(), 'output')
        
        self._patch_result = {
            'output_path': output_path
        }
        
        dialog.dismiss()
        # Continue with patching
        self._execute_patch(self._patch_file, self._patch_result)

    def _execute_patch(self, patch_file, options):
        """Execute MultiworldGGPatch with options in background thread"""
        # Build command
        if is_frozen():
            exe_path = local_path("MultiworldGGPatch.exe") if is_windows else local_path("MultiworldGGPatch")
            cmd = [str(exe_path), patch_file]
            cwd = os.path.dirname(exe_path)
            env = None
        else:
            exe_path = Path(sys.executable)
            file_path = Path(local_path("Patch.py"))
            cmd = [str(exe_path), str(file_path), patch_file]
            cwd = os.path.dirname(file_path)
            # Also set KIVY_NO_ARGS to disable Kivy's argument parser
            env = os.environ.copy()
            env['KIVY_NO_ARGS'] = '1'
        
        if options.get('output_path'):
            cmd.extend(["--outputpath", options['output_path']])
        
        logger.info(f"Starting patch with command: {' '.join(cmd)}")
        
        # Show loading screen
        Clock.schedule_once(lambda dt: self.app.loading_layout.show_loading(), 0)
        
        def run_patch():
            """Run patch in background thread and stream output to logger"""
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=cwd,
                    bufsize=1,  # Line buffered
                    universal_newlines=True,
                    env=env
                )
                
                # Stream stdout
                for line in process.stdout:
                    line = line.rstrip()
                    if line:
                        logger.info(f"[Patch] {line}")
                
                # Wait for process to complete
                process.wait()
                
                # Capture any remaining stderr
                stderr = process.stderr.read()
                if stderr:
                    for line in stderr.splitlines():
                        if line.strip():
                            logger.error(f"[Patch Error] {line}")
                
                # Hide loading screen and schedule UI update on main thread
                def show_success_dialog(dt):
                    self.app.loading_layout.hide_loading()
                    MessageBox("Patch Complete", 
                               "Game patching completed successfully!").open()
                    if hasattr(self, '_patch_file'):
                        delattr(self, '_patch_file')
                    if hasattr(self, '_patch_result'):
                        delattr(self, '_patch_result')
                
                def show_failure_dialog(dt):
                    self.app.loading_layout.hide_loading()
                    error_msg = stderr if stderr else "Unknown error"
                    MessageBox("Patch Failed", 
                               f"Patch failed with code {process.returncode}:\n{error_msg}").open()
                    if hasattr(self, '_patch_file'):
                        delattr(self, '_patch_file')
                    if hasattr(self, '_patch_result'):
                        delattr(self, '_patch_result')

                def show_restart_dialog(dt):
                    self.app.loading_layout.hide_loading()
                    MessageBox("Restart Required", 
                               "You will need to restart the launcher to apply updates.",
                               error=True, 
                               callback=lambda x: self.restart_launcher()).open()
                
                if process.returncode == 0:
                    Clock.schedule_once(show_success_dialog, 0)
                    logger.info("Patch completed successfully")
                elif process.returncode == 10:
                    # Exit code 10 means "wrong environment" - library updates needed
                    logger.info("Patch requested launcher restart for environment refresh")
                    Clock.schedule_once(show_restart_dialog, 0)
                else:
                    Clock.schedule_once(show_failure_dialog, 0)
                    logger.error(f"Patch failed with return code {process.returncode}")
                    
            except Exception as e:
                logger.exception(f"Failed to execute patch: {e}")
                def show_error_dialog(dt):
                    self.app.loading_layout.hide_loading()
                    MessageBox("Patch Error", 
                               f"Failed to execute patch: {str(e)}").open()
                    if hasattr(self, '_patch_file'):
                        delattr(self, '_patch_file')
                    if hasattr(self, '_patch_result'):
                        delattr(self, '_patch_result')
                Clock.schedule_once(show_error_dialog, 0)
        
        # Start patch in background thread
        thread = threading.Thread(target=run_patch, daemon=True)
        thread.start()
    
    def create_yaml(self):
        """Create YAML file for the selected game"""
        if not self.selected_game:
            MessageBox("No Game Selected", "Please select a game before creating YAML.").open()
            return

        try:
            self.yaml_dialog_layout = YamlDialog(
                selected_game=self.selected_game
            )
            self.yaml_dialog_layout.bind(on_dismiss=self.on_yaml_dialog_dismiss)

            self.app.root.add_widget(self.yaml_dialog_layout)
            

            
        except Exception as e:
            logger.error(f"Failed to create YAML for {self.selected_game[1]}: {e}", exc_info=True, stack_info=True)
            MessageBox("YAML Creation Error", f"Failed to create YAML for {self.selected_game[1]}: {str(e)}", is_error=True).open()

    def on_yaml_dialog_dismiss(self, *args):
        """Handle dismissal of the YAML dialog"""
        if hasattr(self, 'yaml_dialog_layout') and self.yaml_dialog_layout:
            self.app.root.remove_widget(self.yaml_dialog_layout)
            self.yaml_dialog_layout = None

    @property
    def server_address(self) -> str:
        # Return the server address as a url parse string for connection.
        server_text = self.launcher_view.ids.server.text or self.launcher_view.ids.server.hint_text
        port_text = self.launcher_view.ids.port.text or self.launcher_view.ids.port.hint_text
        slot_name_text = self.launcher_view.ids.slot_name.text or self.launcher_view.ids.slot_name.hint_text
        if self._password_as_text:
            slot_password_text = self.launcher_view.ids.slot_password.text if self.launcher_view.ids.slot_password.text else ""
        else:
            slot_password_text = "********" if self.launcher_view.ids.slot_password.text else ""
        colon_text = ":" if slot_name_text else ""
        return f"{slot_name_text}{colon_text}{slot_password_text}@{server_text}:{port_text}" if server_text and port_text else None

    def connect(self):
        """Connect to server and launch the selected game module"""
        logger.info("Connect method called!")
        
        # Get the current app context
        current_ctx = self.app.ctx

        self._password_as_text = False
        server_address = "".join(self.server_address) if self.server_address else None
        self._password_as_text = True

        # Check if we're in initial state by checking if ctx has a 'game' attribute
        if not hasattr(current_ctx, 'game'):
            if not self.selected_game:
                MessageBox("No Game Selected", "Please select a game before connecting.").open()
                return
            
            self.app.logo_png = GameIndex.get_game(self.selected_game[0]).get("cover_url", None)

            logger.info(f"Attempting to launch module: {self.selected_game[1]}")
            logger.info(f"Server: {server_address}")
            
            try:
                # Show loading screen
                Clock.schedule_once(lambda dt: self.app.loading_layout.show_loading(display_logs=True), 0)

                # Define ready callback to hide loading layout and switch to console
                def ready_callback(dt: float = 0):
                    Clock.schedule_once(lambda x: self.app.loading_layout.hide_loading(), 0)
                    # Switch to console after successful connection
                    Clock.schedule_once(lambda x: self.app.console_init())
                    Clock.schedule_once(lambda x: self.app.change_screen("console"))
                
                # Define error callback to handle connection failures
                def error_callback(restart_callback=None):
                    Clock.schedule_once(lambda x: self.app.loading_layout.hide_loading(), 0)
                    # If restart_callback is provided, it means we need to restart due to module updates
                    if restart_callback:
                        # Prepare connection arguments for restart
                        connect_args = self._prepare_connect_args(
                            game_module=self.selected_game[0],
                            server_address=self.server_address,
                        )
                        MessageBox("Restart Required", 
                                   "You will need to restart the launcher to apply updates.",
                                   error=True, 
                                   callback=lambda x: self.restart_launcher(connect_args)).open()
                    else:
                        # Stay on launcher screen, don't switch to console
                        # Error dialog will be shown by the context's handle_connection_loss
                        pass
                
                self.app.client_console_init()

                discover_and_launch_module(
                        f"worlds.{self.selected_game[0]}", server_address=self.server_address, ready_callback=ready_callback, error_callback=error_callback
                )
                    
            except Exception as e:
                logger.error(f"Failed to launch {self.selected_game[1]} module: {e}")
                # Hide loading layout on error
                Clock.schedule_once(lambda x: self.app.loading_layout.hide_loading(), 0)
                # Show error dialog and stay on launcher screen
                MessageBox("Launch Error", f"Failed to launch {self.selected_game[1]}: {str(e)}", is_error=True).open()
        
        else:
            # We're in a game context, check if the selected game matches the current context
            # TODO: Use a list for tracker/_sni/_bizhawk/"" and allow for those "game"s (empty is text client)
            if hasattr(current_ctx, 'game') and current_ctx.game and current_ctx.game != self.selected_game[1]:
                # Game mismatch - need to rebuild to InitContext first
                logger.info(f"Game mismatch: current={current_ctx.game}, selected={self.selected_game[1]}")
                MessageBox("Game Mismatch", 
                                f"Current game ({current_ctx.game}) doesn't match selected game ({self.selected_game[1]}). "
                                "Please restart the client to change games.", is_error=True).open()
                return
            
            # Game matches, try to connect using the current context
            try:
                if not self.server_address:
                    MessageBox("Connection Error", "Please enter a valid server address and port.", is_error=True).open()
                    return
                
                logger.info(f"Attempting to connect to: {server_address}")
                
                # Show loading screen
                Clock.schedule_once(lambda dt: self.app.loading_layout.show_loading(), 0)
                
                # Use the context's connect method
                import asyncio
                asyncio.create_task(current_ctx.connect(self.server_address))
                
                # Hide loading screen after a short delay (connection will handle its own UI updates)
                Clock.schedule_once(lambda dt: self.app.loading_layout.hide_loading(), 2)
                
            except Exception as e:
                logger.error(f"Failed to connect: {e}")
                Clock.schedule_once(lambda x: self.app.loading_layout.hide_loading(), 0)
                MessageBox("Connection Error", f"Failed to connect: {str(e)}", is_error=True).open()
