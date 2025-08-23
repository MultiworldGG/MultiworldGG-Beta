from __future__ import annotations
"""
SplashScreen

Run as a standalone script in a separate process    
that will be displayed when the application is launched.

This is used to display the loading animation while the
application is loading.
"""

__all__ = ('SplashScreen',)

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
        # Initialize the main window
        self.loop_done = False
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes("-transparent", "black")  # Enable transparency
        self.root.attributes("-topmost", True)  # Keep window on top
        
        # Load the animated PNG
        self.img = Image.open(png_path)
        
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
        for frame in ImageSequence.Iterator(self.img):
            # Convert to RGBA if not already
            if frame.mode != 'RGBA':
                frame = frame.convert('RGBA')
            
            # Get frame duration in milliseconds
            duration = int(frame.info.get('duration', 100))  # Default to 100ms if not specified
            
            photoframe = ImageTk.PhotoImage(frame)
            self.frames.append(photoframe)
            self.frame_durations.append(duration)
        
        # Start animation
        self.current_frame = 0
        self.animate()
        
        # Add termination monitoring
        self.termination_flag = False
        self.monitor_thread = None
    
    def animate(self):
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
        self.termination_flag = True
        self.cleanup_and_exit()
    
    def listen_for_termination(self):
        """Monitor for termination signals from the main application"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        flag_path = os.path.join(script_dir, "terminate_splash.flag")
        
        while not self.termination_flag:
            if os.path.exists(flag_path):
                logging.info("Termination flag detected")
                self.termination_flag = True
                self.cleanup_and_exit()
            time.sleep(0.1)
    
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
        
        # Start the termination monitor in a separate thread
        self.monitor_thread = threading.Thread(target=self.listen_for_termination)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        # Start the main loop
        try:
            self.root.mainloop()
        except Exception as e:
            logging.error(f"Error in splash screen main loop: {e}")
        finally:
            self.cleanup_and_exit()

def main():
   
    # Get the PNG file path
    png_path = os.path.join(os.getenv("KIVY_DATA_DIR"), "images", "loading_animation.png")
    
    # Check if the file exists
    if not os.path.isfile(png_path):
        logging.warning(f"Error: File '{png_path}' not found.")
        sys.exit(1)
    
    # Check if the file is a PNG
    if not png_path.lower().endswith('.png'):
        logging.warning("Warning: File does not have a .png extension. It may not be a PNG file.")
    
    # Set loop count
    loop_count = 1
    
    # Create and run the viewer
    viewer = SplashScreen(png_path, loop_count)
    viewer.run()

if __name__ == "__main__":
    main()
