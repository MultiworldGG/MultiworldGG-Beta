from kivymd.app import MDApp
from mw_theme import RegisterFonts
from launcher import LauncherScreen
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
import kivymd.uix.textfield
import importlib
import os
import sys
import logging
from kivy.logger import Logger

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

# Set Kivy logger level
Logger.setLevel(logging.DEBUG)

# Create logger for this module
logger = logging.getLogger(__name__)

class TestLauncherApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        RegisterFonts(self)
        importlib.reload(kivymd.uix.textfield)

    def on_start(self):
        logger.info("Application started")
        logger.debug(f"Window size: {self.root_window.size}")

    def build(self):
        logger.info("Starting application build")
        # Ensure the game_details.json exists
        # if not os.path.exists("game_details.json"):
        #     logger.error("game_details.json not found")
        #     sys.exit("game_details.json not found")
        
        logger.debug("Creating screen manager")
        screen_manager = MDScreenManager()
        
        logger.debug("Creating launcher screen")
        launcher_screen = LauncherScreen()
        
        logger.debug("Adding launcher screen to manager")
        screen_manager.add_widget(launcher_screen)
        
        logger.debug("Setting current screen to test")
        screen_manager.current = "launcher"
        
        logger.info("Application build complete")
        return screen_manager

if __name__ == '__main__':
    logger.info("Starting TestLauncherApp")
    TestLauncherApp().run() 