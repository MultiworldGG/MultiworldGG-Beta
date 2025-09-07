"""
FileUtils - OS-specific file dialog implementations
Provides native file and directory selection dialogs for different platforms.
"""

import abc
import typing
import logging
import os
import subprocess
import queue
from abc import ABC, abstractmethod


class FileUtils(ABC):
    """Abstract base class for OS-specific file utilities."""
    
    @abstractmethod
    def open_file_input_dialog(self, title: str, filetypes: typing.Iterable[typing.Tuple[str, typing.Iterable[str]]], suggest: str = "") -> typing.Optional[str]:
        """Open a file selection dialog."""
        pass
    
    @abstractmethod
    def open_directory(self, title: str, suggest: str = "") -> typing.Optional[str]:
        """Open a directory selection dialog."""
        pass


class WinFileUtils(FileUtils):
    """Windows-specific file utilities using native dialogs."""
    
    def open_file_input_dialog(self, title: str, filetypes: typing.Iterable[typing.Tuple[str, typing.Iterable[str]]], suggest: str = "") -> typing.Optional[str]:
        """Windows native file dialog."""
        try:
            import win32gui
            import win32con
            from BaseUtils import user_path
            
            # Define file filters - Windows format uses null separators: "Description\0Pattern\0Description\0Pattern\0"
            filter_parts = []
            for text, ext in filetypes:
                # Convert extensions like ["*.txt", "*.log"] to "*.txt;*.log"
                ext_str = ";".join(ext)
                filter_parts.append(text + " (" + ext_str + ")")
                filter_parts.append(ext_str)
            # Add "All Files" as the last option (only if not already present)
            if not any('All Files' in part for part in filter_parts):
                filter_parts.append('All Files (*.*)')
                filter_parts.append('*.*')
            filter_str = "\0".join(filter_parts) + "\0"
            
            # Open the file dialog with minimal parameters
            try:
                fname, customfilter, flags = win32gui.GetOpenFileNameW(
                    Title=title,
                    Filter=filter_str,
                    FilterIndex=0
                )
                
                if fname:
                    print(f"Selected file: {fname}")
                    return fname
                else:
                    print("No file selected.")
                    return None
            except Exception as dialog_error:
                # Check if it's a cancellation error
                if "No error message is available" in str(dialog_error):
                    print("File dialog cancelled by user.")
                    return None
                else:
                    raise dialog_error
            
        except ImportError:
            logging.warning("win32gui not available, falling back to Kivy")
            return self._kivy_fallback_file(title, filetypes, suggest)
        except Exception as e:
            logging.error(f"Windows file dialog failed: {e}")
            return self._kivy_fallback_file(title, filetypes, suggest)
    
    def open_directory(self, title: str, suggest: str = "") -> typing.Optional[str]:
        """Windows native directory dialog."""
        try:
            from win32com.shell import shell, shellcon # type: ignore
            import win32gui
            from BaseUtils import user_path
            
            # Set up the browse info structure
            pidl, display_name, image_list = shell.SHBrowseForFolder(
                win32gui.GetDesktopWindow(),
                None,
                title,
                shellcon.BIF_RETURNONLYFSDIRS,
                None,
                None
            )
            
            if pidl:
                # Convert PIDL to path
                dirname = shell.SHGetPathFromIDList(pidl)
                print(f"Selected directory: {dirname}")
                return dirname
            else:
                print("No directory selected.")
                return None
                
        except ImportError:
            logging.warning("win32com not available, falling back to Kivy")
            return self._kivy_fallback_directory(title, suggest)
        except Exception as e:
            logging.error(f"Windows directory dialog failed: {e}")
            return self._kivy_fallback_directory(title, suggest)
    
    def _kivy_fallback_file(self, title: str, filetypes: typing.Iterable[typing.Tuple[str, typing.Iterable[str]]], suggest: str = "") -> typing.Optional[str]:
        """Kivy fallback for file selection."""
        from Utils import is_kivy_running
        if not is_kivy_running():
            return None
            
        try:
            from kivymd.app import MDApp
            from kivymd.uix.filemanager import MDFileManager
            
            result_queue = queue.Queue()
            
            def get_file_path(path: str):
                result_queue.put(path)
                file_manager.close()
                
            file_manager = MDFileManager(title=title, 
                                        select_path=get_file_path)
            
            # Check if any filetype contains image extensions
            has_images = any('png' in ext or 'jpg' in ext or 'jpeg' in ext or 'gif' in ext or 'bmp' in ext 
                            for _, extensions in filetypes 
                            for ext in extensions)
            file_manager.preview = has_images
            file_manager.selector = "file"
            file_manager.background_color_toolbar = MDApp.get_running_app().theme_cls.primaryColor
            file_manager.ext = [ext for (_, ext) in filetypes]
            file_manager.show(suggest)
            
            # Wait for result with timeout
            try:
                return result_queue.get(timeout=30)  # 30 second timeout
            except queue.Empty:
                return None
        except Exception as e:
            logging.error(f'Kivy file dialog fallback failed for "{title}": {e}')
            return None
    
    def _kivy_fallback_directory(self, title: str, suggest: str = "") -> typing.Optional[str]:
        """Kivy fallback for directory selection."""
        from Utils import is_kivy_running
        if not is_kivy_running():
            return None
            
        try:
            from kivymd.app import MDApp
            from kivymd.uix.filemanager import MDFileManager
            
            result_queue = queue.Queue()
            
            def get_directory_path(path: str):
                result_queue.put(path)
                file_manager.close()
                
            file_manager = MDFileManager(title=title, 
                                        select_path=get_directory_path)
            file_manager.selector = "folder"
            file_manager.background_color_toolbar = MDApp.get_running_app().theme_cls.primaryColor
            file_manager.show(suggest)
            
            # Wait for result with timeout
            try:
                return result_queue.get(timeout=30)  # 30 second timeout
            except queue.Empty:
                return None
        except Exception as e:
            logging.error(f'Kivy directory dialog fallback failed for "{title}": {e}')
            return None


class MacFileUtils(FileUtils):
    """macOS-specific file utilities using AppleScript."""
    
    def open_file_input_dialog(self, title: str, filetypes: typing.Iterable[typing.Tuple[str, typing.Iterable[str]]], suggest: str = "") -> typing.Optional[str]:
        """macOS native file dialog using AppleScript."""
        try:
            # Build AppleScript for file selection
            applescript = f'''
            tell application "System Events"
                set filePath to choose file with prompt "{title}"
                return POSIX path of filePath
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                file_path = result.stdout.strip()
                print(f"Selected file: {file_path}")
                return file_path
            else:
                print("No file selected.")
                return None
                
        except subprocess.TimeoutExpired:
            logging.warning("AppleScript file dialog timed out")
            return None
        except Exception as e:
            logging.error(f"AppleScript file dialog failed: {e}")
            return self._kivy_fallback_file(title, filetypes, suggest)
    
    def open_directory(self, title: str, suggest: str = "") -> typing.Optional[str]:
        """macOS native directory dialog using AppleScript."""
        try:
            # Build AppleScript for directory selection
            applescript = f'''
            tell application "System Events"
                set folderPath to choose folder with prompt "{title}"
                return POSIX path of folderPath
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                dir_path = result.stdout.strip()
                print(f"Selected directory: {dir_path}")
                return dir_path
            else:
                print("No directory selected.")
                return None
                
        except subprocess.TimeoutExpired:
            logging.warning("AppleScript directory dialog timed out")
            return None
        except Exception as e:
            logging.error(f"AppleScript directory dialog failed: {e}")
            return self._kivy_fallback_directory(title, suggest)
    
    def _kivy_fallback_file(self, title: str, filetypes: typing.Iterable[typing.Tuple[str, typing.Iterable[str]]], suggest: str = "") -> typing.Optional[str]:
        """Kivy fallback for file selection."""
        from Utils import is_kivy_running
        if not is_kivy_running():
            return None
            
        try:
            from kivymd.app import MDApp
            from kivymd.uix.filemanager import MDFileManager
            
            result_queue = queue.Queue()
            
            def get_file_path(path: str):
                result_queue.put(path)
                file_manager.close()
                
            file_manager = MDFileManager(title=title, 
                                        select_path=get_file_path)
            
            # Check if any filetype contains image extensions
            has_images = any('png' in ext or 'jpg' in ext or 'jpeg' in ext or 'gif' in ext or 'bmp' in ext 
                            for _, extensions in filetypes 
                            for ext in extensions)
            file_manager.preview = has_images
            file_manager.selector = "file"
            file_manager.background_color_toolbar = MDApp.get_running_app().theme_cls.primaryColor
            file_manager.ext = [ext for (_, ext) in filetypes]
            file_manager.show(suggest)
            
            # Wait for result with timeout
            try:
                return result_queue.get(timeout=30)  # 30 second timeout
            except queue.Empty:
                return None
        except Exception as e:
            logging.error(f'Kivy file dialog fallback failed for "{title}": {e}')
            return None
    
    def _kivy_fallback_directory(self, title: str, suggest: str = "") -> typing.Optional[str]:
        """Kivy fallback for directory selection."""
        from Utils import is_kivy_running
        if not is_kivy_running():
            return None
            
        try:
            from kivymd.app import MDApp
            from kivymd.uix.filemanager import MDFileManager
            
            result_queue = queue.Queue()
            
            def get_directory_path(path: str):
                result_queue.put(path)
                file_manager.close()
                
            file_manager = MDFileManager(title=title, 
                                        select_path=get_directory_path)
            file_manager.selector = "folder"
            file_manager.background_color_toolbar = MDApp.get_running_app().theme_cls.primaryColor
            file_manager.show(suggest)
            
            # Wait for result with timeout
            try:
                return result_queue.get(timeout=30)  # 30 second timeout
            except queue.Empty:
                return None
        except Exception as e:
            logging.error(f'Kivy directory dialog fallback failed for "{title}": {e}')
            return None


class LinuxFileUtils(FileUtils):
    """Linux-specific file utilities using native dialogs."""
    
    def open_file_input_dialog(self, title: str, filetypes: typing.Iterable[typing.Tuple[str, typing.Iterable[str]]], suggest: str = "") -> typing.Optional[str]:
        """Linux native file dialog using kdialog or zenity."""
        from shutil import which
        from Utils import _run_for_stdout
        
        # Try kdialog first
        kdialog = which("kdialog")
        if kdialog:
            k_filters = '|'.join((f'{text} (*{" *".join(ext)})' for (text, ext) in filetypes))
            return _run_for_stdout(kdialog, f"--title={title}", "--getopenfilename", suggest or ".", k_filters)
        
        # Try zenity
        zenity = which("zenity")
        if zenity:
            z_filters = (f'--file-filter={text} ({", ".join(ext)}) | *{" *".join(ext)}' for (text, ext) in filetypes)
            selection = (f"--filename={suggest}",) if suggest else ()
            return _run_for_stdout(zenity, f"--title={title}", "--file-selection", *z_filters, *selection)
        
        # Fallback to Kivy
        return self._kivy_fallback_file(title, filetypes, suggest)
    
    def open_directory(self, title: str, suggest: str = "") -> typing.Optional[str]:
        """Linux native directory dialog using kdialog or zenity."""
        from shutil import which
        from Utils import _run_for_stdout
        import os
        
        # Try kdialog first
        kdialog = which("kdialog")
        if kdialog:
            return _run_for_stdout(kdialog, f"--title={title}", "--getexistingdirectory",
                       os.path.abspath(suggest) if suggest else ".")
        
        # Try zenity
        zenity = which("zenity")
        if zenity:
            z_filters = ("--directory",)
            selection = (f"--filename={os.path.abspath(suggest)}/",) if suggest else ()
            return _run_for_stdout(zenity, f"--title={title}", "--file-selection", *z_filters, *selection)
        
        # Fallback to Kivy
        return self._kivy_fallback_directory(title, suggest)
    
    def _kivy_fallback_file(self, title: str, filetypes: typing.Iterable[typing.Tuple[str, typing.Iterable[str]]], suggest: str = "") -> typing.Optional[str]:
        """Kivy fallback for file selection."""
        from Utils import is_kivy_running
        if not is_kivy_running():
            return None
            
        try:
            from kivymd.app import MDApp
            from kivymd.uix.filemanager import MDFileManager
            
            result_queue = queue.Queue()
            
            def get_file_path(path: str):
                result_queue.put(path)
                file_manager.close()
                
            file_manager = MDFileManager(title=title, 
                                        select_path=get_file_path)
            
            # Check if any filetype contains image extensions
            has_images = any('png' in ext or 'jpg' in ext or 'jpeg' in ext or 'gif' in ext or 'bmp' in ext 
                            for _, extensions in filetypes 
                            for ext in extensions)
            file_manager.preview = has_images
            file_manager.selector = "file"
            file_manager.background_color_toolbar = MDApp.get_running_app().theme_cls.primaryColor
            file_manager.ext = [ext for (_, ext) in filetypes]
            file_manager.show(suggest)
            
            # Wait for result with timeout
            try:
                return result_queue.get(timeout=30)  # 30 second timeout
            except queue.Empty:
                return None
        except Exception as e:
            logging.error(f'Kivy file dialog fallback failed for "{title}": {e}')
            return None
    
    def _kivy_fallback_directory(self, title: str, suggest: str = "") -> typing.Optional[str]:
        """Kivy fallback for directory selection."""
        from Utils import is_kivy_running
        if not is_kivy_running():
            return None
            
        try:
            from kivymd.app import MDApp
            from kivymd.uix.filemanager import MDFileManager
            
            result_queue = queue.Queue()
            
            def get_directory_path(path: str):
                result_queue.put(path)
                file_manager.close()
                
            file_manager = MDFileManager(title=title, 
                                        select_path=get_directory_path)
            file_manager.selector = "folder"
            file_manager.background_color_toolbar = MDApp.get_running_app().theme_cls.primaryColor
            file_manager.show(suggest)
            
            # Wait for result with timeout
            try:
                return result_queue.get(timeout=30)  # 30 second timeout
            except queue.Empty:
                return None
        except Exception as e:
            logging.error(f'Kivy directory dialog fallback failed for "{title}": {e}')
            return None


class OtherFileUtils(FileUtils):
    """Cross-platform file utilities using Kivy (for mobile apps)."""
    
    def open_file_input_dialog(self, title: str, filetypes: typing.Iterable[typing.Tuple[str, typing.Iterable[str]]], suggest: str = "") -> typing.Optional[str]:
        """Kivy-based file dialog for mobile platforms."""
        from Utils import is_kivy_running
        if not is_kivy_running():
            logging.warning("Kivy not running, cannot show file dialog")
            return None
            
        try:
            from kivymd.app import MDApp
            from kivymd.uix.filemanager import MDFileManager
            
            result_queue = queue.Queue()
            
            def get_file_path(path: str):
                result_queue.put(path)
                file_manager.close()
                
            file_manager = MDFileManager(title=title, 
                                        select_path=get_file_path)
            
            # Check if any filetype contains image extensions
            has_images = any('png' in ext or 'jpg' in ext or 'jpeg' in ext or 'gif' in ext or 'bmp' in ext 
                            for _, extensions in filetypes 
                            for ext in extensions)
            file_manager.preview = has_images
            file_manager.selector = "file"
            file_manager.background_color_toolbar = MDApp.get_running_app().theme_cls.primaryColor
            file_manager.ext = [ext for (_, ext) in filetypes]
            file_manager.show(suggest)
            
            # Wait for result with timeout
            try:
                return result_queue.get(timeout=30)  # 30 second timeout
            except queue.Empty:
                return None
        except Exception as e:
            logging.error(f'Kivy file dialog failed for "{title}": {e}')
            return None
    
    def open_directory(self, title: str, suggest: str = "") -> typing.Optional[str]:
        """Kivy-based directory dialog for mobile platforms."""
        from Utils import is_kivy_running
        if not is_kivy_running():
            logging.warning("Kivy not running, cannot show directory dialog")
            return None
            
        try:
            from kivymd.app import MDApp
            from kivymd.uix.filemanager import MDFileManager
            
            result_queue = queue.Queue()
            
            def get_directory_path(path: str):
                result_queue.put(path)
                file_manager.close()
                
            file_manager = MDFileManager(title=title, 
                                        select_path=get_directory_path)
            file_manager.selector = "folder"
            file_manager.background_color_toolbar = MDApp.get_running_app().theme_cls.primaryColor
            file_manager.show(suggest)
            
            # Wait for result with timeout
            try:
                return result_queue.get(timeout=30)  # 30 second timeout
            except queue.Empty:
                return None
        except Exception as e:
            logging.error(f'Kivy directory dialog failed for "{title}": {e}')
            return None


class FileUtilsSingleton:
    """Singleton wrapper for FileUtils to provide static-like access."""
    
    _instance: typing.Optional[FileUtils] = None
    _initialized: bool = False
    
    def __new__(cls):
        if not hasattr(cls, '_singleton_instance'):
            cls._singleton_instance = super().__new__(cls)
        return cls._singleton_instance
    
    def __init__(self):
        if not self._initialized:
            import sys
            
            if sys.platform in ("win32", "cygwin", "msys"):
                self._instance = WinFileUtils()
            elif sys.platform == "darwin":
                self._instance = MacFileUtils()
            elif sys.platform.startswith("linux"):
                self._instance = LinuxFileUtils()
            else:
                self._instance = OtherFileUtils()
            
            self._initialized = True
    
    def open_file_input_dialog(self, title: str, filetypes: typing.Iterable[typing.Tuple[str, typing.Iterable[str]]], suggest: str = "") -> typing.Optional[str]:
        """Open a file selection dialog."""
        return self._instance.open_file_input_dialog(title, filetypes, suggest)
    
    def open_directory(self, title: str, suggest: str = "") -> typing.Optional[str]:
        """Open a directory selection dialog."""
        return self._instance.open_directory(title, suggest)


# Create the singleton instance
FileUtils = FileUtilsSingleton()
