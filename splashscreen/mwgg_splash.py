from __future__ import annotations
"""
SplashScreen

Run as a standalone script in a separate process    
that will be displayed when the application is launched.

This is used to display the loading animation while the
application is loading.
"""

__all__ = ('SplashScreen',)

from multiprocessing import freeze_support, Process
import os
import sys
import time
import logging
import threading
import signal
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

logger = logging.getLogger("MultiWorld")

class SplashScreen:
    def __init__(self, png_path, loop_count=1):
        try:
            # Initialize the main window
            self.loop_done = False
            self.root = tk.Tk()
            self.root.overrideredirect(True)  # Remove window decorations
            self.root.attributes("-transparent", "black")  # Enable transparency
            self.root.attributes("-topmost", True)  # Keep window on top
            
            # Load the animated PNG
            try:
                self.img = Image.open(png_path)
            except Exception as e:
                logging.error(f"Failed to load image '{png_path}': {e}")
                raise
            
            # Get image dimensions
            self.width, self.height = self.img.size
            
            # Center the window on the screen
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - self.width) // 2
            y = (screen_height - self.height) // 2
            self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
            
            # Create a canvas for displaying the image
            self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, 
                                    highlightthickness=0, borderwidth=0, bg='black')
            self.canvas.pack()
            
            # Configuration
            self.loop_count = loop_count
            self.current_loop = 0
            self.frames = []
            self.frame_durations = []
            
            # Store all frames and their durations
            frame_count = 0
            for frame in ImageSequence.Iterator(self.img):
                try:
                    # Convert to RGBA if not already
                    if frame.mode != 'RGBA':
                        frame = frame.convert('RGBA')
                    
                    # Get frame duration in milliseconds
                    duration = int(frame.info.get('duration', 100))  # Default to 100ms if not specified
                    
                    photoframe = ImageTk.PhotoImage(frame)
                    self.frames.append(photoframe)
                    self.frame_durations.append(duration)
                    frame_count += 1
                except Exception as e:
                    logging.error(f"Failed to process frame {frame_count}: {e}")
                    raise
            
            if frame_count == 0:
                raise ValueError("No valid frames found in the image")
            
            # Start animation
            self.current_frame = 0
            self.animate()
            
            self.monitor_thread = None
            
        except Exception as e:
            logging.error(f"Failed to initialize splash screen: {e}")
            if hasattr(self, 'root') and self.root:
                self.root.destroy()
            raise
    
    def animate(self):
        # Check for timeout before continuing animation
        from datetime import timedelta, datetime, UTC
        timeout = timedelta(seconds=60)

        start_time = datetime.now(UTC)

        if start_time + timeout < datetime.now(UTC):
            logging.warning("Splash screen timeout reached, terminating")
            self.cleanup_and_exit()
            return

            
        # Display the current frame
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.frames[self.current_frame])
        
        # Get the duration for this frame
        duration = self.frame_durations[self.current_frame]
        
        # Move to next frame
        self.current_frame += 1
        
        # If we've reached the end of the frames
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
            self.current_loop += 1
            
            # If we've completed all loops, exit
            if self.loop_count > 0 and self.current_loop >= self.loop_count:
                return
        
        # Schedule the next frame
        self.root.after(duration, self.animate)
    
    def handle_signal(self, sig, frame):
        """Handle termination signals"""
        logging.info(f"Received signal {sig}, terminating splash screen")
        self.cleanup_and_exit()
    
    
    def cleanup_and_exit(self):
        """Clean up resources and exit gracefully"""
        logging.info("Cleaning up and exiting splash screen")
        if self.root:
            self.root.quit()
            self.root.destroy()
        sys.exit(0)
    
    def run(self):
        # Set up signal handlers for graceful exit
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        
        # Start the main loop
        try:
            self.root.mainloop()
        except Exception as e:
            logging.error(f"Error in splash screen main loop: {e}")
        finally:
            self.cleanup_and_exit()

def main(argv):
    try:
        # Check if required environment variables are set
        kivy_data_dir = os.getenv("KIVY_DATA_DIR")
        if not kivy_data_dir:
            logging.error("Error: KIVY_DATA_DIR environment variable is not set.")
            sys.exit(1)
        
        # Get the PNG file path
        png_path = os.path.join(kivy_data_dir, "images", "loading_animation.png")
        
        # Check if the file exists
        if not os.path.isfile(png_path):
            logging.error(f"Error: Loading animation file '{png_path}' not found.")
            sys.exit(1)
        
        # Check if the file is a PNG
        if not png_path.lower().endswith('.png'):
            logging.error(f"Error: File '{png_path}' does not have a .png extension.")
            sys.exit(1)
        
        # Set loop count
        loop_count = int(argv[1]) if len(argv) > 1 else 1
        # Create and run the viewer
        viewer = SplashScreen(png_path, loop_count)
        viewer.run()
        
    except Exception as e:
        logging.error(f"Error starting splash screen: {e}")
        sys.exit(1)

if __name__ == "__main__":
    freeze_support()
    Process(target=main, args=(sys.argv)).start()
